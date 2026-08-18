# Assignment — The Hand-Built Spotlight

**Duration:** 2 class periods  
**Due:** End of Week 3

---

## Objectives

By the end of this assignment you should be able to:

- **Keep the ground rules straight.** State what a position is, what the context window contains, and why nothing in this chapter samples tokens or touches a training corpus.
- **Convert scores to weights.** Implement a numerically stable softmax and explain what it guarantees (positive weights, rows summing to one) and what it never does (assign a permitted position exactly zero).
- **Fill one matrix three ways.** Implement the three fillings of the same causal attention matrix — equal scores (uniform averaging), hand-rule scores (a `ScoreRule`), and dot-product scores — and be able to say what each filling adds that the previous one lacked, and which parts of the pipeline never change at all.
- **Explain the three roles.** Describe query, key, and value with the card-table metaphor — the request slip, the card face, the card contents — and identify which position produces the query.
- **Cross the words-to-numbers bridge.** Explain why token identifiers cannot be dotted, and how feature vectors make match scores emerge from multiply-and-add.
- **Respect causality.** Produce exact-zero future weights and demonstrate that changing a future token cannot alter any earlier output.
- **Read and produce attention matrices.** Print the labeled table and interpret any row as the mixture a position used.

Nothing in this assignment trains. There are no learnable parameters and no backward pass — those arrive in later chapters.

---

## What You Are Given

Copy all four files from [starter/](starter/) into your project.

| File | Status | You write |
|---|---|---|
| [FixedAttention.java](starter/FixedAttention.java) | Starter | TODOs 1–7 (the validators at the bottom are provided) |
| [AttentionFixtures.java](starter/AttentionFixtures.java) | Complete | — |
| [ScoreRule.java](starter/ScoreRule.java) | Complete | — |
| [Tester.java](starter/Tester.java) | Complete | Rerun it after every TODO |

Do not modify the provided files or the validators. `Tester` reproduces every worked trace from the [lesson page](README.md) and reports each check as `PASS`, `FAIL`, or `TODO`.

---

## Part 1 — After Day 1

**On paper:** finish Check Yourself sets A and B from the lesson page and bring them to class. They are the raw material for Day 2's opening discussion.

**In code:** implement the first three TODOs, in order, rerunning `Tester` after each:

| # | Method | The idea it isolates |
|---|---|---|
| 1 | `uniformCausalWeights` | **Filling 1 — equal scores:** each permitted column of a row gets an equal share; every later column stays exactly `0.0` |
| 2 | `stableSoftmax` | Shared machinery, used by all three fillings: subtract the max, exponentiate, normalize — without mutating the input |
| 3 | `applyWeights` | Shared machinery — the blend: `outputs[query][slot]` sums `weights[query][key] * values[key][slot]` over every permitted `key` |

After Part 1, `Tester` must confirm: uniform rows sum to one with exact-zero futures, softmax reproduces `[2,1,0] -> [0.6652, 0.2447, 0.0900]` and `[4,0,0] -> [0.9647, 0.0177, 0.0177]`, equal scores produce equal weights, and blending the three-card fixture uniformly yields `y2 = [1.0, 0.6667, 0.3333, 0.0]`.

## Part 2 — After Day 2

Implement the remaining TODOs, in order:

| # | Method | The idea it isolates |
|---|---|---|
| 4 | `dotProduct` | Filling 3's scorer, met on its own first: multiply matching slots of `queryCard` and `keyCard`, add up the products |
| 5 | `ruleBasedCausalWeights` | **Filling 2 — hand-rule scores:** score each permitted position with a `ScoreRule`, then softmax only that permitted prefix |
| 6 | `dotProductCausalWeights` | **Filling 3 — dot-product scores:** TODO 5's skeleton with one line changed — scores are `dotProduct(queryCard, keyCard) / sqrt(slotsPerCard)` |
| 7 | `formatMatrix` | Shared machinery: the labeled ASCII attention matrix in the lesson's exact format |

Then two experiments:

1. **Run the full `Tester`.** It prints all three attention matrices for the three-card fixture, the uniform-versus-dot-product comparison at position 2, the Order A retrieval run, and the future-change demonstration.
2. **Write your own `ScoreRule`.** The provided `ORDER_RULE` scores the retrieval sequence with +3 for a matching order identifier, +1 for a matching category, minus a distance penalty. Write a second rule of your own design that still concentrates the earlier-position weight on the `Order A` cards, and be ready to defend your point values — there is no single correct rule, which is exactly the point of Stage 2.

