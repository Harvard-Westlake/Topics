# Assignment — The Reader with One-Step Memory

**Due:** End of Week 2

---

## Objectives

You already know Markov chains, so the counting code in this assignment is reinforcement. The graded heart of the assignment is the **measurement**: deriving, implementing, and defending the loss that will judge every model for the rest of the course. By the end you should be able to:

- **Derive negative log-likelihood from scratch.** Build it in three steps — likelihood, then the log, then the negation — and name the specific problem each step solves (matching reality, arithmetic underflow, minimization convention).
- **Defend NLL against the alternatives.** Explain why accuracy's all-or-nothing grading and mean squared error's notion of distance are both wrong for categorical next-token prediction.
- **Translate loss into human terms.** Read perplexity as the size of the die the model is rolling, and bits per byte as a compression claim about the original file.
- **Compute smoothed probabilities that normalize.** Apply additive smoothing and verify every next-token distribution sums to approximately one — because a single unsmoothed zero makes NLL infinite.
- **Build three baselines over integer tokens.** Uniform, unigram, and bigram models that all implement the same two-method `LanguageModel` interface.
- **Respect the experiment boundary.** Train only on training data, tune only on validation data, and touch test data once.
- **Sample reproducibly.** Draw from a categorical distribution so a fixed seed reproduces identical generated text.
- **Diagnose failure at the level of state.** Tie a bad generation to the exact information the one-token state could not hold.

This chapter is the course's **permanent baseline** — every later model is compared against it using the same splits and the same evaluation. Keep it runnable through Chapter 11.

---

## What You Are Given

Copy all eight files from [starter/](starter/) into your project, alongside your completed Chapter 1 `Tokenizer.java`.

| File | Status | You write |
|---|---|---|
| [LanguageModel.java](starter/LanguageModel.java) | Complete | — |
| [UniformModel.java](starter/UniformModel.java) | Complete — read it first as the worked example | — |
| [UnigramModel.java](starter/UnigramModel.java) | Starter | TODO 1: `train` · TODO 2: `probability` |
| [BigramModel.java](starter/BigramModel.java) | Starter | TODO 3: `train` · TODO 4: `probability` |
| [MarkovRevisited.java](starter/MarkovRevisited.java) | Splitting, generation, and validators provided | TODO 5: `evaluate` · TODO 6: `sampleNext` |
| [EvaluationResult.java](starter/EvaluationResult.java) | Complete | — |
| [CorpusSplit.java](starter/CorpusSplit.java) | Complete | — |
| [Tester.java](starter/Tester.java) | Complete | Extend it as you complete each TODO |

Do not modify the provided methods or records. Adding methods to `Tester.java` (or a separate test class) is expected.

> **Note:** `Tester.java` runs `t.train(256)` and then reads the real vocabulary from `t.vocabularySize()` — 256 plus the merges *actually performed*, which is 512 only if all 256 merges succeeded. Never hard-code the vocabulary size. For your first full run, `t.train(0)` keeps raw byte tokens ($V = 256$) — the dense table stays small and generated output can be read directly by converting each token back to a byte.

---

## The Work, in Order

Implement the six TODOs in this order and re-run your tests after each. Each step adds exactly one idea:

| # | Method | The idea it isolates |
|---|---|---|
| 1 | `UnigramModel.train` | Count token frequency — training documents only |
| 2 | `UnigramModel.probability` | Additive smoothing: $\frac{\text{count}(j)+\alpha}{\text{total}+\alpha V}$ |
| 3 | `BigramModel.train` | Count `current -> next` transitions; update `counts` and `rowTotals`; never cross a document boundary |
| 4 | `BigramModel.probability` | One row, normalized: $\frac{\text{count}(i,j)+\alpha}{\text{rowTotal}(i)+\alpha V}$ |
| 5 | `MarkovRevisited.evaluate` | Accumulate $-\log P(\text{target} \mid \text{context})$ over positions 1 through $n-1$ of every document |
| 6 | `MarkovRevisited.sampleNext` | Walk the cumulative distribution past one random draw |

Then run the full experiment:

1. Tokenize your archive files (Chapter 1).
2. Split with the provided `splitDocuments` — 80/10/10, contiguous.
3. Train unigram and bigram models **on the training split only**.
4. Evaluate all three models on training, validation, and test splits.
5. Generate at least one sample from each model with a fixed seed.

---

## Required Tests

Confirm every one of these behaviors — each catches a specific, common bug:

- Every probability is between zero and one.
- Every next-token distribution sums to approximately one.
- Additive smoothing gives nonzero probability to an unseen transition.
- A known synthetic count table produces known probabilities (use `[0, 1, 0, 1, 1]` with $V=2$, $\alpha=1$: the answers are 0.75 / 0.25 / 0.50 / 0.50).
- A fixed random seed produces reproducible generation.
- Evaluating validation data does not alter training counts or probabilities.
- Generation never emits a token identifier outside $[0, V)$.
- The 80/10/10 split remains contiguous inside each document.

