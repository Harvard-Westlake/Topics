# _modules — Curated Curriculum Modules

One JSON file per curated module. Each file is a saved, reusable unit plan: an ordered selection of lessons from this repo (possibly spanning several topic folders), with optional review fragments attached to individual assignments.

These files are the source of truth for course planning. The course hub (the `../Admin` Flask app, which holds the Canvas access key) imports them to create Canvas modules; this repo never contains credentials.

## Workflow

1. **Create / edit** — run the planner UI: `python3 _admin/_coursePlannerUI/server.py`, then open `http://127.0.0.1:8901`. Saving writes `_modules/<slug>.json` and regenerates the readable summary in `_admin/_lessonplans/<slug>.md`.
2. **Verify** — `python3 _admin/_verification/verify.py` confirms every module still points at lessons and review files that exist (also runs in CI on every push).
3. **Import** — in the hub's Create Module drawer, pick the module from the "Load saved module" dropdown. The hub resolves review references to markdown, applies point scaling, and pushes to Canvas.

## File format

Defined by [`_admin/_configuration/module.schema.json`](../_admin/_configuration/module.schema.json). Summary:

| Field | Meaning |
|---|---|
| `name` / `slug` | Display name and kebab-case id (slug must match the filename) |
| `description` | One-paragraph summary |
| `unit_number` | Suggested unit number (hub may override at import) |
| `points_per_assignment` | Base points, before scaling |
| `scale_factor` | Per-unit multiplier (`points × factor^unit`, smart-rounded) |
| `topic_names` | Topic folders the lessons come from |
| `assignments[]` | `{day, duration, title, path, _module, review}` per lesson |
| `assignments[].review` | `{module, path, file}` reference into a lesson's `review/` folder, or `null` |

Review fragments are stored as **references, not inline content** — the repo's markdown stays the single source of truth, and the hub reads the current content at import time.

Do not edit `_admin/_lessonplans/*.md` by hand; they are generated from these files.
