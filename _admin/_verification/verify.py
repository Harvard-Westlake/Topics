#!/usr/bin/env python3
"""Curriculum consistency verifier for the Topics repo.

Checks that lessons, indexes, and curated modules all still point at things
that exist:

  1. Every relative link in every .md file resolves to a real file/folder
  2. Every topic folder has LESSONS.md + README.md, LESSONS.md paths exist,
     and every lesson folder is listed in LESSONS.md
  3. Lesson READMEs contain a Check for Understanding section and link ASSIGNMENT.md
     when one exists; every ASSIGNMENT.md links back to its lesson README
  4. Every topic is listed in the root README
  5. Every _modules/*.json is valid: slug matches filename, lessons and
     review references exist, titles match LESSONS.md, and the generated
     _admin/_lessonplans/<slug>.md summary is in sync

Usage:
    python3 _admin/_verification/verify.py          # check, exit 1 on errors
    python3 _admin/_verification/verify.py --fix    # also regenerate lesson plans

Runs in CI on every push (.github/workflows/verify.yml).
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = ROOT / "_modules"
LESSONPLANS_DIR = ROOT / "_admin" / "_lessonplans"

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ── Repo model ─────────────────────────────────────────────────────────────────

def content_topics():
    """Top-level topic folders (student-facing modules)."""
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_")) and (d / "README.md").exists()
    )


def lesson_folders(topic):
    """Lesson subfolders of a topic (have a README.md; Docs/ is not a lesson)."""
    return sorted(
        d for d in topic.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_"))
        and d.name != "Docs" and (d / "README.md").exists()
    )


LESSONS_ROW = re.compile(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(?:\[(.+?)\]\((.+?)\))?\s*\|?")


def parse_lessons_md(topic):
    """Rows of a topic's LESSONS.md as [{day_raw, title, path}] (path sans slash)."""
    rows = []
    lessons_file = topic / "LESSONS.md"
    if not lessons_file.exists():
        return rows
    for line in lessons_file.read_text().splitlines():
        m = LESSONS_ROW.match(line)
        if not m:
            continue
        day_raw, title = m.group(1).strip(), m.group(2).strip()
        if title.startswith("---") or title.lower() in ("day", "lesson"):
            continue
        path = (m.group(4) or m.group(3) or "").rstrip("/")
        rows.append({"day_raw": day_raw, "title": title, "path": path})
    return rows


# ── 1. Relative link resolution across all markdown ───────────────────────────

MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_SRC = re.compile(r"""src=["']([^"']+)["']""")
FENCED_CODE = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
PRE_BLOCK = re.compile(r"<pre>.*?</pre>", re.DOTALL)


def check_links():
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        rel_md = md.relative_to(ROOT)
        # Format examples inside code blocks aren't real links — skip them
        text = md.read_text()
        for pattern in (FENCED_CODE, PRE_BLOCK, INLINE_CODE):
            text = pattern.sub("", text)
        targets = MD_LINK.findall(text) + HTML_SRC.findall(text)
        for raw in targets:
            target = unquote(raw.split("#")[0])
            if not target or raw.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target.startswith("/"):
                err(f"{rel_md}: absolute link '{raw}' — use a relative path")
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                err(f"{rel_md}: broken link '{raw}'")


# ── 2–4. Topic and lesson structure ────────────────────────────────────────────

def check_structure():
    root_readme = (ROOT / "README.md").read_text()
    for topic in content_topics():
        name = topic.name
        if not (topic / "LESSONS.md").exists():
            err(f"{name}/: missing LESSONS.md")
        if f"]({name}/)" not in root_readme:
            err(f"README.md: topic '{name}' is not linked in the root README")

        listed = {r["path"] for r in parse_lessons_md(topic) if r["path"]}
        actual = {d.name for d in lesson_folders(topic)}
        for missing in sorted(actual - listed):
            err(f"{name}/LESSONS.md: lesson folder '{missing}/' is not listed")
        for ghost in sorted(listed - actual):
            err(f"{name}/LESSONS.md: listed path '{ghost}/' does not exist")

        for lesson in lesson_folders(topic):
            readme = (lesson / "README.md").read_text()
            rel = lesson.relative_to(ROOT)
            if "Check for Understanding" not in readme:
                err(f"{rel}/README.md: missing Check for Understanding section")
            has_assignment = (lesson / "ASSIGNMENT.md").exists()
            links_assignment = "](ASSIGNMENT.md)" in readme
            if has_assignment and not links_assignment:
                err(f"{rel}/README.md: ASSIGNMENT.md exists but is not linked")
            if links_assignment and not has_assignment:
                err(f"{rel}/README.md: links ASSIGNMENT.md but the file does not exist")
            if has_assignment:
                assignment_paras = (lesson / "ASSIGNMENT.md").read_text().split("\n\n", 2)
                lesson_link_para = assignment_paras[1] if len(assignment_paras) > 1 else ""
                if "](README.md)" not in lesson_link_para:
                    err(f"{rel}/ASSIGNMENT.md: missing the *Lesson: [...](README.md)* "
                        "link under the title (see CLAUDE.md \"ASSIGNMENT.md format\")")


