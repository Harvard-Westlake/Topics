# Activity — Clone vs. ZIP Challenge

*Concept: A cloned repository is a living thing with history attached; a downloaded ZIP is a dead snapshot with none.*

## Task

1. Go to [github.com/octocat/Hello-World](https://github.com/octocat/Hello-World) — GitHub's own tiny demo repository.
2. Click **Code → Download ZIP**. Extract the ZIP into a folder named `dead-repo`.
3. In your terminal, clone the same repository into a folder named `live-repo`:
   ```bash
   git clone https://github.com/octocat/Hello-World.git live-repo
   ```
4. Open a terminal inside `dead-repo` and run:
   ```bash
   git status
   git log
   ```
   Write down the exact error each command gives you.
5. Now open a terminal inside `live-repo` and run the same two commands:
   ```bash
   git status
   git log
   ```
   Write down what each one shows you this time.
6. Compare your two write-ups. `dead-repo` has no `.git` folder at all — it's just files, disconnected from GitHub, with none of its own history. `live-repo` carries the entire project history and already knows where it came from.
