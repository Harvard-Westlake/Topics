# Activity — Environment Verification

*Concept: Proving the environment tools are installed and accessible from your terminal.*

## Task

1. Open your terminal and run all three of these commands:
   ```bash
   git --version
   java -version
   code --version
   ```
2. Take a screenshot showing all three returning valid version numbers — none of them should say "command not found." (If `code --version` doesn't work, open VS Code, press `Cmd/Ctrl+Shift+P`, and run **Shell Command: Install 'code' command in PATH**, then try again.)
3. In your terminal, prove your SSH key authenticates to GitHub:
   ```bash
   ssh -T git@github.com
   ```
   You should be greeted with `Hi your-username!` — that means your key pair is generated, loaded into ssh-agent, and registered on GitHub.
4. Open GitKraken and confirm your GitHub account is linked — your name or email should show in the bottom toolbar, not a **FREE**-only, signed-out state.
5. Save your screenshot — you may need to submit it.
