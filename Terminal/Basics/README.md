<div align="center">

# Terminal Basics
*<font color="#8b949e">Navigating, creating, finding, and reading the manual</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Navigating the File System](#navigating-the-file-system)**  
Understanding paths and moving between folders with `cd` and `pwd`.

**[Listing Contents](#listing-contents)**  
Seeing what is inside a folder with `ls`.

**[Creating Folders and Files](#creating-folders-and-files)**  
Building structure with `mkdir` and `touch`.

**[Finding Files](#finding-files)**  
Locating any file anywhere with `find`.

**[The Manual](#the-manual)**  
Reading built-in command documentation with `man`.

---

## <font color="#388bfd">Navigating the File System</font>

Your computer organizes everything into **files** and **folders**. Folders can contain other folders, forming a tree that starts at the **root**, written as `/`.

<pre>
<strong><font color="#f0883e">/</font></strong>
├── <strong><font color="#f0883e">Users/</font></strong>
│   └── <strong><font color="#f0883e">yourname/</font></strong>
│       ├── Desktop/
│       ├── Documents/
│       └── Downloads/
└── Applications/
</pre>

A **path** is the address of a file or folder. Folders are separated by `/`:

```
/Users/yourname/Documents/homework.txt
```

### <font color="#79c0ff">Two kinds of paths</font>

| Type | Starts with | Example |
|---|---|---|
| **Absolute** | `/` — always from the root | `/Users/yourname/Documents` |
| **Relative** | A name, `.`, or `..` — from where you are now | `Documents/homework.txt` |

### <font color="#79c0ff">pwd — where am I?</font>

```bash
pwd
# /Users/yourname/Documents
```

`pwd` prints your exact current location as an absolute path. Use it any time you feel lost.

### <font color="#79c0ff">cd — move between folders</font>

```bash
cd path
```

| Shortcut | Meaning |
|---|---|
| `.` | Current directory |
| `..` | Parent directory — one level up |
| `../..` | Two levels up |
| `~` | Your home directory, from anywhere |

```bash
cd Documents           # move into Documents
cd ..                  # go up one level
cd ../..               # go up two levels
cd ~                   # go home from anywhere
```

> **Tip:**
> Run `pwd` after every `cd` until you have a clear mental model of where you are.

---

## <font color="#388bfd">Listing Contents</font>

```bash
ls          # list current directory
ls -lsa     # full detail: permissions, size, hidden files, dates
```

| Option | What it adds |
|---|---|
| `-l` | Long format — permissions, owner, size, date |
| `-s` | Size in disk blocks |
| `-a` | Hidden files (names starting with `.`) |

Sample output of `ls -lsa`:

```
total 48
 8 drwxr-xr-x  5 yourname  staff   160 Jun 10 09:00 .
 8 drwxr-xr-x  3 yourname  staff    96 Jun  5 14:22 ..
16 -rw-r--r--  1 yourname  staff  3204 Jun 10 09:00 README.md
 8 -rw-r--r--  1 yourname  staff   512 Jun  9 11:30 notes.txt
```

The `d` at the start of a permissions string means directory; `-` means file.

---

## <font color="#388bfd">Creating Folders and Files</font>

### <font color="#79c0ff">mkdir — make a directory</font>

```bash
mkdir folder-name
```

Use `-p` to create a nested path in one command:

```bash
mkdir -p projects/week1/code
```

> **Note:**
> Without `-p`, every parent folder must already exist. With `-p`, any missing folders are created automatically.

### <font color="#79c0ff">touch — create a file</font>

```bash
touch filename.txt
```

Creates an empty file. If the file already exists, `touch` updates its timestamp without changing its content. You can create multiple files at once:

```bash
touch index.html style.css main.js
```

### <font color="#79c0ff">Editing files — vim</font>

```bash
vim filename.txt
```

Opens a file in the terminal text editor. Vim has two modes: **Normal** (navigate and run commands) and **Insert** (type text). Press `i` to enter Insert mode, `Esc` to return to Normal, and `:wq` to save and quit.

---

## <font color="#388bfd">Finding Files</font>

```bash
find path -name "filename"
```

Searches recursively from `path` for anything matching the name. The `.` path means start here:

```bash
find . -name "notes.txt"          # find notes.txt anywhere below current folder
find ~ -name "*.md"               # find all .md files anywhere in home folder
find . -name "main.*"             # find any file named main with any extension
```

> **Note:**
> The quotes around the filename pattern are important when using wildcards (`*`). Without them the shell may expand the `*` before `find` sees it.

---

## <font color="#388bfd">The Manual</font>

Every command on your system has built-in documentation. Read it with `man`:

```bash
man ls
man mkdir
man find
```

Man pages open in a pager. Key controls:

| Key | Action |
|---|---|
| `Space` | Scroll down one page |
| `b` | Scroll up one page |
| `j` / `k` | Scroll down / up one line |
| `/word` | Search for a word |
| `q` | Quit |

> **Tip:**
> Press `/OPTIONS` then Return to jump straight to the flags section of any man page.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Run `pwd` and read the full path it returns.
- [ ] Create a folder with `mkdir` and a file inside it with `touch`.
- [ ] Open a man page and quit it with `q`.

### <font color="#79c0ff">Intermediate</font>

- [ ] Navigate two levels up from a nested folder in a single `cd` command.
- [ ] Use `find` to locate a file by name from your home directory.
- [ ] Read `ls -lsa` output and identify which entries are files and which are folders.

### <font color="#79c0ff">Advanced</font>

- [ ] Create a nested folder structure three levels deep in a single command.
- [ ] Use `find` with a wildcard to locate all files of a given type.
- [ ] Use `man` to discover a flag for a command you have never used before, then apply it.

---

[Assignment](ASSIGNMENT.md)

← Back to [Terminal](../)
