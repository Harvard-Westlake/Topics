# Assignment — Staging and Committing

*Lesson: [Staging and Committing](README.md)*

**Due:** Next class

---

## Part 1 — Create and Publish a Repository

1. Open your terminal and navigate to where you keep your projects. Create a folder with a meaningful name related to this course and turn it into a repository:

```bash
mkdir your-repo-name && cd your-repo-name
git init
```

2. Give it a first file and a first commit:

```bash
echo "# Your Repo Name" > README.md
git add README.md
git commit -m "Initial commit"
```

3. Publish it to GitHub as a **public** repository — one command creates it under your account, connects it as `origin`, and pushes:

```bash
gh repo create your-repo-name --source=. --public --push
```

4. Verify the remote is configured, then open the repository page:

```bash
git remote -v
gh repo view --web
```

---

## Part 2 — Stage, Commit, and Push

1. Create a new file called `journal.md`:

```bash
touch journal.md
```

2. Open it in VS Code and write at least two sentences about what you learned today.
3. Check the current state of the repo:

```bash
git status
```

4. Stage the file and check again:

```bash
git add journal.md
git status
```

5. Commit with a descriptive message:

```bash
git commit -m "Add journal entry for Day 1 Git lesson"
```

6. Push to GitHub:

```bash
git push
```

7. Visit your repository page on GitHub. Confirm the file and commit message appear.

---

## Success Criteria

Before submitting, confirm each of the following:

- [ ] **Repository created locally and published** — you ran `git init`, made a first commit, and published with `gh repo create --source=. --public --push`
- [ ] **Remote configured** — `git remote -v` lists `origin` and the repository is publicly visible on GitHub
- [ ] **File created and edited** — `journal.md` exists with at least two sentences
- [ ] **Staged correctly** — you ran `git add` and confirmed staged status with `git status`
- [ ] **Committed with a meaningful message** — the message describes what was added, not just "update"
- [ ] **Pushed to GitHub** — the commit and file are visible on the GitHub repository page

---

## Submission

Submit **one text response** and **one screenshot** on Canvas.

### Text response

Copy the stencil, fill in each line, and paste it into the Canvas text box:

```
Repository URL:          https://github.com/
File created:            
git add command used:    
Commit message:          
GitHub commit URL:       https://github.com/
```

> **Note:**
> To get the GitHub commit URL: go to your repository on GitHub → click **commits** (or the commit message link) → copy the URL of the individual commit page.

### Screenshot

Take a screenshot of your GitHub repository page showing `journal.md` in the file list and your commit message visible in the commit history.
