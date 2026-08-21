<div align="center">

# The Reader with One-Step Memory
*<font color="#8b949e">Uniform, unigram, and bigram baselines — and the loss function that judges them</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The archive machine can now read every page as integers. Yet when asked what comes next, it has no answer. Your first prediction system will have a memory of exactly one token. It will ask: "Whenever I saw this token before, what usually followed it?" The result will sometimes look surprisingly convincing — and then fail whenever the answer depends on anything farther back.

## <font color="#388bfd">Question to Carry</font>

> **What can be predicted when the model remembers only the previous token?**

## <font color="#388bfd">What Is Actually New Here</font>

You have built Markov chains before. States, transitions, counting what follows what — that part of this chapter is *review*, and the programming is deliberately structured as reinforcement: short, familiar methods over the token sequences from Chapter 1.

What you have **not** done before is leave the deterministic world. Every Markov model you have built so far ultimately answered "what comes next?" with a lookup. A language model refuses to answer with one token. It answers with a **probability for every possible next token**, and that raises a question deterministic models never had to face:

> **How do you grade a prediction that never commits to a single answer?**

That question — not the counting — is the real challenge of this chapter. The answer is the loss function below, and it is the measuring stick for *every model you build for the rest of the course*. The transformer in Chapter 10 will be judged by exactly the same number you implement this week. Keep this chapter runnable through Chapter 11: it is the course's permanent baseline.

## <font color="#388bfd">Assigning Probability to Reality</font>

To understand **negative log-likelihood** (NLL), start with what a language model is actually trying to do: **assign a probability to reality.**

If a model is good, it will say that the actual text in your test set — the text that really occurred — had a high probability of occurring. If the model is bad, it will be *surprised* by the test set and assign it a very low probability. Everything in this section is the step-by-step construction of that idea into a number your code can compute.

### <font color="#79c0ff">Step A: Likelihood — the core idea</font>

Imagine a test document with just three tokens: `[The, dog, barked]`.

To find out how good your model is, calculate the probability of that exact sequence happening, one step at a time, multiplying as you go:

$$L = P(\text{The}) \times P(\text{dog} \mid \text{The}) \times P(\text{barked} \mid \text{dog})$$

This number is the **likelihood**. The higher it is, the better the model matches reality. In principle, we could stop here — train models, compute likelihoods on held-out text, and crown the model with the highest one.

### <font color="#79c0ff">Step B: The log — the engineering fix</font>

Pure likelihood has a fatal mechanical problem. Probabilities are fractions — numbers like $0.05$. If your test document has 10,000 tokens, you are multiplying 10,000 tiny fractions together. Very quickly the product becomes so infinitesimally small (on the order of $10^{-500}$) that a computer's floating-point representation rounds it to exactly $0.0$. This is called **arithmetic underflow**, and once it happens, every model scores identically: zero.

The fix is the logarithm. Because of the rule

$$\log(A \times B) = \log(A) + \log(B)$$

taking the log transforms the impossible multiplication into a safe addition:

$$\log L = \log P(\text{The}) + \log P(\text{dog} \mid \text{The}) + \log P(\text{barked} \mid \text{dog})$$

Now, instead of shrinking toward zero, the running total just becomes increasingly negative — the log of a fraction is a negative number — and negative numbers of any size are easy for a computer to hold.

### <font color="#79c0ff">Step C: The negative — the machine learning convention</font>

Machine learning optimizes models by *minimizing* a **loss function** — think of golf, where a lower score is better. Log-likelihood points the wrong way for that: it is a negative number we want to push *toward zero*. So we multiply by $-1$ to make it a positive penalty that we want to shrink:

$$\text{NLL} = -\sum_{i=1}^{N} \log P(w_i \mid w_{i-1})$$

Lower NLL means fewer errors. Each term $-\log P$ has a natural reading as **surprise**: an outcome the model expected costs little; an outcome the model called nearly impossible costs enormously. (Note the extreme case: if the model assigns the true next token probability $0$, the penalty is $-\log 0 = \infty$. Hold that thought — it is exactly why smoothing exists later in this lesson.)

