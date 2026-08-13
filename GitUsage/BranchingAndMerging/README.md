<div align="center">

# Branching and Merging
*<font color="#8b949e">Parallel development, combining work, and collaborating through pull requests</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[What is a Branch?](#what-is-a-branch)**  
How branches let multiple lines of development exist at the same time.

**[Creating and Switching Branches](#creating-and-switching-branches)**  
`git branch`, `git checkout`, and the shorthand `git checkout -b`.

**[Listing and Deleting Branches](#listing-and-deleting-branches)**  
Seeing what branches exist and cleaning up after merging.

**[Merging Branches](#merging-branches)**  
Combining a finished branch back into main.

**[Fast-Forward Merges](#fast-forward-merges)**  
The simplest merge type and why it produces a clean history.

**[Pull Requests](#pull-requests)**  
Proposing and reviewing changes before they reach the main branch.

**[The .gitignore File](#the-gitignore-file)**  
Telling Git which files to never track.

---

## <font color="#388bfd">What is a Branch?</font>

A **branch** is an independent line of development. It starts as a copy of the branch you create it from and diverges from there — any commits you make on the new branch do not affect the original.

Branches let you:
- Develop a new feature without breaking the working version
- Fix a bug in isolation and test it before it reaches main
- Let multiple people work on different things at the same time

The **main** (or **master**) branch is the stable, production-ready version of the project. Feature work happens on separate branches and merges back into main only when it is ready.

---

## <font color="#388bfd">Creating and Switching Branches</font>

```bash
git branch feature-name         # create a new branch (stay on current)
git checkout feature-name       # switch to an existing branch
git checkout -b feature-name    # create AND switch in one step (most common)
```

After `git checkout -b`, all new commits go to the feature branch. The `main` branch is unchanged until you merge.

**In GitKraken:** click the **Branch** button in the toolbar → enter a name → press Enter. GitKraken switches you to the new branch automatically.

> **Note:**
> A branch is created from whatever branch you are currently on. Always check which branch you are on before branching — run `git branch` to see the current branch marked with `*`.

---

## <font color="#388bfd">Listing and Deleting Branches</font>

```bash
git branch                      # list all local branches (* = current)
git branch -a                   # list local and remote branches
git branch -d branch-name       # delete a branch (safe — only if merged)
git branch -D branch-name       # force delete (even if not merged)
```

After a feature branch is merged, delete it to keep the branch list clean. The commits are preserved in main — deleting the branch just removes the label.

---

## <font color="#388bfd">Merging Branches</font>

Merging brings the commits from one branch into another. To merge a feature branch into main:

```bash
git checkout main               # switch to the destination branch
git merge feature-name          # bring in commits from feature-name
```

After a successful merge, all commits from `feature-name` are now part of `main`.

**In GitKraken:** right-click the branch you want to merge from → select **Merge [branch] into [current branch]**.

> **Tip:**
> Always switch to the **destination** branch before running `git merge`. You are saying "merge this other branch into wherever I am now."

---

## <font color="#388bfd">Fast-Forward Merges</font>

A **fast-forward merge** occurs when `main` has not received any new commits since you branched off it. In this case, Git does not need to create a new merge commit — it simply moves the `main` pointer forward to the tip of the feature branch.

```
Before merge:
main     A---B
              \
feature        C---D---E

After fast-forward merge:
main     A---B---C---D---E
```

```bash
# Force fast-forward only (will fail if not possible)
git merge --ff-only feature-name
```

Fast-forward merges produce a perfectly linear history. They are only possible when no one else has pushed to main while you were working. In active team projects, they are less common — other contributors push to main constantly. When a fast-forward is not possible, Git creates a **merge commit** that ties the two histories together.

---

## <font color="#388bfd">Pull Requests</font>

A **pull request** (PR) is a proposal to merge one branch into another. Instead of merging directly, you push your branch to GitHub and open a PR so teammates (or maintainers) can review, comment, and approve the changes before they reach main.

**The pull request workflow:**

1. Create a feature branch and commit your changes
2. Push the branch to GitHub:
   ```bash
   git push origin branch-name
   ```
3. On GitHub, click **Compare & pull request** (or go to the Pull requests tab → New pull request)
4. Set the **base** branch (where changes go — usually `main`) and the **compare** branch (your feature branch)
5. Write a clear title and description explaining what the PR does and why
6. Click **Create pull request**
7. After review and approval, click **Merge pull request**

**In GitKraken:** right-click your feature branch in the left panel → **Start a pull request** → fill in the form.

> **Tip:**
> A good PR description answers: what changed, why it changed, and how to test it. Even if no one else reviews your PR, writing this forces you to think clearly about what you shipped.

---

## <font color="#388bfd">The .gitignore File</font>

A `.gitignore` file lists paths and patterns that Git should never track. Files matching these patterns will not appear in `git status` and cannot be accidentally staged or committed.

Create a `.gitignore` in the root of your repository:

```bash
touch .gitignore
```

Then open it and add patterns — one per line:

```
# Compiled Java files
*.class

# Build output
build/
target/

# macOS system file
.DS_Store

# VS Code settings
.vscode/

# Environment variables (never commit secrets)
.env
secrets.json

# Log files
*.log
logs/
```

| Pattern | What it ignores |
|---|---|
| `*.class` | All files ending in `.class` |
| `build/` | The entire `build` directory |
| `.DS_Store` | One specific file by exact name |
| `*.log` | All `.log` files anywhere in the repo |

> **Warning:**
> Adding a file to `.gitignore` only works if Git is not already tracking it. If the file was committed before, you must first remove it from tracking with `git rm --cached filename`.

Commit and push your `.gitignore` like any other file. It applies to everyone who clones the repository.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you create a new branch with a descriptive name and switch to it?
- [ ] Can you list all branches in a repository and identify which one is current?
- [ ] Can you merge a feature branch into main and confirm the commits appear?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you push a branch to GitHub and open a pull request with a clear title and description?
- [ ] Can you explain when a fast-forward merge occurs and when it cannot?
- [ ] Can you create a `.gitignore` that correctly excludes compiled Java files and macOS system files?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain the difference between a fast-forward merge and a merge commit, and when each is appropriate?
- [ ] Can you describe the full pull request workflow from branch creation to merged PR?
- [ ] Can you explain why `.gitignore` must be committed and what happens to files Git already tracks?

---

[Assignment](ASSIGNMENT.md)

← [Repositories and Commits](../RepositoriesAndCommits/) — Next: [Forks and Collaboration](../ForksAndCollaboration/)