# ── 5. Curated module JSONs ────────────────────────────────────────────────────

REQUIRED_KEYS = ("name", "slug", "topic_names", "assignments")

# A review file's display name is the concept it covers, not its filename —
# parsed from its own "# Review — <Concept>" title (see _instructions/ review
# file format). An ordered set (review-day-1.md, review-day-2.md, ...) bakes
# ", Day N" into that title to keep each file's title unique on its own; here
# that suffix is stripped back off to find the shared topic underneath it.
REVIEW_TITLE_RE = re.compile(r"^#\s*Review\s*[—-]\s*(.+?)\s*$", re.MULTILINE)
REVIEW_DAY_SUFFIX_RE = re.compile(r",?\s*Day\s+(\d+)\s*$", re.IGNORECASE)


def review_file_title(path):
    """The concept a review file covers, from its own '# Review — X' heading."""
    try:
        text = path.read_text()
    except OSError:
        return path.stem
    m = REVIEW_TITLE_RE.search(text)
    return m.group(1).strip() if m else path.stem


def review_topic_and_day(title):
    """Split a review title into (base topic, explicit day number or None)."""
    m = REVIEW_DAY_SUFFIX_RE.search(title)
    if m:
        return REVIEW_DAY_SUFFIX_RE.sub("", title).strip(), int(m.group(1))
    return title, None


def review_labels(review_dir, filenames):
    """Display label per review filename: the topic it covers, numbered only
    when that same topic recurs across more than one file in `filenames`."""
    parsed = {f: review_topic_and_day(review_file_title(review_dir / f)) for f in filenames}
    counts = {}
    for topic, _ in parsed.values():
        counts[topic] = counts.get(topic, 0) + 1
    next_seq, labels = {}, {}
    for f in filenames:
        topic, day = parsed[f]
        if counts[topic] <= 1:
            labels[f] = topic
        elif day is not None:
            labels[f] = f"{topic} {day}"
        else:
            next_seq[topic] = next_seq.get(topic, 0) + 1
            labels[f] = f"{topic} {next_seq[topic]}"
    return labels


def review_label_for(review_file_path):
    """Display label for one review markdown file, disambiguated against its
    siblings in the same review/ folder (see `review_labels`)."""
    review_dir = review_file_path.parent
    if not review_dir.is_dir():
        return review_file_path.stem
    siblings = sorted(f.name for f in review_dir.iterdir()
                       if f.is_file() and f.suffix == ".md")
    return review_labels(review_dir, siblings).get(review_file_path.name, review_file_path.stem)


def day_label(unit, a):
    base = f"{unit}.{a['day']}" if unit is not None else str(a["day"])
    dur = a.get("duration", 1)
    if dur == 0.5:                      # half day: unit.day.sub (.0 = first of the day)
        return f"{base}.{a.get('sub') or 0}"
    return f"{base} · {dur}d" if dur > 1 else base


def generate_lessonplan(mod):
    """Readable markdown summary of a curated module JSON (generated file)."""
    slug = mod["slug"]
    unit = mod.get("unit_number")
    lines = [
        f"# Module — {mod['name']}",
        "",
        f"*Generated from [`_modules/{slug}.json`](../../_modules/{slug}.json) — do not edit by hand."
        " Regenerate with `python3 _admin/_verification/verify.py --fix` or by saving from the planner UI.*",
        "",
    ]
    meta = []
    if unit is not None:
        meta.append(f"**Unit {unit}**")
    if mod.get("points_per_assignment") is not None:
        meta.append(f"{mod['points_per_assignment']} pts/assignment")
    if mod.get("scale_factor") is not None:
        meta.append(f"scale ×{mod['scale_factor']}")
    if mod.get("updated"):
        meta.append(f"updated {mod['updated']}")
    if meta:
        lines += [" · ".join(meta), ""]
    if mod.get("description"):
        lines += [mod["description"], ""]
    lines += ["| Day | Lesson | Source | Review |", "|---|---|---|---|"]
    for a in mod.get("assignments", []):
        if a.get("placeholder"):
            src_cell = "*placeholder — not yet filled in*"
        else:
            src = f"{a['_module']}/{a['path']}"
            src_cell = f"[{src}](../../{src}/)"
        rev = a.get("review")
        if rev:
            rev_file = ROOT / rev["module"] / rev["path"] / "review" / rev["file"]
            label = review_label_for(rev_file) if rev_file.exists() else rev["file"].removesuffix(".md")
            rev_cell = f"[{label}](../../{rev['module']}/{rev['path']}/review/{rev['file']})"
        else:
            rev_cell = "—"
        lines.append(f"| {day_label(unit, a)} | {a['title']} | {src_cell} | {rev_cell} |")
    lines.append("")
    return "\n".join(lines)


