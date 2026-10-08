# Assignment — Project Setup

*Lesson: [Project Setup](README.md)*

**Duration:** 1 class period  
**Due:** Before the next class

---

## Milestone GP-1.1: Create the Repository

### Instructions

1. In your terminal, create the project folder inside `HTCS_Projects` and turn it into a repository. Name it anything you like. Below, `YOUR-REPO-NAME` stands for the name you pick. Once it is on GitHub, do not rename it, because classmates will fork it later in the project.

    > **Tip:** Try to come up with a fun Git pun as your repository name, such as `git-happens`, `commitment-issues`, or `git-r-done`.

    ```bash
    cd ~/HTCS_Projects
    mkdir YOUR-REPO-NAME && cd YOUR-REPO-NAME
    git init
    ```

2. Create a `README.md` with the project's name as its first line — you will document every method here as the project grows.

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

7. Publish the repository to GitHub from your terminal — this creates `YOUR-REPO-NAME` under your account, connects it as `origin`, and pushes your commit in one command:

    ```bash
    gh repo create YOUR-REPO-NAME --source=. --public --push
    ```

8. Open it and verify all files appear correctly:

    ```bash
    gh repo view --web
    ```

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Repository created** — public, under your account, and not renamed after publishing
- [ ] **`Git.java` committed** — contains a class with an empty `main` method
- [ ] **`.gitignore` committed** — contains `/git` and `.DS_Store` entries
- [ ] **`git/HEAD` created locally** — exists in the `git/` folder (not pushed — it is gitignored)
- [ ] **Commit uses label format** — summary begins with `(GP-1.1):`
- [ ] **Published with `gh repo create --source=. --public --push`** — `git remote -v` shows `origin` under your account. This first commit lives on `main` so GitHub's default branch is right; every later milestone goes on a feature branch, never directly on `main`

---

## Submission

Submit your **GitHub repository URL** on the Hub.

Ensure your repository is public so instructors can access it. Verify that `Git.java` and `.gitignore` are committed and visible on GitHub before submitting.
