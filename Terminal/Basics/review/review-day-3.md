# Review — Terminal Basics, Day 3

*Originally covered in [Terminal Basics](../README.md)*

---

All commands from Days 1 and 2. At this point you should be able to chain operations without step-by-step prompting.

| Reminder | Syntax |
|---|---|
| Nested create | `mkdir -p a/b/c` |
| Navigate multiple levels | `cd ../..` |
| Find by name | `find . -name "*.md"` |
| Find only files | `find . -type f -name "*.txt"` |
| Find only directories | `find . -type d` |
| Manual | `man command` → `/FLAGS` to jump to options |

---

## Tasks

1. In a single command, create the structure `school/cs/projects/`. Navigate to `projects/` and create three files: `Main.java`, `notes.md`, and `README.txt`.

2. Without navigating, list the contents of `school/` using an absolute or relative path argument to `ls`.

3. From `projects/`, navigate back to `school/` one level at a time using only `..`. Print your location with `pwd` after each step.

4. From `school/`, use `find` to locate every file (not directories) anywhere inside it. Then narrow it down: find only `.md` files.

5. Open `man ls`. Find a flag you have not used before in this course. Apply it to the `school/` directory and describe what it changes about the output.

6. From your home directory, create a second folder called `archive`. Move into `school/cs/projects/` using a single absolute `cd` command. Then navigate to `archive/` using a relative path without going through home first.
