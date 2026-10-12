# Git-4.3: Regenerate the Index

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## Recall

The index is the list of what is staged, one `<hash> <path>` line per file. A commit's tree holds the same information as nested folders. After a clone or a checkout, Git throws the old index away and writes a new one from the commit's tree.

---

## Instructions

Add a method to your partner's program that rebuilds `git/index` from a commit:

1. Read the commit file at `git/objects/<commitHash>` and take the hash from its `tree:` line.
2. Walk that root tree, one line at a time:
    - `blob <hash> <name>`: add the index line `<hash> <path>`, where the path is every folder walked so far, then the name (for example `docs/notes.txt`).
    - `tree <hash> <name>`: open `git/objects/<hash>` and walk it the same way, with `<name>/` added to the front of every path inside.
3. Replace the contents of `git/index` with the lines you collected.

**Verify:**

1. Stage a few files, including one inside a folder, and commit.
2. Copy `git/index` somewhere safe, then empty it.
3. Rebuild the index from the commit hash in `git/HEAD`.
4. Confirm the rebuilt index has the same lines as your copy (the order may differ).
5. Commit again right away. The new commit's `tree:` hash must match the first commit's.

---

**Commit summary:** `(Git-4.3): Regenerated Index from Commit Tree`

---

← [Git-4.2](Git-4-2.md) | [Back to assignment](../ASSIGNMENT.md) | Next: [Git-4.4](Git-4-4.md) →
