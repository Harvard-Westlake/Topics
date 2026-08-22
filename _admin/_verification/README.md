# Verification

`verify.py` checks that the curriculum is internally consistent — every link, index, and curated module reference resolves. Run it after any content or module change:

```bash
python3 _admin/_verification/verify.py          # check only (exit 1 on errors)
python3 _admin/_verification/verify.py --fix    # also regenerate _admin/_lessonplans/*.md
```

It also runs automatically on every push via [`.github/workflows/verify.yml`](../../.github/workflows/verify.yml).

## What it checks

| Area | Checks |
|---|---|
| Links | Every relative link and image in every `.md` file resolves to a real file or folder |
| Topics | Each topic folder has `LESSONS.md` + `README.md`; every `LESSONS.md` path exists; every lesson folder is listed; every topic is linked from the root `README.md` |
| Lessons | Each lesson README has a Check for Understanding section; `ASSIGNMENT.md` is linked when present (and only when present) |
| Curated modules | Each `_modules/*.json` parses, its slug matches the filename, every referenced lesson and review file exists, titles match `LESSONS.md` (warns on drift), and the generated `_lessonplans/<slug>.md` is in sync |

Errors fail the run (exit 1); warnings are informational. Python 3 standard library only.
