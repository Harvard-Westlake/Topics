# Git-4.2: Implement the GitWrapper Interface

*Part of the [Commits](../ASSIGNMENT.md) assignment*

---

## About

Every project in the class was built differently on the inside. The `GitWrapper` class is the one place anyone (a tester, your teacher, a classmate) can go to run every operation without learning how your partner's code is organized. Because every project shares it, the whole class has a single, standard way to run (and grade) each project.

---

## What to Build

Add the `GitWrapper` class below to your partner's project and fill in each method by calling their existing code.

- **Use the provided code exactly.** Do not change the class name or any method signature. Changing the interface in any way defeats the purpose of a single way to run everyone's code.
- **Build on their code, don't replace it.** Keep refactoring of your partner's code to a minimum, unless functionality is missing.

```java
public class GitWrapper {

    /**
     * Initializes a new Git repository.
     * This method creates the necessary directory structure
     * and initial files (index, HEAD) required for a Git repository.
     */
    public void init() {
        // to-do: implement functionality here
    }

    /**
     * Stages a file for the next commit.
     * This method adds a file to the index file.
     * If the file does not exist, it throws an IOException.
     * If the file is a directory, it throws an IOException.
     * If the file is already in the index, it does nothing.
     * If the file is successfully staged, it creates a blob for the file.
     * @param filePath The path to the file to be staged.
     */
    public void add(String filePath) {
        // to-do: implement functionality here
    }

    /**
     * Creates a commit with the given author and message.
     * It should capture the current state of the repository by building trees based on the index file,
     * writing the tree to the objects directory,
     * writing the commit to the objects directory,
     * updating the HEAD file,
     * and returning the commit hash.
     *
     * The commit should be formatted as follows:
     * tree: <tree_sha>
     * parent: <parent_sha>
     * author: <author>
     * date: <date>
     * message: <message>
     *
     * @param author  The name of the author making the commit.
     * @param message The commit message describing the changes.
     * @return The SHA1 hash of the new commit.
     */
    public String commit(String author, String message) {
        // to-do: implement functionality here
        return "";
    }

    /**
     * Checks out a specific commit given its hash.
     * This method should read the HEAD file to determine the "checked out" commit.
     * Then it should update the working directory to match the
     * state of the repository at that commit by tracing through the root tree and
     * all its children.
     *
     * @param commitHash The SHA1 hash of the commit to check out.
     */
    public void checkout(String commitHash) {
        // to-do: implement functionality here
    }
}
```

What each method must do:

| Method | Given | What happens |
|---|---|---|
| `init()` | nothing | `git/`, `git/objects/`, `git/index`, and `git/HEAD` exist. Running it again changes nothing and causes no error. |
| `add(filePath)` | a file path | The file's blob is saved and its index line is added. Staging unchanged content does nothing. Staging changed content replaces that file's line. A path that does not exist, or is a folder, is an error. |
| `commit(author, message)` | an author and a message | Everything from [Git-4.1](Git-4-1.md): the commit file is saved, HEAD moves to it, and its hash is given back. |
| `checkout(commitHash)` | a commit hash | Built in [Git-4.4](Git-4-4.md). For now it can do nothing. |

In `README.md`, show how to run each method, with a short example someone could copy.

**Verify:** using only `GitWrapper`, initialize a repository, stage two files (one inside a folder), and commit. Every result in the table above happens.

---

## README Update

Answer these in `README.md`:

1. What bugs did you find in your partner's code, and which did you fix?
2. What was missing? Did you build it?

---

**Commit summary:** `(Git-4.2): Implemented the Interface`

---

← [Git-4.1](Git-4-1.md) | [Back to assignment](../ASSIGNMENT.md) | Next: [Git-4.3](Git-4-3.md) →
