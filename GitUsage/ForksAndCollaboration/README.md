<div align="center">

# Forks and Collaboration
*<font color="#8b949e">Contributing to projects you don't own — forking, syncing, and open source</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Forking vs Branching](#forking-vs-branching)**  
Two ways to diverge from a codebase, and when to use each.

**[How to Fork a Repository](#how-to-fork-a-repository)**  
Creating your own copy of any public repository on GitHub.

**[Cloning Your Fork](#cloning-your-fork)**  
Getting your fork onto your local machine.

**[Making Changes and Pushing](#making-changes-and-pushing)**  
The same stage → commit → push cycle, now on your fork.

**[Keeping Your Fork in Sync](#keeping-your-fork-in-sync)**  
Pulling updates from the original repository into your fork.

**[Contributing Back with Pull Requests](#contributing-back-with-pull-requests)**  
Proposing your changes to the original repository.

---

## <font color="#388bfd">Forking vs Branching</font>

| | Branch | Fork |
|---|---|---|
| **Lives in** | Same repository | Your own copy of the repository |
| **Access needed** | Write access to the repo | None — any public repo can be forked |
| **Used for** | Internal feature development | Contributing to projects you don't own |
| **Syncing with original** | Already connected | Requires adding an upstream remote |
| **PR target** | Another branch in the same repo | The original repository across accounts |

Use a **branch** when you have write access and are working within a shared team repo. Use a **fork** when you want to contribute to someone else's project — an open source library, a classmate's project, or any public repo you cannot push to directly.

Open source projects you may have used that started as forks and contributions: Linux, Android, Firefox, Python, VS Code, React, Node.js.

---

## <font color="#388bfd">How to Fork a Repository</font>

1. Navigate to any public repository on GitHub
2. Click the **Fork** button in the top-right corner of the page
3. Select your account as the destination
4. GitHub creates a full copy of the repository under your account — you will see **"forked from [original]"** under the repo name

Your fork is now completely independent of the original. Changes you make to your fork do not affect the original, and changes to the original do not automatically appear in your fork.

---

## <font color="#388bfd">Cloning Your Fork</font>

Fork first on GitHub, then clone **your fork** (not the original) to your local machine:

```bash
git clone https://github.com/YOUR-USERNAME/repo-name.git
cd repo-name
```

After cloning, `origin` points to your fork:

```bash
git remote -v
# origin  https://github.com/YOUR-USERNAME/repo-name.git (fetch)
# origin  https://github.com/YOUR-USERNAME/repo-name.git (push)
```

You can push freely to `origin` since it is your fork — no permission required.

---

## <font color="#388bfd">Making Changes and Pushing</font>

Working in a fork uses exactly the same workflow as any other repository:

```bash
git checkout -b feature-name    # create a branch for your change
# make your changes
git add .
git commit -m "Describe what you changed and why"
git push origin feature-name    # push branch to your fork
```

Working on a branch (rather than directly on `main`) keeps your fork's main clean and makes it easier to open a PR and sync with upstream later.

---

## <font color="#388bfd">Keeping Your Fork in Sync</font>

The original repository keeps moving after you fork it. To pull those updates into your fork, you need to configure an **upstream** remote pointing to the original:

```bash
# Add once — you only need to do this step once per clone
git remote add upstream https://github.com/ORIGINAL-OWNER/repo-name.git

# Verify both remotes are set up
git remote -v
# origin    https://github.com/YOUR-USERNAME/repo-name.git (fetch)
# origin    https://github.com/YOUR-USERNAME/repo-name.git (push)
# upstream  https://github.com/ORIGINAL-OWNER/repo-name.git (fetch)
# upstream  https://github.com/ORIGINAL-OWNER/repo-name.git (push)
```

To sync your fork with the latest upstream changes:

```bash
git checkout main
git fetch upstream               # download upstream changes (does not merge yet)
git merge upstream/main          # integrate upstream changes into your local main
git push origin main             # update your fork on GitHub
```

Run this whenever the original repo gets new commits you want.

**In GitKraken:** right-click the Remote section → Add Remote → enter `upstream` and the original URL. To sync: right-click upstream → Fetch upstream → right-click `upstream/main` → Merge into current branch → Push.

> **Tip:**
> Sync your fork before starting new feature work. If you branch from a stale fork, your PR will be harder to merge.

---

## <font color="#388bfd">Contributing Back with Pull Requests</font>

After pushing a feature branch to your fork, open a pull request to the **original repository**:

1. Go to **your fork** on GitHub
2. Click **Pull requests** → **New pull request**
3. GitHub shows a **comparing across forks** selector:
   - **base repository:** the original repo, base branch `main`
   - **head repository:** your fork, compare branch `feature-name`
4. Review the diff — confirm only your intended changes are included
5. Write a clear title and description:
   - What did you change?
   - Why is this change useful or necessary?
   - How can the maintainer test it?
6. Click **Create pull request**

The original maintainer will review your PR and may ask for changes, approve it, or close it with feedback. If approved, they merge it and your code becomes part of the original project.

> **Note:**
> You cannot merge your own PR into someone else's repository — that is the maintainer's decision. Your job is to make the PR easy to understand and review.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you fork a repository on GitHub and identify that it now exists under your account?
- [ ] Can you clone your fork and confirm that `origin` points to your copy, not the original?
- [ ] Can you explain the difference between a fork and a branch in one sentence each?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you add an `upstream` remote and verify it with `git remote -v`?
- [ ] Can you sync your fork with upstream changes and push the updated `main` to your fork?
- [ ] Can you push a feature branch to your fork and open a pull request to the original repository?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you walk through the entire open source contribution cycle — fork, clone, branch, commit, push, PR — without referring to notes?
- [ ] Can you explain what happens if you open a PR from a fork while the original repo has diverged from your fork's `main`?
- [ ] Can you describe two scenarios where a PR would be rejected and what you would do in each case?

---

[Assignment](ASSIGNMENT.md)

← [Branching and Merging](../BranchingAndMerging/) — Back to [Git Usage](../)
