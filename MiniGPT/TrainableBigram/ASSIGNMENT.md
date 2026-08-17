# Assignment — A Table That Learns

**Duration:** 2 class periods  
**Due:** End of Week 4

---

## Objectives

By the end of this assignment you should be able to:

- **Keep logits and probabilities straight.** Store unrestricted scores, convert one row to a forecast with the stable softmax from Chapter 3, and explain why the table does not store probabilities directly.
- **Grade one guess.** Implement cross-entropy loss — Chapter 2's penalty charged to a single prediction — and read its scale (0 for certainty in the truth, $\ln V$ for a uniform forecast, huge for confident error).
- **Compute the exact gradient.** Implement `p` minus one-hot for the used row, explain each entry's sign and magnitude, and verify it against a finite-difference wiggle.
- **Run the training loop.** Reset, accumulate a batch, average, and step — and explain *why* the loop averages and *why* it resets.
- **Read a loss trace.** Anchor step 0 at $\ln V$, recognize the loss floor set by the data's own disagreement, and diagnose too-cold and too-hot learning rates from the shape of the curve.
- **Compare learning with counting.** Show that gradient descent converges to Chapter 2's count frequencies on the same order history — with no exact zeros, because softmax cannot say never.

Everything is seeded and deterministic: every number this assignment asks for must reproduce exactly, on any machine.

---

## What You Are Given

Copy all four files from [starter/](starter/) into your project.

| File | Status | You write |
|---|---|---|
| [TrainableBigramModel.java](starter/TrainableBigramModel.java) | Starter | TODOs 1–7 (the constructor and the helpers at the bottom are provided) |
| [TrainingData.java](starter/TrainingData.java) | Complete | — |
| [Trainer.java](starter/Trainer.java) | Complete | — |
| [Tester.java](starter/Tester.java) | Complete | Rerun it after every TODO |

Do not modify the provided files, the provided constructor, or the helpers. `Tester` reproduces every worked trace from the [lesson page](README.md) and reports each check as `PASS`, `FAIL`, or `TODO`. `Trainer` is the experiment bench — `java Trainer` runs the full training run, the learned-versus-counted comparison, and the learning-rate experiment.

---

## Part 1 — After Day 1

**On paper:** finish Check Yourself sets A and B from the lesson page and bring them to class. They are the raw material for Day 2's opening discussion.

**In code:** implement the first four TODOs, in order, rerunning `Tester` after each:

| # | Method | The idea it isolates |
|---|---|---|
| 1 | `stableSoftmax` | Chapter 3's three steps — subtract the max, exponentiate, normalize — without mutating the input |
| 2 | `probabilities` | One row of the table, read as a prediction distribution |
| 3 | `loss` | Cross-entropy for one flashcard: `-Math.log` of the probability given to the target |
| 4 | `backward` | The shortcut gradient `p[nextToken] - (nextToken == target ? 1 : 0)`, *accumulated* into the used row only |

After Part 1, `Tester` must confirm: softmax reproduces `[2,1,0] -> [0.6652, 0.2447, 0.0900]` and survives `[1000, 999, 998]` without overflow, the worked row `[1.2, 0.1, -0.4]` forecasts `[0.6516, 0.2169, 0.1315]` and charges loss `1.5284` for target `pineapple`, the gradient comes out `[0.6516, -0.7831, 0.1315]` and sums to zero, and the gradient check's analytical-versus-wiggle gap prints below $10^{-6}$.

## Part 2 — After Day 2

Implement the remaining TODOs, in order:

| # | Method | The idea it isolates |
|---|---|---|
| 5 | `step` | Average the accumulated gradients (divide by the example count), stride against the slope |
| 6 | `zeroGradients` | Wipe every gradient and the example count — a stale slope describes a table that no longer exists |
| 7 | `averageLoss` | Chapter 2's evaluation: mean loss over every adjacent pair of a token history |

Then run the two experiments on the bench:

1. **The training run.** `java Tester` now trains for 300 steps (batch 24, learning rate 0.5) and prints the CSV loss trace. It must match the lesson page digit for digit — from `1.0987` at step 0 down to `0.3300 / 0.3311` at step 300 — followed by the learned-versus-counted table. Copy the CSV lines into a `.csv` file; that file is part of your submission evidence.
2. **The learning-rate experiment.** `java Trainer` reruns the same training at learning rates 0.01, 0.5, and 20. Record the three final losses and, in one sentence each, describe the shape of each run using the lesson's vocabulary (crawl, floor, bounce).

---

## Required Tests

`Tester` covers all of these — confirm every one reports `PASS`:

