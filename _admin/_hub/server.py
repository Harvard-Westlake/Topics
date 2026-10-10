#!/usr/bin/env python3
"""HW Course Hub — one app for Canvas courses, year schedules, and module planning.

Serves a tabbed UI at http://127.0.0.1:5050 :
  Courses        — Canvas course list, grades, and the Create Module drawer
  Year Schedule  — per-teacher drag-and-drop year plans (_admin/_schedules/<name>.json)
  Module Planner — create/edit curated modules (_modules/<slug>.json) with file editor
  Module Editor  — edit the topic folders themselves (lessons, activities, reviews,
                   uploads) with structural ops that keep every index file in step
  Syllabus       — renders the repo's live SYLLABUS.md

This curriculum repo is the source of truth for all content. The private
sibling Admin repo holds final exams; syncing a test/final day to Canvas creates a
placeholder assignment only — exam content never leaves the private repo.

Per-teacher setup:
    cp .env.example .env          # at the repo root, then paste YOUR Canvas token
    pip3 install -r _admin/_hub/requirements.txt
    python3 _admin/_hub/server.py

The app runs without a token too — the Planner and Schedule tabs are fully
credential-free; only Canvas calls need HUB_TOKEN.
"""
from flask import Flask, jsonify, request, send_file, abort
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import requests, os, sys, json, time, re, html, shutil, uuid, hashlib, subprocess, tempfile
from urllib.parse import urlencode
import markdown as md_lib
from icsimport import compress_calendar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # the Topics repo root

# Per-teacher secrets: repo-root .env first, then legacy ../Admin/.env fallback.
# An empty HUB_TOKEN= placeholder in the root .env must not shadow the fallback.
load_dotenv(ROOT / ".env")
if not os.environ.get("HUB_TOKEN"):
    load_dotenv(ROOT.parent / "Admin" / ".env", override=True)

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

# Repo tooling shared with the verifier and the standalone planner
sys.path.insert(0, str(ROOT / "_admin" / "_verification"))
sys.path.insert(0, str(ROOT / "_admin" / "_coursePlannerUI"))
from verify import (generate_lessonplan, LESSONPLANS_DIR,               # noqa: E402
                    MD_LINK, HTML_SRC, FENCED_CODE, INLINE_CODE, PRE_BLOCK,
                    review_labels, review_label_for)
from mdrender import (md_to_html as planner_md_to_html,                 # noqa: E402
                      review_block as planner_review_block,
                      ENGINE as PLANNER_ENGINE,
                      COURSE_NAME, REPO_LABEL,
                      GITHUB_REPO, GITHUB_BRANCH, GITHUB_RAW, GITHUB_BLOB, PAGES_URL)

# Private sibling Exams repo: <EXAMS_CLASS>/<Topic>/Quizzes/<slug>/ quiz folders (see "Quizzes" below)
EXAMS_DIR = Path(os.environ.get("EXAMS_DIR") or (ROOT.parent / "Exams"))
EXAMS_CLASS = os.environ.get("EXAMS_CLASS") or REPO_LABEL
NEW_QUIZZES_BASE = BASE.replace("/api/v1", "/api/quiz/v1")

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

# Fenced code blocks nested inside list items (indented fences). GitHub renders
# them fine, but python-markdown's fenced_code extension only recognizes fences
# at column 0 — an indented fence collapses into a run-on paragraph, destroying
# the code's whitespace and swallowing generics like ArrayList<Entry> as HTML
# tags. Stash each indented fence before conversion and splice the rendered
# <pre><code> back in afterward. The placeholder keeps at least 4 spaces of
# indentation so python-markdown leaves it inside the surrounding list item.
# Must stay in lockstep with ../_coursePlannerUI/mdrender.py.
_INDENTED_FENCE_RE = re.compile(
    r"^([ \t]+)```([^\n]*)\n(.*?)\n[ \t]*```[ \t]*$", re.MULTILINE | re.DOTALL)

def _stash_indented_fences(text):
    fences = []

    def stash(m):
        indent, lang, body = m.group(1), m.group(2).strip(), m.group(3)
        lines = [ln[len(indent):] if ln.startswith(indent) else ln
                 for ln in body.split("\n")]
        escaped = html.escape("\n".join(lines), quote=False)
        cls = f' class="language-{lang}"' if lang else ""
        fences.append(f"<pre><code{cls}>{escaped}\n</code></pre>")
        pad = indent if len(indent.expandtabs()) >= 4 else "    "
        return f"{pad}«fence{len(fences) - 1}»"

    return _INDENTED_FENCE_RE.sub(stash, text), fences

def _restore_fences(rendered, fences):
    def put(m):
        return fences[int(m.group(1))]
    rendered = re.sub(r"<p>«fence(\d+)»</p>", put, rendered)
    return re.sub(r"«fence(\d+)»", put, rendered)

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

    text, fences = _stash_indented_fences(text)
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
    rendered = md_lib.markdown(text, extensions=["tables", "fenced_code", "toc"])
    return _restore_math(_restore_fences(rendered, fences), math)

def review_block_html(rev_html):
    """Wrap rendered review markdown in the purple callout used on Canvas."""
    return ('<div style="background:#f6f8fa;border-left:4px solid #8957e5;'
            'padding:12px 16px;margin-bottom:20px;border-radius:0 6px 6px 0">'
            '<p style="font-weight:600;color:#8957e5;margin:0 0 8px 0">&#9997;&nbsp;Review</p>'
            + rev_html + '</div>')

# ── Live lesson view (view.html on GitHub Pages) ───────────────────────────────
# Canvas never holds rendered lesson content any more. Every assignment/page the
# hub creates carries a link to (and an embedded frame of) the repo's serverless
# viewer, which fetches the markdown from GitHub for one git ref and renders it
# in the browser. Content edits therefore reach Canvas the moment they are
# pushed — no re-sync — and each teacher's schedule names the ref (branch or
# tag) its course follows, so two teachers can run different branches from one
# repo and take main's changes only when they merge them.

REF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")

def schedule_ref(sched):
    """Git ref a schedule's Canvas links follow (default: the repo's main branch)."""
    ref = (sched or {}).get("ref") or ""
    return ref.strip() if REF_RE.match(ref.strip() or "") else GITHUB_BRANCH

def viewer_url(ref, lesson=None, path=None, reviews=(), homework=True, local=False):
    """URL of view.html for one lesson day or one file.

    lesson  — 'Module/Lesson': composed class day (README, reviews, ASSIGNMENT.md)
    path    — 'Module/Lesson/README.md': a single file
    reviews — repo paths of review fragments to stack as purple blocks
    homework=False leaves ASSIGNMENT.md out (content page / no-homework day)
    local=True targets this hub (reads the working tree via /raw/) — for previews only
    """
    params = []
    if local:
        params.append(("src", "/raw/"))
    params.append(("ref", ref or GITHUB_BRANCH))
    if lesson:
        params.append(("lesson", lesson))
    if path:
        params.append(("path", path))
    for r in reviews:
        params.append(("review", r))
    if not homework:
        params.append(("hw", "0"))
    root = "" if local else PAGES_URL
    return f"{root}/view.html?{urlencode(params, safe='/')}"

def _review_paths(review_ref):
    """Repo paths of the review fragments in a `review` field (one ref or a list)."""
    out = []
    for rev in _review_refs({"review": review_ref}):
        if rev.get("module") and rev.get("path") and rev.get("file"):
            out.append(f"{rev['module']}/{rev['path']}/review/{rev['file']}")
    return out

# HW brand red, matching the hub's light-theme primary buttons. Canvas strips
# :hover rules, so the gold hover state can't follow it into a description.
STUB_BUTTON_BG = "#DA0016"
_STUB_STYLE_RE = re.compile(r"da0016|218,\s*0,\s*22", re.IGNORECASE)

def stub_style_current(description):
    """True when a live-view stub already carries the current button style."""
    return bool(_STUB_STYLE_RE.search(description or ""))

def live_stub_html(url, has_homework=True):
    """The whole Canvas description: a button to the live page plus an embedded
    frame of it. Inline styles only — Canvas strips classes and scripts."""
    what = "lesson and assignment" if has_homework else "lesson"
    u = html.escape(url, quote=True)
    return (f'<p><a href="{u}" target="_blank" rel="noopener" '
            f'style="display:inline-block;background:{STUB_BUTTON_BG};color:#ffffff;font-weight:600;'
            'padding:8px 14px;border-radius:6px;text-decoration:none">'
            f'&#128214;&nbsp;Open the {what}</a> '
            '<span style="color:#57606a;margin-left:8px">Always the current version, '
            f'straight from the {html.escape(REPO_LABEL)} repo.</span></p>\n'
            f'<iframe src="{u}" title="Lesson" width="100%" height="900" loading="lazy" allowfullscreen '
            'style="width:100%;height:900px;border:1px solid #d0d7de;border-radius:6px;background:#ffffff">'
            '</iframe>')

