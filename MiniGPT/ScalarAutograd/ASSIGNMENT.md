# Assignment — Following the Error Backward

*Lesson: [Following the Error Backward](README.md)*

**Duration:** 2 class periods  
**Due:** End of Week 6

---

## Objectives

By the end of this assignment you should be able to:

- **Write and read receipts.** For each of the six operations, state the local derivative and why — including the multiply crossover, the gate's all-or-nothing policy, and the exponential being its own sensitivity.
- **Audit a graph by hand.** Produce a full trace table — forward numbers, local derivatives, accumulated blame — for a small graph, showing the two rules at work: multiply along a path, add across paths.
- **Implement reverse-mode automatic differentiation.** Topological order, the seed of 1, the reverse walk, and the load-bearing `+=` — then prove it against the wiggle referee to six decimal places.
- **Rebuild the Chapter 5 network from receipts** and explain the clone reversal: why look-up must hand out the real card `Value`s this week, and where the read-only discipline moved.
- **Explain what the audit finds.** Score blames are forecast minus one-hot — Chapter 4's shortcut rediscovered — and a card used twice collects two envelopes into one mailbox.
- **Train the network and read the results.** The lifecycle in order (Reset, Grade, Measure, Nudge), the closed gap to Chapter 4's table, the floor that stops everyone, the reproduced oracle, and the drumbeat's two lessons.

Everything is fixed and deterministic — full-batch training has no seeds — so every number this assignment asks for must reproduce exactly, on any machine.

---

## What You Are Given

Copy all five files from [starter/](starter/) into your project.

| File | Status | You write |
|---|---|---|
| [Value.java](starter/Value.java) | Starter | TODOs 1–7 (the constructors, accessors, `setNumber`, `zeroGradient`, and `add` are provided) |
| [TrainableFeatureNetwork.java](starter/TrainableFeatureNetwork.java) | Starter | TODOs 8–12 (the constructor, validators, accessors, softmax, and `forecast` are provided) |
| [Trainer.java](starter/Trainer.java) | Starter | TODOs 13–14 (the reporting, the oracle comparison, and the experiment bench in `main` are provided) |
| [AutogradFixtures.java](starter/AutogradFixtures.java) | Complete | — |
| [Ch6_ScalarAutograd_Tester.java](starter/Ch6_ScalarAutograd_Tester.java) | Complete | Rerun it after every TODO |

Do not modify the provided files, the provided constructors, or the helpers. `Ch6_ScalarAutograd_Tester` reproduces every worked trace from the [lesson page](README.md) and reports each check as `PASS`, `FAIL`, or `TODO`; once everything passes, `java Trainer` produces the three experiment blocks you will quote in your submission.

---

## Part 1 — After Day 1 of 2

**On paper:** finish Check Yourself sets A and B from the lesson page and bring them to class. Set B's diamond audit — including what a second `backward` does — is the raw material for the second day's opening discussion.

**In code:** implement the engine, in order, rerunning `Ch6_ScalarAutograd_Tester` after each TODO:

| # | Method | The idea it isolates |
|---|---|---|
| 1 | `multiply` | The crossover: each ingredient's sensitivity is the other ingredient |
| 2 | `subtract` | Addition's twin — blame through the second door comes out negated |
| 3 | `rectify` | The gate's blame policy: an awake gate passes everything, a silenced gate returns to sender |
| 4 | `exponential` | The receipt whose result is its own sensitivity |
| 5 | `naturalLog` | Sensitivity $1/x$ — and a loud refusal at zero and below |
| 6 | `topologicalOrder` | Every ingredient before its dish, depth-first, visited exactly once |
| 7 | `backward` | Seed 1, walk in reverse, `+=` through every door — the audit itself |

After Part 1, `Ch6_ScalarAutograd_Tester` must confirm: the first trace lands on $4 / 2 / 1$, the reused leaf on $6$, the practice graph on $6 / 4 / 2$ with the silenced variant all exactly zero, the diamond on $21 / 16$ (and $63$ on an illegal second audit), and the composite referee graph agrees with the wiggle to $10^{-6}$ on all three leaves.

