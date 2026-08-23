# Activity — Two Remotes, One Truth

*Concept: A fork has two remotes — origin (your copy, which you can push to) and upstream (the original, which you can only read from).*

![Diagram of a laptop clone tracking two remotes: upstream is the original octocat/Spoon-Knife repository which you can only fetch from — pushing to it is refused for lack of permission — while origin is your own fork, which accepts both push and fetch. A dashed arrow marks that origin was forked from upstream.](../assets/two-remotes-one-truth.svg)

## Task

1. On GitHub, fork the repository `octocat/Spoon-Knife` — GitHub's official practice-fork repo.
2. In your terminal, clone **your fork** and step inside:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Spoon-Knife.git
   cd Spoon-Knife
   ```
3. Still in your terminal, wire up the second remote and inspect both:
   ```bash
   git remote add upstream https://github.com/octocat/Spoon-Knife.git
   git remote -v
   ```
   You should see four lines: `origin` fetch/push pointing at your account, `upstream` fetch/push pointing at octocat — exactly the two boxes in the diagram.
4. Fetch from upstream and compare the two remotes' views of main:
   ```bash
   git fetch upstream
   git log origin/main -1 --oneline
   git log upstream/main -1 --oneline
   ```
5. Write one sentence for each remote: which one can you push to, and why?
