# Git-4.1: Link the Commit File to the Root Tree

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## Recall

A commit file ties the root tree, the previous commit, the author, the date, and the message together into a single object, stored in `objects/` like any blob or tree. After writing it, `git/HEAD` is updated to point to the new commit's hash. **HEAD update must always be the last step.**

See [commits.md](../docs/commits.md) for the full format and step ordering.

---

## Commit File Format

```
tree: <root tree SHA-1>
parent: <previous commit SHA-1>
author: <author name>
date: <current date and time>
message: <commit message>
```

For the **initial commit**, omit the `parent:` line entirely. Do not leave it blank.

---

## Instructions

Update your partner's program to generate commit files:

**Required user inputs (provided by the caller):**
- `author`: the name of the person committing
- `message`: a description of the changes

**Programmatically determined fields:**
- `tree`: SHA-1 of the root tree (built from the index)
- `parent`: current value of `git/HEAD` (empty = first commit, omit the line)
- `date`: current timestamp in a consistent format of your choice

**Steps (in order):**

1. Build tree files from the index and identify the root tree's SHA-1
2. Read `git/HEAD` to get the parent hash (empty file = initial commit)
3. Build the commit file content using the format above
4. Compute the SHA-1 hash of the complete commit content
5. Write the commit file to `git/objects/<commitSHA>`
6. Update `git/HEAD` to the new commit's SHA-1 ← **must be last**

> **Note:** Only the author and message come from the caller. Tree hash, parent hash, and date are all determined by your program.

---

**Commit summary:** `(Git-4.1): Implemented Commit with HEAD Linkage`

---

← [Back to assignment](../ASSIGNMENT.md) | Next: [Git-4.2](Git-4-2.md) →
