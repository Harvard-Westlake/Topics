# Activity — The Split Commit

*Concept: The staging area gives you granular control over exactly what gets saved in a commit.*

## Task

1. Inside the `live-repo` folder you cloned in the previous activity, create two new files:
   ```bash
   echo "Feature A" > feature-a.txt
   echo "Feature B" > feature-b.txt
   ```
2. Using GitKraken (or `git add feature-a.txt` in the terminal), stage **only** `feature-a.txt` — leave `feature-b.txt` untouched.
3. Commit just the staged file with a descriptive message, e.g. `Add feature A`.
4. Run `git status` and confirm `feature-b.txt` still shows up as an untracked/unstaged change — it was deliberately left behind.
5. In your own words, write one sentence explaining what would have happened to `feature-b.txt` if you had run `git add .` instead of `git add feature-a.txt`.
