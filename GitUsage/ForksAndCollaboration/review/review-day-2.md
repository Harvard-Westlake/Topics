# Review — Forks and Collaboration, Day 2

*Originally covered in [Staging and Committing](../RepositoriesAndCommits/README.md), [Branching and Merging](../BranchingAndMerging/README.md), and [Forks and Collaboration](../README.md)*

---

Full collaboration cycle: Fork → Clone → Branch → Commit → Push to fork → PR to original → Sync fork

| Command | What it does |
|---|---|
| `git fetch upstream` | Download upstream changes without merging |
| `git merge upstream/main` | Integrate upstream changes into local main |
| `git push origin main` | Push synced main to your fork |
| `git log --oneline` | View commit history one line per commit |
| `git branch -d name` | Delete a local branch after it is merged |

---

## Tasks

1. In your forked repo, fetch and merge any upstream changes into your local `main`. Push the updated `main` to your fork.
2. Run `git log --oneline`. Identify which commits came from upstream and which you added.
3. Create a branch called `contribution-final`. Add a meaningful change — a new file, an improvement to an existing file, or a README update. Commit it with a specific message.
4. Push the branch to your fork and open a pull request to the **original** repository. Write a title and a full description paragraph as if a real maintainer will read it.
5. After your PR is open, delete the local branch and then delete it from your fork on GitHub.