def check_modules(fix=False):
    if not MODULES_DIR.exists():
        return
    for jf in sorted(MODULES_DIR.glob("*.json")):
        rel = jf.relative_to(ROOT)
        try:
            mod = json.loads(jf.read_text())
        except json.JSONDecodeError as e:
            err(f"{rel}: invalid JSON — {e}")
            continue
        for key in REQUIRED_KEYS:
            if key not in mod:
                err(f"{rel}: missing required key '{key}'")
        if mod.get("slug") != jf.stem:
            err(f"{rel}: slug '{mod.get('slug')}' does not match filename '{jf.stem}'")
        for t in mod.get("topic_names", []):
            if not (ROOT / t).is_dir():
                err(f"{rel}: topic_names entry '{t}' is not a folder in the repo")

        for a in mod.get("assignments", []):
            if not a.get("placeholder"):
                label = f"{a.get('_module')}/{a.get('path')}"
                lesson_dir = ROOT / a.get("_module", "") / a.get("path", "")
                if not (lesson_dir / "README.md").exists():
                    err(f"{rel}: assignment '{a.get('title')}' points at missing lesson '{label}/'")
                    continue
                if not (lesson_dir / "ASSIGNMENT.md").exists():
                    warn(f"{rel}: lesson '{label}/' has no ASSIGNMENT.md — the Canvas assignment body will be empty")
                rows = parse_lessons_md(ROOT / a["_module"])
                row = next((r for r in rows if r["path"] == a["path"]), None)
                if row is None:
                    warn(f"{rel}: lesson '{label}/' is not listed in {a['_module']}/LESSONS.md")
                elif row["title"] != a["title"]:
                    warn(f"{rel}: title '{a['title']}' drifted from LESSONS.md ('{row['title']}') — resave from planner")
            rev = a.get("review")
            if rev:
                rev_file = ROOT / rev["module"] / rev["path"] / "review" / rev["file"]
                if not rev_file.exists():
                    err(f"{rel}: review reference '{rev['module']}/{rev['path']}/review/{rev['file']}' does not exist")

        # Generated lesson plan must be in sync
        if all(k in mod for k in REQUIRED_KEYS):
            plan_file = LESSONPLANS_DIR / f"{jf.stem}.md"
            expected = generate_lessonplan(mod)
            if fix:
                LESSONPLANS_DIR.mkdir(parents=True, exist_ok=True)
                if not plan_file.exists() or plan_file.read_text() != expected:
                    plan_file.write_text(expected)
                    print(f"  regenerated {plan_file.relative_to(ROOT)}")
            elif not plan_file.exists():
                err(f"{rel}: missing generated plan _admin/_lessonplans/{jf.stem}.md — run verify.py --fix")
            elif plan_file.read_text() != expected:
                err(f"_admin/_lessonplans/{jf.stem}.md is stale — run verify.py --fix")

    # Orphaned lesson plans (module JSON was deleted or renamed)
    if LESSONPLANS_DIR.exists():
        for plan in sorted(LESSONPLANS_DIR.glob("*.md")):
            if plan.name != "README.md" and not (MODULES_DIR / f"{plan.stem}.json").exists():
                warn(f"_admin/_lessonplans/{plan.name}: no matching _modules/{plan.stem}.json (orphaned — delete it)")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    fix = "--fix" in sys.argv
    check_links()
    check_structure()
    check_modules(fix=fix)

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) "
          f"across {len(content_topics())} topics and "
          f"{len(list(MODULES_DIR.glob('*.json'))) if MODULES_DIR.exists() else 0} curated module(s).")
    if errors:
        sys.exit(1)
    print("Curriculum verified: all links and module references resolve.")


if __name__ == "__main__":
    main()
