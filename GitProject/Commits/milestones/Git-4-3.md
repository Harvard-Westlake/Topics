# Git-4.3: Regenerate the Index

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## Recall

The index is the list of what is staged, one `<hash> <path>` line per file. After a clone or a checkout, Git throws the old index away and writes a new one from a commit's tree. See the [Commits lesson](../README.md) for how it works.

---

## What to Build

Given a commit, your partner's program can rewrite `git/index` so it lists exactly the files in that commit's snapshot:

- One line per file, `<hash> <path>`, with the full path from the top of the repository (for example `docs/notes.txt`).
- Nothing that is not in that commit's snapshot.
- The same lines you would get by staging those exact files yourself (the order may differ).

**Verify:**

1. Stage a few files, including one inside a folder, and commit.
2. Copy `git/index` somewhere safe, then empty it.
3. Regenerate the index from the commit in `git/HEAD`.
4. The regenerated index has the same lines as your copy.
5. Commit again right away. The new commit's `tree:` hash matches the first commit's.

---

**Commit summary:** `(Git-4.3): Regenerated the Index`

---

← [Git-4.2](Git-4-2.md) | [Back to assignment](../ASSIGNMENT.md) | Next: [Git-4.4](Git-4-4.md) →
