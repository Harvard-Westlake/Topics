# Assignment — Staging and Committing

*Lesson: [Staging and Committing](README.md)*

**Due:** Next class

---

## Part 1 — Create and Clone a Repository

1. Go to GitHub and create a new **public** repository. Give it a meaningful name related to this course.
2. Copy the repository's SSH address from the **Code** button — select the **SSH** tab; the address looks like `git@github.com:your-username/your-repo-name.git`.
3. Open your terminal, navigate to where you keep your projects, and clone it:

```bash
git clone git@github.com:your-username/your-repo-name.git
cd your-repo-name
```

4. Verify the remote is configured:

```bash
git remote -v
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

- [ ] **Repository created on GitHub** — it is publicly visible
- [ ] **Repository cloned locally** — you ran `git clone` and confirmed with `git remote -v`
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
