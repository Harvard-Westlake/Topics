# Assignment — Terminal Basics

**Due:** Next class

---

## Part 1 — Build and Navigate

Work through the following steps in order inside your terminal. You will use what you made in Part 1 to complete Part 2.

1. Create **two directories** — name them anything you like
2. Create **a file inside one of those directories** — use `touch` or `vim`
3. Navigate **two levels up** from inside that directory using `cd`
4. Use **`find`** to locate the file you created

> **Tip:**
> If you get lost at any point, run `pwd` to see where you are and `ls` to see what is around you.

---

## Part 2 — Explore the Manual

Use `man` to look up **three commands you have never used before**. For each one:

- Read the NAME and DESCRIPTION sections
- Try at least one flag from the OPTIONS section in your terminal
- Be ready to explain what the command does in one sentence

Useful starting points: `man cat`, `man cp`, `man mv`, `man rm`, `man grep`, `man echo`, `man wc`, `man diff`, `man chmod`

> **Note:**
> You are not being tested on memorizing these — the goal is to practice the habit of reading documentation and experimenting. Pick three that seem genuinely useful to you.

---

## Success Criteria

Before submitting, confirm each of the following:

- [ ] **Two directories created** — both exist in your file system
- [ ] **A file exists inside one of those directories** — confirmed with `ls`
- [ ] **Navigated two levels up** — you used `cd ../..` or equivalent
- [ ] **`find` returned the file** — the command ran and printed the file path
- [ ] **Three commands explored via `man`** — you can describe what each one does

---

## Submission

Submit **one text response** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Directory 1 name:    
Directory 2 name:    
File created:        
find command used:   find
find output:         

Command 1:           
What it does:        
Flag you tried:      

Command 2:           
What it does:        
Flag you tried:      

Command 3:           
What it does:        
Flag you tried:      
```

Example of a completed stencil:

```
Directory 1 name:    projects
Directory 2 name:    archive
File created:        projects/notes.txt
find command used:   find . -name "notes.txt"
find output:         ./projects/notes.txt

Command 1:           cat
What it does:        prints the contents of a file to the terminal
Flag you tried:      cat -n notes.txt  (adds line numbers)

Command 2:           wc
What it does:        counts lines, words, and characters in a file
Flag you tried:      wc -l notes.txt  (lines only)

Command 3:           cp
What it does:        copies a file or directory to a new location
Flag you tried:      cp notes.txt notes-backup.txt
```
