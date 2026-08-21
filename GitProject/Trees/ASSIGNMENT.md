# Assignment — Trees

*Lesson: [Trees](README.md)*

**Duration:** 3 class periods  
**Due:** End of this block

---

## Reference Docs

- [Trees — file format, bottom-up construction, root tree](../Docs/trees.md)

---

## Milestones

| Milestone | What you'll build | Commit label |
|---|---|---|
| [GP-3.1 — Update the Index Format](milestones/gp-3-1.md) | Relative paths, edge cases, modified files | `(GP-3.1): Updated Index to Store Relative Paths` |
| [GP-3.2 — Create a Basic Tree](milestones/gp-3-2.md) | Recursive tree files from a directory path | `(GP-3.2): Created Basic Tree from Directory` |
| [GP-3.3 — Create a Tree from the Index](milestones/gp-3-3.md) | Working list algorithm, root tree hash | `(GP-3.3): Created Tree from Index` |

---

## Overall Success Criteria

- [ ] **Index stores relative paths** — format is `<hash> <path/to/file>`, not `<hash> <filename>`
- [ ] **Duplicate detection works** — staging the same unchanged file twice does not add a second entry
- [ ] **Modified file updates correctly** — staging a modified file replaces the old hash in the index
- [ ] **`createTree(dirPath)` generates correct tree files** — recursively handles subdirectories; all blobs written to `objects/`
- [ ] **`createTreeFromIndex()` produces a correct root tree** — only staged files appear; root tree hash is accessible for Part 4
- [ ] **Tree hashes are deterministic** — same index produces the same tree hash on every run
- [ ] **Each milestone committed separately** — summary begins with the correct GP label

---

## Submission

Submit the URL of your **commit(s)** for each milestone on the Hub.
