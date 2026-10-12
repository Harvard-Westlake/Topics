# Assignment - Commits

*Lesson: [Commits](README.md)*

**Duration:** 2 class periods  
**Due:** Before the start of the next lesson's class

---

## Reference Docs

- [Commits reference: file format, HEAD chain, step order](docs/commits.md)

---

## Receiving Your Partner's Code

Your teacher assigns you a classmate's repository. **Before writing any code:**

1. Fork and clone their repository.
2. Read their `README.md` to learn how to run their program.
3. Read their source files to learn how they structured their classes.
4. Run their tester and confirm it compiles and gives the expected output.

If their program does not compile or run correctly, write down the issue and the fix in their `README.md` before going on. You get credit for bugs you find and fix. Label those commits clearly.

### Rules for Their Code

- **Extend it. Do not refactor it for taste.** Your job is to add commits on top of their design.
- **`GitWrapper` methods are static, and their signatures never change.** Every project is tested through the same methods, no matter how the inside was designed.

---

## Milestones

| Milestone | What you'll build | Commit label |
|---|---|---|
| [Git-4.1: Link the Commit File](milestones/Git-4-1.md) | Commit files and the HEAD chain | `(Git-4.1): Implemented Commit with HEAD Linkage` |
| [Git-4.2: Implement GitWrapper](milestones/Git-4-2.md) | A standard static interface | `(Git-4.2): Implemented GitWrapper` |
| [Git-4.3: Regenerate the Index](milestones/Git-4-3.md) | Rebuild `git/index` from a commit's tree | `(Git-4.3): Regenerated Index from Commit Tree` |
| [Git-4.4: Check Out a Commit](milestones/Git-4-4.md) | Take the project back to any commit | `(Git-4.4): Implemented Checkout` |

---

## Success Criteria

- [ ] **`commit()` writes the correct format:** every required field present, no parent line on the first commit.
- [ ] **Commit stored in `objects/`:** the file exists at `git/objects/<commitSHA>`.
- [ ] **HEAD updated correctly:** `git/HEAD` holds the new commit's hash after each commit.
- [ ] **Parent chain correct:** the second commit's `parent:` matches the first commit's hash.
- [ ] **`commit()` returns the hash:** confirmed in the `GitTester` output.
- [ ] **`GitWrapper` uses static methods:** signatures unchanged from the provided template.
- [ ] **Index rebuilds from a commit:** emptying `git/index` and rebuilding it gives back the same lines.
- [ ] **Checkout restores a commit:** tracked files match that commit, untracked files are untouched, and the index and HEAD point at it.
- [ ] **`README.md` updated:** bug log and missing features written down.
- [ ] **Each milestone committed separately:** each summary begins with the correct Git label.

---

## Submission

Submit the URL of your **GitHub pull request** on Canvas.
