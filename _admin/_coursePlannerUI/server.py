#!/usr/bin/env python3
"""Local course planner for the curriculum repo — create and edit curated modules.

Serves the same Create Module UI as the course hub (../Admin), but instead of
pushing to Canvas it saves module definitions as JSON into _modules/ and keeps
the readable summaries in _admin/_lessonplans/ in sync. No credentials are
used or required — pushing to Canvas stays in the Admin repo, which holds the
access key.

Usage:
    python3 _admin/_coursePlannerUI/server.py        # http://127.0.0.1:8901

Python 3 standard library only.
"""

import json
import re
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULES_DIR = ROOT / "_modules"
PORT = 8901

sys.path.insert(0, str(ROOT / "_admin" / "_verification"))
from verify import (generate_lessonplan, parse_lessons_md, LESSONPLANS_DIR,  # noqa: E402
                    MD_LINK, HTML_SRC, FENCED_CODE, INLINE_CODE, PRE_BLOCK)
from mdrender import (md_to_html, review_block, ENGINE,  # noqa: E402
                      COURSE_NAME, REPO_LABEL)

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FILE_RE = re.compile(r"^(review/)?[A-Za-z0-9._-]+\.md$|^demos/[A-Za-z0-9._-]+\.html$")


# ── Repo readers (mirror the hub's /api/github/* routes) ──────────────────────

def list_topics():
    # Topic folders are PascalCase; lowercase root dirs (embed/, attachments/)
    # are infrastructure, not topics.
    return sorted(
        d.name for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".") and "_" not in d.name
        and d.name[:1].isupper()
    )


def topic_lessons(name):
    """Lessons of a topic in LESSONS.md order, parsed like the hub does."""
    lessons = []
    for row in parse_lessons_md(ROOT / name):
        day_raw = row["day_raw"]
        range_m = re.match(r"(\d+)\s*[–\-]\s*(\d+)", day_raw)
        if range_m:
            start_day = int(range_m.group(1))
            duration = int(range_m.group(2)) - start_day + 1
        elif day_raw.isdigit():
            start_day, duration = int(day_raw), 1
        else:
            continue  # skip TBD rows
        lessons.append({"day": start_day, "duration": duration,
                        "title": row["title"], "path": row["path"]})
    return lessons


def review_files(module, path):
    review_dir = ROOT / module / path / "review"
    if not review_dir.exists():
        return []
    return sorted(f.name for f in review_dir.iterdir()
                  if f.is_file() and f.suffix == ".md")


def demo_files(module, path):
    demos_dir = ROOT / module / path / "demos"
    if not demos_dir.exists():
        return []
    return sorted(f.name for f in demos_dir.iterdir()
                  if f.is_file() and f.suffix == ".html")


# ── Lesson file viewing/editing ────────────────────────────────────────────────

def resolve_lesson_file(module, path, file):
    """Path-safe resolution of an editable .md inside a lesson (or topic) folder."""
    if module not in list_topics() or not FILE_RE.match(file or ""):
        return None, None
    lesson_dir = (ROOT / module / path).resolve() if path else (ROOT / module).resolve()
    if not lesson_dir.is_dir() or not lesson_dir.is_relative_to(ROOT):
        return None, None
    target = (lesson_dir / file).resolve()
    if not target.is_relative_to(lesson_dir):
        return None, None
    return lesson_dir, target


