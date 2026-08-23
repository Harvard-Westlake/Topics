#!/usr/bin/env python3
"""HW Course Hub — one app for Canvas courses, year schedules, and module planning.

Serves a tabbed UI at http://127.0.0.1:5050 :
  Courses        — Canvas course list, grades, and the Create Module drawer
  Year Schedule  — per-teacher drag-and-drop year plans (_admin/_schedules/<name>.json)
  Module Planner — create/edit curated modules (_modules/<slug>.json) with file editor
  Module Editor  — edit the topic folders themselves (lessons, activities, reviews,
                   uploads) with structural ops that keep every index file in step
  Syllabus       — renders the repo's live SYLLABUS.md

The Topics repo (this repo) is the source of truth for all content. The private
sibling Admin repo holds final exams; syncing a test/final day to Canvas creates a
placeholder assignment only — exam content never leaves the private repo.

Per-teacher setup:
    cp .env.example .env          # at the repo root, then paste YOUR Canvas token
    pip3 install -r _admin/_hub/requirements.txt
    python3 _admin/_hub/server.py

The app runs without a token too — the Planner and Schedule tabs are fully
credential-free; only Canvas calls need HUB_TOKEN.
"""
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import requests, os, sys, json, time, re, html, shutil
import markdown as md_lib
from icsimport import compress_calendar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # the Topics repo root

# Per-teacher secrets: repo-root .env first, then legacy ../Admin/.env fallback
load_dotenv(ROOT / ".env")
load_dotenv(ROOT.parent / "Admin" / ".env")

app    = Flask(__name__, static_folder=str(HERE / "static"), static_url_path="/static")
TOKEN  = os.environ.get("HUB_TOKEN")
BASE   = "https://hw.instructure.com/api/v1"
CACHE  = HERE / ".cache"                    # gitignored — contains student data
TOPICS = ROOT

SCHEDULES_DIR = ROOT / "_admin" / "_schedules"
CALENDARS_DIR = SCHEDULES_DIR / "calendars"   # imported .ics class calendars
FINALS = Path(os.environ.get("FINALS_DIR") or (ROOT.parent / "Admin" / "finals"))
MODULES_DIR = ROOT / "_modules"

COURSE_TTL      = 60 * 60 * 24
SUBRESOURCE_TTL = 60 * 60

GITHUB_REPO   = "Harvard-Westlake/Topics"
GITHUB_BRANCH = "main"
GITHUB_RAW    = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"
GITHUB_BLOB   = f"https://github.com/{GITHUB_REPO}/blob/{GITHUB_BRANCH}"

# Repo tooling shared with the verifier and the standalone planner
sys.path.insert(0, str(ROOT / "_admin" / "_verification"))
sys.path.insert(0, str(ROOT / "_admin" / "_coursePlannerUI"))
from verify import (generate_lessonplan, LESSONPLANS_DIR,               # noqa: E402
                    MD_LINK, HTML_SRC, FENCED_CODE, INLINE_CODE, PRE_BLOCK,
                    review_labels, review_label_for)
from mdrender import (md_to_html as planner_md_to_html,                 # noqa: E402
                      review_block as planner_review_block,
                      ENGINE as PLANNER_ENGINE)

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _\-]*$")
FILE_RE = re.compile(r"^(review/|activities/|milestones/)?[A-Za-z0-9._-]+\.md$|^demos/[A-Za-z0-9._-]+\.html$")

# ── Markdown helpers (Canvas upload rendering) ─────────────────────────────────

def _resolve_path(base_path, rel):
    """Resolve a relative path against a base directory path."""
    parts = base_path.rstrip("/").split("/") if base_path else []
    for seg in rel.split("/"):
        if seg == "..":
            parts = parts[:-1] if parts else []
        elif seg and seg != ".":
            parts.append(seg)
    return "/".join(parts)

# LaTeX math: GitHub renders $$...$$ and $...$ natively; Canvas's MathJax only
# renders \(...\) inline and $$...$$ display — single-dollar math never renders.
# Math is stashed before markdown conversion (which would mangle _ and * inside
# formulas), inline delimiters become \(...\), and the raw LaTeX is restored
# HTML-escaped afterward. Escaped dollars (\$) become literal $, as on GitHub.
# Must stay in lockstep with ../_coursePlannerUI/mdrender.py.

