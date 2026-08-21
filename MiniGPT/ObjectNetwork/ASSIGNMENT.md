# Assignment — From Exact Symbols to Features

*Lesson: [From Exact Symbols to Features](README.md)*

**Duration:** 2 class periods  
**Due:** End of Week 5

---

## Objectives

By the end of this assignment you should be able to:

- **Compute one unit by hand.** Weigh and add — bias plus every input times its wire's weight — then gate the total with the Rectified Linear Unit, and say what a silenced unit contributes downstream (nothing).
- **Keep reads and writes straight.** Name, for every array a forecast touches, whether it is read, created, or overwritten — and explain why calling `forecast` twice must return bit-for-bit identical answers.
- **Show that objects and arrays are one machine.** Build a unit as a `Neuron` graph and as a `weighAndAdd` row and demonstrate agreement to $10^{-9}$.
- **Prove the gate earns its place.** Collapse a gateless two-layer network into a single weighted sum with algebra, and point to the input-dependent routing that the gate makes possible.
- **Run the forecast pipeline.** Look up, join, weigh, gate, weigh, softmax — in that order, reproducing every worked number from the lesson page, and grade the result with Chapter 4's unchanged loss.
- **Argue the punchlines with numbers.** The topping cards are cousins the network found on its own; the after-pizza mixture reappears without any stored row; the parameter formula beats $V^2$ at archive scale; and the frozen model's remaining gap is unfinished training, not architecture.

Everything is fixed and deterministic: every number this assignment asks for must reproduce exactly, on any machine.

---

## What You Are Given

Copy all five files from [starter/](starter/) into your project.

| File | Status | You write |
|---|---|---|
| [Connection.java](starter/Connection.java) | Complete | — |
| [Neuron.java](starter/Neuron.java) | Starter | TODOs 1–2 (the factories and the state helpers are provided) |
| [FeatureNetwork.java](starter/FeatureNetwork.java) | Starter | TODOs 3–10 (the constructor, the softmax, the parameter count, and the validators are provided) |
| [NetworkFixtures.java](starter/NetworkFixtures.java) | Complete | — |
| [Ch5_ObjectNetwork_Tester.java](starter/Ch5_ObjectNetwork_Tester.java) | Complete | Rerun it after every TODO |

Do not modify the provided files, the provided constructor, or the helpers. `Ch5_ObjectNetwork_Tester` reproduces every worked trace from the [lesson page](README.md) and reports each check as `PASS`, `FAIL`, or `TODO`; once everything passes, it also prints the punchline block you will quote in your submission. The provided model's 49 numbers were trained offline and are frozen — nothing you write this week changes any of them, and the Tester checks exactly that.

---

## Part 1 — After Day 1 of 2

**On paper:** finish Check Yourself sets A and B from the lesson page and bring them to class. Set B's collapse algebra is the raw material for the second day's opening discussion.

**In code:** implement the first four TODOs, in order, rerunning `Ch5_ObjectNetwork_Tester` after each:

| # | Method | The idea it isolates |
|---|---|---|
| 1 | `weighAndAddInputs` | One neuron reads its wires — bias plus value-times-weight, totaled; reading writes nothing |
| 2 | `recomputeValue` | The gate, then the chapter's only overwrite: the neuron's own stored value |
| 3 | `weighAndAdd` | A whole layer as one loop over a weight table — a row of neurons without the objects |
| 4 | `rectify` | The gate for a whole layer: negatives silenced to exactly zero, in a new array |

After Part 1, `Ch5_ObjectNetwork_Tester` must confirm: the practice network lands on $[-2, 4]$, $[0, 4]$, $[-4, 6]$ from objects and from arrays alike, the gateless collapse produces $[-8, 4]$ both ways, and hidden unit 3 of the provided model computes $1.8724$ as an object graph and as an array call, agreeing to $10^{-9}$.

## Part 2 — After Day 2 of 2

Implement the remaining TODOs, in order:

| # | Method | The idea it isolates |
|---|---|---|
| 5 | `lookUpStatCards` | Step 1 — token numbers are addresses; cards are fetched as clones, never computed |
| 6 | `joinCards` | Step 2 — cards glued into one row, order preserved, because order is meaning |
| 7 | `unrestrictedScores` | Steps 1–5 chained — fetch, glue, mix, gate, score: logits, manufactured instead of fetched |
| 8 | `forecast` | Step 6 — the provided softmax turns scores into a distribution, exactly as in Chapter 4 |
| 9 | `loss` | Step 7 — Chapter 4's grade, unchanged; computed, and then deliberately nothing happens |
| 10 | `averageLoss` | The report card over a history — flashcards start at position three, so 122 tokens hold 119 |

Then record the punchline readings from the full `Ch5_ObjectNetwork_Tester` run:

