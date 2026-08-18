#!/usr/bin/env python3
"""Compress a Didax teacher-schedule .ics export into a compact calendar JSON.

The export lists every meeting of every block (A-G) plus non-block classes
(e.g. Directed Study), lunch/break/seminar filler, all-day day-cycle markers
("US Day 1".."US Day 6"), and holidays/breaks. This module boils that down to
the part course planning needs: for each class slot, the static ordered list
of real meeting dates and times, in local time.

Classification rules (validated against the 2026-27 Didax export):
  - Real classes carry  DESCRIPTION:Session N of M  — these are "the classes
    the teacher has" (block classes with a course name, and named non-block
    classes like a Directed Study).
  - Free blocks ("Block C ", no course, TRANSP:TRANSPARENT) are still kept as
    mappable slots — a class not present in the export (another section on
    blocks A-F) can be mapped onto its block's meeting times.
  - All-day events are markers: "US Day N ..." becomes the day_cycle map,
    everything else (holidays, breaks, exam days) a special_days entry.
  - Remaining timed filler (Lunch, Break, seminars, office hours) is dropped.

Output shape ("hw-calendar-v1"):
  {
    "format": "hw-calendar-v1",
    "source_file": "HWSchedule.ics",
    "imported": "2026-08-18T12:00:00",
    "timezone": "America/Los_Angeles",
    "year_label": "2026-2027",
    "classes": [
      {"id": "block-a", "block": "A",
       "course": "Honors Topics in Computer Science",   # null on a free block
       "location": "Kutler Center 301", "sessions": 80,
       "meetings": [["2026-08-24", "08:00", "08:35"], ...]},   # local time
      ...
    ],
    "special_days": [{"date": "2026-09-21", "label": "Holiday - Yom Kippur"}, ...],
    "day_cycle": {"2026-08-26": "US Day 1", ...}
  }

Usable standalone:  python3 icsimport.py HWSchedule.ics [name]
writes _admin/_schedules/calendars/<name>.json and prints a summary.
"""
from datetime import datetime, timezone, date as date_cls
from zoneinfo import ZoneInfo
import json, re, sys
from pathlib import Path

DEFAULT_TZ = "America/Los_Angeles"
SESSION_RE = re.compile(r"Session\s+(\d+)\s+of\s+(\d+)")
BLOCK_RE = re.compile(r"^Block\s+([A-Z])\b\s*(?:/\s*(.*))?$")
DAY_CYCLE_RE = re.compile(r"^US Day \d+")
YEAR_RE = re.compile(r"(\d{4}-\d{4})")


def _unfold(text):
    """Join RFC 5545 folded lines (continuations start with space or tab)."""
    out = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if line[:1] in (" ", "\t") and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return out


def _unescape(value):
    return (value.replace("\\n", "\n").replace("\\N", "\n")
                 .replace("\\,", ",").replace("\\;", ";").replace("\\\\", "\\"))


def parse_events(text):
    """(calendar_props, [event dicts]) — property params are stripped from keys."""
    props, events, current = {}, [], None
    for line in _unfold(text):
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.split(";")[0].upper()
        if key == "BEGIN" and value.strip() == "VEVENT":
            current = {}
        elif key == "END" and value.strip() == "VEVENT":
            if current is not None:
                events.append(current)
            current = None
        elif current is not None:
            current[key] = _unescape(value.strip())
        else:
            props[key] = value.strip()
    return props, events


def _parse_dt(value, tz):
    """An ICS DTSTART/DTEND value → (date_iso, 'HH:MM' local or None for all-day)."""
    value = value.strip()
    if re.fullmatch(r"\d{8}", value):                       # all-day: VALUE=DATE
        d = datetime.strptime(value, "%Y%m%d").date()
        return d.isoformat(), None
    if value.endswith("Z"):
        dt = datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        dt = dt.astimezone(tz)
    else:                                                    # floating → already local
        dt = datetime.strptime(value, "%Y%m%dT%H%M%S")
    return dt.date().isoformat(), dt.strftime("%H:%M")


def _slug(text):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-") or "class"


