#!/usr/bin/env python3
"""curriculum — find and re-date the curated modules and schedules that carry a lesson.

Content lives in topic folders; a lesson only reaches the calendar once a curated module
(_modules/<slug>.json) lists it; teacher schedules (_admin/_schedules/<name>.json) reference
modules and re-resolve from the repo on every request. So when a lesson is ADDED to a
topic (a new day in the middle of a unit, say), the module has to gain a row for it —
and every later day in every schedule that carries that module moves by one class
meeting. This tool does the module edit and shows exactly what moved, per teacher.

    python3 _admin/_hub/curriculum.py where  GitProject/PeerCodeVerification
    python3 _admin/_hub/curriculum.py insert git-project GitProject/PeerCodeVerification --after InitAndBlobs
    python3 _admin/_hub/curriculum.py remove git-project GitProject/PeerCodeVerification
    python3 _admin/_hub/curriculum.py dates  theiss [--block git-project]
    python3 _admin/_hub/curriculum.py impact git-project      # which schedules carry this module, with dates
    python3 _admin/_hub/curriculum.py quizzes                 # quizzes in the private Exams checkout, by quiz_id
    python3 _admin/_hub/curriculum.py insert-quiz git-project <quiz_id> --after PeerCodeVerification [--duration 0.5]

`insert` / `remove` rewrite the module JSON (renumbering days like the Planner does,
½-days included), regenerate _admin/_lessonplans/ through verify.py --fix, and print a
before/after table of every affected schedule block. They never touch schedules or
Canvas: dates re-resolve on their own, and pushing them to Canvas is the Year Schedule
tab's Sync button, which updates posted items in place (see CLAUDE.md, "Re-dating").

Runs on the hub's virtualenv (it imports the hub for the resolver):
    _admin/_hub/.venv/bin/python _admin/_hub/curriculum.py …
Plain `python3` re-executes itself there when Flask is missing.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]

try:
    import flask  # noqa: F401  — the hub's resolver needs it
except ImportError:
    venv_py = HERE / ".venv" / "bin" / "python"
    # sys.executable resolves through the venv's symlink to the same binary, so
    # compare the active prefix, not the interpreter path
    if venv_py.exists() and pathlib.Path(sys.prefix).resolve() != (HERE / ".venv").resolve():
        os.execv(str(venv_py), [str(venv_py), __file__] + sys.argv[1:])
    sys.exit("curriculum.py: Flask is not installed — run with _admin/_hub/.venv/bin/python "
             "(or pip3 install -r _admin/_hub/requirements.txt)")

sys.path.insert(0, str(HERE))
import server as hub  # noqa: E402


# ---------------------------------------------------------------- helpers

def split_lesson(arg):
    parts = arg.strip("/").split("/")
    if len(parts) != 2:
        sys.exit(f"curriculum.py: lesson must be <Topic>/<Lesson>, got {arg!r}")
    topic, path = parts
    if not (ROOT / topic / path / "README.md").exists():
        sys.exit(f"curriculum.py: {topic}/{path}/README.md does not exist")
    return topic, path


def module_path(slug):
    p = hub.MODULES_DIR / f"{slug}.json"
    if not p.exists():
        sys.exit(f"curriculum.py: no curated module _modules/{slug}.json")
    return p


def renumber(assignments):
    """Sequential day numbers from array order — the Planner's rule: a full-day item
    takes `duration` days; two consecutive ½-days share one day as .0 and .1; an
    unpaired ½-day still consumes its whole slot."""
    day, half_open = 1, False
    for a in assignments:
        dur = a.get("duration") or 1
        if dur == 0.5:
            if half_open:
                a["day"], a["sub"], half_open = day, 1, False
                day += 1
            else:
                a["day"], a["sub"], half_open = day, 0, True
        else:
            if half_open:
                day, half_open = day + 1, False
            a["day"] = day
            a.pop("sub", None)
            day += int(dur)
    return assignments


def schedules_carrying(slug, topic=None):
    """[(name, sched)] for every schedule whose sequence references the module slug
    (saved module) or the topic folder itself (topic-sourced block)."""
    out = []
    for sf in sorted(hub.SCHEDULES_DIR.glob("*.json")):
        try:
            sched = json.loads(sf.read_text())
        except json.JSONDecodeError:
            continue
        for b in sched.get("sequence", []):
            if b.get("type") != "module":
                continue
            if (b.get("source", "saved") == "saved" and b.get("ref") == slug) or \
               (b.get("source") == "topic" and topic and b.get("ref") == topic):
                out.append((sf.stem, sched))
                break
    return out


def block_table(sched):
    """{block id: (label, start, end, days)} for a schedule's resolved blocks."""
    res = hub.resolve_schedule(sched)
    rows = {}
    for b in res["blocks"]:
        label = (f"Unit {b['unit_number']}: {b.get('name')}" if b["type"] == "module"
                 else f"{b['type']}: {b.get('title')}")
        rows[b.get("id")] = (label, b.get("start"), b.get("end"), b.get("days", 0))
    return rows, res


