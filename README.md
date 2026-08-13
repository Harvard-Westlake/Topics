<div align="center">

# Topics

*<font color="#8b949e">Honors Topics computer science curriculum</font>*

</div>

---

This repository holds every lesson in the **Honors Topics** computer science curriculum. Lessons are student-facing, organized by topic, and written as GitHub-rendered Markdown that the course hub imports directly for scheduling.

## <font color="#388bfd">Why the Curriculum Lives in Git</font>

The curriculum changes every year, and Git is what makes those changes manageable:

- **Branching for year-over-year revision** — each year's updates are developed on branches and merged in when ready, so material can be reworked without disturbing what is currently being taught.
- **History of progression** — the commit history preserves how every lesson has evolved across years: what changed, when, and why.
- **Pick-and-choose scheduling** — every lesson, assignment, review fragment, and milestone is its own file, so the course hub can schedule any subset of items in any order and recombine them differently each year.

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

**[MiniGPT](MiniGPT/)**  
Project Strata: build a tiny decoder-only transformer language model in Java from first principles — tokenization, attention, backpropagation, training, and honest evaluation against a Markov baseline.

- [Patterns Become Tokens](MiniGPT/Tokenizer/) — a Byte Pair Encoding tokenizer that counts adjacent pairs and merges the most frequent
- [The Reader with One-Step Memory](MiniGPT/MarkovBaseline/) — uniform, unigram, and bigram baselines with held-out evaluation
- [The Hand-Built Spotlight](MiniGPT/FixedAttention/) — causal self-attention with hand-written rules, no learning yet
- [A Table That Learns](MiniGPT/TrainableBigram/) — softmax, cross-entropy loss, and gradient descent on a trainable bigram
- [From Exact Symbols to Features](MiniGPT/ObjectNetwork/) — token embeddings and an object-oriented neural network, forward pass only
- [Following the Error Backward](MiniGPT/ScalarAutograd/) — backpropagation and a scalar automatic-differentiation engine
- [From Glass Box to Engine](MiniGPT/DenseEngine/) — the same mathematics on dense primitive arrays
- [Learning What to Look For](MiniGPT/SingleHeadAttention/) — trainable single-head causal attention, proven on synthetic tasks
- [A Team of Readers](MiniGPT/TransformerBlock/) — multi-head attention, feed-forward layers, and a complete transformer block
- [The Machine Writes](MiniGPT/TrainingAndGeneration/) — end-to-end training, Adam, checkpointing, and text generation
- [The Trial of the Archive](MiniGPT/Capstone/) — the capstone experiment, ablation, and responsible evaluation

<font color="#a371f7">■ Reinforce</font>

**[Git Project](GitProject/)**  
Recreate the core of Git in Java — hashing, blobs, trees, and commits — to understand how version control actually works under the hood.

- [Project Setup](GitProject/ProjectSetup/) — GitHub repo, `Git.java`, `.gitignore`, and initial HEAD
- [Initialization and Blobs](GitProject/InitAndBlobs/) — `init()`, SHA-1 hashing, blob files, and the index
- [Trees](GitProject/Trees/) — index formatting, tree files, and building trees from staged files
- [Commits](GitProject/Commits/) — commit files, HEAD chain, and the `GitWrapper` interface
- [Branches](GitProject/Branches/) — branch pointers and HEAD *(coming soon)*
