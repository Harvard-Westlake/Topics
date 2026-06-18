# Assignment — Commits

**Duration:** 4 class periods  
**Due:** End of this block

---

## Reference Docs

- [Commits — file format, HEAD chain, step ordering](../Docs/commits.md)

---

## Receiving Your Partner's Code

Your instructor will assign you a classmate's repository. **Before writing any code:**

1. Fork and clone their repository
2. Read their `README.md` — understand how to run their program
3. Read their source files — understand how they structured their classes
4. Run their tester — confirm it compiles and produces expected output

If their program does not compile or run correctly, document the issue and fix it before proceeding. You will receive credit for identified and repaired bugs. Label those commits clearly.

---

## Milestones

| Milestone | What you'll build | Commit label |
|---|---|---|
| [GP-4.1 — Identify the Root Tree](milestones/gp-4-1.md) | Trace and verify partner's object graph | `(GP-4.1): Verified Root Tree Structure` |
| [GP-4.2 — Link the Commit File](milestones/gp-4-2.md) | Commit files and HEAD chain | `(GP-4.2): Implemented Commit with HEAD Linkage` |
| [GP-4.3 — Implement GitWrapper](milestones/gp-4-3.md) | Standardized static interface | `(GP-4.3): Implemented GitWrapper` |

---

## Overall Success Criteria

- [ ] **GP-4.1 complete** — root tree verified manually, any bugs documented and fixed
- [ ] **`commit()` writes correct file format** — all required fields present, parent line omitted on first commit
- [ ] **Commit stored in `objects/`** — file exists at `git/objects/<commitSHA>`
- [ ] **HEAD updated correctly** — `git/HEAD` contains the new commit's hash after each commit
- [ ] **Parent chain correct** — second commit's `parent:` field matches first commit's hash
- [ ] **`commit()` returns the hash** — confirmed via `GitTester` output
- [ ] **`GitWrapper` uses static methods** — method signatures unchanged from the provided template
- [ ] **`README.md` updated** — bug log and missing functionality documented
- [ ] **Each milestone committed separately** — summary begins with the correct GP label

---

## Submission

Submit the URL of your **GitHub pull request** on the Hub.
