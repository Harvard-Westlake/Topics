<div align="center">

# Branches
*<font color="#8b949e">A branch is a name that points at a commit and moves forward every time you commit on it.</font>*

</div>

---

![Two branches sharing history. Commits C1 and C2 come first. C3 and C4 both have C2 as their parent. The branch main points at C3, the branch feature points at C4, and HEAD points at feature. Underneath, the files behind it: .git/refs/heads/main holds C3's hash, .git/refs/heads/feature holds C4's hash, and .git/HEAD holds ref: refs/heads/feature. A new commit now moves feature forward and leaves main where it is.](assets/branch-layout.svg)

A branch is a bookmark in the history, not a copy of the project:

- **A branch:** a tiny file holding one commit hash.
- **HEAD:** says which branch you are on.
- **Committing:** moves the branch you are on to the new commit. Every other branch stays put.

## <font color="#388bfd">Table of Contents</font>

1. [What a branch really is](#what-a-branch-is)
2. [How HEAD and committing move a branch](#head-and-committing)
3. [Switching to another branch](#switching-branches)

## <font color="#388bfd">What a Branch Is</font>

Real Git keeps each branch as a file in `.git/refs/heads/`, named after the branch. The file holds one line: the hash of the newest commit on that branch.

```
.git/refs/heads/main      → 8c411a89ed6d846f064ed0decdba3a857f0d1667
.git/refs/heads/feature   → 2b98fbd4f414b26b612fa50b17879f62733254e6
```

**Creating a branch** writes one new file holding the commit you are on right now. No files are copied and no commits are made, which is why branches are instant and cost almost nothing. Two branches can even point at the same commit until one of them moves.

## <font color="#388bfd">HEAD and Committing</font>

In the Commits lesson, `HEAD` held a commit hash. With branches, HEAD usually holds the **name** of a branch instead:

```
ref: refs/heads/feature
```

That one change is what makes branches move. When you commit:

1. The new commit's `parent:` is the commit the current branch points at.
2. The commit file is saved, exactly as before.
3. The **branch** file is updated to the new commit's hash. HEAD does not change: it still names the same branch.

Each branch grows its own line of history from the commit where it started, like C3 and C4 above.

If HEAD holds a plain commit hash instead of a branch name, Git calls it a **detached HEAD**. Checking out a commit by its hash, which is every checkout in the Commits lesson, does this. Detached does not mean you are on some unknown branch: you are on no branch at all. The commit may sit on `main`, on `feature`, or on several branches, but none of them is selected. If you commit now, HEAD moves to the new commit and no branch moves with it, so that commit is easy to lose.

## <font color="#388bfd">Switching Branches</font>

Checking out a branch is checking out its commit, plus one more step:

1. Read the branch file to get its commit hash.
2. Check out that commit: tracked files, the index, and the working folder now match it.
3. Write `ref: refs/heads/<branch>` into HEAD, so the next commit moves this branch.

Nothing is lost by switching. Every commit on the other branch is still in `.git/objects/`, and its branch file still points at the newest one.

![Two animated panels comparing checkouts. Left, checking out a commit hash: the HEAD label leaves main and attaches directly to commit C2, a yellow notice says detached HEAD, you are on no branch at all, and a new commit C5 appears under C2 with HEAD moving to it while main still points at C3. Right, checking out the branch feature: HEAD moves from main to the feature label, a new commit C5 appears after C4, and the feature label moves forward to C5 with HEAD following while main stays at C3.](assets/checkout-hash-vs-branch.svg)

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Say what a branch file holds, and why creating a branch copies no files.
- [ ] Explain which file changes when you commit on a branch, and which stays the same.
- [ ] List what changes when you check out a branch, and what a detached HEAD is.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Draw the history after committing twice on `main` and once on `feature`, starting from the diagram above, with every branch label and HEAD in place.

---

[Assignment](ASSIGNMENT.md)

← [Commits](../Commits/) | Next: [Coding Standards](../CodingStandards/)