1. **The cousins.** Copy the three card distances and the two topping-context forecasts. In one sentence each: what did the network discover about the toppings, and which shared arrays carry the discovery?
2. **The mixture.** Copy the after-pizza forecast beside the counted row. In one sentence: where did the 40-vs-20 mixture live, given that no pizza row exists anywhere in this model?
3. **The leaderboard.** Copy the four loss lines (anchor, this network, Chapter 4's table, the floor). In one sentence: why is the network's gap above the table not an argument against networks?

---

## Required Tests

`Ch5_ObjectNetwork_Tester` covers all of these — confirm every one reports `PASS`:

- A neuron's weighted sum reproduces the practice numbers, and computing it twice writes nothing — not even its own stored value.
- `recomputeValue` overwrites the stored value; the gate silences negatives to exactly zero and passes positives; a linear unit keeps its negatives.
- The practice network lands on $[-4, 6]$ as objects and as arrays, and collapses to $[-8, 4]$ without the gate.
- `weighAndAdd` and `rectify` return new arrays, leave their inputs untouched, and refuse mismatched shapes.
- Look-up fetches the right cards as clones — scribbling on a fetched card leaves the binder clean.
- Joining preserves order: $[1, 0, 2]$ and $[2, 0, 1]$ join differently.
- The pipeline reproduces every worked number: hidden sums $[-0.1817, -1.1491, 0.3005, 1.8724]$, scores $[1.5504, -1.6160, -1.1503]$, forecast $[0.9015, 0.0380, 0.0605]$, losses $0.1037$ and $1.1377$.
- A four-token history holds exactly one flashcard; the provided model scores $0.3957 / 0.4013$; a nearly empty network (seed 7) sits at $\ln 3$.
- The topping cards are cousins, both topping contexts forecast pizza above 85%, and the after-pizza forecast matches the counted mixture with no exact zero.
- A hundred forecasts change no stat card; the parameter count is exactly 49; short contexts, out-of-range tokens, and flashcard-less histories are refused.

---

## Concept Questions

Answer in your own words in the Canvas text box, below the stencil. Two to four sentences each — these carry as much weight as the code.

1. **The address question.** A classmate implements look-up as `tokenNumber * someVector` and their shapes all work out. Explain what their design forces onto pepperoni's representation relative to pineapple's, and onto pizza's — and why fetching has no such problem.
2. **The gate question.** Summarize your Set B collapse proof: what single machine is a gateless two-layer network equal to, and what specifically can a gated network do that the collapsed machine cannot? Use the two contexts' different awake squads as your evidence.
3. **The read-write question.** List every write that occurs anywhere in this chapter's code, and every array that is only ever read. Why does the Tester run a hundred forecasts and compare stat cards before and after?
4. **The sharing question.** Chapter 4's flaw: 41 pineapple flashcards taught pepperoni's row nothing. State precisely which of this network's five arrays a pineapple flashcard adjusted during offline training, and which of those a pepperoni forecast flows through. Then translate to mushroom and olive in the archive's full vocabulary.
5. **The anchor question.** A nearly empty network — random near-zero cards and weights, zero biases — scores $1.0986$ before any training, the third machine in a row to do so. Trace why: what do near-zero weights make the scores, and what does softmax make of near-equal scores?
6. **The frozen question.** The provided network sits at $0.3957$ against the table's $0.3300$, and the lesson claims the gap is closable in principle. What exactly is missing — name the two switched-off beats of Chapter 4's loop — and why does Chapter 4's `p` minus one-hot shortcut not survive the trip into this machine?
7. **The scale question.** With the parameter formula, compute the count for $V = 50{,}000$, $D = 64$, $C = 3$, $H = 256$, and compare it to the $V^2$ table. Then give the deeper half of the argument: what happens to a rare token in each design?

---

## Grading Emphasis

| Area | Weight |
|---|---:|
| Implementation: TODOs 1–10 correct on the fixtures | 30% |
| Concept questions | 20% |
| Required tests all passing | 15% |
| Evidence: the punchline readings with their one-sentence explanations | 15% |
| Paper problem sets A and B, including the collapse algebra | 10% |
| Read-write discipline and code clarity | 10% |

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **All ten TODOs implemented** — no `UnsupportedOperationException` remains reachable.
- [ ] **The practice trace reproduces by hand and in code** — $[-2, 4]$, $[0, 4]$, $[-4, 6]$, and the gateless collapse $[-8, 4]$.
- [ ] **Objects equal arrays** — hidden unit 3 lands on $1.8724$ both ways, agreeing to $10^{-9}$.
- [ ] **The worked forecast reproduces** — scores $[1.5504, -1.6160, -1.1503]$, forecast $[0.9015, 0.0380, 0.0605]$, loss $0.1037$.
- [ ] **The anchor holds** — the nearly empty network (seed 7) prints $1.0986$, matching $\ln 3$.
- [ ] **The report card reproduces** — training loss $0.3957$ over 119 flashcards, validation loss $0.4013$ over 39.
- [ ] **The punchlines are recorded** — cousins distances, both topping forecasts, the after-pizza mixture beside the counted row, and the leaderboard, each with its one-sentence explanation.
- [ ] **Nothing moves** — the read-only test passes: a hundred forecasts change no stat card.
- [ ] **Paper problem sets A and B completed** — brought to the second day of this lesson, finished before submission.
- [ ] **All seven concept questions answered** — in your own words, with the specific numbers where asked.
- [ ] **Provided code unmodified** — `Connection`, the fixtures, `Ch5_ObjectNetwork_Tester`, the constructor, the softmax, the parameter count, and the validators are untouched.

---

## Submission

Submit **text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box. Underneath it, paste the three punchline readings with their one-sentence explanations, then your answers to the seven concept questions.

```
Practice network outputs for inputs [1, 2]:
Gateless collapse outputs, and the single weighted sum for outputFirst:
Joined row for context [1, 0, 1]:
Hidden weighted sums / after the gate:
Unrestricted scores:
Forecast, and the loss for target pizza:
Forecast after pizza [0, 1, 0] vs Chapter 4's counted row:
Card distances (pineapple-pepperoni / pizza-pineapple / pizza-pepperoni):
Nearly-empty-network average training loss (seed 7):
Provided model training / validation loss:
Parameter count, with the three-term arithmetic:
```

### Screenshot

The screenshot must show your program's console output from a full `Ch5_ObjectNetwork_Tester` run: the Part 1 and Part 2 test results and the complete punchline block at the bottom. A screenshot of source code alone, or of a partial run missing the punchline block, does not qualify.
