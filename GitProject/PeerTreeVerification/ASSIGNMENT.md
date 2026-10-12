# Assignment — Peer Tree Verification

*Lesson: [Peer Tree Verification](README.md)*

**Due:** Before the start of next class

---

## Your Homework

Copy the table below, fill in a rating and how you identified it for each of the six behaviors, and paste it into the Canvas text box. That is the whole assignment.

1. Fork and clone the classmate's repository your teacher assigned you, and get their code running. The lesson's [Fork and Clone](README.md#1-fork-and-clone-a-classmates-repository) and [Run and Verify](README.md#2-run-and-verify) sections walk through it.
2. Select the whole **Verification Table** below, copy it, and paste it into the Canvas text box. It pastes as a table you can type into.
3. For each row, test the behavior, then fill in the two empty columns.

---

## Verification Table

**What is a root tree?** A tree is a list of what is inside one folder. The **root tree** is the list for the top folder, the one that holds everything else.

Trees are built from the bottom up. The deepest folder gets its tree first, then its parent, and so on up to the root. A parent's list includes each child folder's tree hash, so the root always comes last. In the test folder: `tree-test/docs` becomes `d5ff240d…`, then `tree-test` lists `tree d5ff240d… docs` and becomes `54c35b48…`, the root.

| Behavior | Rating (1–5) | How you identified it |
|---|---|---|
| **1. Index stores relative paths**<br>(Example: staging `hello.txt` writes `aaf4c61d… tree-test/docs/hello.txt`) | | |
| **2. No duplicate entries**<br>(Example: stage `hello.txt` twice, still one line) | | |
| **3. A modified file replaces its entry**<br>(Example: edit `hello.txt` and restage, one line with `714d500f…`) | | |
| **4. `createTree` writes one directory's tree**<br>(Example: `tree-test/docs` becomes `d5ff240d…`) | | |
| **5. Root tree from staged files only**<br>(Example: root is `54c35b48…` or `60a91a23…`, no `scratch.txt`) | | |
| **6. Deterministic**<br>(Example: run it twice, same hash, no new files) | | |

**Rating (5 is best):**

| Rating | Meaning |
|---|---|
| **5** | Works exactly as described, and you proved it. |
| **4** | Works, but one small rule is broken, such as a trailing newline in a tree file. |
| **3** | Partly works. |
| **2** | Runs, but does the wrong thing. |
| **1** | Missing, fails, or could not be tested. Say which. |

**How you identified it:** a few short bullets, not a paragraph. The command or call you ran, what came out, and anything you changed to test it. The full expected hashes are in the lesson's [Hash a Tree by Hand](README.md#hash-a-tree-by-hand) section, and the lesson shows [a complete example row](README.md#grade-each-behavior-in-the-table).

> **Note:** Behavior 3 edits `hello.txt`. Test it last, or rebuild `tree-test/` with the lesson's `printf` commands before testing behaviors 4 through 6, or the expected tree hashes will not match.

---

## Success Criteria

- [ ] **Every row is filled in.** Each behavior has a rating from 1 to 5 and at least one bullet saying how you identified it.
- [ ] **Wrong hashes are explained.** Any hash that does not match is written next to the hash you expected.
- [ ] **Their repository is untouched.** Anything you added or fixed is in your fork, never pushed to theirs.

---

## Submission

Submit **text** on Canvas: your filled-in table, with these two lines above it:

```
Classmate's repository:   https://github.com/THEIR-USERNAME/THEIR-REPO-NAME
My fork:                  https://github.com/YOUR-USERNAME/YOUR-FORK-NAME
```
