<div align="center">

# Following the Error Backward
*<font color="#8b949e">Backpropagation and a scalar automatic-differentiation engine</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The network predicts the wrong token. Forty-nine numbers contributed to that decision — some pushed it toward the error, some pulled against it, and one card was consulted twice in the same forecast. The loss is a single verdict with no way to reach any of them. The machine needs to trace its own error backward through every calculation that produced it.

## <font color="#388bfd">Question to Carry</font>

> **How can the model determine how much each of its numbers contributed to its final error?**

## <font color="#388bfd">Where This Chapter Sits in the Loop</font>

Chapter 4's life cycle — **forecast, grade, measure the slope, nudge** — has been half-dead for a week. Chapter 5 rebuilt the forecast as a network and then had to switch the last two beats off, because no tool you owned could trace blame through it. This chapter builds that tool and turns the beats back on:

| Beat of the loop | Chapter 4 — the table | Chapter 5 — the network | This chapter |
|---|---|---|---|
| 1. Forecast | Read a row, softmax it | The six-step pipeline | Same pipeline — but every step now writes a receipt |
| 2. Grade | $-\ln$ of the truth's probability | Identical | Identical — rebuilt so the grade can be audited |
| 3. Measure | `p` minus one-hot, into the bucket | **Switched off** | **Back on:** one backward pass blames all 49 numbers |
| 4. Nudge | One stride downhill | **Switched off** | **Back on:** one stride moves all 49 numbers |

Chapter 4 promised this moment by name: computing the gradient walks the forecast's road in reverse, so every training library calls it the **backward pass** and names the method `backward`. This is the chapter that writes it.

The chapter is two class periods. Each day ends with homework:

| Day | In class | Homework |
|---|---|---|
| 1 | Receipts and their sensitivities · the chain rule · the first trace · the practice graph and its trace table · the audit order · `backward` | [Assignment](ASSIGNMENT.md) Part 1 — TODOs 1–7 plus problem sets A and B on paper |
| 2 | The network rebuilt from receipts · the loss written for the audit · one backward through the whole machine · the nudge returns · the training run · the oracle · the drumbeat | [Assignment](ASSIGNMENT.md) Part 2 — TODOs 8–14, the evidence runs, and the concept questions |

## <font color="#388bfd">The Starting Line</font>

Same tiny world: the pizzeria's order history, the 122-token training history and 42-token validation history, and the exact network Chapter 5 handed you — 49 numbers, still scoring $0.3957$ training and $0.4013$ validation against the table's $0.3300$ and $0.3311$. Three ground rules for the week:

1. **The frozen weights are the starting line, not the exhibit.** Chapter 5's model arrives in the fixtures unchanged — and this week you resume the training that produced it, from exactly where it stopped.
2. **Nothing is random this week.** Chapter 4 drew random batches, so runs needed seeds. This chapter grades *every* flashcard on *every* step — full batch — so there is nothing to draw, and every machine prints the same loss trace to the last digit.
3. **Receipts are scratch; parameters survive.** Every forecast and every training step builds a fresh pile of records and throws it away, exactly like Chapter 5's scratch rows. The 49 parameters are the only things that persist — the only place blame collects, and the only numbers a nudge may move.

## <font color="#388bfd">Vocabulary — Day 1</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Computation graph | Every operation of one calculation, recorded with what it depended on. | The complete paper trail of one forecast |
| `Value` | One number plus the record of how it was made — this chapter's one new class. | A receipt: the result, the ingredients, the sensitivities |
| Parent | An earlier `Value` used to compute this one. | An ingredient named on the receipt |
| Leaf | A `Value` with no parents: a parameter or a plain input. | A raw ingredient — no receipt behind it |
| Local derivative | How sensitive one result is to one direct ingredient. | The sensitivity, noted on the receipt at purchase time |
| Chain rule | Sensitivities multiply along a path of operations. | Blame scaled at every hop of the trail |
| Gradient accumulation | Blame arriving by different paths adds up. | Two envelopes into the same mailbox |
| Upstream gradient | The blame a receipt has collected from everything computed after it. | The envelope handed back down the trail |
| Topological order | A list where every `Value` appears after all of its ingredients. | Ingredients before dishes |
| Backward pass, or backpropagation | The audit: walk the trail newest-to-oldest, delivering blame. | The auditor working the stack of receipts in reverse |
| Automatic differentiation, or autograd | Exact derivatives computed by recording operations and applying local rules. | Calculus done by bookkeeping |
| Reverse mode | Autograd run from one output back toward many inputs. | One verdict, blame for everyone |

---

## <font color="#388bfd">Day 1 — The Audit, One Receipt at a Time</font>

## <font color="#388bfd">The Dead End, Measured</font>

You already own one tool that finds slopes without seeing inside the machine: Chapter 4's wiggle experiment. Nudge one parameter up by a hair, re-run the whole pipeline, nudge it down, re-run again — two full evaluations buy the slope of *one* parameter. For this chapter's toy that is $98$ pipeline runs per flashcard. For the final course model's roughly $34{,}000$ parameters it is $68{,}000$ runs per flashcard *per step* — Chapter 5 already called that reflex a dead end.

Here is the claim this chapter makes good on: **one forward pass plus one backward pass produces the exact slope of the loss with respect to every parameter at once.** Not an estimate — exact, to floating-point precision, for the cost of roughly one extra trip through the calculation. The trick is that the machine keeps records.

## <font color="#388bfd">Every Big Calculation Is Made of Small Ones</font>

Look back at Chapter 5's pipeline with a bookkeeper's eye. Fetch, join, weigh, gate, weigh, grade — strip away the vocabulary and every single step is built from six tiny operations:

$$x + y \qquad x - y \qquad x \cdot y \qquad \max(0, x) \qquad e^{x} \qquad \ln(x)$$

Nothing else. The whole sophisticated machine is thousands of these, chained. So the plan is not to differentiate *the network* — it is to know, for each tiny operation, how blame passes through it, and then let bookkeeping chain those small answers through any machine whatsoever. That is **automatic differentiation**: calculus supplies six little facts, and a data structure does the rest.

The data structure is a **receipt**. Every time an operation runs, it creates one record holding three things:

1. **The result** — the number it computed.
2. **The ingredients** — which earlier receipts it was computed from.
3. **One sensitivity per ingredient** — if that ingredient wiggled by a tiny amount, how much would this result wiggle? This is the **local derivative**, and it is written down at the moment of creation, while the operation still knows its own numbers.

The word *local* is doing real work: a receipt knows nothing about the loss, the network, or what happens later. It records only its own one-step arithmetic. The audit will do the rest.

## <font color="#388bfd">The Six Sensitivities</font>

Each operation's local derivatives, with the reason in plain words:

| Operation | Result | Sensitivity to each ingredient | Why |
|---|---|---|---|
| $x + y$ | the sum | $1$ and $1$ | wiggle either ingredient, the sum follows it exactly |
| $x - y$ | the difference | $1$ and $-1$ | the second ingredient pulls the opposite way |
| $x \cdot y$ | the product | $y$ and $x$ — **the other ingredient** | wiggling $x$ gets scaled by $y$ on its way in |
| $\max(0, x)$ | the gated value | $1$ if $x > 0$, else $0$ | an awake gate passes wiggles; a silenced gate outputs 0 no matter what |
| $e^{x}$ | the exponential | the result itself | $e^x$ is its own rate of change — the one calculus fact this chapter asks you to accept |
| $\ln(x)$ | the natural logarithm | $1 / x$ | steep near zero, nearly flat far out — also accepted, and the referee will verify both |

Two conventions worth pinning down now. The gate at *exactly* zero stays closed — sensitivity $0$, matching Chapter 5's rule that a weighted sum of exactly zero shows zero. And $\ln$ of zero or a negative number is not a number, so the operation refuses such an ingredient loudly.

### <font color="#79c0ff">Check yourself — Set A</font>