- Softmax sums to one, survives huge logits, and is unchanged by adding a constant to every logit.
- Cross-entropy is near zero for a near-certain correct prediction and large when the truth was called nearly impossible.
- A uniform row costs exactly $\ln 3$ — Chapter 2's anchor.
- Analytical and finite-difference gradients agree at every logit.
- Gradient entries sum to zero, and only the current token's row receives them.
- `backward` changes no logits; `step` moves no row that accumulated nothing.
- Accumulated gradients are averaged, not summed — and `step` with nothing accumulated is refused.
- One gradient step lowers the loss on a one-example dataset (`1.5284` down to `1.0474`).
- Training reduces both training and validation loss, and the learned table matches the counted one.
- A fixed seed reproduces the initial table and the entire training run exactly.

---

## Concept Questions

Answer in your own words in the Canvas text box, below the stencil. Two to four sentences each — these carry as much weight as the code.

1. **The handcuffs question.** The table stores logits and softmaxes on demand, instead of storing probabilities and nudging those directly. What two constraints make stored probabilities miserable to update, and how does the logits-plus-softmax design dodge both?
2. **The messenger question.** A classmate says "the gradient tells the model the right answer." Correct them precisely: what does $\partial L / \partial z_0 = 0.6516$ actually assert about the `pizza` logit, and where in the pipeline does the right answer actually enter?
3. **The signs question.** For the worked gradient `[0.6516, -0.7831, 0.1315]`, explain why exactly one entry is negative, what subtracting each entry does to its logit, and why the three entries must sum to zero.
4. **The anchor question.** Before training, the loss trace starts at `1.0987`. Which Chapter 2 anchor is this, why must a nearly empty table land there, and what should you conclude if your step-0 line prints `0.6931` instead?
5. **The averaging question.** `step` divides the accumulated gradients by the number of examples before updating. What silently goes wrong if you sum instead of average — and which dial does a growing batch size then secretly turn?
6. **The lonely-rows question.** In the batch `pizza -> pineapple`, `pineapple -> pizza`, `pizza -> pepperoni`, which rows receive gradient and why not `pepperoni`'s? What does this row isolation mean for a rare token in a 50,000-word vocabulary?
7. **The two-tables question.** After 300 steps, the learned table sits within a few hundredths of the counted one — but `P(pizza | pizza)` is `0.009`, not `0.000`. Explain both facts: why gradient descent converges toward the count frequencies, and which Chapter 3 fact about softmax makes an exact zero impossible (and which Chapter 2 repair that resembles).

---

## Grading Emphasis

| Area | Weight |
|---|---:|
| Model implementation: TODOs 1–7 correct on the fixtures | 30% |
| Concept questions | 20% |
| Required tests all passing | 15% |
| Evidence: the CSV loss trace and the learned-versus-counted table | 15% |
| Learning-rate experiment with shape descriptions | 10% |
| Gradient check understanding and code clarity | 10% |

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **All seven TODOs implemented** — no `UnsupportedOperationException` remains reachable.
- [ ] **The worked trace reproduces by hand** — softmax `[0.6516, 0.2169, 0.1315]`, loss `1.5284`, gradient `[0.6516, -0.7831, 0.1315]`.
- [ ] **One step lowers the loss** — learning rate 0.5 moves the worked row to `[0.8742, 0.4916, -0.4658]` and the loss to `1.0474`.
- [ ] **The anchor holds** — a nearly empty table's average training loss prints `1.0987`, matching $\ln 3$.
- [ ] **The gradient check passes** — worst analytical-versus-wiggle gap below $10^{-6}$.
- [ ] **The loss trace reproduces digit for digit** — ending at `0.3300` training, `0.3311` validation — and is saved as a `.csv` file.
- [ ] **The tables converge** — learned probabilities within a few hundredths of the counted frequencies, with no exact zeros.
- [ ] **The learning-rate experiment is recorded** — three final losses plus a one-sentence shape description each.
- [ ] **Paper problem sets A and B completed** — brought to Day 2, finished before submission.
- [ ] **All seven concept questions answered** — in your own words, with the specific numbers where asked.
- [ ] **Provided code unmodified** — the fixtures, `Trainer`, `Tester`, the constructor, and the helpers are untouched.

---

## Submission

Submit **text, a screenshot, and your CSV file** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box. Underneath it, paste your answers to the seven concept questions.

```
Softmax of the worked row [1.2, 0.1, -0.4]:
Loss for target pineapple:
Gradient of the worked row:
Row after one step (lr 0.5) and its new loss:
Nearly-empty-table average training loss (seed 7):
Final training / validation loss (300 steps, batch 24, lr 0.5):
Learned P(pineapple | pizza) vs the counted frequency:
Largest analytical-vs-wiggle gap from the gradient check:
Final training loss at lr 0.01 / 0.5 / 20:
```

### Screenshot

The screenshot must show your program's console output from a full `Tester` run: the test results, the complete CSV loss trace from step 0 to step 300, and the learned-versus-counted comparison table. A screenshot of source code alone, or of a partial run missing the trace or the table, does not qualify.