def fmt(d):
    return d or "—"


def print_shift(name, before, after, warnings=()):
    print(f"\n  schedule {name}")
    print(f"    {'block':<44} {'before':<25} {'after':<25} {'shift'}")
    for bid, (label, s1, e1, d1) in before.items():
        label2, s2, e2, d2 = after.get(bid, (label, None, None, 0))
        moved = (s1, e1) != (s2, e2)
        shift = ""
        if moved and s1 and s2:
            delta = (date.fromisoformat(s2) - date.fromisoformat(s1)).days
            shift = f"{delta:+d} cal. days" + (f", {d2 - d1:+d} class day(s)" if d1 != d2 else "")
        elif moved:
            shift = "changed"
        mark = "*" if moved else " "
        print(f"  {mark} {label[:44]:<44} {fmt(s1)} → {fmt(e1):<12} {fmt(s2)} → {fmt(e2):<12} {shift}")
    for w in warnings:
        print(f"    ! {w}")


def regenerate_lessonplans():
    r = subprocess.run([sys.executable, str(ROOT / "_admin" / "_verification" / "verify.py"), "--fix"],
                       capture_output=True, text=True)
    tail = [l for l in r.stdout.splitlines() if "error(s)" in l or "verified" in l.lower()]
    print("  verify.py --fix:", " | ".join(tail) or r.stdout.strip()[-200:])
    if r.returncode != 0:
        print(r.stdout[-2000:], file=sys.stderr)
        sys.exit("curriculum.py: verify.py reported errors — fix them before committing")


