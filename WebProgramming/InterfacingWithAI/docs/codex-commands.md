<div align="center">

# Codex Commands
*<font color="#8b949e">A slash command is an instruction to Codex itself, typed at its prompt, and a few of them change what the agent is allowed to reach.</font>*

</div>

---

Type `/` at the Codex prompt and this list appears:

![Part of Codex's slash-command list, shown after the receipts Explored, List ls -la, and List from an earlier answer: /keymap remap TUI shortcuts; /vim toggle Vim mode for the composer; /experimental toggle experimental features; /approve approve one retry of a recent auto-review denial; /memories configure memory use and generation; /skills use skills to improve how Codex performs specific tasks, highlighted in blue; /import import setup, this project, and recent chats from Claude Code; and /hooks view and manage lifecycle hooks.](../assets/codex-slash-commands.jpg)

Most commands are conveniences. The ones marked **Risk** change what the agent can reach, what it keeps, or who gets your data. Read those before you press Enter. The list is checked against Codex CLI 0.166 (November 2026) and grows with every release; a command you see that is not here is new, so look it up in the [Codex docs](https://learn.chatgpt.com/docs/codex/cli) before using it.

The one rule that covers most of this page: **an agent with write permission is a program running as you.** Anything it is allowed to do, a confused or hijacked agent can do by mistake. Keep it on the workspace permission level, commit before it edits, and read every approval prompt.

## <font color="#388bfd">Permissions, settings, and status</font>

- `/permissions`: Sets how much Codex may do without asking: look only, edit inside this folder, or do anything. **Risk:** full access removes the sandbox, so a confused agent can delete or overwrite anything your account can, with no undo.
- `/approve`: Lets one action that Codex's automatic reviewer just blocked try again. **Risk:** it was blocked for a reason; you are taking responsibility for a command you may not understand. Read the exact command before you say yes.
- `/memories`: Turns on or off Codex's habit of writing notes about you and your projects that it reads back in future chats. **Risk:** anything you type can be saved to disk and resurface later, including classmates' names, personal details, or a secret you pasted by mistake. Old notes also steer new answers in stale directions.
- `/status`: Shows which account, model, permission level, writable folders, and token usage this session has. Safe, and worth running often.
- `/usage`: Shows how much of your Plus allowance you have spent, and lets you spend a reset if your account has one. **Risk:** a reset is a limited resource; burning one in week one leaves nothing for the project weeks.
- `/config`: Searches and changes Codex's terminal preferences. Safe.
- `/keymap`: Changes which keys do what inside Codex. Safe.
- `/vim`: Makes the typing box behave like the Vim editor. Safe, but confusing if you do not know Vim; run it again to turn it off.
- `/experimental`: Turns on features that are not finished. **Risk:** unfinished features crash, lose chats, and behave in ways nobody has documented. If something strange happens after you turned one on, turn it off first.
- `/setup-default-sandbox`: Windows only: sets up the stronger Windows sandbox, which needs administrator rights. On a PC you run Codex inside WSL for this course, so you should not need it.
- `/debug-config`: Prints where every setting came from, for troubleshooting. Safe; it shows file paths, nothing secret.
- `/ide`: Includes the files open in your editor, and your selected text, in the next prompt. **Risk:** whatever is open gets sent to OpenAI, so close secrets first.

## <font color="#388bfd">Chats and sessions</font>

- `/new`: Starts a fresh chat; Codex forgets this conversation's context (the transcript stays saved). Safe.
- `/clear`: Wipes the screen and starts a fresh chat. Safe.
- `/resume`: Reopens a saved chat where you left off. Safe.
- `/fork`: Copies the current chat into a new one so you can try a different direction without losing this one. Safe.
- `/side` (also `/btw`): Opens a quick side conversation that is thrown away afterward, for a question that should not clutter the main chat. Safe.
- `/rename`: Gives the current chat a name so you can find it later. Safe.
- `/archive`: Puts the session away without deleting it. Safe.
- `/delete`: Permanently deletes the current session transcript. **Risk:** there is no undo, and the record of what the agent did and why is gone with it.
- `/compact`: Squashes the conversation into a summary to free up room. **Risk:** details are lost in the summary, so Codex may forget a constraint you gave earlier. Restate anything important after compacting.
- `/recap`: Writes a summary of the conversation without squashing it. Safe.
- `/goal`: Gives Codex a goal it keeps working toward across turns. **Risk:** an agent pursuing a goal keeps acting and keeps spending allowance after you stop paying attention. Set one only with a clear finish line, and pause it when you leave.
- `/plan`: Switches to plan mode, where Codex thinks and writes a plan but does not change files. Safe, and a good habit before any edit.
- `/agents`: Opens the control center for running several agents at once. **Risk:** more agents means more changes landing at the same time to review, and a faster-draining allowance.
- `/subagents`: Switches between those agents' threads. Same risk as `/agents`.

## <font color="#388bfd">Output, review, and files</font>

- `/copy`: Copies a response, code block, or quote to your clipboard. Safe.
- `/diff`: Shows what has changed in the repository, including new files. Safe; this is how you check the agent's work.
- `/review`: Asks Codex to review the uncommitted changes and point out problems. Safe; it reads, it does not fix.
- `/mention`: Attaches a file to the chat so Codex reads it. **Risk:** the whole file goes to OpenAI. Never attach `.env` files, tokens, or anything with other people's personal data.
- `/export`: Saves the conversation as a Markdown file. Safe; mind where you save it if the chat contains code you should not share.
- `/init`: Writes an `AGENTS.md` file describing your project so Codex starts with context next time. **Risk:** low, but it is a real file in your repository: read it before committing, because if it describes your project wrong, every future session will believe it.
- `/raw`: Switches to plain scrolling output, for copying or when the fancy display misbehaves. Safe.
- `/feedback`: Sends logs to OpenAI's maintainers. **Risk:** logs can include your chat and code. Do not send them from a project you are not allowed to share.

## <font color="#388bfd">Models, tools, and extensions</font>

- `/model`: Picks which model answers and how hard it thinks. **Risk:** the biggest model at high effort can empty a Plus allowance in an afternoon. Stay on the fast and efficient one.
- `/fast`: Turns on Fast mode, which answers quicker. **Risk:** it spends the allowance at two and a half times the normal rate. Leave it off.
- `/daybreak`: Toggles a newer mode OpenAI is rolling out to some accounts; most accounts will not see it. Leave it alone this unit.
- `/voice`: Starts a spoken conversation. **Risk:** turns on your microphone and streams the audio to OpenAI, and everyone near you is in the recording.
- `/apps`: Browses apps Codex can hand tasks to and inserts them into a prompt. **Risk:** each app is another service that receives your prompt and data.
- `/plugins`: Installs and lists plugins that add tools to Codex. **Risk:** a plugin is software from a third party running with your permissions. Install only what the course names.
- `/hooks`: Views and manages hooks: real shell commands that run automatically on events (session start, before and after the agent acts). **Risk:** a hook copied from the internet runs a stranger's script on your laptop every time, with no approval prompt. Treat a hook like a script you have read all the way through.
- `/mcp`: Lists the connected MCP servers, which give Codex tools such as reading your GitHub, Drive, or a database. **Risk:** each one widens what the agent can read and change, and the text a tool returns can carry prompt injection aimed at the agent.
- `/skills`: Browses and uses skills: files of step-by-step instructions the agent follows for a task. **Risk:** a skill from someone else is instructions you did not write, and it can tell the agent to run commands or send data. Read a skill before using it, the way you would before installing software.
- `/presets`: Saves prompts or commands you reuse and runs them. **Risk:** a preset can be a command, so a preset you did not write is a command you did not read.
- `/import`: Copies setup, this project, and recent chats from Claude Code into Codex. **Risk:** old chats may hold private information, classmates' code, and secrets, and you are handing all of it to a second company. It also imports that tool's hooks and instructions.

## <font color="#388bfd">Appearance and terminal</font>

- `/statusline`: Chooses what the footer line shows. Safe.
- `/title`: Chooses what the terminal window title shows. Safe.
- `/theme`: Picks the code-coloring theme. Safe.
- `/pets` (also `/pet`): Shows or hides a small terminal pet. Safe.
- `/tui`: Chooses scrolling or full-screen display for the next launch. Safe.

## <font color="#388bfd">Background work and workspace</font>

- `/ps`: Lists commands Codex is still running in the background and their recent output. Safe.
- `/stop` (also `/clean`): Stops all of those background commands. Safe; use it if something is spinning.
- `/cd`: Moves Codex's working folder. **Risk:** the working folder is the fence. Moving it to your home folder makes everything you own editable.
- `/pwd` (also `/cwd`): Shows which folder Codex is working in. Safe; check it when an answer sounds like the wrong project.
- `/worktree`: Starts the chat in a separate Git worktree so edits do not touch your main checkout. Safe, and a good idea for experiments; it does create extra folders.
- `/daemon`: Controls a background Codex server that keeps running after you close the window. **Risk:** an agent that keeps running when you are not watching. Stop it when you are done.
- `/warnings`: Shows warnings Codex has kept from this session. Safe.
- `/app`: Continues the session in the ChatGPT desktop app. Safe.
- `/logout`: Signs out and deletes the saved login. Safe; you sign in again next time.

## <font color="#388bfd">Leaving</font>

- `/quit` (also `/exit`, or Ctrl+C): Exits Codex. Safe; commit first if the agent edited anything you want to keep.

## <font color="#388bfd">Not a slash command, but the most dangerous switch</font>

- `codex --yolo`, long name `--dangerously-bypass-approvals-and-sandbox`: Starts Codex with no sandbox and no approval prompts at all. **Risk:** every command the agent decides to run, runs, as you, anywhere on the machine. OpenAI's own docs say to use it only inside a throwaway virtual machine. Never on your laptop, never on a school computer.

---

← Back to [lesson](../README.md)
