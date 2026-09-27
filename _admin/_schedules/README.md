# _schedules — Per-Teacher Year Plans

One JSON file per teacher (e.g. `theiss.json`), edited with the **Year Schedule**
tab of the course hub (`python3 _admin/_hub/server.py`). Each teacher paces their
own sections independently; the files are plain diffable JSON, so plans can be
compared side-by-side in review meetings.

Module blocks store only a **reference** (a `_modules/` slug or a topic folder
name) — lessons and day counts resolve live from the repo, so a change to a
module's `LESSONS.md` automatically re-dates every schedule that uses it.

`"ref"` (default `"main"`) is the git branch or tag this teacher's Canvas course
follows: every Canvas item the hub creates for the schedule links to the live
lesson view (`view.html` on GitHub Pages) for that ref, so students see content
straight from the repo and each teacher can run their own branch. Set it with
the **Branch** field in the Year Schedule tab.

Block types: `module`, `test`, `final`, `review`, `flex`, `custom`, `lesson`.
Module blocks may carry `inserts` — items placed after a given day inside the
unit. Test/final content itself lives in the private Admin repo, never here.

## calendars/

`calendars/<name>.json` is the compressed local copy of a Didax teacher-schedule
`.ics` export (imported with the Year Schedule tab's **Import .ics** button, or
`python3 _admin/_hub/icsimport.py <file.ics> <name>`). It lists every class slot
— Blocks A–G (free blocks included, so unlisted sections can still be mapped)
plus named non-block classes — each with its real meeting `[date, start, end]`
triples in local time, plus holiday/special-day and day-cycle markers.

A schedule binds to one class via `"calendar"` (file name) and
`"calendar_class"` (class id, e.g. `"block-a"`) — its class dates then come
from the real meeting list instead of the weekday grid, and Canvas sync gains
real times: assignments unlock at class start and are due 11:59 PM the night
before the next class meeting. No student data lives in these files.