def save_module(path, mod):
    mod["updated"] = date.today().isoformat()
    path.write_text(json.dumps(mod, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- commands

def cmd_where(args):
    topic, path = split_lesson(args.lesson)
    usage = hub._scan_usage(topic, path)
    print(f"{topic}/{path}")
    if not usage["modules"]:
        print("  in no curated module — it is NOT on any calendar. "
              f"Add it with: curriculum.py insert <slug> {topic}/{path} --after <PrevLesson>")
    for m in usage["modules"]:
        print(f"  module _modules/{m['slug']}.json  (unit {m['unit_number']}, “{m['name']}”)")
    lessons_by_sched = {}
    for m in usage["modules"]:
        for name, sched in schedules_carrying(m["slug"], topic):
            _, res = block_table(sched)
            for b in res["blocks"]:
                for s in b.get("slots", []):
                    les = s.get("lesson") or {}
                    if les.get("_module") == topic and les.get("path") == path and s.get("part", 1) == 1:
                        lessons_by_sched.setdefault(name, []).append(
                            f"Unit {b['unit_number']} day {s.get('day_num')} — {fmt(s.get('date'))}"
                            + (f" (ref {hub.schedule_ref(sched)})" if sched.get("ref") else ""))
    for name, hits in lessons_by_sched.items():
        print(f"  schedule {name}: " + "; ".join(hits))
    if usage["modules"] and not lessons_by_sched:
        print("  no schedule carries those modules")


def cmd_impact(args):
    slug = args.module
    mod = json.loads(module_path(slug).read_text())
    topic = (mod.get("topic_names") or [None])[0]
    carriers = schedules_carrying(slug, topic)
    print(f"_modules/{slug}.json — {len(mod.get('assignments', []))} rows, "
          f"{sum(int(a.get('duration') or 1) for a in mod.get('assignments', []))} class days")
    if not carriers:
        print("  no schedule carries this module")
    for name, sched in carriers:
        rows, res = block_table(sched)
        print(f"  schedule {name} (ref {hub.schedule_ref(sched)}):")
        for bid, (label, s, e, d) in rows.items():
            print(f"    {label[:44]:<44} {fmt(s)} → {fmt(e)}  ({d} class days)")
        for w in res["warnings"]:
            print(f"    ! {w}")


def cmd_dates(args):
    sched = hub.load_schedule(args.schedule)
    if sched is None:
        sys.exit(f"curriculum.py: no schedule _admin/_schedules/{args.schedule}.json")
    res = hub.resolve_schedule(sched)
    print(f"{args.schedule} — ref {hub.schedule_ref(sched)}; class days used {res['calendar']['used']}"
          f" of {res['calendar']['total']}" + (f"; day 0 syllabus {res['day0_date']}" if res.get("day0_date") else ""))
    for b in res["blocks"]:
        if args.block and b.get("ref") != args.block and b.get("title") != args.block:
            continue
        label = f"Unit {b['unit_number']}: {b.get('name')}" if b["type"] == "module" else f"{b['type']}: {b.get('title')}"
        print(f"\n  {label}  {fmt(b.get('start'))} → {fmt(b.get('end'))}  ({b.get('days', 0)} class days)")
        for s in b.get("slots", []):
            num = f"{b['unit_number']}.{s.get('day_num')}" if b["type"] == "module" else "   "
            print(f"    {fmt(s.get('date')):<12} {num:<6} {s.get('title')}")
    for w in res["warnings"]:
        print(f"  ! {w}")


def _edit_module(args, mutate):
    slug = args.module
    path = module_path(slug)
    mod = json.loads(path.read_text())
    topic = (mod.get("topic_names") or [None])[0]
    carriers = schedules_carrying(slug, topic)
    before = {name: block_table(sched)[0] for name, sched in carriers}
    mutate(mod)
    renumber(mod["assignments"])
    if args.dry_run:
        print(json.dumps(mod["assignments"], indent=2, ensure_ascii=False))
        print("(dry run — nothing written)")
        return
    save_module(path, mod)
    print(f"wrote _modules/{slug}.json:")
    for a in mod["assignments"]:
        sub = f".{a['sub']}" if a.get("sub") is not None else ""
        tag = (f"  [quiz {a.get('quiz_id')}]" if a.get("kind") == "quiz" else
               "  (placeholder)" if a.get("placeholder") else f"  [{a.get('_module')}/{a.get('path')}]")
        print(f"  day {a['day']}{sub:<3} ×{a.get('duration', 1):<4} {a['title']}{tag}")
    regenerate_lessonplans()
    if not carriers:
        print("no schedule carries this module — nothing re-dates")
        return
    print(f"\nre-dated {len(carriers)} schedule(s) — * marks blocks whose dates moved:")
    for name, sched in carriers:
        rows, res = block_table(sched)
        print_shift(name, before[name], rows, res["warnings"])
    print("\nnext: commit, then in the Year Schedule tab click Sync on each * block whose unit is already "
          "on Canvas — Sync updates posted items in place (renames, re-dates, creates the new day).")


def cmd_quizzes(_args):
    if not hub.exams_available():
        sys.exit(f"curriculum.py: no Exams checkout at {hub.EXAMS_DIR / hub.EXAMS_CLASS} (set EXAMS_DIR)")
    qs = hub.list_quizzes()
    if not qs:
        print("no quizzes — add <Class>/<Topic>/Quizzes/<slug>/quiz.meta.json in the Exams repo")
    for q in qs:
        state = "unlocked" if q["unlocked"] else ("locked" if q["locked"] else "no archive")
        print(f"{q['quiz_id']}  {q['topic']:<16} {q['title'][:60]:<60} {q['points'] or '?':>4} pts  {state}")
        if q.get("lesson"):
            print(f"{'':18}pairs with {q['lesson']}")


def cmd_insert_quiz(args):
    q = hub.quiz_by_id(args.quiz_id)
    if q is None:
        sys.exit(f"curriculum.py: quiz_id {args.quiz_id!r} is not in {hub.EXAMS_DIR / hub.EXAMS_CLASS} — run `quizzes`")

    def mutate(mod):
        rows = mod.setdefault("assignments", [])
        if any(a.get("quiz_id") == q["quiz_id"] for a in rows):
            sys.exit(f"curriculum.py: quiz {q['quiz_id']} is already in _modules/{args.module}.json")
        new = {"day": 0, "duration": args.duration, "title": args.title or f"Quiz: {q['title']}",
               "path": "", "_module": "", "placeholder": True, "kind": "quiz", "quiz_id": q["quiz_id"],
               "review": None}
        if args.after in (None, "start"):
            idx = 0
        else:
            idx = next((i + 1 for i, a in enumerate(rows) if a.get("path") == args.after), None)
            if idx is None:
                sys.exit(f"curriculum.py: --after {args.after!r} is not a lesson path in this module; "
                         f"rows: {[a.get('path') for a in rows]}")
        rows.insert(idx, new)
    _edit_module(args, mutate)


def cmd_insert(args):
    topic, lesson = split_lesson(args.lesson)

    def mutate(mod):
        rows = mod.setdefault("assignments", [])
        if any(a.get("_module") == topic and a.get("path") == lesson for a in rows):
            sys.exit(f"curriculum.py: {topic}/{lesson} is already in _modules/{args.module}.json")
        if topic not in (mod.get("topic_names") or []):
            mod.setdefault("topic_names", []).append(topic)
        title = args.title or hub._lesson_title(topic, lesson)
        new = {"day": 0, "duration": args.duration, "title": title, "path": lesson,
               "_module": topic, "review": None}
        if args.after in (None, "start"):
            idx = 0
        else:
            idx = next((i + 1 for i, a in enumerate(rows) if a.get("path") == args.after), None)
            if idx is None:
                sys.exit(f"curriculum.py: --after {args.after!r} is not a lesson path in this module; "
                         f"rows: {[a.get('path') for a in rows]}")
        rows.insert(idx, new)
    _edit_module(args, mutate)


def cmd_remove(args):
    topic, lesson = split_lesson(args.lesson)

    def mutate(mod):
        rows = mod.get("assignments", [])
        keep = [a for a in rows if not (a.get("_module") == topic and a.get("path") == lesson)]
        if len(keep) == len(rows):
            sys.exit(f"curriculum.py: {topic}/{lesson} is not in _modules/{args.module}.json")
        mod["assignments"] = keep
    _edit_module(args, mutate)


def main():
    ap = argparse.ArgumentParser(prog="curriculum.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("where", help="which modules and schedules carry a lesson, and on what dates")
    p.add_argument("lesson")
    p = sub.add_parser("impact", help="which schedules carry a module; block dates")
    p.add_argument("module")
    p = sub.add_parser("dates", help="every block and day of a schedule with its date")
    p.add_argument("schedule"); p.add_argument("--block")
    sub.add_parser("quizzes", help="quizzes available in the private Exams checkout (quiz_id, title, state)")
    p = sub.add_parser("insert-quiz", help="place a quiz (by quiz_id) in a curated module and re-date")
    p.add_argument("module"); p.add_argument("quiz_id")
    p.add_argument("--after", help="lesson path to insert after ('start' = first)")
    p.add_argument("--duration", type=float, default=1); p.add_argument("--title")
    p.add_argument("--dry-run", action="store_true")
    for name, helptext in (("insert", "add a lesson to a curated module and re-date"),
                           ("remove", "drop a lesson from a curated module and re-date")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("module"); p.add_argument("lesson")
        if name == "insert":
            p.add_argument("--after", help="lesson path to insert after ('start' = first)")
            p.add_argument("--duration", type=float, default=1)
            p.add_argument("--title")
        p.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if getattr(args, "duration", None) is not None:
        args.duration = 0.5 if args.duration == 0.5 else int(args.duration)
    {"where": cmd_where, "impact": cmd_impact, "dates": cmd_dates, "quizzes": cmd_quizzes,
     "insert": cmd_insert, "insert-quiz": cmd_insert_quiz, "remove": cmd_remove}[args.cmd](args)


if __name__ == "__main__":
    main()
