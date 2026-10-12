<div align="center">

# Commits
*<font color="#8b949e">Commits save a snapshot of the repository and link them into a history.</font>*

</div>

---

![Layout of a commit file: a commit box with five lines (tree, parent, author, date, message). The tree line points to the root tree, a box listing two blobs and one subtree that make up the snapshot of every staged file. The parent line points to the commit before it, which has its own tree and parent. The first commit has no parent line.](assets/commit-layout.svg)

A commit is yet another Git object, but this one captures the whole project at one moment:

- **tree:** the root tree, the snapshot of every staged file.
- **parent:** the commit that came before, which links the snapshots into a history.
- **author, date, message:** who saved it, when, and why.

## <font color="#388bfd">Table of Contents</font>

1. [What a commit file holds](#what-a-commit-file-holds)
2. [How commits chain together through HEAD](#the-chain-and-head)
3. [The steps of making a commit, in order](#making-a-commit)
4. [Rebuilding the index from a commit's tree](#rebuilding-the-index)
5. [Checking out a commit to go back to that point in time](#checking-out-a-commit)

## <font color="#388bfd">What a Commit File Holds</font>

A commit is a small text file, stored in `git/objects/` under the SHA-1 hash of its own contents, just like a blob or a tree:

```
tree: 8c411a89ed6d846f064ed0decdba3a857f0d1667
parent: 2b98fbd4f414b26b612fa50b17879f62733254e6
author: Mr. Theiss
date: Thu Oct 09 11:56:39 PDT 2025
message: Add initial project files
```

The very first commit has nothing before it, so it has **no `parent:` line** at all.

## <font color="#388bfd">The Chain and HEAD</font>

Each commit points back at the one before it. Start at the newest commit, follow `parent:` again and again, and you walk the whole history back to the first commit:

```
C1 ← C2 ← C3 ← C4
```

`git/HEAD` is a one-line file that holds the hash of the newest commit. That is how Git knows where the chain ends:

- Before any commits, HEAD is empty.
- Making a commit reads HEAD to fill in `parent:`, then writes the new commit's hash into HEAD.

## <font color="#388bfd">Making a Commit</font>

1. Read `git/index` to see what is staged.
2. Build a tree for every staged directory, deepest first, until you have the root tree hash.
3. Read `git/HEAD` for the parent hash (empty means this is the first commit).
4. Write the commit's lines: tree, parent (if any), author, date, message.
5. Hash those lines with SHA-1 and save the file as `git/objects/<hash>`.
6. Write the new hash into `git/HEAD`. **This is always last.**

HEAD goes last for safety. If HEAD changed first and the program crashed before the commit file was saved, HEAD would point at a commit that does not exist.

## <font color="#388bfd">Rebuilding the Index</font>

The index is the list of what is staged. Sometimes there is no good list to start from: right after someone **clones** a repository, or right after a **checkout** swaps in an older snapshot. So Git writes a fresh index from the commit's tree.

The tree already has everything the index needs. Walk it from the root:

- A `blob` line becomes one index line: its hash, then its path.
- A `tree` line is a folder. Open that tree and keep walking, adding the folder's name to the front of every path inside it.

For the commit in the diagram above, the root tree `8c411a…` and its `docs` tree become this index:

```
aaf4c6… README.md
e3b0c4… Git.java
0a4d55… docs/notes.txt
```

Every committed file is now staged exactly as it was in that commit, so committing again right away would produce the same root tree.

## <font color="#388bfd">Checking Out a Commit</font>

Checkout takes the project back to a point in time: every file looks exactly the way it did in that commit.

1. Read the commit and find its root tree.
2. Delete every file listed in the **current** index, then any folders left empty.
3. Walk the commit's tree and write each blob back to its path, creating folders as you go.
4. Rebuild the index from that tree.
5. Write the commit's hash into `git/HEAD`.

Step 2 only deletes files Git tracks, not the whole folder. Files that were never added (and the `git/` folder itself) are left alone, just like real Git. Wiping the whole folder would also delete anything that was never committed.

> **Note:** Real Git also refuses to check out when a tracked file has changes that were never committed, because step 2 would erase them.

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Name the five lines of a commit file, and follow the `parent:` lines from HEAD back to the first commit.
- [ ] List the steps of making a commit in order, and explain why HEAD is updated last.
- [ ] Rebuild an index by hand from a commit's tree, and list what checkout deletes and what it leaves alone.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Make checkout refuse to run when a tracked file has changes that were never committed, the way real Git does.

---

[Assignment](ASSIGNMENT.md)

← [Peer Tree Verification](../PeerTreeVerification/) | Next: [Branches](../Branches/)