---

## Required Tests

`Tester` covers all of these — confirm every one reports `PASS`:

- Each attention-matrix row sums to approximately one.
- All future-position weights are exactly zero.
- A one-token sequence returns a valid one-row matrix.
- Equal scores produce equal permitted weights.
- Adding the same constant to all permitted scores leaves softmax unchanged.
- A future input change leaves previous outputs unchanged.
- Known vectors produce known dot products.
- No input array is mutated.

---

## Concept Questions

Answer in your own words in the Canvas text box, below the stencil. Two to four sentences each — these carry as much weight as the code.

1. **The positions question.** The sequence is `[7, 12, 7, 31]`. Standing at position 2, which positions may attention use, and what weights does uniform averaging assign? Explain why the training corpus is irrelevant to your answer.
2. **The roles question.** Using the stat cards on the table, explain query, key, and value in one sentence each. Then state precisely where the query comes from — one position or many?
3. **The scores question.** Stage 2 produced scores `[4, 0, 0]`. Why can these not be used directly as mixing fractions? Name the two properties weights must have, and what softmax guarantees about each.
4. **The bridge question.** `PINEAPPLE` is token 301 and `PEPPERONI` is token 17. Explain why `301 * 17` is meaningless (cite Chapter 1's misconception) and what a feature vector provides that an identifier cannot.
5. **The zero-slot question.** In the dot product, why does a feature slot contribute nothing when either card holds `0.0` there? What happens to the score when a shared slot holds a negative value — and is a negative score a problem for softmax?
6. **The workflow question.** A classmate asks whether attention happens during training or during generation. Give the correct answer, and state what is — and is not — being trained in this chapter.
7. **The bridge-to-Chapter-2 question.** The bigram reader answered with one row lookup. Describe the spotlight reader's pipeline in four steps (compare, score, weigh, blend) and name the one capability it has that the bigram reader structurally cannot have.

---

## Grading Emphasis

| Area | Weight |
|---|---:|
| Attention implementations: TODOs 1–6 correct on the fixtures | 30% |
| Concept questions | 20% |
| Required tests all passing | 15% |
| Evidence: three matrices plus the uniform-versus-selective comparison | 15% |
| Causality demonstration and your own `ScoreRule` | 10% |
| Visualization (TODO 7) and code clarity | 10% |

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **All seven TODOs implemented** — no `UnsupportedOperationException` remains reachable.
- [ ] **The softmax traces reproduce by hand** — `[2,1,0]` yields `[0.6652, 0.2447, 0.0900]` and `[4,0,0]` yields `[0.9647, 0.0177, 0.0177]`.
- [ ] **Rows normalize** — every row of every attention matrix sums to approximately one.
- [ ] **The mask produces exact zeros** — every future-position weight is `0.0`, not merely small.
- [ ] **The pipeline trace reproduces** — dot-product attention at position 2 of the three-card fixture gives weights `[0.384, 0.233, 0.384]` and output `[1.0, 0.767, 0.233, 0.0]`.
- [ ] **The spotlight beats the blur** — the printed comparison shows `sweet` at 0.667 (uniform) versus 0.767 (dot product) at position 2.
- [ ] **Retrieval succeeds** — rule-based attention on the retrieval fixture concentrates earlier-position weight on the `Order A` cards, under both `ORDER_RULE` and your own rule.
- [ ] **The future is powerless** — the `Tester` demonstration shows identical outputs at positions 0 and 1 after the last card is replaced.
- [ ] **Paper problem sets A and B completed** — brought to Day 2, finished before submission.
- [ ] **All seven concept questions answered** — in your own words, with the specific numbers where asked.
- [ ] **Provided code unmodified** — the fixtures, `ScoreRule`, `Tester`, and validators are untouched.

---

## Submission

Submit **both text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box. Underneath it, paste your answers to the seven concept questions.

```
Softmax of [2.0, 1.0, 0.0]:
Dot product PINEAPPLE . PEPPERONI (4 slots):
Scaled scores at position 2 of the three-card fixture:
Dot-product attention weights at position 2:
Output y2 (dot-product attention):
Sweet feature at position 2 (uniform / dot product):
Your ScoreRule, described in one sentence:
Your rule's weights at the final retrieval position:
```

### Screenshot

The screenshot must show your program's console output from a full `Tester` run: all three attention matrices for the three-card fixture, the uniform-versus-dot-product comparison line, and the future-change demonstration result. A screenshot of source code alone, or of a partial run missing the matrices, does not qualify.
