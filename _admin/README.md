# _admin — Course Administration Namespace

Everything in this folder is tooling, configuration, and documentation for running the course — none of it is student-facing curriculum. Underscore-prefixed folders are ignored by the module importer and excluded from all student-facing indexes (see the `_` prefix convention in the root `CLAUDE.md`).

| Folder | Purpose |
|---|---|
| [`_instructions/`](_instructions/) | Authoring guides and content-review notes for maintaining lessons |
| [`_coursePlannerUI/`](_coursePlannerUI/) | Local web UI for creating and editing curated modules — `python3 _admin/_coursePlannerUI/server.py` |
| [`_configuration/`](_configuration/) | Schemas and configuration — [`module.schema.json`](_configuration/module.schema.json) defines the curated module format |
| [`_lessonplans/`](_lessonplans/) | **Generated** readable summaries of each curated module — do not edit by hand |
| [`_verification/`](_verification/) | [`verify.py`](_verification/verify.py) — link and reference checker, run locally or via CI |

Curated module JSONs themselves live at the repo top level in [`_modules/`](../_modules/) so they are easy to find and update.

## The planning pipeline

```
lessons (topic folders)          the source content, one folder per topic
        │
        ▼
_coursePlannerUI                 pick lessons + reviews, set unit/points
        │
        ▼
_modules/<slug>.json             curated module (this repo = source of truth)
        │                        └─ _admin/_lessonplans/<slug>.md (generated summary)
        ▼
../Admin course hub              "Load saved module" in the Create Module drawer;
        │                        holds the Canvas access key (never stored here)
        ▼
Canvas module + assignments
```

`_verification/verify.py` runs on every push (`.github/workflows/verify.yml`) and confirms all of the arrows above still point at things that exist.
