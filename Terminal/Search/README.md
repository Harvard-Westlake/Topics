<div align="center">

# Search
*<font color="#8b949e">Listing folder contents with ls</font>*

<font color="#a371f7">Learning</font>

</div>

---

The `ls` command **lists** the contents of a directory. It's one of the most-used commands in the terminal.

---

## <font color="#388bfd">Basic usage</font>

```bash
ls
```

With no argument, `ls` lists the contents of your **current** directory.

```bash
ls Documents/
```

Pass a path to list the contents of any folder.

---

## <font color="#388bfd">What are options?</font>

**Options** (also called *flags*) modify how a command behaves. They follow the command name and always start with a `-`:

```
ls  -options  argument
     ↑
     starts with a dash
```

You can stack multiple options behind a single dash — they don't need spaces between them:

```bash
ls -l -s -a     # three separate flags
ls -lsa         # identical — combined behind one dash
```

---

## <font color="#388bfd">The `-lsa` options</font>

| Option | Name | What it does |
|---|---|---|
| `-l` | **Long format** | Shows permissions, size, owner, and modification date |
| `-s` | **Size** | Shows each file's size in disk blocks |
| `-a` | **All** | Includes hidden files (names that start with `.`) |

### <font color="#79c0ff">Running `-lsa`</font>

```bash
ls -lsa
```

Sample output:

```
total 48
 8 drwxr-xr-x  5 yourname  staff   160 Jun 10 09:00 .
 8 drwxr-xr-x  3 yourname  staff    96 Jun  5 14:22 ..
 0 -rw-r--r--  1 yourname  staff     0 Jun 10 08:45 .gitkeep
16 -rw-r--r--  1 yourname  staff  3204 Jun 10 09:00 README.md
 8 -rw-r--r--  1 yourname  staff   512 Jun  9 11:30 notes.txt
```

### <font color="#79c0ff">Reading the output columns</font>

| Column | Meaning |
|---|---|
| `8` (leftmost) | Size in 512-byte disk blocks |
| `drwxr-xr-x` | Permissions — `d` = directory, `-` = regular file |
| `5` | Number of hard links |
| `yourname` | Owner |
| `staff` | Group |
| `160` | Size in bytes |
| `Jun 10 09:00` | Date and time last modified |
| `README.md` | File or folder name |

> [!NOTE]
> The `-a` flag reveals **hidden files** — files whose names begin with a `.`, like `.gitkeep` or `.DS_Store`. They're invisible to plain `ls` but show up with `-a`. That's also why `.` (current directory) and `..` (parent directory) appear in the output — they're treated as entries in every folder.

---

## <font color="#388bfd">Comparing plain `ls` vs `ls -lsa`</font>

```bash
ls
# README.md   notes.txt
```

```bash
ls -lsa
# total 48
#  8 drwxr-xr-x  5 yourname  staff   160 Jun 10 09:00 .
#  8 drwxr-xr-x  3 yourname  staff    96 Jun  5 14:22 ..
#  0 -rw-r--r--  1 yourname  staff     0 Jun 10 08:45 .gitkeep
# 16 -rw-r--r--  1 yourname  staff  3204 Jun 10 09:00 README.md
#  8 -rw-r--r--  1 yourname  staff   512 Jun  9 11:30 notes.txt
```

Plain `ls` gives you names. `-lsa` gives you the full picture — sizes, dates, hidden files, and permissions.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you run `ls` and list your current directory?
- [ ] Can you pass a folder path to `ls` to list a directory you're not inside?
- [ ] Can you name what each of the flags `-l`, `-s`, and `-a` does?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you run `ls -lsa` and identify the name, size, and last-modified date for each file?
- [ ] Can you explain why `.` and `..` appear in the output of `ls -a`?
- [ ] Can you tell from the permissions column which entries are folders and which are files?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you find at least one hidden file in your home directory?
- [ ] Can you explain what the permissions string `drwxr-xr-x` means, one character at a time?
- [ ] Can you run `ls` on a folder two levels above your current location without using `cd` first?

---

← [Navigation](../Navigation/) — Next: [Experiment](../Experiment/)
