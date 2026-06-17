<div align="center">

# Terminal
*<font color="#8b949e">An introduction to the command line</font>*

<font color="#a371f7">Learning</font>

</div>

---

A terminal is a text-based interface for talking directly to your computer. Instead of clicking icons, you type instructions — called **commands** — and press Return to run them. The program that reads your commands and runs them is called a **shell**.

---

## <font color="#388bfd">Anatomy of a command</font>

Every terminal command follows the same structure:

```
command  -options  argument
```

| Part | Role | Example |
|---|---|---|
| **command** | The program to run | `ls` |
| **options** | Flags that change how the command behaves | `-la` |
| **argument** | The file or folder to act on | `Documents/` |

Put together:

```bash
ls -la Documents/
```

This tells `ls` (list) to show all files (`-a`) in long format (`-l`) inside the `Documents/` folder.

> [!NOTE]
> Options always start with a dash (`-`). You can stack multiple options behind one dash — `-la` is the same as `-l -a`.

---

## <font color="#388bfd">Running a command</font>

1. Type your command at the prompt
2. Press **Return** to execute it
3. Read any output the terminal prints
4. A new prompt appears — the terminal is ready for the next command

---

## <font color="#388bfd">The prompt</font>

The blinking cursor sits after a **prompt**, which typically looks like:

```
yourname@computer ~ %
```

| Part | Meaning |
|---|---|
| `yourname` | Your user account |
| `computer` | Your machine's name |
| `~` | Your current location (here, your home folder) |
| `%` or `$` | The shell is ready for input |

The `~` is shorthand for your **home directory** — the folder that belongs to your account. You'll see it constantly as you navigate.

---

## <font color="#388bfd">Lessons</font>

| # | Lesson | What you'll learn |
|---|---|---|
| 1 | [Navigation](Navigation/) | Moving between folders with `cd` and understanding paths |
| 2 | [Search](Search/) | Listing folder contents with `ls` and its options |
| 3 | [Experiment](Experiment/) | Exploring command documentation with `man` |
| 4 | [Files](Files/) | Creating files with `mkdir` and `touch`, editing with `vim` |

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you open a terminal on your computer?
- [ ] Can you identify the three parts of a command: command, options, and argument?
- [ ] Can you run `ls` and see output appear?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you read the prompt and identify what the `~` symbol means?
- [ ] Can you run a command that uses both an option and an argument at the same time?
- [ ] Can you explain the difference between a command and an option in your own words?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you predict what `ls -la Documents/` will do before running it?
- [ ] Can you explain what the shell is and how it differs from the terminal window itself?
- [ ] Can you describe what happens between pressing Return and seeing the next prompt?
