# _hub — HW Course Hub

One local web app for everything course-related, run by each teacher on their own
machine. Three tabs:

| Tab | What it does |
|---|---|
| **Courses** | Canvas course list, assignments, modules, grades, and the Create Module drawer |
| **Year Schedule** | Per-teacher drag-and-drop year plans saved to [`../_schedules/`](../_schedules/) |
| **Module Planner** | Create/edit curated modules in [`../../_modules/`](../../_modules/) with a lesson file editor and Canvas-fidelity preview |

## Setup (once per teacher)

```bash
pip3 install -r _admin/_hub/requirements.txt
cp .env.example .env        # at the repo root — then paste YOUR Canvas token
python3 _admin/_hub/server.py
```

Open http://127.0.0.1:5050.

- `.env` is gitignored — every teacher uses their own Canvas token, which scopes
  syncing to their own course sections.
- **No token?** The app still runs: the Module Planner and Year Schedule tabs are
  fully credential-free; only Canvas features are disabled.
- **Finals** live in the private sibling `Admin` repo (`../Admin/finals/` relative
  to this repo's parent, or set `FINALS_DIR` in `.env`). Teachers without that repo
  cloned simply see finals disabled. Syncing a test/final day to Canvas creates a
  **placeholder assignment only** — exam content never leaves the private repo.

## How the year schedule stays dynamic

`_schedules/<teacher>.json` stores only *references*: a module block points at a
curated `_modules/<slug>.json` or a topic folder. Every request re-reads this repo,
so editing a module's `LESSONS.md` re-dates every schedule that uses it. Tests,
finals, review/flex days, and single lessons can be dropped between modules or
*inside* a module after any given day.

## Class calendars (imported .ics)

The Year Schedule tab's **Import .ics** button accepts a Didax teacher-schedule
export and compresses it into `_schedules/calendars/<schedule>.json` — for every
class slot (Blocks A–G plus named classes like a Directed Study), the static list
of real meeting `[date, start, end]` triples in local time (`icsimport.py`, also
usable standalone: `python3 _admin/_hub/icsimport.py HWSchedule.ics <name>`).
Free blocks are kept too, so a section not present in the export can still be
mapped onto its block's meeting times.

Picking a class in the **Class** dropdown binds the schedule to it
(`calendar` + `calendar_class` in the schedule JSON): class dates then come from
the actual meeting list instead of the weekday grid. First/Last day still clip
the range (start a plan at any meeting) and no-school days still skip dates.
Canvas sync uses the real times: each assignment unlocks when its class period
starts and is due at **11:59 PM the night before the class meets next**.

## Collaboration model

The repo is the sync layer: make changes on a branch, open a change request, and
review together in meetings. The app never commits — it edits your working tree.

`.cache/` here holds Canvas API responses (including student names and grades) —
it is gitignored and must never be committed.
