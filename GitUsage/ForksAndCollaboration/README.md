<div align="center">

# Forks and Collaboration
*<font color="#8b949e">Contributing to projects you don't own — forking, syncing, and open source</font>*

<font color="#a371f7">Learning</font>

</div>

---

Yesterday you branched, merged, and reviewed inside a repository you own. But the most interesting code on Earth belongs to *other people* — open source projects, classmates' repos, libraries you use every day. Today you learn the machinery that lets a stranger safely contribute to a project they can't even push to: the **fork**. This exact workflow — fork, change, propose — built Linux, Firefox, Python, VS Code, React, and nearly every tool you touched this week.

## <font color="#388bfd">Table of Contents</font>

1. [Choose the right tool: branch, collaborator, or fork](#three-ways-to-collaborate)
2. [Fork any public repository into your own account](#how-to-fork-a-repository)
3. [Clone your fork and understand where origin points](#cloning-your-fork)
4. [Make changes and push them to your fork](#making-changes-and-pushing)
5. [Keep your fork in sync with the original using an upstream remote](#keeping-your-fork-in-sync)
6. [Contribute back with a cross-fork pull request](#contributing-back-with-pull-requests)
7. [See how real maintainers review contributions](#how-maintainers-review-your-pr)
8. [Check your understanding and try the stretch goals](#check-for-understanding)

---

## <font color="#388bfd">Three Ways to Collaborate</font>

By now you've seen two collaboration tools, and today adds the third. Each answers a different trust question:

| | Branch | Collaborator | Fork |
|---|---|---|---|
| **Lives in** | Same repository | Same repository | Your own copy of the repository |
| **Access needed** | Write access | Owner invites you (Settings → Collaborators) | None — any public repo can be forked |
| **Used for** | Your own feature work | Trusted teammates on a shared project | Contributing to projects you don't own |
| **Syncing with original** | Already connected | Already connected | Requires adding an upstream remote |
| **PR target** | Another branch, same repo | Another branch, same repo | The original repository, across accounts |

- Use a **branch** when it's your repository.
- Use a **collaborator invite** for a small trusted team — the owner adds teammates under **Settings → Collaborators**, and everyone pushes branches to the *same* repo and PRs internally, exactly like yesterday.
- Use a **fork** when you have no write access and never will — an open source library, a stranger's project, or any public repo. Forking creates a complete copy **under your account** that you fully control.

The fork is what makes open source possible: millions of people who don't trust each other can still build one project, because nobody needs write access to contribute.

👉 <details>
<summary><h3>Activity: Branch, Collaborator, or Fork? — click to expand</h3></summary>

*Concept: The right collaboration tool is determined by one question — what access do you have, and what access should you have?*

![Three-panel diagram of the collaboration tools: BRANCH is a second timeline inside a repo you already own; COLLABORATOR is a shared repo where the owner invited you and both people push directly; FORK is a full copy of a stranger's project under your own account, with a pull request arrow proposing changes back to the original.](assets/branch-collaborator-fork.svg)

## Task

For each scenario, write down **branch**, **collaborator**, or **fork**, plus one phrase of justification:

1. You want to fix a typo in the README of the Python programming language's official repository.
2. You and two classmates are building a group project together for the next month.
3. You want to add a feature to your own personal website's repository without breaking the live version.
4. Your teacher posts a starter-code repository and wants every student to build on it independently and propose their solution back.
5. A classmate asks you to help debug their personal project for one afternoon — they trust you and want you pushing directly.
6. Compare answers with a neighbor. For any disagreement, argue it out: what happens if the *wrong* tool is used in that scenario?

*(Standalone file: [activities/01-branch-collaborator-or-fork.md](activities/01-branch-collaborator-or-fork.md))*

</details>

---

## <font color="#388bfd">How to Fork a Repository</font>

1. Navigate to any public repository on GitHub
2. Click the **Fork** button in the top-right corner of the page
3. Select your account as the destination
4. GitHub creates a full copy of the repository under your account — you will see **"forked from [original]"** under the repo name

Your fork is now completely independent of the original. Changes you make to your fork do not affect the original, and changes to the original do not automatically appear in your fork.

> **Note:**
> A fork copies the whole history — every commit, every branch. It is the same "living repository" idea from Day 1's Clone vs. ZIP challenge, just copied *account-to-account* instead of *cloud-to-laptop*.

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

**In GitKraken:** right-click the Remote section → Add Remote → enter `upstream` and the original URL. To sync: right-click upstream → Fetch upstream → right-click `upstream/main` → Merge into current branch → Push. GitKraken's ahead/behind indicators show at a glance when your fork has fallen behind.

> **Tip:**
> Sync your fork before starting new feature work. If you branch from a stale fork, your PR will be harder to merge.

👉 <details>
<summary><h3>Activity: Two Remotes, One Truth — click to expand</h3></summary>

*Concept: A fork has two remotes — origin (your copy, which you can push to) and upstream (the original, which you can only read from).*

![Diagram of a laptop clone tracking two remotes: upstream is the original octocat/Spoon-Knife repository which you can only fetch from — pushing to it is refused for lack of permission — while origin is your own fork, which accepts both push and fetch. A dashed arrow marks that origin was forked from upstream.](assets/two-remotes-one-truth.svg)

## Task

1. On GitHub, fork the repository `octocat/Spoon-Knife` — GitHub's official practice-fork repo.
2. In your terminal, clone **your fork** and step inside:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Spoon-Knife.git
   cd Spoon-Knife
   ```
3. Still in your terminal, wire up the second remote and inspect both:
   ```bash
   git remote add upstream https://github.com/octocat/Spoon-Knife.git
   git remote -v
   ```
   You should see four lines: `origin` fetch/push pointing at your account, `upstream` fetch/push pointing at octocat — exactly the two boxes in the diagram.
4. Fetch from upstream and compare the two remotes' views of main:
   ```bash
   git fetch upstream
   git log origin/main -1 --oneline
   git log upstream/main -1 --oneline
   ```
5. Write one sentence for each remote: which one can you push to, and why?

*(Standalone file: [activities/02-two-remotes-one-truth.md](activities/02-two-remotes-one-truth.md))*

</details>

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

**In GitKraken:** create the PR from your fork and check the direction carefully — the **To Repo** must be the original repository and the **From Repo** your fork.

> **Note:**
> You cannot merge your own PR into someone else's repository — that is the maintainer's decision. Your job is to make the PR easy to understand and review.

---

## <font color="#388bfd">How Maintainers Review Your PR</font>

Yesterday you learned to review PRs inside your own repo. Cross-fork review works the same, with higher stakes: the maintainer has never met you, so **your PR has to speak for itself.** A maintainer receiving your PR will:

1. **Read the description first** — if they can't tell what the change does and why, many won't read further
2. **Examine the diff** — checking that the change is minimal, focused, and touches nothing unrelated
3. **Test it** — does the project still build and behave?
4. **Respond** — approve and merge, request changes with comments, or close it with an explanation

If changes are requested, you don't open a new PR — you push more commits to the **same branch on your fork**, and the PR updates automatically. This review loop can repeat several times on real projects; it's normal, not a failure.

> **Tip:**
> Before contributing to any real open source project, read its `CONTRIBUTING.md` file. Maintainers spell out exactly what they want in a PR — matching it is the single biggest factor in getting merged.

👉 <details>
<summary><h3>Activity: The Review Hat — click to expand</h3></summary>

*Concept: Real code review is a conversation — requested changes get pushed to the same branch, and the PR evolves until the maintainer is satisfied.*

![Diagram of the pull request review loop: the author opens the PR, the reviewer reads every changed line, and either approves and merges, or requests changes with comments on specific lines; the author then pushes fixes to the same branch, the PR updates automatically, and the loop repeats until the reviewer approves.](assets/the-review-hat.svg)

## Task

1. In your browser, open the pull requests page of a major open source project — for example: `github.com/microsoft/vscode/pulls`.
2. Filter to closed PRs and open one that is **merged** and has review comments (look for PRs with a conversation count — click a few until you find one where a reviewer left line comments).
3. Read the conversation with the review checklist from yesterday in mind, and write down:
   - One thing the reviewer asked the author to change, quoted or paraphrased
   - How the author responded (a code change? a counter-argument? both?)
   - How many rounds of the loop in the diagram the conversation took before merge
4. Look at the PR's description. Does it answer *what changed, why, and how to test*? Grade it out of 3.
5. Write one sentence: what did the reviewer catch that the author missed — and what does that tell you about why maintainers require review before merging?

*(Standalone file: [activities/03-the-review-hat.md](activities/03-the-review-hat.md))*

</details>

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Fork a repository on GitHub and identify that it now exists under your account.
- [ ] Clone your fork and confirm that `origin` points to your copy, not the original.
- [ ] Pick the right tool — branch, collaborator, or fork — for a given collaboration scenario and justify the choice.

### <font color="#79c0ff">Intermediate</font>

- [ ] Add an `upstream` remote and verify both remotes with `git remote -v`.
- [ ] Sync your fork with upstream changes and push the updated `main` to your fork.
- [ ] Push a feature branch to your fork and open a pull request across forks, with the base and head repositories set correctly.

### <font color="#79c0ff">Advanced</font>

- [ ] Walk through the entire open source contribution cycle — fork, clone, branch, commit, push, PR, review loop — without referring to notes.
- [ ] Explain what happens if you open a PR from a fork while the original repo has diverged from your fork's `main`, and how syncing first prevents it.
- [ ] Describe the maintainer's review process for an incoming cross-fork PR and two reasons a PR would be rejected.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] **Use the shortcut:** find the **Sync fork** button on your fork's GitHub page and compare what it does to the fetch/merge/push sequence you ran by hand.
- [ ] **Read a real CONTRIBUTING.md:** open the contributing guide of a project you use (VS Code, React, Python) and list two rules that surprised you.
- [ ] **Find first-timer bait:** search GitHub for issues labeled `good first issue` in a language you know, and read what an actual entry-level open source contribution looks like.

---

[Assignment](ASSIGNMENT.md)

← [Branching and Merging](../BranchingAndMerging/) — Next: [File Hashing and Integrity](../FileHashing/)