_FENCED_CODE_RE = re.compile(r"```[\s\S]*?```")
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_INLINE_MATH_RE = re.compile(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$(?!\$)")

def _extract_math(text):
    """Replace math with inert placeholders; return (text, stash)."""
    code = []

    def stash_code(m):
        code.append(m.group(0))
        return f"«code{len(code) - 1}»"

    # hide code first so $ inside fences/spans is never mistaken for math
    text = _FENCED_CODE_RE.sub(stash_code, text)
    text = _INLINE_CODE_RE.sub(stash_code, text)

    math = []

    def stash_display(m):
        math.append(("$$", m.group(1)))
        return f"«math{len(math) - 1}»"

    def stash_inline(m):
        math.append((r"\(", m.group(1)))
        return f"«math{len(math) - 1}»"

    text = _DISPLAY_MATH_RE.sub(stash_display, text)
    text = _INLINE_MATH_RE.sub(stash_inline, text)
    text = text.replace(r"\$", "$")
    # put code back so the renderer sees real fences and spans
    text = re.sub(r"«code(\d+)»", lambda m: code[int(m.group(1))], text)
    return text, math

def _restore_math(rendered, math):
    def put(m):
        kind, body = math[int(m.group(1))]
        body = html.escape(body, quote=False)
        if kind == "$$":
            return f"$${body}$$"
        return f"\\({body}\\)"

    return re.sub(r"«math(\d+)»", put, rendered)

# GFM task-list checkboxes: python-markdown's "tables"/"fenced_code" extensions
# don't render `- [ ]` as a real checkbox, so it shows up as literal "[ ]" text
# in the Canvas-fidelity preview and on Canvas itself. Rewrite the marker to an
# inline, disabled checkbox before markdown conversion — GitHub still renders
# the untouched .md source with its own native task-list support.
# Must stay in lockstep with ../_coursePlannerUI/mdrender.py.
_TASKLIST_RE = re.compile(r'^(\s*[-*])\s\[([ xX])\]\s+', re.MULTILINE)

def _rewrite_tasklist(m):
    checked = " checked" if m.group(2).lower() == "x" else ""
    return f'{m.group(1)} <input type="checkbox" disabled{checked}> '

# Centered title blocks (`<div align="center">` — see CLAUDE.md "Title format").
# GitHub's CommonMark renderer ends a raw HTML block at the first blank line
# after the opening tag, so the "# Title" / subtitle / label lines inside are
# parsed as normal markdown. python-markdown has no such rule: it swallows the
# whole <div>...</div> as one opaque raw block and never parses the markdown
# inside it, so titles rendered literally as "# Title" instead of a heading.
# Pre-render just the inner markdown so this matches what GitHub shows.
# Must stay in lockstep with ../_coursePlannerUI/mdrender.py.
_TITLE_DIV_RE = re.compile(r'^<div align="center">\n\n(.*?)\n\n</div>[ \t]*$', re.MULTILINE | re.DOTALL)

def _rewrite_title_divs(text):
    def render_block(m):
        inner_html = md_lib.markdown(m.group(1), extensions=["tables", "fenced_code", "toc"])
        return f'<div align="center">\n\n{inner_html}\n\n</div>'
    return _TITLE_DIV_RE.sub(render_block, text)

def md_to_html(text, base_path=""):
    """Convert markdown to HTML with relative links rewritten to absolute GitHub URLs."""
    def rewrite_img(m):
        alt, path = m.group(1), m.group(2)
        if path.startswith(("http://", "https://")):
            return m.group(0)
        return f'![{alt}]({GITHUB_RAW}/{_resolve_path(base_path, path)})'

    def rewrite_link(m):
        text, path = m.group(1), m.group(2)
        if path.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        return f'[{text}]({GITHUB_BLOB}/{_resolve_path(base_path, path)})'

    def rewrite_html_src(m):
        attr, path = m.group(1), m.group(2)
        if path.startswith(("http://", "https://", "data:")):
            return m.group(0)
        return f'{attr}="{GITHUB_RAW}/{_resolve_path(base_path, path)}"'

    text, math = _extract_math(text)
    text = _TASKLIST_RE.sub(_rewrite_tasklist, text)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', rewrite_img, text)
    text = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', rewrite_link, text)
    # raw HTML <img src=""> / <source srcset=""> (e.g. light/dark logo <picture> blocks)
    text = re.sub(r'(src|srcset)="([^"]+)"', rewrite_html_src, text)
    text = _rewrite_title_divs(text)
    # "toc" only for its side effect of stamping id="..." on headings so that
    # #anchor links (a lesson's own TOC, our cross-lesson link back to it)
    # resolve once this HTML lands in Canvas — we never insert a [TOC] marker.
    return _restore_math(md_lib.markdown(text, extensions=["tables", "fenced_code", "toc"]), math)

def review_block_html(rev_html):
    """Wrap rendered review markdown in the purple callout used on Canvas."""
    return ('<div style="background:#f6f8fa;border-left:4px solid #8957e5;'
            'padding:12px 16px;margin-bottom:20px;border-radius:0 6px 6px 0">'
            '<p style="font-weight:600;color:#8957e5;margin:0 0 8px 0">&#9997;&nbsp;Review</p>'
            + rev_html + '</div>')

def _lesson_readme_html(module_dir, lesson_path):
    """Collapsible <details> block with the day's README, so a Canvas
    assignment can show full lesson context without the student leaving
    Canvas. Native HTML disclosure widget — no JS, survives Canvas's HTML
    sanitization. Complements (doesn't replace) the plain README.md link
    every ASSIGNMENT.md opens with (see CLAUDE.md "ASSIGNMENT.md format")."""
    if not (module_dir and lesson_path):
        return None
    rf = TOPICS / module_dir / lesson_path / "README.md"
    if not rf.exists():
        return None
    return ('<details style="background:#f6f8fa;border:1px solid #d0d7de;'
            'border-radius:6px;margin-bottom:20px;padding:10px 16px">'
            '<summary style="cursor:pointer;font-weight:600;color:#57606a">'
            '&#128214;&nbsp;View the lesson for this assignment</summary>'
            '<div style="margin-top:12px">'
            + md_to_html(rf.read_text(), f"{module_dir}/{lesson_path}")
            + '</div></details>')

# ── Canvas helpers ─────────────────────────────────────────────────────────────

def create_canvas_page(course_id, module_id, name, body_html):
    """Create an unpublished Canvas wiki page and link it into a module. Used by
    'page' placeholders — an in-class day with content but no assignment/homework."""
    pr = requests.post(f"{BASE}/courses/{course_id}/pages", headers=hdrs(),
                       json={"wiki_page": {"title": name, "body": body_html,
                                           "published": False}})
    if not pr.ok:
        return None, pr.text
    page_url = pr.json().get("url")
    linked = False
    if module_id:
        mr = requests.post(f"{BASE}/courses/{course_id}/modules/{module_id}/items", headers=hdrs(),
                           json={"module_item": {"title": name, "type": "Page",
                                                 "page_url": page_url}})
        linked = mr.ok
    return {"name": name, "page_url": page_url, "linked": linked, "page": True}, None

def no_token():
    """503 response when a Canvas route is hit without a configured token."""
    if TOKEN:
        return None
    return jsonify({"error": "No HUB_TOKEN configured — copy .env.example to .env "
                             "at the repo root and paste your Canvas token"}), 503

def hdrs():
    return {"Authorization": f"Bearer {TOKEN}"}

def canvas_paged(path, params=None):
    results, url, p = [], BASE + path, dict(params or {})
    p.setdefault("per_page", 100)
    while url:
        r = requests.get(url, headers=hdrs(), params=p)
        r.raise_for_status()
        results.extend(r.json())
        url, p = None, {}
        for part in r.headers.get("Link", "").split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
    return results

# ── Cache helpers ──────────────────────────────────────────────────────────────

def cache_path(name):
    CACHE.mkdir(exist_ok=True)
    return CACHE / f"{name}.json"

def cache_read(name):
    p = cache_path(name)
    if not p.exists():
        return None, None
    d = json.loads(p.read_text())
    return d.get("data"), d.get("fetched_at")

def cache_write(name, data):
    cache_path(name).write_text(json.dumps({"fetched_at": time.time(), "data": data}))
    return data

def cached(name, ttl, fetch_fn):
    data, fetched_at = cache_read(name)
    stale = fetched_at is None or (time.time() - fetched_at) > ttl
    source = "cache"
    if stale:
        try:
            data       = cache_write(name, fetch_fn())
            source     = "live"
            fetched_at = time.time()
        except Exception:
            if data is None:
                raise
            source = "cache-fallback"
    return data, source, fetched_at

def year_key(c):
    n = c.get("name", "")
    return (0, n.split(" :: ")[0]) if " :: " in n else (1, "")

# ── Courses / favorites ────────────────────────────────────────────────────────

@app.route("/api/courses")
def api_courses():
    err = no_token()
    if err:
        return err
    force = request.args.get("refresh") == "1"
    def fetch():
        # Both states: unpublished courses (next year's shells) are exactly the
        # ones being set up. include[]=concluded marks term-ended (read-only)
        # courses so the UI can block them as sync targets.
        return sorted(
            canvas_paged("/courses", {"enrollment_type": "teacher",
                                      "state[]": ["available", "unpublished"],
                                      "include[]": "concluded"}),
            key=year_key, reverse=True)
    if force:
        try:
            data = cache_write("courses", fetch())
            return jsonify({"courses": data, "source": "live", "fetched_at": time.time()})
        except Exception as e:
            data, fetched_at = cache_read("courses")
            if data:
                return jsonify({"courses": data, "source": "cache-fallback",
                                "fetched_at": fetched_at, "error": str(e)})
            return jsonify({"error": str(e)}), 502
    data, source, fetched_at = cached("courses", COURSE_TTL, fetch)
    return jsonify({"courses": data, "source": source, "fetched_at": fetched_at})

@app.route("/api/favorites")
def api_favorites():
    err = no_token()
    if err:
        return err
    force = request.args.get("refresh") == "1"
    def fetch():
        return [c["id"] for c in canvas_paged("/users/self/favorites/courses")]
    if force:
        try:
            ids = cache_write("favorites", fetch())
            return jsonify({"favorite_ids": ids, "source": "live"})
        except Exception as e:
            ids, _ = cache_read("favorites")
            if ids:
                return jsonify({"favorite_ids": ids, "source": "cache-fallback", "error": str(e)})
            return jsonify({"error": str(e)}), 502
    ids, source, fetched_at = cached("favorites", COURSE_TTL, fetch)
    return jsonify({"favorite_ids": ids, "source": source, "fetched_at": fetched_at})

# ── Per-course sub-resources ───────────────────────────────────────────────────

@app.route("/api/courses/<int:course_id>/assignments")
def api_assignments(course_id):
    err = no_token()
    if err:
        return err
    def fetch():
        rows = canvas_paged(f"/courses/{course_id}/assignments", {"order_by": "due_at"})
        return [{"id": a["id"], "name": a["name"], "due_at": a.get("due_at"),
                 "points": a.get("points_possible"), "html_url": a.get("html_url")} for a in rows]
    data, source, fetched_at = cached(f"assignments_{course_id}", SUBRESOURCE_TTL, fetch)
    return jsonify({"assignments": data, "source": source, "fetched_at": fetched_at})

@app.route("/api/courses/<int:course_id>/modules")
def api_modules(course_id):
    err = no_token()
    if err:
        return err
    def fetch():
        rows = canvas_paged(f"/courses/{course_id}/modules", {"include[]": "items_count"})
        return [{"id": m["id"], "name": m["name"], "items_count": m.get("items_count", 0),
                 "published": m.get("published"), "position": m.get("position")} for m in rows]
    data, source, fetched_at = cached(f"modules_{course_id}", SUBRESOURCE_TTL, fetch)
    return jsonify({"modules": data, "source": source, "fetched_at": fetched_at})

@app.route("/api/courses/<int:course_id>/grades")
def api_grades(course_id):
    err = no_token()
    if err:
        return err
    def fetch():
        rows = canvas_paged(f"/courses/{course_id}/enrollments",
                            {"type[]": "StudentEnrollment", "state[]": "active"})
        students = [{"name": e["user"]["name"],
                     "current_score": e.get("grades", {}).get("current_score"),
                     "final_score":   e.get("grades", {}).get("final_score")} for e in rows]
        scores = [s["current_score"] for s in students if s["current_score"] is not None]
        return {"students": sorted(students, key=lambda s: s["name"]),
                "count": len(students),
                "avg_current": round(sum(scores)/len(scores), 1) if scores else None}
    data, source, fetched_at = cached(f"grades_{course_id}", SUBRESOURCE_TTL, fetch)
    return jsonify({"grades": data, "source": source, "fetched_at": fetched_at})

# ── Module creation ────────────────────────────────────────────────────────────

@app.route("/api/courses/<int:course_id>/next-unit")
def api_next_unit(course_id):
    err = no_token()
    if err:
        return err
    modules = canvas_paged(f"/courses/{course_id}/modules")
    nums = [int(m.group(1)) for m in
            (re.match(r"[Uu]nit\s+(\d+)", mod.get("name", "")) for mod in modules) if m]
    return jsonify({"next_unit": max(nums) + 1 if nums else 0,
                    "existing_count": len(modules)})

@app.route("/api/courses/<int:course_id>/create-module", methods=["POST"])
def api_create_module(course_id):
    err = no_token()
    if err:
        return err
    body        = request.get_json()
    unit_num    = int(body["unit_number"])
    assignments = body["assignments"]
    start_date  = body.get("start_date")
    points      = body.get("points_per_assignment", 10)
    topics      = body.get("topic_names", [])

    if len(topics) == 1:
        mod_name = f"Unit {unit_num}: {topics[0]}"
    elif len(topics) == 2:
        mod_name = f"Unit {unit_num}: {topics[0]} and {topics[1]}"
    elif len(topics) >= 3:
        mod_name = f"Unit {unit_num}: {', '.join(topics[:-1])}, and {topics[-1]}"
    else:
        mod_name = f"Unit {unit_num}"

    def due_at(day, duration=1):
        if not start_date:
            return None
        # day is 1-indexed; assignment spans day..day+duration-1
        # due at 23:59 on the last day → offset = (day-1) + (duration-1)
        offset = int(day) - 1 + int(duration) - 1
        d = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=offset)
        return d.replace(hour=23, minute=59, second=0, tzinfo=timezone.utc).isoformat()

    def unlock_at(day):
        if not start_date:
            return None
        offset = int(day) - 1
        d = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=offset)
        return d.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc).isoformat()

    mod_res = requests.post(f"{BASE}/courses/{course_id}/modules", headers=hdrs(),
                            json={"module": {"name": mod_name, "position": 1}})
    if not mod_res.ok:
        hint = (" — Canvas returns this for concluded (term-ended) courses, which are "
                "read-only; pick a current-year course"
                if mod_res.status_code == 401 else "")
        return jsonify({"error": f"Module creation failed: {mod_res.text}{hint}"}), 502
    module_id = mod_res.json()["id"]

    results, errors = [], []
    for a in assignments:
        if a.get("placeholder"):
            # 'page' → Canvas Page (content, no assignment/homework);
            # 'test' → reserved day number for manual test placement;
            # plain  → not yet filled in. Only 'page' creates anything.
            if a.get("kind") == "page":
                pname = f"{unit_num}.{a['day']}: {a['title']}"
                parts = []
                if a.get("review_markdown"):
                    parts.append(review_block_html(md_to_html(a["review_markdown"])))
                parts.append("<p>In-class day — no assignment due.</p>")
                page, perr = create_canvas_page(course_id, module_id, pname, "\n".join(parts))
                if perr:
                    errors.append({"name": pname, "error": perr})
                else:
                    results.append(page)
            continue
        day      = a["day"]
        duration = a.get("duration", 1)
        name     = f"{unit_num}.{day}: {a['title']}"

        # Build HTML description
        html_parts = []
        mod_dir  = a.get("_module", "")
        lesson_p = a.get("path", "")

        # Lesson context (collapsible, so the student can pull up the day's
        # README without leaving Canvas)
        readme_html = _lesson_readme_html(mod_dir, lesson_p)
        if readme_html:
            html_parts.append(readme_html)

        # Review section (rendered markdown)
        if a.get("review_markdown"):
            html_parts.append(review_block_html(md_to_html(a["review_markdown"])))

        # Assignment content from ASSIGNMENT.md
        if mod_dir and lesson_p:
            assign_file = TOPICS / mod_dir / lesson_p / "ASSIGNMENT.md"
            if assign_file.exists():
                assign_html = md_to_html(assign_file.read_text(), f"{mod_dir}/{lesson_p}")
                html_parts.append(assign_html)

        description = "\n".join(html_parts)

        asgn_body = {"assignment": {
            "name": name,
            "points_possible": points,
            "submission_types": ["online_upload", "online_text_entry"],
            "description": description,
            "published": False,
        }}
        if due_at(day, duration):
            asgn_body["assignment"]["due_at"]    = due_at(day, duration)
            asgn_body["assignment"]["unlock_at"] = unlock_at(day)

        ar = requests.post(f"{BASE}/courses/{course_id}/assignments", headers=hdrs(), json=asgn_body)
        if not ar.ok:
            errors.append({"name": name, "error": ar.text})
            continue
        asgn_id = ar.json()["id"]
        mr = requests.post(f"{BASE}/courses/{course_id}/modules/{module_id}/items", headers=hdrs(),
                           json={"module_item": {"title": name, "type": "Assignment",
                                                 "content_id": asgn_id}})
        results.append({"name": name, "assignment_id": asgn_id, "linked": mr.ok})

    for key in [f"modules_{course_id}", f"assignments_{course_id}"]:
        p = cache_path(key)
        if p.exists():
            p.unlink()
    for p in CACHE.glob(f"module_items_{course_id}_*.json"):
        p.unlink()

    return jsonify({"module_id": module_id, "unit_number": unit_num,
                    "created": results, "errors": errors})

# ── Topics repo readers ────────────────────────────────────────────────────────

def list_topics():
    return sorted(d.name for d in TOPICS.iterdir()
                  if d.is_dir() and not d.name.startswith(".") and "_" not in d.name)

