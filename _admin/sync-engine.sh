#!/usr/bin/env bash
# One-way engine sync: copy the course-engine files from this repo (the
# canonical engine home) into a sibling course repo.
#
#   Usage (from the Topics repo):  _admin/sync-engine.sh ../DND
#
# The ENGINE is everything that makes a course repo behave like this one:
# the hub, the course planner UI, the module editor, the verifier, schemas,
# styleguides, CI, and the root scaffolding (CLAUDE.md, .gitignore, embed/).
#
# COURSE-SPECIFIC files are NEVER synced (they are excluded below, and
# rsync's --delete never removes excluded paths on the target):
#   _admin/_configuration/course.json      — course name / GitHub repo
#   _admin/_configuration/engine-version.json — the target's sync stamp
#   _admin/_schedules/*.json + calendars/  — per-teacher schedules
#   _admin/_lessonplans/*.md               — generated per-course plans
#   _modules/*.json                        — per-course curated modules
#   topic folders, README.md, SYLLABUS.md, NOTES.md, index.html,
#   attachments/, .env, .claude/
#
# Rule of thumb: engine files must contain ZERO course-specific data — anything
# course-specific belongs in course.json, .env, _modules/, or _admin/_schedules/.
# Feature work on the engine happens ONLY in this repo, then flows outward.

set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_ARG="${1:-}"
if [ -z "$TARGET_ARG" ]; then
  echo "usage: _admin/sync-engine.sh <target-course-repo>   e.g. _admin/sync-engine.sh ../DND" >&2
  exit 1
fi
TARGET="$(cd "$TARGET_ARG" && pwd)"

if [ "$TARGET" = "$SRC" ]; then
  echo "error: target is the source repo" >&2
  exit 1
fi
if [ ! -d "$TARGET/.git" ]; then
  echo "error: $TARGET is not a git repository" >&2
  exit 1
fi

# Engine manifest
ENGINE_DIRS=( _admin embed .github )
ENGINE_FILES=( CLAUDE.md .gitignore .nojekyll .env.example _modules/README.md )

# Warn if the engine is dirty in the source — the stamped commit hash would
# not describe the files actually copied.
if [ -n "$(git -C "$SRC" status --porcelain -- "${ENGINE_DIRS[@]}" "${ENGINE_FILES[@]}" 2>/dev/null)" ]; then
  echo "warning: uncommitted engine changes in $SRC — the stamped commit will not match the copied files" >&2
fi

echo "Syncing engine: $SRC → $TARGET"

rsync -a --delete \
  --exclude '_configuration/course.json' \
  --exclude '_configuration/engine-version.json' \
  --exclude '_schedules/*.json' \
  --exclude '_schedules/calendars/**' \
  --include '_lessonplans/README.md' \
  --exclude '_lessonplans/*.md' \
  --exclude '_solutions/' \
  --exclude '.cache/' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.DS_Store' \
  "$SRC/_admin/" "$TARGET/_admin/"

rsync -a --delete --exclude '.DS_Store' "$SRC/embed/"   "$TARGET/embed/"
rsync -a --delete --exclude '.DS_Store' "$SRC/.github/" "$TARGET/.github/"

for f in "${ENGINE_FILES[@]}"; do
  mkdir -p "$TARGET/$(dirname "$f")"
  cp "$SRC/$f" "$TARGET/$f"
done

# Stamp the engine version so the target always records exactly which commit
# of the canonical repo its engine came from (re-sync from any commit by
# checking it out here first).
COMMIT="$(git -C "$SRC" rev-parse HEAD)"
ORIGIN="$(git -C "$SRC" remote get-url origin 2>/dev/null || echo "$SRC")"
mkdir -p "$TARGET/_admin/_configuration"
cat > "$TARGET/_admin/_configuration/engine-version.json" <<EOF
{
  "synced_from": "$ORIGIN",
  "commit": "$COMMIT",
  "date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

# First sync into a fresh repo: seed a course.json the teacher edits once.
COURSE_JSON="$TARGET/_admin/_configuration/course.json"
if [ ! -f "$COURSE_JSON" ]; then
  NAME="$(basename "$TARGET")"
  cat > "$COURSE_JSON" <<EOF
{
  "course_name": "$NAME",
  "repo_label": "$NAME",
  "github_repo": "Harvard-Westlake/$NAME",
  "github_branch": "main"
}
EOF
  echo "created $COURSE_JSON — edit course_name / github_repo if needed"
fi

echo "done — engine at commit ${COMMIT:0:12}"
echo "review with:  git -C $TARGET status  &&  git -C $TARGET diff"