def live_description(ref, module_dir, lesson_path, review_ref, include_assignment=True):
    """Canvas description for a class day: the live-view stub for the lesson
    (README + attached reviews + ASSIGNMENT.md unless include_assignment is
    False), or '' when there is nothing to show."""
    lesson = f"{module_dir}/{lesson_path}" if module_dir and lesson_path else None
    reviews = _review_paths(review_ref)
    if not lesson and not reviews:
        return ""
    has_hw = bool(include_assignment and lesson
                  and (TOPICS / module_dir / lesson_path / "ASSIGNMENT.md").exists())
    url = viewer_url(ref, lesson=lesson, reviews=reviews, homework=include_assignment)
    return live_stub_html(url, has_homework=has_hw)

_VIEWER_REF_RE = re.compile(r"view\.html\?(?:[^\"'<>]*?&(?:amp;)?)?ref=([^&\"'<>;]+)")

def viewer_ref_in(description):
    """Git ref a Canvas description's live-view link follows, or None when the
    description is a pre-live-view snapshot (or has no lesson content)."""
    m = _VIEWER_REF_RE.search(description or "")
    return html.unescape(m.group(1)) if m else None

# ── Quizzes (private Exams repo) ───────────────────────────────────────────────
# Quiz content never enters this repo. The sibling Exams checkout holds
# <EXAMS_CLASS>/<Topic>/Quizzes/<slug>/ folders encrypted at rest (examcrypt);
# the only plaintext the hub reads is quiz.meta.json — an opaque quiz_id, title,
# points, question count. A curated module row stores just that quiz_id
# ({"placeholder": true, "kind": "quiz", "quiz_id": …}); the Planner offers the
# quizzes below as the choices for it, and sync places the quiz by id.

def exams_available():
    return (EXAMS_DIR / EXAMS_CLASS).is_dir()

