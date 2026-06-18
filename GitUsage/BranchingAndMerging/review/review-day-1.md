# Review — Branching and Merging, Day 1

*Originally covered in [Repositories and Commits](../RepositoriesAndCommits/README.md) and [Branching and Merging](../README.md)*

---

| Command | What it does |
|---|---|
| `git branch` | List all local branches (`*` = current) |
| `git branch name` | Create a new branch without switching |
| `git checkout name` | Switch to an existing branch |
| `git checkout -b name` | Create and switch in one step |
| `git merge branch` | Merge a branch into the current branch |
| `git add .` | Stage all changed files |
| `git commit -m "msg"` | Commit staged changes |
| `git push` | Push current branch to remote |

Branches isolate work — commits on a feature branch do not affect `main` until you merge.

---

## Tasks

1. In a repository you have access to, run `git branch`. Note which branch is current.
2. Create a new branch called `feature-review`. Switch to it. Confirm with `git branch`.
3. Create a new file on this branch. Stage it and commit it with a clear message.
4. Switch back to `main`. Run `ls` or check the directory — confirm the new file is NOT there.
5. Merge `feature-review` into `main`. Confirm the file now appears.
6. Delete `feature-review` locally. Confirm the branch list no longer shows it.
