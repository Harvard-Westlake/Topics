<div align="center">

# Topics

*<font color="#8b949e">Honors Topics computer science curriculum</font>*

</div>

---

Student-facing lessons organized by topic.

## <font color="#388bfd">Lesson Types</font>

| | Type | What it means |
|---|---|---|
| <font color="#3fb950">■</font> | **Environment Configuration** | Sets up your machine and tools so you are ready to code |
| <font color="#a371f7">■</font> | **Learning** / **Reinforce** | Introduces new concepts and builds on them through practice |
| <font color="#e3b341">■</font> | **Review** | Revisits and consolidates material already covered |

---

## <font color="#388bfd">Table of Contents</font>

<font color="#3fb950">■ Environment Configuration</font>

**[Computer Setup](ComputerSetup/)**  
Step-by-step guide to standardizing your terminal environment and installing developer tools on Mac or PC.

- [Initial Install](ComputerSetup/InitialInstall/) — terminal, Git, GitKraken, VS Code, and Java 21 on Mac or PC

<font color="#a371f7">■ Learning</font>

**[Terminal](Terminal/)**  
Introduction to the command line: how commands work, navigating the file system, listing files, and creating your own structure.

- [Terminal Basics](Terminal/Basics/) — navigation, listing, creating files and folders, `find`, and `man`

**[Git Usage](GitUsage/)**  
Core Git concepts and workflows: staging, committing, branching, merging, and contributing through forks and pull requests.

- [Repositories and Commits](GitUsage/RepositoriesAndCommits/) — repositories, cloning, staging, committing, pushing, and pulling
- [Branching and Merging](GitUsage/BranchingAndMerging/) — branches, `git merge`, fast-forward merges, pull requests, and `.gitignore`
- [Forks and Collaboration](GitUsage/ForksAndCollaboration/) — forking, upstream remotes, syncing forks, and cross-fork pull requests

<font color="#a371f7">■ Reinforce</font>

**[Git Project](GitProject/)**  
Recreate the core of Git in Java — hashing, blobs, trees, and commits — to understand how version control actually works under the hood.

- [Project Setup](GitProject/ProjectSetup/) — GitHub repo, `Git.java`, `.gitignore`, and initial HEAD
- [Initialization and Blobs](GitProject/InitAndBlobs/) — `init()`, SHA-1 hashing, blob files, and the index
- [Trees](GitProject/Trees/) — index formatting, tree files, and building trees from staged files
- [Commits](GitProject/Commits/) — commit files, HEAD chain, and the `GitWrapper` interface
- [Branches](GitProject/Branches/) — branch pointers and HEAD *(coming soon)*
