# Assignment — Peer Code Verification

*Lesson: [Peer Code Verification](README.md)*

**Due:** End of class today

---

## Table of Contents

1. [Get a classmate's repository: fork, clone your fork, open it](#setup)
2. [What reviewers may and may not change](#rules)
3. [The verification table you fill in — nine behaviors, evidence on the right](#verification-table)
4. [Success criteria](#success-criteria)
5. [What to submit on the Hub](#submission)

---

## Setup

1. Your teacher assigns you a classmate's `git-project-THEIRNAME` repository at random. You do not pick.
2. On GitHub, **Fork** it into your own account. Keep the name.
3. In your terminal, clone **your fork** and confirm `origin` is yours:
   ```bash
   cd ~/HTCS_Projects
   git clone git@github.com:YOUR-USERNAME/git-project-THEIRNAME.git
   cd git-project-THEIRNAME
   git remote -v
   ```
4. Open the folder in your Java editor. Read their `README.md` first, then `Git.java`.
5. Get your copy of the table: download the spreadsheet — [verification-table.xlsx](assets/verification-table.xlsx) — and open it in Excel, Numbers, or Google Sheets (**File → Import**). If you prefer, copy the markdown table below into a document instead. The rows are identical either way.

---

## Rules

- **Verify, don't fix.** You may add a driver class (`Verify.java`) with a `main` that calls their methods, and you may change a hardcoded path so their code runs on your machine. You may not rewrite their methods. Record every change you make in the last column.
- **Evidence for every row.** Each row names the method responsible and the approach it takes, and shows the exact commands or calls you ran with the output you saw. Paste output; do not paraphrase it.
- **Use the fixed verdicts.** Works · Partly · Fails · Could not test · Not implemented. The lesson's [evidence section](README.md#writing-evidence-that-convinces) defines each one.
- **Project rules apply.** No AI tools. None of their code goes into your own project. Anything you commit goes to your fork only — never open a pull request to their repository today.
- **Start clean between experiments.** Delete `git/` and run their `init()` again so each behavior is tested from a known state.

> **Note:** Behavior 9 (compression) was an optional stretch milestone. Most repositories will not have it — **Not implemented**, with a sentence on how you know, is a complete answer for that row.

---

## Verification Table

Fill in every white cell for all nine rows. The behaviors on the left are fixed; the three columns on the right are yours.

| # | Behavior to verify | Verdict | How their code does it (method names, approach, data types) | How I verified it (exact commands or calls, and what you saw) | What I changed to test it (or "nothing") |
|---|---|---|---|---|---|
| 1 | **Initialize** — `init()` creates `git/`, `git/objects/`, `git/index`, and `git/HEAD`. Running it a second time reports that the repository already exists and changes nothing. | | | | |
| 2 | **Stage a file into a blob** — adding a file creates `git/objects/<hash>` whose content is byte for byte identical to the original file. | | | | |
| 3 | **Hash correctness** — the blob's filename is the true SHA-1 of the content. A file containing exactly `sha1test` (8 bytes, no newline) must produce `12c4c60ee087ae0f12dc6abc88495e459f6f2654`, the same as `printf 'sha1test' \| shasum` or `echo -n "sha1test" \| sha1sum`. | | | | |
| 4 | **Index tracks the file** — after adding a file, `git/index` contains a line for that file. | | | | |
| 5 | **Index line format** — each line is `<hash>`, one space, `<relative path>`. The hash matches the blob's filename. No trailing space. No blank final line. | | | | |
| 6 | **Multiple entries** — adding several different files produces one correct line per file, each on its own line. | | | | |
| 7 | **Duplicate content** — two files with identical content at different paths produce two index lines with the same hash but exactly one blob in `git/objects/`. | | | | |
| 8 | **Modify and re-add** — changing a file's content and adding it again replaces its index line with the new hash (no duplicate path) and writes a new blob. The old blob remains. | | | | |
| 9 | **Compression** — blob content is compressed on disk and decompresses back to the original. *(Optional stretch milestone — Not implemented is a legitimate verdict.)* | | | | |

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Forked, not cloned from the original** — `git remote -v` in your working copy shows your own username on both `origin` lines
- [ ] **All nine rows have a verdict** — every verdict is one of the five fixed words
- [ ] **Every row names the method responsible** — even a Fails or Not implemented row says where you looked and what you found or did not find
- [ ] **Every Works or Partly row shows a command and its output** — pasted, not described
- [ ] **Row 3 includes the hash comparison** — your own `shasum`/`sha1sum` result next to the blob filename their program produced
- [ ] **Rows 7 and 8 include blob and index counts** — how many files in `git/objects/` and how many lines in `git/index` before and after
- [ ] **Every change you made to their repository is listed** — in the last column, or the word "nothing"
- [ ] **No edits to their methods** — your fork's diff against theirs contains only your driver class and any path fix you recorded

---

## Submission

Submit **both** on the Hub: the completed table and the text response below.

### Table

Upload your filled-in `verification-table.xlsx` (or a PDF export of it), or paste a **view-only** link to your Google Sheet copy.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Classmate's repository:      https://github.com/THEIR-USERNAME/git-project-THEIRNAME
My fork:                     https://github.com/YOUR-USERNAME/git-project-THEIRNAME
Compiled and ran as cloned:  yes / no
What I changed to run it:    (file names and one line each, or "nothing")
Verdicts 1–9:                1 Works, 2 Works, 3 Partly, ...
Most surprising finding:     one sentence
```
