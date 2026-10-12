# Git-4.4: Check Out a Commit

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## Recall

Checkout takes the project back to a point in time. Real Git only deletes and rewrites files it tracks. Files that were never added, and the `git/` folder, are left alone.

---

## Instructions

Implement `GitWrapper.checkout(commitHash)` in your partner's program:

1. Read the commit file at `git/objects/<commitHash>` and take its root tree hash.
2. Delete every file listed in the **current** `git/index`. Then delete any folders that are left empty. Never touch `git/`.
3. Walk the commit's tree and write every blob back to its path:
    - The blob file in `git/objects/<hash>` holds the file's contents. Copy them to the path.
    - Create each folder before writing the files inside it.
4. Rebuild `git/index` from the commit's tree, using your Git-4.3 method.
5. Write `commitHash` into `git/HEAD`, last.

**Verify:**

1. Stage `a.txt` with the text `one` and commit. Save the hash as commit A.
2. Change `a.txt` to `two`, add a new file `docs/b.txt`, stage both, and commit as commit B.
3. Create `scratch.txt` but do not stage it.
4. Check out commit A. Confirm:
    - `a.txt` says `one`.
    - `docs/b.txt` and the `docs` folder are gone.
    - `scratch.txt` is still there, untouched.
    - `git/index` lists only `a.txt`, and `git/HEAD` holds commit A's hash.
5. Check out commit B. Every file from commit B is back, with commit B's contents.

---

**Commit summary:** `(Git-4.4): Implemented Checkout`

---

← [Git-4.3](Git-4-3.md) | [Back to assignment](../ASSIGNMENT.md)
