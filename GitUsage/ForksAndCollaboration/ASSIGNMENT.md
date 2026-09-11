# Assignment — Forks and Collaboration

*Lesson: [Forks and Collaboration](README.md)*

**Due:** Next class

---

## Part 1 — Fork and Clone

1. Go to GitHub and find a public repository to contribute to. You can use a repository shared by your teacher, a classmate's project, or any public repo you find interesting.
2. Fork it — click **Fork** in the top-right corner of the repository page.
3. Clone **your fork** to your local machine:

```bash
git clone git@github.com:YOUR-USERNAME/repo-name.git
cd repo-name
```

4. Add the original repository as `upstream`:

```bash
git remote add upstream git@github.com:ORIGINAL-OWNER/repo-name.git
git remote -v
```

Confirm that both `origin` (your fork) and `upstream` (the original) are listed.

---

## Part 2 — Branch, Change, and Push

1. Create a feature branch:

```bash
git checkout -b feature-contribution
```

2. Make a meaningful change — add a file, improve a README, or add a comment. The change should be something that could genuinely improve the project.
3. Stage, commit, and push to your fork:

```bash
git add .
git commit -m "Describe the change you made"
git push origin feature-contribution
```

---

## Part 3 — Open a Pull Request

1. On GitHub, go to your fork and open a pull request targeting the **original repository's** `main` branch.
2. Write a title that describes the change in under ten words.
3. In the description, write a full paragraph covering:
   - What you changed
   - Why this change is useful
   - How the maintainer can verify it

> **Warning:**
> The description must be written in complete sentences. A vague or empty description will not receive full credit.

4. Click **Create pull request** and copy the URL.

---

## Part 4 — Sync Your Fork

1. Fetch and merge any changes from the original repository into your local `main`:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

2. Run `git log --oneline` on your local `main` and record the last three commit messages.

---

## Success Criteria

Before submitting, confirm each of the following:

- [ ] **Repository forked** — appears under your GitHub account with "forked from" shown
- [ ] **Fork cloned locally** — `origin` points to your fork, confirmed with `git remote -v`
- [ ] **Upstream remote added** — `upstream` points to the original repo
- [ ] **Feature branch created and pushed** — visible in your fork's branch list
- [ ] **Pull request opened** — targets the original repo's `main` with a full description
- [ ] **Fork synced** — ran the fetch/merge/push sequence from upstream

---

## Submission

Submit **one text response** and **one screenshot** on Canvas.

### Text response

```
Your fork URL:              https://github.com/
Original repository URL:    https://github.com/
Feature branch name:        
Pull request URL:           https://github.com/
PR description summary:     

git log --oneline (last 3):
  1.
  2.
  3.
```

### Screenshot

Take a screenshot of your **open pull request** on GitHub showing the title, your description paragraph, and the base and compare branch selectors confirming you are proposing changes across forks.
