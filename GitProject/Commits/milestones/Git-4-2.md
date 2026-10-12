# Git-4.2: Implement the Interface

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## About

Every project in the class was built differently on the inside. The interface is the one place anyone (a tester, your teacher, a classmate) can go to run every operation without learning how your partner's code is organized. Build it on top of their existing code rather than rewriting their logic.

---

## What to Build

One clear place in the program where each of these operations can be run:

| Operation | Given | What happens |
|---|---|---|
| **Initialize** | nothing | `git/`, `git/objects/`, `git/index`, and `git/HEAD` exist. Running it again changes nothing and causes no error. |
| **Stage a file** | a file path | The file's blob is saved and its index line is added. Staging unchanged content does nothing. Staging changed content replaces that file's line. A path that does not exist, or is a folder, is an error. |
| **Commit** | an author and a message | Everything from [Git-4.1](Git-4-1.md): the commit file is saved, HEAD moves to it, and its hash is given back. |
| **Check out** | a commit hash | Built in [Git-4.4](Git-4-4.md). For now it can do nothing. |

In `README.md`, show how to run each operation, with a short example someone could copy.

**Verify:** using only the interface, initialize a repository, stage two files (one inside a folder), and commit. Every result in the table above happens.

---

## README Update

Answer these in `README.md`:

1. What bugs did you find in your partner's code, and which did you fix?
2. What was missing? Did you build it?

---

**Commit summary:** `(Git-4.2): Implemented the Interface`

---

← [Git-4.1](Git-4-1.md) | [Back to assignment](../ASSIGNMENT.md) | Next: [Git-4.3](Git-4-3.md) →
