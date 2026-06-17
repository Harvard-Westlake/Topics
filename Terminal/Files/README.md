<div align="center">

# Files
*<font color="#8b949e">Creating and editing files from the terminal</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[mkdir — Creating Folders](#mkdir--creating-folders)**  
Making new directories, including nested ones in a single command.

**[touch — Creating Files](#touch--creating-files)**  
Creating empty files instantly from the terminal.

**[vim — Editing Files](#vim--editing-files)**  
Opening, editing, and saving files using vim, including how modes work and the commands you'll use most.

---

## <font color="#388bfd">mkdir — Creating Folders</font>

```bash
mkdir folder-name
```

Creates a new folder in your current directory. To create nested folders all at once, use the `-p` flag:

```bash
mkdir -p projects/week1/code
```

> [!NOTE]
> Without `-p`, the parent folder must already exist. With `-p`, every missing folder in the chain is created automatically.

---

## <font color="#388bfd">touch — Creating Files</font>

```bash
touch filename.txt
```

Creates a new, empty file. If the file already exists, `touch` updates its last-modified timestamp without changing its contents. You can create multiple files at once:

```bash
touch index.html style.css main.js
```

---

## <font color="#388bfd">vim — Editing Files</font>

`vim` is a terminal-based text editor. It opens directly in the terminal — no separate window, no mouse required. Open any file by passing its name:

```bash
vim filename.txt
```

If the file doesn't exist yet, vim creates it when you save.

---

### <font color="#79c0ff">The two modes</font>

Vim works differently from every text editor you've used before. When you open vim, **you cannot type yet**. Vim starts in **Normal mode**, which is for navigation and commands — not typing.

To actually write text, you switch to **Insert mode**.

```
┌──────────────────┐              ┌──────────────────┐
│                  │──── i ──────→│                  │
│   Normal mode    │              │   Insert mode    │
│  navigate &      │←──── Esc ───│   type freely    │
│  run commands    │              │                  │
└──────────────────┘              └──────────────────┘
```

| Mode | What you can do | How to get here |
|---|---|---|
| **Normal** | Navigate, delete, copy, undo, run commands | Press `Esc` from anywhere |
| **Insert** | Type and edit text freely | Press `i` from Normal mode |

> [!IMPORTANT]
> The most common beginner mistake is trying to type while in Normal mode. Always check the bottom of the screen — vim shows `-- INSERT --` when you're in Insert mode and nothing (or `-- NORMAL --`) when you're not.

---

### <font color="#79c0ff">Where to look</font>

Vim shows its current state at the very **bottom of the terminal window**.

```
 1 Hello world
 2
~
~
-- INSERT --                                    3,1   All
```

| Bottom-bar element | Meaning |
|---|---|
| `-- INSERT --` | You are in Insert mode — typing will add text |
| *(blank)* | You are in Normal mode |
| `:` prompt | You typed `:` to start a command (e.g. `:w`, `:q`) |
| `3,1` | Cursor is on line 3, column 1 |
| `All` | The whole file fits on screen |

---

### <font color="#79c0ff">Essential Normal mode commands</font>

You must be in Normal mode (press `Esc` first) before using any of these.

**Saving and quitting**

| Command | What it does |
|---|---|
| `:w` | Save (write) the file |
| `:q` | Quit |
| `:wq` | Save and quit |
| `:q!` | Quit without saving — discards all changes |

**Editing**

| Command | What it does |
|---|---|
| `i` | Enter Insert mode at the cursor |
| `o` | Insert a new line below and enter Insert mode |
| `dd` | Delete the current line |
| `u` | Undo |
| `Ctrl` + `r` | Redo |

**Navigation**

| Key | Moves |
|---|---|
| Arrow keys | One character or line in that direction |
| `gg` | Jump to the top of the file |
| `G` | Jump to the bottom of the file |
| `0` | Jump to the start of the line |
| `$` | Jump to the end of the line |

> [!TIP]
> You can also navigate with `h` `j` `k` `l` (left, down, up, right) — vim's classic keys from before arrow keys existed. They're faster once your fingers know them, but arrow keys work too.

---

### <font color="#79c0ff">A minimal workflow</font>

```bash
vim notes.txt        # open the file
```

Once inside:

1. Press `i` to enter Insert mode
2. Type your text
3. Press `Esc` to return to Normal mode
4. Type `:wq` and press Return to save and exit

---

### <font color="#79c0ff">Where to go next</font>

Vim has a built-in interactive tutorial. Run it from the terminal:

```bash
vimtutor
```

It takes about 30 minutes and teaches everything above plus much more, step by step. Inside vim, `:help` opens the full documentation for any command.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you create a new folder with `mkdir`?
- [ ] Can you create an empty file with `touch`?
- [ ] Can you open a file in vim and exit without saving using `:q!`?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you create a nested folder structure in a single `mkdir -p` command?
- [ ] Can you open vim, type a sentence, save the file, and exit cleanly?
- [ ] Can you switch between Normal and Insert mode without looking at a reference?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you delete a line in vim, undo it, and redo it?
- [ ] Can you explain the difference between `:q`, `:q!`, and `:wq` — and when you would use each?
- [ ] Can you open `vimtutor` and complete the first lesson without quitting early?

---

← [Experiment](../Experiment/) — Back to [Terminal](../)
