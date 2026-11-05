# Activity - Check What Codex May Touch

*Concept: Codex's permission level decides whether a wrong answer is a wrong sentence or a deleted file, so you check the level before you ask it to do anything.*

![A ladder of three rungs. Read only, in green: looks at files and answers questions, nothing is written or run; a wrong answer costs you a wrong sentence. Workspace, in blue and marked "stay here": edits inside the folder it was started in and must stop and ask before leaving that folder, using the network, or running a flagged command; a wrong answer costs you a change you can see with git diff and undo. Full access, in red and marked "never on your laptop": no sandbox and no questions, any file, any command, anywhere, where the --yolo flag starts; a wrong answer costs you deleted files with no undo. A footer says to commit before letting an agent edit because Git is the undo button Codex does not have.](../assets/codex-permission-levels.svg)

## Task

1. In your terminal, go to the Git project repository you built last unit and start Codex there:
   ```bash
   cd ~/HTCS_Projects/YOUR-PROJECT
   codex
   ```
   If Codex asks whether you trust this folder, say yes: it is your own code.
2. Type `/status`. Find the lines that name the approval policy, the sandbox, and the writable roots. The writable roots should be this project folder and nothing wider.
3. Type `/permissions` and read the options. If the selection is not the middle, workspace level (Codex may call it **Auto**), move it there. Never pick the full-access level.
4. Ask Codex, in plain English:
   ```
   Create a file named codex-test.txt in this folder containing the single word hello.
   ```
   Watch what happens: inside the workspace Codex may do it directly or ask first. Run `ls` in your other terminal to confirm the file exists.
5. Now ask it to step outside the fence:
   ```
   Create a file named hello.txt on my Desktop.
   ```
   The Desktop is outside the writable roots, so Codex has to stop and ask for approval. Answer **no**. That pause is the sandbox working.
6. Ask Codex to delete `codex-test.txt`, then run `git status` in your other terminal. The repository should be clean: nothing added, nothing changed.
7. Type `/quit`.
