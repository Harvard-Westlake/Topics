# Configuration

Schemas and configuration for the course-planning tooling.

| File | Purpose |
|---|---|
| [`module.schema.json`](module.schema.json) | JSON Schema for curated module files in [`_modules/`](../../_modules/) — the contract between the planner UI, the verifier, and the course hub's import |
| `course.json` | **Course-specific, never synced** — course name, UI repo label, and GitHub repo/branch, read at startup by the hub and planner. Every course repo has its own. |
| `engine-version.json` | **Course-specific, never synced** — present only in sibling course repos; records which commit of the canonical engine repo the last `sync-engine.sh` run copied from |

The planner UI (`../_coursePlannerUI/`) and verifier (`../_verification/verify.py`) enforce the referential parts of this schema (referenced lessons and review files must exist); the schema file itself documents the full shape for editors and for JSON-aware tooling.
