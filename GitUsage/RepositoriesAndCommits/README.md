<div align="center">

# Repositories and Commits
*<font color="#8b949e">How Git tracks your work — repositories, cloning, staging, and sharing code</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

1. [Learn what a repository is and how Git stores its history](#what-is-a-repository)
2. [See where a repository actually lives — local vs. GitHub](#where-is-a-repository)
3. [Start tracking a project with Git two different ways](#initializing-a-repository)
4. [Download a complete copy of any repository from GitHub](#cloning-a-repository)
5. [Read GitKraken's commit graph, staging panel, and commit message area](#the-gitkraken-interface)
6. [Choose exactly which changes go into your next commit](#staging-changes)
7. [Save a permanent, labeled snapshot of your staged work](#committing-changes)
8. [Keep your local repo and GitHub in sync](#pushing-and-pulling)

---

## <font color="#388bfd">What is a Repository?</font>

A **repository** (repo) is a project folder that Git has been set up to track. It stores not just your current files but the entire history of every change ever saved — who made it, when, and why.

That history lives inside a hidden folder called `.git` at the root of your project. Every commit, every branch, every author name and timestamp is stored in there. You will never edit `.git` directly — Git manages it for you through commands like `git commit` and `git push`. But knowing it exists explains why a repo folder seems "normal" while carrying years of history.

```bash
ls -a                   # show hidden files — you will see .git listed
ls .git                 # peek inside: branches, commits, config, objects
```

> **Tip:**
> A name that starts with a dot, like `.git`, is the Unix convention for a **hidden file or folder** — a plain `ls` (and your file manager) skips over anything named this way by default, since it's meant for tools to read, not for you to browse. That's the whole reason `.git` doesn't clutter your project folder even though it's quietly holding your entire history. `ls -a` — the `a` is for "all" — overrides that and shows hidden names too.

---

## <font color="#388bfd">Where is a Repository?</font>

A single repository actually exists in two places at once, and Git treats them as genuinely separate copies:

| Type | Where | Purpose |
|---|---|---|
| **Local** | Your machine | Where you write and test code |
| **Remote** | GitHub (or similar) | Shared backup and collaboration hub |

Your **local** repo is just a folder on your computer with a `.git` inside it — it works completely offline, and every commit you make happens there first. Your **remote** repo is that same project hosted on the internet (GitHub, in this course), so anyone with access can see it, clone it, or collaborate on it.

The two stay in sync through **push** (local → remote) and **pull** (remote → local). Git never assumes the two are in sync — you always sync them explicitly. This means you can commit freely offline and push everything when you are ready.

> **Note:**
> The remote is not a real-time mirror. Until you push, changes you commit locally exist only on your machine. Until you pull, changes others pushed exist only on GitHub.

---

## <font color="#388bfd">Initializing a Repository</font>

### <font color="#79c0ff">Recommended: create on GitHub first, then clone</font>

1. Go to GitHub and click **New repository**
2. Give it a name, set it to public or private, and click **Create repository**
3. Copy the URL and clone it (see [Cloning a Repository](#cloning-a-repository) below)

This approach sets up the remote automatically so there is nothing to configure.

### <font color="#79c0ff">Alternative: initialize locally</font>

```bash
git init
```

This creates a `.git` folder in the current directory. Git now tracks this folder. To connect it to GitHub afterward:

```bash
git remote add origin https://github.com/username/repo-name.git
git push -u origin main
```

**In GitKraken:** folder icon (top left) → Init → Local Only → select your folder → Create Repository.

> **Tip:**
> Creating on GitHub first and cloning is cleaner for beginners — the remote is already configured when you clone.

---

## <font color="#388bfd">Cloning a Repository</font>

**Cloning** downloads a complete copy of a repository to your machine — not just the current files but the entire commit history, all branches, and all metadata.

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

After cloning:
- The project files are in your current directory
- The full commit history is available locally — run `git log` to see it
- Git has automatically configured `origin` to point to the URL you cloned from

```bash
# Verify the remote was set up automatically
git remote -v
# origin  https://github.com/username/repo-name.git (fetch)
# origin  https://github.com/username/repo-name.git (push)
```

**Cloning vs downloading a ZIP:**

| | `git clone` | Download ZIP |
|---|---|---|
| Gets commit history | Yes — every past commit | No — current files only |
| Sets up remote | Yes — `origin` is ready | No — disconnected from GitHub |
| Can push changes | Yes | No |

Always clone. Downloading a ZIP gives you the files but none of the Git machinery that makes collaboration possible.

**Finding the URL:** click the green or blue **Code** button on any GitHub repository page and copy the HTTPS link.

**In GitKraken:** click **Clone a Repo** on the home screen → paste the repository URL → choose a destination folder → click **Clone the repo!**

---

## <font color="#388bfd">The GitKraken Interface</font>

When you open a repository in GitKraken, three areas matter most:

- **Commit graph** (center) — each dot is a commit; lines show how branches diverge and merge; the top is the most recent work
- **Unstaged / Staged panel** (top right) — files you have changed since the last commit; click the `+` to stage a file
- **Commit message panel** (bottom right) — the Summary field (required) and Description field (optional) before you click **Commit Changes**

The commit graph is the visual record of your project. Every dot is a decision that was made and saved.

---

## <font color="#388bfd">Staging Changes</font>

In plain English, "saving" your work in Git actually happens in two stages: **staging**, then **committing**. Staging is a preparation step that lets you choose exactly which changes to include in the next commit. Even if you modified ten files, you can commit just one.

```bash
git status              # see what has changed since the last commit
git add filename.txt    # stage a specific file
git add .               # stage every changed file in the current directory
git status              # run again to confirm what is now staged
```

After `git add`, run `git status` again. Staged files appear under **"Changes to be committed"** — these are the files that will be saved in the next commit. Unstaged files will not be included.

> **Note:**
> `git add .` stages everything changed in your current directory. Use `git add filename` when you want precise control over what a commit contains — for example, when you fixed two separate bugs and want one commit per fix.

**In GitKraken:** changed files appear in the top-right panel. Click the `+` next to any file to stage it, or click **Stage all changes**.

---

## <font color="#388bfd">Committing Changes</font>

![Meme from Spaceballs: a soldier peers through binoculars as another asks "What are you preparing? You're always preparing!" and a third yells "JUST GO!" — staging is the preparing; committing is the JUST GO](assets/spaceballs-staging-vs-committing.jpg)

Staging is the preparing. Committing is the "just go" — it's where the save actually happens. A commit saves a permanent, labeled snapshot of everything currently staged. Every commit requires a message explaining what changed.

```bash
git commit -m "Short present-tense description of what changed"
```

**Writing good commit messages:**

| Good | Too vague |
|---|---|
| `Fix login redirect after password reset` | `fixed stuff` |
| `Add dark mode toggle to settings page` | `update` |
| `Remove duplicate user check in registration` | `changes` |

- Use **present tense**: `Add feature` not `Added feature`
- Be **specific**: a future reader should understand what changed without reading the diff
- Describe **what and why**, not how

> **Important:**
> Commits are permanent. You cannot easily undo one without rewriting history. Think about the message before you commit.

**In GitKraken:** fill in the **Summary** field and optionally a **Description**, then click **Commit Changes**.

---

## <font color="#388bfd">Pushing and Pulling</font>

Pushing is a third stage hiding behind the word "saving": staging prepares it, committing saves it locally, and pushing saves it online. So saving your work in Git is secretly three steps — stage, commit, push.

**Push** uploads your local commits to GitHub so teammates (and backups) can see them:

```bash
git push
```

**Pull** downloads and integrates the latest commits from GitHub into your local repo:

```bash
git pull
```

> **Tip:**
> Always `git pull` before starting new work. If someone pushed changes while you were away, pulling first means you are working from the latest version and are less likely to encounter conflicts when you push.

**In GitKraken:** use the **Push** and **Pull** buttons in the top toolbar.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain the difference between a local and a remote repository?
- [ ] Can you clone a repository from GitHub and identify what `origin` is set to?
- [ ] Can you stage a file using `git add` and confirm it is staged with `git status`?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain what the `.git` folder is, why its name starts with a dot, and why you should never edit it directly?
- [ ] Can you explain the difference between `git clone` and downloading a ZIP?
- [ ] Can you push commits to GitHub and verify they appear on the repository page?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you walk through the full workflow — clone, edit, stage, commit, push — without referring to notes?
- [ ] Can you explain why `git add .` and `git add filename` produce different results and when each is appropriate?
- [ ] Can you write a commit message that someone reading the history in six months would find genuinely useful?

---

[Assignment](ASSIGNMENT.md)

← Back to [Git Usage](../) — Next: [Branching and Merging](../BranchingAndMerging/)