def compress_calendar(ics_text, source_file="upload.ics", now=None):
    """Compress raw ICS text into the hw-calendar-v1 dict. Raises ValueError."""
    props, events = parse_events(ics_text)
    if not events:
        raise ValueError("No VEVENT entries found — is this an .ics export?")
    tzname = props.get("X-WR-TIMEZONE") or DEFAULT_TZ
    try:
        tz = ZoneInfo(tzname)
    except Exception:
        tzname, tz = DEFAULT_TZ, ZoneInfo(DEFAULT_TZ)

    classes = {}          # id -> class record
    special, day_cycle = {}, {}
    year_label = None

    for ev in events:
        summary = (ev.get("SUMMARY") or "").strip()
        start = ev.get("DTSTART")
        if not summary or not start:
            continue
        cats = ev.get("CATEGORIES", "")
        if not year_label:
            m = YEAR_RE.search(cats)
            if m:
                year_label = m.group(1)
        date_iso, start_hm = _parse_dt(start, tz)

        if start_hm is None or ev.get("X-MICROSOFT-CDO-ALLDAYEVENT", "").upper() == "TRUE":
            if DAY_CYCLE_RE.match(summary):
                day_cycle[date_iso] = summary
            else:
                special.setdefault(date_iso, summary)
            continue

        session = SESSION_RE.search(ev.get("DESCRIPTION", ""))
        block = BLOCK_RE.match(summary)
        if not session and not block:
            continue                                 # lunch, break, seminars, …

        if block:
            letter = block.group(1)
            course = (block.group(2) or "").strip() or None
            cid, name = f"block-{letter.lower()}", None
        else:
            letter, course = None, summary
            cid = _slug(summary)

        _, end_hm = _parse_dt(ev.get("DTEND", start), tz)
        rec = classes.setdefault(cid, {"id": cid, "block": letter, "course": course,
                                       "location": None, "sessions": 0, "meetings": []})
        if course and not rec["course"]:
            rec["course"] = course
        if ev.get("LOCATION") and not rec["location"]:
            rec["location"] = ev["LOCATION"]
        if session:
            rec["sessions"] = max(rec["sessions"], int(session.group(2)))
        rec["meetings"].append([date_iso, start_hm, end_hm])

    for rec in classes.values():
        rec["meetings"].sort()
        if not rec["sessions"]:
            rec["sessions"] = len(rec["meetings"])

    # Blocks with a course first (A→G), then named classes, then free blocks
    def order(rec):
        return (rec["course"] is None, rec["block"] is None, rec["block"] or "", rec["id"])

    return {
        "format": "hw-calendar-v1",
        "source_file": source_file,
        "imported": (now or datetime.now()).isoformat(timespec="seconds"),
        "timezone": tzname,
        "year_label": year_label,
        "classes": sorted(classes.values(), key=order),
        "special_days": [{"date": d, "label": lbl} for d, lbl in sorted(special.items())],
        "day_cycle": dict(sorted(day_cycle.items())),
    }


def calendar_summary(cal):
    lines = [f"{cal['year_label'] or 'calendar'} — timezone {cal['timezone']}"]
    for c in cal["classes"]:
        first = c["meetings"][0][0] if c["meetings"] else "?"
        last = c["meetings"][-1][0] if c["meetings"] else "?"
        label = (f"Block {c['block']} — {c['course']}" if c["block"] and c["course"]
                 else f"Block {c['block']} (free)" if c["block"] else c["course"])
        lines.append(f"  {label}: {len(c['meetings'])} meetings, {first} → {last}"
                     + (f" @ {c['location']}" if c["location"] else ""))
    lines.append(f"  special days: {len(cal['special_days'])}, "
                 f"day-cycle markers: {len(cal['day_cycle'])}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 icsimport.py <schedule.ics> [name]")
    src = Path(sys.argv[1])
    cal = compress_calendar(src.read_text(), source_file=src.name)
    print(calendar_summary(cal))
    if len(sys.argv) > 2:
        out = Path(__file__).resolve().parents[1] / "_schedules" / "calendars" / f"{sys.argv[2]}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(cal, indent=2) + "\n")
        print(f"wrote {out}")
