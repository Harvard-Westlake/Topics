<div align="center">

# Peer Tree Verification
*<font color="#8b949e">Fork a classmate's Part 3, hash their trees by hand, and prove which behaviors actually work</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

Where you are in the project:

- **You can save a file in Git.** Your code turns a file's contents into a **blob** in `git/objects/`, named by its SHA-1 hash (Part 2).
- **You can now save a whole folder.** Your code reads the **index** and writes **tree** files that list what is inside each folder (Part 3).
- **Today you check a classmate's version.** You copy their code, get it running, and prove which parts work, with evidence anyone could repeat.

## <font color="#388bfd">Table of Contents</font>

1. [Fork and clone a classmate's repository, in the terminal or in GitKraken](#1-fork-and-clone-a-classmates-repository)
2. [Run their code and verify the six tree behaviors: hash trees by hand and grade each behavior 1 to 5](#2-run-and-verify)
3. [Optional: rename their code so it makes sense, and the rules for what you may fix](#3-optional-rename-and-fix)

---

## <font color="#388bfd">1. Fork and Clone a Classmate's Repository</font>

Your teacher assigns you a classmate. You make your own copy of their repository (a **fork**), then download that copy to your laptop (a **clone**). You never need their permission, and nothing you do touches their original.

Everyone forked once in Part 2, so the repository you get may already be a fork of someone else's. That is fine. You review whatever code your classmate worked on.

**In the terminal:**

```bash
cd ~/HTCS_Projects
gh repo fork THEIR-USERNAME/THEIR-REPO-NAME --clone --fork-name ANY-NAME-YOU-WANT
cd ANY-NAME-YOU-WANT
git remote -v
```

`origin` must be under **your** username and `upstream` under theirs.

**In GitKraken:** open the classmate's repository on github.com and click **Fork**. Then in GitKraken choose **File → Clone Repo → GitHub.com**, pick your fork, and clone it into `HTCS_Projects`. GitKraken adds the classmate's original as a remote when you open the fork; if it does not, add it in the **Remote** panel with **+** and name it `upstream`.

Then open the folder in VS Code and read their `README.md` before any `.java` file, because it is their list of claims.

> **Note:** You never push to the classmate's repository and you never open a pull request to it. Anything you add or change stays in your fork and gets recorded in your chart.

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Fork, Clone, Open</strong></summary>

*Concept: Grab a classmate's code without asking their permission, and start working from your own copy of it.*

![Diagram of the fork-then-clone path: on the left, the classmate's repository THEIR-REPO-NAME on GitHub; a Fork arrow copies it into your account as YOUR-USERNAME/THEIR-REPO-NAME, labeled forked from the original; a gh repo fork --clone arrow brings that fork down to your laptop in HTCS_Projects, where origin points at your fork and upstream at the original. A crossed-out arrow from the laptop straight to the classmate's repository is marked push refused. You never write to their repo.](assets/fork-clone-open.svg)

## Task

1. Wait for your teacher to assign you a classmate. Open their repository on GitHub and confirm it belongs to that classmate, not to you, and not to the classmate whose code you reviewed in Part 2. Everyone forked once in Part 2, so the repository you get is often a fork itself. Under its name you may see a line like this:
   ```
   THEIR-USERNAME/THEIR-REPO-NAME
   forked from ANOTHER-CLASSMATE/THEIR-REPO-NAME
   ```
   That is expected. You are reviewing the code your classmate worked on, wherever it started.
2. In your terminal, go to your projects folder, then fork the repository and clone your fork in one step. `--fork-name` lets you call your copy whatever you want, which matters if you already have a repository with the same name:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/THEIR-REPO-NAME --clone --fork-name ANY-NAME-YOU-WANT
   cd ANY-NAME-YOU-WANT
   ```
   On GitHub, your copy now shows **forked from THEIR-USERNAME/THEIR-REPO-NAME** under its title.
3. Prove where the remotes point:
   ```bash
   git remote -v
   ```
   You should see four lines like these:
   ```
   origin    git@github.com:YOUR-USERNAME/ANY-NAME-YOU-WANT.git (fetch)
   origin    git@github.com:YOUR-USERNAME/ANY-NAME-YOU-WANT.git (push)
   upstream  git@github.com:THEIR-USERNAME/THEIR-REPO-NAME.git (fetch)
   upstream  git@github.com:THEIR-USERNAME/THEIR-REPO-NAME.git (push)
   ```
   `origin` is under **your** username (your fork) and `upstream` is under the classmate's (the original). If `origin` shows the classmate's username, you cloned the original. Delete the folder and run the fork command again.
4. Optional: check that your classmate worked on this recently.
   ```bash
   git log
   ```
   Look at the `Date:` lines. The newest commit is at the top:
   <pre>
   commit 9f2c1e7a4b8d0c3e5f6a7b8c9d0e1f2a3b4c5d6e (HEAD -> main, origin/main)
   Author: Their Name &lt;them@example.com&gt;
   <strong><font color="#f0883e">Date:   Wed Oct 7 21:14:03 2026 -0700</font></strong>

       finished root tree

   commit 41d07be29c8a51f3e6b0d2a7c94e18f5b3a6d720
   Author: Their Name &lt;them@example.com&gt;
   <strong><font color="#f0883e">Date:   Mon Oct 5 19:02:47 2026 -0700</font></strong>

       index paths
   </pre>
   Recent dates mean they were working on it. Do not rely on the commit messages; classmates do not always label them clearly. Press `q` to leave the log.
5. Open the folder in VS Code and read their `README.md` first. Write down, in one line each, every tree-related method it claims exists.

*(Standalone file: [activities/01-fork-clone-open.md](activities/01-fork-clone-open.md))*

</details>

---

## <font color="#388bfd">2. Run and Verify</font>

Get their program running, then prove which of the six tree behaviors work. You know the right answers ahead of time because you can hash trees by hand, and you record what you find in a chart.

### <font color="#79c0ff">Get Their Code Running</font>

Before you can judge their trees, you need their program to run on your laptop. Work through these in order and stop to write down what you find:

1. **Figure out how to run it.** Find their `main` method. If it does not call the tree methods, add a `Verify.java` with a `main` that does. If a hardcoded path stops it on your machine, change the path.
2. **Give it an index.** Stage a few files with their code, then open `git/index`. Each line should be a hash and a path like `tree-test/docs/hello.txt`, not just `hello.txt`.
3. **Check the files and folders it makes.** After it runs, `git/objects/` should hold one blob per staged file and one tree per folder.
4. **Try one harder folder.** Make a folder a few levels deep with several files, stage it, and build the trees. If the result looks right, their code probably handles nesting. How you build that folder is up to you.

Pull up the [Index-to-Tree Visualizer](https://learnhw.web.app/static/code/widgets/index-tree/index-tree.html) in another tab. Paste in any index their code writes and watch the correct trees get built, so you can compare.

### <font color="#79c0ff">What Should You Verify?</font>

Six things. They are the Trees assignment's success criteria, and the assignment chart lists them in this order:

1. **Index stores relative paths.** After staging `tree-test/docs/hello.txt`, its index line reads `aaf4c61d… tree-test/docs/hello.txt`, not a bare filename.
2. **No duplicate entries.** Staging the same unchanged file twice leaves exactly one index line for it.
3. **A modified file replaces its entry.** After `printf 'hello again' > tree-test/docs/hello.txt` and staging it again, its line carries `714d500fdb9ddeb5b957022131ac8a13c437a3bd`, the old hash is gone, and there is still one line for it.
4. **`createTree` writes one directory's tree.** For `tree-test/docs` it writes two lines, `blob` + hash + final name, into a file named `d5ff240dd607e36048326aaf7982a025debb0cd7`, and returns that hash.
5. **`createTreeFromIndex` builds the root from staged files only.** With `scratch.txt` on disk but never staged, the root tree is `54c35b48…` (or `60a91a23…` with one extra level) and contains no `scratch.txt`.
6. **Tree hashes are deterministic.** Running the root-tree method twice on an unchanged index returns the same hash, and the number of files in `git/objects/` does not change.

> **Note:** Behavior 3 changes `hello.txt`, so run it last, or rebuild `tree-test/` with the `printf` commands before you test behaviors 4 through 6.

Trees are harder to judge than blobs because one wrong character in one tree changes the hash of every tree above it. These are the usual mistakes and what they look like:

| If this is wrong | This is what you see |
|---|---|
| The index stores bare filenames | The program cannot tell `docs/hello.txt` from `hello.txt`, so trees for different folders merge |
| A tree line holds the full path instead of the final name | That tree's hash is wrong, so every tree above it is wrong too |
| The tree file ends with an extra newline | Same content to your eye, a completely different hash |
| The working list is never sorted | The lines can come out in a different order, so the hash can change between runs |
| The trees are built from the folder on disk | Files that were never staged show up in the snapshot |

Part 4 hands you a classmate's codebase and asks you to build commits on top of their trees. A commit stores one root tree hash, so if that hash is wrong, every commit built on it is wrong. Today is practice at catching that before you depend on it.

### <font color="#79c0ff">Hash a Tree by Hand</font>

A tree file is plain text, and its name is supposed to be the SHA-1 hash of that text. That means you can check any tree their code wrote, without trusting their code:

1. Get their code running and find their index with `cat git/index`.
2. Have their code build the trees from that index.
3. Open any file in `git/objects/` whose lines start with `blob` or `tree`. That is a tree file.
4. Hash it and compare the result to its filename:
   ```bash
   shasum git/objects/THE-FILE-NAME     # macOS
   sha1sum git/objects/THE-FILE-NAME    # Linux / WSL
   ```
   If the hash matches the filename, they hashed exactly what they wrote. To check that what they wrote is *right*, select all of its text, then type the lines yourself with `printf` (below) and hash that.

Tree lines are sorted by name and joined with one newline, and there is no newline after the last line. The Docs example in [Trees](../Docs/trees.md) follows the same rule: its `scripts` tree hashes to `483b5e08…` only when the file has no trailing newline.

For a test with known answers, build this folder at the root of the fork. Stage the first three files, and **never** stage `scratch.txt`:

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

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Hash a Tree by Hand</strong></summary>

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

*(Standalone file: [activities/02-hash-a-tree-by-hand.md](activities/02-hash-a-tree-by-hand.md))*

</details>

### <font color="#79c0ff">Grade Each Behavior in the Chart</font>

Your chart has the six behaviors on the left and two answers per row, exactly like Part 2.

**Answer one: how well does it work, 1 to 5.**

| Rating | Meaning |
|---|---|
| **5** | Works exactly as described, and you proved it. The command and its output are recorded. |
| **4** | Works, but one small rule is broken, such as a trailing newline in a tree file. Say which. |
| **3** | Partly works. The core behavior happens, but something the milestone asked for does not. |
| **2** | Runs, but does the wrong thing. Record what it did instead. |
| **1** | Missing, fails, or could not be tested. Say which, and paste the error or explain how you know. |

**Answer two: short bullets, not paragraphs.** Under three labels, write a few quick notes each:

- **How:** the data structures it uses, how it reads its input, how it splits or sorts things.
- **Verified:** the command or call you ran, and what came out.
- **Modified:** what you changed so you could test it, or "nothing".

Here is a complete row:

| Behavior | 1–5 | Notes |
|---|---|---|
| 4. `createTree` writes one directory's tree | 4 | **How:**<br>• stores the index as a `List<String> workingList`<br>• keeps lines whose parent folder equals `dirPath`<br>• writes `type hash name` per line, each ending in `\n`<br>• hashes with their Part 2 `sha1(String)`<br>**Verified:**<br>• called `createTree(list, "tree-test/docs")` from `Verify.java`<br>• got `aa4c9c79…`, expected `d5ff240d…`<br>• `tail -c 1` on that file shows `\n`: an extra newline at the end<br>**Modified:**<br>• nothing beyond adding `Verify.java` |

Every bullet names a method, a command, or a hash. None of them says "seems fine".

---

## <font color="#388bfd">3. Optional: Rename and Fix</font>

Once the chart is done, make their code easier to read without changing what it does.

### <font color="#79c0ff">Rename for Sense</font>

As in Part 2, the second half of the assignment is renaming, and only renaming, on a branch in your fork. Tree code has its own vocabulary, and good names use it:

| Ask | Fix | Example |
|---|---|---|
| **What does this variable hold?** | Name it for its contents | `List<String> list` holding working-list lines → `workingList` · `String s` holding a directory path → `dirPath` · `String l` holding one tree line → `treeLine` |
| **What does this method do?** | Name it for its one job | `makeTree()` that builds every tree from the index → `createTreeFromIndex()` · `getDir(String p)` that drops the final `/name` → `parentDirectory(String path)` · `helper()` that picks the next directory to collapse → `deepestUnfinishedDirectory()` |

The same three rules apply. Rename only, with no logic changes; any fix belongs in Part 1. Rename with VS Code's **Rename Symbol** (F2), never find-and-replace. Prove nothing changed by running `Verify.java` again: the same tree hashes must come out.

### <font color="#79c0ff">Reviewer Rules</font>

- **In Part 1, fix what is broken, and only that.** You may add `Verify.java`, change a hardcoded path, and fix code that does not work so you can test the rest. You may not change how a working method does its job, even if you would have written it differently. Record every fix in the chart's **Modified** notes.
- **In Part 2, rename, only rename.** Fixes belong in Part 1. The tree hashes before and after renaming must be identical.
- **The project rules still apply.** No AI tools, and none of their code goes into your own repository.
- **Describe behavior, not people.** "The `docs` tree hashes to `aa4c9c79…` because `createTree` writes a newline after the last line" is a finding. "This is wrong" is not.
- **Expected hashes are evidence.** If you write that a hash is wrong, write the hash you expected and how you computed it.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Fork a classmate's repository and confirm with `git remote -v` that `origin` is yours and `upstream` is theirs.
- [ ] Get their code running and verify the six tree behaviors against hashes you computed by hand.
- [ ] Grade each behavior 1 to 5 in the chart, with the command you ran and what you saw.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Create the most complex tree case you can think of and verify that it works on their code.

---

[Assignment](ASSIGNMENT.md)

← [Trees](../Trees/) — Next: [Commits](../Commits/)
