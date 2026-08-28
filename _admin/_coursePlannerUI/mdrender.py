"""Markdown → HTML rendering that matches the course hub (../Admin/app.py).

The hub renders ASSIGNMENT.md and review fragments to HTML for Canvas with
python-markdown (extensions: tables, fenced_code) after rewriting relative
image/link paths to absolute GitHub URLs. This module ports that exactly.

If the `markdown` package is installed (pip3 install markdown) rendering is
byte-identical to the hub's. Otherwise a small built-in fallback renderer
covers the constructs this repo's conventions allow (headings, tables, fenced
code, blockquotes, lists, bold/italic/inline code, images, links, hr, and
pass-through HTML). The active engine is reported so the UI can say which
fidelity you are getting.
"""

import html
import json
import re
from pathlib import Path

try:
    import markdown as md_lib
    ENGINE = "markdown"
except ImportError:
    md_lib = None
    ENGINE = "builtin"

# Course-specific values live in _admin/_configuration/course.json so the same
# engine files run unmodified in every course repo (see _admin/sync-engine.sh).
# Both the hub and the planner import these from here.
_ROOT = Path(__file__).resolve().parents[2]
try:
    _course = json.loads((_ROOT / "_admin" / "_configuration" / "course.json").read_text())
except (OSError, ValueError):
    _course = {}
COURSE_NAME   = _course.get("course_name", _ROOT.name)
REPO_LABEL    = _course.get("repo_label", _ROOT.name)
GITHUB_REPO   = _course.get("github_repo", f"Harvard-Westlake/{_ROOT.name}")
GITHUB_BRANCH = _course.get("github_branch", "main")
GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"
GITHUB_BLOB = f"https://github.com/{GITHUB_REPO}/blob/{GITHUB_BRANCH}"


def _resolve_path(base_path, rel):
    parts = base_path.rstrip("/").split("/") if base_path else []
    for seg in rel.split("/"):
        if seg == "..":
            parts = parts[:-1] if parts else []
        elif seg and seg != ".":
            parts.append(seg)
    return "/".join(parts)


def _rewrite_github_urls(text, base_path):
    def rewrite_img(m):
        alt, path = m.group(1), m.group(2)
        if path.startswith(("http://", "https://")):
            return m.group(0)
        return f"![{alt}]({GITHUB_RAW}/{_resolve_path(base_path, path)})"

    def rewrite_link(m):
        label, path = m.group(1), m.group(2)
        if path.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        return f"[{label}]({GITHUB_BLOB}/{_resolve_path(base_path, path)})"

    def rewrite_html_src(m):
        attr, path = m.group(1), m.group(2)
        if path.startswith(("http://", "https://", "data:")):
            return m.group(0)
        return f'{attr}="{GITHUB_RAW}/{_resolve_path(base_path, path)}"'

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", rewrite_img, text)
    text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", rewrite_link, text)
    # raw HTML <img src=""> / <source srcset=""> (e.g. light/dark logo <picture> blocks)
    text = re.sub(r'(src|srcset)="([^"]+)"', rewrite_html_src, text)
    return text


# ── LaTeX math handling ────────────────────────────────────────────────────────
# GitHub renders $$...$$ (display) and $...$ (inline) natively. Canvas renders
# LaTeX via MathJax, but only inside \(...\) (inline) and $$...$$ (display) —
# single-dollar inline math is never rendered. Math segments are therefore
# stashed before markdown conversion (which would otherwise mangle _ and * in
# formulas), inline delimiters are converted to \(...\), and the raw LaTeX is
# restored HTML-escaped afterward. Escaped dollars (\$) become literal $, as on
# GitHub. Must stay in lockstep with ../Admin/app.py.

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


# GFM task-list checkboxes: neither python-markdown's "tables"/"fenced_code"
# extensions nor the builtin fallback below render `- [ ]` as a real checkbox,
# so it shows up as literal "[ ]" text in this preview and on Canvas itself.
# Rewrite the marker to an inline, disabled checkbox before rendering — GitHub
# still renders the untouched .md source with its own native task-list support.
# Must stay in lockstep with ../_hub/server.py.
_TASKLIST_RE = re.compile(r"^(\s*[-*])\s\[([ xX])\]\s+", re.MULTILINE)


def _rewrite_tasklist(m):
    checked = " checked" if m.group(2).lower() == "x" else ""
    return f'{m.group(1)} <input type="checkbox" disabled{checked}> '


