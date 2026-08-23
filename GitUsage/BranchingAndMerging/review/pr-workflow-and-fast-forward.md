# Review — Pull Request Workflow and Fast-Forward Merges

*Originally covered in [Repositories and Commits](../../RepositoriesAndCommits/README.md) and [Branching and Merging](../README.md)*

---

Everything from Day 1, plus:

| Command | What it does |
|---|---|
| `git push origin branch-name` | Push a specific branch to GitHub |
| `git merge --ff-only branch` | Merge only if fast-forward is possible |
| `git branch -d name` | Delete a merged local branch safely |
| `git pull` | Pull latest changes from remote |
| `git merge --squash branch` | Collapse a branch's commits into one staged change |
| `git log --graph --oneline` | Draw the branch/merge structure of history |

Fast-forward merge: only possible when `main` has no new commits since you branched. PR workflow: push branch → open PR on GitHub → review (approve or request changes) → merge (squash or regular) → delete branch.

---

## Tasks

1. Create a branch called `feature-pr-practice`. Add two files with different content. Commit them.
2. Push the branch to GitHub: `git push origin feature-pr-practice`.
3. On GitHub, open a pull request from `feature-pr-practice` into `main`. Write a title and a full description paragraph.
4. Determine whether this will be a fast-forward merge: has `main` received any new commits since you created the branch? State your answer and why.
5. Before merging, review your own PR the way a maintainer would: open the Files changed tab and leave one comment on a specific line.
6. Merge the PR on GitHub, choosing **squash and merge** if your branch has messy intermediate commits and a regular merge otherwise — state which you picked and why. Pull the changes locally. Delete the branch both locally and on GitHub.
7. Create a `.gitignore` file on `main` that ignores `.DS_Store`, all `.log` files, and the `build/` directory. Commit and push it.
