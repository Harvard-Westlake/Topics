# _admin — Course Administration Namespace

Everything in this folder is tooling, configuration, and documentation for running the course — none of it is student-facing curriculum. Underscore-prefixed folders are ignored by the module importer and excluded from all student-facing indexes (see the `_` prefix convention in the root `CLAUDE.md`).

| Folder | Purpose |
|---|---|
| [`_hub/`](_hub/) | **The course hub** — one tabbed web app for Canvas courses, per-teacher year schedules, and module planning — `python3 _admin/_hub/server.py` |
| [`_schedules/`](_schedules/) | Per-teacher year-plan JSONs edited by the hub's Year Schedule tab |
| [`_instructions/`](_instructions/) | Authoring guides and content-review notes for maintaining lessons |
| [`_coursePlannerUI/`](_coursePlannerUI/) | Standalone credential-free planner (superseded by the hub's Module Planner tab, kept as a stdlib-only fallback) — `python3 _admin/_coursePlannerUI/server.py` |
| [`_configuration/`](_configuration/) | Schemas and configuration — [`module.schema.json`](_configuration/module.schema.json) defines the curated module format |
| [`_lessonplans/`](_lessonplans/) | **Generated** readable summaries of each curated module — do not edit by hand |
| [`_verification/`](_verification/) | [`verify.py`](_verification/verify.py) — link and reference checker, run locally or via CI |

Curated module JSONs themselves live at the repo top level in [`_modules/`](../_modules/) so they are easy to find and update.

## The planning pipeline

```
lessons (topic folders)          the source content, one folder per topic
        │
        ▼
_hub Module Planner tab          pick lessons + reviews, set unit/points
        │
        ▼
_modules/<slug>.json             curated module (this repo = source of truth)
        │                        └─ _admin/_lessonplans/<slug>.md (generated summary)
        ▼
_hub Year Schedule tab           drag modules/tests/finals onto real class dates
        │                        (_admin/_schedules/<teacher>.json, one per teacher)
        ▼
Canvas module + assignments      synced with each teacher's own token (.env,
                                 gitignored — never stored in this repo)
```

Final exam **content** lives only in the private sibling Admin repo; syncing a
test/final day pushes a placeholder assignment (title, date, points) to Canvas.

`_verification/verify.py` runs on every push (`.github/workflows/verify.yml`) and confirms all of the arrows above still point at things that exist.

## The engine and other course repos

The tooling above (plus `CLAUDE.md`, `embed/`, `.github/`, `.gitignore`, `.env.example`, `_modules/README.md`) is the **course engine**, and this repo is its canonical home. Sibling course repos (e.g. `../DND`) run the identical engine over completely independent content.

- **All engine feature work happens here** — never in a sibling repo — then flows outward with [`sync-engine.sh`](sync-engine.sh):

  ```
  _admin/sync-engine.sh ../DND     # then review with git diff in ../DND
  ```

- **Engine files contain zero course-specific data.** Anything course-specific lives in `_admin/_configuration/course.json` (course name, GitHub repo — read by the hub and planner at startup), `.env`, `_modules/*.json`, `_admin/_schedules/`, or content folders. The sync never touches those, so each course repo keeps its own.
- Each sibling repo records which commit of this repo its engine came from in `_admin/_configuration/engine-version.json` — stamped on every sync. To sync a specific engine version, check out that commit here first.
