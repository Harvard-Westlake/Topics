# Git-5.1: Get the Code Running

*Part of the [Branches](../ASSIGNMENT.md) assignment*

---

## Recall

Branching builds on commits and checkout. If those do not work, nothing in Git-5.2 will. See the [Commits reference](../../Commits/docs/commits.md) for how they work.

---

## What to Build

A repository where every Part 4 operation provably works, run only through its interface:

| Operation | What must happen |
|---|---|
| **Initialize** | `git/`, `git/objects/`, `git/index`, and `git/HEAD` exist. Running it again changes nothing. |
| **Stage a file** | The blob is saved and the index lists it. Changed content replaces that file's line. |
| **Commit** | The commit file is saved, HEAD holds its hash, and the hash is given back. |
| **Check out** a commit | Tracked files, the index, and HEAD match that commit. Untracked files are untouched. |

**Verify:**

1. Initialize, stage two files (one inside a folder), and commit. Call this commit A.
2. Change one file, stage it, and commit. Call this commit B. Its `parent:` is commit A.
3. Check out commit A, then commit B. The files match each commit.
4. Write every bug you found, and how you fixed it, in `README.md`.

---

**Commit summary:** `(Git-5.1): Code Running`

---

← [Back to assignment](../ASSIGNMENT.md) | Next: [Git-5.2](Git-5-2.md) →
