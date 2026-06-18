<div align="center">

# Trees
*<font color="#8b949e">Represent directory structure as a chain of hashed snapshot files</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">What You'll Build</font>

| Milestone | What it does |
|---|---|
| GP-3.1 | Update the index to store relative paths instead of bare filenames |
| GP-3.2 | `createTree(dirPath)` — recursively build tree files from a directory |
| GP-3.3 | `createTreeFromIndex()` — build trees from the index using a working list |

After GP-3.1, the index stores full relative paths. After GP-3.2, your program can snapshot any directory into tree objects. After GP-3.3, your program creates trees only for what has actually been staged — the basis of every real Git commit.

## <font color="#388bfd">Read Before Starting</font>

- [Trees](../Docs/trees.md) — tree file format, bottom-up construction, the root tree

## <font color="#388bfd">Why Two Tree Methods?</font>

GP-3.2 and GP-3.3 both build tree files, but they serve different purposes:

| Method | Input | Use |
|---|---|---|
| `createTree(dirPath)` | A directory path | Snapshots any directory, including files not staged |
| `createTreeFromIndex()` | The index file | Snapshots only staged files — what `commit` actually uses |

You implement GP-3.2 first because the recursive logic is easier to understand from a concrete directory. GP-3.3 then applies that logic to staged files specifically.

## <font color="#388bfd">The Working List (GP-3.3)</font>

A working list is a temporary data structure that starts as a copy of the index and gets compressed, directory by directory, until only the root tree remains. It is built and collapsed at runtime — it is not stored on disk permanently.

The algorithm works bottom-up: find the deepest directory whose children are all already resolved, create its tree file, replace all its entries in the working list with a single `tree` entry, and repeat until the working list contains only a root tree entry.

See [Docs/trees.md](../Docs/trees.md) and the interactive visualizer linked in the assignment for a step-by-step walkthrough.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain why tree files must be built from the inside out (deepest directory first)?
- [ ] Can you describe what a tree file contains — what each line represents?
- [ ] Can you trace from a root tree hash through all child hashes to reconstruct a directory's contents?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement `createTree(dirPath)` recursively so it handles subdirectories of any depth?
- [ ] Can you explain the difference between `createTree(dirPath)` and `createTreeFromIndex()` and when each is used?
- [ ] Can you walk through the working list algorithm for a three-file, two-directory example without looking at notes?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why the working list is sorted by path before processing, and what would go wrong if it weren't?
- [ ] Can you show that running `createTreeFromIndex()` twice on the same index produces identical tree hashes?
- [ ] Can you modify your implementation so that adding only one file to the index changes only the tree files along that file's path — not the entire tree structure?

---

[Assignment](ASSIGNMENT.md)

← [Initialization and Blobs](../InitAndBlobs/) — Next: [Commits](../Commits/)
