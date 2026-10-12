# Assignment — Initialization and Blobs

**Lesson:** [Initialization and Blobs](README.md)  
**Duration:** 3 class periods  
**Due:** End of this block

---

## Reference Docs

Read before starting any milestone:

- [BLOBs — how content-addressed storage works](docs/blobs.md)
- [Index File — what the index tracks and its format](docs/index-file.md)

---

## Milestones

| Milestone | What you'll build | Commit label |
|---|---|---|
| [Git-2.1 — Initialize a Repository](milestones/Git-2-1.md) | `git/`, `objects/`, `index`, `HEAD` | `(Git-2.1): Program Can Initialize Repository` |
| [Git-2.2 — Create a Hash Function](milestones/Git-2-2.md) | SHA-1 hash from file contents | `(Git-2.2): Created a Hash Function` |
| [Git-2.3 — Create BLOB Files](milestones/Git-2-3.md) | Store files in `objects/` by hash | `(Git-2.3): Create BLOB Files` |
| [Git-2.4 — Update the Index File](milestones/Git-2-4.md) | Write `hash path` entries to `git/index` | `(Git-2.4): Updated Index File` |

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
- [ ] **Each milestone committed separately** — summary begins with the correct Git label

---

## Submission

Submit the URL of your **commit** for each milestone on the Hub.