def parse_topic_lessons(name):
    """Lessons of a topic folder in LESSONS.md order; None if the topic is missing."""
    mod_path = TOPICS / name
    if not name or not mod_path.exists():
        return None
    lessons_file = mod_path / "LESSONS.md"
    assignments = []
    if lessons_file.exists():
        for line in lessons_file.read_text().splitlines():
            # Match: | Day or Day–Day | Title | [Path](path) |
            m = re.match(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(?:\[(.+?)\]\((.+?)\))?\s*\|?", line)
            if not m:
                continue
            day_raw = m.group(1).strip()
            title   = m.group(2).strip()
            if title.startswith("---") or title.lower() in ("day", "lesson"):
                continue
            # Parse single day "3" or range "2–4" / "2-4"
            range_m = re.match(r"(\d+)\s*[–\-]\s*(\d+)", day_raw)
            if range_m:
                start_day = int(range_m.group(1))
                duration  = int(range_m.group(2)) - start_day + 1
            elif day_raw.isdigit():
                start_day = int(day_raw)
                duration  = 1
            else:
                continue  # skip TBD or unknown
            path = (m.group(4) or m.group(3) or "").rstrip("/")
            assignments.append({"day": start_day, "duration": duration,
                                 "title": title, "path": path})
    else:
        subdirs = sorted([d.name for d in mod_path.iterdir()
                          if d.is_dir() and not d.name.startswith(".")])
        assignments = [{"day": i + 1, "duration": 1, "title": d, "path": d}
                       for i, d in enumerate(subdirs)]
    return assignments

def review_files(module, path):
    review_dir = TOPICS / module / path / "review" if path else TOPICS / module / "review"
    if not review_dir.exists():
        return []
    return sorted(f.name for f in review_dir.iterdir()
                  if f.is_file() and f.suffix == ".md")

def review_files_labeled(module, path):
    """Review files for one lesson, each with its display label (the concept
    it covers, numbered only when that concept repeats — see verify.review_labels)."""
    review_dir = TOPICS / module / path / "review" if path else TOPICS / module / "review"
    files = review_files(module, path)
    labels = review_labels(review_dir, files)
    return [{"file": f, "label": labels[f]} for f in files]

def demo_files(module, path):
    demos_dir = TOPICS / module / path / "demos"
    if not demos_dir.exists():
        return []
    return sorted(f.name for f in demos_dir.iterdir()
                  if f.is_file() and f.suffix == ".html")

@app.route("/api/github/modules")
def api_github_modules():
    return jsonify({"modules": list_topics(), "path": str(TOPICS)})

@app.route("/api/github/modules/<name>")
def api_github_module_lessons(name):
    assignments = parse_topic_lessons(name)
    if assignments is None:
        return jsonify({"error": f"Module '{name}' not found"}), 404
    return jsonify({"name": name, "assignments": assignments})

@app.route("/api/github/reviews")
@app.route("/api/reviews")
def api_github_reviews():
    module = request.args.get("module", "")
    path   = request.args.get("path", "")
    if not module:
        return jsonify({"error": "module param required"}), 400
    return jsonify({"files": review_files_labeled(module, path)})

@app.route("/api/github/review-content")
def api_github_review_content():
    module   = request.args.get("module", "")
    path     = request.args.get("path", "")
    filename = request.args.get("file", "")
    if not module or not filename:
        return jsonify({"error": "module and file params required"}), 400
    review_file = (TOPICS / module / path / "review" / filename if path
                   else TOPICS / module / "review" / filename)
    if not review_file.exists():
        return jsonify({"error": "file not found"}), 404
    return jsonify({"content": review_file.read_text()})

# ── Curated modules saved in _modules/*.json ───────────────────────────────────

# Saved-modules lists everywhere share one order: unit_number, then name.
# A drag-reorder in the planner sidebar renumbers unit_number 1..N (see
# /api/saved-order), so the planner, schedule palette, and courses drawer
# all present the library in the same teacher-chosen sequence.
def _saved_sort_key(m):
    return (m.get("unit_number") is None, m.get("unit_number") or 0,
            (m.get("name") or "").lower())

@app.route("/api/github/saved-modules")
def api_github_saved_modules():
    if not MODULES_DIR.exists():
        return jsonify({"modules": []})
    out = []
    for jf in sorted(MODULES_DIR.glob("*.json")):
        try:
            mod = json.loads(jf.read_text())
        except json.JSONDecodeError:
            continue
        assignments = mod.get("assignments", [])
        out.append({"slug": jf.stem,
                    "name": mod.get("name", jf.stem),
                    "unit_number": mod.get("unit_number"),
                    "topic_names": mod.get("topic_names", []),
                    "lesson_count": len(assignments),
                    "updated": mod.get("updated"),
                    "days": max((a.get("day", 1) + a.get("duration", 1) - 1
                                 for a in assignments), default=0)})
    return jsonify({"modules": sorted(out, key=_saved_sort_key)})

@app.route("/api/github/saved-modules/<slug>")
def api_github_saved_module(slug):
    if not SLUG_RE.match(slug):
        return jsonify({"error": "invalid slug"}), 400
    jf = MODULES_DIR / f"{slug}.json"
    if not jf.exists():
        return jsonify({"error": f"saved module '{slug}' not found"}), 404
    mod = json.loads(jf.read_text())
    # Resolve review references to markdown so the drawer can use them directly
    for a in mod.get("assignments", []):
        rev = a.pop("review", None)
        if rev:
            rf = TOPICS / rev["module"] / rev["path"] / "review" / rev["file"]
            if rf.exists():
                a["review_markdown"] = rf.read_text()
                a["review_ref"] = rev
    return jsonify(mod)

# ── Module planner (create/edit curated modules + lesson file editor) ──────────

def resolve_lesson_file(module, path, file):
    """Path-safe resolution of an editable file inside a lesson (or topic) folder."""
    if module not in list_topics() or not FILE_RE.match(file or ""):
        return None, None
    lesson_dir = (TOPICS / module / path).resolve() if path else (TOPICS / module).resolve()
    if not lesson_dir.is_dir() or not lesson_dir.is_relative_to(TOPICS):
        return None, None
    target = (lesson_dir / file).resolve()
    if not target.is_relative_to(lesson_dir):
        return None, None
    return lesson_dir, target

def _sub_md_files(module, path, sub):
    d = TOPICS / module / path / sub if path else TOPICS / module / sub
    if not d.exists():
        return []
    return sorted(f.name for f in d.iterdir() if f.is_file() and f.suffix == ".md")

def asset_files(module, path):
    d = TOPICS / module / path / "assets" if path else TOPICS / module / "assets"
    if not d.exists():
        return []
    return [{"name": f.name, "size": f.stat().st_size}
            for f in sorted(d.iterdir()) if f.is_file() and not f.name.startswith(".")]

def lesson_file_listing(module, path):
    lesson_dir = TOPICS / module / path if path else TOPICS / module
    files = sorted(f.name for f in lesson_dir.iterdir()
                   if f.is_file() and f.suffix == ".md")
    # README first, ASSIGNMENT second, variants after
    files.sort(key=lambda f: {"README.md": 0, "ASSIGNMENT.md": 1}.get(f, 2))
    return {
        "files": files,
        "review": [f"review/{f}" for f in review_files(module, path)],
        "activities": [f"activities/{f}" for f in _sub_md_files(module, path, "activities")],
        "milestones": [f"milestones/{f}" for f in _sub_md_files(module, path, "milestones")],
        "demos": [f"demos/{f}" for f in demo_files(module, path)],
        "assets": asset_files(module, path),
        "can_create": [] if "ASSIGNMENT.md" in files else ["ASSIGNMENT.md"],
    }

def scan_file_links(md_path):
    """Broken relative links in one file (same rules as verify.py)."""
    from urllib.parse import unquote as _unquote
    text = md_path.read_text()
    for pattern in (FENCED_CODE, PRE_BLOCK, INLINE_CODE):
        text = pattern.sub("", text)
    broken = []
    for raw in MD_LINK.findall(text) + HTML_SRC.findall(text):
        target = _unquote(raw.split("#")[0])
        if not target or raw.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if not (md_path.parent / target).resolve().exists():
            broken.append(raw)
    return broken

def validate_module(mod):
    problems = []
    for key in ("name", "slug", "topic_names", "assignments"):
        if not mod.get(key):
            problems.append(f"missing required field '{key}'")
    slug = mod.get("slug", "")
    if slug and not SLUG_RE.match(slug):
        problems.append(f"slug '{slug}' must be kebab-case (a-z, 0-9, -)")
    for t in mod.get("topic_names", []):
        if not (TOPICS / t).is_dir():
            problems.append(f"topic '{t}' is not a folder in the repo")
    for a in mod.get("assignments", []):
        if not a.get("placeholder"):
            lesson_dir = TOPICS / a.get("_module", "") / a.get("path", "")
            if not (lesson_dir / "README.md").exists():
                problems.append(f"lesson '{a.get('_module')}/{a.get('path')}' does not exist")
        rev = a.get("review")
        if rev:
            rev_file = TOPICS / rev.get("module", "") / rev.get("path", "") / "review" / rev.get("file", "")
            if not rev_file.exists():
                problems.append(
                    f"review '{rev.get('module')}/{rev.get('path')}/review/{rev.get('file')}' does not exist")
    return problems

@app.route("/api/topics")
def api_topics():
    topics = list_topics()
    # ?with_lessons=1 → only real topic folders (the Module Editor's browse list);
    # folders like attachments/ or embed/ have no LESSONS.md and aren't topics
    if request.args.get("with_lessons"):
        topics = [t for t in topics if (TOPICS / t / "LESSONS.md").exists()]
    return jsonify({"topics": topics})

@app.route("/api/topics/<name>")
def api_topic_lessons(name):
    assignments = parse_topic_lessons(name)
    if assignments is None:
        return jsonify({"error": f"topic '{name}' not found"}), 404
    return jsonify({"name": name, "assignments": assignments})

@app.route("/api/lesson-files")
def api_lesson_files():
    module = request.args.get("module", "")
    path   = request.args.get("path", "")
    if module not in list_topics() or not (TOPICS / module / path).is_dir():
        return jsonify({"error": "lesson not found"}), 404
    return jsonify(lesson_file_listing(module, path))

@app.route("/api/file", methods=["GET", "POST"])
def api_file():
    if request.method == "GET":
        module = request.args.get("module", "")
        path   = request.args.get("path", "")
        file   = request.args.get("file", "")
        _, target = resolve_lesson_file(module, path, file)
        if target is None:
            return jsonify({"error": "invalid file"}), 400
        if not target.exists():
            return jsonify({"content": "", "exists": False})
        return jsonify({"content": target.read_text(), "exists": True})
    body = request.get_json(force=True) or {}
    module, path, file = body.get("module", ""), body.get("path", ""), body.get("file", "")
    _, target = resolve_lesson_file(module, path, file)
    if target is None:
        return jsonify({"error": "invalid file"}), 400
    target.parent.mkdir(parents=True, exist_ok=True)  # review/ may not exist yet
    content = body.get("content", "")
    if content and not content.endswith("\n"):
        content += "\n"
    target.write_text(content)
    # Link scanning is a markdown check; demo .html saves skip it
    broken = scan_file_links(target) if target.suffix == ".md" else []
    return jsonify({"saved": f"{module}/{path + '/' if path else ''}{file}",
                    "broken_links": broken})

@app.route("/api/syllabus")
def api_syllabus():
    syllabus = ROOT / "SYLLABUS.md"
    if not syllabus.exists():
        return jsonify({"error": "SYLLABUS.md not found"}), 404
    return jsonify({"html": md_to_html(syllabus.read_text(), "")})

@app.route("/api/render", methods=["POST"])
def api_render():
    # Compose the HTML exactly the way the hub uploads it to Canvas
    body = request.get_json(force=True) or {}
    html_parts = []
    engine = PLANNER_ENGINE
    if body.get("review_markdown"):
        rev_html, engine = planner_md_to_html(body["review_markdown"])
        html_parts.append(planner_review_block(rev_html))
    content_html, engine = planner_md_to_html(body.get("markdown", ""), body.get("base_path", ""))
    html_parts.append(content_html)
    return jsonify({"html": "\n".join(html_parts), "engine": engine})

def _saved_modules_list():
    out = []
    if MODULES_DIR.exists():
        for jf in sorted(MODULES_DIR.glob("*.json")):
            try:
                mod = json.loads(jf.read_text())
            except json.JSONDecodeError:
                out.append({"slug": jf.stem, "name": jf.stem, "error": "invalid JSON"})
                continue
            out.append({
                "slug": jf.stem,
                "name": mod.get("name", jf.stem),
                "unit_number": mod.get("unit_number"),
                "topic_names": mod.get("topic_names", []),
                "lesson_count": len(mod.get("assignments", [])),
                "updated": mod.get("updated"),
            })
    return sorted(out, key=_saved_sort_key)

@app.route("/api/saved")
def api_saved_list():
    return jsonify({"modules": _saved_modules_list()})

@app.route("/api/saved-order", methods=["POST"])
def api_saved_order():
    """Persist a drag-reorder of the saved-modules library. unit_number becomes
    the 1-based list position and the module's generated lesson plan is
    refreshed (it embeds the unit in its day labels)."""
    body = request.get_json(force=True) or {}
    order = body.get("order") or []
    if not order or not all(isinstance(s, str) and SLUG_RE.match(s) for s in order):
        return jsonify({"error": "'order' must be a list of module slugs"}), 400
    if len(set(order)) != len(order):
        return jsonify({"error": "duplicate slugs in 'order'"}), 400
    missing = [s for s in order if not (MODULES_DIR / f"{s}.json").exists()]
    if missing:
        return jsonify({"error": f"unknown module(s): {', '.join(missing)}"}), 404
    changed = []
    for position, slug in enumerate(order, start=1):
        jf = MODULES_DIR / f"{slug}.json"
        try:
            mod = json.loads(jf.read_text())
        except json.JSONDecodeError:
            return jsonify({"error": f"_modules/{slug}.json is not valid JSON"}), 422
        if mod.get("unit_number") != position:
            mod["unit_number"] = position
            jf.write_text(json.dumps(mod, indent=2) + "\n")
            LESSONPLANS_DIR.mkdir(parents=True, exist_ok=True)
            (LESSONPLANS_DIR / f"{slug}.md").write_text(generate_lessonplan(mod))
            changed.append(slug)
    return jsonify({"changed": changed, "modules": _saved_modules_list()})

@app.route("/api/saved/<slug>", methods=["GET", "POST", "DELETE"])
def api_saved(slug):
    if not SLUG_RE.match(slug):
        return jsonify({"error": "invalid slug"}), 400
    jf = MODULES_DIR / f"{slug}.json"
    if request.method == "GET":
        if not jf.exists():
            return jsonify({"error": "not found"}), 404
        return jsonify(json.loads(jf.read_text()))
    if request.method == "DELETE":
        plan = LESSONPLANS_DIR / f"{slug}.md"
        if not jf.exists():
            return jsonify({"error": "not found"}), 404
        jf.unlink()
        if plan.exists():
            plan.unlink()
        return jsonify({"deleted": slug})
    body = request.get_json(force=True) or {}
    body["slug"] = slug
    problems = validate_module(body)
    if problems:
        return jsonify({"error": "validation failed", "problems": problems}), 422
    body["updated"] = datetime.now().date().isoformat()
    MODULES_DIR.mkdir(exist_ok=True)
    jf.write_text(json.dumps(body, indent=2) + "\n")
    LESSONPLANS_DIR.mkdir(parents=True, exist_ok=True)
    (LESSONPLANS_DIR / f"{slug}.md").write_text(generate_lessonplan(body))
    return jsonify({"saved": slug, "updated": body["updated"]})

# ── Year schedules (per-teacher, _admin/_schedules/<name>.json) ────────────────
# A schedule stores an ordered list of blocks. Module blocks hold only a
# REFERENCE into this repo (a curated _modules slug or a topic folder) — lessons
# and day counts are re-read on every resolve, so editing a module here reshapes
# every teacher's year automatically.

DEFAULT_SCHEDULE = {
    "year": "2026-27",
    "start_date": "2026-08-26",
    "end_date": "2027-06-04",
    "meeting_days": [0, 1, 2, 3, 4],   # weekday numbers, Monday=0 … Friday=4
    "no_school": [],                   # [{"date": "YYYY-MM-DD", "label": "…"}]
    "show_day0_syllabus": False,        # reserve the first class day for the syllabus (see resolve_schedule)
    "sequence": [],
}

def schedule_path(name):
    return SCHEDULES_DIR / f"{name}.json"

def load_schedule(name):
    p = schedule_path(name)
    if p.exists():
        return json.loads(p.read_text())
    return None

# ── Class calendars (imported .ics, _admin/_schedules/calendars/<name>.json) ───
# A calendar is the compressed local copy of a Didax teacher-schedule export:
# per class slot (Block A-G + named non-block classes), the static list of real
# meeting [date, start, end] triples in local time. A schedule binds to one
# class via {"calendar": <name>, "calendar_class": <class id>} — its class
# dates then come from actual meetings instead of the weekday grid.

def calendar_path(name):
    return CALENDARS_DIR / f"{name}.json"

def load_calendar(name):
    p = calendar_path(name or "")
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None

def schedule_calendar_class(sched):
    """(calendar, class record) a schedule is bound to, or (None, None)."""
    cal_name, class_id = sched.get("calendar"), sched.get("calendar_class")
    if not cal_name or not class_id or not NAME_RE.match(cal_name):
        return None, None
    cal = load_calendar(cal_name)
    if not cal:
        return None, None
    cls = next((c for c in cal.get("classes", []) if c.get("id") == class_id), None)
    return (cal, cls) if cls else (None, None)

def _no_school_dates(sched):
    return {n["date"] if isinstance(n, dict) else n for n in sched.get("no_school", [])}

def schedule_class_meetings(sched):
    """Bound-calendar meetings [date, start, end] after start/end clip and
    no-school skips, or None when the schedule has no working calendar binding."""
    cal, cls = schedule_calendar_class(sched)
    if not cls:
        return None
    off = _no_school_dates(sched)
    start = sched.get("start_date") or "0000"
    end = sched.get("end_date") or "9999"
    out, seen = [], set()
    for m in cls.get("meetings", []):
        if start <= m[0] <= end and m[0] not in off and m[0] not in seen:
            seen.add(m[0])
            out.append(m)
    return out

def schedule_class_dates(sched):
    """Every date the class meets, in order — real meetings when a calendar
    class is bound, otherwise meeting weekdays minus no-school days."""
    meetings = schedule_class_meetings(sched)
    if meetings is not None:
        return [m[0] for m in meetings]
    try:
        start = datetime.strptime(sched["start_date"], "%Y-%m-%d").date()
        end   = datetime.strptime(sched["end_date"], "%Y-%m-%d").date()
    except (KeyError, TypeError, ValueError):
        return []
    meeting = set(sched.get("meeting_days") or [0, 1, 2, 3, 4])
    off = _no_school_dates(sched)
    out, d = [], start
    while d <= end:
        if d.weekday() in meeting and d.isoformat() not in off:
            out.append(d.isoformat())
        d += timedelta(days=1)
    return out

def _saved_module(slug):
    if not SLUG_RE.match(slug or ""):
        return None
    jf = MODULES_DIR / f"{slug}.json"
    if not jf.exists():
        return None
    try:
        return json.loads(jf.read_text())
    except json.JSONDecodeError:
        return None

def _lookup_lesson_title(module, path):
    for a in parse_topic_lessons(module) or []:
        if a.get("path") == path:
            return a.get("title")
    return None

def _insert_slots(item):
    """Day slots for a non-module item (standalone block or a module's insert)."""
    kind  = item.get("type", "custom")
    days  = max(1, int(item.get("days", 1) or 1))
    title = item.get("title") or kind.title()
    if kind == "lesson" and item.get("module") and item.get("path"):
        live = _lookup_lesson_title(item["module"], item["path"])
        if live:
            title = live
    slots = []
    for k in range(days):
        slots.append({"kind": kind,
                      "title": title if days == 1 else f"{title} — day {k + 1}/{days}",
                      "base_title": title,
                      "insert_id": item.get("id"),
                      "group": f"ins-{item.get('id')}",
                      "part": k + 1, "parts": days,
                      "points": item.get("points"), "file": item.get("file"),
                      "lesson_ref": ({"module": item.get("module"), "path": item.get("path")}
                                     if kind == "lesson" else None)})
    return slots

def expand_module_block(block):
    """(meta, slots) for a module block, read live from the repo.

    Inserts (tests, extra lessons, …) are placed after their `after_day`; inserts
    pointing past the module's current length land at the end instead of vanishing,
    so they survive the module shrinking."""
    if block.get("source") == "topic":
        lessons = parse_topic_lessons(block.get("ref", ""))
        if lessons is None:
            return None, None
        lessons = [dict(a, _module=block["ref"]) for a in lessons]
        meta = {"name": block.get("ref"), "topic_names": [block.get("ref")],
                "points": 10, "scale": 1.15}
    else:
        mod = _saved_module(block.get("ref", ""))
        if mod is None:
            return None, None
        lessons = mod.get("assignments", [])
        meta = {"name": mod.get("name", block.get("ref")),
                "topic_names": mod.get("topic_names", []),
                "points": mod.get("points_per_assignment", 10),
                "scale": mod.get("scale_factor", 1.15)}
    total = max((a["day"] + a.get("duration", 1) - 1 for a in lessons), default=0)
    inserts = block.get("inserts", [])
    slots = []

    def add_inserts(after_day):
        for ins in inserts:
            if int(ins.get("after_day", 0) or 0) == after_day:
                slots.extend(_insert_slots(ins))

    add_inserts(0)
    for day in range(1, total + 1):
        # several lessons may share one class day — later ones ride along (co_day)
        active = [x for x in lessons if x["day"] <= day < x["day"] + x.get("duration", 1)]
        if active:
            for j, a in enumerate(active):
                dur, part = a.get("duration", 1), day - a["day"] + 1
                slots.append({"kind": "lesson",
                              "title": a["title"] + (f" — day {part}/{dur}" if dur > 1 else ""),
                              "module_day": day, "part": part, "parts": dur,
                              "co_day": j > 0,
                              "group": f"lesson-{a['day']}-{a.get('path', '')}",
                              "lesson": {"day": a["day"], "duration": dur, "title": a["title"],
                                         "path": a.get("path"), "_module": a.get("_module"),
                                         "review": a.get("review")}})
        else:
            slots.append({"kind": "gap", "title": "(open day)", "module_day": day,
                          "part": 1, "parts": 1, "group": f"gap-{day}"})
        add_inserts(day)
    for ins in inserts:
        if int(ins.get("after_day", 0) or 0) > total:
            slots.extend(_insert_slots(ins))
    return meta, slots

def resolve_schedule(sched):
    """Expand every block against the repo and map its days onto real class dates."""
    dates = schedule_class_dates(sched)
    # Day 0 (first day of class) is a syllabus placeholder, not a block — it
    # reserves the first class date for itself so the sequence's real content
    # starts on the day after, but it adds no entry to `blocks`, consumes no
    # unit_number, and has nothing to sync to Canvas.
    day0_date = None
    if sched.get("show_day0_syllabus") and dates:
        day0_date, dates = dates[0], dates[1:]
    blocks, warnings, idx, unit = [], [], 0, 0
    cal, cls = schedule_calendar_class(sched)
    if sched.get("calendar_class") and not cls:
        warnings.append(f"Calendar class '{sched.get('calendar_class')}' not found in "
                        f"calendar '{sched.get('calendar')}' — re-import the .ics or "
                        "pick a class again; falling back to weekday-grid dates")
    # Meeting times + the next class day after any date (for homework due dates).
    # next_date uses the full meeting list past the end clip, minus no-school
    # skips, so the last scheduled day still knows when the class meets next.
    times = {m[0]: {"start": m[1], "end": m[2]} for m in (cls or {}).get("meetings", [])}
    off = _no_school_dates(sched)
    future = sorted({m[0] for m in (cls or {}).get("meetings", [])} - off)

    def next_class_date(date_str):
        for d in future:
            if d > date_str:
                return d
        return None
    for block in sched.get("sequence", []):
        btype = block.get("type")
        if btype == "module":
            this_unit = unit  # first module in the sequence is Unit 0
            unit += 1
            meta, slots = expand_module_block(block)
            if meta is None:
                warnings.append(f"Module '{block.get('ref')}' was not found in the repo")
                blocks.append({"id": block.get("id"), "type": "module", "ref": block.get("ref"),
                               "source": block.get("source", "saved"), "unit_number": this_unit,
                               "name": block.get("ref"), "missing": True, "slots": [],
                               "days": 0, "start": None, "end": None})
                continue
            out = {"id": block.get("id"), "type": "module", "ref": block.get("ref"),
                   "source": block.get("source", "saved"), "unit_number": this_unit,
                   "name": meta["name"], "topic_names": meta["topic_names"],
                   "points": meta["points"], "scale": meta["scale"],
                   "missing": False, "slots": slots}
        else:
            out = {"id": block.get("id"), "type": btype,
                   "title": block.get("title") or (btype or "day").title(),
                   "file": block.get("file"), "points": block.get("points"),
                   "slots": _insert_slots(block)}
        day_num, last_date = -1, None  # first day in a block is day_num 0, matching Unit 0
        for s in out["slots"]:
            if s.get("co_day"):
                s["date"] = last_date          # shares the class day of the slot above
            else:
                s["date"] = dates[idx] if idx < len(dates) else None
                last_date = s["date"]
                idx += 1
                day_num += 1
            s["day_num"] = day_num
            if s["date"] and cls:
                s["time"] = times.get(s["date"])
                s["next_date"] = next_class_date(s["date"])
        out["days"] = day_num + 1  # count of distinct days, not the 0-indexed last day_num
        dated = [s["date"] for s in out["slots"] if s["date"]]
        out["start"] = dated[0] if dated else None
        out["end"] = dated[-1] if dated else None
        blocks.append(out)
    if idx > len(dates):
        warnings.append(f"The schedule needs {idx} class days but only {len(dates)} exist "
                        f"between {sched.get('start_date')} and {sched.get('end_date')}")
    calendar_out = {"total": len(dates), "used": idx, "remaining": len(dates) - idx}
    if cls:
        mts = cls.get("meetings", [])
        calendar_out["class"] = {
            "id": cls["id"], "block": cls.get("block"), "course": cls.get("course"),
            "location": cls.get("location"), "meetings": len(mts),
            "first": mts[0][0] if mts else None, "last": mts[-1][0] if mts else None,
            "timezone": cal.get("timezone"), "calendar": sched.get("calendar")}
    return {"blocks": blocks, "warnings": warnings, "calendar": calendar_out, "day0_date": day0_date}

@app.route("/api/schedules")
def api_schedules():
    out = []
    if SCHEDULES_DIR.exists():
        for jf in sorted(SCHEDULES_DIR.glob("*.json")):
            try:
                s = json.loads(jf.read_text())
            except json.JSONDecodeError:
                continue
            out.append({"name": jf.stem, "year": s.get("year"),
                        "updated": s.get("updated"),
                        "blocks": len(s.get("sequence", []))})
    return jsonify({"schedules": out})

@app.route("/api/schedules/<name>", methods=["GET", "POST", "DELETE"])
def api_schedule(name):
    if not NAME_RE.match(name):
        return jsonify({"error": "invalid schedule name"}), 400
    if request.method == "DELETE":
        p = schedule_path(name)
        if p.exists():
            p.unlink()
        return jsonify({"deleted": name})
    if request.method == "POST":
        sched = request.get_json(force=True) or {}
        for key in ("start_date", "end_date", "sequence"):
            if key not in sched:
                return jsonify({"error": f"missing '{key}'"}), 400
        sched["updated"] = datetime.now().isoformat(timespec="seconds")
        SCHEDULES_DIR.mkdir(parents=True, exist_ok=True)
        schedule_path(name).write_text(json.dumps(sched, indent=2) + "\n")
    else:
        sched = load_schedule(name)
        if sched is None:
            sched = json.loads(json.dumps(DEFAULT_SCHEDULE))
    return jsonify({"name": name, "schedule": sched, "resolved": resolve_schedule(sched)})

@app.route("/api/calendars")
def api_calendars():
    out = []
    if CALENDARS_DIR.exists():
        for jf in sorted(CALENDARS_DIR.glob("*.json")):
            cal = load_calendar(jf.stem)
            if cal:
                out.append({"name": jf.stem, "year_label": cal.get("year_label"),
                            "imported": cal.get("imported"),
                            "classes": len(cal.get("classes", []))})
    return jsonify({"calendars": out})

@app.route("/api/calendars/<name>", methods=["GET", "DELETE"])
def api_calendar(name):
    if not NAME_RE.match(name):
        return jsonify({"error": "invalid calendar name"}), 400
    if request.method == "DELETE":
        p = calendar_path(name)
        if p.exists():
            p.unlink()
        return jsonify({"deleted": name})
    cal = load_calendar(name)
    if cal is None:
        return jsonify({"error": "calendar not found"}), 404
    return jsonify({"name": name, "calendar": cal})

@app.route("/api/calendars/<name>/import", methods=["POST"])
def api_calendar_import(name):
    """Body is the raw .ics text; compresses it to calendars/<name>.json."""
    if not NAME_RE.match(name):
        return jsonify({"error": "invalid calendar name"}), 400
    text = request.get_data(as_text=True) or ""
    try:
        cal = compress_calendar(text, source_file=request.args.get("filename") or "upload.ics")
    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Could not parse the .ics file: {e}"}), 400
    if not cal["classes"]:
        return jsonify({"error": "No class meetings found in this .ics file"}), 422
    CALENDARS_DIR.mkdir(parents=True, exist_ok=True)
    calendar_path(name).write_text(json.dumps(cal, indent=2) + "\n")
    return jsonify({"name": name, "calendar": cal})

# ── Final exams (private sibling Admin repo) ───────────────────────────────────
# One markdown file per topic final, stored OUTSIDE this public repo. Content
# NEVER leaves the private repo: syncing a test/final day to Canvas creates a
# placeholder assignment (title, date, points) with no exam content.

FINAL_TEMPLATE = """# {name} — Final Exam

**Duration:** 1 class period
**Points:** 100

---

## Format

Describe the exam format here (written / practical / on-paper / on-machine).

## Questions

1. ...
"""

def finals_available():
    return FINALS.parent.is_dir()

@app.route("/api/finals")
def api_finals():
    if not finals_available():
        return jsonify({"available": False, "dir": str(FINALS), "finals": []})
    FINALS.mkdir(exist_ok=True)
    out = []
    for f in sorted(FINALS.glob("*.md")):
        if f.name == "README.md":
            continue
        title = f.stem
        for line in f.read_text().splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        out.append({"name": f.stem, "file": f.name, "title": title})
    return jsonify({"available": True, "dir": str(FINALS), "finals": out})

@app.route("/api/finals/<name>", methods=["GET", "POST", "DELETE"])
def api_final(name):
    if not NAME_RE.match(name):
        return jsonify({"error": "invalid name"}), 400
    if not finals_available():
        return jsonify({"error": f"private finals repo not found at {FINALS.parent}"}), 404
    path = FINALS / f"{name}.md"
    if request.method == "GET":
        if not path.exists():
            return jsonify({"error": "not found"}), 404
        return jsonify({"name": name, "content": path.read_text()})
    if request.method == "DELETE":
        if path.exists():
            path.unlink()
        return jsonify({"deleted": name})
    body = request.get_json(force=True) or {}
    content = body.get("content")
    if content is None:
        content = FINAL_TEMPLATE.format(name=name)
    if content and not content.endswith("\n"):
        content += "\n"
    FINALS.mkdir(exist_ok=True)
    path.write_text(content)
    return jsonify({"saved": name})

# ── Sync a scheduled block to Canvas ───────────────────────────────────────────

def _round_half_up(n):
    return int(n + 0.5)

def smart_round(n):
    """Mirror of the UI's point rounding."""
    if n >= 1000: return _round_half_up(n / 50) * 50
    if n >= 100:  return _round_half_up(n / 10) * 10
    if n >= 50:   return _round_half_up(n / 5) * 5
    return _round_half_up(n)

def _canvas_due(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return d.replace(hour=23, minute=59, second=0, tzinfo=timezone.utc).isoformat()

def _canvas_unlock(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return d.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc).isoformat()

def _lesson_description(module_dir, lesson_path, review_ref):
    html_parts = []
    readme_html = _lesson_readme_html(module_dir, lesson_path)
    if readme_html:
        html_parts.append(readme_html)
    if review_ref:
        rf = (TOPICS / review_ref.get("module", "") / review_ref.get("path", "")
              / "review" / review_ref.get("file", ""))
        if rf.exists():
            html_parts.append(review_block_html(md_to_html(rf.read_text())))
    if module_dir and lesson_path:
        af = TOPICS / module_dir / lesson_path / "ASSIGNMENT.md"
        if af.exists():
            html_parts.append(md_to_html(af.read_text(), f"{module_dir}/{lesson_path}"))
    return "\n".join(html_parts)

def _sched_time_fns(sched):
    """(_due_at, _unlock_at) for a schedule. With a bound class calendar, Canvas
    gets real local times: an assignment unlocks when its class period starts and
    is due at 11:59 PM the night before the class meets next. Without one, the
    legacy UTC date stamps hold."""
    cal, cls = schedule_calendar_class(sched)
    tzname = (cal or {}).get("timezone")
    off = _no_school_dates(sched)
    class_meetings = [m for m in (cls or {}).get("meetings", []) if m[0] not in off]
    start_by_date = {m[0]: m[1] for m in class_meetings}
    meeting_dates = sorted({m[0] for m in class_meetings})

    def _next_meeting(date_str):
        return next((d for d in meeting_dates if d > date_str), None)

    def _due_at(date_str):
        if not date_str:
            return None
        if tzname and cls:
            nxt = _next_meeting(date_str)
            d = (datetime.strptime(nxt, "%Y-%m-%d") - timedelta(days=1)) if nxt \
                else datetime.strptime(date_str, "%Y-%m-%d")
            return d.replace(hour=23, minute=59, tzinfo=ZoneInfo(tzname)).isoformat()
        return _canvas_due(date_str)

    def _unlock_at(date_str):
        if not date_str:
            return None
        start_hm = start_by_date.get(date_str)
        if tzname and start_hm:
            hour, minute = map(int, start_hm.split(":"))
            d = datetime.strptime(date_str, "%Y-%m-%d")
            return d.replace(hour=hour, minute=minute, tzinfo=ZoneInfo(tzname)).isoformat()
        return _canvas_unlock(date_str)

    return _due_at, _unlock_at

def _unit_module_name(block):
    """The Canvas module name a resolved module block syncs to."""
    unit = block["unit_number"]
    topics = block.get("topic_names", [])
    if len(topics) == 1:
        return f"Unit {unit}: {topics[0]}"
    if len(topics) == 2:
        return f"Unit {unit}: {topics[0]} and {topics[1]}"
    if len(topics) >= 3:
        return f"Unit {unit}: {', '.join(topics[:-1])}, and {topics[-1]}"
    return f"Unit {unit}: {block.get('name', '')}".rstrip(": ")

def _expected_block_items(block):
    """What syncing this resolved module block would create on Canvas:
    [{title, type ('Assignment'|'Page'), points, due (date str or None)}].
    Mirrors the create loop in api_schedule_sync_block exactly."""
    slots = block.get("slots", [])
    unit = block["unit_number"]
    pts = smart_round((block.get("points") or 10) * ((block.get("scale") or 1.15) ** unit))

    def group_end(s):
        dated = [x.get("date") for x in slots
                 if x.get("group") == s.get("group") and x.get("date")]
        return dated[-1] if dated else s.get("date")

    expected = []
    for i, s in enumerate(slots):
        if s.get("part", 1) != 1:
            continue
        day_num = s.get("day_num", i + 1)
        kind = s.get("kind")
        if kind == "lesson" and s.get("lesson"):
            a = s["lesson"]
            if not (a.get("_module") and a.get("path")):
                if a.get("kind") == "page":
                    expected.append({"title": f"{unit}.{day_num}: {a['title']}",
                                     "type": "Page", "points": None, "due": None})
                continue
            expected.append({"title": f"{unit}.{day_num}: {a['title']}",
                             "type": "Assignment", "points": pts, "due": group_end(s)})
        elif kind == "lesson" and s.get("lesson_ref"):
            expected.append({"title": f"{unit}.{day_num}: {s.get('base_title') or s['title']}",
                             "type": "Assignment", "points": pts, "due": group_end(s)})
        elif kind in ("test", "final"):
            expected.append({"title": f"{unit}.{day_num}: {s.get('base_title') or s['title']}",
                             "type": "Assignment", "points": s.get("points") or 100,
                             "due": group_end(s)})
    return expected

@app.route("/api/schedules/<name>/sync-status")
def api_schedule_sync_status(name):
    """Compare every syncable block against what actually exists in a Canvas
    course: 'synced' (module + all items found, points and due dates match),
    'partial' (found but incomplete or drifted), or 'unsynced' (nothing there
    yet). Reads through the normal Canvas caches, so repeat checks are cheap."""
    err = no_token()
    if err:
        return err
    if not NAME_RE.match(name):
        return jsonify({"error": "invalid schedule name"}), 400
    sched = load_schedule(name)
    if sched is None:
        return jsonify({"error": "schedule not found"}), 404
    course_id = request.args.get("course_id", type=int)
    if not course_id:
        return jsonify({"error": "course_id required"}), 400
    ttl = 0 if request.args.get("refresh") == "1" else SUBRESOURCE_TTL

    resolved = resolve_schedule(sched)
    _due_at, _ = _sched_time_fns(sched)

    try:
        modules, _, _ = cached(f"modules_{course_id}", ttl, lambda: [
            {"id": m["id"], "name": m["name"], "items_count": m.get("items_count", 0),
             "published": m.get("published"), "position": m.get("position")}
            for m in canvas_paged(f"/courses/{course_id}/modules", {"include[]": "items_count"})])
        assignments, _, _ = cached(f"assignments_{course_id}", ttl, lambda: [
            {"id": a["id"], "name": a["name"], "due_at": a.get("due_at"),
             "points": a.get("points_possible"), "html_url": a.get("html_url")}
            for a in canvas_paged(f"/courses/{course_id}/assignments", {"order_by": "due_at"})])
    except Exception as e:
        return jsonify({"error": f"Canvas fetch failed: {e}"}), 502

    mod_by_name = {m["name"]: m for m in modules}
    asgn_by_name = {}
    for a in assignments:
        asgn_by_name.setdefault(a["name"], a)

    def same_instant(expected_iso, canvas_iso):
        try:
            e = datetime.fromisoformat(expected_iso)
            c = datetime.fromisoformat(canvas_iso.replace("Z", "+00:00"))
            return abs((e - c).total_seconds()) < 60
        except (ValueError, TypeError):
            return False

    def assignment_issues(title, points, due_date):
        """Points/due-date drift for one Canvas assignment (empty list = match)."""
        a = asgn_by_name.get(title)
        if not a:
            return None   # not in the course's assignment list at all
        issues = []
        if points is not None and a.get("points") is not None \
                and float(a["points"]) != float(points):
            issues.append(f"“{title}”: {a['points']:g} pts on Canvas, schedule says {points:g}")
        if due_date:
            exp = _due_at(due_date)
            if exp and a.get("due_at") and not same_instant(exp, a["due_at"]):
                issues.append(f"“{title}”: due dates differ (Canvas {a['due_at'][:10]}, schedule {exp[:10]})")
            elif exp and not a.get("due_at"):
                issues.append(f"“{title}”: no due date on Canvas")
        return issues

    def module_items(mid):
        data, _, _ = cached(f"module_items_{course_id}_{mid}", ttl, lambda: [
            {"title": it.get("title"), "type": it.get("type")}
            for it in canvas_paged(f"/courses/{course_id}/modules/{mid}/items")])
        return data

    statuses = {}
    for block in resolved["blocks"]:
        bid = block.get("id")
        if not bid or block.get("missing"):
            continue
        if block["type"] == "module":
            expected = _expected_block_items(block)
            if not expected:
                continue
            mod_name = _unit_module_name(block)
            mod = mod_by_name.get(mod_name)
            if not mod:
                statuses[bid] = {"status": "unsynced",
                                 "detail": f"Ready to sync — no module named “{mod_name}” in the course yet"}
                continue
            try:
                item_keys = {(it["title"], it["type"]) for it in module_items(mod["id"])}
            except Exception:
                item_keys = set()
            missing, drifted = [], []
            for e in expected:
                if (e["title"], e["type"]) not in item_keys:
                    missing.append(e["title"])
                    continue
                if e["type"] == "Assignment":
                    drifted.extend(assignment_issues(e["title"], e["points"], e["due"]) or [])
            if not missing and not drifted:
                statuses[bid] = {"status": "synced",
                                 "detail": f"It seems to be synced — “{mod_name}” has all {len(expected)} "
                                           "item(s) with matching titles, points, and due dates"}
            else:
                bits = []
                if missing:
                    bits.append("missing from Canvas: " + ", ".join(f"“{t}”" for t in missing[:4])
                                + ("…" if len(missing) > 4 else ""))
                if drifted:
                    bits.append("; ".join(drifted[:3]) + ("…" if len(drifted) > 3 else ""))
                statuses[bid] = {"status": "partial",
                                 "detail": f"Partially synced — “{mod_name}” exists but " + " · ".join(bits)}
        elif block["type"] in ("test", "final", "lesson"):
            first = block["slots"][0] if block.get("slots") else {}
            title = first.get("base_title") or block.get("title") or block["type"].title()
            points = block.get("points") or (100 if block["type"] in ("test", "final") else 10)
            if title not in asgn_by_name:
                statuses[bid] = {"status": "unsynced",
                                 "detail": f"Ready to sync — no assignment named “{title}” in the course yet"}
            else:
                drifted = assignment_issues(title, points, block.get("end")) or []
                statuses[bid] = ({"status": "synced",
                                  "detail": f"It seems to be synced — “{title}” found with matching points and due date"}
                                 if not drifted else
                                 {"status": "partial", "detail": "Partially synced — " + "; ".join(drifted)})
    return jsonify({"course_id": course_id, "statuses": statuses})

@app.route("/api/schedules/<name>/sync-block", methods=["POST"])
def api_schedule_sync_block(name):
    err = no_token()
    if err:
        return err
    if not NAME_RE.match(name):
        return jsonify({"error": "invalid schedule name"}), 400
    sched = load_schedule(name)
    if sched is None:
        return jsonify({"error": "schedule not found"}), 404
    body = request.get_json(force=True) or {}
    course_id = body.get("course_id")
    block_id = body.get("block_id")
    if not course_id or not block_id:
        return jsonify({"error": "course_id and block_id required"}), 400
    resolved = resolve_schedule(sched)
    block = next((b for b in resolved["blocks"] if b.get("id") == block_id), None)
    if block is None:
        return jsonify({"error": "block not found in schedule"}), 404
    if block.get("missing"):
        return jsonify({"error": "block source is missing from the repo"}), 422

    _due_at, _unlock_at = _sched_time_fns(sched)

    results, errors = [], []

    def create_assignment(name, points, description, due, unlock, module_id=None):
        payload = {"assignment": {
            "name": name, "points_possible": points,
            "submission_types": ["online_upload", "online_text_entry"],
            "description": description, "published": False}}
        if due:
            payload["assignment"]["due_at"] = _due_at(due)
        if unlock:
            payload["assignment"]["unlock_at"] = _unlock_at(unlock)
        r = requests.post(f"{BASE}/courses/{course_id}/assignments", headers=hdrs(), json=payload)
        if not r.ok:
            errors.append({"name": name, "error": r.text})
            return
        asgn_id = r.json()["id"]
        linked = True
        if module_id:
            mr = requests.post(f"{BASE}/courses/{course_id}/modules/{module_id}/items",
                               headers=hdrs(),
                               json={"module_item": {"title": name, "type": "Assignment",
                                                     "content_id": asgn_id}})
            linked = mr.ok
        results.append({"name": name, "assignment_id": asgn_id, "linked": linked})

    if block["type"] == "module":
        unit = block["unit_number"]
        mod_name = _unit_module_name(block)
        points = smart_round((block.get("points") or 10) * ((block.get("scale") or 1.15) ** unit))
        mod_res = requests.post(f"{BASE}/courses/{course_id}/modules", headers=hdrs(),
                                json={"module": {"name": mod_name, "position": 1}})
        if not mod_res.ok:
            return jsonify({"error": f"Module creation failed: {mod_res.text}"}), 502
        module_id = mod_res.json()["id"]

        slots = block["slots"]

        def group_end(s):
            dated = [x.get("date") for x in slots
                     if x.get("group") == s.get("group") and x.get("date")]
            return dated[-1] if dated else s.get("date")

        for i, s in enumerate(slots):
            if s.get("part", 1) != 1:
                continue  # later day of a multi-day item — covered by its first day
            day_num = s.get("day_num", i + 1)
            kind = s.get("kind")
            if kind == "lesson" and s.get("lesson"):
                a = s["lesson"]
                if not (a.get("_module") and a.get("path")):
                    # placeholder: 'page' syncs a Canvas Page (no assignment);
                    # 'test' / plain reserve the day number and create nothing
                    if a.get("kind") == "page":
                        pname = f"{unit}.{day_num}: {a['title']}"
                        desc = (_lesson_description("", "", a.get("review"))
                                or "<p>In-class day — no assignment due.</p>")
                        page, perr = create_canvas_page(course_id, module_id, pname, desc)
                        if perr:
                            errors.append({"name": pname, "error": perr})
                        else:
                            results.append(page)
                    continue
                create_assignment(f"{unit}.{day_num}: {a['title']}", points,
                                  _lesson_description(a.get("_module"), a.get("path"),
                                                      a.get("review")),
                                  group_end(s), s.get("date"), module_id)
            elif kind == "lesson" and s.get("lesson_ref"):
                ref = s["lesson_ref"]
                create_assignment(f"{unit}.{day_num}: {s.get('base_title') or s['title']}", points,
                                  _lesson_description(ref.get("module"), ref.get("path"), None),
                                  group_end(s), s.get("date"), module_id)
            elif kind in ("test", "final"):
                label = "final exam" if kind == "final" else "test"
                create_assignment(f"{unit}.{day_num}: {s.get('base_title') or s['title']}",
                                  s.get("points") or 100,
                                  f"<p>In-class {label}. Details will be provided in class.</p>",
                                  group_end(s), s.get("date"), module_id)
            # review / flex / custom / gap days are schedule-only — nothing in Canvas
        payload_out = {"module_id": module_id, "module_name": mod_name, "unit_number": unit,
                       "created": results, "errors": errors}
    else:
        kind = block["type"]
        first = block["slots"][0] if block.get("slots") else {}
        title = first.get("base_title") or block.get("title") or kind.title()
        if kind in ("test", "final"):
            label = "final exam" if kind == "final" else "test"
            create_assignment(title, block.get("points") or 100,
                              f"<p>In-class {label}. Details will be provided in class.</p>",
                              block.get("end"), block.get("start"))
        elif kind == "lesson":
            ref = first.get("lesson_ref") or {}
            create_assignment(title, block.get("points") or 10,
                              _lesson_description(ref.get("module"), ref.get("path"), None),
                              block.get("end"), block.get("start"))
        else:
            return jsonify({"error": f"'{kind}' days are schedule-only — nothing to sync"}), 422
        payload_out = {"created": results, "errors": errors}

    for key in [f"modules_{course_id}", f"assignments_{course_id}"]:
        p = cache_path(key)
        if p.exists():
            p.unlink()
    for p in CACHE.glob(f"module_items_{course_id}_*.json"):
        p.unlink()
    return jsonify(payload_out)

# ── Module Editor ──────────────────────────────────────────────────────────────
# Edits the repo topic folders (the content source of truth). Strict one-way
# flow: content -> curated modules (references) -> schedules (references).
# Structural changes here keep every index file in step (LESSONS.md, topic
# README table, root README bullets, CLAUDE.md topics line, prev/next navs)
# and rewrite _modules/*.json references on rename. Deleting anything a
# curated module still references is refused — unhook it in the Planner first.

FOLDER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")   # lesson/topic folder names
ASSET_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf",
              ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx",
              ".csv", ".txt", ".zip"}
TYPE_COLORS = {"Environment Configuration": "#3fb950", "Learning": "#a371f7",
               "Reinforce": "#a371f7", "Review": "#e3b341"}

def _kebab(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")

def _first_h1(md_path, fallback):
    if md_path.exists():
        m = re.search(r"^# (.+)$", md_path.read_text(), re.MULTILINE)
        if m:
            return m.group(1).strip()
    return fallback

def _topic_title(topic):
    return _first_h1(TOPICS / topic / "README.md", topic)

def _lesson_title(topic, path):
    return _first_h1(TOPICS / topic / path / "README.md", path)

def _scan_usage(topic, path=None, review_file=None):
    """Which curated modules (and, through them, teacher schedules) reference
    this topic / lesson / review file. Powers the impact banner and delete guards."""
    mods = []
    for jf in sorted(MODULES_DIR.glob("*.json")) if MODULES_DIR.exists() else []:
        try:
            mod = json.loads(jf.read_text())
        except json.JSONDecodeError:
            continue
        hit = False
        for a in mod.get("assignments", []):
            rev = a.get("review") or {}
            if review_file:
                hit = hit or (rev.get("module") == topic and rev.get("path") == path
                              and rev.get("file") == review_file)
            elif path:
                hit = hit or (a.get("_module") == topic and a.get("path") == path) \
                          or (rev.get("module") == topic and rev.get("path") == path)
            else:
                hit = hit or a.get("_module") == topic
        if not path and not review_file and topic in (mod.get("topic_names") or []):
            hit = True
        if hit:
            mods.append({"slug": jf.stem, "name": mod.get("name", jf.stem),
                         "unit_number": mod.get("unit_number")})
    slugs = {m["slug"] for m in mods}
    scheds = []
    if SCHEDULES_DIR.exists():
        for sf in sorted(SCHEDULES_DIR.glob("*.json")):
            try:
                sched = json.loads(sf.read_text())
            except json.JSONDecodeError:
                continue
            for b in sched.get("sequence", []):
                if b.get("type") != "module":
                    continue
                if (b.get("source") == "saved" and b.get("ref") in slugs) or \
                   (b.get("source") != "saved" and b.get("ref") == topic):
                    scheds.append({"name": sf.stem, "year": sched.get("year")})
                    break
    return {"modules": mods, "schedules": scheds}

# ── index-file rewriters (LESSONS.md, READMEs, CLAUDE.md, navs) ────────────────

def _day_cell(a):
    dur = a.get("duration") or 1
    return f"{a['day']}–{a['day'] + dur - 1}" if dur > 1 else str(a["day"])

def _renumber(assignments):
    day = 1
    for a in assignments:
        a["day"] = day
        day += a.get("duration") or 1
    return assignments

def _write_lessons_md(topic, assignments):
    lines = [f"# {topic} — Lesson Plan", "", "| Day | Lesson | Path |", "|---|---|---|"]
    for a in assignments:
        lines.append(f"| {_day_cell(a)} | {a['title']} | [{a['path']}/]({a['path']}/) |")
    (TOPICS / topic / "LESSONS.md").write_text("\n".join(lines) + "\n")

def _rewrite_topic_readme_table(topic, assignments):
    """Regenerate the data rows of the topic README's Lessons table, preserving
    each lesson's 'What you'll learn' cell by path."""
    rf = TOPICS / topic / "README.md"
    if not rf.exists():
        return
    lines = rf.read_text().split("\n")
    head = next((i for i, l in enumerate(lines)
                 if re.match(r"\|\s*(Day|#)\s*\|\s*Lesson\s*\|", l)), None)
    if head is None:
        return
    start = head + 2                                   # skip header + separator
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    learn = {}
    for l in lines[start:end]:
        m = re.match(r"\|[^|]*\|\s*\[[^\]]*\]\(([^)]+?)/?\)\s*\|\s*(.*?)\s*\|?\s*$", l)
        if m:
            learn[m.group(1)] = m.group(2)
    rows = [f"| {_day_cell(a)} | [{a['title']}]({a['path']}/) | "
            f"{learn.get(a['path'], 'TODO: one-line description')} |" for a in assignments]
    lines[start:end] = rows
    rf.write_text("\n".join(lines))

def _rewrite_root_readme_bullets(topic, assignments):
    """Regenerate the topic's subtopic bullet list in the root README,
    preserving each bullet's one-line summary by path."""
    rf = ROOT / "README.md"
    lines = rf.read_text().split("\n")
    bullet_re = re.compile(r"^- \[(.+?)\]\(%s/([^)]+?)/?\)(?:\s*—\s*(.*))?\s*$" % re.escape(topic))
    idxs = [i for i, l in enumerate(lines) if bullet_re.match(l)]
    if not idxs:
        return
    summaries = {}
    for i in idxs:
        m = bullet_re.match(lines[i])
        summaries[m.group(2)] = m.group(3) or ""
    new = [f"- [{a['title']}]({topic}/{a['path']}/) — "
           f"{summaries.get(a['path']) or 'TODO: one-line summary'}" for a in assignments]
    lines[idxs[0]:idxs[-1] + 1] = new
    rf.write_text("\n".join(lines))

def _rewrite_claude_topics_line(topic, assignments):
    cf = ROOT / "CLAUDE.md"
    if not cf.exists():
        return
    text = cf.read_text()
    lesson_list = ", ".join(a["path"] for a in assignments)
    entry_re = re.compile(r"`%s/` \([^)]*\)" % re.escape(topic))
    if entry_re.search(text):
        text = entry_re.sub(f"`{topic}/` ({lesson_list})", text, count=1)
    else:
        text = re.sub(r"^(Current topics: .*?)$",
                      lambda m: f"{m.group(1)}, `{topic}/` ({lesson_list})",
                      text, count=1, flags=re.MULTILINE)
    cf.write_text(text)

def _nav_line(topic_title, prev_a, next_a):
    if prev_a and next_a:
        return (f"← [{prev_a['title']}](../{prev_a['path']}/) — "
                f"Next: [{next_a['title']}](../{next_a['path']}/)")
    if next_a:
        return f"← Back to [{topic_title}](../) — Next: [{next_a['title']}](../{next_a['path']}/)"
    if prev_a:
        return f"← [{prev_a['title']}](../{prev_a['path']}/) — Back to [{topic_title}](../)"
    return f"← Back to [{topic_title}](../)"

def _rewrite_navs(topic, assignments):
    """Rewrite the bottom nav line of every lesson README to match the current
    order (first/middle/last patterns per CLAUDE.md)."""
    title = _topic_title(topic)
    for i, a in enumerate(assignments):
        rf = TOPICS / topic / a["path"] / "README.md"
        if not rf.exists():
            continue
        nav = _nav_line(title, assignments[i - 1] if i > 0 else None,
                        assignments[i + 1] if i + 1 < len(assignments) else None)
        lines = rf.read_text().split("\n")
        for j in range(len(lines) - 1, -1, -1):
            if lines[j].startswith("←"):
                lines[j] = nav
                break
        else:
            while lines and not lines[-1].strip():
                lines.pop()
            lines += ["", nav, ""]
        rf.write_text("\n".join(lines))

def _rewrite_module_refs(topic, old_path, new_path):
    """Point _modules/*.json references at a renamed lesson folder and refresh
    the generated lesson plans. Returns the changed slugs."""
    changed = []
    for jf in sorted(MODULES_DIR.glob("*.json")) if MODULES_DIR.exists() else []:
        try:
            mod = json.loads(jf.read_text())
        except json.JSONDecodeError:
            continue
        hit = False
        for a in mod.get("assignments", []):
            if a.get("_module") == topic and a.get("path") == old_path:
                a["path"] = new_path
                hit = True
            rev = a.get("review")
            if rev and rev.get("module") == topic and rev.get("path") == old_path:
                rev["path"] = new_path
                hit = True
        if hit:
            jf.write_text(json.dumps(mod, indent=2) + "\n")
            LESSONPLANS_DIR.mkdir(parents=True, exist_ok=True)
            (LESSONPLANS_DIR / f"{jf.stem}.md").write_text(generate_lessonplan(mod))
            changed.append(jf.stem)
    return changed

def _rewrite_md_links(topic, old_path, new_path):
    """Repo-wide link fixup after a lesson rename: 'Topic/Old/' anywhere, and
    sibling-relative '../Old/' inside the same topic."""
    for mf in ROOT.rglob("*.md"):
        if any(part.startswith(("_", ".")) for part in mf.relative_to(ROOT).parts):
            continue
        text = mf.read_text()
        out = text.replace(f"{topic}/{old_path}/", f"{topic}/{new_path}/")
        if mf.is_relative_to(TOPICS / topic) and not mf.is_relative_to(TOPICS / topic / new_path):
            out = out.replace(f"../{old_path}/", f"../{new_path}/")
        if out != text:
            mf.write_text(out)

def _sync_all_indexes(topic, assignments):
    _renumber(assignments)
    _write_lessons_md(topic, assignments)
    _rewrite_topic_readme_table(topic, assignments)
    _rewrite_root_readme_bullets(topic, assignments)
    _rewrite_claude_topics_line(topic, assignments)
    _rewrite_navs(topic, assignments)

# ── activity toggle sync (README <details> embeds) ─────────────────────────────

def _parse_activity(content):
    m = re.match(r"# Activity — (.+?)\n(.*)", content, re.DOTALL)
    if not m:
        return None, content.strip()
    return m.group(1).strip(), m.group(2).strip()

def _activity_toggle(file, title, body):
    # <h3> in the summary so activity headers render larger than body text
    return ("👉 <details>\n"
            f"<summary><h3>Activity: {title} — click to expand</h3></summary>\n\n"
            f"{body}\n\n"
            f"*(Standalone file: [activities/{file}](activities/{file}))*\n\n"
            "</details>")

def _find_activity_toggle(text, file):
    """(start, end) of the <details> block that embeds activities/<file>, or None."""
    marker = f"(activities/{file})"
    for m in re.finditer(r"👉 <details>", text):
        end = text.find("</details>", m.start())
        if end == -1:
            continue
        end += len("</details>")
        if marker in text[m.start():end]:
            return m.start(), end
    return None

def _sync_activity_toggle(topic, path, file, title, body):
    """Regenerate (or insert) the README's embedded toggle for one activity.
    The standalone file and the embed are duplicates by convention — this keeps
    them from drifting. Returns True if the README changed."""
    rf = TOPICS / topic / path / "README.md"
    if not rf.exists():
        return False
    # the one permitted divergence between the two copies: the activity file
    # sees the lesson's assets/ from inside activities/, the README from the
    # lesson root — rewrite the prefix so images resolve in both places
    body = body.replace("](../assets/", "](assets/").replace('src="../assets/', 'src="assets/')
    text = rf.read_text()
    block = _activity_toggle(file, title, body)
    span = _find_activity_toggle(text, file)
    if span:
        new = text[:span[0]] + block + text[span[1]:]
    else:
        # default insertion point: just above Check for Understanding, else nav
        anchor = re.search(r"^## <font[^>]*>☑️ Check for Understanding</font>", text, re.MULTILINE)
        if anchor:
            new = text[:anchor.start()] + block + "\n\n" + text[anchor.start():]
        else:
            nav = None
            for m in re.finditer(r"^←", text, re.MULTILINE):
                nav = m
            if nav:
                new = text[:nav.start()] + block + "\n\n" + text[nav.start():]
            else:
                new = text.rstrip() + "\n\n" + block + "\n"
    if new != text:
        rf.write_text(new)
        return True
    return False

def _remove_activity_toggle(topic, path, file):
    rf = TOPICS / topic / path / "README.md"
    if not rf.exists():
        return False
    text = rf.read_text()
    span = _find_activity_toggle(text, file)
    if not span:
        return False
    start, end = span
    while start > 0 and text[start - 1] == "\n":
        start -= 1
    rf.write_text(text[:start] + text[end:])
    return True

# ── editor routes ───────────────────────────────────────────────────────────────

@app.route("/api/editor/bundle")
def api_editor_bundle():
    """Everything written for one lesson as a single labeled text blob — the
    raw material pasted into an AI chat when drafting a new review/activity."""
    topic = request.args.get("module", "")
    path = request.args.get("path", "")
    if topic not in list_topics() or not (TOPICS / topic / path).is_dir():
        return jsonify({"error": "unknown lesson"}), 404
    lesson_dir = TOPICS / topic / path
    parts = []

    def add(label, p):
        if p.exists():
            parts.append(f"===== {label} =====\n{p.read_text().strip()}")

    add("LESSON README", lesson_dir / "README.md")
    add("ASSIGNMENT", lesson_dir / "ASSIGNMENT.md")
    for f in _sub_md_files(topic, path, "milestones"):
        add(f"MILESTONE: {f}", lesson_dir / "milestones" / f)
    for f in _sub_md_files(topic, path, "review"):
        add(f"REVIEW: {f}", lesson_dir / "review" / f)
    for f in _sub_md_files(topic, path, "activities"):
        add(f"ACTIVITY: {f}", lesson_dir / "activities" / f)
    return jsonify({"text": "\n\n".join(parts)})

@app.route("/api/editor/impact")
def api_editor_impact():
    topic = request.args.get("module", "")
    path = request.args.get("path", "") or None
    review_file = request.args.get("review_file", "") or None
    if topic not in list_topics():
        return jsonify({"error": "unknown topic"}), 404
    return jsonify(_scan_usage(topic, path, review_file))

def _scaffold_readme(title, subtitle, type_label, topic_title, prev_a):
    color = TYPE_COLORS.get(type_label, "#a371f7")
    nav = _nav_line(topic_title, prev_a, None)
    return f"""<div align="center">

# {title}
*<font color="#8b949e">{subtitle}</font>*

<font color="{color}">{type_label}</font>

</div>

---

TODO: introduce the lesson here.

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] I can ...

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] ...

---

{nav}
"""

@app.route("/api/editor/topics", methods=["POST"])
def api_editor_topics():
    """Create a new topic folder with its first lesson, keeping every index in
    step (root README group entry, CLAUDE.md topics line)."""
    body = request.get_json(force=True) or {}
    folder = (body.get("folder") or "").strip()
    title = (body.get("title") or "").strip()
    summary = (body.get("summary") or "").strip() or "TODO: one-sentence topic summary."
    type_label = body.get("type_label") or "Learning"
    lesson = body.get("lesson") or {}
    lfolder = (lesson.get("folder") or "").strip()
    ltitle = (lesson.get("title") or "").strip()
    if not FOLDER_RE.match(folder):
        return jsonify({"error": "topic folder must be CamelCase letters/digits"}), 400
    if (TOPICS / folder).exists():
        return jsonify({"error": f"'{folder}' already exists"}), 409
    if not FOLDER_RE.match(lfolder) or not ltitle:
        return jsonify({"error": "a first lesson (folder + title) is required"}), 400
    if type_label not in TYPE_COLORS:
        return jsonify({"error": "unknown lesson type"}), 400
    # topic README
    (TOPICS / folder).mkdir()
    color = TYPE_COLORS[type_label]
    (TOPICS / folder / "README.md").write_text(f"""<div align="center">

# {title or folder}
*<font color="#8b949e">{summary}</font>*

<font color="{color}">{type_label}</font>

</div>

---

{summary}

## <font color="#388bfd">Lessons</font>

| Day | Lesson | What you'll learn |
|---|---|---|
| 1 | [{ltitle}]({lfolder}/) | TODO: one-line description |
""")
    # first lesson
    (TOPICS / folder / lfolder).mkdir()
    (TOPICS / folder / lfolder / "README.md").write_text(
        _scaffold_readme(ltitle, lesson.get("subtitle") or "TODO: short italic subtitle",
                         type_label, title or folder, None))
    assignments = [{"day": 1, "duration": 1, "title": ltitle, "path": lfolder}]
    _write_lessons_md(folder, assignments)
    # root README: append entry to the matching ■-type group
    rf = ROOT / "README.md"
    lines = rf.read_text().split("\n")
    group_label = "Learning" if type_label == "Reinforce" else type_label
    gi = next((i for i, l in enumerate(lines) if f"■ {group_label}" in l), None)
    entry = [f"**[{title or folder}]({folder}/)**  ", summary, "",
             f"- [{ltitle}]({folder}/{lfolder}/) — TODO: one-line summary", ""]
    if gi is None:
        lines += ["", f'<font color="{color}">■ {group_label}</font>', ""] + entry
    else:
        end = gi + 1
        while end < len(lines) and "■ " not in lines[end]:
            end += 1
        while end > gi + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = [""] + entry
    rf.write_text("\n".join(lines))
    _rewrite_claude_topics_line(folder, assignments)
    return jsonify({"created": folder, "lesson": lfolder})

@app.route("/api/editor/lessons", methods=["POST"])
def api_editor_lessons():
    """Structural lesson operations on a topic: create / rename / delete / reorder.
    Every op regenerates LESSONS.md, the topic README table, root README bullets,
    the CLAUDE.md topics line, and all prev/next navs."""
    body = request.get_json(force=True) or {}
    topic = body.get("topic", "")
    op = body.get("op", "")
    if topic not in list_topics():
        return jsonify({"error": "unknown topic"}), 404
    assignments = parse_topic_lessons(topic) or []

    if op == "create":
        folder = (body.get("folder") or "").strip()
        title = (body.get("title") or "").strip()
        if not FOLDER_RE.match(folder):
            return jsonify({"error": "lesson folder must be CamelCase letters/digits"}), 400
        if (TOPICS / topic / folder).exists():
            return jsonify({"error": f"'{topic}/{folder}' already exists"}), 409
        if not title:
            return jsonify({"error": "a lesson title is required"}), 400
        type_label = body.get("type_label") or "Learning"
        if type_label not in TYPE_COLORS:
            return jsonify({"error": "unknown lesson type"}), 400
        pos = body.get("position")
        pos = len(assignments) if not isinstance(pos, int) or not (0 <= pos <= len(assignments)) else pos
        (TOPICS / topic / folder).mkdir()
        prev_a = assignments[pos - 1] if pos > 0 else None
        (TOPICS / topic / folder / "README.md").write_text(
            _scaffold_readme(title, body.get("subtitle") or "TODO: short italic subtitle",
                             type_label, _topic_title(topic), prev_a))
        assignments.insert(pos, {"day": 0, "duration": int(body.get("duration") or 1),
                                 "title": title, "path": folder})
        _sync_all_indexes(topic, assignments)
        return jsonify({"created": f"{topic}/{folder}"})

    if op == "rename":
        old = body.get("path", "")
        new = (body.get("new_folder") or "").strip()
        new_title = (body.get("new_title") or "").strip()
        cur = next((a for a in assignments if a["path"] == old), None)
        if not cur or not (TOPICS / topic / old).is_dir():
            return jsonify({"error": f"unknown lesson '{old}'"}), 404
        if not FOLDER_RE.match(new):
            return jsonify({"error": "new folder must be CamelCase letters/digits"}), 400
        if new != old and (TOPICS / topic / new).exists():
            return jsonify({"error": f"'{topic}/{new}' already exists"}), 409
        if new != old:
            shutil.move(str(TOPICS / topic / old), str(TOPICS / topic / new))
            _rewrite_md_links(topic, old, new)
            changed = _rewrite_module_refs(topic, old, new)
        else:
            changed = []
        cur["path"] = new
        if new_title:
            cur["title"] = new_title
            rf = TOPICS / topic / new / "README.md"
            if rf.exists():
                rf.write_text(re.sub(r"^# .+$", f"# {new_title}", rf.read_text(),
                                     count=1, flags=re.MULTILINE))
        _sync_all_indexes(topic, assignments)
        return jsonify({"renamed": f"{topic}/{new}", "modules_updated": changed})

    if op == "delete":
        path = body.get("path", "")
        cur = next((a for a in assignments if a["path"] == path), None)
        if not cur or not (TOPICS / topic / path).is_dir():
            return jsonify({"error": f"unknown lesson '{path}'"}), 404
        usage = _scan_usage(topic, path)
        if usage["modules"]:
            return jsonify({"error": "lesson is referenced by curated module(s) — remove it "
                                     "there first (Module Planner)",
                            "modules": usage["modules"]}), 409
        if body.get("confirm") != path:
            return jsonify({"error": "confirmation mismatch — type the folder name to confirm"}), 400
        shutil.rmtree(TOPICS / topic / path)
        assignments = [a for a in assignments if a["path"] != path]
        _sync_all_indexes(topic, assignments)
        return jsonify({"deleted": f"{topic}/{path}"})

    if op == "reorder":
        order = body.get("order") or []
        if sorted(order) != sorted(a["path"] for a in assignments):
            return jsonify({"error": "'order' must be a permutation of the topic's lessons"}), 400
        by_path = {a["path"]: a for a in assignments}
        assignments = [by_path[p] for p in order]
        _sync_all_indexes(topic, assignments)
        return jsonify({"reordered": order})

    return jsonify({"error": f"unknown op '{op}'"}), 400

@app.route("/api/editor/review", methods=["POST"])
def api_editor_review():
    body = request.get_json(force=True) or {}
    topic, path, op = body.get("topic", ""), body.get("path", ""), body.get("op", "")
    if topic not in list_topics() or not (TOPICS / topic / path).is_dir():
        return jsonify({"error": "unknown lesson"}), 404

    if op == "create":
        concept = (body.get("concept") or "").strip()
        if not concept:
            return jsonify({"error": "a concept name is required"}), 400
        file = _kebab(concept) + ".md"
        target = TOPICS / topic / path / "review" / file
        if target.exists():
            return jsonify({"error": f"review/{file} already exists"}), 409
        target.parent.mkdir(exist_ok=True)
        target.write_text(f"""# Review — {concept}

*Originally covered in [{_lesson_title(topic, path)}](../README.md)*

---

| Command | What it does |
|---|---|
| `TODO` | TODO |

---

## Tasks

1. TODO: concrete action the student performs
""")
        return jsonify({"created": f"review/{file}"})

    if op == "delete":
        file = body.get("file", "")
        target = TOPICS / topic / path / "review" / file
        if not FILE_RE.match(f"review/{file}") or not target.exists():
            return jsonify({"error": "unknown review file"}), 404
        usage = _scan_usage(topic, path, review_file=file)
        if usage["modules"]:
            return jsonify({"error": "review file is attached to curated module(s) — detach it "
                                     "there first (Module Planner)",
                            "modules": usage["modules"]}), 409
        if not body.get("confirm"):
            return jsonify({"error": "missing confirmation"}), 400
        target.unlink()
        return jsonify({"deleted": f"review/{file}"})

    return jsonify({"error": f"unknown op '{op}'"}), 400

@app.route("/api/editor/activity", methods=["POST"])
def api_editor_activity():
    """Create / save / delete an activity. Save and create keep the README's
    embedded <details> toggle in lockstep with the standalone file (the two are
    intentional duplicates — see CLAUDE.md 'activities/ folders')."""
    body = request.get_json(force=True) or {}
    topic, path, op = body.get("topic", ""), body.get("path", ""), body.get("op", "")
    if topic not in list_topics() or not (TOPICS / topic / path).is_dir():
        return jsonify({"error": "unknown lesson"}), 404
    act_dir = TOPICS / topic / path / "activities"

    if op == "create":
        title = (body.get("title") or "").strip()
        concept = (body.get("concept") or "").strip() or "TODO: one sentence naming the idea this activity proves"
        if not title:
            return jsonify({"error": "an activity title is required"}), 400
        existing = _sub_md_files(topic, path, "activities")
        file = f"{len(existing) + 1:02d}-{_kebab(title)}.md"
        target = act_dir / file
        if target.exists():
            return jsonify({"error": f"activities/{file} already exists"}), 409
        content = f"""# Activity — {title}

*Concept: {concept}*

## Task

1. TODO: concrete, numbered step
"""
        act_dir.mkdir(exist_ok=True)
        target.write_text(content)
        _, act_body = _parse_activity(content)
        synced = _sync_activity_toggle(topic, path, file, title, act_body)
        return jsonify({"created": f"activities/{file}", "readme_synced": synced})

    if op == "save":
        file = body.get("file", "")
        content = body.get("content", "")
        if not FILE_RE.match(f"activities/{file}"):
            return jsonify({"error": "invalid activity file"}), 400
        if content and not content.endswith("\n"):
            content += "\n"
        title, act_body = _parse_activity(content)
        if not title:
            return jsonify({"error": "activity must start with '# Activity — [Title]'"}), 400
        act_dir.mkdir(exist_ok=True)
        (act_dir / file).write_text(content)
        synced = _sync_activity_toggle(topic, path, file, title, act_body)
        broken = scan_file_links(act_dir / file)
        return jsonify({"saved": f"activities/{file}", "readme_synced": synced,
                        "broken_links": broken})

    if op == "delete":
        file = body.get("file", "")
        target = act_dir / file
        if not FILE_RE.match(f"activities/{file}") or not target.exists():
            return jsonify({"error": "unknown activity file"}), 404
        if not body.get("confirm"):
            return jsonify({"error": "missing confirmation"}), 400
        target.unlink()
        removed = _remove_activity_toggle(topic, path, file)
        return jsonify({"deleted": f"activities/{file}", "readme_synced": removed})

    return jsonify({"error": f"unknown op '{op}'"}), 400

@app.route("/api/editor/upload", methods=["POST"])
def api_editor_upload():
    """Upload a packet/worksheet/image into the lesson's assets/ folder.
    Filenames are normalized to kebab-case; returns a ready-to-paste snippet."""
    topic = request.form.get("module", "")
    path = request.form.get("path", "")
    f = request.files.get("file")
    if topic not in list_topics() or not (TOPICS / topic / path).is_dir():
        return jsonify({"error": "unknown lesson"}), 404
    if not f or not f.filename:
        return jsonify({"error": "no file uploaded"}), 400
    stem, ext = os.path.splitext(f.filename)
    ext = ext.lower()
    if ext not in ASSET_EXTS:
        return jsonify({"error": f"file type '{ext}' not allowed "
                                 f"({', '.join(sorted(ASSET_EXTS))})"}), 400
    name = (_kebab(stem) or "file") + ext
    assets = TOPICS / topic / path / "assets"
    assets.mkdir(exist_ok=True)
    if (assets / name).exists():
        return jsonify({"error": f"assets/{name} already exists — delete it first "
                                 "or rename your file"}), 409
    f.save(assets / name)
    label = stem.replace("-", " ").replace("_", " ").strip().title()
    snippet = (f"![{label}](assets/{name})"
               if ext in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
               else f"[{label}](assets/{name})")
    return jsonify({"uploaded": f"assets/{name}", "snippet": snippet,
                    "assets": asset_files(topic, path)})

@app.route("/api/editor/asset-delete", methods=["POST"])
def api_editor_asset_delete():
    body = request.get_json(force=True) or {}
    topic, path, name = body.get("topic", ""), body.get("path", ""), body.get("file", "")
    target = TOPICS / topic / path / "assets" / name
    if topic not in list_topics() or not re.match(r"^[A-Za-z0-9._-]+$", name or "") \
            or not target.is_file():
        return jsonify({"error": "unknown asset"}), 404
    # refuse while any markdown in the topic still links to it
    refs = [str(mf.relative_to(ROOT)) for mf in (TOPICS / topic).rglob("*.md")
            if f"assets/{name}" in mf.read_text()]
    if refs:
        return jsonify({"error": "asset is still referenced — remove the links first",
                        "referenced_by": refs}), 409
    if not body.get("confirm"):
        return jsonify({"error": "missing confirmation"}), 400
    target.unlink()
    return jsonify({"deleted": f"assets/{name}", "assets": asset_files(topic, path)})

# ── Frontend ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(str(HERE), "index.html")

if __name__ == "__main__":
    print(f"HW Course Hub → http://127.0.0.1:5050")
    print(f"Repo root: {ROOT}")
    print(f"Finals dir: {FINALS} ({'found' if finals_available() else 'NOT FOUND — finals disabled'})")
    print(f"Canvas token: {'configured' if TOKEN else 'MISSING — Canvas features disabled'}")
    app.run(port=5050, debug=True)