def lesson_file_listing(module, path):
    lesson_dir = ROOT / module / path if path else ROOT / module
    files = sorted(f.name for f in lesson_dir.iterdir()
                   if f.is_file() and f.suffix == ".md")
    # README first, ASSIGNMENT second, variants after
    files.sort(key=lambda f: {"README.md": 0, "ASSIGNMENT.md": 1}.get(f, 2))
    return {
        "files": files,
        "review": [f"review/{f}" for f in review_files(module, path)],
        "demos": [f"demos/{f}" for f in demo_files(module, path)],
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


# ── Saved module validation ────────────────────────────────────────────────────

def validate_module(mod):
    problems = []
    for key in ("name", "slug", "topic_names", "assignments"):
        if not mod.get(key):
            problems.append(f"missing required field '{key}'")
    slug = mod.get("slug", "")
    if slug and not SLUG_RE.match(slug):
        problems.append(f"slug '{slug}' must be kebab-case (a-z, 0-9, -)")
    for t in mod.get("topic_names", []):
        if not (ROOT / t).is_dir():
            problems.append(f"topic '{t}' is not a folder in the repo")
    for a in mod.get("assignments", []):
        if not a.get("placeholder"):
            lesson_dir = ROOT / a.get("_module", "") / a.get("path", "")
            if not (lesson_dir / "README.md").exists():
                problems.append(f"lesson '{a.get('_module')}/{a.get('path')}' does not exist")
        revs = a.get("review") or []
        if not isinstance(revs, list):
            revs = [revs]
        for rev in revs:
            rev_file = ROOT / rev.get("module", "") / rev.get("path", "") / "review" / rev.get("file", "")
            if not rev_file.exists():
                problems.append(
                    f"review '{rev.get('module')}/{rev.get('path')}/review/{rev.get('file')}' does not exist")
    return problems


def saved_summaries():
    out = []
    if not MODULES_DIR.exists():
        return out
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
    return out


# ── HTTP handler ───────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def _json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, path):
        text = path.read_text(encoding="utf-8")
        text = text.replace("__COURSE_NAME__", COURSE_NAME).replace("__REPO_LABEL__", REPO_LABEL)
        body = text.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # keep the terminal quiet

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        parts = [unquote(p) for p in url.path.strip("/").split("/") if p]

        if url.path == "/":
            return self._html(HERE / "index.html")
        if url.path == "/api/topics":
            return self._json({"topics": list_topics()})
        if len(parts) == 3 and parts[0] == "api" and parts[1] == "topics":
            name = parts[2]
            if name not in list_topics():
                return self._json({"error": f"topic '{name}' not found"}, 404)
            return self._json({"name": name, "assignments": topic_lessons(name)})
        if url.path == "/api/reviews":
            module = q.get("module", [""])[0]
            path = q.get("path", [""])[0]
            if not module:
                return self._json({"error": "module param required"}, 400)
            return self._json({"files": review_files(module, path)})
        if url.path == "/api/lesson-files":
            module = q.get("module", [""])[0]
            path = q.get("path", [""])[0]
            if module not in list_topics() or not (ROOT / module / path).is_dir():
                return self._json({"error": "lesson not found"}, 404)
            return self._json(lesson_file_listing(module, path))
        if url.path == "/api/file":
            module = q.get("module", [""])[0]
            path = q.get("path", [""])[0]
            file = q.get("file", [""])[0]
            _, target = resolve_lesson_file(module, path, file)
            if target is None:
                return self._json({"error": "invalid file"}, 400)
            if not target.exists():
                return self._json({"content": "", "exists": False})
            return self._json({"content": target.read_text(), "exists": True})
        if url.path == "/api/saved":
            return self._json({"modules": saved_summaries()})
        if len(parts) == 3 and parts[0] == "api" and parts[1] == "saved":
            jf = MODULES_DIR / f"{parts[2]}.json"
            if not SLUG_RE.match(parts[2]) or not jf.exists():
                return self._json({"error": "not found"}, 404)
            return self._json(json.loads(jf.read_text()))
        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        url = urlparse(self.path)
        parts = [unquote(p) for p in url.path.strip("/").split("/") if p]
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")

        if url.path == "/api/render":
            # Compose the HTML exactly the way the hub uploads it to Canvas
            html_parts = []
            engine = ENGINE
            if body.get("review_markdown"):
                rev_html, engine = md_to_html(body["review_markdown"])
                html_parts.append(review_block(rev_html))
            content_html, engine = md_to_html(body.get("markdown", ""), body.get("base_path", ""))
            html_parts.append(content_html)
            return self._json({"html": "\n".join(html_parts), "engine": engine})
        if url.path == "/api/file":
            module, path, file = body.get("module", ""), body.get("path", ""), body.get("file", "")
            _, target = resolve_lesson_file(module, path, file)
            if target is None:
                return self._json({"error": "invalid file"}, 400)
            target.parent.mkdir(parents=True, exist_ok=True)  # review/ may not exist yet
            content = body.get("content", "")
            if content and not content.endswith("\n"):
                content += "\n"
            target.write_text(content)
            # Link scanning is a markdown check; demo .html saves skip it
            broken = scan_file_links(target) if target.suffix == ".md" else []
            return self._json({"saved": f"{module}/{path + '/' if path else ''}{file}",
                               "broken_links": broken})
        if len(parts) == 3 and parts[0] == "api" and parts[1] == "saved":
            slug = parts[2]
            if not SLUG_RE.match(slug):
                return self._json({"error": "invalid slug"}, 400)
            body["slug"] = slug
            # This UI doesn't render "Additional Day" placeholder entries added
            # from the hub's Module Planner — merge any back in from the prior
            # save instead of silently dropping them (see CLAUDE.md "Placeholder
            # ('Additional Day') entries").
            prior_file = MODULES_DIR / f"{slug}.json"
            if prior_file.exists():
                try:
                    prior = json.loads(prior_file.read_text())
                except json.JSONDecodeError:
                    prior = {}
                placeholders = [a for a in prior.get("assignments", []) if a.get("placeholder")]
                if placeholders:
                    body["assignments"] = sorted(
                        list(body.get("assignments", [])) + placeholders,
                        key=lambda a: a.get("day", 0))
            problems = validate_module(body)
            if problems:
                return self._json({"error": "validation failed", "problems": problems}, 422)
            body["updated"] = date.today().isoformat()
            MODULES_DIR.mkdir(exist_ok=True)
            (MODULES_DIR / f"{slug}.json").write_text(json.dumps(body, indent=2) + "\n")
            LESSONPLANS_DIR.mkdir(parents=True, exist_ok=True)
            (LESSONPLANS_DIR / f"{slug}.md").write_text(generate_lessonplan(body))
            return self._json({"saved": slug, "updated": body["updated"]})
        return self._json({"error": "not found"}, 404)

    def do_DELETE(self):
        url = urlparse(self.path)
        parts = [unquote(p) for p in url.path.strip("/").split("/") if p]
        if len(parts) == 3 and parts[0] == "api" and parts[1] == "saved" and SLUG_RE.match(parts[2]):
            jf = MODULES_DIR / f"{parts[2]}.json"
            plan = LESSONPLANS_DIR / f"{parts[2]}.md"
            if not jf.exists():
                return self._json({"error": "not found"}, 404)
            jf.unlink()
            if plan.exists():
                plan.unlink()
            return self._json({"deleted": parts[2]})
        return self._json({"error": "not found"}, 404)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"{COURSE_NAME} course planner → http://127.0.0.1:{PORT}")
    print(f"Repo root: {ROOT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
