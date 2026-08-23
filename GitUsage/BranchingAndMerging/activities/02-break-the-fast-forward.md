# Activity — Break the Fast-Forward

*Concept: A fast-forward is only possible while main holds still — one commit on main while you work forces a real merge commit.*

![Diagram of diverged history: main holds commits A and B, then a teammate's commit F lands on main while your commit C sits on the side-quest branch. git merge --ff-only refuses because the histories diverged; a plain git merge instead creates merge commit M with two parents, F and C.](../assets/break-the-fast-forward.svg)

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
