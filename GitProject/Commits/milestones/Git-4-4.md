# Git-4.4: Check Out a Commit

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## Recall

Checkout takes the project back to a point in time. Real Git only changes files it tracks. See the [Commits lesson](../README.md) for how it works.

---

## What to Build

Fill in `checkout(commitHash)` in `GitWrapper`. Given a commit hash, afterward:

- Every file in that commit's snapshot exists at its path, with that commit's contents.
- Files that were tracked before but are not in that commit are gone, and so are folders they leave empty.
- Files that were never staged are untouched, and so is everything in `git/`.
- `git/index` lists exactly that commit's files, the same as regenerating it (Git-4.3).
- `git/HEAD` holds that commit's hash.

**Verify:**

1. Stage `a.txt` containing `one` and commit. Call this commit A.
2. Change `a.txt` to `two`, add `docs/b.txt`, stage both, and commit. Call this commit B.
3. Create `scratch.txt` but do not stage it.
4. Check out commit A:
    - `a.txt` says `one`.
    - `docs/b.txt` and the `docs` folder are gone.
    - `scratch.txt` is still there.
    - The index lists only `a.txt`, and HEAD holds commit A's hash.
5. Check out commit B. Every file from commit B is back with commit B's contents.

---

**Commit summary:** `(Git-4.4): Checked Out a Commit`

---

← [Git-4.3](Git-4-3.md) | [Back to assignment](../ASSIGNMENT.md)