### <font color="#79c0ff">Why not accuracy?</font>

Why not grade like a quiz — the percentage of next tokens guessed exactly right?

Because accuracy is all-or-nothing, and probabilistic predictions live in the in-between. Suppose the text says *"I drank a glass of milk."*

- **Model A** predicts "water" with 51% confidence and "milk" with 49%.
- **Model B** predicts "concrete" with 99% confidence and "milk" with 1%.

Accuracy gives both models the same score — zero, both guessed wrong — treating them as equally bad. That is plainly false: Model A nearly had it; Model B was arrogantly, absurdly wrong. NLL separates them exactly as it should: Model A pays $-\log(0.49)$, a modest penalty, while Model B pays $-\log(0.01)$, a huge one. **NLL measures confidence and nuance, not just right and wrong.**

### <font color="#79c0ff">Why not mean squared error?</font>

Mean squared error is the right tool for *continuous* quantities — predicting a house price, where being off by \$1,000 is measurably better than being off by \$100,000. But next-token prediction is a **categorical** problem. There is no mathematical distance between the token "Apple" and the token "Zebra" — token 301 is not "far from" token 17; they are just different categories (remember Chapter 1's misconception: identifiers are labels). Squaring the difference between token identifiers would measure something meaningless.

NLL — which is mathematically identical to **cross-entropy loss**, a name you will meet again in Chapter 4 — is designed precisely for this situation: it measures how far the model's probability distribution is from the distribution of what actually happened.

### <font color="#79c0ff">Perplexity: the human translation</font>

NLL is mathematically ideal for computers and nearly meaningless to humans. "My model's average NLL is 4.2" gives you no intuition at all. That is why your `EvaluationResult` record carries two translations, and the first is **perplexity**:

$$\text{perplexity} = e^{\text{average loss}}$$

Perplexity answers: *on average, how confused was the model at each step?* A perplexity of 50 means that at every prediction, the model was as confused as if it were rolling a fair 50-sided die.

Two anchor points make this concrete — and give you a free correctness test:

- Your **uniform model** with vocabulary size 512 must have a perplexity of **exactly 512** on any text. It is maximally confused; its average loss is exactly $\ln V$ (about $6.24$ for $V = 512$, about $5.55$ for $V = 256$). If your evaluation prints anything else, the bug is in the evaluation, not the model.
- A **perfect model** that assigns 100% to the true next token every time has perplexity **1** — no confusion at all.

Every real model lives between those poles, and this week you will watch the bigram model pull away from 512 toward something meaningfully smaller.

### <font color="#79c0ff">Bits per byte: the compression test</font>

NLL uses the natural logarithm (base $e$). Divide by $\ln 2$ and it converts to base 2 — the unit becomes **bits**, the currency of Claude Shannon's information theory. Spread the total over the original file size and you get **bits per byte**:

$$\text{bits per byte} = \frac{\text{totalNll}}{\ln(2) \cdot \text{originalByteCount}}$$

Bits per byte answers a startlingly physical question: *if this language model powered a file compressor, how many bits would it need to store each byte of the original text?* Uncompressed text costs exactly 8 bits per byte. If your bigram model achieves 3.5 bits per byte, you have mathematically proven that it understands the text's patterns well enough to compress the file to less than half its size — prediction and compression are the same ability wearing different clothes.

Bits per byte has one more job: it is the only fair way to compare models that use **different tokenizers**. Average loss *per token* changes meaning when the tokenizer changes what "one token" is; bits per original byte does not.

### <font color="#79c0ff">Where each idea lives in your code</font>

| Concept | In `EvaluationResult` |
|---|---|
| Total NLL, summed over held-out targets | `totalNll` (you accumulate this in `evaluate`) |
| Average loss per prediction | `averageLoss()` |
| Perplexity | `perplexity()` — literally `Math.exp(averageLoss())` |
| Bits per byte | `bitsPerByte(originalByteCount)` |

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Language model | A system that assigns probabilities to token sequences or predicts likely next tokens. |
| State | The information a Markov model currently remembers. |
| Transition | A move from one state or token to the next. |
| Transition count | How many times one token was followed by another. |
| Transition probability | The estimated probability of the next state given the current state. |
| Conditional probability | The probability of an event given known context. |
| Unigram | A model or count involving one token at a time. |
| Bigram | A pair of consecutive tokens. |
| Trigram | A sequence of three consecutive tokens. |
| N-gram | A sequence containing `n` consecutive tokens. |
| Order-one Markov model | A model that predicts the next token using only the current token. |
| Context | Earlier information used to make a prediction. |
| Smoothing | Reserving probability for events not observed in training. |
| Additive smoothing | Adding a positive constant to every possible count before normalization. Also called Lidstone smoothing. |
| Laplace smoothing | Additive smoothing with the constant fixed at 1 — the original "add-one" technique. |
| Hyperparameter | A setting chosen by the experimenter rather than learned from data, such as the smoothing constant. |
| Categorical distribution | A probability distribution over a finite set of choices. |
| Sampling | Randomly selecting an outcome according to a probability distribution. |
| Baseline | A simple reference model used to judge whether a more complicated model improves. |
| Training set | Data used to estimate model parameters. |
| Validation set | Separate data used during development to compare settings. |
| Test set | Data reserved for final evaluation. |
| Data leakage | Allowing validation or test information to influence training. |
| Likelihood | The probability a model assigns to an entire observed sequence. |
| Negative log-likelihood | The accumulated penalty for probability the model failed to assign to actual outcomes. |
| Cross-entropy loss | Another name for negative log-likelihood; the standard loss for categorical prediction. |
| Arithmetic underflow | A computed value so close to zero that floating-point arithmetic rounds it to exactly zero. |
| Perplexity | The exponential of average negative log-likelihood; the size of the fair die the model is effectively rolling. |
| Bits per byte | Average predictive cost in binary information units per original input byte. |

## <font color="#388bfd">The Ladder of Three Models</font>

With the measuring stick built, you need something to measure. You will build three models, not one, because each answers a different question:

| Model | What it knows | What it ignores | Its probability |
|---|---|---|---|
| Uniform | Only the vocabulary size | The corpus *and* the current token | $P(j) = \frac{1}{V}$ |
| Unigram | How often each token appears overall | The current token | $P(j) = \frac{\text{count}(j)+\alpha}{\text{total}+\alpha V}$ |
| Bigram | What followed each token in training | Everything before the current token | $P(j \mid i) = \frac{\text{count}(i,j)+\alpha}{\text{rowTotal}(i)+\alpha V}$ |

Read the ladder top to bottom as *adding one piece of knowledge at a time*. Whatever loss improvement you measure between uniform and unigram is the value of knowing corpus frequencies. Whatever improvement you measure between unigram and bigram is the value of remembering **one** token of context. Later chapters extend exactly this ladder — always judged by the same loss.

## <font color="#388bfd">From Counts to Probabilities</font>

Counting is the familiar part. The step your earlier Markov work may have skipped is turning a count table into a *forecast* that can be graded by the loss above.

Take a tiny synthetic sequence with a two-token vocabulary ($V = 2$), small enough to check every number by hand:

```text
[0, 1, 0, 1, 1]
```

Walk it once, recording each transition `current -> next`:

| Transition | Count |
|---|---:|
| 0 → 0 | 0 |
| 0 → 1 | 2 |
| 1 → 0 | 1 |
| 1 → 1 | 1 |

Counts alone are not predictions. A prediction must answer: *given that I am looking at token 0 right now, how should I divide 100% of my belief among the possible next tokens?* That word "divide" is the reason we normalize — the numbers for each current token must sum to exactly 1, because exactly one of the options will happen.

So we divide each count by its **row total**. Row 0 (transitions leaving token 0) has total 2:

$$P(1 \mid 0) = \frac{2}{2} = 1.0 \qquad P(0 \mid 0) = \frac{0}{2} = 0.0$$

The vertical bar is read "given": $P(1 \mid 0)$ is the probability of 1 *given* that the current token is 0. This is a **conditional probability**, the load-bearing idea on the modeling side of this chapter:

> **Conceptual hinge:** A bigram model is not merely a table of frequent pairs. Each **row** of the table is a separate categorical probability distribution, conditioned on the current token. Asking the model "what comes next?" means selecting one row and reading it as a forecast.

But look at what our two-line calculation just claimed: $P(0 \mid 0) = 0$. After seeing token 0 exactly twice, the model has concluded that 0 can **never** be followed by 0 — not "rarely," but *impossible*. You already know from Step C what that costs: one unseen transition in the test set, and $-\log 0 = \infty$ detonates the entire evaluation.

## <font color="#388bfd">Why Smoothing Exists</font>

To understand why smoothing is necessary — and what the `alpha` variable in your constructors is actually doing — look at the biggest flaw in basic probability models.

### <font color="#79c0ff">The zero probability problem</font>

Imagine you train a bigram model on a million books, but the phrase *"hilarious toaster"* never appears once. The entry `counts["hilarious"]["toaster"]` is 0. When your model is asked for the probability of "toaster" following "hilarious," it does the math:

$$\frac{0}{\text{rowTotal}} = 0.0$$

This is catastrophic, and you already know both reasons from the loss section. The probability of a whole sentence is the product of the probabilities of its parts — if even a single transition is exactly $0.0$, multiplying it by everything else instantly turns the entire sentence's probability to zero. The model is declaring, *"this sentence is mathematically impossible,"* merely because it never saw one specific word pairing. And on the measurement side, $-\log 0 = \infty$: one unseen transition detonates the entire evaluation.

Your held-out text **will** contain such transitions. That is not bad luck; it is the nature of language. Real text keeps producing reasonable pairings that no finite training corpus happens to contain — that is precisely why "hilarious toaster" is a *sentence you just understood* and simultaneously a count of zero.

### <font color="#79c0ff">The solution: additive smoothing</font>

The fix must guarantee the numerator is never zero, and it does so by artificially adding a small number to every single count. Here is the raw, unsmoothed unigram formula:

$$P(w) = \frac{\text{count}(w)}{N}$$

and here is the additively smoothed version:

$$P(w) = \frac{\text{count}(w) + \alpha}{N + \alpha V}$$

Exactly how the two new pieces work:

- **The numerator ($+\,\alpha$).** We pretend we saw every possible token $\alpha$ more times than we actually did. A token that appeared 0 times now has an effective count of $\alpha$. It is no longer impossible — just highly unlikely.
- **The denominator ($+\,\alpha V$).** The golden rule of probability is that all possible outcomes must sum to exactly $1.0$. We just added $\alpha$ to the numerator of *every one* of the $V$ tokens in the vocabulary, so the fractions became top-heavy. To rebalance the scales, we add $\alpha \times V$ to the denominator — exactly the total amount of fake count we handed out.

The bigram model applies the same repair to each row separately:

$$P(\text{next}=j \mid \text{current}=i) = \frac{\text{count}(i,j)+\alpha}{\sum_k \text{count}(i,k)+\alpha V}$$

Redo the tiny example from above with $\alpha = 1$:

$$P(1 \mid 0) = \frac{2+1}{2+2} = 0.75 \qquad P(0 \mid 0) = \frac{0+1}{2+2} = 0.25$$

$$P(0 \mid 1) = \frac{1+1}{2+2} = 0.50 \qquad P(1 \mid 1) = \frac{1+1}{2+2} = 0.50$$

Check each row: $0.75 + 0.25 = 1$ and $0.50 + 0.50 = 1$. The impossible became merely unlikely, and normalization survived.

### <font color="#79c0ff">Laplace versus additive smoothing</font>

You will hear these terms used interchangeably, but there is a distinction worth knowing:

- **Laplace smoothing** is the original technique, invented by Pierre-Simon Laplace in the 18th century. It specifically means $\alpha = 1$ — you simply add one to every count. It is often called *add-one smoothing*.
- **Additive smoothing** (sometimes *Lidstone smoothing*) is the modern generalization, where $\alpha$ can be any number greater than zero.

Your starter code implements the general form: `alpha` is a constructor parameter, not a constant.

### <font color="#79c0ff">Why is alpha a variable?</font>

Because in natural language processing, adding a full 1 to everything is usually far too aggressive.

Run the arithmetic: if your vocabulary has 50,000 tokens, add-one smoothing pours $50{,}000$ fake observations into the denominator. If your training document contains only 10,000 real tokens, the fake data completely overwhelms the real data — the denominator becomes $10{,}000 + 50{,}000 = 60{,}000$, and five sixths of it is fabricated. Every row flattens, and your carefully trained model becomes practically the uniform model, washing away the actual patterns it learned from real text.

Making $\alpha$ a variable — often a tiny fraction like $0.1$ or $0.01$ — gives zero-count tokens *just enough* probability to survive the math, without drowning the evidence.

Two things to understand about $\alpha$, not just memorize:

- **Smoothing does not invent evidence — it hedges.** The model still prefers what it saw; it just refuses to bet *everything* on a finite sample.
- **$\alpha$ is a dial between data and ignorance.** As $\alpha \to 0$ the model trusts raw counts completely (and courts the zero catastrophe); as $\alpha$ grows every row flattens toward uniform. Choosing $\alpha$ is your first *hyperparameter* decision — made by comparing validation losses, never test losses.

## <font color="#388bfd">The Experiment Boundary</font>

A count model can *memorize*. If you score it on the same text it counted, you learn how well it memorized — not how well it predicts. So before any training, the corpus is divided:

```text
document: [------------------------------------------]
          [        80% train        ][10% val][10% test]
```

The provided `splitDocuments` cuts each document into **contiguous** sections. Contiguous matters: nearby passages share near-identical local patterns, so randomly scattering windows across the three sets would plant near-copies of training text inside the test set, and every score would flatter the model.

The boundary rules, all of which the required tests enforce:

1. **Only training data updates counts.** Validation and test data are scored, never counted.
2. **No transition crosses a boundary.** The split hands you three separate lists per document, so a pair can never straddle train → validation.
3. **Validation chooses settings; test is touched once.** Tune $\alpha$ by comparing validation losses. Report test loss only after your choices are frozen.
4. **A learned tokenizer can leak too.** Merge rules learned from the *whole* corpus have already extracted statistics from the held-out text.

> **Warning:** Our own `Ch2_MarkovBaseline_Tester.java` trains BPE merges on the full files *before* splitting — a small, deliberate simplification for this week. Can you explain precisely why it is a leak? (Hint: merge rules learned from the whole corpus have already read the test text.)

When the course begins making **formal held-out comparisons**, the pipeline must change to the leak-free order, and the pieces are already in place for it:

1. **Split first.** The provided `splitDocuments` already keeps each document's training, validation, and test regions contiguous — that separation must survive every later design change.
2. **Learn merge rules from the training text only**, then freeze them. This is exactly why your Chapter 1 tokenizer records an ordered `MergeRule` list instead of just mutating its documents.
3. **Encode validation and test text with the frozen rules** — the job of the `encode` stub waiting in your tokenizer. The held-out text gets *tokenized* by the learned vocabulary but never *shapes* it.

## <font color="#388bfd">What You Are Given</font>

The programming this week is reinforcement: familiar counting and lookup patterns, kept short so your effort goes to the measurement ideas above. The starter code is in [starter/](starter/) — eight files. Three contain TODOs; the rest are complete infrastructure:

| File | Status | Role |
|---|---|---|
| [LanguageModel.java](starter/LanguageModel.java) | Complete | The two-method interface every model implements — this contract survives to Chapter 11 |
| [UniformModel.java](starter/UniformModel.java) | Complete | A fully worked example of the interface — read it first |
| [UnigramModel.java](starter/UnigramModel.java) | **TODO 1–2** | Frequency counting and smoothed probability |
| [BigramModel.java](starter/BigramModel.java) | **TODO 3–4** | Transition counting and conditional probability |
| [MarkovRevisited.java](starter/MarkovRevisited.java) | **TODO 5–6** | Provided: splitting, generation loop, validators. You write: evaluation and sampling |
| [EvaluationResult.java](starter/EvaluationResult.java) | Complete | Turns accumulated loss into average loss, perplexity, bits per byte |
| [CorpusSplit.java](starter/CorpusSplit.java) | Complete | The train/validation/test record |
| [Ch2_MarkovBaseline_Tester.java](starter/Ch2_MarkovBaseline_Tester.java) | Complete | Runs your Chapter 1 tokenizer, then the first model check |

`Ch2_MarkovBaseline_Tester.java` needs your completed Chapter 1 `Tokenizer.java` in the same folder — the archive pipeline is now cumulative: **files → bytes → tokens → predictions**. Note how it sizes the models: it asks `t.vocabularySize()` rather than assuming 512, because `train(256)` only guarantees *up to* 256 merges — on a small corpus, merging stops early the moment no pair repeats.

Implement the TODOs in this order, testing after each one. Each step isolates exactly one idea:

1. `UnigramModel.train` — count token frequency, training data only.
2. `UnigramModel.probability` — normalize counts with additive smoothing.
3. `BigramModel.train` — count `current -> next` transitions; never across a document boundary.
4. `BigramModel.probability` — normalize one outgoing row with additive smoothing.
5. `MarkovRevisited.evaluate` — the heart of the chapter: accumulate $-\log P(\text{target} \mid \text{context})$ over positions $1$ through $n-1$ of each document, so all three models are scored on identical targets (uniform and unigram simply ignore the context argument).
6. `MarkovRevisited.sampleNext` — draw one token from a categorical distribution.

The dense `long[V][V]` table in `BigramModel` is a deliberate choice: each row is *visible* as a distribution, which makes the concept and the tests easy. With byte tokens the whole table is about half a megabyte. It does not stay cheap — see the stretch goals.

## <font color="#388bfd">Generation: Making the Model Speak</font>

Scoring is how models are judged; generation is how their limits become visible. The provided `generate` loop does exactly this, using your `sampleNext`:

1. Take the final token of the output so far — that token is the model's *entire state*.
2. Read the model's probability for every possible next token — one categorical distribution.
3. Draw one random number $r$ in $[0, 1)$.
4. Walk the distribution, accumulating probability, until the running total exceeds $r$; that token wins.
5. Append it and repeat.

Picture the cumulative walk for a two-token row $[0.25, 0.75]$: the interval $[0, 0.25)$ belongs to token 0 and $[0.25, 1)$ to token 1. A draw of $r = 0.6$ lands in token 1's territory. Over many draws, each token wins in exact proportion to its probability — that is all "sampling from a distribution" means.

Use a **fixed seed** while debugging so every run reproduces the same text. Before you run the three models, write down your prediction: what should uniform output look like? Unigram? Bigram? (Expect: structureless noise; common characters with no local syntax; convincing local texture that loses the thread beyond one step.)

> **Note:** Generated output is a list of token identifiers. If you ran with raw bytes ($V = 256$, zero merges), each token *is* a byte — collect them into a `byte[]` and build a `String` to read your model's prose. If you trained BPE merges, token identifiers above 255 have no direct byte meaning — reading that output requires the decode stretch goal from Chapter 1. Raw bytes are the recommended first run.

## <font color="#388bfd">Evidence Checkpoint</font>

Fill in this table from your own runs, and record $\alpha$, $V$, the tokenizer used, and the random seed beside it so the experiment can be reproduced:

| Model | Training loss | Validation loss | Test loss |
|---|---:|---:|---:|
| Uniform | | | |
| Unigram | | | |
| Bigram | | | |

Three things the numbers must show before you trust anything else:

- Uniform loss equals $\ln V$ to several decimal places, on all three splits — and its perplexity equals $V$ exactly.
- Every row of your bigram table sums to approximately 1.
- The ladder holds: bigram beats unigram beats uniform on validation data.

## <font color="#388bfd">Failure Analysis</font>

Find **two** generated bigram passages that expose the one-token memory limit. For each, identify the exact token where the output goes wrong, then explain at the level of *state*:

1. Write the current token — the only thing the model actually knew.
2. Describe the continuation it sampled.
3. Name the earlier information that would have prevented the failure — and that sat outside the one-token state.
4. Explain why the corpus statistics still made the sampled continuation *locally* plausible.

Good hunting grounds: punctuation that opens and never coherently closes; a continuation that is plausible byte-by-byte but drifts into a different topic mid-word; a token that appeared in several incompatible contexts in training, forcing the model to average them together.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** A frequent continuation is not necessarily a true continuation. The model estimates patterns in its training corpus; it does not verify scientific, historical, or semantic truth.

More traps worth defusing now:

| If you catch yourself thinking… | Remember |
|---|---|
| "A model that guessed the wrong word deserves zero credit." | Accuracy thinks so; NLL correctly distinguishes a near-miss from an arrogant miss. |
| "Bigram means it remembers two previous tokens." | A bigram is *current and next*; the state holds exactly one token. |
| "Smoothing invents evidence." | Smoothing reserves probability mass so unseen events are not called impossible. |
| "Low training loss proves the better model." | Only held-out validation and test behavior counts in this course. |
| "Perplexity can compare any two models." | Across different tokenizers, use bits per original byte. |
| "Validation data can help the counts a little." | Validation chooses settings like $\alpha$; the moment it updates counts, it has become training data. |

## <font color="#388bfd">Stretch Goals</font>

1. **Trigram model** — two-token state; watch the count table become $V^3$.
2. **Variable-order N-gram model.**
3. **Interpolation** — a weighted combination of unigram, bigram, and trigram probabilities.
4. **Backoff** — use a shorter context whenever the longer one has inadequate evidence.
5. **Dense versus sparse memory** — the $256 \times 256$ `long` table costs about 0.5 MB, but a 30,000-token vocabulary would need roughly 7.2 GB. Rebuild the counts as a sparse `HashMap` and measure the difference.
6. **Fast categorical sampling** — precompute a cumulative or alias table instead of walking the row every draw.
7. **Corpus comparison** — train on local-history, science, and literary corpora and compare what each bigram model absorbs.
8. **Compression demonstration** — use your bits-per-byte number to predict how small your corpus could compress, then compare against an actual zip of the same file.

---

The Markov reader can imitate local texture, but it forgets almost everything. The next question is no longer whether counts help — they do. The question is how a model can carry forward useful information from farther back *without* enumerating every possible history. The answer begins with selective memory.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain what it means for a language model to "assign probability to reality," and how that differs from a deterministic lookup of the most common next token?
- [ ] Can you walk through the three steps that turn likelihood into negative log-likelihood — and name the specific problem each step solves?
- [ ] Can you compute the four smoothed probabilities for `[0, 1, 0, 1, 1]` with $V=2$ and $\alpha=1$ by hand, and verify each row sums to one?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you use the milk example to explain why accuracy scores a near-miss and an arrogant miss identically, while NLL separates them?
- [ ] Can you explain why the uniform model's perplexity is exactly $V$ and a perfect model's perplexity is exactly 1?
- [ ] Can you explain why the 80/10/10 split must be contiguous, using the near-duplicate-windows argument?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why mean squared error is the wrong loss for next-token prediction, and what NLL measures instead?
- [ ] Can you interpret a bits-per-byte of 3.5 as a compression claim, and explain when bits per byte must replace per-token loss?
- [ ] Can you explain why our Tester's train-merges-then-split pipeline is technically data leakage, and how to restructure it?

---

[Assignment](ASSIGNMENT.md)

← [Patterns Become Tokens](../Tokenizer/) — Next: [The Hand-Built Spotlight](../FixedAttention/)
