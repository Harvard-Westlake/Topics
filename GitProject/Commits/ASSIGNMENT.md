# Assignment - Commits

**Lesson:** [Commits](README.md)  
**Duration:** 2 class periods  
**Due:** Before the start of the next lesson's class

---

## Receiving Your Partner's Code

Your teacher assigns you a classmate's repository. **Before writing any code:**

1. Fork and clone their repository.
2. Read their `README.md` to learn how to run their program.
3. Read their source files to learn how they structured their classes.
4. Run their tester and confirm it compiles and gives the expected output.

If their program does not compile or run correctly, write down the issue and the fix in their `README.md` before going on. You get credit for bugs you find and fix. Label those commits clearly.

Extend their code. Do not refactor it for taste: your job is to add commits on top of their design.

---

## Milestones

| Milestone | What it does | Commit label |
|---|---|---|
| [Git-4.1: Create a Commit (File and HEAD Link)](milestones/Git-4-1.md) | Save the staged snapshot as a commit and move HEAD to it | `(Git-4.1): Created a Commit` |
| [Git-4.2: Implement the GitWrapper Interface](milestones/Git-4-2.md) | Fill in the provided `GitWrapper` class: init, add, commit, and checkout | `(Git-4.2): Implemented the Interface` |
| [Git-4.3: Regenerate the Index](milestones/Git-4-3.md) | Rewrite the index from any commit's snapshot | `(Git-4.3): Regenerated the Index` |
| [Git-4.4: Check Out a Commit](milestones/Git-4-4.md) | Take the project back to any commit | `(Git-4.4): Checked Out a Commit` |

---

## Success Criteria

- [ ] **Commits are correct:** every commit file has the five lines, the first has no `parent:` line, and each later `parent:` is the commit before it.
- [ ] **HEAD follows the newest commit:** after each commit or checkout, `git/HEAD` holds that commit's hash.
- [ ] **`GitWrapper` runs every operation:** `init`, `add`, `commit`, and `checkout` work through the provided class with unchanged signatures, and `README.md` shows how.
- [ ] **The index regenerates:** emptying `git/index` and regenerating it from a commit gives back the same lines.
- [ ] **Checkout restores a commit:** tracked files match that commit, untracked files are untouched.
- [ ] **`README.md` updated:** bugs found and fixed, and anything missing, written down.
- [ ] **Each milestone committed separately:** each summary begins with the correct Git label.

---

## Submission

Submit the URL of your **GitHub pull request** on Canvas.
