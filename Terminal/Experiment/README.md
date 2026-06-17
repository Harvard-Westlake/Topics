<div align="center">

# Experiment
*<font color="#8b949e">Discovering what commands can do with man</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[What is man?](#what-is-man)**  
The built-in manual that documents every command on your system.

**[Reading a Man Page](#reading-a-man-page)**  
The sections every man page follows and what each one tells you.

**[Navigating](#navigating)**  
How to scroll, search, and quit inside a man page.

**[Try it](#try-it)**  
Opening the manual for commands you already know.

---

## <font color="#388bfd">What is man?</font>

`man` stands for **manual**. It opens the built-in documentation for any terminal command — written by the same people who built the command. You don't need an internet connection; it's always available.

```bash
man command
```

For example:

```bash
man ls
```

This opens the full manual for `ls` directly in your terminal.

---

## <font color="#388bfd">Reading a Man Page</font>

Every man page follows the same structure. You don't need to read the whole thing — learn where to look for what you need.

| Section | What it contains |
|---|---|
| **NAME** | The command name and a one-line summary |
| **SYNOPSIS** | The command's full syntax — what options and arguments it accepts |
| **DESCRIPTION** | A detailed explanation of what the command does |
| **OPTIONS** | Every flag listed individually with an explanation |
| **EXAMPLES** | *(when present)* Common usage examples |
| **SEE ALSO** | Related commands worth knowing |

### <font color="#79c0ff">Reading the SYNOPSIS</font>

The SYNOPSIS line uses a shorthand notation:

```
ls [-@ABCFGHILOPRSTUWabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
```

| Notation | Meaning |
|---|---|
| `[-abc]` | These options are optional |
| `[file ...]` | Zero or more file arguments |
| `<file>` | A required argument |

You don't need to memorize the SYNOPSIS — use it as a quick reference when you already know the command and just want to check a specific flag.

---

## <font color="#388bfd">Navigating</font>

Man pages open in a **pager** — a program that lets you scroll through text. The pager used by most systems is called `less`.

### <font color="#79c0ff">Scrolling</font>

| Key | Action |
|---|---|
| `Space` or `f` | Scroll down one full page |
| `b` | Scroll up one full page |
| `j` or `↓` | Scroll down one line |
| `k` or `↑` | Scroll up one line |
| `g` | Jump to the top |
| `G` | Jump to the bottom |

### <font color="#79c0ff">Searching</font>

Press `/` followed by a word, then Return to search:

```
/option
```

Press `n` to jump to the next match, `N` to go backwards.

> [!TIP]
> To jump straight to the OPTIONS section, type `/OPTIONS` and press Return.

### <font color="#79c0ff">Quitting</font>

Press `q` to exit the man page and return to the terminal prompt.

---

## <font color="#388bfd">Try it</font>

Open the manual for each command you've learned so far. For each one, try to find: what the command does (NAME), and at least one option you didn't know about (OPTIONS).

### <font color="#79c0ff">man ls</font>

```bash
man ls
```

`ls` has many more options than `-lsa`. Look for `-R` (recursive), `-t` (sort by time), and `-h` (human-readable sizes).

### <font color="#79c0ff">man pwd</font>

```bash
man pwd
```

Short and simple — a good first man page to read in full.

### <font color="#79c0ff">man mkdir</font>

```bash
man mkdir
```

Look for the `-m` flag, which lets you set folder permissions at creation time.

### <font color="#79c0ff">man touch</font>

```bash
man touch
```

Find the `-t` flag — it lets you set a specific timestamp instead of using the current time.

### <font color="#79c0ff">man cd</font>

```bash
man cd
```

> [!NOTE]
> `cd` is a **shell builtin** — it's built directly into the shell rather than existing as a standalone program. On macOS, `man cd` opens a page called `builtin` that covers many shell builtins at once. Scroll down or search `/cd` to find the `cd` entry specifically.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you open the man page for `ls`?
- [ ] Can you scroll down one page and then back up?
- [ ] Can you quit a man page and return to the terminal prompt?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you jump directly to the OPTIONS section using a search?
- [ ] Can you search for a specific flag inside a man page and jump between matches?
- [ ] Can you explain what the brackets `[ ]` mean in a SYNOPSIS line?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you find a flag in `man ls` that you've never used before and then use it successfully?
- [ ] Can you explain why `man cd` looks different from `man ls`?
- [ ] Can you run `man man` and find out what the numbered sections (1, 2, 3…) refer to?

---

← [Search](../Search/) — Next: [Files](../Files/)
