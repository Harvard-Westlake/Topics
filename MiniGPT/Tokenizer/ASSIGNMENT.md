# Assignment — Patterns Become Tokens

*Lesson: [Patterns Become Tokens](README.md)*

**Due:** End of Week 1

---

## Objectives

By the end of this assignment you should be able to:

- **Count frequencies with a map.** Walk one or more token sequences and tally every adjacent pair in a `HashMap`, using a record as the key.
- **Perform non-overlapping sequence replacement.** Replace every left-to-right occurrence of a pair in a list without double-consuming tokens.
- **Explain how Byte Pair Encoding builds a vocabulary.** Describe how repeatedly merging the most frequent pair turns 256 byte tokens into a learned vocabulary.
- **Reason about cost.** Explain the difference between rebuilding a document in one linear pass and rescanning it once per replacement.

You are **not** implementing file input. The provided `addFiles` reads each attached `.txt` file and converts every byte straight to an integer token — that pipeline (`files → bytes → integer tokens`) is the standard corpus-loading format for the rest of the course.

---

## What You Are Given

Copy [starter/Tokenizer.java](starter/Tokenizer.java) into your project.

| Provided — do not modify | You implement |
|---|---|
| `addFiles` — reads files, converts bytes to `int` tokens, one document per file | `countPairs` — Part 1 |
| `Pair` record — ready to use as a `HashMap` key | `mergeMostFrequentPair` — Part 2, including the tie rule and merge recording |
| `MergeRule` record and `getMergeRules()` — the ordered log Part 2 fills in | |
| `train` — calls Part 2 repeatedly, stops when it returns `false` | |
| `vocabularySize()` — 256 plus merges actually performed; call it, never assume 512 | |
| `getDocuments` — access for printing and testing | |
| `encode` / `decode` — TODO stubs for later; not graded this week (`decode` is the stretch goal) | |

You may add a `main` method or a separate test class to run and inspect your tokenizer. Printing each merge from inside `mergeMostFrequentPair` is allowed and encouraged.

---

## Part 1 — Count Adjacent Pairs

```java
// Count every adjacent pair across all documents.
private Map<Pair, Integer> countPairs()
```

Count how often each adjacent pair occurs across **all** documents combined. For a document `[97, 98, 97, 98]` the result must contain exactly `(97, 98) -> 2` and `(98, 97) -> 1`. Pairs never span from the end of one document to the start of the next.

## Part 2 — Merge the Most Frequent Pair

```java
// Find the most common pair, assign it a new token ID,
// and replace every non-overlapping occurrence in every document.
private boolean mergeMostFrequentPair()
```

One call performs one merge:

1. Count all pairs with Part 1.
2. Select the winning pair **deterministically**: largest count; if counts tie, smaller left identifier; if still tied, smaller right identifier. (`HashMap` order is unspecified — "first one seen" is not deterministic.)
3. If no pair occurs at least twice, return `false`.
4. Assign the new token identifier `nextTokenId++`.
5. Record the merge: append `new MergeRule(left, right, newToken)` to the rule list.
6. Replace every non-overlapping occurrence, left to right, in every document — `[97, 97, 97]` becomes `[256, 97]`, not `[256, 256]`.
7. Return `true`.

---

## Grading Levels

Both levels must produce **identical, correct final documents** on the same input. The difference is how the work is done.

| Level | Requirement |
|---|---|
| **A** | The replacement in Part 2 rebuilds each document in a **single left-to-right pass**: examine each position once, appending either the new token (advance two) or the current token (advance one). One merge does an amount of work proportional to the total token count — O(n) — with no repeated searching. `countPairs` likewise makes exactly one pass over each document. |
| **B** | The replacement works but takes **multiple passes** — for example, searching from the beginning for the next occurrence, replacing it, and searching again. Correct output, but each merge may rescan the documents many times. |

> **Note:** If you finish the B version, do not stop — converting it to the single-pass A version is a small rewrite of the replacement loop, not a new program.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **`countPairs` is correct** — for a document `[97, 98, 97, 98]` it reports `(97, 98) -> 2` and `(98, 97) -> 1`, and counts combine across all documents.
- [ ] **Pairs never cross documents** — the last token of one file is never paired with the first token of the next.
- [ ] **Replacement is non-overlapping and left to right** — merging `(97, 97)` in `[97, 97, 97]` yields `[256, 97]`.
- [ ] **New token identifiers count up from 256** — the first merge creates 256, the second 257, and so on.
- [ ] **Training stops when nothing repeats** — `mergeMostFrequentPair` returns `false` when no pair occurs at least twice, and `train` stops early.
- [ ] **Ties break deterministically** — largest count, then smaller left identifier, then smaller right identifier. Re-running training on the same input produces the identical merge sequence every time.
- [ ] **Every merge is recorded** — after training, `getMergeRules()` holds one `MergeRule` per merge performed, in learned order, the first with result 256.
- [ ] **Vocabulary size is asked, never assumed** — `vocabularySize()` equals 256 plus merges performed, and nothing in your test code hard-codes 512.
- [ ] **The worked trace reproduces exactly** — training on a file containing `abab ab` performs one merge and produces `[256, 256, 32, 256]`.
- [ ] **Token count falls on real text** — training on an archive `.txt` file with 128 merges substantially reduces the total token count, and your program prints the before and after counts.
- [ ] **Provided code is unmodified** — `addFiles`, `train`, `vocabularySize`, `getDocuments`, `getMergeRules`, and the `Pair` and `MergeRule` records are untouched (adding a `main` method or test class is fine).

---

## Submission

Submit **both text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Level attempted (A or B):
Files trained on:
Tokens before training:
Merges requested:
Merges performed:
Tokens after training:
Final vocabulary size (vocabularySize()):
First three merges (left, right -> new id):
```

### Screenshot

The screenshot must show your program's console output from a real training run: the token count before training, at least the first three merges as they happen, and the token count after training. A screenshot showing only source code, or output without the before-and-after counts, does not qualify.
