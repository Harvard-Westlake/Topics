# _schedules — Per-Teacher Year Plans

One JSON file per teacher (e.g. `theiss.json`), edited with the **Year Schedule**
tab of the course hub (`python3 _admin/_hub/server.py`). Each teacher paces their
own sections independently; the files are plain diffable JSON, so plans can be
compared side-by-side in review meetings.

Module blocks store only a **reference** (a `_modules/` slug or a topic folder
name) — lessons and day counts resolve live from the repo, so a change to a
module's `LESSONS.md` automatically re-dates every schedule that uses it.

Block types: `module`, `test`, `final`, `review`, `flex`, `custom`, `lesson`.
Module blocks may carry `inserts` — items placed after a given day inside the
unit. Test/final content itself lives in the private Admin repo, never here.
