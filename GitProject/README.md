<div align="center">

# Git Project
*<font color="#8b949e">Recreate the core of Git in Java — hashing, blobs, trees, and commits</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

In this project you will implement a simplified version of Git in Java. You will start by understanding how a single file gets stored as a hash, then build up to a working version control system that can initialize a repository, stage files, build directory snapshots, and chain commits into a history.

The project is designed around reading unfamiliar code. After the first part, each subsequent part picks up where a random classmate left off. You will need to read their README, understand their design, and extend it — exactly how software development works on a team.

---

## <font color="#388bfd">Collaboration Pattern</font>

| Part | Whose code | What you build |
|---|---|---|
| 1 | Your own | GitHub repo, Java class, `.gitignore`, HEAD setup |
| 2 | Your own | `init()`, SHA-1 hashing, blob files, index file |
| 3 | Your own | Index formatting, tree files, trees from index |
| 4 | A classmate's codebase | Commit files, HEAD chain, `GitWrapper` |
| 5 | TBD | Branches *(not yet specced)* |

---

## <font color="#388bfd">Project Rules</font>

1. **No AI-generated code.** Using any AI tool to produce code is prohibited.
2. **No sharing code with classmates.** Work individually. Copied code is subject to honor board review.
3. **Small snippets from online resources are permitted**, as long as you cite them in a code comment and they help build a single function — do not copy a complete Git implementation.
4. **Commit summaries must use the milestone label.** Every commit begins with the milestone tag, e.g. `(GP-2.1): Initialize Repository`. This is required — a cluttered commit history affects your grade.
5. **Never commit directly to `main`.** Create a feature branch for each milestone and merge via pull request.

---

## <font color="#388bfd">Reference Documentation</font>

Read the doc for each concept before starting the part that uses it.

| Document | Read before | Covers |
|---|---|---|
| [BLOBs](Docs/blobs.md) | Part 2 | Content-addressed file storage |
| [Index File](Docs/index-file.md) | Part 2 | Staging and the index |
| [Trees](Docs/trees.md) | Part 3 | Directory snapshots |
| [Commits](Docs/commits.md) | Part 4 | Commit files and the HEAD chain |

---

## <font color="#388bfd">Lessons</font>

| Day | Lesson | What you'll build |
|---|---|---|
| 1 | [Project Setup](ProjectSetup/) | GitHub repo, `Git.java`, `.gitignore`, initial HEAD |
| 2–4 | [Initialization and Blobs](InitAndBlobs/) | `init()`, SHA-1 hashing, blob files, index file |
| 5–7 | [Trees](Trees/) | Index formatting, basic trees, trees from index |
| 8–11 | [Commits](Commits/) | Root tree, commit files, HEAD chain, `GitWrapper` |
| TBD | [Branches](Branches/) | Branch files, HEAD pointers *(coming soon)* |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain what a blob is and why it uses a hash as its filename.
- [ ] Explain the difference between staging a file and committing it.
- [ ] Trace from a commit hash through a root tree to a specific file's content.

### <font color="#79c0ff">Intermediate</font>

- [ ] Implement `init()` so it is safe to call multiple times without overwriting existing data.
- [ ] Build tree files for a directory structure where some subdirectories are nested three levels deep.
- [ ] Read a classmate's codebase, understand their design, and extend it without breaking existing behavior.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why the working list algorithm in GP-3.3 produces trees bottom-up rather than top-down.
- [ ] Implement `checkout` — restoring the working directory to the exact state of any prior commit.
- [ ] Explain what a directed acyclic graph is and why the commit chain is one.
