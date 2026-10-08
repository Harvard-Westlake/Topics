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
| GP-3.2 | `createTree(workingList, dirPath)` — write one directory's tree file from the working list |
| GP-3.3 | `createTreeFromIndex()` — build the working list from the index and collapse it to the root tree |

After GP-3.1, the index stores full relative paths. After GP-3.2, your program can turn one directory's staged entries into a tree object. After GP-3.3, your program creates the whole tree, root included, from exactly what has been staged — the basis of every real Git commit.

## <font color="#388bfd">Read Before Starting</font>

- [Trees](../Docs/trees.md) — tree file format, bottom-up construction, the root tree

## <font color="#388bfd">How the Two Tree Methods Fit Together</font>

GP-3.2 and GP-3.3 both build tree files, at different scales:

| Method | Input | Use |
|---|---|---|
| `createTree(workingList, dirPath)` | The working list and one directory path | Writes that directory's tree file and returns its hash |
| `createTreeFromIndex()` | The index file | Builds the working list, calls `createTree` deepest-first, returns the root tree hash — what `commit` actually uses |

You implement GP-3.2 first because one directory is the unit of work; GP-3.3 is the loop around it. Neither method reads the file system — the file system holds everything on disk, including files that were never staged, so a tree built from it would not match the index. Built from the working list, a file that was never staged can never end up in a tree.

## <font color="#388bfd">The Working List (GP-3.2 and GP-3.3)</font>

A working list is a temporary data structure that starts as a copy of the index and gets compressed, directory by directory, until only the root tree remains. It is built and collapsed at runtime — it is not stored on disk permanently.

The algorithm works bottom-up: find the deepest directory whose children are all already resolved, create its tree file with `createTree`, replace all its entries in the working list with a single `tree` entry, and repeat until the working list contains only a root tree entry.

See [Docs/trees.md](../Docs/trees.md) and the interactive visualizer linked in the assignment for a step-by-step walkthrough.

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain why tree files must be built from the inside out (deepest directory first).
- [ ] Describe what a tree file contains — what each line represents.
- [ ] Given a working list entry, state which directory it belongs to.
- [ ] Trace from a root tree hash through all child hashes to reconstruct a directory's contents.

### <font color="#79c0ff">Intermediate</font>

- [ ] Implement `createTree(workingList, dirPath)` so it writes one directory's tree from the entries that belong directly to it.
- [ ] Explain how `createTree(workingList, dirPath)` and `createTreeFromIndex()` divide the work and when each is called.
- [ ] Explain why trees are built from the working list rather than by reading the file system.
- [ ] Walk through the working list algorithm for a three-file, two-directory example without looking at notes.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why the working list is sorted by path before processing, and what would go wrong if it weren't.
- [ ] Show that running `createTreeFromIndex()` twice on the same index produces identical tree hashes.
- [ ] Modify your implementation so that adding only one file to the index changes only the tree files along that file's path — not the entire tree structure.

---

[Assignment](ASSIGNMENT.md)

← [Peer Code Verification](../PeerCodeVerification/) — Next: [Peer Tree Verification](../PeerTreeVerification/)
