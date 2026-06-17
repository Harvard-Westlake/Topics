<div align="center">

# Navigation
*<font color="#8b949e">Moving between folders and understanding paths</font>*

<font color="#a371f7">Learning</font>

</div>

---

To move between folders in the terminal, you use the `cd` command — short for **change directory**.

---

## <font color="#388bfd">Table of Contents</font>

**[File System — Overview](#file-system--overview)**  
How files and folders are organized on your computer as a nested tree of folders and files.

**[Path](#path)**  
The address system the terminal uses to locate any file or folder, and the difference between absolute and relative paths.

**[pwd — Where Am I?](#pwd--where-am-i)**  
The command for printing your exact current location in the file system.

**[cd — Changing Directories](#cd--changing-directories)**  
The command for moving between folders, special shortcut symbols, and how to read your current location.

---

## <font color="#388bfd">File System — Overview</font>

Your computer organizes everything into **files** and **folders** (also called *directories*). Folders can contain other folders, creating a nested hierarchy — like a tree.

```
📁 Users/
└── 📁 yourname/
    ├── 📁 Desktop/
    │   └── 📄 todo.txt
    ├── 📁 Documents/
    │   ├── 📄 homework.txt
    │   └── 📁 projects/
    │       ├── 📄 main.py
    │       └── 📄 notes.md
    └── 📁 Downloads/
        └── 📄 setup.dmg
```

| Symbol | Meaning |
|---|---|
| `📁` | Folder (directory) — contains other files and folders |
| `📄` | File — holds actual content (text, code, images, etc.) |

The entire tree has a single starting point at the very top called the **root**, written as `/`. Everything on your computer lives somewhere inside it.

---

## <font color="#388bfd">Path</font>

A **path** is an address that tells the terminal exactly where a file or folder lives. Folders are separated by `/`:

```
/Users/yourname/Documents/homework.txt
```

The tree below traces this path — each **bold** step is a folder you pass through to reach `homework.txt`:

<pre>
<strong><font color="#f0883e">/</font></strong>
├── <strong><font color="#f0883e">Users/</font></strong>
│   └── <strong><font color="#f0883e">yourname/</font></strong>
│       ├── Desktop/
│       ├── <strong><font color="#f0883e">Documents/</font></strong>
│       │   ├── <strong><font color="#f0883e">homework.txt</font></strong>
│       │   └── projects/
│       └── Downloads/
└── Applications/
</pre>

### <font color="#79c0ff">Two kinds of paths</font>

| Type | Starts with | Meaning | Example |
|---|---|---|---|
| **Absolute** | `/` | Always points to the same place, from the root | `/Users/yourname/Documents` |
| **Relative** | A folder name or `.` / `..` | Relative to wherever you are right now | `Documents/homework` |

Think of it like giving directions. An **absolute** path is a full street address. A **relative** path is "turn left at the corner" — it only makes sense depending on where you're standing.

---

## <font color="#388bfd">pwd — Where Am I?</font>

```bash
pwd
```

`pwd` stands for **p**rint **w**orking **d**irectory. It tells you your exact location in the file system right now, always as an **absolute path**:

```bash
pwd
# /Users/yourname/Documents
```

Use it any time you feel lost, or to confirm a `cd` landed you where you expected.

### <font color="#79c0ff">Seeing it in the tree</font>

If `pwd` outputs `/Users/yourname/Documents`, your position looks like this:

<pre>
/
├── Users/
│   └── yourname/
│       ├── Desktop/
│       ├── <strong><font color="#f0883e">Documents/</font></strong>   ← you are here
│       └── Downloads/
└── Applications/
</pre>

---

## <font color="#388bfd">cd — Changing Directories</font>

```bash
cd path
```

Type `cd` followed by any path — absolute or relative — and the terminal moves you there.

### <font color="#79c0ff">Special path shortcuts</font>

| Shortcut | Meaning |
|---|---|
| `.` | The **current** directory — where you are right now |
| `..` | The **parent** directory — one level up |
| `~` | Your **home** directory |
| `/` | The **root** of the entire file system |

### <font color="#79c0ff">Examples</font>

```bash
cd Documents           # move into Documents (relative to current location)
cd /Users/yourname     # move to an exact location (absolute path)
cd ..                  # go up one level
cd ../..               # go up two levels
cd ~                   # go home, from anywhere
cd .                   # stay exactly where you are (harmless no-op)
```

> [!TIP]
> After every `cd`, run `pwd` to confirm where you ended up. See [pwd — Where Am I?](#pwd--where-am-i) for details.

### <font color="#79c0ff">Where do these take you?</font>

If you are currently inside `/Users/yourname/Documents/`:

| What you type | Where you end up |
|---|---|
| `cd .` | `/Users/yourname/Documents/` (no change) |
| `cd ..` | `/Users/yourname/` |
| `cd ../Desktop` | `/Users/yourname/Desktop/` |
| `cd ~` | `/Users/yourname/` |
| `cd /Applications` | `/Applications/` (absolute jump) |
| `cd projects` | `/Users/yourname/Documents/projects/` |

> [!NOTE]
> Folder names are case-sensitive on most systems. `Documents` and `documents` are different paths.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you run `pwd` and read the full path it outputs?
- [ ] Can you use `cd` to move into a folder?
- [ ] Can you use `cd ..` to go up one level?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you navigate to your home directory from anywhere using a single command?
- [ ] Can you use a relative path to move into a sibling folder (e.g. `cd ../Desktop`)?
- [ ] Can you explain the difference between an absolute and a relative path to someone who has never heard either term?

### <font color="#79c0ff">Advanced</font>

- [ ] Starting from anywhere on your computer, can you navigate to a deeply nested folder using a single `cd` command?
- [ ] Can you navigate into a folder whose name contains a space?
- [ ] Can you explain what `.` and `..` are without using the words "current" or "parent"?

---

← Back to [Terminal](../) — Next: [Search](../Search/)
