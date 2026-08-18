<div align="center">

# Patterns Become Tokens
*<font color="#8b949e">Build a Byte Pair Encoding tokenizer — teach the machine its first symbols</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The pizzeria's archive has been digitized, but the machine does not see words, sentences, or recipes. It sees bytes. Even the word "mozzarella" has no special status. Before the machine can predict anything, your team must decide what its basic symbols will be. Choose symbols that are too small and every sentence becomes extremely long. Choose symbols that are too large and most of them will appear too rarely to learn.

## <font color="#388bfd">Question to Carry</font>

> **What should count as one reusable unit of text?**

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Corpus | The complete collection of text used in an experiment. |
| Document | One separately identifiable item in the corpus, such as one book, report, or notebook. |
| Character | A textual symbol such as `A`, `7`, `?`, or a newline. |
| Unicode | A standard that assigns identifiers to characters used by many writing systems. |
| Unicode Transformation Format, 8-bit form, abbreviated UTF-8 | A way to store Unicode characters as sequences of bytes. |
| Byte | An integer from 0 through 255 representing eight bits of data. |
| Token | One discrete unit presented to the language model. |
| Token identifier | The integer assigned to a token. The number itself has no semantic magnitude. |
| Tokenizer | A program that converts text into token identifiers. |
| Vocabulary | The complete set of tokens recognized by a tokenizer. |
| Adjacent pair | Two tokens that appear side by side in the same document. |
| Merge | Replacing every non-overlapping occurrence of one adjacent pair with a single new token. |
| Byte Pair Encoding, abbreviated BPE | A tokenization method that repeatedly merges the most frequent adjacent pair. |