---

## Evidence Table

| Model | Training loss | Validation loss | Test loss |
|---|---:|---:|---:|
| Uniform | | | |
| Unigram | | | |
| Bigram | | | |

Record $\alpha$, the vocabulary size, the tokenizer choice, and the random seed next to the table so the experiment can be reproduced. Sanity anchors: uniform loss must equal $\ln V$ (≈ 5.545 for $V=256$, ≈ 6.238 for $V=512$), and the ladder must hold on validation data: bigram < unigram < uniform.

---

## Failure Analysis

Find **two** generated bigram passages that reveal the one-token memory limit. For each, write four numbered lines:

1. The current token at the failure point — the state the model actually knew.
2. The continuation the model sampled.
3. The earlier information that would have helped but sat outside the one-token state.
4. Why the corpus transition statistics still made that continuation locally plausible.

---

## Concept Questions

Answer these in your own words in the Canvas text box, below the stencil. Short, precise answers beat long vague ones — two to four sentences each. These carry as much weight as the code.

1. **The underflow question.** Your test split has 20,000 tokens. Explain what happens if you compute its raw likelihood by multiplication, and exactly how the logarithm fixes it.
2. **The negation question.** Log-likelihood already ranks models correctly. Why negate it? What convention does the sign change serve?
3. **The milk question.** The text says *"I drank a glass of milk."* Model A predicted "water" at 51% and "milk" at 49%; Model B predicted "concrete" at 99% and "milk" at 1%. What score does accuracy give each model? What penalty does NLL charge each ($-\log 0.49$ vs $-\log 0.01$)? Which grading is right, and why?
4. **The die question.** Your bigram model reports validation perplexity 38. Say what that number means in one sentence. Then explain why the uniform model's perplexity must be exactly $V$, with no training data involved.
5. **The compression question.** Your bigram model achieves 3.5 bits per byte. What claim does that make about compressing the original file, and what is the uncompressed baseline? Why is bits per byte the only fair metric when two models use different tokenizers?
6. **The infinity question.** Connect smoothing to the loss: what exact numerical disaster does one unseen transition cause in an unsmoothed model's evaluation, and how does $\alpha$ prevent it?
7. **The alpha question.** Laplace smoothing fixes $\alpha = 1$. Suppose your vocabulary has 50,000 tokens but your training text contains only 10,000. Using the denominator arithmetic, explain why add-one smoothing all but erases what the model learned — and what a better choice of $\alpha$ looks like, and which data split you may use to choose it.

---

## Grading Emphasis

| Area | Weight |
|---|---:|
| Evaluation: NLL implementation, perplexity, bits per byte | 25% |
| Concept questions on loss motivation | 20% |
| Bigram counts and smoothed probabilities | 15% |
| Uniform and unigram baselines | 10% |
| Correct contiguous split, no leakage | 10% |
| Sampling and reproducibility | 10% |
| Tests and failure analysis | 10% |

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **All six TODOs implemented** — no `UnsupportedOperationException` remains reachable.
- [ ] **The synthetic trace reproduces by hand** — training a bigram model on `[0, 1, 0, 1, 1]` with $\alpha=1$ yields 0.75 / 0.25 / 0.50 / 0.50.
- [ ] **Rows normalize** — summing `probability(i, j)` over all $j$ gives approximately 1 for several rows $i$.
- [ ] **Uniform anchors the evaluation** — its average loss equals $\ln V$ on every split.
- [ ] **Only training data updates counts** — evaluating validation or test data changes nothing.
- [ ] **The ladder holds** — on validation data, bigram beats unigram beats uniform.
- [ ] **Generation is reproducible and legal** — a fixed seed regenerates identical output, and every emitted identifier is inside $[0, V)$.
- [ ] **Two failure analyses written** — each names the exact state and the missing earlier information.
- [ ] **All seven concept questions answered** — in your own words, with the specific numbers where asked.
- [ ] **Provided code unmodified** — `splitDocuments`, `generate`, the validators, and the records are untouched.

---

## Submission

Submit **both text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box. Underneath it, paste your two failure analyses and your answers to the seven concept questions.

```
Vocabulary size (V):
Alpha:
Random seed:
Tokenizer (raw bytes or BPE merges):
Uniform  loss (train / val / test):
Unigram  loss (train / val / test):
Bigram   loss (train / val / test):
Bigram perplexity (validation):
```

### Screenshot

The screenshot must show your program's console output from the full experiment: the evaluation results for all three models on all three splits, and one generated sample. Output must include the uniform model's loss so the $\ln V$ anchor is visible. A screenshot of source code alone does not qualify.
