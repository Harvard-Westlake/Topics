# Review — Forks and Collaboration, Day 1

*Originally covered in [Repositories and Commits](../../RepositoriesAndCommits/README.md), [Branching and Merging](../../BranchingAndMerging/README.md), and [Forks and Collaboration](../README.md)*

---

| Command | What it does |
|---|---|
| `git clone url` | Clone any repository (including your fork) |
| `git remote -v` | List all configured remotes and their URLs |
| `git remote add upstream url` | Add the original repo as a second remote |
| `git fetch upstream` | Download upstream changes without merging |
| `git merge upstream/main` | Merge upstream changes into current branch |
| `git push origin branch` | Push a branch to your fork on GitHub |

Fork = your personal copy of another repo on your account. `origin` = your fork. `upstream` = the original.

---

## Tasks

1. Fork any public repository on GitHub. Clone your fork to your local machine.
2. Run `git remote -v`. Identify which URL `origin` points to.
3. Add the original repository as `upstream`. Run `git remote -v` again — confirm both remotes appear.
4. Create a branch called `feature-fork-test`. Add a new file. Commit it.
5. Push the branch to your fork: `git push origin feature-fork-test`. Verify it appears in your fork on GitHub.