# Centered title blocks (`<div align="center">` — see CLAUDE.md "Title format").
# GitHub's CommonMark renderer ends a raw HTML block at the first blank line
# after the opening tag, so the "# Title" / subtitle / label lines inside are
# parsed as normal markdown. python-markdown has no such rule: it swallows the
# whole <div>...</div> as one opaque raw block and never parses the markdown
# inside it, so titles render literally as "# Title" instead of a heading. The
# builtin fallback below doesn't have this problem (it processes each line on
# its own regardless of surrounding raw tags), so this only applies when
# python-markdown is the active engine. Must stay in lockstep with ../_hub/server.py.
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
# Must stay in lockstep with ../_hub/server.py.
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
    """Render markdown the way the hub does. Returns (html, engine)."""
    text, fences = _stash_indented_fences(text)
    text, math = _extract_math(text)
    text = _TASKLIST_RE.sub(_rewrite_tasklist, text)
    text = _rewrite_github_urls(text, base_path)
    if md_lib:
        text = _rewrite_title_divs(text)
        # "toc" only for its side effect of stamping id="..." on headings so
        # #anchor links resolve — see the matching comment in ../_hub/server.py.
        rendered = md_lib.markdown(text, extensions=["tables", "fenced_code", "toc"])
    else:
        rendered = _builtin_render(text)
    return _restore_math(_restore_fences(rendered, fences), math), ENGINE


def review_block(review_html):
    """The purple review wrapper the hub prepends to Canvas assignment bodies."""
    return (
        '<div style="background:#f6f8fa;border-left:4px solid #8957e5;'
        'padding:12px 16px;margin-bottom:20px;border-radius:0 6px 6px 0">'
        '<p style="font-weight:600;color:#8957e5;margin:0 0 8px 0">&#9997;&nbsp;Review</p>'
        + review_html + "</div>"
    )


# ── Built-in fallback renderer (used only when python-markdown is missing) ────

_INLINE_RULES = [
    (re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"), r'<img alt="\1" src="\2" style="max-width:100%">'),
    (re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)"), r"<em>\1</em>"),
]


def _inline(s):
    # protect inline code spans from other inline rules
    spans = []

    def stash(m):
        spans.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(spans) - 1}\x00"

    s = re.sub(r"`([^`\n]+)`", stash, s)
    for rx, repl in _INLINE_RULES:
        s = rx.sub(repl, s)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], s)


def _heading_slug(text, seen):
    """id="..." for a heading, approximating python-markdown's "toc" slugs
    closely enough for hand-written #anchor links to resolve in this fallback
    renderer too (see the "toc" extension note in ../_hub/server.py)."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[`*_]', '', text)
    slug = re.sub(r'[-\s]+', '-', re.sub(r'[^\w\s-]', '', text).strip().lower())
    if slug in seen:
        seen[slug] += 1
        return f"{slug}-{seen[slug]}"
    seen[slug] = 0
    return slug


def _builtin_render(text):
    out, i = [], 0
    lines = text.splitlines()
    in_list = None  # 'ul' | 'ol' | None
    seen_ids = {}

    def close_list():
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            close_list()
            code, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
            close_list()
            headers = [c.strip() for c in stripped.strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{_inline(h)}</th>" for h in headers) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        m = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if m:
            close_list()
            level = len(m.group(1))
            slug = _heading_slug(m.group(2), seen_ids)
            out.append(f'<h{level} id="{slug}">{_inline(m.group(2))}</h{level}>')
        elif re.match(r"^(-{3,}|\*{3,})$", stripped):
            close_list()
            out.append("<hr>")
        elif stripped.startswith(">"):
            close_list()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>" + _inline(" ".join(q for q in quote if q)) + "</p></blockquote>")
            continue
        elif re.match(r"^[-*]\s+", stripped):
            if in_list != "ul":
                close_list()
                out.append("<ul>")
                in_list = "ul"
            out.append("<li>" + _inline(re.sub(r"^[-*]\s+", "", stripped)) + "</li>")
        elif re.match(r"^\d+\.\s+", stripped):
            if in_list != "ol":
                close_list()
                out.append("<ol>")
                in_list = "ol"
            out.append("<li>" + _inline(re.sub(r"^\d+\.\s+", "", stripped)) + "</li>")
        elif stripped.startswith("<"):
            close_list()
            out.append(line)  # raw HTML passes through, as python-markdown does
        elif stripped:
            close_list()
            out.append(f"<p>{_inline(stripped)}</p>")
        else:
            close_list()
        i += 1

    close_list()
    return "\n".join(out)
