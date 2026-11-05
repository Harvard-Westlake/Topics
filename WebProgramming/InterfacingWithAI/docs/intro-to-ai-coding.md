<div align="center">

# Intro to AI Coding
*<font color="#8b949e">AI coding means you decide what gets built and check every result, while the AI does the typing.</font>*

</div>

---

This lesson takes two class days. Day 1 puts an AI agent, OpenAI's **Codex CLI**, into your terminal and teaches you what it is allowed to touch. Day 2 is about managing Codex CLI, or any AI that writes code for you: the assumptions it makes, and the loop that keeps you in charge.

## <font color="#388bfd">Table of Contents</font>

1. [Day 1: Codex in your terminal, signed in to ChatGPT Plus on a model that lasts the month](#day-1-codex-in-your-terminal)
2. [What Codex may touch: permissions, the real dangers, and the risky commands](#what-codex-may-touch)
3. [Interview your repository: the first prompt is the folder you start in](#interview-your-repository)
4. [Day 2: assumptions, what the AI decides when you do not](#day-2-assumptions)
5. [Ask, Plan, and Agent: picking the right way to run Codex CLI](#ask-plan-and-agent)
6. [The manager's loop for building any feature](#the-managers-loop)

## <font color="#388bfd">Day 1: Codex in Your Terminal</font>

So far you have used AI through a chat window: you paste, it answers, you copy. **Codex** is a program that lives in your terminal. You start it inside a folder, it reads what is there, and it can run commands and change files when you let it. Today it only reads and explains.

**Install it.** The install is one line, from the [Codex getting-started page](https://learn.chatgpt.com/docs/codex/cli#getting-started):

![The Install Codex step from the Codex documentation: a tab bar offering macOS/Linux, Windows, npm, and Homebrew with macOS/Linux selected, the sentence "Install the Codex CLI with the standalone installer for macOS and Linux", and two code boxes, Install Codex and Update Codex, both holding the same command: curl -fsSL https://chatgpt.com/codex/install.sh piped into sh.](../assets/codex-install-docs.png)

In your terminal (on a Mac, Terminal; on a PC, the Ubuntu terminal you use for every other command in this course, where the macOS/Linux installer is the right one), run:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

![Terminal output of the installer, typed at a zsh prompt inside a folder named MyWebsite: Installing Codex CLI; Detected platform: macOS (Apple Silicon); Resolved version: 0.166.0; Downloading Codex CLI; Installing standalone package to the .codex/packages/standalone/releases folder in the home directory; a WARNING that it could not safely inspect old Codex releases and skipped the remaining cleanup; a note that .local/bin is already on PATH; Current terminal: codex; Future terminals: open a new terminal and run: codex; Codex CLI 0.166.0 installed successfully; and the prompt Start Codex now? [y/N] with the cursor waiting.](../assets/codex-install-output.jpg)

Type `y` to start it. The `WARNING` about old releases is harmless on a first install. From now on you start Codex by typing `codex` in a new terminal, and the same `curl` line updates it later. `codex --version` proves the install worked; if the shell says `command not found`, open a new terminal window.

**Sign in with ChatGPT Plus.** The first time Codex starts it asks how you want to use it:

![Codex's first-run menu titled "Choose how you want to use Codex", listing 1. Sign in with ChatGPT (Usage included with Plus, Pro, Business, and Enterprise plans), 2. Sign in with Device Code (Sign in from another device with a one-time code), 3. Use an OpenAI API key (Pay for what you use), and 4. Use Amazon Bedrock (Connect using your AWS credentials). Option 1 is selected and the footer reads Press enter to continue.](../assets/codex-sign-in-menu.jpg)

Leave **1. Sign in with ChatGPT** selected and press Enter. A browser tab opens on chatgpt.com. Log in, or create an account. If ChatGPT asks you to verify your age, use your real birthday and finish the check; Codex waits until it is done. Then upgrade the account to **ChatGPT Plus** ($20 per month, the plan that includes Codex) and pay with the class card written on the board. Back in the terminal, `/status` shows your account and plan. If you upgraded after logging in and Codex says the plan does not include it, type `/logout`, run `codex`, and sign in again.

> **Warning:** The class card goes into the ChatGPT payment form once and nowhere else: not a file, not a chat, not a commit, not a message to a friend. Everything you type into Codex is sent to OpenAI and may be kept.

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Install Codex and Sign In</strong></summary>

*Concept: Codex is a program on your laptop that borrows your ChatGPT account, so the install and the sign-in are two separate steps and each one can be checked.*

![Three boxes left to right. Your terminal: the curl install command, "Start Codex now? y", then choosing "1. Sign in with ChatGPT". Your browser on chatgpt.com: log in or create an account, verify your age if asked, upgrade to Plus for $20 a month, pay with the class card on the board. Back in the terminal: signed in, the prompt appears, /status shows account, plan Plus, and model, and codex --version proves the install. A red footer says the card goes into the browser's payment form once and never into a file, a chat, or a commit.](../assets/codex-sign-in-flow.svg)

## Task

1. In your terminal (on a PC, the Ubuntu terminal you use for every other command in this course), run the installer:
   ```bash
   curl -fsSL https://chatgpt.com/codex/install.sh | sh
   ```
   When it ends with `Start Codex now? [y/N]`, type `y` and press Enter.
2. Codex asks how you want to use it. Leave **1. Sign in with ChatGPT** selected and press Enter. A browser tab opens on chatgpt.com.
3. In the browser, log in to ChatGPT or create an account. If ChatGPT asks you to verify your age, complete that step with your real birthday. Codex will not continue until the check is done.
4. Still in the browser, upgrade the account to **ChatGPT Plus** ($20 per month) using the class card written on the board. Type the card number into the ChatGPT payment form and nowhere else.
5. Return to the terminal. Codex now shows its prompt. Type `/status` and press Enter: the account line should name your ChatGPT login and say Plus. If it says your plan does not include Codex, type `/logout`, run `codex` again, and sign in a second time so it picks up the upgrade.
6. Open a second terminal window and run `codex --version`. Write the version number down; the assignment stencil asks for it.
7. Back in the Codex window, type `/quit` to leave.

*(Standalone file: [activities/01-install-codex-and-sign-in.md](../activities/01-install-codex-and-sign-in.md))*

</details>

**Pick a model that lasts the month.** Plus does not give you unlimited Codex. It gives you a **usage allowance** that refills on a schedule, and every answer spends some of it. OpenAI's pricing page lists its smallest model as allowing roughly ten to sixty times more messages per period than its largest, and says reasoning effort, long chats, and tool use spend the allowance faster too. A big model at high effort is gone in an afternoon. A small one lasts the month, which is how long this unit needs it.

![Codex's model picker titled "Select Model and Effort", listing 1. GPT-6-Luna, fast and affordable model for easier tasks; 2. GPT-5.6-Terra, older balanced model for straightforward work; and 3. GPT-5.6-Luna, older fast and efficient model. Row 3 is highlighted in blue, and the footer reads enter select, esc back.](../assets/codex-model-picker.png)

Type `/model`, choose **GPT-5.6-Luna** (the entry described as "Older fast and efficient model"), and pick the lowest reasoning effort if Codex asks for one. The names change with every release; the rule does not: pick the one described as fast, efficient, or affordable, never the one with the biggest number. `/status` shows the active model, and Codex remembers your choice. Leave Fast mode (`/fast`) off: it spends the allowance at two and a half times the normal rate.

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Pick a Model That Lasts the Month</strong></summary>

*Concept: Which model you choose is a budget decision: the same Plus allowance runs dry in days on a big model and lasts the month on a small one.*

![Two horizontal bars across a four-week axis. The top bar, labeled biggest model at high effort, is filled red only for the first part of week one and then reads "allowance gone, locked out until it resets". The bottom bar, labeled GPT-5.6-Luna at low effort, is filled green across all four weeks and reads "still answering in week 4, the whole unit". A footer notes that model choice, reasoning effort, long chats, tool use, and Fast mode at 2.5 times all spend the allowance faster, and that /usage shows what is left.](../assets/codex-usage-budget.svg)

## Task

1. In your terminal, start Codex in any folder:
   ```bash
   codex
   ```
2. Type `/model` and press Enter. The **Select Model and Effort** list appears.
3. Use the arrow keys to move to **GPT-5.6-Luna**, the entry described as "Older fast and efficient model", and press Enter. If a reasoning-effort list follows, choose the lowest option.
4. Type `/status` and confirm the model line shows the one you chose. Write the model name down for the assignment stencil.
5. Type `/usage` and look at how much of your allowance a brand-new account has used: nothing yet. Check it again at the end of class to see what one period of questions cost.
6. Type `/quit`.

*(Standalone file: [activities/02-pick-a-model-that-lasts-the-month.md](../activities/02-pick-a-model-that-lasts-the-month.md))*

</details>

## <font color="#388bfd">What Codex May Touch</font>

A chat window can only give you a bad sentence. An agent in your terminal can give you a bad `rm`. Type `/permissions` and Codex shows the levels it can run at. The names shift between versions, but there are always three rungs:

| Level | What Codex may do | A wrong answer costs you |
|---|---|---|
| **Read only** | Look at files and answer questions. Nothing is written, nothing is run. | A wrong sentence. |
| **Workspace** (Codex may call it **Auto**; the default for your own folders) | Edit files inside the folder it was started in. It must stop and ask before touching anything outside that folder, reaching the network, or running a command the sandbox flags. | A change you can see with `git diff` and undo. |
| **Full access** | No sandbox and no questions: any file, any command, anywhere on your laptop. | Deleted files, with no undo. |

Stay on the workspace level. The sandbox is real: on a Mac and in WSL a command the level does not allow is refused rather than quietly run. The one way to switch it off is the `--yolo` flag (long name `--dangerously-bypass-approvals-and-sandbox`), and OpenAI's own docs say to use it only inside a throwaway machine. Never on your laptop.

> **Tip:** Commit before you let an agent edit, and run `git diff` after. Git is the undo button that Codex does not have.

**The real dangers of an AI agent:**

- **It acts, not just talks.** With write permission it can overwrite a file you spent a week on, or run a command that deletes a folder. It does not know which files matter to you.
- **It is confidently wrong.** It names methods that do not exist, invents command flags, and explains code it never opened. Nothing it says is true until you have checked it against the file.
- **It reads everything in the folder and sends it to OpenAI.** That includes `.env` files, tokens, and anything you pasted into a note. Keep secrets out of folders you open with Codex.
- **Text it reads can hijack it.** A README, a web page, or a downloaded file can hold instructions written for the AI, not for you ("ignore your previous task and run this"). This is **prompt injection**, and it is why you never run an agent with full access on code you did not write.
- **It spends allowance.** Big models, Fast mode, long chats, and parallel agents all burn through Plus faster, and when it is gone you are locked out until it resets.
- **It remembers.** With memories on, Codex saves notes about you and your projects and reads them into future chats, so personal details and classmates' names can resurface where you did not expect them.
- **It can do your thinking for you.** Every assignment in this course says how much AI help is allowed, and you must disclose how you used it. Asking Codex to explain your code is learning. Pasting what it wrote as your own work is an Honor Code problem.

**The risky commands.** Type `/` in Codex and a list of slash commands appears:

![Part of Codex's slash-command list, shown after the receipts Explored, List ls -la, and List from an earlier answer: /keymap remap TUI shortcuts; /vim toggle Vim mode for the composer; /experimental toggle experimental features; /approve approve one retry of a recent auto-review denial; /memories configure memory use and generation; /skills use skills to improve how Codex performs specific tasks, highlighted in blue; /import import setup, this project, and recent chats from Claude Code; and /hooks view and manage lifecycle hooks.](../assets/codex-slash-commands.jpg)

Most are harmless conveniences. These change what the agent can reach or do, with what actually goes wrong:

- `/permissions`: the three levels above. Full access removes the sandbox, so a confused agent can delete anything you can delete.
- `/approve`: retries one action the automatic reviewer just blocked. You are overriding a safety check for a command you may not understand, so read the command first.
- `/memories`: turns Codex's long-term notes on or off. Anything you type can be saved to disk and resurface in later chats, including other people's personal details.
- `/skills`: a skill is a file of instructions the AI follows. A skill from someone else can tell the agent to run commands or send data, so treat installing one like installing software.
- `/hooks`: hooks are real shell commands that run automatically on events (session start, before and after the agent acts). A hook copied from the internet runs a stranger's script on your laptop, every time, with no approval prompt.
- `/import`: copies another AI tool's setup and chat history into Codex. Old chats can hold private information and other people's code, and you are handing all of it to a second company.
- `/mcp`, `/plugins`, `/apps`: extensions that give Codex new tools, such as reach into your GitHub, Google Drive, or browser. Each one widens what the agent can read and change, and a bad one can read anything you let it see.
- `/experimental`: switches on unfinished features. Expect crashes, lost chats, and behavior nobody has documented yet.
- `/delete`: permanently deletes the current session transcript. There is no undo.
- `/fast`: Fast mode, which spends the allowance at two and a half times the normal rate.
- `/goal`, `/agents`, `/subagents`: set a goal the agent keeps pursuing on its own, or run several agents at once. More autonomy means more changes to review and a faster-draining allowance.
- `/cd`: moves the agent's working folder. Moving it to your home folder makes everything you own the workspace.
- `/voice`: turns on your microphone and streams the audio to OpenAI.

Every command, including the cosmetic ones, gets one plain sentence in the [Codex commands reference](codex-commands.md).

### <font color="#79c0ff">Activity 3</font>
<details>
<summary><strong>Check What Codex May Touch</strong></summary>

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

*(Standalone file: [activities/03-check-what-codex-may-touch.md](../activities/03-check-what-codex-may-touch.md))*

</details>

## <font color="#388bfd">Interview Your Repository</font>

Codex answers about the folder it was started in. Start it on your Desktop and it will tell you about your Desktop. So the first prompt is the `cd`:

```bash
cd ~/HTCS_Projects/YOUR-PROJECT
codex
```

If Codex asks whether you trust this folder, say yes for a folder that holds your own code, and no for anything you downloaded.

The Codex docs suggest the first question: **"Tell me about this project."** While it works, it prints what it is doing (`Explored`, `List`, `Read`, file names). Those lines are the receipts: they show which files it actually opened before it answered. An answer that arrives with no receipts was written from the file names alone.

Good questions for your Git project:

- "Which file does most of the work? Walk me through it from the top."
- "Which method computes the SHA-1 hash of a blob, and exactly what bytes go into the hash?"
- "What does the most recent commit change?"
- "What is one thing you would change in this code, and why?"

After every answer that names a file, open the file. Checking is not an insult to the tool; it is the only way to find out when it is wrong. Today Codex only reads: if it asks for approval to edit something, answer no.

> **Note:** `/init` asks Codex to write an `AGENTS.md` file describing your project so it has a head start next time. It is a real file in your repository. Read it before you commit it.

### <font color="#79c0ff">Activity 4</font>
<details>
<summary><strong>Interview Your Repository</strong></summary>

*Concept: Codex only knows the folder it was started in, so starting it in the right place is the first prompt, and checking its answers against the files is the last.*

![Left, a folder box for ~/HTCS_Projects/YOUR-PROJECT listing README.md, src/Blob.java, src/Tree.java, src/Commit.java, and .git/, captioned "you typed: cd here, then codex". An arrow labeled reads points to a Codex box showing its receipts: Explored, List ls -la, Read Blob.java. An arrow labeled answers points to the exchange: you ask which file hashes a blob, Codex answers Blob.java, sha1 over "blob size null byte" plus the bytes, and you open Blob.java to check it. A red footer warns that started on your Desktop it will confidently describe your Desktop, and a grey one that no receipts means an answer written from the file names alone.](../assets/codex-reads-your-repo.svg)

## Task

1. In your terminal, start Codex inside your Git project repository:
   ```bash
   cd ~/HTCS_Projects/YOUR-PROJECT
   codex
   ```
2. Ask the opening question the Codex docs suggest:
   ```
   Tell me about this project. What does it do, and which file does most of the work?
   ```
   Watch the lines it prints while it works (`Explored`, `List`, `Read`, file names). Those are the files it opened before answering.
3. Ask something only a reader of the code could answer, for example:
   ```
   Which method computes the SHA-1 hash of a blob, and exactly what bytes go into the hash?
   ```
4. Open the file it named in VS Code and check the claim line by line. Write down one thing it got right and one thing it got wrong, vague, or invented. If everything checks out, ask a harder question until something does not.
5. Ask for an opinion:
   ```
   What is one thing you would change in this code, and why?
   ```
   Decide whether you agree. Do not let it make the change today: if it asks for approval to edit, answer no.
6. Type `/quit`.

*(Standalone file: [activities/04-interview-your-repository.md](../activities/04-interview-your-repository.md))*

</details>

## <font color="#388bfd">Day 2: Assumptions</font>

![Two ideas side by side. On the left, every prompt is what you said, for example "a quiz page about the heart", plus what you left out, such as colors, layout, how many questions, and what happens on a wrong answer; the AI decides those for you. On the right, the manager's loop: 1 Ask, 2 Plan, 3 Agent, 4 Test, then back to Ask for the next small piece. Test means the browser and the console, not the AI saying it works. The AI writes drafts; your name is on the commit.](../assets/ai-coding-loop.svg)

You already know HTML, CSS, JavaScript, hosting, and Firestore. Now you get a very fast assistant:

- **The AI fills every gap** you leave in a prompt with its own guess.
- **You are the manager:** you plan, you choose, and you check.
- **Work in small pieces** and test each one in the browser before asking for the next.

When you ask an AI for something, everything you **do not** say gets filled in for you. Ask for "a website about dogs" and the AI silently picks the colors, the layout, the tone, the breed in the photos, and whether there is a navigation bar. Those choices are **assumptions**: gaps in your prompt that the AI covers with its own defaults.

| If you don't manage assumptions | If you do |
|---|---|
| Two people with the "same" idea get completely different results. | You can predict and repeat what you get. |
| The AI's choices quietly replace yours. | Your intent survives the trip through the AI. |
| You can't tell a bug from a guess. | You know what you specified and what you left open. |

You could never specify everything. The skill is knowing which decisions you care about, stating those, and leaving the rest open on purpose.

## <font color="#388bfd">Ask, Plan, and Agent</font>

Codex CLI has three ways to run, and choosing one is a management decision:

| Way to run | How you get it | What it does | Use it when |
|---|---|---|---|
| **Ask** | `/permissions` on the read-only level | Answers questions about your code. Changes nothing. | You want to **understand** what to do. |
| **Plan** | `/plan` | Researches your files and writes a step-by-step plan for you to edit and approve, without touching a file. | You want to **decide how** it gets built. |
| **Agent** | `/permissions` on the workspace level, Day 1's default | Edits files and runs commands to carry out the work, inside the folder it was started in. | You know what you want and are ready to **hand off the typing**. |

Two more tools keep you in charge:

- **Context:** type `@` and start typing a file name to point Codex CLI at the exact files it should read, instead of letting it guess.
- **Rules:** the `AGENTS.md` file in your repository (`/init` writes the first draft) states your standing decisions once, like "use the learnhw styles" or "no frameworks", so you do not repeat them in every prompt.

> **Warning:** AI makes mistakes and then confidently insists it is right. It will say code works that was never run, and "fix" one bug by breaking something else. Check results in the browser and the console, never in the chat window.

## <font color="#388bfd">The Manager's Loop</font>

Build every feature the same way:

1. **Ask** (read only) until you can describe the feature precisely in plain English.
2. **Plan** (`/plan`) the pieces: which files, which functions, which events, what data goes to Firestore.
3. **Agent** (workspace level) one piece at a time, small enough to test right away. Commit before each Agent step so you can always go back, and read `/diff` after it.
4. **Test** in the browser with the console open. Have the AI fix what is actually broken, not what it claims is broken.

Managers who skip straight to Agent get code they do not understand, solving a problem they never defined.

---

← Back to [lesson](../README.md)
