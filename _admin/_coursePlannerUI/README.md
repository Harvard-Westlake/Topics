# Course Planner UI

Local web UI for creating and editing curated curriculum modules — the same Create Module experience as the course hub (`../Admin`), but it saves to `_modules/<slug>.json` in this repo instead of pushing to Canvas. No credentials are used; the Canvas access key stays in the Admin repo.

## Run

```bash
python3 _admin/_coursePlannerUI/server.py
```

Then open <http://127.0.0.1:8901>. Python 3 standard library only — no dependencies to install.

## What it does

- Lists topics and lessons by reading the repo directly (same `LESSONS.md` parsing as the hub)
- Lets you select lessons across topics, attach review fragments, and set unit number / points / scale factor
- **Save** validates every referenced lesson and review file exists, writes `_modules/<slug>.json`, and regenerates the readable summary at `_admin/_lessonplans/<slug>.md`
- Loading a saved module re-reads lessons fresh from the repo (the repo is the source of truth), re-applies your selection, and flags any saved lessons that no longer exist

## Viewing and editing lessons

Click any lesson title in the table to open the lesson editor:

- **Tabs** for every `.md` in the lesson folder (`README.md`, `ASSIGNMENT.md`, platform variants, `review/*.md`) and every standalone demo page (`demos/*.html`), plus a `+ ASSIGNMENT.md` tab to create one where missing
- **Edit** mode is a plain markdown editor; saving writes straight to the repo file and reports any broken relative links you just introduced
- **Canvas Preview** renders the file exactly as the hub uploads it — same markdown pipeline, relative images/links rewritten to GitHub URLs, and for `ASSIGNMENT.md` the attached review fragment is prepended in the hub's purple review block, on a white Canvas-style page
- **Live Preview** (demo tabs) renders the standalone HTML page itself in an embedded frame — demo tabs open straight into it, and it previews the current buffer, so edits show without saving. Saving writes the file back like any other tab

Preview fidelity: if the `markdown` package is installed (`pip3 install markdown`), rendering is identical to the hub's; otherwise a built-in fallback covers this repo's conventions and the UI notes that the preview is approximate.

## Files

| File | Purpose |
|---|---|
| `server.py` | stdlib HTTP server: serves the UI and the read/write API |
| `index.html` | single-page UI (same design as the hub's drawer) |
| `mdrender.py` | markdown → HTML matching the hub's `md_to_html` (GitHub URL rewriting + tables/fenced-code) |

After editing modules or lessons, run the verifier to confirm everything still links:

```bash
python3 _admin/_verification/verify.py
```
