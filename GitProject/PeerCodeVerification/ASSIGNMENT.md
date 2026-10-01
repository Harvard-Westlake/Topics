# Assignment — Peer Code Verification

*Lesson: [Peer Code Verification](README.md)*

**Due:** End of class today

---

## Table of Contents

1. [Part 1: fork a classmate's code, get it running, and verify it](#part-1-verify)
2. [The verification chart you fill out — six behaviors, two answers each](#verification-chart)
3. [Part 2: rename their variables and methods so they make sense](#part-2-rename)
4. [Four checks before you submit](#success-criteria)
5. [What to submit on the Hub: the chart and your commit URL](#submission)

---

## Part 1: Verify

1. Your teacher assigns you a classmate's `git-project-THEIRNAME` repository at random.
2. In your terminal, fork it and clone your fork in one step, then confirm the remotes:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/git-project-THEIRNAME --clone
   cd git-project-THEIRNAME
   git remote -v
   ```
   `origin` must be under your username (your fork) and `upstream` under theirs (the original).
3. Open the folder in **VS Code**. Read their `README.md`, then `Git.java`.
4. Get it running as best you can. If `main` is empty, add a `Verify.java` with a `main` that calls their methods. If a hardcoded path stops it on your machine, change the path. Do not change how their methods work — that is Part 2, and it is renaming only.
5. Verify each of the six behaviors in the chart **one way or another**: run it and inspect `git/`, or read the code path and predict what it does, then check. The lesson's [black-box toolkit](README.md#two-ways-to-verify-a-feature) has the commands.
6. Commit what you added to a **new branch** in your fork, for example `peer-review-YOURNAME`, and push it:
   ```bash
   git checkout -b peer-review-YOURNAME
   git add .
   git commit -m "Add Verify.java driver to run THEIRNAME's Part 2"
   git push -u origin peer-review-YOURNAME
   ```

Get your copy of the chart: download [verification-table.xlsx](assets/verification-table.xlsx) and open it in Excel, Numbers, or Google Sheets (**File → Import**), or copy the table below into a document. The rows are identical either way.

---

## Verification Chart

One row per behavior, two answers per row. The left column is fixed.

**How well does it work (1–5, 5 is best):** 5 = works exactly as described and you proved it · 4 = works, one small rule broken (a trailing space, a blank last line) · 3 = partly works · 2 = runs but does the wrong thing · 1 = missing, fails, or could not be tested (say which).

| Behavior to verify | How well does it work? (1–5) | Is it functional / verified the functionality? What was modified to get it working?<br>*How their code does it (method names, approach, data types) · how you verified it (exact commands or calls, and what you saw) · what you changed to test it, or "nothing"* |
|---|---|---|
| **1. Initialize** — `init()` creates `git/`, `git/objects/`, `git/index`, and `git/HEAD`. Running it a second time reports that the repository already exists and changes nothing. | | |
| **2. Stage a file into a blob** — adding a file creates `git/objects/<hash>` whose content is byte for byte identical to the original file. | | |
| **3. Hash correctness** — the blob's filename is the true SHA-1 of the content. A file containing exactly `sha1test` (8 bytes, no newline) must produce `12c4c60ee087ae0f12dc6abc88495e459f6f2654`, the same as `printf 'sha1test' \| shasum` or `echo -n "sha1test" \| sha1sum`. | | |
| **4. Index tracks the file** — after adding a file, `git/index` contains a line for that file. | | |
| **5. Duplicate content** — two files with identical content at different paths produce two index lines with the same hash but exactly one blob in `git/objects/`. | | |
| **6. Compression** — blob content is compressed on disk and decompresses back to the original. *(Optional stretch milestone — a 1 with the note "not implemented" is a complete answer.)* | | |

---

## Part 2: Rename

Their code works as well as it works. Now make it readable. On your branch, go through every variable and method name and ask two questions:

- **"What does this variable hold?"** The answer is its name. A `String s` that holds a SHA-1 is `hash`. A `File f` that is the blob being written is `blobFile`. An `int i` walking index lines is `lineNumber`.
- **"What does this method do?"** That is what it should be called. A `doStuff()` that appends one line to the index is `appendIndexEntry()`. A `helper()` that turns bytes into hex is `bytesToHex()`.

Rules for renaming:

- **Rename only.** No logic changes, no reordering, no "while I'm here" fixes. If you find a bug, describe it in the chart; do not fix it.
- **Use VS Code's Rename Symbol** (right-click the name → Rename Symbol, or F2) so every reference updates together and nothing breaks.
- **Prove nothing changed.** Re-run your `Verify.java` after renaming. Same blobs, same index, same output.
- **Commit and push** on the same branch:
  ```bash
  git add .
  git commit -m "Rename variables and methods so they say what they hold and do"
  git push
  ```
  On GitHub, open your fork → **Commits** → this commit, and copy its URL for the submission.

---

## Success Criteria

- [ ] **Forked theirs and cloned your fork of theirs** — `git remote -v` shows `origin` under your username and `upstream` under theirs
- [ ] **Loaded it in VS Code, tried to run it, and verified each behavior one way or another** — every chart row has a 1–5 and a written answer
- [ ] **Committed to a new branch after you got their code running as best you can**
- [ ] **Renamed and refactored variable and method names to be sensible** — behavior unchanged, committed and pushed

---

## Submission

Submit **both** on the Hub: the entire chart and the URL of your rename commit.

### Chart

Upload your filled-in `verification-table.xlsx` (or a PDF export), or paste a **view-only** link to your Google Sheet copy.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Classmate's repository:   https://github.com/THEIR-USERNAME/git-project-THEIRNAME
My fork and branch:       https://github.com/YOUR-USERNAME/git-project-THEIRNAME/tree/peer-review-YOURNAME
Rename commit URL:        https://github.com/YOUR-USERNAME/git-project-THEIRNAME/commit/SHA
```
