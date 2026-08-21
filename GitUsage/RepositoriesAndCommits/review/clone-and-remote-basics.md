# Review — Cloning and Remotes

*Originally covered in [Repositories and Commits](../README.md)*

---

| Command | What it does |
|---|---|
| `git clone url` | Download a full copy of a remote repository |
| `git remote -v` | List configured remotes and their URLs |
| `git add .` | Stage all changed files |
| `git commit -m "msg"` | Snapshot staged changes |
| `git push` | Upload commits to remote |
| `git pull` | Download remote changes locally |

The daily cycle: `pull` → edit → `add` → `commit` → `push`

---

## Tasks

1. Clone any public GitHub repository to your machine. Navigate into it and run `git remote -v`.
2. Create two new files with different names and extensions. Stage only one of them. Run `git status` — confirm one is staged and one is not.
3. Stage the second file. Write a single commit message that accurately describes both files being added.
4. Push to GitHub. Verify both files appear in the commit on the repository page.
5. On GitHub, use the pencil edit button to add a line to one file directly in the browser. Then pull the change locally and confirm it appears in your local copy.
