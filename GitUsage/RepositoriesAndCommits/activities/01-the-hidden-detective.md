# Activity — The Hidden Detective

*Concept: Proving that a repository's history lives locally, inside the hidden `.git` folder.*

## Task

1. Open your terminal and create a new folder anywhere convenient, then move into it:
   ```bash
   mkdir git-detective
   cd git-detective
   ```
2. Turn it into a repository:
   ```bash
   git init
   ```
3. List the folder's contents normally:
   ```bash
   ls
   ```
   Nothing prints — the folder looks empty.
4. Now list *all* files, including hidden ones:
   ```bash
   ls -a
   ```
   You should see `.git` in the output. That's the folder `git init` just created.
5. Move inside it and look around:
   ```bash
   cd .git
   ls
   ```
   You're looking at Git's raw machinery: `objects/` (where every version of every file is actually stored), `refs/` (where branch names point to), and `HEAD` (a plain text file naming your current branch).
6. Return to your project root before you finish:
   ```bash
   cd ..
   ```
