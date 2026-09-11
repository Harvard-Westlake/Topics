<div align="center">

# Git Usage
*<font color="#8b949e">Version control fundamentals from a user's perspective</font>*

<font color="#a371f7">Learning</font>

</div>

---

Git is the industry-standard tool for tracking changes in code, collaborating with teammates, and maintaining a complete history of a project. This module covers how Git works from the ground up — what you are doing every time you save, share, and collaborate on code.

---

## <font color="#388bfd">Table of Contents</font>

**[Repositories and Commits](RepositoriesAndCommits/)**  
What a repository is, how to initialize and clone one, and how the stage → commit → push cycle works.

**[Branching and Merging](BranchingAndMerging/)**  
Creating parallel lines of development, merging them, reviewing pull requests, choosing squash vs regular merges, and ignoring files.

**[Forks and Collaboration](ForksAndCollaboration/)**  
Forking public repositories, keeping your fork in sync, and contributing back through cross-fork pull requests.

**[File Hashing](FileHashing/)**  
Hash table review, the probability of collisions and how to size a hash space, and the terminal's built-in hashing commands.

---

## <font color="#388bfd">Lessons</font>

| Day | Lesson | What you'll learn |
|---|---|---|
| 1 | [Repositories and Commits](RepositoriesAndCommits/) | Repos, `git clone`, `git add`, `git commit`, `git push`, `git pull` |
| 2 | [Branching and Merging](BranchingAndMerging/) | `git branch`, `git checkout`, `git merge`, pull requests, `.gitignore` |
| 3 | [Forks and Collaboration](ForksAndCollaboration/) | Forking, upstream remotes, syncing forks, cross-repo pull requests |
| 4 | [File Hashing](FileHashing/) | Hash tables, collision probability, sizing a hash space, `sum`, `md5sum`, `sha256sum` |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain the difference between a local and a remote repository.
- [ ] Stage, commit, and push a change using only the terminal.
- [ ] Create a branch, commit to it, and switch back to `main`.

### <font color="#79c0ff">Intermediate</font>

- [ ] Clone a repository, make a change, and open a pull request on GitHub.
- [ ] Explain when a fast-forward merge occurs and why it matters.
- [ ] Fork a repository and push a change to your fork.
- [ ] Hash a file with `sha256sum` and explain what the output represents.

### <font color="#79c0ff">Advanced</font>

- [ ] Sync a fork with an upstream repository using the terminal.
- [ ] Explain the entire open source contribution workflow from fork to merged PR.
- [ ] Write commit messages that clearly communicate intent to a future reader.
- [ ] Compute a collision probability and explain how Git uses hashing to name every commit.
