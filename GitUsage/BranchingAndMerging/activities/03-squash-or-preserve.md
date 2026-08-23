# Activity — Squash or Preserve

*Concept: Squashing collapses a messy branch into one clean commit on main — the work survives, the noise doesn't.*

![Diagram comparing the two ways the same branch can land in history: the messy-feature branch holds three commits (wip, still broken, actually works now); a regular merge delivers all three commits plus a merge commit to main, while squash-and-merge delivers a single clean commit named Add widget feature. The final content is identical either way — only the history differs.](../assets/squash-or-preserve.svg)

## Task

1. In your terminal, inside your practice repository, create a branch and deliberately make three low-quality commits — the kind every programmer actually makes:
   ```bash
   git checkout -b messy-feature
   echo "draft" > widget.txt && git add . && git commit -m "wip"
   echo "draft 2" > widget.txt && git add . && git commit -m "still broken"
   echo "final version" > widget.txt && git add . && git commit -m "actually works now"
   ```
2. Look at the mess you'd be sending to main:
   ```bash
   git log --oneline -3
   ```
3. Squash-merge the branch locally (this is what GitHub's "Squash and merge" button does):
   ```bash
   git checkout main
   git merge --squash messy-feature
   git commit -m "Add widget feature"
   ```
4. Compare histories:
   ```bash
   git log --oneline -3
   ```
   Main received **one** commit. Check `cat widget.txt` — the final content all arrived; the "wip" and "still broken" steps did not.
5. Write one sentence describing a situation where you would want the opposite — a regular merge that preserves every commit.