def list_quizzes():
    out = []
    base = EXAMS_DIR / EXAMS_CLASS
    if not base.is_dir():
        return out
    for meta_path in sorted(base.glob("*/Quizzes/*/quiz.meta.json")):
        try:
            meta = json.loads(meta_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if not meta.get("quiz_id"):
            continue
        folder = meta_path.parent
        unlocked = (folder / "quiz.json").exists()
        live_hash = None
        if unlocked:
            try:
                live_hash = _quiz_content_hash(json.loads((folder / "quiz.json").read_text()))
            except (OSError, json.JSONDecodeError, TypeError):
                live_hash = None
        meta_hash = meta.get("content_hash") or None
        out.append({"quiz_id": str(meta["quiz_id"]), "title": meta.get("title") or folder.name,
                    "topic": meta.get("topic") or folder.parent.parent.name, "slug": folder.name,
                    "lesson": meta.get("lesson"), "points": meta.get("points"),
                    "questions": meta.get("questions"),
                    "folder": str(folder.relative_to(EXAMS_DIR)),
                    "unlocked": unlocked,
                    "locked": (folder / "exam-content.tar.enc").exists(),
                    # the fingerprint of the questions: the unlocked quiz.json when present (what a
                    # push would send), else what build_qti.py recorded in the meta at the last build
                    "version": live_hash or meta_hash, "meta_version": meta_hash,
                    "meta_stale": bool(live_hash and meta_hash and live_hash != meta_hash)})
    return out

def quiz_by_id(quiz_id):
    return next((q for q in list_quizzes() if q["quiz_id"] == str(quiz_id)), None)

@app.route("/api/quizzes")
def api_quizzes():
    return jsonify({"available": exams_available(), "dir": str(EXAMS_DIR / EXAMS_CLASS),
                    "quizzes": list_quizzes()})

_QUIZ_ID_RE = re.compile(r"Quiz ID:\s*(?:<code>)?([0-9a-f]{8,64})")

def quiz_id_in(description):
    """The quiz_id marker a synced quiz assignment's description carries, or None."""
    m = _QUIZ_ID_RE.search(description or "")
    return m.group(1) if m else None

def _quiz_content_hash(spec):
    """Fingerprint of a quiz.json — the same value Exams/Tools/qti/build_qti.py
    writes to quiz.meta.json as `content_hash` (keep the two in lockstep).
    Canonical JSON, so reformatting the file does not change the version."""
    canon = json.dumps(spec, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:12]

_QUIZ_VERSION_RE = re.compile(r"Quiz version:\s*(?:<code>)?([0-9a-f]{6,64})")
_QUIZ_VERSION_P_RE = re.compile(r"\s*<p[^>]*>Quiz version:.*?</p>", re.S)

def quiz_version_in(description):
    """The content version a pushed New Quiz's description was stamped with
    (`Quiz version: <hash>`), or None for a placeholder or a pre-versioning push."""
    m = _QUIZ_VERSION_RE.search(description or "")
    return m.group(1) if m else None

def _with_quiz_version(description, version):
    """The description with its version stamp replaced (or added). Written only on
    assignments that really carry the questions, so the sync planner can tell a
    pushed quiz whose questions are behind the Exams repo from a current one."""
    base = _QUIZ_VERSION_P_RE.sub("", description or "")
    if not version:
        return base
    return base + f'<p style="color:#57606a;font-size:12px">Quiz version: <code>{html.escape(str(version))}</code></p>'

def _asgn_identity(a):
    """Stable identity of a Canvas assignment as the sync planner sees it."""
    if a.get("lesson"):
        return f"lesson:{a['lesson']}"
    if a.get("quiz"):
        return f"quiz:{a['quiz']}"
    return None

def _new_quiz_items(spec):
    """Canvas New Quizzes item payloads for a quiz.json (the Exams repo's quiz
    format: `topical` essays, `features` × (yes/no, 1–5, pointed essay), one
    reflection). Part headers are folded into the first item of each part."""
    pts = spec["points"]

    def essay(body, points, header=""):
        return {"entry_type": "Item", "points_possible": points,
                "entry": {"title": "", "item_body": (header or "") + body, "interaction_type_slug": "essay",
                          "interaction_data": {"rce": True, "essay": None, "word_count": False,
                                               "file_upload": False, "spell_check": False,
                                               "word_limit_enabled": False},
                          "properties": {}, "scoring_data": {"value": ""}, "scoring_algorithm": "None"}}

    def choice(body, points, choices, header=""):
        ids = [str(uuid.uuid4()) for _ in choices]
        return {"entry_type": "Item", "points_possible": points,
                "entry": {"title": "", "item_body": (header or "") + body, "interaction_type_slug": "choice",
                          "interaction_data": {"choices": [
                              {"id": cid, "position": i + 1, "item_body": f"<p>{html.escape(str(c))}</p>"}
                              for i, (cid, c) in enumerate(zip(ids, choices))]},
                          "properties": {"shuffle_rules": {"choices": {"shuffled": False}},
                                         "vary_points_by_answer": False},
                          "scoring_data": {"value": ids[0]}, "scoring_algorithm": "Equivalence"}}

    items = []
    for n, q in enumerate(spec.get("topical", []), start=1):
        items.append(essay(q["prompt"], pts["topical"], spec.get("topical_header", "") if n == 1 else ""))
    for n, f in enumerate(spec.get("features", []), start=1):
        lead = (f"<p><strong>Behavior {n} — {html.escape(f['name'])}.</strong> "
                f"<em>{html.escape(f['description'])}</em></p>")
        items.append(choice(lead + f"<p>{html.escape(spec['yes_no_prompt'])}</p>", pts["yes_no"],
                            spec["yes_no_choices"], spec.get("self_assessment_header", "") if n == 1 else ""))
        items.append(choice(f"<p><strong>Behavior {n} — {html.escape(f['name'])}.</strong> "
                            f"{html.escape(spec['confidence_prompt'])}</p>", pts["confidence"],
                            spec["confidence_choices"]))
        items.append(essay(f"<p><strong>Behavior {n} — {html.escape(f['name'])}.</strong> {f['pointed']}</p>",
                           pts["pointed"]))
    if spec.get("reflection"):
        items.append(essay(spec["reflection"]["prompt"], pts["reflection"], spec.get("reflection_header", "")))
    return items

def _quiz_payload(e):
    """(items, version, error) for the quiz an expected item carries — read from
    the UNLOCKED quiz.json in the Exams checkout, never from a cache, so what
    reaches Canvas is always the file as it is on disk right now."""
    q = quiz_by_id(e["quiz"]["quiz_id"])
    if not q or not q["unlocked"]:
        return None, None, "quiz folder is locked — run `examcrypt.py unlock` in the Exams repo first"
    try:
        spec = json.loads((EXAMS_DIR / q["folder"] / "quiz.json").read_text())
        return _new_quiz_items(spec), _quiz_content_hash(spec), None
    except Exception as ex:
        return None, None, f"could not read quiz.json: {ex}"

def _quiz_has_submissions(course_id, asgn_id):
    subs = canvas_paged(f"/courses/{course_id}/assignments/{asgn_id}/submissions")
    return any(s.get("submitted_at") or s.get("workflow_state") not in (None, "unsubmitted") for s in subs)

def _refresh_new_quiz_items(course_id, asgn_id, items):
    """Replace every question of an existing New Quiz with `items` (the current
    quiz.json), in order. Refused once any student has submitted — a quiz with
    submissions is graded against the questions it had. Returns an error or None."""
    try:
        if _quiz_has_submissions(course_id, asgn_id):
            return ("students have already submitted this quiz — its questions were left as they are "
                    "(change them in Canvas by hand if you must)")
    except Exception as ex:
        return f"could not check for submissions: {ex}"
    r = requests.get(f"{NEW_QUIZZES_BASE}/courses/{course_id}/quizzes/{asgn_id}/items", headers=hdrs())
    if not r.ok:
        return f"New Quizzes API {r.status_code} listing items: {r.text[:200]}"
    old = r.json() if isinstance(r.json(), list) else []
    failed = []
    for it in old:
        dr = requests.delete(f"{NEW_QUIZZES_BASE}/courses/{course_id}/quizzes/{asgn_id}/items/{it.get('id')}",
                             headers=hdrs())
        if not dr.ok:
            failed.append(f"remove item {it.get('id')}: {dr.status_code}")
    if failed:
        return f"{len(failed)} old item(s) could not be removed, new questions not pushed: " + "; ".join(failed[:3])
    for pos, it in enumerate(items, start=1):
        it["position"] = pos
        ir = requests.post(f"{NEW_QUIZZES_BASE}/courses/{course_id}/quizzes/{asgn_id}/items",
                           headers=hdrs(), json={"item": it})
        if not ir.ok:
            failed.append(f"item {pos}: {ir.status_code} {ir.text[:100]}")
    if failed:
        return f"{len(failed)} of {len(items)} new items failed: " + "; ".join(failed[:3])
    return None

def _push_new_quiz(course_id, e, due_at, unlock_at):
    """Create a Canvas New Quiz (an assignment) with the questions from the
    quiz's UNLOCKED quiz.json, stamped with their content version. Returns
    (assignment_id, error) — an id with an error means the quiz exists but some
    items failed."""
    items, version, qerr = _quiz_payload(e)
    if qerr:
        return None, qerr
    description = _with_quiz_version(e["description"], version)
    payload = {"quiz": {"title": e["title"], "points_possible": e["points"], "instructions": description,
                        "quiz_settings": {
                            "shuffle_answers": False, "shuffle_questions": False,
                            "multiple_attempts": {"multiple_attempts_enabled": False},
                            "result_view_settings": {
                                "result_view_restricted": True, "display_points_awarded": True,
                                "display_points_possible": True, "display_items": False,
                                "display_item_response": False, "display_item_response_correctness": False,
                                "display_item_correct_answer": False, "display_item_feedback": False}}}}
    if e.get("due"):
        payload["quiz"]["due_at"] = due_at(e["due"])
    if e.get("unlock"):
        payload["quiz"]["unlock_at"] = unlock_at(e["unlock"])
    r = requests.post(f"{NEW_QUIZZES_BASE}/courses/{course_id}/quizzes", headers=hdrs(), json=payload)
    if not r.ok:
        return None, f"New Quizzes API {r.status_code}: {r.text[:300]}"
    asgn_id = r.json().get("id")
    # The New Quizzes API drops `instructions` from the Canvas assignment, so the
    # Quiz ID marker the sync planner matches on has to be set through the regular
    # Assignments API (verified to persist on a quiz_lti assignment). Best effort.
    requests.put(f"{BASE}/courses/{course_id}/assignments/{asgn_id}", headers=hdrs(),
                 json={"assignment": {"description": description}})
    failed = []
    for pos, it in enumerate(items, start=1):
        it["position"] = pos
        ir = requests.post(f"{NEW_QUIZZES_BASE}/courses/{course_id}/quizzes/{asgn_id}/items",
                           headers=hdrs(), json={"item": it})
        if not ir.ok:
            failed.append(f"item {pos}: {ir.status_code} {ir.text[:100]}")
    if failed:
        return asgn_id, f"quiz created but {len(failed)} of {len(items)} items failed: " + "; ".join(failed[:3])
    return asgn_id, None

# ── Canvas helpers ─────────────────────────────────────────────────────────────

def _day_sub_suffix(a):
    """'.0' / '.1' sub-index for a ½-day assignment sharing its class day —
    Canvas names become unit.day.0 / unit.day.1. Empty for full-day items."""
    if a and (a.get("duration") == 0.5 or a.get("sub") is not None):
        return f".{a.get('sub') or 0}"
    return ""

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

def _quiz_kind(a):
    """Classify a Canvas assignment as a 'new' or 'classic' quiz, or None.

    Mirrors classify() in Exams/Tools/quiz-export/export_quiz.py so the Courses
    tab can show an export control only on quiz rows.
    """
    if a.get("is_quiz_lti_assignment"):
        return "new"
    if a.get("quiz_id"):
        return "classic"
    types = a.get("submission_types") or []
    if "online_quiz" in types:
        return "classic"
    if "external_tool" in types:
        url = (a.get("external_tool_tag_attributes") or {}).get("url", "")
        if "quiz-lti" in url:
            return "new"
    return None


# The quiz-response exporter lives in the private Exams repo, not here; the hub
# runs it as a subprocess (same interpreter, so it has requests) and streams back
# the CSV. Keeping the logic in Exams matches how the hub reads other Exams content.
QUIZ_EXPORT_SCRIPT = EXAMS_DIR / "Tools" / "quiz-export" / "export_quiz.py"


@app.route("/api/courses/<int:course_id>/quiz-export/<int:assignment_id>")
def api_quiz_export(course_id, assignment_id):
    err = no_token()
    if err:
        return err
    if not QUIZ_EXPORT_SCRIPT.exists():
        return jsonify({"error": f"quiz-export tool not found at {QUIZ_EXPORT_SCRIPT} — "
                        "pull the Exams repo next to this one."}), 404
    out_dir = tempfile.mkdtemp(prefix="quiz-export-")
    out_path = Path(out_dir) / f"{course_id}-{assignment_id}.csv"
    try:
        proc = subprocess.run(
            [sys.executable, str(QUIZ_EXPORT_SCRIPT),
             "--course", str(course_id), "--assignment", str(assignment_id),
             "--out", str(out_path), "--emit-path"],
            capture_output=True, text=True, env=os.environ, timeout=300)
    except subprocess.TimeoutExpired:
        shutil.rmtree(out_dir, ignore_errors=True)
        return jsonify({"error": "The export timed out after 5 minutes."}), 504

    if proc.returncode == 2:
        # Unsupported quiz (New Quiz, or not a quiz): the reason is on stderr.
        shutil.rmtree(out_dir, ignore_errors=True)
        reason = (proc.stderr or proc.stdout).strip() or "This quiz can't be exported."
        return jsonify({"error": reason, "unsupported": True}), 422
    if proc.returncode != 0:
        shutil.rmtree(out_dir, ignore_errors=True)
        return jsonify({"error": (proc.stderr or proc.stdout).strip()[:2000]
                        or "Export failed."}), 500

    produced = proc.stdout.strip().splitlines()
    path = Path(produced[-1]) if produced else out_path
    if not path.exists():
        shutil.rmtree(out_dir, ignore_errors=True)
        return jsonify({"error": "The export produced no file."}), 500
    resp = _no_store(send_file(path, mimetype="text/csv", as_attachment=True,
                               download_name=path.name))

    @resp.call_on_close
    def _cleanup():
        shutil.rmtree(out_dir, ignore_errors=True)
    return resp


@app.route("/api/courses/<int:course_id>/assignments")
def api_assignments(course_id):
    err = no_token()
    if err:
        return err
    def fetch():
        rows = canvas_paged(f"/courses/{course_id}/assignments", {"order_by": "due_at"})
        return [{"id": a["id"], "name": a["name"], "due_at": a.get("due_at"),
                 "points": a.get("points_possible"), "html_url": a.get("html_url"),
                 "quiz_kind": _quiz_kind(a)} for a in rows]
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

def _drawer_review_refs(a):
    """Review references a Create-Module drawer row carries: `review_refs`
    (all refs of a saved module row) or the legacy single `review_ref`."""
    return a.get("review_refs") or ([a["review_ref"]] if a.get("review_ref") else [])

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
    ref         = body.get("ref") or GITHUB_BRANCH
    if not REF_RE.match(ref):
        return jsonify({"error": f"invalid git ref '{ref}'"}), 400

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
        # (a ½-day item is due on its own day: max() keeps the offset at day-1)
        offset = int(day) - 1 + max(int(duration) - 1, 0)
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
                pname = f"{unit_num}.{a['day']}{_day_sub_suffix(a)}: {a['title']}"
                parts = []
                stub = live_description(ref, "", "", _drawer_review_refs(a), include_assignment=False)
                if stub:
                    parts.append(stub)
                elif a.get("review_markdown"):      # content-only review (no repo ref) — baked
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
        name     = f"{unit_num}.{day}{_day_sub_suffix(a)}: {a['title']}"

        # Build HTML description: the live-view stub (lesson + referenced
        # reviews + ASSIGNMENT.md, fetched from GitHub when the student opens
        # it). A review that arrived as bare markdown with no repo reference
        # can't be linked, so it is baked in below the stub as before.
        html_parts = []
        mod_dir  = a.get("_module", "")
        lesson_p = a.get("path", "")
        refs = _drawer_review_refs(a)
        stub = live_description(ref, mod_dir, lesson_p, refs,
                                include_assignment=not a.get("no_assignment"))
        if stub:
            html_parts.append(stub)
        if not refs:
            for review_md in (a.get("review_markdowns")
                              or ([a["review_markdown"]] if a.get("review_markdown") else [])):
                html_parts.append(review_block_html(md_to_html(review_md)))

        # 'no assignment' day: lesson content becomes a Canvas Page — no
        # homework spec, no points, no due date
        if a.get("no_assignment"):
            page, perr = create_canvas_page(course_id, module_id, name, "\n".join(html_parts))
            if perr:
                errors.append({"name": name, "error": perr})
            else:
                results.append(page)
            continue

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

    for key in [f"modules_{course_id}", f"assignments_{course_id}", f"assignments_ref_{course_id}"]:
        p = cache_path(key)
        if p.exists():
            p.unlink()
    for p in CACHE.glob(f"module_items_{course_id}_*.json"):
        p.unlink()

    return jsonify({"module_id": module_id, "unit_number": unit_num,
                    "created": results, "errors": errors})

# ── Topics repo readers ────────────────────────────────────────────────────────

def list_topics():
    # Topic folders are PascalCase; lowercase root dirs (embed/, attachments/)
    # are infrastructure, not topics.
    return sorted(d.name for d in TOPICS.iterdir()
                  if d.is_dir() and not d.name.startswith(".") and "_" not in d.name
                  and d.name[:1].isupper())

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
    # Resolve review references to markdown so the drawer can use them directly.
    # A row may carry several attached reviews — the drawer's single-review
    # pickers replay only a lone ref; multiple refs travel as resolved markdown.
    for a in mod.get("assignments", []):
        refs = _review_refs(a)
        a.pop("review", None)
        contents = []
        for rev in refs:
            rf = TOPICS / rev["module"] / rev["path"] / "review" / rev["file"]
            if rf.exists():
                contents.append(rf.read_text())
        if contents:
            a["review_markdowns"] = contents
            a["review_markdown"] = "\n\n---\n\n".join(contents)  # legacy single field
            a["review_refs"] = refs           # live view links reviews by reference
            if len(refs) == 1:
                a["review_ref"] = refs[0]
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

def _review_refs(a):
    """An assignment's review attachments as a list. The `review` field holds
    one ref (legacy saves) or a list of refs (multiple reviews stacked on one
    day) — every consumer goes through here so both shapes just work."""
    rev = a.get("review")
    if not rev:
        return []
    return rev if isinstance(rev, list) else [rev]

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
        elif a.get("kind") == "quiz":
            qid = a.get("quiz_id")
            if not qid:
                problems.append(f"quiz row '{a.get('title')}' has no quiz_id — pick a quiz in the Planner")
            elif exams_available() and quiz_by_id(qid) is None:
                problems.append(f"quiz_id '{qid}' is not in {EXAMS_DIR / EXAMS_CLASS} — pull the Exams repo, "
                                f"or the quiz was removed")
        for rev in _review_refs(a):
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
    review_mds = body.get("review_markdowns") or \
        ([body["review_markdown"]] if body.get("review_markdown") else [])
    for review_md in review_mds:
        rev_html, engine = planner_md_to_html(review_md)
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
    "ref": "main",                      # git branch/tag this teacher's Canvas links follow (see schedule_ref)
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
    # ceil-style day span: a ½-day item still occupies (part of) its one day
    total = max((a["day"] + max(int(a.get("duration", 1) or 1) - 1, 0) for a in lessons), default=0)
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
            # two ½-day items pair on one day: order them by sub-index (.0 first)
            active.sort(key=lambda x: x.get("sub", 0) if x.get("duration", 1) == 0.5 else 0)
            for j, a in enumerate(active):
                dur, part = a.get("duration", 1), day - a["day"] + 1
                slots.append({"kind": "lesson",
                              "title": a["title"] + (f" — day {part}/{dur}" if dur > 1 else ""),
                              "module_day": day, "part": part, "parts": dur,
                              "co_day": j > 0,
                              "group": f"lesson-{a['day']}-{a.get('sub', '')}-{a.get('path', '')}",
                              "lesson": {"day": a["day"], "duration": dur, "title": a["title"],
                                         "path": a.get("path"), "_module": a.get("_module"),
                                         "sub": a.get("sub"), "kind": a.get("kind"),
                                         "quiz_id": a.get("quiz_id"),
                                         "no_assignment": a.get("no_assignment"),
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
        sched["ref"] = (sched.get("ref") or "").strip() or GITHUB_BRANCH
        if not REF_RE.match(sched["ref"]):
            return jsonify({"error": f"invalid git ref '{sched['ref']}' — use a branch or tag name"}), 400
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

def _lesson_description(ref, module_dir, lesson_path, review_ref, include_assignment=True):
    """Canvas description of a scheduled day — see live_description."""
    return live_description(ref, module_dir, lesson_path, review_ref, include_assignment)

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

# ── Sync planning ──────────────────────────────────────────────────────────────
# What a resolved block should leave on Canvas, matched against what is already
# there. Shared by sync-status (read-only) and sync-block (the upsert), so the
# status dot and the Sync button can never disagree. Canvas items are matched by
# a stable identity — the lesson their live-view link composes — not by title, so
# inserting or removing a day (which renumbers every later "unit.day:" title)
# renames and re-dates the existing items in place instead of duplicating them.
# Nothing is ever deleted: items the schedule no longer expects are unpublished.

_VIEWER_URL_RE = re.compile(r"https?://[^\"'<>\s]*view\.html\?[^\"'<>\s]*")
_VIEWER_LESSON_RE = re.compile(r"view\.html\?(?:[^\"'<>]*?&(?:amp;)?)?lesson=([^&\"'<>;]+)")
_NUMBERED_TITLE_RE = re.compile(r"^\d+\.\d+(?:\.\d)?:\s*")

def viewer_url_in(description):
    """The live-view URL inside a Canvas description, or None."""
    m = _VIEWER_URL_RE.search(description or "")
    return html.unescape(m.group(0)) if m else None

def viewer_lesson_in(description):
    """'Module/Lesson' that a description's live-view link composes, or None."""
    m = _VIEWER_LESSON_RE.search(description or "")
    return html.unescape(m.group(1)) if m else None

def _base_title(name):
    """A Canvas title without its 'unit.day: ' numbering prefix."""
    return _NUMBERED_TITLE_RE.sub("", name or "").strip()

def _same_instant(expected_iso, canvas_iso):
    try:
        e = datetime.fromisoformat(expected_iso)
        c = datetime.fromisoformat(canvas_iso.replace("Z", "+00:00"))
        return abs((e - c).total_seconds()) < 60
    except (ValueError, TypeError, AttributeError):
        return False

def _expected_block_items(block, ref):
    """What syncing this resolved module block should leave on Canvas, in module
    order: [{title, type ('Assignment'|'Page'), identity, base_title, points, due,
    unlock, description, content}]. `identity` survives renumbering:
    'lesson:<Module>/<Lesson>' for anything linking a live lesson view, else
    'page:' / 'test:' / 'final:' plus the un-numbered title."""
    slots = block.get("slots", [])
    unit = block["unit_number"]
    pts = smart_round((block.get("points") or 10) * ((block.get("scale") or 1.15) ** unit))

    def group_end(s):
        dated = [x.get("date") for x in slots
                 if x.get("group") == s.get("group") and x.get("date")]
        return dated[-1] if dated else s.get("date")

    cur_slot = [0]   # index of the slot being expanded — the key the Sync dialog's per-day checkboxes use

    def item(title, type_, identity, points=None, due=None, unlock=None, description="", content=False):
        return {"title": title, "type": type_, "identity": identity, "base_title": _base_title(title),
                "points": points, "due": due, "unlock": unlock, "description": description,
                "content": content, "slot": cur_slot[0]}

    expected = []
    for i, s in enumerate(slots):
        if s.get("part", 1) != 1:
            continue  # later day of a multi-day item — covered by its first day
        cur_slot[0] = i
        day_num = s.get("day_num", i + 1)
        kind = s.get("kind")
        if kind == "lesson" and s.get("lesson"):
            a = s["lesson"]
            name = f"{unit}.{day_num}{_day_sub_suffix(a)}: {a['title']}"
            if not (a.get("_module") and a.get("path")):
                # placeholder: 'quiz' syncs an assignment carrying the quiz_id (or the
                # real New Quiz when pushed); 'page' syncs a Canvas Page (no assignment);
                # 'test' / plain reserve the day number and create nothing
                if a.get("kind") == "quiz" and a.get("quiz_id"):
                    q = quiz_by_id(a["quiz_id"])
                    desc = (f"<p>In-class quiz — {html.escape((q or {}).get('title') or a['title'])}. "
                            "Questions are delivered in Canvas; the source stays in the private Exams repo.</p>"
                            f'<p style="color:#57606a;font-size:12px">Quiz ID: <code>{html.escape(str(a["quiz_id"]))}</code></p>')
                    it = item(name, "Assignment", f"quiz:{a['quiz_id']}", (q or {}).get("points") or 100,
                              group_end(s), s.get("date"), desc)
                    it["quiz"] = {"quiz_id": str(a["quiz_id"]), "known": q is not None,
                                  "unlocked": bool(q and q["unlocked"]), "folder": (q or {}).get("folder"),
                                  "version": (q or {}).get("version"),
                                  "meta_stale": bool(q and q.get("meta_stale"))}
                    expected.append(it)
                    continue
                if a.get("kind") == "page":
                    desc = live_description(ref, "", "", a.get("review"))
                    desc = (desc + "\n" if desc else "") + "<p>In-class day — no assignment due.</p>"
                    expected.append(item(name, "Page", f"page:{a['title']}", description=desc))
                continue
            lesson_id = f"lesson:{a['_module']}/{a['path']}"
            if a.get("no_assignment"):
                # content page instead of homework — no points, no due date
                desc = live_description(ref, a["_module"], a["path"], a.get("review"),
                                        include_assignment=False)
                expected.append(item(name, "Page", lesson_id, description=desc, content=True))
                continue
            expected.append(item(name, "Assignment", lesson_id, pts, group_end(s), s.get("date"),
                                 live_description(ref, a["_module"], a["path"], a.get("review")),
                                 content=True))
        elif kind == "lesson" and s.get("lesson_ref"):
            lref = s["lesson_ref"]
            expected.append(item(f"{unit}.{day_num}: {s.get('base_title') or s['title']}", "Assignment",
                                 f"lesson:{lref.get('module')}/{lref.get('path')}", pts,
                                 group_end(s), s.get("date"),
                                 live_description(ref, lref.get("module"), lref.get("path"), None),
                                 content=True))
        elif kind in ("test", "final"):
            label = "final exam" if kind == "final" else "test"
            base = s.get("base_title") or s["title"]
            expected.append(item(f"{unit}.{day_num}: {base}", "Assignment", f"{kind}:{base}",
                                 s.get("points") or 100, group_end(s), s.get("date"),
                                 f"<p>In-class {label}. Details will be provided in class.</p>"))
        # review / flex / custom / gap days are schedule-only — nothing in Canvas
    return expected

def _canvas_course_state(course_id, ttl):
    """(modules, assignments, module_items_fn): the course as the sync planner
    sees it, read through the normal caches (ttl 0 = live). Descriptions are
    never stored whole — only the live-view link parsed out of them."""
    modules, _, _ = cached(f"modules_{course_id}", ttl, lambda: [
        {"id": m["id"], "name": m["name"], "items_count": m.get("items_count", 0),
         "published": m.get("published"), "position": m.get("position")}
        for m in canvas_paged(f"/courses/{course_id}/modules", {"include[]": "items_count"})])

    def _asgn(a):
        desc = a.get("description")
        return {"id": a["id"], "name": a["name"], "due_at": a.get("due_at"),
                "unlock_at": a.get("unlock_at"), "points": a.get("points_possible"),
                "published": a.get("published"), "html_url": a.get("html_url"),
                "viewer_url": viewer_url_in(desc), "viewer_ref": viewer_ref_in(desc),
                "stub_current": stub_style_current(desc),
                "lesson": viewer_lesson_in(desc), "quiz": quiz_id_in(desc),
                "quiz_version": quiz_version_in(desc),
                "new_quiz": bool(a.get("is_quiz_lti_assignment"))}
    assignments, _, _ = cached(f"assignments_sync_v3_{course_id}", ttl, lambda: [
        _asgn(a) for a in canvas_paged(f"/courses/{course_id}/assignments", {"order_by": "due_at"})])

    def module_items(mid):
        data, _, _ = cached(f"module_items_v2_{course_id}_{mid}", ttl, lambda: [
            {"id": it.get("id"), "title": it.get("title"), "type": it.get("type"),
             "content_id": it.get("content_id"), "page_url": it.get("page_url"),
             "position": it.get("position"), "published": it.get("published")}
            for it in canvas_paged(f"/courses/{course_id}/modules/{mid}/items")])
        return data
    return modules, assignments, module_items

def _invalidate_course_caches(course_id):
    for key in [f"modules_{course_id}", f"assignments_{course_id}",
                f"assignments_ref_{course_id}", f"assignments_sync_{course_id}",
                f"assignments_sync_v3_{course_id}"]:
        p = cache_path(key)
        if p.exists():
            p.unlink()
    for p in list(CACHE.glob(f"module_items_{course_id}_*.json")) + \
             list(CACHE.glob(f"module_items_v2_{course_id}_*.json")):
        p.unlink()

def _quiz_refresh_change(qz, a):
    tail = f"stamped {a['quiz_version']}" if a.get("quiz_version") else "pushed before versioning"
    note = "" if qz.get("unlocked") else " — unlock the quiz folder in ../Exams first"
    return f"quiz questions → version {qz['version']} ({tail}){note}"

def _assignment_changes(e, a, due_at, unlock_at, options=None):
    """Human-readable drift between an expected item and a Canvas assignment
    (empty list = nothing to update). For a quiz day: a pushed New Quiz whose
    stamped version is not the Exams repo's current one needs its questions
    replaced; with options["push_quizzes"], a day that only has a placeholder
    is upgraded to a real New Quiz."""
    ch = []
    if a["name"] != e["title"]:
        ch.append(f"rename from “{a['name']}”")
    if e.get("points") is not None and a.get("points") is not None \
            and float(a["points"]) != float(e["points"]):
        ch.append(f"points {a['points']:g} → {e['points']:g}")
    if e.get("due"):
        exp = due_at(e["due"])
        if exp and not a.get("due_at"):
            ch.append(f"set due date {exp[:10]}")
        elif exp and not _same_instant(exp, a["due_at"]):
            ch.append(f"due {a['due_at'][:10]} → {exp[:10]}")
    if e.get("unlock"):
        exp = unlock_at(e["unlock"])
        if exp and not a.get("unlock_at"):
            ch.append(f"set unlock date {exp[:10]}")
        elif exp and not _same_instant(exp, a["unlock_at"]):
            ch.append(f"unlock {a['unlock_at'][:10]} → {exp[:10]}")
    if e.get("content"):
        want = viewer_url_in(e["description"])
        if a.get("viewer_url") is None:
            ch.append("replace the fixed content snapshot with the live lesson view")
        elif want and a["viewer_url"] != want:
            ch.append("live view link → " + want.split("?", 1)[-1])
        elif not a.get("stub_current"):
            ch.append("restyle the open-lesson button")
    if e.get("quiz"):
        qz = e["quiz"]
        if a.get("quiz") != qz["quiz_id"]:
            ch.append("add the quiz id marker")   # so future renumbering finds it by id, not title
        if a.get("new_quiz"):
            # the questions are on Canvas — compare the version stamped there with the Exams repo
            if qz.get("version") and a.get("quiz_version") != qz["version"]:
                ch.append(_quiz_refresh_change(qz, a))
        elif (options or {}).get("push_quizzes") and qz.get("unlocked"):
            ch.append("replace the placeholder with a New Quiz carrying the questions")
    return ch

def _plan_module_sync(block, ref, state, due_at, unlock_at, options=None):
    """Match a module block's expected items against the course. Returns
    {module_name, module_id, expected, create, update, unchanged, retire, reorder}
    where update/unchanged entries carry the matched Canvas item and retire lists
    module items the schedule no longer expects. Matching order per expected
    item: exact title in the module → same lesson identity in the module → same
    un-numbered title in the module → same lesson identity anywhere in the course
    (an assignment whose module link was removed).

    options["slots"] (a set of slot indexes) limits the sync to those class days:
    every expected item is still matched (so module order can be restored), but
    only the chosen days land in create/update — the rest are listed under
    `skipped`, with what a full sync would have done to them — and nothing is
    retired, so unselected days are left exactly as they are."""
    modules, assignments, module_items = state
    expected = _expected_block_items(block, ref)
    only = (options or {}).get("slots")
    mod_name = _unit_module_name(block)
    mod = next((m for m in modules if m["name"] == mod_name), None)
    plan = {"module_name": mod_name, "module_id": mod["id"] if mod else None, "expected": expected,
            "create": [], "update": [], "unchanged": [], "retire": [], "skipped": [],
            "reorder": False, "partial": only is not None}
    if not expected:
        return plan
    asgn_by_id = {a["id"]: a for a in assignments}
    cands = []
    for it in (module_items(mod["id"]) if mod else []):
        if it.get("type") == "Assignment":
            a = asgn_by_id.get(it.get("content_id"))
            if a is None:
                continue
            cands.append({"kind": "Assignment", "item": it, "asgn": a, "name": a["name"],
                          "identity": _asgn_identity(a), "base": _base_title(a["name"])})
        elif it.get("type") == "Page":
            cands.append({"kind": "Page", "item": it, "asgn": None, "name": it.get("title") or "",
                          "identity": None, "base": _base_title(it.get("title"))})
    linked = {c["asgn"]["id"] for c in cands if c["asgn"]}
    loose = [{"kind": "Assignment", "item": None, "asgn": a, "name": a["name"],
              "identity": _asgn_identity(a), "base": _base_title(a["name"])}
             for a in assignments if a["id"] not in linked and _asgn_identity(a)]
    claimed = set()

    def take(pool, pred):
        for c in pool:
            if id(c) not in claimed and pred(c):
                claimed.add(id(c))
                return c
        return None

    matched_positions = []
    for idx, e in enumerate(expected):
        chosen = only is None or e["slot"] in only
        same_kind = lambda c, e=e: c["kind"] == e["type"]
        c = (take(cands, lambda c: same_kind(c) and c["name"] == e["title"])
             or take(cands, lambda c: same_kind(c) and c["identity"] and c["identity"] == e["identity"])
             or take(cands, lambda c: same_kind(c) and c["base"] == e["base_title"])
             or (take(loose, lambda c: c["identity"] == e["identity"]) if e["type"] == "Assignment" else None))
        if c is None:
            if not chosen:
                plan["skipped"].append({"expected": e, "title": e["title"], "type": e["type"],
                                        "slot": e["slot"], "would": "create", "changes": []})
                continue
            plan["create"].append(e)
            plan["reorder"] = True   # a new item lands at the end; positions must be redone
            continue
        if c["kind"] == "Assignment":
            changes = _assignment_changes(e, c["asgn"], due_at, unlock_at, options)
        else:
            changes = [f"rename from “{c['name']}”"] if c["name"] != e["title"] else []
        if c["item"] is None:
            changes.append("link into the module again")
            if chosen:
                plan["reorder"] = True
        else:
            matched_positions.append(c["item"].get("position") or 0)
        e["_canvas"] = (("Assignment", c["asgn"]["id"]) if c["kind"] == "Assignment"
                        else ("Page", (c["item"] or {}).get("page_url")))
        entry = {"expected": e, "match": c, "title": e["title"], "type": e["type"],
                 "from": c["name"], "changes": changes, "slot": e["slot"]}
        if not chosen:
            entry["would"] = "update" if changes else "unchanged"
            plan["skipped"].append(entry)
            continue
        (plan["update"] if changes else plan["unchanged"]).append(entry)
    if matched_positions != sorted(matched_positions):
        plan["reorder"] = True
    if only is None:
        for c in cands:
            if id(c) not in claimed:
                plan["retire"].append({"match": c, "title": c["name"], "type": c["kind"],
                                       "published": (c["asgn"] or c["item"]).get("published")})
    return plan

def _plan_public(plan):
    """The plan without Canvas internals — what the dry-run preview shows."""
    def strip(entries):
        return [{"title": x["title"], "type": x["type"], "from": x.get("from"),
                 "changes": x.get("changes", []), "slot": x.get("slot")} for x in entries]
    return {"module_name": plan["module_name"], "module_exists": plan["module_id"] is not None,
            "create": [{"title": e["title"], "type": e["type"], "quiz": e.get("quiz"), "slot": e.get("slot")}
                       for e in plan["create"]],
            "update": strip(plan["update"]), "unchanged": strip(plan["unchanged"]),
            "retire": [{"title": r["title"], "type": r["type"], "published": r.get("published")}
                       for r in plan["retire"]],
            "skipped": [dict(pub, would=x.get("would"))
                        for x, pub in zip(plan.get("skipped", []), strip(plan.get("skipped", [])))],
            "partial": plan.get("partial", False), "reorder": plan["reorder"]}

def _plan_summary(plan, ref):
    """(status, detail) for the sync-status dot."""
    mod_name = plan["module_name"]
    if plan["module_id"] is None:
        return "unsynced", f"Ready to sync — no module named “{mod_name}” in the course yet"
    if not plan["create"] and not plan["update"] and not plan["retire"]:
        return "synced", (f"It seems to be synced — “{mod_name}” has all {len(plan['expected'])} "
                          f"item(s) with matching titles, points, and due dates, live from “{ref}”")
    bits = []
    if plan["create"]:
        bits.append("to create: " + ", ".join(f"“{e['title']}”" for e in plan["create"][:4])
                    + ("…" if len(plan["create"]) > 4 else ""))
    if plan["update"]:
        bits.append("to update: " + "; ".join(f"“{u['title']}” ({', '.join(u['changes'])})"
                                              for u in plan["update"][:3])
                    + ("…" if len(plan["update"]) > 3 else ""))
    if plan["retire"]:
        bits.append("no longer in the schedule (will be unpublished): "
                    + ", ".join(f"“{r['title']}”" for r in plan["retire"][:3])
                    + ("…" if len(plan["retire"]) > 3 else ""))
    return "partial", f"Partially synced — “{mod_name}” exists but " + " · ".join(bits) + ". Sync updates in place."

def _apply_module_sync(course_id, plan, ref, due_at, unlock_at, options=None):
    """Carry out a module plan against Canvas. Creates what is missing, updates
    matched items in place (name, points, dates, module link, and the live-view
    description when its link drifted), unpublishes retired items, and rewrites
    module positions when the order changed. Never deletes anything.
    options["push_quizzes"]: create quiz days as real New Quizzes (questions from
    the unlocked quiz.json) instead of placeholder assignments, and upgrade days
    already on Canvas as placeholders. A pushed quiz whose stamped version is
    behind the Exams repo gets its questions replaced in place."""
    options = options or {}
    out = {"module_name": plan["module_name"], "module_id": plan["module_id"], "ref": ref,
           "created": [], "updated": [], "retired": [],
           "unchanged": [u["title"] for u in plan["unchanged"]],
           "skipped": [x["title"] for x in plan.get("skipped", [])],
           "partial": plan.get("partial", False), "errors": []}
    module_id = plan["module_id"]
    if module_id is None:
        mod_res = requests.post(f"{BASE}/courses/{course_id}/modules", headers=hdrs(),
                                json={"module": {"name": plan["module_name"], "position": 1}})
        if not mod_res.ok:
            out["errors"].append({"name": plan["module_name"], "error": f"Module creation failed: {mod_res.text}"})
            return out
        module_id = out["module_id"] = mod_res.json()["id"]

    def put(url, payload):
        return requests.put(url, headers=hdrs(), json=payload)

    def link(title, type_, **content):
        mr = requests.post(f"{BASE}/courses/{course_id}/modules/{module_id}/items", headers=hdrs(),
                           json={"module_item": {"title": title, "type": type_, **content}})
        return mr.ok

    for e in plan["create"]:
        if e["type"] == "Page":
            page, perr = create_canvas_page(course_id, module_id, e["title"], e["description"])
            if perr:
                out["errors"].append({"name": e["title"], "error": perr})
            else:
                out["created"].append(page)
                e["_canvas"] = ("Page", page.get("page_url"))
            continue
        if e.get("quiz") and options.get("push_quizzes"):
            asgn_id, perr = _push_new_quiz(course_id, e, due_at, unlock_at)
            if asgn_id:
                e["_canvas"] = ("Assignment", asgn_id)
                out["created"].append({"name": e["title"], "assignment_id": asgn_id, "new_quiz": True,
                                       "linked": link(e["title"], "Assignment", content_id=asgn_id)})
                if perr:
                    out["errors"].append({"name": e["title"], "error": perr})
                continue
            out["errors"].append({"name": e["title"],
                                  "error": f"New Quizzes push failed — created a placeholder assignment instead: {perr}"})
        submission = ["none"] if e.get("quiz") else ["online_upload", "online_text_entry"]
        payload = {"assignment": {"name": e["title"], "points_possible": e["points"],
                                  "submission_types": submission,
                                  "description": e["description"], "published": False}}
        if e.get("due"):
            payload["assignment"]["due_at"] = due_at(e["due"])
        if e.get("unlock"):
            payload["assignment"]["unlock_at"] = unlock_at(e["unlock"])
        r = requests.post(f"{BASE}/courses/{course_id}/assignments", headers=hdrs(), json=payload)
        if not r.ok:
            out["errors"].append({"name": e["title"], "error": r.text})
            continue
        asgn_id = r.json()["id"]
        e["_canvas"] = ("Assignment", asgn_id)
        out["created"].append({"name": e["title"], "assignment_id": asgn_id,
                               "linked": link(e["title"], "Assignment", content_id=asgn_id)})

    for u in plan["update"]:
        e, c = u["expected"], u["match"]
        if e["type"] == "Assignment":
            a = c["asgn"]
            if any(ch.startswith("replace the placeholder") for ch in u["changes"]):
                # "push quiz questions" ticked for a day that so far has only a placeholder:
                # create the real New Quiz in its place and drop the placeholder — submission
                # type "none", so nothing a student could have handed in is lost
                asgn_id, perr = _push_new_quiz(course_id, e, due_at, unlock_at)
                if asgn_id:
                    e["_canvas"] = ("Assignment", asgn_id)
                    linked = link(e["title"], "Assignment", content_id=asgn_id)
                    dr = requests.delete(f"{BASE}/courses/{course_id}/assignments/{a['id']}", headers=hdrs())
                    if not dr.ok:
                        out["errors"].append({"name": e["title"],
                                              "error": f"placeholder could not be removed: {dr.text[:200]}"})
                    if perr:
                        out["errors"].append({"name": e["title"], "error": perr})
                    out["updated"].append({"name": e["title"], "from": c["name"], "changes": u["changes"],
                                           "new_quiz": True, "linked": linked})
                    plan["reorder"] = True
                    continue
                out["errors"].append({"name": e["title"],
                                      "error": f"New Quizzes push failed — placeholder kept: {perr}"})
            refreshed = None
            if any(ch.startswith("quiz questions") for ch in u["changes"]):
                items, version, qerr = _quiz_payload(e)
                qerr = qerr or _refresh_new_quiz_items(course_id, a["id"], items)
                if qerr:
                    out["errors"].append({"name": e["title"], "error": f"quiz questions not refreshed: {qerr}"})
                else:
                    refreshed = version
            payload = {"assignment": {"name": e["title"]}}
            if e.get("points") is not None:
                payload["assignment"]["points_possible"] = e["points"]
            if e.get("due"):
                payload["assignment"]["due_at"] = due_at(e["due"])
            if e.get("unlock"):
                payload["assignment"]["unlock_at"] = unlock_at(e["unlock"])
            if refreshed or any(ch.startswith(("replace the fixed", "live view link", "add the quiz id", "restyle the open-lesson"))
                                for ch in u["changes"]):
                desc = e["description"]
                if e.get("quiz") and a.get("new_quiz"):
                    # never strip the version stamp off a quiz that carries questions
                    desc = _with_quiz_version(desc, refreshed or a.get("quiz_version"))
                payload["assignment"]["description"] = desc
            r = put(f"{BASE}/courses/{course_id}/assignments/{a['id']}", payload)
            if not r.ok:
                out["errors"].append({"name": e["title"], "error": r.text})
                continue
            if c["item"] is None:
                link(e["title"], "Assignment", content_id=a["id"])
            elif c["item"].get("title") != e["title"]:
                put(f"{BASE}/courses/{course_id}/modules/{module_id}/items/{c['item']['id']}",
                    {"module_item": {"title": e["title"]}})
        else:
            page_url = c["item"].get("page_url")
            r = put(f"{BASE}/courses/{course_id}/pages/{page_url}", {"wiki_page": {"title": e["title"]}})
            if not r.ok:
                out["errors"].append({"name": e["title"], "error": r.text})
                continue
            put(f"{BASE}/courses/{course_id}/modules/{module_id}/items/{c['item']['id']}",
                {"module_item": {"title": e["title"]}})
        out["updated"].append({"name": e["title"], "from": c["name"], "changes": u["changes"]})

    for rt in plan["retire"]:
        c = rt["match"]
        if c["kind"] == "Assignment":
            r = put(f"{BASE}/courses/{course_id}/assignments/{c['asgn']['id']}",
                    {"assignment": {"published": False}})
        else:
            r = put(f"{BASE}/courses/{course_id}/pages/{c['item'].get('page_url')}",
                    {"wiki_page": {"published": False}})
        if r.ok:
            out["retired"].append({"name": c["name"], "type": c["kind"]})
        else:
            # Canvas refuses to unpublish an assignment that already has submissions
            out["errors"].append({"name": c["name"], "error": f"could not unpublish: {r.text}"})

    if plan["reorder"]:
        # Restore module order even when an item above reported an error (a quiz
        # push with a failed question, say) — a new day must still land in its
        # place, not at the end. Items are found by the Canvas object they wrap
        # (assignment id / page url), titles only as a fallback; every one of ours
        # is re-positioned 1..n in expected order, so stale positions can't mislead.
        try:
            live = canvas_paged(f"/courses/{course_id}/modules/{module_id}/items")
        except Exception as ex:  # ordering is cosmetic — never fail the sync over it
            live = []
            out["errors"].append({"name": "(reorder)", "error": str(ex)})
        by_key, by_title = {}, {}
        for it in live:
            if it.get("type") == "Assignment" and it.get("content_id") is not None:
                by_key[("Assignment", it["content_id"])] = it
            elif it.get("type") == "Page" and it.get("page_url"):
                by_key[("Page", it["page_url"])] = it
            by_title.setdefault((it.get("title"), it.get("type")), it)
        ordered = []
        for e in plan["expected"]:
            it = by_key.get(e.get("_canvas")) or by_title.get((e["title"], e["type"]))
            if it and it not in ordered:
                ordered.append(it)
        current = sorted(ordered, key=lambda it: it.get("position") or 0)
        if [it["id"] for it in current] != [it["id"] for it in ordered]:
            for pos, it in enumerate(ordered, start=1):
                r = put(f"{BASE}/courses/{course_id}/modules/{module_id}/items/{it['id']}",
                        {"module_item": {"position": pos}})
                if not r.ok:
                    out["errors"].append({"name": f"(reorder) {it.get('title')}", "error": r.text[:200]})
            out["reordered"] = len(ordered)
    _invalidate_course_caches(course_id)
    return out

def _standalone_expected(block, ref):
    """The one assignment a standalone test / final / lesson block syncs to."""
    kind = block["type"]
    first = block["slots"][0] if block.get("slots") else {}
    title = first.get("base_title") or block.get("title") or kind.title()
    if kind in ("test", "final"):
        label = "final exam" if kind == "final" else "test"
        return {"title": title, "type": "Assignment", "identity": f"{kind}:{title}", "base_title": title,
                "points": block.get("points") or 100, "due": block.get("end"), "unlock": block.get("start"),
                "description": f"<p>In-class {label}. Details will be provided in class.</p>", "content": False}
    if kind == "lesson":
        lref = first.get("lesson_ref") or {}
        return {"title": title, "type": "Assignment",
                "identity": f"lesson:{lref.get('module')}/{lref.get('path')}", "base_title": title,
                "points": block.get("points") or 10, "due": block.get("end"), "unlock": block.get("start"),
                "description": live_description(ref, lref.get("module"), lref.get("path"), None),
                "content": True}
    return None

def _match_standalone(e, assignments):
    a = next((a for a in assignments if a["name"] == e["title"]), None)
    if a is None and e["identity"].startswith("lesson:"):
        a = next((a for a in assignments if a.get("lesson") and f"lesson:{a['lesson']}" == e["identity"]), None)
    return a

@app.route("/api/schedules/<name>/sync-status")
def api_schedule_sync_status(name):
    """Compare every syncable block against what actually exists in a Canvas
    course, using the same planner as sync-block: 'synced' (module + all items
    found, titles, points, and due dates match), 'partial' (found but some items
    would be created, updated, or unpublished by a sync — the detail says which),
    or 'unsynced' (nothing there yet). Reads through the Canvas caches."""
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
    _due_at, _unlock_at = _sched_time_fns(sched)
    ref = schedule_ref(sched)
    try:
        state = _canvas_course_state(course_id, ttl)
    except Exception as e:
        return jsonify({"error": f"Canvas fetch failed: {e}"}), 502
    _, assignments, _ = state

    statuses = {}
    for block in resolved["blocks"]:
        bid = block.get("id")
        if not bid or block.get("missing"):
            continue
        if block["type"] == "module":
            try:
                plan = _plan_module_sync(block, ref, state, _due_at, _unlock_at)
            except Exception as e:
                statuses[bid] = {"status": "partial", "detail": f"Could not check: {e}"}
                continue
            if not plan["expected"]:
                continue
            status, detail = _plan_summary(plan, ref)
            items = ([{"slot": e["slot"], "title": e["title"], "status": "missing"} for e in plan["create"]]
                     + [{"slot": u["slot"], "title": u["title"], "status": "drifted",
                         "detail": "; ".join(u["changes"])} for u in plan["update"]]
                     + [{"slot": u["slot"], "title": u["title"], "status": "synced"} for u in plan["unchanged"]])
            statuses[bid] = {"status": status, "detail": detail,
                             "items": sorted(items, key=lambda x: x["slot"])}
        elif block["type"] in ("test", "final", "lesson"):
            e = _standalone_expected(block, ref)
            a = _match_standalone(e, assignments)
            if a is None:
                statuses[bid] = {"status": "unsynced",
                                 "detail": f"Ready to sync — no assignment named “{e['title']}” in the course yet"}
                continue
            changes = _assignment_changes(e, a, _due_at, _unlock_at)
            statuses[bid] = ({"status": "synced",
                              "detail": f"It seems to be synced — “{e['title']}” found with matching points and due date"}
                             if not changes else
                             {"status": "partial", "detail": "Partially synced — " + "; ".join(changes)
                                                             + ". Sync updates in place."})
    return jsonify({"course_id": course_id, "statuses": statuses})

@app.route("/api/schedules/<name>/sync-items")
def api_schedule_sync_items(name):
    """The Canvas items a module block would sync, one per class day, so the
    Sync dialog can offer per-day checkboxes before (and without) a course is
    picked. Repo-only — no Canvas call, no token needed."""
    if not NAME_RE.match(name):
        return jsonify({"error": "invalid schedule name"}), 400
    sched = load_schedule(name)
    if sched is None:
        return jsonify({"error": "schedule not found"}), 404
    block_id = request.args.get("block_id")
    block = next((b for b in resolve_schedule(sched)["blocks"] if b.get("id") == block_id), None)
    if block is None:
        return jsonify({"error": "block not found in schedule"}), 404
    if block["type"] != "module" or block.get("missing"):
        return jsonify({"items": []})
    keys = ("slot", "title", "type", "points", "due")
    return jsonify({"items": [{k: e[k] for k in keys}
                              for e in _expected_block_items(block, schedule_ref(sched))]})

@app.route("/api/schedules/<name>/sync-block", methods=["POST"])
def api_schedule_sync_block(name):
    """Upsert one schedule block into a Canvas course. Body: {course_id, block_id,
    dry_run?, push_quizzes?, slots?}. With dry_run the plan is returned and
    nothing is written — the Sync dialog shows it as a preview. Otherwise:
    missing items are created, matched items are updated in place, items the
    schedule no longer expects are unpublished (never deleted), and module order
    is restored. `slots` (slot indexes from /sync-items) limits a module block
    to those class days: only they are created/updated, nothing is unpublished,
    and every other day is left exactly as it is."""
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
    dry_run = bool(body.get("dry_run"))
    options = {"push_quizzes": bool(body.get("push_quizzes"))}
    if not course_id or not block_id:
        return jsonify({"error": "course_id and block_id required"}), 400
    if body.get("slots") is not None:
        try:
            options["slots"] = {int(x) for x in body["slots"]}
        except (TypeError, ValueError):
            return jsonify({"error": "slots must be a list of slot indexes"}), 400
    resolved = resolve_schedule(sched)
    block = next((b for b in resolved["blocks"] if b.get("id") == block_id), None)
    if block is None:
        return jsonify({"error": "block not found in schedule"}), 404
    if block.get("missing"):
        return jsonify({"error": "block source is missing from the repo"}), 422

    _due_at, _unlock_at = _sched_time_fns(sched)
    ref = schedule_ref(sched)
    try:
        # a real sync always looks at the live course; a preview may use the caches
        state = _canvas_course_state(course_id, SUBRESOURCE_TTL if dry_run else 0)
    except Exception as e:
        return jsonify({"error": f"Canvas fetch failed: {e}"}), 502
    _, assignments, _ = state

    if block["type"] == "module":
        plan = _plan_module_sync(block, ref, state, _due_at, _unlock_at, options)
        if not plan["expected"]:
            return jsonify({"error": "nothing in this block syncs to Canvas"}), 422
        if plan["partial"] and not (plan["create"] or plan["update"] or plan["unchanged"]):
            return jsonify({"error": "none of the selected days creates a Canvas item"}), 422
        if dry_run:
            return jsonify({"dry_run": True, "ref": ref, "unit_number": block["unit_number"],
                            "plan": _plan_public(plan)})
        out = _apply_module_sync(course_id, plan, ref, _due_at, _unlock_at, options)
        out["unit_number"] = block["unit_number"]
        return jsonify(out)

    e = _standalone_expected(block, ref)
    if e is None:
        return jsonify({"error": f"'{block['type']}' days are schedule-only — nothing to sync"}), 422
    a = _match_standalone(e, assignments)
    changes = _assignment_changes(e, a, _due_at, _unlock_at) if a else []
    if dry_run:
        return jsonify({"dry_run": True, "ref": ref, "plan": {
            "module_name": None, "module_exists": True,
            "create": [] if a else [{"title": e["title"], "type": "Assignment"}],
            "update": [{"title": e["title"], "type": "Assignment", "from": a["name"], "changes": changes}] if a and changes else [],
            "unchanged": [{"title": e["title"], "type": "Assignment", "from": a["name"], "changes": []}] if a and not changes else [],
            "retire": [], "reorder": False}})
    out = {"ref": ref, "created": [], "updated": [], "retired": [], "unchanged": [], "errors": []}
    if a is None:
        payload = {"assignment": {"name": e["title"], "points_possible": e["points"],
                                  "submission_types": ["online_upload", "online_text_entry"],
                                  "description": e["description"], "published": False}}
        if e.get("due"):
            payload["assignment"]["due_at"] = _due_at(e["due"])
        if e.get("unlock"):
            payload["assignment"]["unlock_at"] = _unlock_at(e["unlock"])
        r = requests.post(f"{BASE}/courses/{course_id}/assignments", headers=hdrs(), json=payload)
        if r.ok:
            out["created"].append({"name": e["title"], "assignment_id": r.json()["id"], "linked": False})
        else:
            out["errors"].append({"name": e["title"], "error": r.text})
    elif changes:
        payload = {"assignment": {"name": e["title"], "points_possible": e["points"]}}
        if e.get("due"):
            payload["assignment"]["due_at"] = _due_at(e["due"])
        if e.get("unlock"):
            payload["assignment"]["unlock_at"] = _unlock_at(e["unlock"])
        if any(ch.startswith(("replace the fixed", "live view link", "restyle the open-lesson")) for ch in changes):
            payload["assignment"]["description"] = e["description"]
        r = requests.put(f"{BASE}/courses/{course_id}/assignments/{a['id']}", headers=hdrs(), json=payload)
        if r.ok:
            out["updated"].append({"name": e["title"], "from": a["name"], "changes": changes})
        else:
            out["errors"].append({"name": e["title"], "error": r.text})
    else:
        out["unchanged"].append(e["title"])
    _invalidate_course_caches(course_id)
    return jsonify(out)

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
            revs = _review_refs(a)   # one reference or a stacked list — never index it directly
            if review_file:
                hit = hit or any(r.get("module") == topic and r.get("path") == path
                                 and r.get("file") == review_file for r in revs)
            elif path:
                hit = hit or (a.get("_module") == topic and a.get("path") == path) \
                          or any(r.get("module") == topic and r.get("path") == path for r in revs)
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

ACTIVITY_HEADER = '### <font color="#79c0ff">Activity</font>'
# an embed's opening, old format ("👉 <details>") or current (header line + "<details>")
_ACTIVITY_OPEN_RE = re.compile(
    r'(?:^### <font color="#79c0ff">Activity</font>\n|👉 )?<details>', re.MULTILINE)

def _activity_toggle(file, title, body):
    # "Activity" is its own large header; the dropdown right under it is named
    # for the activity — the arrow already says it expands
    return (f"{ACTIVITY_HEADER}\n"
            "<details>\n"
            f"<summary><strong>{title}</strong></summary>\n\n"
            f"{body}\n\n"
            f"*(Standalone file: [activities/{file}](activities/{file}))*\n\n"
            "</details>")

def _find_activity_toggle(text, file):
    """(start, end) of the header + <details> block that embeds activities/<file>, or None."""
    marker = f"(activities/{file})"
    for m in _ACTIVITY_OPEN_RE.finditer(text):
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

def local_branch():
    """Branch checked out in this working tree (what the hub's previews show)."""
    try:
        head = (ROOT / ".git" / "HEAD").read_text().strip()
        return head.split("refs/heads/", 1)[1] if "refs/heads/" in head else head[:12]
    except OSError:
        return GITHUB_BRANCH

def hub_config():
    return {"course_name": COURSE_NAME, "repo_label": REPO_LABEL, "github_repo": GITHUB_REPO,
            "github_branch": GITHUB_BRANCH, "pages_url": PAGES_URL, "local_branch": local_branch()}

@app.route("/api/config")
def api_config():
    return jsonify(hub_config())

@app.route("/")
def index():
    page = (HERE / "index.html").read_text(encoding="utf-8")
    page = page.replace("__COURSE_NAME__", COURSE_NAME).replace("__REPO_LABEL__", REPO_LABEL)
    page = page.replace("__HUB_CONFIG__", json.dumps(hub_config()))
    return app.response_class(page, mimetype="text/html")

# The live lesson viewer, served from the repo root so the hub can preview the
# working tree exactly as students will see it once pushed: view.html fetches
# its files from /raw/ (same origin) instead of raw.githubusercontent.com.
RAW_EXT = {".md", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

def _no_store(resp):
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/view.html")
def viewer_page():
    return _no_store(send_file(ROOT / "view.html", mimetype="text/html"))

@app.route("/raw/<path:relpath>")
def raw_file(relpath):
    target = (ROOT / relpath).resolve()
    if not target.is_relative_to(ROOT) or not target.is_file():
        abort(404)
    rel_parts = target.relative_to(ROOT).parts
    if any(part.startswith(".") for part in rel_parts) or target.suffix.lower() not in RAW_EXT:
        abort(404)                              # never dotfiles (.env) or non-content files
    mime = "text/markdown" if target.suffix.lower() == ".md" else None
    return _no_store(send_file(target, mimetype=mime))

if __name__ == "__main__":
    print(f"HW Course Hub ({COURSE_NAME}) → http://127.0.0.1:5050")
    print(f"Repo root: {ROOT}")
    print(f"Finals dir: {FINALS} ({'found' if finals_available() else 'NOT FOUND — finals disabled'})")
    print(f"Exams dir: {EXAMS_DIR / EXAMS_CLASS} ({len(list_quizzes())} quiz(zes)" if exams_available()
          else f"Exams dir: {EXAMS_DIR / EXAMS_CLASS} (NOT FOUND — quizzes disabled)")
    print(f"Canvas token: {'configured' if TOKEN else 'MISSING — Canvas features disabled'}")
    app.run(port=5050, debug=True)
