# Assignment — Initialization and Blobs

*Lesson: [Initialization and Blobs](README.md)*

**Duration:** 3 class periods  
**Due:** End of this block

---

## Reference Docs

Read before starting any milestone:

- [BLOBs — how content-addressed storage works](../Docs/blobs.md)
- [Index File — what the index tracks and its format](../Docs/index-file.md)

---

## Milestones

| Milestone | What you'll build | Commit label |
|---|---|---|
| [GP-2.1 — Initialize a Repository](milestones/gp-2-1.md) | `git/`, `objects/`, `index`, `HEAD` | `(GP-2.1): Program Can Initialize Repository` |
| [GP-2.2 — Create a Hash Function](milestones/gp-2-2.md) | SHA-1 hash from file contents | `(GP-2.2): Created a Hash Function` |
| [GP-2.3 — Create BLOB Files](milestones/gp-2-3.md) | Store files in `objects/` by hash | `(GP-2.3): Create BLOB Files` |
| [GP-2.4 — Update the Index File](milestones/gp-2-4.md) | Write `hash path` entries to `git/index` | `(GP-2.4): Updated Index File` |

---

## Overall Success Criteria

Confirm each of the following across all four milestones before submitting:

- [ ] **`init()` creates all required files and directories** — `git/`, `git/objects/`, `git/index`, `git/HEAD`
- [ ] **`init()` is idempotent** — calling it twice does not error or overwrite existing files
- [ ] **SHA-1 hash is correct** — verified against the online tool for at least one test file
- [ ] **Blob files are created correctly** — `git/objects/<hash>` content matches the original file exactly
- [ ] **Index entries are correctly formatted** — `<hash> <relativePath>`, no trailing spaces, no blank final line
- [ ] **Modified file re-staging works** — staging a modified file replaces the old hash in the index
- [ ] **`README.md` updated** — documents all methods added in this part
- [ ] **Each milestone committed separately** — summary begins with the correct GP label

---

## Submission

Submit the URL of your **commit** for each milestone on the Hub.