## Part 2 — After Day 2 of 2

Implement the network and the training, in order:

| # | Method | The idea it isolates |
|---|---|---|
| 8 | `weighAndAddValues` | Chapter 5's layer loop, third notation — same arithmetic, now leaving a trail |
| 9 | `unrestrictedScoreValues` | Fetch the REAL cards (no clones), join, mix, gate, score |
| 10 | `lossValueFromScores` | The grade as $\ln \sum e - $ target — division dissolved, `maxShift` a constant leaf |
| 11 | `averageLossValue` | One graph for the whole history — Chapter 4's bucket, dissolved into receipts |
| 12 | `zeroGradients` | Reset: parameters are the only survivors between steps, so only they need wiping |
| 13 | `gradientDescentStep` | The full lifecycle in order: Reset, Grade, Measure, Nudge |
| 14 | the loop in `train` | Learning is nothing else — the same step, repeated |

Then run `java Trainer` and record the three experiment blocks:

1. **The worked run.** Copy the 120-step trace plus the after-`pizza` and card lines. In one sentence: what closed the gap to Chapter 4's table, and what stops everyone at about $0.3174$?
2. **The oracle.** Copy the fresh-start loss, the 10-step loss, and the largest-gap line. In one sentence: what exactly did this run prove about Chapter 5's "trained offline" weights?
3. **The drumbeat.** Copy the before/after losses and the forecast line. In two sentences: why can the drumbeat reach near zero when the pizzeria cannot, and what happened to the pizzeria skill — by what mechanism?

---

## Required Tests

`Ch6_ScalarAutograd_Tester` covers all of these — confirm every one reports `PASS`:

- Each operation mints a new receipt with the right number, touches no ingredient, and assigns no blame at creation; `naturalLog` refuses zero and negatives; the gate is closed at exactly zero; computed receipts refuse `setNumber`.
- `topologicalOrder` lists every receipt exactly once, ingredients first, the audited receipt last — on the first trace and the diamond.
- `backward` reproduces every hand trace — $4/2/1$, the reused leaf's $6$, the practice graph's $6/4/2$, the silenced zeros, the diamond's $21/16$ — and moves no forward number.
- A second audit of the same graph corrupts ($21 \rightarrow 63$); fresh graphs without Reset accumulate ($-0.0597 \rightarrow -0.1193$); Reset restores.
- The wiggle referee agrees with the audit to $10^{-6}$ — on the composite graph and on three network parameters.
- The rebuilt pipeline reproduces Chapter 5 exactly: scores $[1.5504, -1.6160, -1.1503]$, forecast $[0.9015, 0.0380, 0.0605]$, losses $0.1037$ and $1.1377$, report card $0.3957 / 0.4013$ — and a hundred forecasts move no parameter.
- Score blames equal forecast minus one-hot; pineapple's card reads $[-0.0597, -0.0444]$, pepperoni's exactly zero.
- One step reports $0.3957$ and lands at $0.3754 / 0.3806$; thirty steps land at $0.3210 / 0.3252$ — past the table on both histories.
- Ten steps from the fresh start ($1.3626$) land at $0.3958$, within $0.005$ of every frozen number; the drumbeat memorizes below $0.005$ while the pizzeria decays past $2$; malformed contexts, tokens, and histories are refused.

---

## Concept Questions

Answer in your own words in the Canvas text box, below the stencil. Two to four sentences each — these carry as much weight as the code.

