# Activity — Fork, Clone, Open

*Concept: Grab a classmate's code without asking their permission, and start working from your own copy of it.*

![Diagram of the fork-then-clone path: on the left, the classmate's repository THEIR-REPO-NAME on GitHub; a Fork arrow copies it into your account as YOUR-USERNAME/THEIR-REPO-NAME, labeled forked from the original; a gh repo fork --clone arrow brings that fork down to your laptop in HTCS_Projects, where origin points at your fork and upstream at the original. A crossed-out arrow from the laptop straight to the classmate's repository is marked push refused. You never write to their repo.](../assets/fork-clone-open.svg)

## Task

1. Wait for your teacher to assign you a classmate. Open their repository on GitHub and confirm it belongs to that classmate, not to you, and not to the classmate whose code you reviewed in Part 2. Everyone forked once in Part 2, so the repository you get is often a fork itself. Under its name you may see a line like this:
   ```
   THEIR-USERNAME/THEIR-REPO-NAME
   forked from ANOTHER-CLASSMATE/THEIR-REPO-NAME
   ```
   That is expected. You are reviewing the code your classmate worked on, wherever it started.
2. In your terminal, go to your projects folder, then fork the repository and clone your fork in one step. `--fork-name` lets you call your copy whatever you want, which matters if you already have a repository with the same name:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/THEIR-REPO-NAME --clone --fork-name ANY-NAME-YOU-WANT
   cd ANY-NAME-YOU-WANT
   ```
   On GitHub, your copy now shows **forked from THEIR-USERNAME/THEIR-REPO-NAME** under its title.
3. Prove where the remotes point:
   ```bash
   git remote -v
   ```
   You should see four lines like these:
   ```
   origin    git@github.com:YOUR-USERNAME/ANY-NAME-YOU-WANT.git (fetch)
   origin    git@github.com:YOUR-USERNAME/ANY-NAME-YOU-WANT.git (push)
   upstream  git@github.com:THEIR-USERNAME/THEIR-REPO-NAME.git (fetch)
   upstream  git@github.com:THEIR-USERNAME/THEIR-REPO-NAME.git (push)
   ```
   `origin` is under **your** username (your fork) and `upstream` is under the classmate's (the original). If `origin` shows the classmate's username, you cloned the original. Delete the folder and run the fork command again.
4. Optional: check that your classmate worked on this recently.
   ```bash
   git log
   ```
   Look at the `Date:` lines. The newest commit is at the top:
   <pre>
   commit 9f2c1e7a4b8d0c3e5f6a7b8c9d0e1f2a3b4c5d6e (HEAD -> main, origin/main)
   Author: Their Name &lt;them@example.com&gt;
   <strong><font color="#f0883e">Date:   Wed Oct 7 21:14:03 2026 -0700</font></strong>

       finished root tree

   commit 41d07be29c8a51f3e6b0d2a7c94e18f5b3a6d720
   Author: Their Name &lt;them@example.com&gt;
   <strong><font color="#f0883e">Date:   Mon Oct 5 19:02:47 2026 -0700</font></strong>

       index paths
   </pre>
   Recent dates mean they were working on it. Do not rely on the commit messages; classmates do not always label them clearly. Press `q` to leave the log.
5. Open the folder in VS Code and read their `README.md` first. Write down, in one line each, every tree-related method it claims exists.
