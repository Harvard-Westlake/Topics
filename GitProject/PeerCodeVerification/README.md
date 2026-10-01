<div align="center">

# Peer Code Verification
*<font color="#8b949e">Fork a classmate's Git, read it cold, and prove which behaviors actually work</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

For the last three classes you built `init()`, a SHA-1 hasher, blob files, and an index — and you know exactly where the rough edges are in your own code. Today you trade repositories with a classmate you did not pick. You will fork their Part 2 work, clone your fork, and spend the period finding out which of their features actually do what the milestones asked, with evidence you could show a stranger. Nobody is grading their code today. You are practicing the skill that Part 4 of this project (and every real software job) demands: reading code you did not write, working out how it fits together, and separating what it *claims* to do from what it *provably* does.

## <font color="#388bfd">Table of Contents</font>

1. [Why reading a stranger's code is the skill being taught](#why-read-code-you-didnt-write)
2. [Fork the repository, clone your fork, and open it](#fork-clone-open)
3. [A method for reading unfamiliar code: categorize, read, gauge](#reading-code-you-didnt-write)
4. [Two ways to verify a feature: black box and white box](#two-ways-to-verify-a-feature)
5. [Verify a SHA-1 hash by hand in the terminal](#verifying-a-hash-by-hand)
6. [Write evidence that would convince a stranger](#writing-evidence-that-convinces)
7. [The six behaviors you are verifying today](#what-you-are-verifying)
8. [Rename their variables and methods so they say what they hold and do](#renaming-for-sense)
9. [Rules for reviewers](#reviewer-rules)

---

## <font color="#388bfd">Why Read Code You Didn't Write</font>

Professional programmers spend far more time reading code than writing it. Every bug fix starts with reading someone else's decision. Every code review is reading. Part 4 of this project will hand you a random classmate's codebase and ask you to *extend* it — you cannot extend what you cannot read.

Reading code well is three separate verbs, and today you practice each one:

| Verb | The question you are answering | What you produce |
|---|---|---|
| **Categorize** | Which method is responsible for which milestone? | A feature map (method → milestone) |
| **Read** | How does this method actually do its job, line by line? | Notes on the approach: data types, file handling, edge cases |
| **Gauge** | Does it do what the milestone asked — provably? | A verdict, with the command you ran and the output you saw |

The trap most beginners fall into is skipping straight to *gauge* ("I ran it and something happened") without *categorize* and *read*. Then they cannot explain why it worked, and they cannot tell the difference between a feature that works and a feature that happened to look right once.

---

## <font color="#388bfd">Fork, Clone, Open</font>

You learned the fork workflow in [Forks and Collaboration](../../GitUsage/ForksAndCollaboration/). Today it is not an exercise — it is how you get the code.

**Why fork instead of cloning their repository directly?** Two reasons. You have no write access to a classmate's repo, so anything you commit has nowhere to go. And you *will* need to commit something: at minimum a small `Verify.java` driver that calls their methods, because many Part 2 submissions have an empty `main`. A fork gives you a copy under your own account where all of that is allowed.

1. In your terminal, inside your projects folder, fork the classmate's `git-project-THEIRNAME` and clone your fork in one step:
   ```bash
   cd ~/HTCS_Projects
   gh repo fork THEIR-USERNAME/git-project-THEIRNAME --clone
   cd git-project-THEIRNAME
   git remote -v
   ```
   Four lines: `origin` under **your** username (your fork — you can push here) and `upstream` under the classmate's (their original — fetch only). On GitHub your copy is labeled **forked from THEIR-USERNAME/git-project-THEIRNAME**.
2. If `origin` shows the classmate's username, you cloned the original instead of forking — delete the folder and run the `gh repo fork` line again.
3. Open the folder in the editor you use for Java. Read their `README.md` before any `.java` file: the milestones required them to document every method, so the README is their list of claims. Your job is to check the claims.

> **Note:** You never push to the classmate's repository and you never open a pull request to it today. Your fork is a sandbox. If you change anything to get their code running, it stays in your fork and gets recorded in your table.

👉 <details>
<summary><h3>Activity: Fork, Clone, Open — click to expand</h3></summary>

*Concept: A fork is a copy of a classmate's repository under your own account — you clone the fork, not the original, so everything you do today lands in a repository you control.*

![Diagram of the fork-then-clone path: on the left, the classmate's repository git-project-THEIRNAME on GitHub; a Fork arrow copies it into your account as YOUR-USERNAME/git-project-THEIRNAME, labeled forked from the original; a gh repo fork --clone arrow brings that fork down to your laptop in HTCS_Projects, where origin points at your fork and upstream at the original. A crossed-out arrow from the laptop straight to the classmate's repository is marked push refused — you never write to their repo.](assets/fork-clone-open.svg)

## Task

1. On GitHub, open the repository you were assigned (`git-project-THEIRNAME`). Confirm it belongs to a classmate and not to you, and note the owner's username.
2. In your terminal, go to your projects folder and fork the repository and clone your fork in one step:
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
4. Try to push to the original to see the refusal for yourself:
   ```bash
   git push upstream main
   ```
   GitHub refuses: you have no write access, and today you never need it.
5. Open the folder in the editor you use for Java and read `README.md` first. Write down, in one line each, every method the README claims exists.
6. Look at the history for your first clue about what was attempted:
   ```bash
   git log --oneline | head -20
   ```
   Count how many commits carry a `(GP-2.x)` label. A milestone with no commit is a milestone you should expect to find missing.

*(Standalone file: [activities/01-fork-clone-open.md](activities/01-fork-clone-open.md))*

</details>

---

## <font color="#388bfd">Reading Code You Didn't Write</font>

Do not start at line 1 and read to the end. Read with a purpose, in this order:

1. **Start with the README.** Write down every method it names. This is the author's claim of what exists.
2. **Find the entry point.** Open `Git.java` and locate `main`. Does it call anything? Many Part 2 programs have an empty `main` and were tested by hand — that tells you how you will have to test them too.
3. **Build the feature map.** For each of the four milestones — GP-2.1 `init`, GP-2.2 hash, GP-2.3 blob, GP-2.4 index — find the method that does it. Note the signature: what does it take in (a `String` path? a `File`?) and what does it return or write?
4. **Follow one call all the way down.** Pick the method that stages a file and trace it: read the content → hash it → write the blob → write the index line. At each step, note the data shape (`String` vs `byte[]`), how the path to `git/objects/<hash>` is built, and what happens when something already exists.
5. **Gauge before you run.** Predict what will happen when you stage two files with identical content at different paths. Write the prediction down. Then run it. A prediction that comes true is the strongest evidence there is; a prediction that fails tells you exactly where to look.

While you read, these patterns deserve a note in your table:

| What you see | Why it matters |
|---|---|
| An absolute path such as `/Users/theirname/...` or `C:\Users\...` | The code only runs on their machine. You may change it to run the test — record that you did. |
| `catch (Exception e) { }` with an empty body | Failures are silently swallowed. A feature can look like it "worked" while writing nothing. |
| A `FileWriter` or stream that is never closed | The last write may never reach disk, so the index can be missing its final line. |
| `println` where a file write should be | The output goes to the screen, not to `git/index`. |
| Content read as a `String` with `readLine()` in a loop | Newlines are dropped and re-added; the hash may not match the original bytes. |

👉 <details>
<summary><h3>Activity: Map the Features — click to expand</h3></summary>

*Concept: Before you can judge whether code works, you have to know which piece of it is supposed to do what — a feature map turns a pile of methods into a checklist you can test.*

![Diagram of a feature map: on the left, a source file Git.java listing methods such as main, initRepo, sha1, writeBlob, and addToIndex; arrows connect each method to a row on the right in a table of the four Part 2 milestones — GP-2.1 init, GP-2.2 hash, GP-2.3 blob, GP-2.4 index — with columns for what the method takes in and what it writes. main is marked empty with a note to add a Verify.java driver.](assets/map-the-features.svg)

## Task

1. Open `Git.java` and any other `.java` files in your fork. Find `main`. Write down what happens when it runs: nothing, prints something, or calls other methods.
2. Copy this table into your notes and fill in one row per milestone, using the **actual method names** from their code:

   | Milestone | Method name(s) | Takes in | Produces or writes |
   |---|---|---|---|
   | GP-2.1 init | | | |
   | GP-2.2 hash | | | |
   | GP-2.3 blob | | | |
   | GP-2.4 index | | | |

3. Pick the method that stages a file (blob plus index) and read it top to bottom. Note where the file content is held (a `String`? a `byte[]`?), how the path to `git/objects/<hash>` is built, and what happens if a blob with that name already exists.
4. Highlight anything that would stop the code from running on your machine — an absolute path such as `/Users/theirname/...`, a file that is assumed to exist, an empty `main`. Write it down **before** you change anything; it goes in your table.
5. If `main` does not exercise the methods, create a new file `Verify.java` in your fork with a `main` that calls them in order: init, then stage a file. Do not edit their methods — your job is to test them, not to fix them.

*(Standalone file: [activities/02-map-the-features.md](activities/02-map-the-features.md))*

</details>

---

## <font color="#388bfd">Two Ways to Verify a Feature</font>

**Black box:** run the program and inspect what it left behind in `git/`. You do not need to understand the code to do this — you only need to know what the milestone promised.

**White box:** read the code path and predict the result before running. This catches things a single run will not — for example, a hasher that reads the file line by line and only produces the right blob name for files that happen to end in a newline.

A verdict of **Works** needs both: you read the code and can say *how* it does it, and you ran it and can show *that* it did. These commands, run in your terminal from the root of the fork, are the black-box toolkit for Part 2:

| Question | Command | What to look for |
|---|---|---|
| Did `init()` build the structure? | `ls -la git git/objects` | `objects/`, `index`, and `HEAD` all present; `index` and `HEAD` may be 0 bytes |
| What exactly is in the index? | `cat -e git/index` | every line ends in `$` with no space before it; no line that is only `$` |
| Does the index end in a newline? | `tail -c 1 git/index \| od -c` | `\n` means the file ends with a newline, which the milestone forbids |
| Is the blob a faithful copy? | `diff original.txt git/objects/<hash> && echo IDENTICAL` | prints only `IDENTICAL` |
| Is the hash right? | `shasum original.txt` (macOS) or `sha1sum original.txt` (Linux/WSL) | the 40 characters match the blob's filename exactly |
| How many blobs exist? | `ls git/objects \| wc -l` | count before and after each stage — identical content must not add a second blob |

> **Tip:** Delete the whole `git/` folder between experiments (`rm -rf git`) and run `init()` again so each test starts from a known state. Their `.gitignore` already keeps `git/` out of the fork's history.

---

## <font color="#388bfd">Verifying a Hash by Hand</font>

A blob's filename is the SHA-1 of the file's exact bytes, so you can compute the correct answer without their program. In your terminal:

```bash
printf 'sha1test' > sha1test.txt   # exactly 8 bytes, no newline
shasum sha1test.txt                 # macOS — SHA-1 is the default
sha1sum sha1test.txt                # Linux / WSL
```

Both print `12c4c60ee087ae0f12dc6abc88495e459f6f2654`. If their program stages `sha1test.txt`, that must be the name of the new file in `git/objects/`.

The most common reason a hash is "almost right" is one invisible byte. `echo "sha1test"` adds a newline; `echo -n "sha1test"` does not:

```bash
echo "sha1test" | shasum      # c06872ab31a625a1e19278fb222283f8b1d04c52  (9 bytes)
echo -n "sha1test" | shasum   # 12c4c60ee087ae0f12dc6abc88495e459f6f2654  (8 bytes)
```

Every character changed. When a classmate's hash does not match, check `wc -c` on the test file first, then look at *how their code reads the file* — reading line by line and rebuilding the string is the classic way to lose or add a newline.

👉 <details>
<summary><h3>Activity: Hash It by Hand — click to expand</h3></summary>

*Concept: A blob's filename is the SHA-1 of its exact bytes — you can compute that hash yourself in the terminal and compare it to what the classmate's program produced.*

![Diagram comparing two hashes of the same word: the top path creates sha1test.txt with printf, eight bytes and no newline, runs shasum, and gets 12c4c60ee087ae0f12dc6abc88495e459f6f2654, which matches the blob filename in git/objects with a green check. The bottom path uses echo without -n, nine bytes ending in a newline, and gets a completely different hash starting c06872ab, marked with a red cross — one invisible byte changes every character.](assets/hash-it-by-hand.svg)

## Task

1. In your terminal, inside the fork, create a test file containing exactly the text `sha1test` with **no newline** at the end, and count its bytes:
   ```bash
   printf 'sha1test' > sha1test.txt
   wc -c sha1test.txt
   ```
   `wc -c` must report `8`. If it says `9`, a newline sneaked in — recreate the file.
2. Hash it yourself:
   ```bash
   shasum sha1test.txt        # macOS — SHA-1 is shasum's default
   sha1sum sha1test.txt       # Linux / WSL
   ```
   Expected: `12c4c60ee087ae0f12dc6abc88495e459f6f2654`.
3. See the trap. Hash the same word with and without a trailing newline:
   ```bash
   echo "sha1test" | shasum
   echo -n "sha1test" | shasum
   ```
   Only the `-n` version matches. One invisible byte changes every character of the hash — remember this when a classmate's hash is "almost right".
4. Run the classmate's program so it stages `sha1test.txt` (use your `Verify.java` driver if their `main` does nothing), then list the blobs:
   ```bash
   ls git/objects
   ```
   Record whether a file named `12c4c60ee087ae0f12dc6abc88495e459f6f2654` appeared. A different 40-character name means their hash is wrong, or they hashed something other than the raw bytes — a newline, the path, or a header.
5. Confirm the content survived byte for byte:
   ```bash
   diff sha1test.txt git/objects/12c4c60ee087ae0f12dc6abc88495e459f6f2654 && echo IDENTICAL
   ```
   If `diff` prints anything, the blob is not a faithful copy — note exactly what differs.

*(Standalone file: [activities/03-hash-it-by-hand.md](activities/03-hash-it-by-hand.md))*

</details>

---

## <font color="#388bfd">Writing Evidence That Convinces</font>

Your assignment is a chart with the six behaviors on the left and two answers per row on the right. A finding a stranger cannot reproduce is an opinion, not evidence.

**Answer one — how well does it work, 1 to 5:**

| Rating | Meaning |
|---|---|
| **5** | Works exactly as described, and you proved it — command and output recorded. |
| **4** | Works, but one small rule is broken — a trailing space, a blank final line. Say which. |
| **3** | Partly works — the core behavior happens but something the milestone asked for does not. |
| **2** | Runs, but does the wrong thing. Record what it did instead. |
| **1** | Missing, fails, or could not be tested — say which, and paste the error or explain how you know it is absent. |

**Answer two — one written cell that covers three things:** how their code does it (the method name, the approach, the data types), how you verified it (the exact commands or calls you ran and what you saw — paste output, do not paraphrase it), and what you changed to test it, or "nothing".

Here is what a complete row looks like:

| Behavior | 1–5 | Is it functional / verified the functionality? What was modified to get it working? |
|---|---|---|
| 5. Same content at two paths → two index lines, one blob | 5 | **How:** `add(String path)` calls `hashFile` then `writeBlob`, which checks `blobFile.exists()` before writing; `updateIndex` appends unconditionally with `new FileWriter(index, true)`. **Verified:** `printf 'same' > a.txt; mkdir -p sub; printf 'same' > sub/b.txt`, then staged both from `Verify.java`. `ls git/objects` → one file, `ff3390557335ba88d37755e41514beb03bc499ec`. `cat -e git/index` → two lines with that hash, paths `a.txt$` and `sub/b.txt$`. **Modified:** nothing beyond adding `Verify.java`. |

Notice what the row does *not* say: "seems fine", "worked for me", "I think it appends". Every claim points at a method or a command.

---

## <font color="#388bfd">What You Are Verifying</font>

The assignment chart lists these six behaviors in this order. Read them now so you know what to look for while you build your feature map.

1. **Initialize** — `init()` creates `git/`, `git/objects/`, `git/index`, and `git/HEAD`; running it a second time reports that the repository already exists and changes nothing.
2. **Stage a file into a blob** — adding a file creates `git/objects/<hash>` whose content is byte for byte identical to the original.
3. **Hash correctness** — the blob's name is the true SHA-1 of the content; a file containing exactly `sha1test` produces `12c4c60ee087ae0f12dc6abc88495e459f6f2654`.
4. **Index tracks the file** — after adding a file, `git/index` contains a line for it.
5. **Duplicate content** — two files with identical content at different paths produce two index lines with the same hash and exactly one blob in `git/objects/`.
6. **Compression** — blob content is compressed on disk and decompresses back to the original. This was an optional stretch milestone; a **1** with the note "not implemented" is a complete answer here.

---

## <font color="#388bfd">Renaming for Sense</font>

Once you know what their code does, you are in a rare position: you can see which names helped you and which ones fought you. The second half of the assignment is to fix the names — and only the names — on a branch in your fork.

Two questions decide every name:

| Ask | The answer is the name | Example |
|---|---|---|
| **What does this variable hold?** | Name it for its contents, not its type or its position | `String s` holding a SHA-1 → `hash` · `File f` being written → `blobFile` · `int i` walking index lines → `lineNumber` |
| **What does this method do?** | Name it for the one job it performs, as a verb phrase | `doStuff()` that appends one line → `appendIndexEntry()` · `helper()` that turns bytes into hex → `bytesToHex()` · `run(String p)` that hashes, writes the blob, and updates the index → `stageFile(String path)` |

Three rules keep a rename from becoming a rewrite:

- **Rename only.** No logic changes, no reordering, no fixing the bug you found — that goes in your chart, not in their code.
- **Rename with the tool, not with find-and-replace.** In VS Code, right-click the name → **Rename Symbol** (or press F2). Every reference updates together; a hand-edited rename that misses one reference is the classic way to break code you meant to leave alone.
- **Prove nothing changed.** Run your `Verify.java` again after renaming. Same blobs, same index, same output. If a rating in your chart would move, you changed more than a name.

This is the same standard this course holds its own starter code to — no single-letter identifiers, parameters that say what they hold, the lesson's vocabulary (hash, blob, index entry) in the names — now applied to a classmate's code.

---

## <font color="#388bfd">Reviewer Rules</font>

- **In Part 1, verify — don't fix.** You may add a driver class (`Verify.java`) and you may change a hardcoded path so the code runs on your machine. You may not rewrite their methods. Anything you change goes in the chart's written answer.
- **In Part 2, rename — only rename.** Behavior stays identical; your `Verify.java` proves it.
- **The project rules still apply.** No AI tools, and none of their code goes into your own `git-project-YOURNAME`.
- **Describe behavior, not people.** "A second blob appears for identical content because `writeBlob` never checks whether the file already exists" is a finding. "This is sloppy" is not.
- **Honesty beats a clean sheet.** A chart with two rows rated **1** and pasted errors is worth more than six unexplained **5**s. Your classmate gets this chart back — make it something they can act on.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Fork a classmate's repository, clone the fork, and confirm with `git remote -v` that `origin` points at your own account.
- [ ] Locate the method that implements each Part 2 milestone in a codebase you did not write.
- [ ] Compute the SHA-1 of a short string in the terminal and explain why a trailing newline changes it.

### <font color="#79c0ff">Intermediate</font>

- [ ] Write a small driver class in your fork that exercises a classmate's init, hash, blob, and index methods without modifying those methods.
- [ ] Give one piece of black-box evidence and one piece of white-box evidence for the same feature, and explain what each proves.
- [ ] Show, with commands and their output, that two identical files produce two index lines but only one blob.
- [ ] Rename a variable and a method in someone else's code by answering "What does it hold?" and "What does it do?", using Rename Symbol, without changing behavior.

### <font color="#79c0ff">Advanced</font>

- [ ] Prove whether an index file ends in a blank line or has a trailing space using byte-level tools such as `cat -e`, `od -c`, or `tail -c`.
- [ ] Trace a second add of identical content through a classmate's code and predict, before running it, whether a second blob will be written.
- [ ] Write a verification row a stranger could reproduce exactly: the command, the observed output, the method responsible, and the 1–5 rating it earns.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Turn your `Verify.java` into an automated tester that prints PASS or FAIL for all six behaviors, then run it unchanged against a second classmate's fork.
- [ ] In a real Git repository, compare `git hash-object sha1test.txt` with `shasum sha1test.txt`. They differ — find out what real Git prepends to the content before hashing.
- [ ] Decompress a real Git blob to see behavior 6 in the wild. In your terminal, inside any real repository:
  ```bash
  python3 -c "import sys, zlib; sys.stdout.buffer.write(zlib.decompress(open(sys.argv[1], 'rb').read()))" .git/objects/ab/cdef...
  ```

---

[Assignment](ASSIGNMENT.md)

← [Initialization and Blobs](../InitAndBlobs/) — Next: [Trees](../Trees/)
