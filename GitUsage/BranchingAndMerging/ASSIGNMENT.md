# Assignment — Branching and Merging

*Lesson: [Branching and Merging](README.md)*

**Due:** Next class

---

## Part 1 — Create a Feature Branch

Using the repository you set up in Day 1:

1. Confirm you are on `main` and your repo is up to date:

```bash
git checkout main
git pull
```

2. Create and switch to a new feature branch:

```bash
git checkout -b feature-notes
```

3. Confirm the switch:

```bash
git branch
# * feature-notes
#   main
```

4. Add a new file called `notes.md` to the branch. Write at least three bullet points covering something you have learned in this module so far.

5. Stage, commit, and push the branch:

```bash
git add notes.md
git commit -m "Add module notes on Git basics"
git push origin feature-notes
```

---

## Part 2 — Open and Merge a Pull Request

1. On GitHub, open a pull request from `feature-notes` into `main`.
2. Write a descriptive title and a one-paragraph description explaining what is in the PR and why.
3. Check whether the merge will be a fast-forward merge (has `main` changed since you branched?).
4. Merge the pull request on GitHub.
5. Delete the `feature-notes` branch on GitHub after merging.
6. Pull the merged changes back locally and delete the local branch:

```bash
git checkout main
git pull
git branch -d feature-notes
```

---

## Part 3 — Add a .gitignore

1. In your repository on `main`, create a `.gitignore` file:

```bash
touch .gitignore
```

2. Open it in VS Code and add rules to ignore: all `.class` files, the `build/` directory, `.DS_Store`, and `.vscode/`.
3. Commit and push the `.gitignore`:

```bash
git add .gitignore
git commit -m "Add .gitignore for Java and editor files"
git push
```

---

## Success Criteria

Before submitting, confirm each of the following:

- [ ] **Feature branch created** — named `feature-notes`, created from `main`
- [ ] **File added and committed on the branch** — `notes.md` with at least three bullet points
- [ ] **Branch pushed to GitHub** — visible in the repository's branch list
- [ ] **Pull request opened** — has a descriptive title and a written description
- [ ] **PR merged** — `notes.md` now appears on `main`
- [ ] **Branch deleted** — removed from GitHub and locally after merge
- [ ] **.gitignore committed** — contains rules for `.class`, `build/`, `.DS_Store`, `.vscode/`

---

## Submission

Submit **one text response** and **one screenshot** on Canvas.

### Text response

```
Repository URL:          https://github.com/
Branch name used:        
Pull request URL:        https://github.com/
Merge type:              fast-forward / merge commit
.gitignore rules added:  
```

### Screenshot

Take a screenshot of the **closed pull request** on GitHub showing the branch name, your PR description, and the merged status.
