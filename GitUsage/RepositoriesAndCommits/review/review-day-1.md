# Review — Staging and Committing, Day 1

*Originally covered in [Staging and Committing](../README.md)*

---

| Command | What it does |
|---|---|
| `git status` | Show changed, staged, and untracked files |
| `git add filename` | Stage one specific file |
| `git add .` | Stage all changed files in current directory |
| `git commit -m "msg"` | Save a snapshot of staged files with a message |
| `git push` | Upload local commits to GitHub |
| `git pull` | Download latest commits from GitHub |

---

## Tasks

1. Navigate to a git repository you have already cloned. Run `git status` and read the output.
2. Create a new file called `test.md`. Run `git status` again — observe how the output changed.
3. Stage `test.md`. Run `git status` to confirm it moved from untracked to staged.
4. Commit with a specific message. Run `git status` one more time and note the result.
5. Push to GitHub. Open the repository in your browser and locate the commit in the history.