[Byte Pair Encoding](https://aclanthology.org/P16-1162/) became an influential method for representing text with variable-length subword units. For this course, you implement a deliberately small byte-based version rather than using a production vocabulary containing tens of thousands of tokens.

## <font color="#388bfd">Provided: From Files to Tokens</font>

Every training document in this course is a plain UTF-8 text file. That is the standard corpus format for the entire project: one `.txt` file per document, attached to the tokenizer by path. The starter code handles the whole loading pipeline for you:

```text
files  →  bytes  →  integer tokens
```

Copy the starter class from [starter/Tokenizer.java](starter/Tokenizer.java). Its `addFiles` method is complete:

```java
public void addFiles(Path... files) throws IOException {
    for (Path file : files) {
        byte[] bytes = Files.readAllBytes(file);
        List<Integer> tokens = new ArrayList<>(bytes.length);

        for (byte b : bytes) {
            tokens.add(Byte.toUnsignedInt(b));
        }

        documents.add(tokens);
    }
}
```

This method quietly removes three problems that have nothing to do with the algorithm you are here to learn:

1. **File input.** `Files.readAllBytes` reads an entire file into memory in one call. You never touch streams or readers.
2. **Signed Java bytes.** Java's `byte` type runs from −128 to 127, so a byte like `0xE9` (part of the UTF-8 encoding of `é`) shows up as a *negative* number. `Byte.toUnsignedInt` converts every byte to its true value from 0 through 255.
3. **Token identifiers outgrow bytes.** Every merge invents a new token, and the first one is numbered 256 — already too large for a byte. Storing tokens as `int` from the start means merging never requires a change of representation.

Each file becomes its own entry in `documents`, and the lists are never concatenated. That matters: the last byte of one report and the first byte of the next were never actually next to each other, so they must never be counted as a pair.

Beyond loading, the starter provides three more pieces of scaffolding:

- **`vocabularySize()`** — returns `nextTokenId`: 256 byte tokens plus the merges *actually performed*. Calling `train(256)` does **not** guarantee a vocabulary of 512, because training stops early when no pair occurs at least twice. Downstream code must ask the tokenizer for its vocabulary size, never assume it.
- **The `MergeRule` record and `getMergeRules()`** — the ordered log of what training learned. Part 2 fills it in; the section below explains why it is the tokenizer's most important product.
- **`encode` and `decode` stubs** — empty for now, waiting on the merge-rule log. `decode` is this week's stretch goal; `encode` becomes necessary the moment experiments must tokenize text the trainer never saw.

## <font color="#388bfd">Your Task: Two Parts</font>

The entire assignment is two methods. Everything else — loading, the training loop, access to the documents — is already written.

```java
// PART 1:
// Count every adjacent pair across all documents.
private Map<Pair, Integer> countPairs()

// PART 2:
// Find the most common pair, assign it a new token ID,
// and replace every non-overlapping occurrence in every document.
private boolean mergeMostFrequentPair()
```

The supplied `train` method simply calls Part 2 repeatedly:

```java
public void train(int merges) {
    for (int i = 0; i < merges; i++) {
        if (!mergeMostFrequentPair()) {
            break;
        }
    }
}
```

### <font color="#79c0ff">Part 1 — count adjacent pairs</font>

Walk every document and count how many times each adjacent pair occurs, across all documents combined. For a single document

```text
[97, 98, 97, 98]
```

the correct counts are:

```text
(97, 98) -> 2
(98, 97) -> 1
```

The `Pair` record in the starter code already works as a `HashMap` key — records get `equals` and `hashCode` for free.

### <font color="#79c0ff">Part 2 — merge the most frequent pair</font>

One call performs one merge, following these rules:

1. Count all pairs using Part 1.
2. Select the winning pair **deterministically**: prefer the larger count; if counts tie, prefer the smaller left token identifier; if those also tie, prefer the smaller right token identifier.
3. If no pair occurs at least **twice**, return `false` — there is nothing worth merging, and `train` will stop.
4. Claim a new token identifier with `nextTokenId++`. The first merge creates token 256, the second 257, and so on.
5. Record what was learned: append `new MergeRule(left, right, newToken)` to `mergeRules`.
6. In **every** document, replace each non-overlapping occurrence of the pair with the new token, scanning left to right.
7. Return `true`.

If the most frequent pair in

```text
[97, 98, 97, 98, 99]
```

is `(97, 98)`, the merge assigns `256 = (97, 98)` and produces:

```text
[256, 256, 99]
```

**Non-overlapping, left to right.** In `[97, 97, 97]`, Part 1 counts `(97, 97)` twice — positions 0–1 and 1–2. But the merge produces `[256, 97]`, not `[256, 256]`: once the first two tokens are consumed by a replacement, the middle `97` is gone, so the second occurrence no longer exists.

> **Warning:** The lists hold `Integer` objects. Comparing a list element to an `int` such as `best.left()` works, because Java unboxes the `Integer`. Comparing two list elements to each other with `==` does **not** work reliably — it compares object references, and it happens to succeed for values under 128 and fail above. Use `int` values or `.equals` in comparisons.

### <font color="#79c0ff">Why ties must break deterministically</font>

Suppose `(97, 98)` and `(32, 101)` both occur five times, and nothing occurs six. Which merges first? If your answer is "whichever the loop happens to see first," your tokenizer is built on sand: the counts live in a `HashMap`, and `HashMap` iteration order is **unspecified** — it can differ between two correct programs, and even between runs. Two students could train on the identical file, both implement everything "correctly," and produce different vocabularies. A saved experiment could stop being reproducible.

The tie rule removes the coin flip: larger count first; then smaller left identifier; then smaller right identifier. With it, the same input produces the same merges, every time, on every machine. Determinism is what makes tokenizers comparable, gradable, and — later in the course — reloadable.

### <font color="#79c0ff">The rules are the tokenizer</font>

Training mutates `documents`, but the transformed documents are not the durable product — the **ordered list of merge rules** is. Without that log, your tokenizer can only ever transform the text it trained on. With it, the same learned vocabulary can be applied anywhere:

- `encode` can tokenize *new* text — a validation set, a test set, a user's prompt — by converting it to bytes and replaying the rules **in learned order**. Order matters: a later rule may merge tokens that only exist because an earlier rule created them.
- `decode` can reverse the process, expanding each learned token back through its rule until only bytes remain, reconstructing the original text exactly.

That is why Part 2 appends a `MergeRule` on every merge. The `encode` and `decode` stubs in the starter stay unimplemented this week (`decode` is a stretch goal), but the log they depend on must be built now — retrofitting it later means retraining every tokenizer you ever saved.

## <font color="#388bfd">Worked Trace</font>

A file containing the seven characters `abab ab` loads as (`a` = 97, `b` = 98, space = 32):

```text
[97, 98, 97, 98, 32, 97, 98]
```

**Merge 1.** The pair counts are:

```text
(97, 98) -> 3
(98, 97) -> 1
(98, 32) -> 1
(32, 97) -> 1
```

`(97, 98)` wins with 3, becomes token 256, and the document shrinks from 7 tokens to 4:

```text
[256, 256, 32, 256]
```

**Merge 2.** The new counts are `(256, 256) -> 1`, `(256, 32) -> 1`, and `(32, 256) -> 1`. No pair occurs at least twice, so `mergeMostFrequentPair` returns `false` and training stops — even if more merges were requested.

## <font color="#388bfd">One Pass or Many?</font>

There are two honest ways to write the replacement in Part 2, and the [assignment](ASSIGNMENT.md) grades them differently:

- **Multiple passes (B level).** Repeatedly search a document from the beginning for the next occurrence of the pair, replace it, and search again. This is correct, but every replacement rescans the document, so a merge can cost time proportional to *n²* for a document of *n* tokens.
- **Single pass (A level).** Walk each document exactly once, left to right, building a new list: when the tokens at positions `i` and `i + 1` match the pair, append the new token and jump ahead two positions; otherwise append the current token and move ahead one. One merge then costs time proportional to *n* — the best possible, since every token must at least be looked at.

Carry this question into later chapters: even the single-pass version recounts *every* pair from scratch after *every* merge, though one merge only changes counts near the positions it touched. Could the counts be updated instead of recomputed? That is the first rung of the stretch ladder.

## <font color="#388bfd">Evidence Checkpoint</font>

Train on a real archive file and watch the numbers. Add a `main` method (or a separate test class) that:

1. Adds one or more `.txt` files.
2. Prints the total token count before training.
3. Runs `train(128)`, printing each merge as it happens — the pair chosen and the token identifier it received.
4. Prints the total token count after training.
5. Prints `vocabularySize()` and `getMergeRules().size()`, and confirms that vocabulary size equals 256 plus the merges *performed* — which may be fewer than the 128 requested.

On ordinary English text the token count should fall substantially, and the earliest merges should be recognizable — spaces attached to common letters, then fragments like `th` and `in`. On the tiny `abab ab` trace above, your program must reproduce the numbers by hand exactly.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** Token identifier 301 is not "more meaningful" or "larger" than token identifier 17. Identifiers are labels.

## <font color="#388bfd">Stretch Goals</font>

1. **Incremental pair counts:** After a merge, update the counts around the replaced positions instead of recounting every document from scratch.
2. **Decode:** Implement the provided `decode` stub using the recorded merge rules — expand each learned token back into bytes, rebuild the text, and verify the result matches the original file exactly.
3. **Compression experiment:** Train with 64, 128, 256, and 512 merges and plot vocabulary size against tokens per original byte.
4. **Vocabulary browser:** Print each learned token's text in human-readable form, with newlines and tabs escaped.

---

The machine now possesses an alphabet, but an alphabet does not predict anything. The next chapter gives it the smallest possible memory.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain the difference between a character, a byte, and a token?
- [ ] Can you trace how `addFiles` turns a text file into a list of integers, and explain why every starting token is between 0 and 255?
- [ ] Can you explain why `nextTokenId` starts at 256, and why `vocabularySize()` reports the merges actually performed rather than the merges requested?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you count every adjacent pair in `[97, 98, 97, 98]` by hand and match what `countPairs` must return?
- [ ] Can you explain why `mergeMostFrequentPair` returns `false` when no pair occurs at least twice, and what `train` does when that happens?
- [ ] Can you show why merging `(97, 97)` turns `[97, 97, 97]` into `[256, 97]` and not `[256, 256]`?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why the single-pass merge costs time proportional to the document length, while a search-and-replace loop can cost quadratic time?
- [ ] Can you explain how two correct programs trained on the same file could learn different vocabularies without the tie rule — and walk through the rule that prevents it?
- [ ] Can you explain why the ordered `MergeRule` list is exactly what `encode` needs to tokenize text the trainer never saw, and why replaying the rules out of order breaks it?

---

[Assignment](ASSIGNMENT.md)

← Back to [Project Strata](../) — Next: [The Reader with One-Step Memory](../MarkovBaseline/)
