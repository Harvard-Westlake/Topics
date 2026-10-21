# Review - Pull Requests Across Forks

*Originally covered in [Forks and Collaboration](../README.md)*

---

| Where | What |
|---|---|
| Your repository → **Insights → Forks** | Every fork of your code; a fork's own page says `forked from OWNER/REPO` |
| `gh repo view THEM/REPO --json parent -q .parent.nameWithOwner` | What a fork was forked from, from the terminal |
| Your repository → **Pull requests → New pull request → compare across forks** | base: your repository, `main`; head: their fork, their branch |
| `gh pr create --repo YOU/REPO --base main --head THEM:their-branch --title "Bring in THEM's work"` | The same pull request from the terminal |
| GitKraken: left panel **Pull Requests → +**, or drag their branch onto your `main` | **From:** their fork and branch; **To:** your repository, `main` |
| `gh pr list --repo YOU/REPO` | Open pull requests and their numbers |
| **Files changed** tab | Every line the merge would add or remove |
| `gh pr merge NUMBER --repo YOU/REPO --merge` | Merge it (same as the green **Merge pull request** button) |
| `git pull` on `main` | Bring the merged work down into your clone |

A pull request across forks moves work from a fork (the head) into the repository it came from (the base). Whoever can push to the base can open it and merge it, even when the fork is a fork of a fork.

---

## Tasks

1. Open your repository's fork list and write down every fork and what each was forked from. Pick the one with the newest work on your code and note the branch it was done on.
2. Open a pull request across forks from that branch into your `main`, titled with whose work it brings in. Before you create it, confirm the base is your repository and the head is their fork.
3. In **Files changed**, find one file that changed and say in one sentence what the change does. If GitHub says it cannot merge automatically, name the file with the conflict.
4. Merge it. In your terminal, pull `main` and confirm the merge commit is at the top of `git log --oneline -3`.
5. If a second classmate also worked on your code, bring their branch in the same way. Where both changed the same lines, keep the version that compiles and say so in the merge commit message.