1. **The two-envelope question.** Chapter 5 ended by asking how credit is split when a card is used twice in one context. State the resolution precisely: which line of `backward` does the splitting, why look-up must not clone this week, and what pineapple's $-0.0597$ is made of.
2. **The shortcut question.** Chapter 4 gave you `p` minus one-hot as a formula to take on referee'd faith. What did this chapter reveal it to be, and why did Chapter 4's machine need only that one step of backpropagation while this machine needs many?
3. **The gate question.** On the featured flashcard, hidden units 0 and 1 received blame of $0.0321$ and $0.1271$ — and passed none of it on. Explain the mechanism, and what it means for a unit that is silenced on *every* flashcard in the deck.
4. **The referee question.** The wiggle experiment is too slow to train with, yet it referees the audit. Give both halves: the cost argument (evaluations per parameter, each way), and what a passing gradient check does and does not certify.
5. **The reset question.** Fresh graphs are born with zero gradients, yet `zeroGradients` is still required. What exactly survives between steps, what does its mailbox read after two un-reset audits of the featured flashcard, and what goes wrong at the nudge?
6. **The oracle question.** The fixtures print the fresh start as 49 literal numbers instead of drawing them from a seed. Why was that necessary, what did your 10-step run land within $0.005$ of, and why does full-batch determinism make this reproduction possible at all?
7. **The floor question.** After 120 steps the network sits at $0.3181$ against a floor of about $0.3174$ — yet the same engine drove the drumbeat to $0.0029$. Reconcile: what does the floor belong to, and what property of the drumbeat history removes it?

---

## Grading Emphasis

| Area | Weight |
|---|---:|
| Implementation: TODOs 1–14 correct on the fixtures | 30% |
| Concept questions | 20% |
| Required tests all passing | 15% |
| Evidence: the three experiment blocks with their explanations | 15% |
| Paper problem sets A and B, including the diamond audit | 10% |
| One-audit-per-graph and Reset discipline, and code clarity | 10% |

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **All fourteen TODOs implemented** — no `UnsupportedOperationException` remains reachable.
- [ ] **Every hand trace reproduces in code** — $4/2/1$, the practice graph's $6/4/2$, the silenced zeros, the diamond's $21/16$.
- [ ] **The referee is satisfied** — audit and wiggle agree to $10^{-6}$ on the composite graph and on three network parameters.
- [ ] **Chapter 5 reproduces through receipts** — scores, forecast, losses $0.1037$ / $1.1377$, and the $0.3957 / 0.4013$ report card.
- [ ] **The shortcut is rediscovered** — score blames $[-0.0985, 0.0380, 0.0605]$, equal to forecast minus one-hot.
- [ ] **The binder learns correctly** — pineapple $[-0.0597, -0.0444]$ (two envelopes), pepperoni exactly zero.
- [ ] **The gap closes** — the 120-step trace ends at $0.3181 / 0.3222$, past the table on both histories.
- [ ] **The oracle is reproduced** — ten steps from the fresh start, largest gap below $0.005$.
- [ ] **The drumbeat runs** — memorized below $0.005$, pizzeria forgotten past $2$, forecast above 99%.
- [ ] **Paper problem sets A and B completed** — brought to the second day of this lesson, finished before submission.
- [ ] **All seven concept questions answered** — in your own words, with the specific numbers where asked.
- [ ] **Provided code unmodified** — the fixtures, `Ch6_ScalarAutograd_Tester`, both constructors, the validators, the accessors, `add`, the softmax, and the bench are untouched.

---

## Submission

Submit **text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box. Underneath it, paste the three experiment blocks with their explanations, then your answers to the seven concept questions.

```
First trace blames (dL/da / dL/db / product's):
Practice graph blames (dL/dw / dL/dx / dL/db):
Diamond blames (dL/da / dL/db), and after an illegal second audit:
Score blames for [1,0,1] -> pizza, beside the forecast:
Pineapple slot 0 blame, and its two addends:
Referee verdict on pineapple slot 0 (audit / wiggle):
One step from frozen (loss reported / loss after):
120-step finish (training / validation):
Oracle reproduction (fresh loss / 10-step loss / largest gap):
Drumbeat after 50 steps (drumbeat loss / pizzeria loss):
```

### Screenshot

The screenshot must show your program's console output from a full `Ch6_ScalarAutograd_Tester` run: the Part 1 and Part 2 test results and the complete punchline block at the bottom. A screenshot of source code alone, or of a partial run missing the punchline block, does not qualify.
