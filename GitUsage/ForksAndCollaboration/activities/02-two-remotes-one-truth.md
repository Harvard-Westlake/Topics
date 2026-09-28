# Activity — Two Remotes, One Truth

*Concept: A fork has two remotes — origin (your copy, which you can push to) and upstream (the original, which you can only read from).*

![Diagram of a laptop clone tracking two remotes: upstream is the original octocat/Spoon-Knife repository which you can only fetch from — pushing to it is refused for lack of permission — while origin is your own fork, which accepts both push and fetch. A dashed arrow marks that origin was forked from upstream.](../assets/two-remotes-one-truth.svg)

## Task

1. In your terminal, fork `octocat/Spoon-Knife` — GitHub's official practice-fork repo — and clone your fork in one step, then step inside:
   ```bash
   gh repo fork octocat/Spoon-Knife --clone
   cd Spoon-Knife
   ```
2. Still in your terminal, inspect the remotes `gh` configured for you:
   ```bash
   git remote -v
   ```
   You should see four lines: `origin` fetch/push pointing at your account, `upstream` fetch/push pointing at octocat — exactly the two boxes in the diagram. (Had you forked on the website and cloned by hand, `git remote add upstream git@github.com:octocat/Spoon-Knife.git` is the one line that adds the second box.)
3. Fetch from upstream and compare the two remotes' views of main:
   ```bash
   git fetch upstream
   git log origin/main -1 --oneline
   git log upstream/main -1 --oneline
   ```
4. Write one sentence for each remote: which one can you push to, and why?