Answers are in the [Answer Key](#answer-key) below. Do these on paper before moving on.

1. The receipt for $p = u \cdot v$ with $u = -2$, $v = 5$: what result does it hold, and what sensitivity does it record for each ingredient?
2. The gate $r = \max(0, z)$: what sensitivity does its receipt record at $z = 3$? At $z = -3$? At exactly $z = 0$?
3. The receipt for $d = u - v$ with $u = 1$, $v = 4$: the result and both sensitivities. Now blame of $-2$ arrives at $d$ — how much reaches $u$, and how much reaches $v$?
4. The receipt for $e^{x}$ at $x = 0$: result and sensitivity. The receipt for $\ln(x)$ at $x = 2$: result and sensitivity.

## <font color="#388bfd">The Chain Rule: Blame Flows Multiplied</font>

Now chain two receipts. Suppose $a$ feeds $c$, and $c$ feeds the loss $L$. You know two local facts: wiggling $a$ moves $c$ at some rate, and wiggling $c$ moves $L$ at some rate. Then wiggling $a$ moves $L$ at the *product* of the two rates — the first wiggle is scaled once on the way into $c$ and again on the way into $L$. That is the entire **chain rule**: along a path, sensitivities multiply.

One more rule and the whole method is on the table: if $a$ reaches $L$ by *two different paths*, each path delivers its own blame, and the deliveries **add**. Why addition? Wiggle $a$ by a hair and both paths transmit the wiggle simultaneously — their effects on $L$ arrive together, summed. That is **gradient accumulation**, and it is about to matter enormously: remember that in Chapter 5, pineapple's card sat in the joined row *twice*.

## <font color="#388bfd">First Worked Trace</font>

The smallest graph with a fork in it:

$$c = a \cdot b \qquad L = c + a$$

with $a = 2$, $b = 3$. Forward: $c = 6$, $L = 8$. Now the audit, by hand. $a$ reaches $L$ two ways:

```text
path through c:  a's wiggle is scaled by 3 entering c (multiply: the other
                 ingredient), then by 1 entering L (add)      ->  3 * 1 = 3
direct path:     a's wiggle enters L through the add          ->  1
total blame for a:                                                3 + 1 = 4
```

So $\partial L / \partial a = 4$. For $b$ there is one path: scaled by $2$ entering $c$ (the other ingredient), then by $1$ entering $L$ — total $2$. Check it the Chapter 4 way, with an actual wiggle: raise $a$ to $2.01$ and recompute — $c = 6.03$, $L = 8.04$. The loss moved $0.04$ for a wiggle of $0.01$: rate $4$, exactly as the receipts said.

> **Note:** gradients answer "which direction, and how steeply" — not "what should the new value be." The number $4$ says: raise $a$ and $L$ rises four times as fast. It is a slope, and the stride length is still a separate decision, exactly as in Chapter 4.

## <font color="#388bfd">The Receipt, as an Object</font>

The starter code makes the receipt a class called `Value` — one scalar that remembers how it was made:

```java
Value a = new Value(2.0, "a");
Value b = new Value(3.0, "b");
Value L = a.multiply(b).add(a);    // forward: 8.0 — and two receipts written
L.backward();                       // the audit
a.gradient();                       // 4.0
```

`a` and `b` are **leaves** — original numbers with no ingredients. Every operation mints one new `Value` recording its parents and local derivatives. `add` is provided as the worked example; the other five operations are yours (TODOs 1–5). The design you are building is the standard one — the same shape sits at the heart of [a working GPT built on scalar autograd](https://karpathy.github.io/2026/02/12/microgpt/) and, at tensor scale, inside every real training library.

Who reads and who writes — this week's ledger:

| Method | Stage | State |
|---|---|---|
| `add`, `multiply`, `subtract`, `rectify`, `exponential`, `naturalLog` | Forecast / Grade | **Create** one new receipt each; read ingredient numbers; change nothing that exists |
| `topologicalOrder` | Measure, step 1 | Reads the graph; creates a list; changes nothing |
| `backward` | Measure, step 2 | **Writes `gradient`** on every receipt in the graph — always `+=` |
| `zeroGradient` | Reset | Writes `gradient` back to $0.0$ |
| `setNumber` | Nudge | The only writer of `number` — and only on a leaf |

## <font color="#388bfd">The Practice Graph</font>

Everything on Day 1 lands on one graph small enough for a pencil, built to rhyme with the real network — a weight, an input, a bias, a gate:

$$z = w \cdot x + b \qquad a = \max(0, z) \qquad L = a \cdot a$$

with $w = 2$, $x = 3$, $b = -5$. Forward: product $6$, $z = 1$, $a = 1$, $L = 1$. The audit, receipt by receipt — this table's format is the **trace artifact** you will produce for graphs of your own:

| Receipt | How it was made | Forward number | Local derivatives | Accumulated blame |
|---|---|---:|---|---:|
| $L$ | $a \cdot a$ | $1$ | $1$ for $a$, $1$ for $a$ — the other ingredient, twice | $1$ (the seed) |
| $a$ | $\max(0, z)$ | $1$ | $1$ for $z$ (awake) | $1 + 1 = 2$ — two envelopes from $L$ |
| $z$ | product $+\, b$ | $1$ | $1$, $1$ | $2$ |
| product | $w \cdot x$ | $6$ | $3$ for $w$, $2$ for $x$ | $2$ |
| $b$ | leaf | $-5$ | — | $2$ |
| $w$ | leaf | $2$ | — | $2 \cdot 3 = 6$ |
| $x$ | leaf | $3$ | — | $2 \cdot 2 = 4$ |

Read the $a$ row twice — it is the chapter's punchline in miniature. $a$ is used twice by $L$, so it receives two deliveries, and they add: accumulation, exactly as promised.

Now the variant that rhymes with Chapter 5's silenced units: set $b = -7$. Forward: $z = -1$, the gate closes, $a = 0$, $L = 0$. The audit: blame arrives at the gate and meets sensitivity $0$ — every parcel is returned to sender. $w$, $x$, and $b$ all end with blame exactly $0.0$. **A silenced unit takes no blame**, for the same reason it contributed nothing forward.

## <font color="#388bfd">The Audit Order</font>

One rule keeps the audit honest: **a receipt may be graded only after every receipt that used it has reported.** The practice graph shows why — $a$'s blame ($2$) had to be complete before $z$ could be graded, because $z$'s blame is built from $a$'s. Grade $z$ first and you would hand it half an envelope. You met this rule's mirror image in Chapter 5: a neuron may only recompute after every neuron it reads from is up to date. This is the general version, and it has a name — **topological order**: every `Value` listed after all of its ingredients. The audit then walks that list in *reverse*, dishes before ingredients.

Building the order is a classic algorithm (TODO 6): depth-first — to place a receipt, first place its ingredients, then append the receipt. A visited set keeps a receipt that feeds two dishes from being listed twice. For the first trace, `[a, b, product, L]` and `[b, a, product, L]` are both valid; the *property* is what matters, not the tie-breaks.

## <font color="#388bfd">backward, the Whole Method</font>

With ordered receipts, the audit is five lines (TODO 7):

```java
// seed: the loss is perfectly sensitive to itself
this.gradient = 1.0;
// walk newest-to-oldest; at each receipt, hand blame through every door
for each receipt, in reverse topological order:
    for each parent of that receipt:
        parent.gradient += localDerivative * receipt.gradient;
```

That `+=` line is the chain rule and gradient accumulation fused: multiply along the path, add across paths. It is also the week's most load-bearing character — write `=` instead and a card used twice loses its first envelope silently.

> **Warning:** one audit per graph. `backward` assumes the graph's gradients start at zero, which fresh receipts guarantee. Audit the same graph twice and interior receipts still holding blame get compounded — on Set B's diamond graph, a second `backward` turns $\partial L / \partial a = 21$ into $63$, not $42$. Each training step builds a fresh graph; only the parameters persist, and the network's Reset clears them between steps.

### <font color="#79c0ff">Check yourself — Set B</font>

1. Rerun the first trace with $a = 4$, $b = 2$: forward values of $c$ and $L$, and both leaf blames.
2. The practice graph with $x = 1$ (keep $w = 2$, $b = -5$): trace forward, then explain what the audit delivers to $w$, $x$, and $b$, and why.
3. The diamond graph: $s = a + b$, $\,p = a \cdot b$, $\,L = s \cdot p$, with $a = 2$, $b = 3$. Forward all four values, then audit by hand — show the two-path addition for both $a$ and $b$.
4. Call `backward` a second time on the diamond's graph, with no zeroing anywhere. What does $a$'s blame read now, and which single character of the audit loop made it happen?

**Day 1 homework:** [Assignment](ASSIGNMENT.md) Part 1 — implement the engine (TODOs 1–7), and bring problem sets A and B worked on paper.

---

## <font color="#388bfd">Vocabulary — Day 2</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Full-batch gradient descent | Every flashcard graded into one averaged update, every step. | The whole deck, every step |
| Stochastic gradient descent | Chapter 4's word, unchanged: random handfuls instead of the whole deck. | A shuffled sample per step |
| Constant leaf | A number wrapped as a leaf whose blame is deliberately ignored. | Bookkeeping stapled to the trail — not an ingredient |
| Gradient check | Chapter 4's referee, unchanged: wiggle versus formula, to six decimals. | The wiggle experiment, hired as referee |
| Memorization | Driving loss toward zero on data that has no mixture to be honest about. | The drumbeat, learned exactly |
| Catastrophic forgetting | New training overwriting the shared machinery old skills lived in. | The pizzeria, lost to the drumbeat |

## <font color="#388bfd">Day 2 — The Machine Rebuilt, Audited, and Finally Trained</font>

## <font color="#388bfd">The Network, Rebuilt from Receipts</font>

The starter's `TrainableFeatureNetwork` is Chapter 5's architecture with one change of material: all 49 numbers are now leaf `Value`s. Same binder, same layers, same gate — but every forecast now leaves a paper trail from the loss back into the binder. The contrast is worth a table:

| | Chapter 5 | This chapter |
|---|---|---|
| The 49 numbers | `double`s, frozen | Leaf `Value`s, moved by every step |
| Fetched cards | **Clones** — so nothing could touch the binder | **The real cards** — blame must reach the binder |
| Logits | Computed, used, forgotten | Computed, and remembered by the trail |
| The loss | A verdict with no way back | The root of the audit |

The clone reversal deserves a beat. Chapter 5's look-up cloned each fetched card as a *protection*: the forward pass must not alter the model. This week the joined row holds the card `Value`s **themselves** — because if it held copies, `backward` would deliver blame to the copies, and the real cards would never learn. Protection has not been abandoned; it moved. Forward evaluation still writes nothing (the Tester still proves a hundred forecasts move no parameter) — receipts are *created*, parameters are only *read*. And when the same token sits at two context positions, the same card `Value` sits at two row positions — one mailbox, two future envelopes.

## <font color="#388bfd">The Loss, Written for the Audit</font>

Chapter 4's grade was $-\ln(p_{\text{target}})$, computed through softmax — and softmax divides, an operation your engine does not have. Algebra dissolves the problem. Start from what the grade *is* and push the logarithm through:

$$L = -\ln\!\left(\frac{e^{z_t - m}}{\sum_j e^{z_j - m}}\right) = \ln\!\Big(\sum_j e^{z_j - m}\Big) - (z_t - m)$$

| Symbol | What it is |
|---|---|
| $z_j$ | token $j$'s unrestricted score — a `Value` with a paper trail |
| $z_t$ | the score belonging to the true next token |
| $m$ | the largest score, subtracted from all of them — Chapter 4's overflow shield, which provably changes no share |
| $\ln \sum e^{(\cdot)}$ | the natural logarithm of the summed exponentials — built from `exponential`, `add`, `naturalLog` |

The division is gone: the grade is a log of a sum of exponentials, minus the target's shifted score — every piece an operation you built on Day 1. One bookkeeping subtlety (TODO 10): $m$ is found with a plain `double` loop and wrapped as a **constant leaf**. It is a shield, not an ingredient — Chapter 4 proved the shift changes nothing, so its blame is simply never read. The referee will confirm the gradients come out exactly right anyway.

Run it on the featured flashcard — context `pineapple pizza pineapple`, truth `pizza`. The receipts reproduce Chapter 5 to the last digit: scores $[1.5504, -1.6160, -1.1503]$, loss $0.1037$. Same numbers, one difference: these remember where they came from.

## <font color="#388bfd">One Backward Through the Whole Machine</font>

Now audit that flashcard's loss and read the gradients layer by layer — every number below is machine-verified, and the Tester reproduces each one.

**At the scores.** The three score receipts read:

```text
forecast (from Chapter 5):   [ 0.9015,  0.0380,  0.0605 ]     truth: pizza
score blame after backward:  [-0.0985,  0.0380,  0.0605 ]
```

Look hard at that second row: it is the forecast **minus one-hot**. Chapter 4's "almost insultingly simple" shortcut — the formula you took on referee'd faith — just *fell out* of six local rules and a reverse walk. It was never a special trick: it is what the chain rule computes for softmax-plus-cross-entropy. Chapter 4's machine needed only this first step of backpropagation, because its logits *were* its parameters. This machine keeps going.

**Through the output layer.** Each gated hidden value collects blame from all three scores, scaled by its output weights — for unit 3: $(-0.0985)(0.53) + (0.0380)(-0.84) + (0.0605)(-0.18) = -0.0950$. Each output weight's blame is one product — the weight from unit 3 into pizza's score: $(-0.0985)(1.8724) = -0.1845$. And each output bias's blame *is* its score's blame (the bias enters through an add, sensitivity 1).

```text
gated hidden blame:   [ 0.0321,  0.1271, -0.0448, -0.0950 ]
```

**Through the gate.** Units 0 and 1 were silenced on this forecast ($z < 0$). They *received* blame — $0.0321$ and $0.1271$ — and the gate returns it to sender:

```text
hidden-sum blame:     [ 0.0,     0.0,    -0.0448, -0.0950 ]
```

**Through the hidden layer, into the joined row.** Each joined slot collects from the awake units only — slot 0: $(-0.0448)(-0.48) + (-0.0950)(0.26) = -0.0032$; slot 4: $(-0.0448)(0.39) + (-0.0950)(0.41) = -0.0564$.

```text
joined-row blame:     [-0.0032, -0.0014,  0.0594, -0.1120, -0.0564, -0.0430 ]
                        └─ pineapple ─┘   └── pizza ───┘   └─ pineapple ─┘
```

**Into the binder — the cliffhanger resolves.** Chapter 5 left you with a puzzle: how is credit split when a card is used twice in the same row? The answer costs nothing: pineapple's card `Value` sits at *both* positions, so `+=` delivers both envelopes to the same mailbox:

```text
pineapple slot 0:   -0.0032  +  -0.0564   =  -0.0597
pineapple slot 1:   -0.0014  +  -0.0430   =  -0.0444
pizza's card:       [ 0.0594, -0.1120 ]
pepperoni's card:   [ 0.0,     0.0    ]      not consulted -> no blame
```

**The referee confirms it.** Chapter 4's wiggle experiment, too slow to train with, is the perfect judge: nudge pineapple's slot 0 by $\pm 10^{-5}$, recompute the loss both ways, form the finite difference:

```text
wiggle says:    -0.059654
backward says:  -0.059654       agreement to six decimal places
```

### <font color="#79c0ff">Check yourself — Set C</font>

The whole audit by hand, on Chapter 5's Set C miniature (vocabulary of 2; one-slot cards $[2]$ and $[-1]$; context length 2; one rectified hidden unit, weights $[0.5, 1]$, bias $0$; output units $[1]$ and $[-1]$, biases $0$). You traced its forward pass in Chapter 5: joined row $[-1, 2]$, hidden $z = 1.5$, gated $1.5$, forecast $[0.9526, 0.0474]$. The history shows token 1 next.

1. The score blames, straight from forecast minus one-hot.
2. The blame on the gated hidden value, and what the gate does with it at $z = 1.5$.
3. Both hidden-weight blames and the hidden-bias blame.
4. Both card blames — and, had the context been $[1, 1]$ instead of $[1, 0]$, what card 1's total would have been.

## <font color="#388bfd">The Nudge Returns</font>

The audit fills every parameter's `gradient`; the nudge is Chapter 4's, verbatim — stride downhill:

```text
pineapple slot 0, blamed -0.0597 by that one flashcard, stride 0.5:
    0.38 - 0.5 * (-0.0597)  =  0.4098        raised, because raising it lowers the loss
```

One flashcard should not steer alone, and Chapter 4's bucket taught you the fix: grade many, average, step once. This week the bucket dissolves into the graph itself (TODO 11): grade **every** flashcard, chain the 119 losses with `add`, multiply by $\tfrac{1}{119}$ — one receipt for the whole history's average loss. Audit that single receipt and every parameter receives its averaged blame in one pass. Then one training step is the full lifecycle in order (TODO 13):

```text
zeroGradients()                                Reset    - wipe all 49 mailboxes
averageLoss = averageLossValue(training)       Forecast
                                               + Grade  - one graph, 119 flashcards
averageLoss.backward()                         Measure  - one audit, all 49 blames
for each parameter:                            Nudge    - one stride downhill
    setNumber(number - learningRate * gradient)
```

Because every step grades the whole deck, this is **full-batch** gradient descent — Chapter 4's *stochastic* version drew random handfuls because its deck-of-decks was conceptually huge; this deck is 119 cards, so you can afford the whole thing, and determinism comes free.

## <font color="#388bfd">The Training Run</font>

Resume from the frozen weights — the exact place the offline run stopped — at Chapter 4's stride, $0.5$. The first three steps: $0.3957 \rightarrow 0.3754 \rightarrow 0.3621 \rightarrow 0.3531$. Then the trace, reported every ten steps (`java Trainer` prints exactly this):

```text
step,training loss,validation loss
0,0.3957,0.4013
10,0.3301,0.3345
20,0.3233,0.3275
30,0.3210,0.3252
40,0.3200,0.3241
50,0.3194,0.3235
60,0.3190,0.3231
70,0.3187,0.3229
80,0.3185,0.3227
90,0.3184,0.3225
100,0.3183,0.3224
110,0.3182,0.3223
120,0.3181,0.3222
```

Savor step 10: $0.3301$ — one ten-thousandth *above* the table's $0.3300$. The very next step crosses, at $0.3289$. The gap Chapter 5 could only stare at closes in eleven steps of the loop you built, and the leaderboard resolves:

```text
uniform / nearly empty anything:   1.0986  = ln 3
Chapter 5's frozen network:        0.3957 training,  0.4013 validation
Chapter 4's trained table:         0.3300 training,  0.3311 validation
this network, 120 steps later:     0.3181 training,  0.3222 validation
the data's own floor:              about 0.3174
```

Both of Chapter 5's honest readings paid off. The gap above the table really was unfinished training — you finished it. And the floor really belongs to the data, not the machine: the network now sits essentially *on* it, tying what a perfect context-3 counter could do on this history. The last $0.0007$ is not worth chasing — the mixture after `pizza` is genuinely 40-versus-20, and no machine can outpredict honest uncertainty.

The training also moved the binder, and the punchlines survived: after 120 steps the after-`pizza` forecast is $[0.0004, 0.6608, 0.3388]$ — hugging the counted $[0, 0.667, 0.333]$ tighter than the frozen model's $[0.0366, 0.6428, 0.3206]$, with `pizza pizza` driven near zero but never *to* zero. The cousins are still cousins: topping cards $0.49$ apart while pizza's card sits $2.28$ and $1.86$ away.

## <font color="#388bfd">Punchline: You Reproduce the Oracle</font>

Chapter 5's weights "arrived pre-trained — gradient descent was run on this same order history ahead of time." That sentence has been load-bearing for a week, and you can now delete the mystery from it. The fixtures include the **fresh start**: the exact 49 numbers the offline run began from (printed as literals — they were drawn in Python, whose random number generator differs from Java's). From there:

```text
fresh start:                  training loss 1.3626
10 full-batch steps at 0.5:   training loss 0.3958
round every number to 2dp:    Chapter 5's frozen fixture, exactly
largest gap to any frozen number: 0.004952   — inside the 0.005 rounding bound
```

There was never an oracle. There was this loop, run ten times, a week before you built it. Note the fresh start's loss: $1.3626$, *worse* than the empty network's $1.0986$ anchor — random weights at this scale make confidently wrong guesses, and confidence costs more than ignorance. Ten steps fixed that too.

## <font color="#388bfd">Punchline: The Drumbeat</font>

Nothing in the engine knows about pizza. Hand the trained machinery a different world — the drumbeat history `0, 1, 2, 0, 1, 2, ...` — and retrain the frozen network on it:

```text
drumbeat loss before:            2.0522
after 50 steps at stride 0.5:    0.0029      forecast after [0,1,2]: 99.7% token 0
pizzeria training loss, now:     3.7264
```

Two lessons in three lines. First, the drumbeat has **no mixture** — every context has exactly one continuation — so its floor is zero, and gradient descent happily memorizes it to near-certainty. The 0.3174 floor was never the machine's limit; it was the pizzeria's. Second, the pizzeria is *gone*: the same shared machinery that let every flashcard teach every forecast means new training overwrites old skill. The standard name is **catastrophic forgetting**, and it is the dark twin of the sharing Chapter 5 celebrated. You will meet it again at archive scale.

### <font color="#79c0ff">Check yourself — Set D</font>

1. A parameter holds $0.38$ and the audit assigns it blame $-0.0597$. Where does one stride of length $0.5$ move it, and in which direction — and why is the sign right?
2. You forget the Reset. Monday's step audits a fresh graph and pineapple's slot 0 reads $-0.0597$; Tuesday's step builds another fresh graph and audits it. What does the mailbox read before Tuesday's nudge, and what slope does that nudge actually stride down?
3. Chapter 4's `train` took a seed. This chapter's takes none. What exactly removed the randomness?
4. Read the trace: at step 10 the training loss is $0.3301$. Has the network beaten the table? What happens one step later?

## <font color="#388bfd">What Is Read, What Is Written</font>

The week's discipline in one table — the receipts' fates, and who may touch what:

| Thing | Created when | Written by | Fate |
|---|---|---|---|
| The 49 parameter `Value`s | Once, at construction | `backward` (`gradient`, `+=`), `zeroGradients` (`gradient`, to 0), the Nudge (`number`) | **Persist** — the only survivors between steps |
| Scratch receipts (scores, exponentials, sums, the loss) | Fresh, every forecast and every step | `backward` writes their `gradient` during the audit | Created, audited at most once, discarded |
| The constant leaves (`maxShift`, $\tfrac{1}{119}$) | Fresh, inside the loss | `backward` writes blame they never spend | Bookkeeping — discarded with the graph |
| Forward `number`s of computed receipts | At creation, exactly once | Nobody — `setNumber` refuses non-leaves | The audit reads the forward pass; it never redoes it |

## <font color="#388bfd">What You Are Given</font>

The starter code is in [starter/](starter/) — five files. Three contain TODOs; the rest are complete:

| File | Status | Role |
|---|---|---|
| [Value.java](starter/Value.java) | **TODO 1–7** | The receipt: six operations, the audit order, and `backward` (`add` is provided as the worked example) |
| [TrainableFeatureNetwork.java](starter/TrainableFeatureNetwork.java) | **TODO 8–12** | Chapter 5's pipeline rebuilt from receipts, the auditable loss, and the Reset |
| [Trainer.java](starter/Trainer.java) | **TODO 13–14** | One full-batch step, the training loop, and the provided experiment bench |
| [AutogradFixtures.java](starter/AutogradFixtures.java) | Complete | The frozen start, the fresh offline start, both histories, and the drumbeat |
| [Tester.java](starter/Tester.java) | Complete | Reproduces every worked number on this page, runs the required tests, prints the punchlines |

Implement the TODOs in order, rerunning `Tester` after each — unimplemented stages report as `TODO`, not `FAIL`:

1. `multiply` — the crossover rule: each ingredient's sensitivity is the other ingredient (Day 1)
2. `subtract` — addition's twin, one sign flipped (Day 1)
3. `rectify` — the gate's blame policy: all of it, or none of it (Day 1)
4. `exponential` — the receipt whose result is its own sensitivity (Day 1)
5. `naturalLog` — sensitivity $1/x$, and a loud refusal below zero (Day 1)
6. `topologicalOrder` — every ingredient before its dish, depth-first (Day 1)
7. `backward` — seed 1, walk in reverse, `+=` through every door (Day 1)
8. `weighAndAddValues` — Chapter 5's layer loop, third notation (Day 2)
9. `unrestrictedScoreValues` — fetch (no clones!), join, mix, gate, score (Day 2)
10. `lossValueFromScores` — the grade as $\ln \sum e - $ target, ready for audit (Day 2)
11. `averageLossValue` — one graph for the whole history; the bucket, dissolved (Day 2)
12. `zeroGradients` — Reset: wipe all 49 mailboxes (Day 2)
13. `gradientDescentStep` — the full lifecycle: Reset, Grade, Measure, Nudge (Day 2)
14. the loop in `train` — learning is nothing else (Day 2)

## <font color="#388bfd">Evidence Checkpoint</font>

Six observations your finished code must produce:

1. **Every hand trace reproduces.** First trace $4 / 2 / 1$; practice graph $6 / 4 / 2$ with the silenced variant all zeros; diamond $21 / 16$.
2. **The referee is satisfied twice.** The composite graph's three audits match the wiggle to $10^{-6}$, and three network parameters match on the featured flashcard — worst gap printed near $10^{-11}$.
3. **The shortcut is rediscovered.** Score blames $[-0.0985, 0.0380, 0.0605]$, equal to forecast minus one-hot to $10^{-9}$.
4. **Blame reaches the binder correctly.** Pineapple $[-0.0597, -0.0444]$ — two envelopes, added; pepperoni exactly $[0, 0]$; one full-batch step moves $0.3957 \rightarrow 0.3754$.
5. **The gap closes.** The 120-step trace lands at $0.3181 / 0.3222$ — past the table's $0.3300 / 0.3311$ on both histories, at the $0.3174$ floor.
6. **The oracle and the drumbeat.** Ten steps from the fresh start ($1.3626$) land at $0.3958$, within $0.005$ of every frozen number; fifty drumbeat steps reach $0.0029$ while the pizzeria decays to $3.7264$.

## <font color="#388bfd">Required Tests</font>

`Tester` covers all of these — confirm every one reports `PASS`:

- Each operation mints a new receipt with the right number, touches no ingredient, and assigns no blame at creation; `naturalLog` refuses zero and negatives; the gate is closed at exactly zero.
- A computed receipt refuses `setNumber` — only leaves may be nudged.
- `topologicalOrder` lists every receipt exactly once, ingredients always first, the audited receipt last — on the first trace and on the diamond.
- `backward` reproduces the first trace ($4/2/1$, seed exactly $1$), the reused leaf ($a \cdot a \rightarrow 6$), the practice graph ($6/4/2$), the silenced variant (all exactly $0.0$), and the diamond ($21/16$) — and moves no forward number.
- A second audit of the same graph corrupts ($21 \rightarrow 63$); a second *fresh* graph without Reset accumulates ($-0.0597 \rightarrow -0.1193$); Reset restores.
- The wiggle referee agrees with the audit to $10^{-6}$ on the composite graph and on three network parameters.
- The rebuilt pipeline reproduces Chapter 5's every number: scores, forecast, both losses, the $0.3957 / 0.4013$ report card — and a hundred forecasts move no parameter.
- Score blames equal forecast minus one-hot; the binder receives $[-0.0597, -0.0444]$ / $[0.0594, -0.1120]$ / exactly zero.
- One step reports the loss it stood on ($0.3957$) and lands at $0.3754 / 0.3806$; thirty steps land at $0.3210 / 0.3252$, past the table.
- Ten steps from the fresh start land within rounding of every frozen number; the drumbeat memorizes below $0.005$ while the pizzeria is forgotten; short contexts, bad tokens, and flashcard-less histories are refused.

## <font color="#388bfd">Answer Key</font>

**Set A**

1. Result $-10$; sensitivity $5$ for $u$ and $-2$ for $v$ — each ingredient's sensitivity is the *other* ingredient.
2. $1$ at $z = 3$; $0$ at $z = -3$; $0$ at exactly $z = 0$ — this course's gate is closed at zero.
3. Result $-3$; sensitivities $1$ for $u$, $-1$ for $v$. Blame $-2$ delivers $-2 \cdot 1 = -2$ to $u$ and $-2 \cdot (-1) = +2$ to $v$.
4. $e^0 = 1$ with sensitivity $1$ (the result itself); $\ln 2 = 0.6931$ with sensitivity $1/2 = 0.5$.

**Set B**

1. $c = 8$, $L = 12$; $\partial L/\partial a = b + 1 = 3$ (path through $c$ contributes $2$, direct path $1$); $\partial L/\partial b = a = 4$.
2. Product $2$, $z = -3$, gate closed: $a = 0$, $L = 0$. The audit reaches the gate, meets sensitivity $0$, and delivers exactly $0.0$ to $w$, $x$, and $b$ — a silenced unit takes no blame.
3. Forward: $s = 5$, $p = 6$, $L = 30$. Blames: $\partial L/\partial s = 6$, $\partial L/\partial p = 5$; then $a$ collects $6 \cdot 1 + 5 \cdot 3 = 21$ and $b$ collects $6 \cdot 1 + 5 \cdot 2 = 16$.
4. $63$. The `+=` — interior receipts still held their first-audit blame ($6$ and $5$), so the second audit compounded them instead of starting clean. One audit per graph.

**Set C**

1. Forecast minus one-hot with truth token 1: $[0.9526, -0.9526]$.
2. $0.9526 \cdot 1 + (-0.9526) \cdot (-1) = 1.9051$; the gate is awake at $z = 1.5$, so all $1.9051$ passes through.
3. Joined row was $[-1, 2]$: slot 0 blame $1.9051 \cdot (-1) = -1.9051$; slot 1 blame $1.9051 \cdot 2 = 3.8103$; bias blame $1.9051$.
4. Card 1 (position 0): $1.9051 \cdot 0.5 = 0.9526$. Card 0 (position 1): $1.9051 \cdot 1 = 1.9051$. Had the context been $[1, 1]$, card 1's mailbox would collect both envelopes: $0.9526 + 1.9051 = 2.8577$.

**Set D**

1. $0.38 - 0.5 \cdot (-0.0597) = 0.4098$ — raised. Negative blame means the loss *falls* as the parameter rises, and the nudge subtracts the gradient, so it strides toward lower loss.
2. $-0.0597 + (-0.0597) = -0.1193$ — Monday's blame is still in the mailbox. Tuesday's nudge strides down a two-day phantom slope that belongs to no single step.
3. Full batch. Chapter 4 drew random flashcards, so the draw order needed a seed; this chapter grades all 119 flashcards every step — there is nothing left to draw.
4. Not yet — $0.3301$ is one ten-thousandth above $0.3300$. Step 11 crosses, at $0.3289$.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** backpropagation is not a second, smarter intelligence inspecting the network. It is two small rules — multiply along a path, add across paths — applied by bookkeeping to receipts the forward pass already wrote.

> **Misconception:** a gradient is not the new value for a parameter. It is a slope: which direction the loss responds, and how steeply. The stride length is a separate decision — Chapter 4's learning-rate lesson survives intact.

More traps worth defusing now:

| If you catch yourself thinking… | Remember |
|---|---|
| "`backward` re-runs the pipeline in reverse." | It never recomputes anything. It reads receipts written during the forward pass; every forward `number` is untouched — the Tester checks. |
| "Blame $0$ means the parameter is useless." | It means the loss is locally flat with respect to it *for this graph*. Pepperoni's card drew zero because this flashcard never consulted it; the next flashcard may blame it plenty. |
| "`=` instead of `+=` is close enough." | A card used twice loses an envelope — one delivery erases the other, silently. The practice graph's $a$ row and pineapple's $-0.0597$ both exist to catch exactly this. |
| "Audit twice for double confirmation." | Same graph, second audit: interior blame compounds — the diamond's $21$ becomes $63$. One audit per graph; fresh graph per step. |
| "The `maxShift` needs blame too." | It is a shield, not an ingredient. Chapter 4 proved the shift changes no share; wrapping it as a constant leaf whose blame is never read leaves every real gradient exact — the referee confirms. |
| "Look-up should clone, like Chapter 5." | Then blame would land on the copies and the binder would never learn. The discipline moved: snapshots for printing, real `Value`s for computing. |
| "Training should feel random, like Chapter 4." | Full batch grades the same 119 flashcards every step. No seed, no draws — the trace reproduces digit for digit on any machine. |
| "$0.3181$ means undertrained — keep pushing toward zero." | The floor $0.3174$ belongs to the data: the mixture after `pizza` is honestly 40-versus-20. Only a mixture-free history — the drumbeat — can be driven toward zero. |
| "The drumbeat run improved the machine." | It overwrote it: the pizzeria's loss went $0.3957 \rightarrow 3.7264$. Shared machinery means new training moves *everything* — sharing's dark twin, catastrophic forgetting. |

## <font color="#388bfd">Stretch Goals</font>

1. **Hyperbolic tangent** — add `tanh` with local derivative $1 - \tanh^2(x)$, and referee it with the wiggle.
2. **Sigmoid** — add $\sigma(x) = 1/(1 + e^{-x})$ with local derivative $\sigma(1 - \sigma)$; note that, like `exponential`, its result feeds its own sensitivity.
3. **Divide and power** — add the two operations this chapter dodged, then rewrite the loss the Chapter 4 way ($-\ln$ of an explicit softmax share) and show both forms produce identical gradients.
4. **Graph exporter** — walk `topologicalOrder` and print the featured flashcard's graph in Graphviz DOT format: every receipt, every door, every sensitivity.
5. **Receipt counter** — instrument `Value` creation and count receipts per full-batch step. Estimate the count for the final course model's roughly 34,000 parameters, and feel exactly why Chapter 7 exists.
6. **The learning-rate bench, network edition** — rerun Chapter 4's experiment (strides $0.01$, $0.5$, $20$) on this network and describe what each trace does.
7. **Race the oracle from your own start** — invent your own 49 starting numbers, train, and compare your path to the fresh start's. Does where you begin change where you end?
8. **Find the stumble** — train well past 120 steps, reporting every 10. The stride tuned for the start eventually becomes slightly too long near the floor; find a stumble in your trace and explain it with Chapter 4's learning-rate vocabulary.

---

The model now learns — genuinely, end to end, from its own mistakes. But look at what one training step costs: every add, every multiply, every gate mints a Java object, and a single full-batch step writes tens of thousands of receipts that a garbage collector must then sweep up. On the pizzeria this is invisible; on an archive of millions of token positions it is fatal. The glass-box engine is the correctness reference now — the next chapter performs the same mathematics on flat primitive arrays, with explicit backward formulas standing in for the receipts, and proves the fast engine right by checking it against this one.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you write the receipt for a multiply — result, ingredients, both sensitivities — and explain the crossover rule?
- [ ] Can you state what a topological order guarantees, and why the audit must walk it in reverse?
- [ ] Can you explain why the loss's own gradient seeds to exactly 1, and why blame is delivered with `+=` rather than `=`?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you produce the full trace table for the practice graph — forward numbers, local derivatives, accumulated blame — landing on $6 / 4 / 2$?
- [ ] Can you hand-audit the Set C miniature from score blames to card blames, starting from forecast minus one-hot?
- [ ] Can you explain the two-envelope resolution: why a card used twice in one context receives added blame, and why an unconsulted card receives exactly zero?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you derive the loss's $\ln \sum e^{z_j - m} - (z_t - m)$ form from $-\ln(p_{\text{target}})$, and justify treating $m$ as a constant leaf?
- [ ] Can you run the training experiments and read the leaderboard: what closed the gap to the table, and why the floor stops everyone at $0.3174$?
- [ ] Can you argue the cost case: why the wiggle needs two evaluations per parameter while one backward pass blames every parameter at once — and verify both agree to six decimals?

---

[Assignment](ASSIGNMENT.md)

← [From Exact Symbols to Features](../ObjectNetwork/) — Next: [From Glass Box to Engine](../DenseEngine/)
