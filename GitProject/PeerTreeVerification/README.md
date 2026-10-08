<div align="center">

# Peer Tree Verification
*<font color="#8b949e">Fork a classmate's Part 3, hash their trees by hand, and prove which behaviors actually work</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

You spent the last three classes turning the index into tree files: relative paths in GP-3.1, one directory's tree in GP-3.2, and the whole snapshot down to a root tree in GP-3.3. Today you do what you did after Part 2, with harder material. You fork a classmate's repository, get their tree code running, and find out which behaviors really work, with evidence a stranger could repeat. Trees are a better test of reading skill than blobs: one wrong character in one tree changes the hash of every tree above it. That means you can know the right answer before you run anything, by building the tree files yourself in the terminal.

## <font color="#388bfd">Table of Contents</font>

1. [Why trees are the hardest part of the project to verify by eye](#why-verify-trees)
2. [Fork the repository, clone your fork, and open it](#fork-clone-open)
3. [Map the three tree milestones to the methods that do them](#reading-tree-code)
4. [Black-box commands that show what their code left in git/](#black-box-toolkit-for-trees)
5. [Hash a tree by hand so you know the answer before you run](#hashing-a-tree-by-hand)
6. [Write evidence that would convince a stranger](#writing-evidence-that-convinces)
7. [The six Part 3 behaviors you are verifying today](#what-you-are-verifying)
8. [Rename their tree code so it says what it holds and does](#renaming-for-sense)
9. [Rules for reviewers](#reviewer-rules)

---

## <font color="#388bfd">Why Verify Trees</font>

A blob is easy to judge: the file in `git/objects/` either matches the original or it does not. A tree is harder, because its correctness is spread across three methods and a chain of hashes:

| If this is wrong | This is what you see |
|---|---|
| The index stores bare filenames | The program cannot tell `docs/hello.txt` from `hello.txt`, so trees for different folders merge |
| A tree line holds the full path instead of the final name | That tree's hash is wrong, so every tree above it is wrong too |
| The tree file ends with an extra newline | Same content to your eye, a completely different hash |
| The working list is never sorted | The lines can come out in a different order, so the hash can change between runs |
| The trees are built from the folder on disk | Files that were never staged show up in the snapshot |

Part 4 of this project hands you a classmate's codebase and asks you to build commits on top of their trees. A commit stores one root tree hash. If that hash is wrong, every commit built on it is wrong. Today is practice at catching that before you depend on it.

---

## <font color="#388bfd">Fork, Clone, Open</font>

The workflow is the same one you used in [Peer Code Verification](../PeerCodeVerification/). You will be assigned a different classmate this time.

1. In your terminal, inside your projects folder, fork the classmate's `git-project-THEIRNAME` and clone your fork in one step:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/git-project-THEIRNAME --clone
   cd git-project-THEIRNAME
   git remote -v
   ```
   `origin` must be under **your** username and `upstream` under theirs.
2. Open the folder in VS Code. Read their `README.md` before any `.java` file, because it is their list of claims.
3. Pull up the [Index-to-Tree Visualizer](https://learnhw.web.app/static/code/widgets/index-tree/index-tree.html) in another tab. Once their code has written an index, you can paste it in and watch the correct trees get built.

> **Note:** You never push to the classmate's repository and you never open a pull request to it. Anything you add or change stays in your fork and gets recorded in your chart.

👉 <details>
<summary><h3>Activity: Fork, Clone, Open — click to expand</h3></summary>

*Concept: A fork is a copy of a classmate's repository under your own account — you clone the fork, not the original, so everything you do today lands in a repository you control.*

![Diagram of the fork-then-clone path: on the left, the classmate's repository git-project-THEIRNAME on GitHub; a Fork arrow copies it into your account as YOUR-USERNAME/git-project-THEIRNAME, labeled forked from the original; a gh repo fork --clone arrow brings that fork down to your laptop in HTCS_Projects, where origin points at your fork and upstream at the original. A crossed-out arrow from the laptop straight to the classmate's repository is marked push refused — you never write to their repo.](assets/fork-clone-open.svg)

## Task

1. On GitHub, open the repository you were assigned (`git-project-THEIRNAME`). Confirm it belongs to a classmate, not to you, and not to the classmate whose code you reviewed in Part 2.
2. In your terminal, go to your projects folder, then fork the repository and clone your fork in one step:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/git-project-THEIRNAME --clone
   cd git-project-THEIRNAME
   ```
   On GitHub, your copy now shows **forked from THEIR-USERNAME/git-project-THEIRNAME** under its title.
3. Prove where the remotes point:
   ```bash
   git remote -v
   ```
   Four lines: `origin` under **your** username (your fork) and `upstream` under the classmate's (the original). If `origin` shows the classmate's username, you cloned the original — delete the folder and run the fork command again.
4. Read the history for your first clue about what was attempted:
   ```bash
   git log --oneline | head -20
   ```
   Count the commits labeled `(GP-3.1)`, `(GP-3.2)`, and `(GP-3.3)`. A milestone with no commit is a milestone you should expect to find missing.
5. Open the folder in the editor you use for Java and read `README.md` first. Write down, in one line each, every tree-related method it claims exists.

*(Standalone file: [activities/01-fork-clone-open.md](activities/01-fork-clone-open.md))*

</details>

---

## <font color="#388bfd">Reading Tree Code</font>

Read in this order. Do not start at line 1 of `Git.java` and read to the end.

1. **Start with the README and the commit log.** List every tree method the README names, and check that each milestone label `(GP-3.1)`, `(GP-3.2)`, `(GP-3.3)` has a commit.
2. **Find the index writer.** This is the `add` (or `stage`) method from Part 2, changed in GP-3.1. Check that it writes `<hash> <relative path>`, and look for the two new checks: skip an exact duplicate, and replace the line of a file whose content changed.
3. **Find `createTree`.** Note how it decides that an entry belongs to a directory, and what it writes on each line. The milestone asks for the type, the hash, and the **final name only**.
4. **Find the loop.** `createTreeFromIndex` (or whatever they named it) builds the working list from the index, sorts it, and repeatedly calls `createTree` on the deepest unfinished directory. Note how it decides which directory is deepest, and what it returns.
5. **Predict before you run.** Write down the tree hashes you expect, using the next two sections, before you run their code.

These patterns deserve a note in your chart:

| What you see | Why it matters |
|---|---|
| `File.listFiles()`, `Files.walk`, or `isDirectory()` inside the tree code | The trees come from the folder on disk, not the index. Unstaged files leak into the snapshot. |
| `line.split(" ")` on an index line | It works, until a filename contains a space. Note it, and do not fail them for it. |
| No call to `Collections.sort`, `.sort(`, or a `TreeMap` | Line order depends on the order files were staged, so the hash is not guaranteed to repeat. |
| `writer.write(line + "\n")` for every line | The tree file ends with a newline, so its hash is not the hash the milestone expects. |
| The full path written into a tree line | The most common Part 3 bug. Every ancestor tree's hash is wrong. |
| An absolute path such as `/Users/theirname/...` | The code only runs on their machine. Change it so it runs, and record that you did. |

👉 <details>
<summary><h3>Activity: Map the Tree Methods — click to expand</h3></summary>

*Concept: Part 3 is three cooperating pieces — the index format, one directory's tree, and the loop that builds every tree — and you cannot judge any of them until you know which method is which.*

![Diagram of a Part 3 feature map: on the left, a source file Git.java listing methods such as add, createTree, createTreeFromIndex, and main; arrows connect each method to a row in a table of the three Part 3 milestones — GP-3.1 index stores relative paths, GP-3.2 createTree writes one directory's tree, GP-3.3 createTreeFromIndex builds the root — with columns for what the method takes in and what it writes. A red flag marks any call to File.listFiles, because trees must come from the index, never from the folder on disk.](assets/map-the-tree-methods.svg)

## Task

1. Open `Git.java` and any other `.java` files in your fork. Find `main`, and write down whether it does nothing, prints something, or calls the tree methods.
2. Copy this table into your notes and fill in one row per milestone, using the **actual method names** from their code:

   | Milestone | Method name(s) | Takes in | Produces or writes |
   |---|---|---|---|
   | GP-3.1 index stores relative paths | | | |
   | GP-3.2 one directory's tree | | | |
   | GP-3.3 root tree from the index | | | |

3. Find where the working list is built. Note its data type (a `List<String>`? an `ArrayList` of objects? a `TreeMap`?) and the line that **sorts** it. No sort is a finding: the tree files may come out in a different order on a different run.
4. Find how `createTree` decides which entries belong to a directory. Write down the expression, for example `path.substring(0, path.lastIndexOf('/'))`. Then find the line that writes each tree line and check whether it writes the final name or the whole path.
5. Search the whole project for `listFiles`, `Files.walk`, and `isDirectory`. Any of these inside the tree code means it is reading the folder on disk instead of the index. Write down the method name; this is the behavior 5 trap.
6. If `main` does not exercise these methods, create a new file `Verify.java` in your fork with a `main` that calls init, stages the test files, and calls their root-tree method. Do not edit their methods.

*(Standalone file: [activities/02-map-the-tree-methods.md](activities/02-map-the-tree-methods.md))*

</details>

---

## <font color="#388bfd">Black-Box Toolkit for Trees</font>

Run these in your terminal from the root of the fork, after their code has staged files and built trees.

| Question | Command | What to look for |
|---|---|---|
| Does the index store relative paths? | `cat -e git/index` | every line is `<40 hex> <path/with/folders>$`, not a bare filename |
| Is a file listed twice? | `cut -d' ' -f2- git/index \| sort \| uniq -d` | prints nothing; any output is a path that appears twice |
| What is in a tree file? | `cat git/objects/<hash>` | one line per direct child: `blob` or `tree`, a hash, and a name with no `/` in it |
| Does the tree file end in a newline? | `tail -c 1 git/objects/<hash> \| od -c` | the last byte is a letter or `.`, not `\n` |
| Is the tree's name its own hash? | `shasum git/objects/<hash>` (macOS) or `sha1sum git/objects/<hash>` (Linux/WSL) | the 40 characters match the filename exactly |
| Did a second run create new objects? | `ls git/objects \| wc -l` before and after | the count does not change when nothing was staged in between |

> **Tip:** Delete `git/` between experiments (`rm -rf git`) and run their init again, so each test starts from a known state.

---

## <font color="#388bfd">Hashing a Tree by Hand</font>

A tree file is plain text, so you can write it with `printf` and hash it yourself. Lines are sorted by name and joined with one newline, and there is no newline after the last line. The Docs example in [Trees](../Docs/trees.md) follows the same rule: its `scripts` tree hashes to `483b5e08…` only when the file has no trailing newline.

Build this test folder at the root of the fork. Stage the first three files, and **never** stage `scratch.txt`:

```bash
mkdir -p tree-test/docs
printf 'hello' > tree-test/docs/hello.txt
printf 'world' > tree-test/docs/world.txt
printf 'notes' > tree-test/notes.txt
printf 'scratch' > tree-test/scratch.txt
```

These are the right answers for that folder:

| Object | What it is | Expected name in `git/objects/` |
|---|---|---|
| `hello.txt` blob | the bytes `hello` | `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d` |
| `world.txt` blob | the bytes `world` | `7c211433f02071597741e6ff5a8ea34789abbf43` |
| `notes.txt` blob | the bytes `notes` | `3add7b9612102f2a7dbe4ed4fe886e07e847c24d` |
| `docs` tree | `blob aaf4… hello.txt` and `blob 7c21… world.txt` | `d5ff240dd607e36048326aaf7982a025debb0cd7` |
| `tree-test` tree, the root | `tree d5ff… docs` and `blob 3add… notes.txt` | `54c35b48b2551e71b9bc43f0d44264807fbf6cc9` |

Some programs add one more level above `tree-test`, a tree whose only line is `tree 54c35b48… tree-test`. That root is named `60a91a23cb87e720ab7cf5bc8f5f5c34da9c0e79`. Either root is fine, as long as the `tree-test` tree under it is correct.

A wrong hash is useful when you know which mistake makes it:

| Name in their `git/objects/` | What it means |
|---|---|
| `aa4c9c79cf6ad534fadfa67db12574cbfd4a3e21` | the `docs` tree ends with a newline |
| `048864846e5172fecc5a824fb81594ac0fcb3422` | the `docs` tree has full paths instead of names |
| `93309814fd7fef8ce1ef9d72fccde9f3ea0df77e` | the root includes `scratch.txt`, so the trees came from the folder, not the index |

👉 <details>
<summary><h3>Activity: Hash a Tree by Hand — click to expand</h3></summary>

*Concept: A tree's filename is the SHA-1 of its exact text, so you can write the tree file yourself, hash it in the terminal, and know the right answer before you run a classmate's code.*

![Diagram of a tree hashed by hand: two blob lines for hello.txt and world.txt, joined by one newline and with no newline after the last line, go into shasum and produce d5ff240dd607e36048326aaf7982a025debb0cd7, the docs tree. That hash becomes the line tree d5ff240d… docs, which joins blob 3add7b96… notes.txt and hashes to 54c35b48b2551e71b9bc43f0d44264807fbf6cc9, the tree-test tree. Two red near-misses show what a wrong answer looks like: a trailing newline gives aa4c9c79…, and writing full paths instead of names gives 04886484….](assets/hash-a-tree-by-hand.svg)

## Task

1. In your terminal, at the root of the fork, build the test folder. `printf` writes the exact bytes with no newline at the end, and `scratch.txt` is the file you will never stage:
   ```bash
   mkdir -p tree-test/docs
   printf 'hello' > tree-test/docs/hello.txt
   printf 'world' > tree-test/docs/world.txt
   printf 'notes' > tree-test/notes.txt
   printf 'scratch' > tree-test/scratch.txt
   ```
2. Hash the three blobs you will stage, and keep the output on screen:
   ```bash
   shasum tree-test/docs/hello.txt tree-test/docs/world.txt tree-test/notes.txt    # macOS
   sha1sum tree-test/docs/hello.txt tree-test/docs/world.txt tree-test/notes.txt   # Linux / WSL
   ```
   Expected: `aaf4c61d…434d` for hello, `7c211433…bf43` for world, `3add7b96…c24d` for notes.
3. Write the `docs` tree by hand and hash it. Its lines are sorted by name, they use the final name only, and there is no newline after the last line:
   ```bash
   printf 'blob aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d hello.txt\nblob 7c211433f02071597741e6ff5a8ea34789abbf43 world.txt' | shasum
   ```
   Expected: `d5ff240dd607e36048326aaf7982a025debb0cd7`. Use `sha1sum` instead of `shasum` on Linux or WSL.
4. Use that hash to write the `tree-test` tree, then hash it:
   ```bash
   printf 'tree d5ff240dd607e36048326aaf7982a025debb0cd7 docs\nblob 3add7b9612102f2a7dbe4ed4fe886e07e847c24d notes.txt' | shasum
   ```
   Expected: `54c35b48b2551e71b9bc43f0d44264807fbf6cc9`. `scratch.txt` is not in this tree, because it was never staged.
5. See the two near-misses. A trailing newline and full paths each change every character:
   ```bash
   printf 'blob aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d hello.txt\nblob 7c211433f02071597741e6ff5a8ea34789abbf43 world.txt\n' | shasum
   printf 'blob aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d tree-test/docs/hello.txt\nblob 7c211433f02071597741e6ff5a8ea34789abbf43 tree-test/docs/world.txt' | shasum
   ```
   Expected: `aa4c9c79…3e21` and `04886484…3422`. If one of these names shows up in their `git/objects/`, you know exactly which rule they broke.
6. Run the classmate's code: init, stage `hello.txt`, `world.txt`, and `notes.txt` (not `scratch.txt`), then build the root tree. Check the result:
   ```bash
   ls git/objects | grep -E 'd5ff240d|54c35b48|aa4c9c79|04886484|93309814'
   cat git/objects/d5ff240dd607e36048326aaf7982a025debb0cd7
   ```
   `93309814…` means `scratch.txt` leaked into the tree, so their code read the folder instead of the index.

*(Standalone file: [activities/03-hash-a-tree-by-hand.md](activities/03-hash-a-tree-by-hand.md))*

</details>

---

## <font color="#388bfd">Writing Evidence That Convinces</font>

Your chart has the six behaviors on the left and two answers per row, exactly like Part 2.

**Answer one: how well does it work, 1 to 5.**

| Rating | Meaning |
|---|---|
| **5** | Works exactly as described, and you proved it. The command and its output are recorded. |
| **4** | Works, but one small rule is broken, such as a trailing newline in a tree file. Say which. |
| **3** | Partly works. The core behavior happens, but something the milestone asked for does not. |
| **2** | Runs, but does the wrong thing. Record what it did instead. |
| **1** | Missing, fails, or could not be tested. Say which, and paste the error or explain how you know. |

**Answer two: one written cell covering three things.** Say how their code does it, with method names and data types. Say how you verified it, with the exact commands and the output you saw. Say what you changed to test it, or "nothing".

Here is a complete row:

| Behavior | 1–5 | Is it functional / verified the functionality? What was modified to get it working? |
|---|---|---|
| 4. `createTree` writes one directory's tree | 4 | **How:** `createTree(List<String> workingList, String dirPath)` keeps entries whose `path.substring(0, path.lastIndexOf('/'))` equals `dirPath`, writes `type + " " + hash + " " + name + "\n"` for each, then hashes the file with their Part 2 `sha1(String)`. **Verified:** built `tree-test/`, staged three files from `Verify.java`, called `createTree(list, "tree-test/docs")`. It returned `aa4c9c79cf6ad534fadfa67db12574cbfd4a3e21`, not the expected `d5ff240d…`. `tail -c 1 git/objects/aa4c9c79… \| od -c` printed `\n`. **Modified:** nothing beyond adding `Verify.java`. |

The row names a method, shows a command and its output, and explains the gap between expected and actual. It does not say "seems fine" anywhere.

---

## <font color="#388bfd">What You Are Verifying</font>

The assignment chart lists these six behaviors in this order. They are the Trees assignment's success criteria.

1. **Index stores relative paths.** After staging `tree-test/docs/hello.txt`, its index line reads `aaf4c61d… tree-test/docs/hello.txt`, not a bare filename.
2. **No duplicate entries.** Staging the same unchanged file twice leaves exactly one index line for it.
3. **A modified file replaces its entry.** After `printf 'hello again' > tree-test/docs/hello.txt` and staging it again, its line carries `714d500fdb9ddeb5b957022131ac8a13c437a3bd`, the old hash is gone, and there is still one line for it.
4. **`createTree` writes one directory's tree.** For `tree-test/docs` it writes two lines, `blob` + hash + final name, into a file named `d5ff240dd607e36048326aaf7982a025debb0cd7`, and returns that hash.
5. **`createTreeFromIndex` builds the root from staged files only.** With `scratch.txt` on disk but never staged, the root tree is `54c35b48…` (or `60a91a23…` with one extra level) and contains no `scratch.txt`.
6. **Tree hashes are deterministic.** Running the root-tree method twice on an unchanged index returns the same hash, and the number of files in `git/objects/` does not change.

> **Note:** Behavior 3 changes `hello.txt`, so run it last, or rebuild `tree-test/` with the `printf` commands before you test behaviors 4 through 6.

---

## <font color="#388bfd">Renaming for Sense</font>

As in Part 2, the second half of the assignment is renaming, and only renaming, on a branch in your fork. Tree code has its own vocabulary, and good names use it:

| Ask | Fix | Example |
|---|---|---|
| **What does this variable hold?** | Name it for its contents | `List<String> list` holding working-list lines → `workingList` · `String s` holding a directory path → `dirPath` · `String l` holding one tree line → `treeLine` |
| **What does this method do?** | Name it for its one job | `makeTree()` that builds every tree from the index → `createTreeFromIndex()` · `getDir(String p)` that drops the final `/name` → `parentDirectory(String path)` · `helper()` that picks the next directory to collapse → `deepestUnfinishedDirectory()` |

The same three rules apply. Rename only, with no logic changes. Rename with VS Code's **Rename Symbol** (F2), never find-and-replace. Prove nothing changed by running `Verify.java` again: the same tree hashes must come out.

---

## <font color="#388bfd">Reviewer Rules</font>

- **In Part 1, verify, don't fix.** You may add `Verify.java`, and you may change a hardcoded path so the code runs on your machine. You may not rewrite their methods.
- **In Part 2, rename, only rename.** The tree hashes before and after must be identical.
- **The project rules still apply.** No AI tools, and none of their code goes into your own `git-project-YOURNAME`.
- **Describe behavior, not people.** "The `docs` tree hashes to `aa4c9c79…` because `createTree` writes a newline after the last line" is a finding. "This is wrong" is not.
- **Expected hashes are evidence.** If you write that a hash is wrong, write the hash you expected and how you computed it.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Fork a classmate's repository, clone the fork, and confirm with `git remote -v` that `origin` points at your own account.
- [ ] Find the methods that implement GP-3.1, GP-3.2, and GP-3.3 in a codebase you did not write.
- [ ] Read a tree file with `cat` and say what each of its lines represents.

### <font color="#79c0ff">Intermediate</font>

- [ ] Write a tree file by hand with `printf`, hash it in the terminal, and compare the result to a classmate's `git/objects/`.
- [ ] Show, with commands and their output, that staging an unchanged file twice leaves one index line and staging a modified file replaces its hash.
- [ ] Explain why a file that was never staged must not appear in any tree, and prove whether it does in a classmate's code.
- [ ] Rename a classmate's tree variables and methods using the lesson's vocabulary, without changing any tree hash.

### <font color="#79c0ff">Advanced</font>

- [ ] Given a wrong tree hash, work out which rule was broken by hashing the likely mistakes yourself.
- [ ] Explain why one wrong character in the `docs` tree changes the root tree's hash.
- [ ] Prove whether a classmate's root-tree method is deterministic by running it twice and comparing hashes and object counts.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Extend your `Verify.java` so it prints PASS or FAIL for all six behaviors, then run it unchanged against a second classmate's fork.
- [ ] Paste their `git/index` into the [Index-to-Tree Visualizer](https://learnhw.web.app/static/code/widgets/index-tree/index-tree.html) and compare its tree hashes with the ones their code wrote.
- [ ] In a real Git repository, run `git cat-file -p HEAD^{tree}` to see a real tree. Find two ways its lines differ from the tree files in this project.

---

[Assignment](ASSIGNMENT.md)

← [Trees](../Trees/) — Next: [Commits](../Commits/)
