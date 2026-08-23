<div align="center">

# Initial Install
*<font color="#8b949e">Setting up your terminal environment and developer tools</font>*

<font color="#3fb950">Environment Configuration</font>

</div>

---

This lesson gets your machine ready for the rest of the course. Mac and PC take different paths to the same destination — a Unix terminal with Git, GitKraken, VS Code, and Java 25.

Choose your operating system and follow the steps in order.

> **Important:**
> Complete this before starting the Terminal lessons. Every lesson from here on assumes you have a working Unix terminal with Git installed.

👉 <details>
<summary><h3>Activity: Environment Verification — click to expand</h3></summary>

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

*(Standalone file: [activities/01-environment-verification.md](activities/01-environment-verification.md))*

</details>

---

## <font color="#388bfd">Table of Contents</font>

1. [Pick Mac or PC and follow the matching setup guide](#choose-your-operating-system)
2. [Understand pwd and the difference between absolute and relative paths](#where-am-i-understanding-pwd-and-paths)
3. [Learn the four commands that drive the terminal — pwd, mkdir, cd, and cd ..](#driving-the-terminal-your-first-four-commands)
4. [Compare the finished Mac and PC environments side by side](#what-youll-have-when-youre-done)
5. [Check your understanding and try the stretch goals](#check-for-understanding)

---

## <font color="#388bfd">Choose your operating system</font>

**[Mac](Mac.md)**  
Open Terminal, install Homebrew and Git, connect to GitHub with an SSH key, set up GitKraken and VS Code, and install Java 25.

**[PC](PC.md)**  
Install WSL and Ubuntu to get a Unix terminal, then install Git, connect to GitHub with an SSH key, and set up GitKraken, VS Code, and Java 25.

---

## <font color="#388bfd">Where Am I? Understanding pwd and Paths</font>

When you open a GUI (Graphical User Interface) like Finder or File Explorer, you can physically see what folder you are in. When you open a terminal, you are flying blind.

To find out where you are, you type `pwd` (**p**rint **w**orking **d**irectory). The terminal spits back a text string showing your exact location on the hard drive. Understanding how to navigate this system comes down to mastering two concepts: **absolute** and **relative** paths.

### <font color="#79c0ff">The absolute path (the GPS coordinate)</font>

An absolute path is the full, undeniable address of a file. It always starts from the absolute root of your computer (represented by a `/` on Mac/Unix or a `C:\` on Windows).

```
/Users/andrew/Documents/homework/File.java
```

Think of it like "123 Main Street, Los Angeles, CA 90001." No matter where you are in the world, this address gets you to the exact same building.

### <font color="#79c0ff">The relative path (the local directions)</font>

A relative path is an address that assumes a starting point based on where you currently are (your `pwd`). It does not start with a root slash.

```
homework/File.java
```

Think of it like "take a left out the front doors and it's the second building on the right." These directions only work if you are standing in the correct starting location. If you are at school, you'll find a coffee shop. If you try those same directions at home, you'll walk into your neighbor's living room.

> **Note:**
> When programming, relative paths are usually better — if you send your project folder to a teammate, their user folder is going to be named differently than yours. A relative path ensures the code still finds the files inside the project folder no matter whose computer it's on.

👉 <details>
<summary><h3>Activity: The Path Finder — click to expand</h3></summary>

*Concept: Experiencing the strict difference between absolute and relative paths in code.*

## Task

1. On your Desktop, create a new folder called `path-activity`. Inside it, create three files:
   - `PathFinder.java` (paste the code below into it)
   - `absolute.txt` containing exactly: `I am absolute!`
   - `relative.txt` containing exactly: `I am relative!`
2. Open `PathFinder.java` and update the `absolutePath` string so it matches your own computer's real path to `absolute.txt` (see the comments in the code for examples).
3. Compile and run the program from inside `path-activity`:
   ```bash
   cd path-activity
   javac PathFinder.java
   java PathFinder
   ```
   Both reads should print `SUCCESS`.
4. Now run the program again from *outside* the folder:
   ```bash
   cd ..
   java -cp path-activity PathFinder
   ```
   Watch what happens: the absolute path still succeeds, but the relative path fails — because `relative.txt` is no longer sitting where the terminal's `pwd` is looking.
5. In your own words, write one sentence explaining why the absolute path survived the move but the relative path didn't.

**Code for `PathFinder.java`:**

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class PathFinder {
    public static void main(String[] args) {
        // 1. ABSOLUTE PATH (change this to match your actual computer's path!)
        // Mac/Linux example: "/Users/yourname/Desktop/path-activity/absolute.txt"
        // Windows WSL example: "/mnt/c/Users/yourname/Desktop/path-activity/absolute.txt"
        String absolutePath = "/Users/REPLACE_ME/Desktop/path-activity/absolute.txt";

        System.out.println("--- Reading Absolute Path ---");
        try (BufferedReader br = new BufferedReader(new FileReader(absolutePath))) {
            System.out.println("SUCCESS: " + br.readLine());
        } catch (IOException e) {
            System.out.println("FAIL: Could not find the absolute file. Did you update the path string?");
        }

        // 2. RELATIVE PATH (looks for the file exactly where the terminal is currently sitting)
        String relativePath = "relative.txt";

        System.out.println("\n--- Reading Relative Path ---");
        try (BufferedReader br = new BufferedReader(new FileReader(relativePath))) {
            System.out.println("SUCCESS: " + br.readLine());
        } catch (IOException e) {
            System.out.println("FAIL: Could not find the relative file. Are you in the right folder?");
        }
    }
}
```

*(Standalone file: [activities/02-the-path-finder.md](activities/02-the-path-finder.md))*

</details>

---

## <font color="#388bfd">Driving the Terminal: Your First Four Commands</font>

The terminal you just installed is driven by typed commands instead of clicks. Four commands are your steering wheel — everything else in this course builds on them. These are vocabulary: know each one by name, by what it stands for, and by what it does.

| Command | Stands for | What it does |
|---|---|---|
| `pwd` | **p**rint **w**orking **d**irectory | Shows the folder your terminal is standing in right now |
| `mkdir name` | **m**a**k**e **dir**ectory | Creates a new folder called `name` inside your current location |
| `cd name` | **c**hange **d**irectory | Steps *into* the folder called `name` |
| `cd ..` | change directory, up | Steps *out* to the parent folder (`..` always means "one level up") |

Here is a complete round trip — notice how `pwd` is used between every move to confirm where you are, the same way you'd check a map after each turn:

```bash
pwd                 # /Users/you            ← starting point
mkdir practice      # a new folder appears here
cd practice         # step inside it
pwd                 # /Users/you/practice   ← the path grew by one folder
cd ..               # step back out
pwd                 # /Users/you            ← right back where you started
```

> **Tip:**
> Make `pwd` a reflex. The single most common terminal mistake is running a command in the wrong folder — and it costs one three-letter command to rule that out. When in doubt, `pwd` it out.

---

## <font color="#388bfd">What you'll have when you're done</font>

| | Mac | PC |
|---|---|---|
| Unix terminal app | Terminal.app | Ubuntu (WSL) |
| Shell | zsh | bash |
| Package manager | Homebrew | apt |
| Version control | Git | Git |
| GitHub authentication | SSH key (ed25519) + ssh-agent | SSH key (ed25519) + ssh-agent |
| Visual Git client | GitKraken | GitKraken |
| Code editor | VS Code | VS Code |
| Language runtime | Java 25 LTS | Java 25 LTS |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] I can successfully open a Unix terminal on my computer.
- [ ] I can run `git --version`, `java -version`, and `code --version` without seeing "command not found" errors.
- [ ] I have linked GitKraken and my terminal environment to my GitHub account.
- [ ] I have generated an ed25519 SSH key pair, loaded it into ssh-agent, added the public key to GitHub, and confirmed `ssh -T git@github.com` greets me by username.
- [ ] I can explain which half of my SSH key pair is allowed to leave my machine, and why.
- [ ] I can explain what `pwd` stands for and how to use it to orient myself in the terminal.
- [ ] I can navigate the terminal with the four core commands — `pwd`, `mkdir`, `cd folder`, and `cd ..` — checking my location with `pwd` after each move.
- [ ] I can articulate why a relative path will break if the terminal is executing a program from the wrong directory.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] **The Profile Hacker:** Use the terminal to configure your global Git variables (`git config --global user.name` and `user.email`). Then use `git config --list` to verify them.
- [ ] **The Explorer:** Use the `cd` (change directory) command to navigate your terminal to the root of your hard drive (`cd /`), use `ls` to look around, and then use `cd ~` to get back to your home folder.

---

[Assignment](ASSIGNMENT.md)

← Back to [Computer Setup](../)
