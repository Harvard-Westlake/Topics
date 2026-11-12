# Activity - Install Codex and Sign In

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
