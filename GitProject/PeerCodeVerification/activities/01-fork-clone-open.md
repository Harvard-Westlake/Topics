# Activity — Fork, Clone, Open

*Concept: A fork is a copy of a classmate's repository under your own account — you clone the fork, not the original, so everything you do today lands in a repository you control.*

![Diagram of the fork-then-clone path: on the left, the classmate's repository git-project-THEIRNAME on GitHub; a Fork arrow copies it into your account as YOUR-USERNAME/git-project-THEIRNAME, labeled forked from the original; a git clone arrow brings that fork down to your laptop in HTCS_Projects, where origin points at your fork. A crossed-out arrow from the laptop straight to the classmate's repository is marked push refused — you never write to their repo.](../assets/fork-clone-open.svg)

## Task

1. On GitHub, open the repository you were assigned (`git-project-THEIRNAME`). Confirm it belongs to a classmate and not to you.
2. Click **Fork** in the top-right corner, keep the repository name, and click **Create fork**. Wait until you see **forked from THEIR-USERNAME/git-project-THEIRNAME** under the title.
3. In your terminal, go to your projects folder and clone **your fork** — not the original:
   ```bash
   cd ~/HTCS_Projects
   git clone git@github.com:YOUR-USERNAME/git-project-THEIRNAME.git
   cd git-project-THEIRNAME
   ```
4. Prove where `origin` points:
   ```bash
   git remote -v
   ```
   Both lines must show **your** username. If they show the classmate's, you cloned the original — delete the folder and clone the fork instead.
5. Open the folder in the editor you use for Java and read `README.md` first. Write down, in one line each, every method the README claims exists.
6. Look at the history for your first clue about what was attempted:
   ```bash
   git log --oneline | head -20
   ```
   Count how many commits carry a `(GP-2.x)` label. A milestone with no commit is a milestone you should expect to find missing.
