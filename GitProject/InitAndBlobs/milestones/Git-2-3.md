# Git-2.3 — Create BLOB Files

*Part of the [Initialization and Blobs](../ASSIGNMENT.md) assignment*

---

## Recall

A blob is a copy of a file stored under the name of its SHA-1 hash in the `objects/` directory. The filename is the hash. The content is exactly what the original file contained.

See [blobs.md](../docs/blobs.md) for details.

---

## Instructions

> **Branch reminder:** Are you in a new feature branch?

Implement a method that creates a blob for a given file:

1. Compute the SHA-1 hash of the file's content
2. Create a new file in `git/objects/` using that hash as the filename
3. Write the original file's content into the blob file — byte for byte, unchanged

---

## Stretch Goal — Git-2.3.1

In your tester:

1. Verify programmatically that generated blob files exist in `git/objects/`
2. Update your cleanup method to also remove blob files from `objects/` so tests can be run repeatedly

---

## Stretch Goal — Git-2.3.2 (Optional)

In real Git, file content is compressed before the SHA-1 hash is computed, and the blob stores the compressed data.

Implement this compression behavior:
- Add a global boolean to toggle compression on or off
- Test both modes thoroughly

> **Warning:** Do not implement this unless you are certain your partner in Part 4 will also implement it. Mismatched compression behavior will break the integration.

---

**Commit summary:** `(Git-2.3): Create BLOB Files`

---

← [Git-2.2](Git-2-2.md) — [Back to assignment](../ASSIGNMENT.md) — Next: [Git-2.4](Git-2-4.md) →
