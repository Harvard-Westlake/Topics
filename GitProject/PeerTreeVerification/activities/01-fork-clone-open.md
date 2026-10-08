# Activity — Fork, Clone, Open

*Concept: A fork is a copy of a classmate's repository under your own account — you clone the fork, not the original, so everything you do today lands in a repository you control.*

![Diagram of the fork-then-clone path: on the left, the classmate's repository git-project-THEIRNAME on GitHub; a Fork arrow copies it into your account as YOUR-USERNAME/git-project-THEIRNAME, labeled forked from the original; a gh repo fork --clone arrow brings that fork down to your laptop in HTCS_Projects, where origin points at your fork and upstream at the original. A crossed-out arrow from the laptop straight to the classmate's repository is marked push refused — you never write to their repo.](../assets/fork-clone-open.svg)

## Task

1. On GitHub, open the repository you were assigned (`git-project-THEIRNAME`). Confirm it belongs to a classmate, not to you, and not to the classmate whose code you reviewed in Part 2.
2. In your terminal, go to your projects folder, then fork the repository and clone your fork in one step:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/git-project-THEIRNAME --clone
   cd git-project-THEIRNAME
   ```
   On GitHub, your copy now shows **forked from THEIR-USERNAME/git-project-THEIRNAME** under its title.
3. Prove where the remotes point:
   ```bash
   git remote -v
   ```
   Four lines: `origin` under **your** username (your fork) and `upstream` under the classmate's (the original). If `origin` shows the classmate's username, you cloned the original — delete the folder and run the fork command again.
4. Read the history for your first clue about what was attempted:
   ```bash
   git log --oneline | head -20
   ```
   Count the commits labeled `(GP-3.1)`, `(GP-3.2)`, and `(GP-3.3)`. A milestone with no commit is a milestone you should expect to find missing.
5. Open the folder in the editor you use for Java and read `README.md` first. Write down, in one line each, every tree-related method it claims exists.
