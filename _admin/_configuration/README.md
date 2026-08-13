# Configuration

Schemas and configuration for the course-planning tooling.

| File | Purpose |
|---|---|
| [`module.schema.json`](module.schema.json) | JSON Schema for curated module files in [`_modules/`](../../_modules/) — the contract between the planner UI, the verifier, and the course hub's import |

The planner UI (`../_coursePlannerUI/`) and verifier (`../_verification/verify.py`) enforce the referential parts of this schema (referenced lessons and review files must exist); the schema file itself documents the full shape for editors and for JSON-aware tooling.
