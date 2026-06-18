# Assignment — Project Setup

**Duration:** 1 class period  
**Due:** Before the next class

---

## Milestone GP-1.1: Create the Repository

### Instructions

1. Initialize a Git repository on GitHub with a `README.md`. Name it exactly `git-project-YOURNAME`, where YOURNAME is your own name. **Never rename this repository** — it is referenced throughout the project.

2. Clone the repository to your local machine, navigating to your HTCS_Projects folder first:

    ```bash
    git clone [repository-url]
    cd git-project-YOURNAME
    ```

3. Create a Java class file called `Git.java` with an empty `main` method.

4. Create a `.gitignore` file in the root of the repository and add the following entries:

    ```
    /git
    .DS_Store
    ```

    The `/git` entry tells GitHub's own Git to ignore the `git/` directory your program will create in later parts. Without this, your blobs, trees, and commits would be committed to GitHub alongside your source code.

5. Create the `git/` directory and inside it create a file called `HEAD` (no extension). Leave it empty for now. This file will store the hash of the most recent commit once you begin committing.

    > **Note:**
    > The `HEAD` file inside `git/` is your program's HEAD, not GitHub's. Your `.gitignore` entry for `/git` means this file will never be pushed to GitHub.

6. Commit your changes with the required label format:
    - **Summary:** `(GP-1.1): Initialized Project`
    - **Description:** List every file you created and what its purpose is.

7. Visit your repository on GitHub to verify all files appear correctly.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Repository named correctly** — `git-project-YOURNAME`, public, never renamed
- [ ] **`Git.java` committed** — contains a class with an empty `main` method
- [ ] **`.gitignore` committed** — contains `/git` and `.DS_Store` entries
- [ ] **`git/HEAD` created locally** — exists in the `git/` folder (not pushed — it is gitignored)
- [ ] **Commit uses label format** — summary begins with `(GP-1.1):`
- [ ] **Branch used** — committed on a feature branch, not directly on `main`

---

## Submission

Submit your **GitHub repository URL** on the Hub.

Ensure your repository is public so instructors can access it. Verify that `Git.java` and `.gitignore` are committed and visible on GitHub before submitting.
