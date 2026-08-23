# Activity — The Parallel Universe

*Concept: A branch is a genuinely separate line of development — files committed on it don't exist on main until you merge.*

![Diagram of one folder with two universes: the main timeline holds commits A and B, while the experiment branch forks off with commit C containing universe-b.txt. Two terminal panels show that ls on main lists only clue.txt, while ls on experiment also lists universe-b.txt — the file waits inside .git/ while you stand on main.](../assets/parallel-universe.svg)

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
