# Review — Terminal Basics, Day 2

*Originally covered in [Terminal Basics](../README.md)*

---

Everything from Day 1, plus:

| Command | What it does |
|---|---|
| `mkdir -p a/b/c` | Create a nested path in one command |
| `find path -name "file"` | Search recursively for a file by name |
| `find path -name "*.ext"` | Search using a wildcard pattern |
| `man command` | Open the manual page for any command |

Inside `man`: `Space` scroll down · `b` scroll up · `/word` search · `q` quit

---

## Tasks

1. From your home directory, create the nested structure `projects/week1/` in a single command. Navigate to `week1/`.
2. Create a file called `notes.md` inside `week1/`. Navigate back to your home directory.
3. Use `find` to locate `notes.md` starting from your home directory. Write down the exact command you used and what it printed.
4. Run `ls -lsa` on the `projects/` folder without navigating into it.
5. Open `man find`. Search for `-type`. Use `find . -type d` from your home directory and observe what it lists.
6. Create a second file called `readme.md` inside `projects/`. Use `find` with a wildcard to locate all `.md` files under `projects/` in a single command.
