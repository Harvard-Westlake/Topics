<div align="center">

# Project Setup
*<font color="#8b949e">Create the repository, project structure, and initial Git configuration</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">What You'll Set Up</font>

In this part you create the foundation the entire project builds on:

- A public GitHub repository named `git-project-YOURNAME` — this name never changes
- A `Git.java` file with an empty `main` method — your program lives here
- A `.gitignore` that tells GitHub's own Git to ignore the `git/` folder your program will create
- An initial `HEAD` file inside `git/` — this will track the most recent commit

The `.gitignore` entry for `/git` is critical. Without it, your program's simulated `git/` directory would be committed to GitHub alongside your code — every blob, tree, and commit file your program generates.

## <font color="#388bfd">The git/ vs .git/ Distinction</font>

Your project has two separate "git" directories:

| Directory | What it is | Who manages it |
|---|---|---|
| `.git/` | GitHub's own hidden Git folder | Git (hands off — never touch this) |
| `git/` | Your simulated repository | Your Java code |

You are building `git/` from scratch. The `.git/` folder already exists and is managed by real Git. They are completely separate.

## <font color="#388bfd">Milestone Commit Labels</font>

Every commit in this project must begin with the milestone label in its summary:

```
(GP-1.1): Initialized Project
(GP-2.3): Create BLOB Files
```

This format is required throughout the entire project. A commit history without these labels is incomplete and will affect your grade.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain the difference between the `.git/` folder and the `git/` folder your code creates?
- [ ] Can you explain why `/git` must be in `.gitignore`?
- [ ] Can you create a GitHub repository, clone it, and verify the remote with `git remote -v`?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain what the `HEAD` file stores and why it is part of `init()`?
- [ ] Can you describe the role of the commit label convention (GP-X.Y) and why a consistent history matters?
- [ ] Can you verify that your `.gitignore` is working by checking that `git/` does not appear in `git status`?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you set up the full project structure — repo, class, `.gitignore`, HEAD — from memory without referencing the instructions?
- [ ] Can you explain what would happen if you forgot the `/git` entry in `.gitignore` and pushed to GitHub?
- [ ] Can you write a commit message that would help a classmate understand exactly what was changed, if they were picking up your code in Part 4?

---

[Assignment](ASSIGNMENT.md)

← Back to [Git Project](../)
