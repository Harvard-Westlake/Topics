# Assignment - Branches

*Lesson: [Branches](README.md)*

**Due:** Before the start of next class

---

## Receiving the Code

Your teacher assigns you a repository with a finished Part 4 (commits and checkout). **Before writing any code:**

1. Fork and clone the repository.
2. Read its `README.md` to learn how to run each operation in its interface.
3. Run it and confirm that initialize, stage, commit, and check out all work.

If something does not compile or run correctly, write down the issue and the fix in the `README.md` before going on. You get credit for bugs you find and fix. Label those commits clearly.

Extend the code. Do not refactor it for taste: your job is to add branches on top of its design.

---

## Milestones

| Milestone | What it does | Commit label |
|---|---|---|
| [Git-5.1: Get the Code Running](milestones/Git-5-1.md) | Prove every Part 4 operation works before you change anything | `(Git-5.1): Code Running` |
| [Git-5.2: Add Branching](milestones/Git-5-2.md) | Create branches, commit on them, and check them out | `(Git-5.2): Added Branching` |

---

## Success Criteria

- [ ] **The code runs:** every Part 4 operation works, and any bugs are written down and fixed.
- [ ] **Branches are files:** each branch is `git/refs/heads/<name>` holding one commit hash.
- [ ] **Commits move only the current branch:** HEAD keeps naming the branch, and every other branch stays where it was.
- [ ] **Checking out a branch works:** the files, index, and HEAD all match that branch, and untracked files are untouched.
- [ ] **The interface has both new operations:** Create a branch and Check out a branch, and `README.md` shows how to run them.
- [ ] **Each milestone committed separately:** each summary begins with the correct Git label.

---

## Submission

Submit the URL of your **GitHub pull request** on Canvas.
