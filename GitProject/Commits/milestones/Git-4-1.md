# Git-4.1: Create a Commit (File and HEAD Link)

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## Recall

A commit saves the staged snapshot as one more object in `git/objects/` and links it to the commit before it. See the [Commits lesson](../README.md) for how it works.

---

## What to Build

Your partner's program can make a commit from whatever is staged, given an author and a message.

**A commit file** holds exactly these lines:

```
tree: <root tree SHA-1>
parent: <previous commit SHA-1>
author: <author name>
date: <date and time>
message: <commit message>
```

- `tree` is the root tree of what is staged right now.
- `parent` is the commit HEAD held before this one. The first commit has **no `parent:` line** at all, not a blank one.
- `date` is when the commit was made, in any consistent format.
- Only the author and the message come from whoever makes the commit. Everything else your program works out.

**After a commit:**

- The commit file is saved as `git/objects/<its SHA-1>`.
- `git/HEAD` holds the new commit's hash.
- The new commit's hash is given back to whoever made it.
- If anything fails partway, HEAD still holds the old commit. It never points at a commit that was not saved.

**Verify:**

1. Stage a file and commit. The commit file has no `parent:` line, and HEAD holds its hash.
2. Stage a change and commit again. The new commit's `parent:` is the first commit's hash.
3. Open each commit's `tree:` hash in `git/objects/` and confirm it is the snapshot you staged.

---

**Commit summary:** `(Git-4.1): Created a Commit`

---

← [Back to assignment](../ASSIGNMENT.md) | Next: [Git-4.2](Git-4-2.md) →
