<div align="center">

# Branching and Merging
*<font color="#8b949e">Parallel development, combining work, and collaborating through pull requests</font>*

<font color="#a371f7">Learning</font>

</div>

---

Yesterday you learned to save your work as commits on a single timeline. But real projects don't have one timeline — they have many running in parallel: a feature in progress here, a bug fix there, an experiment that might be deleted tomorrow. Today you learn how Git runs parallel universes of your code (**branches**), how those universes get recombined (**merging**), and how teams control what gets recombined (**pull requests and review**).

## <font color="#388bfd">Table of Contents</font>

1. [Understand what a branch is and why parallel development needs them](#what-is-a-branch)
2. [Create, switch, list, and delete branches from the terminal and GitKraken](#creating-and-switching-branches)
3. [Merge a finished branch back into main](#merging-branches)
4. [See when a fast-forward merge happens — and when a team makes it impossible](#fast-forward-merges)
5. [Propose changes with a pull request instead of merging directly](#pull-requests)
6. [Review someone else's pull request like a maintainer](#reviewing-a-pull-request)
7. [Choose between squash-and-merge and a regular merge](#squash-and-merge-vs-regular-merge)
8. [Keep junk out of your repository with .gitignore](#the-gitignore-file)
9. [Check your understanding and try the stretch goals](#check-for-understanding)

---

## <font color="#388bfd">What is a Branch?</font>

A **branch** is an independent line of development. It starts as a copy of the branch you create it from and diverges from there — any commits you make on the new branch do not affect the original.

Branches let you:
- Develop a new feature without breaking the working version
- Fix a bug in isolation and test it before it reaches main
- Let multiple people work on different things at the same time

The **main** (or **master**) branch is the stable, production-ready version of the project. Feature work happens on separate branches and merges back into main only when it is ready.

> **Note:**
> A branch is not a copy of your files — it's a movable label pointing at a commit. That's why creating one is instant even in a huge repository, and why you can have dozens of branches without using more disk space.

---

## <font color="#388bfd">Creating and Switching Branches</font>

```bash
git branch feature-name         # create a new branch (stay on current)
git checkout feature-name       # switch to an existing branch
git checkout -b feature-name    # create AND switch in one step (most common)
```

After `git checkout -b`, all new commits go to the feature branch. The `main` branch is unchanged until you merge.

**In GitKraken:** click the **Branch** button in the toolbar → enter a name → press Enter. GitKraken switches you to the new branch automatically.

Listing and cleaning up:

```bash
git branch                      # list all local branches (* = current)
git branch -a                   # list local and remote branches
git branch -d branch-name       # delete a branch (safe — only if merged)
git branch -D branch-name       # force delete (even if not merged)
```

After a feature branch is merged, delete it to keep the branch list clean. The commits are preserved in main — deleting the branch just removes the label.

> **Note:**
> A branch is created from whatever branch you are currently on. Always check which branch you are on before branching — run `git branch` to see the current branch marked with `*`.

👉 <details>
<summary><h3>Activity: The Parallel Universe — click to expand</h3></summary>

*Concept: A branch is a genuinely separate line of development — files committed on it don't exist on main until you merge.*

![Diagram of one folder with two universes: the main timeline holds commits A and B, while the experiment branch forks off with commit C containing universe-b.txt. Two terminal panels show that ls on main lists only clue.txt, while ls on experiment also lists universe-b.txt — the file waits inside .git/ while you stand on main.](assets/parallel-universe.svg)

## Task

1. Open a terminal in the `git-detective` repository you created in the Day 1 activities (or any local practice repo). Make sure it has at least one commit — if not, create a file and commit it.
2. In your terminal, create and switch to a branch in one step:
   ```bash
   git checkout -b experiment
   ```
3. Still in your terminal, create a file that only exists in this universe, then commit it:
   ```bash
   echo "only visible on the experiment branch" > universe-b.txt
   git add universe-b.txt
   git commit -m "Add universe-b marker file"
   ```
4. Now jump back to the original universe and look around:
   ```bash
   git checkout main
   ls
   ```
   `universe-b.txt` is **gone** — not deleted, just not part of this branch's reality.
5. Switch back to `experiment` and confirm the file reappears:
   ```bash
   git checkout experiment
   ls
   ```
6. Write one sentence: where does `universe-b.txt` live while you're standing on `main`? (Hint: think back to The Hidden Detective — everything Git knows lives somewhere in `.git/`.)

*(Standalone file: [activities/01-the-parallel-universe.md](activities/01-the-parallel-universe.md))*

</details>

---

## <font color="#388bfd">Merging Branches</font>

Merging brings the commits from one branch into another. To merge a feature branch into main:

```bash
git checkout main               # switch to the destination branch
git merge feature-name          # bring in commits from feature-name
```

After a successful merge, all commits from `feature-name` are now part of `main`.

**In GitKraken:** double-click `main` to switch to it, then right-click the branch you want to merge from → select **Merge [branch] into main**.

> **Tip:**
> Always switch to the **destination** branch before running `git merge`. You are saying "merge this other branch into wherever I am now."

---

## <font color="#388bfd">Fast-Forward Merges</font>

A **fast-forward merge** occurs when `main` has not received any new commits since you branched off it. Git doesn't need to combine anything — every commit on your branch is *directly ahead* of main, so Git simply slides the `main` pointer forward to the tip of the feature branch:

```
Before merge:
main     A---B
              \
feature        C---D---E

After fast-forward merge:
main     A---B---C---D---E
```

A fast-forward happens exactly when all four of these are true: you branched from main, you committed on the branch, **nobody committed to main in the meantime**, and then you merged back. It's the simplest merge — no new commit is created, no conflict is possible, and the history stays perfectly linear.

**Why teams rarely see them.** On a solo project, main holds still while you work. On a team, it doesn't — classmates merge their own branches into main while yours is in progress:

```
Before merge:
main     A---B---F---G      ← F and G landed while you worked
              \
feature        C---D---E
```

Now the two branches have genuinely diverged, and a fast-forward is impossible. Git instead creates a **merge commit** — a special commit with two parents that ties both histories together. You can force Git to refuse anything but a fast-forward:

```bash
git merge --ff-only feature-name    # merges only if fast-forward is possible, else stops
```

> **Note:**
> Don't confuse the mechanism with the workflow. A *fast-forward merge* is how Git technically combines branches; a *pull request* (next section) is a team process for deciding **whether** to combine them. When a PR is approved, the merge underneath might be a fast-forward, a merge commit, or a squash — that's a settings choice, not a different kind of PR.

👉 <details>
<summary><h3>Activity: Break the Fast-Forward — click to expand</h3></summary>

*Concept: A fast-forward is only possible while main holds still — one commit on main while you work forces a real merge commit.*

![Diagram of diverged history: main holds commits A and B, then a teammate's commit F lands on main while your commit C sits on the side-quest branch. git merge --ff-only refuses because the histories diverged; a plain git merge instead creates merge commit M with two parents, F and C.](assets/break-the-fast-forward.svg)

## Task

1. In your terminal, inside your practice repository, create a branch but **stay on main**:
   ```bash
   git checkout main
   git branch side-quest
   ```
2. Commit something on `main` first — you are playing the role of "a teammate who didn't wait":
   ```bash
   echo "teammate's change" > teamwork.txt
   git add teamwork.txt
   git commit -m "Teammate commits to main"
   ```
3. Now switch to the branch and commit there too:
   ```bash
   git checkout side-quest
   echo "your feature" > feature.txt
   git add feature.txt
   git commit -m "Add feature on side-quest"
   ```
4. Try to merge with fast-forward only — and watch Git refuse:
   ```bash
   git checkout main
   git merge --ff-only side-quest
   ```
   Read the error message out loud. The histories have diverged; there is nothing to "slide forward."
5. Do the real merge and inspect what Git built:
   ```bash
   git merge side-quest
   git log --graph --oneline
   ```
   Find the **merge commit** at the top — the commit with two parent lines flowing into it, just like commit M in the diagram.
6. Write one sentence: what would you have needed to do differently in steps 2–3 for `--ff-only` to succeed?

*(Standalone file: [activities/02-break-the-fast-forward.md](activities/02-break-the-fast-forward.md))*

</details>

---

## <font color="#388bfd">Pull Requests</font>

A **pull request** (PR) is a proposal to merge one branch into another. Instead of merging directly, you push your branch to GitHub and open a PR so teammates (or maintainers) can review, comment, and approve the changes before they reach main.

Think of a PR as a **suggestion box for code**: you can push freely to your own branch without disturbing anyone, and the team decides together what makes it into the shared version. That gatekeeping is what keeps main stable — nothing lands without a second look.

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
7. After review and approval, merge it

**In GitKraken:** right-click your feature branch in the left panel → **Start a pull request** → fill in the form. Open PRs appear in the **Pull Requests** section on the left.

> **Tip:**
> A good PR description answers: what changed, why it changed, and how to test it. Even if no one else reviews your PR, writing this forces you to think clearly about what you shipped.

---

## <font color="#388bfd">Reviewing a Pull Request</font>

Half of the PR workflow is being on the **other side** — the reviewer. When someone opens a PR against your repository, you have two choices: **approve** it, or **request changes** with feedback. A real review checks four things:

1. **Examine the changes** — read every modified line in the "Files changed" view, not just the description
2. **Check for conflicts** — will this clash with what's already on main?
3. **Test the functionality** — does the code actually do what the description claims, without breaking anything else?
4. **Give constructive feedback** — comment on specific lines; say *why*, not just *what* ("this crashes when the file is empty — try guarding the read")

If you request changes, the PR goes back to the author, they push fixes to the **same branch** (the PR updates automatically), and you review again. Only when a reviewer is satisfied does the merge button get pressed.

> **Note:**
> Review is not about catching bad programmers — it's how good teams share knowledge. The reviewer learns what changed; the author gets a second brain on their logic. You will both write and review PRs in this course, and both sides are graded skills.

---

## <font color="#388bfd">Squash and Merge vs. Regular Merge</font>

When you press the merge button on GitHub, a dropdown offers choices. The two that matter:

| | Regular merge | Squash and merge |
|---|---|---|
| **Commits on main** | Every commit from the branch, plus a merge commit | Exactly one new commit containing all the changes |
| **History shows** | The full development story, including "wip" and "fix typo" | A clean, one-line summary per feature |
| **Best when** | The intermediate steps matter for future readers | The branch history is messy and only the result matters |

**Squash and merge** collapses your whole branch — five commits of experimentation, backtracking, and typo fixes — into a single tidy commit on main. **Regular merge** preserves every step. Neither is "correct": teams choose based on whether the journey or the destination belongs in main's history. In this course, squash-merge your PRs when your branch history is scratch work, and regular-merge when each commit is meaningful on its own.

👉 <details>
<summary><h3>Activity: Squash or Preserve — click to expand</h3></summary>

*Concept: Squashing collapses a messy branch into one clean commit on main — the work survives, the noise doesn't.*

![Diagram comparing the two ways the same branch can land in history: the messy-feature branch holds three commits (wip, still broken, actually works now); a regular merge delivers all three commits plus a merge commit to main, while squash-and-merge delivers a single clean commit named Add widget feature. The final content is identical either way — only the history differs.](assets/squash-or-preserve.svg)

## Task

1. In your terminal, inside your practice repository, create a branch and deliberately make three low-quality commits — the kind every programmer actually makes:
   ```bash
   git checkout -b messy-feature
   echo "draft" > widget.txt && git add . && git commit -m "wip"
   echo "draft 2" > widget.txt && git add . && git commit -m "still broken"
   echo "final version" > widget.txt && git add . && git commit -m "actually works now"
   ```
2. Look at the mess you'd be sending to main:
   ```bash
   git log --oneline -3
   ```
3. Squash-merge the branch locally (this is what GitHub's "Squash and merge" button does):
   ```bash
   git checkout main
   git merge --squash messy-feature
   git commit -m "Add widget feature"
   ```
4. Compare histories:
   ```bash
   git log --oneline -3
   ```
   Main received **one** commit. Check `cat widget.txt` — the final content all arrived; the "wip" and "still broken" steps did not.
5. Write one sentence describing a situation where you would want the opposite — a regular merge that preserves every commit.

*(Standalone file: [activities/03-squash-or-preserve.md](activities/03-squash-or-preserve.md))*

</details>

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

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Create a new branch with a descriptive name and switch to it.
- [ ] List all branches in a repository and identify which one is current.
- [ ] Merge a feature branch into main and confirm the commits appear.

### <font color="#79c0ff">Intermediate</font>

- [ ] Push a branch to GitHub and open a pull request with a clear title and description.
- [ ] Explain when a fast-forward merge occurs and construct a situation where it cannot.
- [ ] Review a pull request: examine the changed files, then approve it or request changes with a specific, constructive comment.
- [ ] Create a `.gitignore` that correctly excludes compiled Java files and macOS system files.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain the difference between a fast-forward merge and a merge commit, and why teams rarely get fast-forwards.
- [ ] Distinguish the merge *mechanism* (fast-forward, merge commit, squash) from the PR *workflow*, and explain how one PR could end in any of the three.
- [ ] Choose between squash-and-merge and regular merge for a given branch history, and defend the choice.
- [ ] Explain why `.gitignore` must be committed and what happens to files Git already tracks.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] **Visualize everything:** run `git log --graph --oneline --all` after your activities and identify every branch, merge commit, and squash in the drawing.
- [ ] **Research branch protection:** find out how GitHub's protected-branch rules force every change to main through a reviewed PR — and why companies turn this on.
- [ ] **Meet the other history tool:** read about `git rebase` and how it differs from merging. (We don't use it yet — but you'll recognize it in the wild.)

---

[Assignment](ASSIGNMENT.md)

← [Repositories and Commits](../RepositoriesAndCommits/) — Next: [Forks and Collaboration](../ForksAndCollaboration/)
