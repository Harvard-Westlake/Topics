# Review — Branching and Merging, Day 2

*Originally covered in [Repositories and Commits](../../RepositoriesAndCommits/README.md) and [Branching and Merging](../README.md)*

---

Everything from Day 1, plus:

| Command | What it does |
|---|---|
| `git push origin branch-name` | Push a specific branch to GitHub |
| `git merge --ff-only branch` | Merge only if fast-forward is possible |
| `git branch -d name` | Delete a merged local branch safely |
| `git pull` | Pull latest changes from remote |

Fast-forward merge: only possible when `main` has no new commits since you branched. PR workflow: push branch → open PR on GitHub → review → merge → delete branch.

---

## Tasks

1. Create a branch called `feature-pr-practice`. Add two files with different content. Commit them.
2. Push the branch to GitHub: `git push origin feature-pr-practice`.
3. On GitHub, open a pull request from `feature-pr-practice` into `main`. Write a title and a full description paragraph.
4. Determine whether this will be a fast-forward merge: has `main` received any new commits since you created the branch? State your answer and why.
5. Merge the PR on GitHub. Pull the changes locally. Delete the branch both locally and on GitHub.
6. Create a `.gitignore` file on `main` that ignores `.DS_Store`, all `.log` files, and the `build/` directory. Commit and push it.
