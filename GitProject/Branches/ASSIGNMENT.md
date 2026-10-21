# Assignment - Branches

**Lesson:** [Branches](README.md)  
**Due:** Before the start of next class

---

## Bring Your Code Home

Since Part 2, every part of this project was built on a fork of a classmate's repository, so the newest version of your code, with Part 4 finished, lives in a fork of a fork of your original. None of it was ever sent back to you. **Before writing any code**, get it into your own `main`:

1. Find the fork of a fork that holds your Part 4, and the branch it was done on. On GitHub, your repository's **Insights → Forks** lists every fork, and each fork's page says what it was forked from; follow that chain to the newest one. Ask the classmates who had your code if you are not sure.
2. Open a pull request across forks from that branch into your repository's `main`, then merge it. The [Forks and Collaboration](../../GitUsage/ForksAndCollaboration/README.md#contributing-back-with-pull-requests) lesson shows the compare-across-forks picker on GitHub and in GitKraken.
3. In your terminal, pull `main` and run it. [Git-5.1](milestones/Git-5-1.md) proves every Part 4 operation works.
4. If something broke along the way, write the issue and the fix in `README.md`. You get credit for bugs you find and fix. Label those commits clearly.

Everything below is built in your own repository and ends up merged and pushed on `main`. Do not refactor your classmates' work for taste: your job is to add branches on top of it.

---

## Milestones

| Milestone | What it does | Commit label |
|---|---|---|
| [Git-5.1: Bring Your Code Home](milestones/Git-5-1.md) | Merge the fork of a fork into your `main`, then prove every Part 4 operation works | `(Git-5.1): Code Running` |
| [Git-5.2: Add Branching](milestones/Git-5-2.md) | Create branches, commit on them, and check them out | `(Git-5.2): Added Branching` |

---

## Success Criteria

- [ ] **Your `main` holds everything:** the fork of a fork that holds your Part 4 is merged into your `main` through a pull request across forks, and your Part 5 work is merged and pushed to `main` too.
- [ ] **The code runs:** every Part 4 operation works, and any bugs are written down and fixed.
- [ ] **Branches are files:** each branch is `git/refs/heads/<name>` holding one commit hash.
- [ ] **Commits move only the current branch:** HEAD keeps naming the branch, and every other branch stays where it was.
- [ ] **Checking out a branch works:** the files, index, and HEAD all match that branch, and untracked files are untouched.
- [ ] **The interface has both new operations:** Create a branch and Check out a branch, and `README.md` shows how to run them.
- [ ] **Each milestone committed separately:** each summary begins with the correct Git label.

---

## Stretch Goal

Worth the last 5% of the grade. Checking out a name that is not a branch and not a commit **creates the branch** instead of being an error:

- [ ] **A new branch from a name:** `git/refs/heads/<name>` is created holding the commit you are on, `git/HEAD` holds `ref: refs/heads/<name>`, and no file in the working folder changes. The next commit moves the new branch and leaves `main` where it was.

---

## Submission

Submit **text** on Canvas. Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Merged into main (across forks):   https://github.com/YOUR-USERNAME/YOUR-REPO/pull/N
Part 5 pull request:               https://github.com/YOUR-USERNAME/YOUR-REPO/pull/N
```
