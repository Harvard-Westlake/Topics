# Assignment — Peer Tree Verification

*Lesson: [Peer Tree Verification](README.md)*

**Due:** End of class today

---

## Table of Contents

1. [Part 1: fork a classmate's Part 3, get it running, and verify it](#part-1-verify)
2. [The verification chart you fill out — six behaviors, two answers each](#verification-chart)
3. [Part 2: rename their tree variables and methods so they make sense](#part-2-rename)
4. [Four checks before you submit](#success-criteria)
5. [What to submit on the Hub: the chart and your commit URL](#submission)

---

## Part 1: Verify

1. Your teacher assigns you a classmate's `git-project-THEIRNAME` repository at random. It will not be the classmate you reviewed in Part 2.
2. In your terminal, fork it and clone your fork in one step, then confirm the remotes:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/git-project-THEIRNAME --clone
   cd git-project-THEIRNAME
   git remote -v
   ```
   `origin` must be under your username (your fork) and `upstream` under theirs (the original).
3. Open the folder in **VS Code**. Read their `README.md`, then the tree code: the index writer, `createTree`, and the method that builds the root tree.
4. Get it running as best you can. If `main` does not call the tree methods, add a `Verify.java` with a `main` that does. If a hardcoded path stops it on your machine, change the path. Do not change how their methods work.
5. Build the lesson's `tree-test/` folder and verify each of the six behaviors in the chart **one way or another**: run it and inspect `git/`, or read the code path and predict the result, then check. The lesson's [expected hashes](README.md#hashing-a-tree-by-hand) are the right answers, and its [black-box toolkit](README.md#black-box-toolkit-for-trees) has the commands.
6. Commit what you added to a **new branch** in your fork, for example `tree-review-YOURNAME`, and push it:
   ```bash
   git checkout -b tree-review-YOURNAME
   git add .
   git commit -m "Add Verify.java driver to run THEIRNAME's Part 3"
   git push -u origin tree-review-YOURNAME
   ```

Get your copy of the chart: download [verification-table.xlsx](assets/verification-table.xlsx) and open it in Excel, Numbers, or Google Sheets (**File → Import**), or copy the table below into a document. The rows are identical either way.

---

## Verification Chart

One row per behavior, two answers per row. The left column is fixed. Hashes are shortened here; the full values are in the lesson's [expected hashes](README.md#hashing-a-tree-by-hand).

- **Rating (1–5, 5 is best):** 5 = works exactly as described and you proved it · 4 = works, one small rule broken (a trailing newline in a tree file) · 3 = partly works · 2 = runs but does the wrong thing · 1 = missing, fails, or could not be tested (say which).
- **Notes:** **How** their code does it (method names, approach, data types) · how you **verified** it (exact commands or calls, and what you saw) · what you **modified** to test it, or "nothing".

| Behavior to verify | Rating (1–5) | Notes |
|---|---|---|
| **1. Index stores relative paths** — after staging `tree-test/docs/hello.txt`, its index line is `aaf4c61d… tree-test/docs/hello.txt`, not a bare filename. | | **How:**<br>**Verified:**<br>**Modified:** |
| **2. No duplicate entries** — staging the same unchanged file twice leaves exactly one index line for it. | | **How:**<br>**Verified:**<br>**Modified:** |
| **3. A modified file replaces its entry** — after `printf 'hello again'` into `hello.txt` and staging it again, its line carries `714d500f…`, the old hash is gone, and there is one line for it. | | **How:**<br>**Verified:**<br>**Modified:** |
| **4. `createTree` writes one directory's tree** — for `tree-test/docs` it writes two lines (`blob`, hash, final name only) into `git/objects/d5ff240d…` and returns that hash. | | **How:**<br>**Verified:**<br>**Modified:** |
| **5. Root tree from staged files only** — with `scratch.txt` never staged, the root tree is `54c35b48…` (or `60a91a23…` with one extra level) and no tree lists `scratch.txt`. | | **How:**<br>**Verified:**<br>**Modified:** |
| **6. Deterministic** — running the root-tree method twice on an unchanged index returns the same hash, and `git/objects/` gains no files. | | **How:**<br>**Verified:**<br>**Modified:** |

> **Note:** Behavior 3 edits `hello.txt`. Test it last, or rebuild `tree-test/` with the lesson's `printf` commands before testing behaviors 4–6, or the expected tree hashes will not match.

---

## Part 2: Rename

Their code works as well as it works. Now make it readable. On your branch, go through every variable and method name in the tree code and ask two questions:

- **"What does this variable hold?"** The answer is its name. A `List<String> list` of working-list lines is `workingList`. A `String s` holding a directory is `dirPath`. A `String l` holding one tree line is `treeLine`.
- **"What does this method do?"** That is what it should be called. A `getDir(String p)` that drops the final `/name` is `parentDirectory(String path)`. A `helper()` that picks the next directory to collapse is `deepestUnfinishedDirectory()`.

Rules for renaming:

- **Rename only.** No logic changes, no reordering, no fixes. If you find a bug, describe it in the chart.
- **Use VS Code's Rename Symbol** (right-click the name → Rename Symbol, or F2) so every reference updates together.
- **Prove nothing changed.** Re-run your `Verify.java` after renaming. The same tree hashes must come out.
- **Commit and push** on the same branch:
  ```bash
  git add .
  git commit -m "Rename tree variables and methods so they say what they hold and do"
  git push
  ```
  On GitHub, open your fork → **Commits** → this commit, and copy its URL for the submission.

---

## Success Criteria

- [ ] **Forked theirs and cloned your fork of theirs** — `git remote -v` shows `origin` under your username and `upstream` under theirs
- [ ] **Got it running and verified each behavior one way or another** — every chart row has a 1–5 and a written answer, and every wrong hash is reported next to the hash you expected
- [ ] **Committed to a new branch after you got their code running as best you can**
- [ ] **Renamed tree variables and methods to be sensible** — tree hashes unchanged, committed and pushed

---

## Submission

Submit **both** on the Hub: the entire chart and the URL of your rename commit.

### Chart

Upload your filled-in `verification-table.xlsx` (or a PDF export), or paste a **view-only** link to your Google Sheet copy.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Classmate's repository:   https://github.com/THEIR-USERNAME/git-project-THEIRNAME
My fork and branch:       https://github.com/YOUR-USERNAME/git-project-THEIRNAME/tree/tree-review-YOURNAME
Rename commit URL:        https://github.com/YOUR-USERNAME/git-project-THEIRNAME/commit/SHA
```
