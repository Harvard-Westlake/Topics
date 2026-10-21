# Git-5.2: Add Branching

*Part of the [Branches](../ASSIGNMENT.md) assignment*

---

## Recall

A branch is a file holding one commit hash, HEAD names the branch you are on, and committing moves only that branch. See the [Branches lesson](../README.md) for how it works.

---

## What to Build

A simpler version of real Git's branches, inside your `git/` folder.

**The files:**

| File | Holds |
|---|---|
| `git/refs/heads/<name>` | One line: the hash of the newest commit on that branch. |
| `git/HEAD` | Either `ref: refs/heads/<name>` (on a branch), or a commit hash (detached). |

**Initialize** now also creates `git/refs/heads/` and writes `ref: refs/heads/main` into HEAD, so every new repository starts on `main`.

**Commit**, when HEAD names a branch:

- The new commit's `parent:` is the hash in that branch's file. If the branch file does not exist yet (the first commit), there is no `parent:` line.
- Afterward the branch file holds the new commit's hash, and it is created if it did not exist. HEAD is unchanged.
- When HEAD holds a commit hash (detached), commit works exactly as in Part 4.

**Two new operations in the interface:**

| Operation | Given | What happens |
|---|---|---|
| **Create a branch** | a branch name | A new branch file holds the commit you are on. HEAD does not change. It is an error if that branch already exists, or if there are no commits yet. |
| **Check out a branch** | a branch name | Everything from checking out that branch's commit (Git-4.4), then HEAD holds `ref: refs/heads/<name>`. It is an error if the branch does not exist. |

The interface's `checkout` now takes a branch name as well as a commit hash. A hash still leaves HEAD holding that hash, detached, exactly as in Part 4. Any other name is an error, unless you take on the assignment's [stretch goal](../ASSIGNMENT.md#stretch-goal).

Show both new operations in `README.md`, with a short example someone could copy.

**Verify:**

1. Delete `git/` and initialize. HEAD holds `ref: refs/heads/main`.
2. Stage `a.txt` containing `one` and commit. `git/refs/heads/main` now holds that commit's hash.
3. Create a branch `feature`. Both branch files hold the same hash, and HEAD still names `main`.
4. Check out `feature`. Change `a.txt` to `two`, stage it, and commit. `feature` moved to the new commit; `main` did not.
5. Check out `main`. `a.txt` says `one`, and HEAD holds `ref: refs/heads/main`.
6. Check out `feature` again. `a.txt` says `two`.
7. Creating `feature` a second time, or checking out a branch that does not exist, is an error and changes nothing.

---

**Commit summary:** `(Git-5.2): Added Branching`

---

← [Git-5.1](Git-5-1.md) | [Back to assignment](../ASSIGNMENT.md)
