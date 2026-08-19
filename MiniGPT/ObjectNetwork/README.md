<div align="center">

# From Exact Symbols to Features
*<font color="#8b949e">Token embeddings and an object-oriented neural network — forward pass only</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The trainable bigram table treats every token as a separate universe. If "mushroom" and "olive" tend to appear in similar sentences throughout the archive, the table has no direct way to share that discovery. The next machine will describe each token using a small collection of learned numerical features and combine those features through a network of connections.

## <font color="#388bfd">Question to Carry</font>

> **How can different tokens share useful predictive features?**

## <font color="#388bfd">Where This Chapter Sits in the Loop</font>

Chapter 4 gave every model for the rest of the course its life cycle: **forecast, grade, measure the slope, nudge** — repeated thousands of times. Before touching anything new, place this chapter on that map:

| Beat of the loop | Chapter 4 — the table | This chapter — the network |
|---|---|---|
| 1. Forecast | Read the current token's row, softmax it | **Rebuilt this week**: a six-step pipeline through shared features |
| 2. Grade | $-\ln$ of the probability given the truth | Identical — reused, unchanged |
| 3. Measure the slope | `p` minus one-hot, poured into the bucket | **Switched off** — no formula yet reaches inside this machine |
| 4. Nudge | One stride downhill | **Switched off** — every number is frozen |

This week rebuilds beat 1 and only beat 1. The grade still works — the loss never cared what machine made the forecast. But the table's slope shortcut, `p` minus one-hot, only knew how to blame *one row of logits it could see directly*. This machine computes its scores through internal machinery, and no tool you own can yet trace blame through it. So the weights you use this week were trained for you, offline, and **nothing in this chapter changes a single number**. That constraint is not a limitation to apologize for — it is the cliffhanger the next chapter resolves.

One more promise about method: you will meet every piece **as objects first** — a `Neuron` you can point at, a `Connection` you can print — and then discover that a whole layer of objects is one loop over arrays. The object form is a bridge for your intuition, not the final machinery.

The chapter is two class periods. Each day ends with homework:

| Day | In class | Homework |
|---|---|---|
| 1 | One unit: weigh and add · the gate · the practice network traced by hand · the same network as objects · a layer of objects becomes one loop · the collapse proof | [Assignment](ASSIGNMENT.md) Part 1 — TODOs 1–4 plus problem sets A and B on paper |
| 2 | The binder of learned stat cards · the life of one forecast, six steps with real numbers · what is read and what is written · the punchlines: cousins, the rediscovered mixture, the parameter argument · the gap this chapter cannot close | [Assignment](ASSIGNMENT.md) Part 2 — TODOs 5–10, the punchline readings, and the concept questions |

## <font color="#388bfd">The Order History Returns</font>

Same tiny world as Chapter 4 — the pizzeria's order history, three-word vocabulary, the same 122-token training history and 42-token validation history, provided in the starter fixtures:

```text
token 0 = pizza      token 1 = pineapple      token 2 = pepperoni

the history reads:  pineapple pizza pineapple pizza pepperoni pizza ...
as tokens:          1, 0, 1, 0, 2, 0, ...
```

Three ground rules for the week:

1. **The forecast now reads three tokens, not one.** Chapter 4's table stood at one token and read one row. This network reads a **fixed context** of the three most recent tokens. A history of $n$ tokens therefore holds $n - 3$ flashcards, not $n - 1$: the training history that gave the table 121 flashcards gives this network 119.
2. **The weights are provided, trained, and frozen.** The network's 49 numbers arrive pre-trained: gradient descent was run on this same order history ahead of time, and the results were rounded to two decimals and printed into the fixtures file. The tools that training required do not exist in this course yet — Chapter 6 builds them. This week, you are given the trained numbers, not the training.
3. **Nothing is written this week.** Chapter 4 alternated reads and writes: accumulate, step, reset. This chapter is pure reading. Every forecast creates a few scratch rows, uses them, and throws them away; the model itself comes back bit-for-bit identical, and the Tester checks that a hundred forecasts change nothing.

## <font color="#388bfd">Vocabulary — Day 1</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Neuron, or unit | A component that combines its inputs into one number. Only loosely inspired by biology. | A tiny scale that weighs its inputs and reports one total |
| Connection | A weighted link from one unit to another. | A labeled wire: where from, and how loud |
| Weight | Chapter 4's word, unchanged: a parameter that scales information. | A volume knob on one wire |
| Bias | A trainable constant added to a unit's total. | The unit's resting level before any input arrives |
| Weighted sum | Inputs multiplied by their weights and totaled, plus the bias. | Weigh every input, add it all up |
| Activation function | A function applied to the weighted sum before it is passed on. | A gate on the unit's output |
| Rectified Linear Unit (ReLU) | The gate $\max(0, z)$: negatives are silenced to zero. Also the name for a unit that wears this gate. | A one-way valve — positive flows, negative stops |
| Linear unit | A unit with no gate: it reports its weighted sum unchanged. | The scale's reading, passed along as-is |
| Nonlinearity | Any gate that keeps stacked layers from collapsing into one. | The bend in the pipe |
| Layer | Units that read the same inputs at the same stage. | One row of scales, weighing in parallel |
| Hidden layer | A layer between input and output — visible to you, internal to the machine. | The mixing chamber |
| Linear transformation | What weigh-and-add computes: a weighted combination of inputs. | A recipe of proportions |

---

## <font color="#388bfd">Day 1 — The Machine, One Neuron at a Time</font>

## <font color="#388bfd">One Unit: Weigh and Add</font>

The atom of every neural network is one small calculation. A unit has several incoming wires, each with a **weight**; it multiplies each arriving value by its wire's weight, totals the products, and adds its own **bias**:

$$z = b + \sum_{i} w_i \, x_i$$

| Symbol | What it is |
|---|---|
| $z$ | the unit's **weighted sum** — the one number this unit produces before its gate |
| $b$ | the unit's **bias** — a constant the unit owns; its output when every input is zero |
| $i$ | which input slot, counting $0, 1, 2, \ldots$ up to the number of wires minus one |
| $w_i$ | the **weight** on wire $i$ — how loudly input $i$ counts, and in which direction |
| $x_i$ | the value arriving on wire $i$ — the source unit's current output |

Why the bias? Without it, every unit would be forced to output zero whenever its inputs are zero. The bias sets a resting level — and once the gate arrives below, it also decides how hard the inputs must push before the unit wakes up.

## <font color="#388bfd">The Gate</font>

The weighted sum can be any number. Before passing it on, the unit applies a gate. This course's default gate is the **Rectified Linear Unit**, abbreviated **ReLU**:

$$a = \max(0, z)$$

| Symbol | What it is |
|---|---|
| $a$ | the unit's output — what the next layer actually receives |
| $z$ | the weighted sum from the formula above |
| $\max(0, z)$ | whichever is larger: $0$ or $z$ — so negatives become exactly $0$, positives pass unchanged |

The name unpacks piece by piece. *Rectified* is borrowed from electronics, where a rectifier is a one-way valve for current — this gate is a one-way valve for numbers. *Linear* describes the open half: for positive input the gate passes the value through unchanged, a straight line. And *Unit* is because the whole term names more than the gate — a unit that wears this gate is itself called **a Rectified Linear Unit (ReLU)**; this page also says **rectified unit**, which is what the starter code calls it.

Not every unit wears the gate. A unit with no gate at all — one that reports its weighted sum exactly as computed — is a **linear unit**: its output is a plain weighted combination of its inputs, no bend, no silencing, negatives allowed. In this course's networks the division of labor is always the same: units in the middle of the machine wear the gate, and the final output units stay linear — their job is to produce unrestricted scores, Chapter 4's logits, which must be free to go negative; a gate there would clamp half the scale to zero.

A unit whose weighted sum came out negative is **silenced**: it outputs exactly zero, and zero times any downstream weight is still zero, so a silenced unit contributes nothing at all to the next layer. Hold on to a suspicion here — *why silence anything?* Wouldn't keeping the information be better? The answer is just ahead, in [Why the Gate: the Collapse Proof](#why-the-gate-the-collapse-proof) — a proof you do by hand that without the gate, stacking layers is pointless.

## <font color="#388bfd">The Practice Network</font>

So far, one unit: weigh, add, gate. Everything on Day 1 happens on one machine built by wiring a few of them together, small enough to trace with a pencil. It has three rows. At the top, two **inputs** — units with no wires coming in; their values are set from outside. In the middle, two **hidden units** — *hidden* because they are the machine's internal scratch work: nothing outside the machine ever reads them; they exist only to feed the row below. Both are Rectified Linear Units (ReLU) — they wear the gate. At the bottom, two **output units**, whose two numbers are the machine's answer — linear units, no gate, so the answer may be any number. Every weight is an integer:

```text
   inputLeft = 1     inputRight = 2        inputs, set from outside
          \   \       /   /
           \   \     /   /                 every input wired to every hidden unit
        hiddenTop   hiddenBottom           rectified units, biases 1 and -1
          \   \     /   /
           \   \   /   /                   every hidden unit wired to every output
      outputFirst   outputSecond           linear units, biases 0 and 2
```

Eight wires, each with its weight:

| Wire | Weight | | Wire | Weight |
|---|---:|---|---|---:|
| `inputLeft` → `hiddenTop` | 1 | | `hiddenTop` → `outputFirst` | 2 |
| `inputRight` → `hiddenTop` | -2 | | `hiddenBottom` → `outputFirst` | -1 |
| `inputLeft` → `hiddenBottom` | 3 | | `hiddenTop` → `outputSecond` | 1 |
| `inputRight` → `hiddenBottom` | 1 | | `hiddenBottom` → `outputSecond` | 1 |

Trace it, unit by unit, with inputs $1$ and $2$:

```text
hiddenTop:     z = 1 + (1)(1) + (-2)(2) = -2     gate: max(0, -2) = 0    silenced
hiddenBottom:  z = -1 + (3)(1) + (1)(2) =  4     gate: max(0, 4)  = 4    awake

outputFirst:   z = 0 + (2)(0) + (-1)(4) = -4     linear: -4
outputSecond:  z = 2 + (1)(0) + (1)(4)  =  6     linear:  6
```

The machine's answer to input $[1, 2]$ is $[-4, 6]$. Notice what the silenced unit did to the outputs: `hiddenTop`'s wires into both outputs carried exactly nothing.

## <font color="#388bfd">The Same Machine as Objects</font>

The starter code represents this with two classes you can hold in your head — a `Connection` is a labeled wire, and a `Neuron` owns a bias, a gate, a list of incoming connections, and one stored number:

```java
Neuron inputLeft = Neuron.input("inputLeft");
Neuron hiddenTop = Neuron.rectified("hiddenTop", 1.0);
hiddenTop.connectFrom(inputLeft, 1.0);
hiddenTop.connectFrom(inputRight, -2.0);
```

Two methods are yours to write, and the split between them is the day's discipline about **state** — about who reads and who writes:

| Method | What it does | State |
|---|---|---|
| `weighAndAddInputs()` (TODO 1) | Computes $z$: bias plus every source's value times its wire's weight | **Reads only.** Calling it twice changes nothing, not even this neuron's own stored value |
| `recomputeValue()` (TODO 2) | Applies the gate to $z$, then stores the result | **Overwrites** the neuron's stored value — the only computing method that changes anything |

Order matters when you run a whole network of these: a neuron may only recompute after every neuron it reads from is up to date — inputs first, then hidden, then output. (File that rule away; Chapter 6 will give the general version a name.)

### <font color="#79c0ff">Check yourself — Set A</font>

Answers are in the [Answer Key](#answer-key) below. Do these on paper before moving on.

1. A unit has bias $2$ and two wires: weight $0.5$ from a source holding $4$, and weight $-1$ from a source holding $3$. Compute its weighted sum, and its output if it is a rectified unit.
2. Same unit, but the second source now holds $6$. Weighted sum, gated output — and what does this unit now contribute to every unit downstream of it?
3. Without a bias, what would every unit in a network output when all of its inputs are zero — and what does the bias let a rectified unit do about *when* it wakes up?
4. In the practice trace, which method call is the moment `hiddenTop`'s stored value actually changes: `weighAndAddInputs` or `recomputeValue`? What does the other one touch?

## <font color="#388bfd">A Layer of Objects Is One Loop</font>

Look back at the trace: `hiddenTop` and `hiddenBottom` did the *same operation* over the *same inputs* — only their weights and biases differed. So a whole **layer** can be written without objects at all: pack the weights into a table, one row per unit, and run one loop.

```java
// one whole layer: for each unit, weigh every input slot and add the bias
for (int unit = 0; unit < layerWeights.length; unit++) {
    double weightedSum = layerBiases[unit];
    for (int slot = 0; slot < inputRow.length; slot++) {
        weightedSum += layerWeights[unit][slot] * inputRow[slot];
    }
    weightedSums[unit] = weightedSum;
}
```

This is `weighAndAdd` (TODO 3), and its inner loop should look familiar: multiply matching slots, total them — the **dot product** from Chapter 3, now weighing an input row against a unit's weight row instead of two stat cards. The practice network's hidden layer becomes:

```text
weighAndAdd([1, 2], [[1, -2], [3, 1]], [1, -1])  =  [-2, 4]
rectify([-2, 4])                                  =  [ 0, 4]
weighAndAdd([0, 4], [[2, -1], [1, 1]], [0, 2])    =  [-4, 6]
```

Same numbers as the object trace — and not approximately: the Tester builds one hidden unit of the real model both ways and requires agreement to $10^{-9}$. **Objects and arrays are two notations for one machine.** The array form wins on bookkeeping (no object per wire), which is why every real system uses it, and why Chapter 7 will lean on it hard.

`rectify` (TODO 4) is the gate applied to the whole layer: a new array where every negative weighted sum has become exactly $0.0$.

## <font color="#388bfd">Why the Gate: the Collapse Proof</font>

Now settle the suspicion. Remove the gate from the practice network — make the hidden units linear — and chase the algebra. Write the hidden sums as expressions, not numbers:

```text
z_top    = 1 + 1·x0 − 2·x1
z_bottom = −1 + 3·x0 + 1·x1

outputFirst (no gate) = 0 + 2·z_top − 1·z_bottom
                      = 2 + 2·x0 − 4·x1 + 1 − 3·x0 − 1·x1
                      = 3 − 1·x0 − 5·x1
```

Read that last line again: it is a *single* weighted sum — bias $3$, weights $[-1, -5]$. The two-layer gateless machine **is** a one-layer machine wearing a costume. (`outputSecond` collapses the same way, to $2 + 4 \cdot x_0 - 1 \cdot x_1$; check with input $[1,2]$: the gateless network outputs $[-8, 4]$, and so do the collapsed formulas.) Stack fifty gateless layers and the same algebra flattens all fifty.

The gate breaks the collapse, and the practice trace shows how: whether $\max(0, z)$ passes $z$ or silences it *depends on the input*. Different inputs wake different units, so the machine routes different inputs through genuinely different arithmetic. That input-dependent routing is the thing a single weighted sum cannot fake — and you will see it happen in the real model on Day 2.

### <font color="#79c0ff">Check yourself — Set B</font>

1. Re-trace the practice network with inputs $[2, 1]$: hidden sums, gated values, both outputs.
2. Collapse `outputSecond` of the gateless practice network into a single weighted sum of $x_0$ and $x_1$, showing the algebra. What does the result prove about depth without gates?
3. How many multiplications does `weighAndAdd` perform for a layer of 4 units reading 6 slots? Where does each product's weight live in the weight table?
4. A row of `Neuron` objects and one `weighAndAdd` call produce identical numbers. What is actually different between the two forms, and what is identical?

**Day 1 homework:** [Assignment](ASSIGNMENT.md) Part 1 — implement the neuron and the layer machinery (TODOs 1–4), and bring problem sets A and B worked on paper.

---

## <font color="#388bfd">Vocabulary — Day 2</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Representation | The numbers a machine uses internally to stand for an input. | What the machine writes on its scratch paper |
| Feature | Chapter 3's word, unchanged: one numerical property of an item. | One slot on a stat card |
| Embedding | The standard name for a *learned* stat card: a vector of features adjusted during training. | A stat card the machine filled in itself |
| Embedding table | One embedding per token, stacked. This page calls it **the binder**. | A binder of stat cards, one page per token |
| Look-up | Fetching a token's card from the binder by its token number. | Opening the binder to page 2 |
| Concatenation | Joining vectors end to end, in order. | Gluing cards side by side into one long strip |
| Fixed context | A predetermined number of recent tokens supplied to the model — here, three. | A viewing slit that shows exactly three tokens |
| Logit | Chapter 4's word, unchanged: an unrestricted score, pre-softmax. | A raw score — this week *computed*, not fetched |
| Forward pass | The standard name for the whole pipeline run start to finish, input to scores. | The forecast, manufactured left to right |
| Shape | The dimensions of an array — how many rows, how many slots. | The label on the box, before you look inside |
| Multi-Layer Perceptron (MLP) | The standard name for this architecture: layers of weigh-and-add with gates between. | The whole assembly line, named |

## <font color="#388bfd">Day 2 — The Life of One Forecast</font>

The model is **five frozen arrays** — meet them before the pipeline runs:

| Array | Shape | Role |
|---|---|---|
| `statCards` | $3 \times 2$ | the binder: one learned two-slot card per token |
| `hiddenWeights` | $4 \times 6$ | four hidden units, each with one weight per slot of the joined row |
| `hiddenBiases` | $4$ | one bias per hidden unit |
| `outputWeights` | $3 \times 4$ | one output unit per vocabulary token, each reading all four hidden units |
| `outputBiases` | $3$ | one bias per output unit |

That is $6 + 28 + 15 = 49$ numbers, every one trained offline on the order history and then frozen. The whole of Day 2 follows **one forecast** through them: the context `pineapple pizza pineapple` — tokens `[1, 0, 1]` — which really occurs at the very start of the training history, where the next token is `pizza`. Six steps, in the order they always run. For each step: *when* it happens, then *how*.

## <font color="#388bfd">Step 1 — Look Up: a Token Number Becomes a Stat Card</font>

**When:** first, always. The context arrives as bare token numbers, and nothing downstream can weigh a token number.

**How:** each token number is used as an *address* into the binder. Here is the entire binder — these are real trained values, and the code calls this step `lookUpStatCards`:

```text
the binder (statCards):
  card 0  pizza      [-1.12,  0.47]
  card 1  pineapple  [ 0.38, -0.01]
  card 2  pepperoni  [-0.07, -0.06]

context [1, 0, 1] fetches:  card 1, card 0, card 1
```

Chapter 3's stat cards had slots you named yourself — `[topping, sweet, savory, laundry]`. These cards have **no named slots**. Each slot holds whatever value made forecasts better during offline training; slot 0 does not "mean" anything you could put into English. That is what *learned features* are.

One question you must be able to answer cold: **why is look-up not multiplication?** Token 2 does not mean "two of something" — it means *page 2 of the binder*. If the machine instead multiplied the token number by some vector, then pepperoni's representation would be forced to be exactly twice pineapple's, and pizza's (token 0) would be forced to be all zeros forever. The token number never enters any arithmetic. It is an address, and look-up is a fetch.

**State:** the binder is **read**. The fetched cards are **clones** — the Tester scribbles on one and checks the binder stayed clean.

## <font color="#388bfd">Step 2 — Join: Three Cards Become One Row</font>

**When:** immediately after look-up — the hidden layer wants one flat row of slots, not a stack of cards.

**How:** glue the cards end to end, oldest context position first (`joinCards`):

```text
card 1  [ 0.38, -0.01]  ┐
card 0  [-1.12,  0.47]  ├─ join ─►  [ 0.38, -0.01, -1.12, 0.47, 0.38, -0.01 ]
card 1  [ 0.38, -0.01]  ┘             slots 0–1: three back   slots 2–3: two back   slots 4–5: one back
```

Order **is** meaning here: the hidden layer's weight for slot 4 is specifically a weight for "slot 0 of the most recent token." Shuffle the cards and every weight silently changes meaning. Notice also that pineapple's card appears **twice** in the row — the same card, fetched twice, because the same token sits at two context positions. Remember that fact; it matters enormously in Chapter 6.

**State:** a new six-slot row is **created**. Nothing is altered.

## <font color="#388bfd">Step 3 — Weigh and Add: the Hidden Layer</font>

**When:** the joined row exists; now the four hidden units each weigh all six slots — Day 1's `weighAndAdd`, verbatim, just wider.

**How:** unit by unit, $z = b + \sum_i w_i x_i$. Two of the four, with every product shown:

```text
joined row x:      [ 0.38,  -0.01,  -1.12,   0.47,   0.38,  -0.01  ]

unit 0 weights:    [ 0.67,   0.25,   0.62,   0.15,   0.24,   0.11  ]   bias 0.10
        products:  [ 0.2546, -0.0025, -0.6944, 0.0705, 0.0912, -0.0011]
        z = 0.10 + (sum of products = -0.2817) = -0.1817

unit 3 weights:    [ 0.26,   0.17,  -0.63,   1.15,   0.41,   0.66  ]   bias 0.38
        products:  [ 0.0988, -0.0017,  0.7056, 0.5405, 0.1558, -0.0066]
        z = 0.38 + (sum of products = 1.4924) = 1.8724

all four units:    z_hidden = [ -0.1817,  -1.1491,   0.3005,   1.8724 ]
```

**State:** `hiddenWeights` and `hiddenBiases` are **read**. A new four-entry row is **created**.

## <font color="#388bfd">Step 4 — Rectify: the Gate Decides Who Speaks</font>

**When:** between the two weigh-and-adds — exactly where the collapse proof said a gate must stand.

**How:** $\max(0, z)$, entry by entry (`rectify`):

```text
z_hidden:  [ -0.1817,  -1.1491,   0.3005,   1.8724 ]
a_hidden:  [  0.0,      0.0,      0.3005,   1.8724 ]     units 0 and 1 silenced
```

For this context, units 2 and 3 are awake. Now watch the input-dependent routing the collapse proof promised — run a *different* context, `pizza pineapple pizza`, through the same frozen weights:

```text
context [0, 1, 0]:   z_hidden = [ -0.5159,   2.6345,   0.0521,  -0.2312 ]
                     a_hidden = [  0.0,      2.6345,   0.0521,   0.0    ]
```

A different squad wakes up — unit 3 carried the topping-ending forecast, unit 1 carries the pizza-ending one. Same 49 numbers, genuinely different arithmetic per context. No single weighted sum can do that.

**State:** a new row is **created**; the weighted sums come back untouched.

## <font color="#388bfd">Step 5 — Weigh and Add Again: the Unrestricted Scores</font>

**When:** the gated hidden row is ready; one output unit per vocabulary token now weighs it.

**How:** `weighAndAdd` once more — output weights, output biases:

```text
a_hidden:                 [ 0.0,  0.0,  0.3005,  1.8724 ]

pizza's unit:      0.57 + (-0.37)(0) + (-0.71)(0) + (-0.04)(0.3005) + (0.53)(1.8724) =  1.5504
pineapple's unit:  0.05 + ( 0.38)(0) + ( 0.58)(0) + (-0.31)(0.3005) + (-0.84)(1.8724) = -1.6160
pepperoni's unit: -0.63 + (-0.31)(0) + ( 0.58)(0) + (-0.61)(0.3005) + (-0.18)(1.8724) = -1.1503

unrestricted scores:      [ 1.5504,  -1.6160,  -1.1503 ]
```

You know these by their standard name: **logits** — Chapter 4's word for unrestricted scores whose destiny is softmax. The only difference from last week is their birthplace. The table *fetched* its logits from a stored row; this machine *manufactured* them from features. Softmax neither knows nor cares.

**State:** `outputWeights` and `outputBiases` are **read**; the length-3 score row is **created**.

## <font color="#388bfd">Step 6 — Softmax: the Forecast</font>

**When:** last step of manufacturing — scores become a probability distribution.

**How:** Chapter 4's stable softmax, handed back to you as a provided tool — same three moves:

```text
scores:                [ 1.5504,  -1.6160,  -1.1503 ]
subtract max (1.5504): [ 0.0,     -3.1663,  -2.7007 ]
exponentiate:          [ 1.0000,   0.0422,   0.0672 ]
divide by sum 1.1093:  [ 0.9015,   0.0380,   0.0605 ]
```

After `pineapple pizza pineapple`, the model says: 90% `pizza`, 4% `pineapple`, 6% `pepperoni`. For the formula-minded, the same machine in one line:

$$p_k = \frac{e^{z_k - m}}{\sum_{j} e^{z_j - m}}$$

| Symbol | What it is |
|---|---|
| $p_k$ | the forecast probability for vocabulary token $k$ |
| $z_k$ | token $k$'s unrestricted score from Step 5 |
| $m$ | the largest of the scores — subtracted from every score so `Math.exp` cannot overflow; provably changes no share |
| $j$ | runs over every vocabulary token, so the denominator is the total of all the exponentials |
| $e^{(\cdot)}$ | the exponential function, `Math.exp` — makes every share positive, never exactly zero |

## <font color="#388bfd">Step 7 — Grade: Chapter 4's Loss, Untouched</font>

**When:** after the forecast, whenever a flashcard supplies the true next token. The history says `pizza` followed this context.

**How:** exactly Chapter 4 — charge the negative natural log of the probability given the truth:

$$L = -\ln(p_{\text{target}})$$

| Symbol | What it is |
|---|---|
| $L$ | the loss — the grade for this one forecast; 0 for certainty in the truth, growing with surprise |
| $p_{\text{target}}$ | the single forecast entry belonging to the true next token — here $p_0 = 0.9015$ |
| $\ln$ | the natural logarithm, `Math.log` |

```text
loss([1,0,1] -> pizza)     = -ln(0.9015) = 0.1037     a good forecast, cheap
loss([0,1,0] -> pepperoni) = -ln(0.3206) = 1.1377     an honest mixture, moderate
```

And here the week's story stops mid-sentence — *deliberately*. In Chapter 4, the grade immediately fed the slope: `p` minus one-hot, poured into the bucket. Run that reflex here and it dies instantly: that shortcut assigned blame to *a stored row of logits*. This machine has no stored row — its logits were manufactured through cards, weights, a gate, and more weights. The grade is computed, and then **nothing happens**. There is no bucket. There is no step. The loss is a verdict with no way to reach the 49 numbers that caused it.

### <font color="#79c0ff">Check yourself — Set C</font>

The whole pipeline by hand, on a miniature model. Vocabulary of 2; the binder holds one-slot cards: card 0 = $[2]$, card 1 = $[-1]$. Context length 2. One hidden unit: weights $[0.5, 1]$, bias $0$, rectified. Two output units: weights $[1]$ and $[-1]$, biases $[0, 0]$.

1. Look up and join for context $[1, 0]$.
2. Hidden weighted sum, and the gated value.
3. The unrestricted scores, and the forecast (softmax of two entries — subtract the max, exponentiate, normalize).
4. The history shows token 1 next. What loss is charged? And what would the charge have been had the history shown token 0?

## <font color="#388bfd">What Is Read, What Is Written</font>

The week's discipline, in one table — every array a forecast touches, and its fate:

| Array | Created when | Read by | Ever changed? |
|---|---|---|---|
| `statCards`, `hiddenWeights`, `hiddenBiases`, `outputWeights`, `outputBiases` | Once, at construction (copied in) | Every forecast | **Never** — frozen all week |
| fetched cards | Step 1, fresh every forecast | Step 2 | Created, used, discarded |
| joined row | Step 2 | Step 3 | Created, used, discarded |
| hidden sums / gated row | Steps 3–4 | Steps 4–5 | Created, used, discarded |
| scores / forecast | Steps 5–6 | Steps 6–7 | Created, used, discarded |

Compare Chapter 4, where the gradient bucket was **accumulated** into, the logits were **overwritten** by `step`, and the bucket was **reset** by `zeroGradients`. This chapter has no accumulate, no overwrite, no reset — the only writes anywhere are `Neuron.setValue` and `recomputeValue` overwriting one neuron's stored value during Day 1's object traces. That is why the Tester can demand: a hundred forecasts and grades, then every stat card bit-for-bit identical.

## <font color="#388bfd">Punchline One: the Cousins Found Each Other</font>

Chapter 4 ended on a flaw with a face: `pineapple` and `pepperoni` both demand `pizza` next, yet each row had to learn it alone — 41 flashcards of confidence for one, 20 for the other, and nothing shared. Now open this network's binder again:

```text
  card 0  pizza      [-1.12,  0.47]
  card 1  pineapple  [ 0.38, -0.01]
  card 2  pepperoni  [-0.07, -0.06]
```

Nobody told the network the toppings behave alike. But offline training pushed both topping cards toward the same neighborhood, and pizza's card far away. Measure it — straight-line distance between cards:

$$d = \sqrt{\sum_{\text{slot}} (u_{\text{slot}} - v_{\text{slot}})^2}$$

| Symbol | What it is |
|---|---|
| $d$ | the distance between two cards — small means the network treats the tokens similarly |
| $u_{\text{slot}}, v_{\text{slot}}$ | the two cards' values in the same slot |
| $\sum_{\text{slot}}$ | totaled over every slot of the card — here, both of them |

```text
pineapple <-> pepperoni:  sqrt(0.45^2 + 0.05^2) = 0.4528     cousins
pizza     <-> pineapple:                          1.5749
pizza     <-> pepperoni:                          1.1762
```

And similar cards produce similar forecasts, because everything after Step 1 is **shared machinery**:

```text
after ...pineapple  (context [1,0,1]):  [ 0.9015,  0.0380,  0.0605 ]
after ...pepperoni  (context [1,0,2]):  [ 0.8736,  0.0517,  0.0747 ]
```

Be precise about the mechanism, because it is the answer to the Question to Carry. The cards are per-token, like Chapter 4's rows — but the hidden and output layers are **used by every forecast and were trained by every flashcard**. A pineapple flashcard sharpened weights that pepperoni's forecasts flow through. In Chapter 4, 41 pineapple flashcards taught pepperoni's row *nothing*; here, they polished 43 of the 49 numbers pepperoni depends on. Scale that up: in the archive's full vocabulary, every order ticket mentioning `mushroom` now sharpens machinery that `olive` rides through — the sharing the motivation demanded.

## <font color="#388bfd">Punchline Two: the Mixture, Rediscovered</font>

Chapter 4's trained table earned its punchline by rediscovering counting. Ask this machine — which contains **no row for pizza anywhere** — what follows pizza:

```text
network forecast after pizza (context [0,1,0]):  [ 0.0366,  0.6428,  0.3206 ]
Chapter 4's counted frequencies:                 [ 0.000,   0.667,   0.333  ]
```

The 40-vs-20 mixture emerges from cards, weights, and a gate — machinery that never stored a count and never held a `pizza` row. And the old guarantees survived the rebuild: `pizza pizza` is forecast at $0.0366$ — rare, never zero, because softmax still cannot say never.

## <font color="#388bfd">Punchline Three: Why Bother — the Parameter Argument</font>

For a three-word vocabulary, 49 parameters versus the table's 9 looks like a bad trade. The trade inverts at scale. Count this architecture's numbers:

$$P = V \cdot D \;+\; (C \cdot D \cdot H + H) \;+\; (H \cdot V + V)$$

| Symbol | What it is |
|---|---|
| $P$ | the total parameter count — every number training is allowed to change |
| $V$ | vocabulary size — 3 here |
| $D$ | slots per stat card — 2 here |
| $C$ | context length — 3 here |
| $V \cdot D$ | the binder: one $D$-slot card per token — $6$ here |
| $C \cdot D \cdot H + H$ | the hidden layer: each of $H$ units weighs all $C \cdot D$ joined slots, plus one bias each — $28$ here |
| $H$ | hidden units — 4 here |
| $H \cdot V + V$ | the output layer: one unit per token, each weighing all $H$ hidden values, plus biases — $15$ here |

Now the archive scale. Chapter 4 warned that a 50,000-token table needs $50{,}000^2 = 2.5$ **billion** cells, almost all starved of flashcards. This architecture at a realistic size — $V = 50{,}000$, $D = 64$, $C = 3$, $H = 256$:

```text
binder   50,000 x 64            =  3,200,000
hidden   (3 x 64) x 256 + 256   =     49,408
output   256 x 50,000 + 50,000  = 12,850,000
total                           = 16,099,408      about 155x smaller than the table
```

Smaller is only half the win. The deeper half: in the table, a rare token's row stays forever ignorant. Here, a rare token still gets a card of its own — but 13 million of the 16 million numbers serving its forecasts are **shared**, trained by every flashcard in the corpus.

## <font color="#388bfd">The Gap This Chapter Cannot Close</font>

Grade the provided network on the full histories and put it on the course leaderboard:

```text
uniform / nearly empty anything:   1.0986  = ln 3        (Chapter 2's anchor)
this network, frozen:              0.3957 training,  0.4013 validation
Chapter 4's trained table:         0.3300 training,  0.3311 validation
the data's own floor:              about 0.317
```

Two honest readings. First: the extra context bought nothing *on this history* — check the deck and you find the topping two tokens back carries no information about the next topping, so three-token context and one-token context share the same floor. A bigger machine is not automatically a better one; it is a machine with more *capacity to be trained*. Second, and this is the cliffhanger: the network sits **0.07 above a table it should at least match**, because its offline training was stopped early and rounded off. The gap is sitting right there. You can compute the loss that proves it. And you cannot fix it — this chapter has no way to determine which of the 49 numbers to move, or by how much.

You met one tool that could, in principle, do it: Chapter 4's wiggle experiment never needed to see inside the machine. Nudge one parameter, re-run the pipeline, watch the loss — $2$ evaluations per parameter, $98$ per flashcard for this toy. For the final course model's roughly 34,000 parameters, that reflex is a dead end (Chapter 4 already did that arithmetic). The slope must come from a formula — and the formula must somehow pass blame *backward* through join, weigh, gate, weigh, and softmax, splitting credit when a card was used twice in the same row. Building that formula-machine is Chapter 6.

### <font color="#79c0ff">Check yourself — Set D</font>

1. Compute the pineapple–pepperoni card distance from the binder yourself and confirm $0.4528$.
2. During offline training, a flashcard with context $[1, 0, 1]$ arrived. Which of the five arrays received adjustments from it — and which of those does a *pepperoni-ending* forecast later flow through? What is the Chapter 4 contrast?
3. Count the parameters for $V = 1000$, $D = 16$, $C = 3$, $H = 64$, and compare against a $1000 \times 1000$ table.
4. A classmate looks at the leaderboard and concludes "networks are worse than tables." Give the two-part correction.

**Day 2 homework:** [Assignment](ASSIGNMENT.md) Part 2 — implement the pipeline (TODOs 5–10), record the punchline readings, and answer the concept questions.

---

## <font color="#388bfd">What You Are Given</font>

The starter code is in [starter/](starter/) — five files. Two contain TODOs; the rest are complete:

| File | Status | Role |
|---|---|---|
| [Connection.java](starter/Connection.java) | Complete | One weighted wire — a label, never a computation |
| [Neuron.java](starter/Neuron.java) | **TODO 1–2** | One unit: weigh and add, then the gate — the object form |
| [FeatureNetwork.java](starter/FeatureNetwork.java) | **TODO 3–10** | The forecast pipeline as arrays (the softmax and the parameter count are provided) |
| [NetworkFixtures.java](starter/NetworkFixtures.java) | Complete | The practice network, the trained-and-frozen provided model, and the order history |
| [Tester.java](starter/Tester.java) | Complete | Reproduces every worked trace on this page, runs the required tests, prints the punchlines |

Implement the TODOs in order, rerunning `Tester` after each — unimplemented stages report as `TODO`, not `FAIL`:

1. `weighAndAddInputs` — one neuron reads its wires: bias plus value-times-weight, totaled (Day 1)
2. `recomputeValue` — the gate, then the only overwrite: the neuron's stored value (Day 1)
3. `weighAndAdd` — a whole layer as one loop over a weight table (Day 1)
4. `rectify` — the gate applied to a whole layer, negatives silenced to exactly zero (Day 1)
5. `lookUpStatCards` — Step 1: token numbers fetch cloned cards from the binder (Day 2)
6. `joinCards` — Step 2: cards glued into one row, order preserved (Day 2)
7. `unrestrictedScores` — Steps 1–5 chained: fetch, glue, mix, gate, score (Day 2)
8. `forecast` — Step 6: the provided softmax turns scores into a distribution (Day 2)
9. `loss` — Step 7: Chapter 4's grade, charged to this pipeline (Day 2)
10. `averageLoss` — the report card over a history, flashcards starting at position three (Day 2)

## <font color="#388bfd">Evidence Checkpoint</font>

Six observations your finished code must produce:

1. **The practice trace reproduces.** Hidden sums $[-2, 4]$, gated $[0, 4]$, outputs $[-4, 6]$ — from objects and from `weighAndAdd` alike, and the gateless collapse lands on $[-8, 4]$ both ways.
2. **The worked forecast reproduces.** Joined row → hidden sums $[-0.1817, -1.1491, 0.3005, 1.8724]$ → scores $[1.5504, -1.6160, -1.1503]$ → forecast $[0.9015, 0.0380, 0.0605]$ → loss $0.1037$.
3. **Objects equal arrays.** Hidden unit 3 built as a `Neuron` graph matches the array pipeline to $10^{-9}$ — both landing on $1.8724$.
4. **The anchor holds.** A nearly empty network (seed 7) scores average training loss $1.0986$ — $\ln 3$, Chapter 2's anchor, now three machines in a row.
5. **The punchlines print.** Topping cards $0.4528$ apart against $1.5749$ and $1.1762$ to pizza; the after-pizza forecast within a few hundredths of the counted $[0, 0.667, 0.333]$ with no exact zeros; training loss $0.3957$, validation $0.4013$.
6. **Nothing moves.** A hundred forecasts and grades leave every stat card bit-for-bit unchanged, and the parameter count prints exactly $49$.

## <font color="#388bfd">Required Tests</font>

`Tester` covers all of these — confirm every one reports `PASS`:

- A neuron's weighted sum reproduces the practice numbers, and computing it twice changes nothing — reading is not writing.
- `recomputeValue` overwrites the stored value; the gate silences negative totals to exactly zero, passes positives, and a linear unit keeps its negatives.
- The full practice network lands on $[-4, 6]$ as objects and as arrays, and without the gate collapses to the single weighted sums $[-8, 4]$.
- `weighAndAdd` and `rectify` return new arrays and leave their inputs untouched; mismatched shapes are refused.
- Look-up fetches the right cards as clones — scribbling on a fetched card leaves the binder clean.
- Joining preserves order: contexts $[1,0,2]$ and $[2,0,1]$ join differently.
- The pipeline reproduces every worked number: hidden sums, gated row, scores, forecast, and both losses.
- A four-token history holds exactly one flashcard; the provided model scores $0.3957 / 0.4013$; a nearly empty network sits at $\ln 3$.
- The topping cards are cousins, both topping contexts forecast pizza above 85%, and the after-pizza forecast matches the counted mixture with no exact zero.
- A hundred forecasts change nothing; the parameter count is 49; short contexts, bad tokens, and flashcard-less histories are refused.

## <font color="#388bfd">Answer Key</font>

**Set A**

1. $z = 2 + (0.5)(4) + (-1)(3) = 1$; rectified output $\max(0, 1) = 1$.
2. $z = 2 + 2 - 6 = -2$; gated output $0$ — and it contributes exactly nothing downstream, since $0$ times any weight is $0$.
3. Zero, for every unit, always. The bias sets a resting level — and for a rectified unit it moves the wake-up threshold: how much input it takes before $z$ crosses $0$.
4. `recomputeValue` — it overwrites the stored value. `weighAndAddInputs` only reads: the bias, and each source's value through its wire.

**Set B**

1. $z = [1 + 2 - 2, \; -1 + 6 + 1] = [1, 6]$; gated $[1, 6]$; outputs $[0 + 2 - 6, \; 2 + 1 + 6] = [-4, 9]$.
2. $2 + z_{\text{top}} + z_{\text{bottom}} = 2 + (1 + x_0 - 2x_1) + (-1 + 3x_0 + x_1) = 2 + 4x_0 - x_1$ — one weighted sum, bias $2$, weights $[4, -1]$. Depth without gates is a single linear layer in disguise.
3. $4 \times 6 = 24$ multiplications; the product for unit `u`, slot `s` uses `layerWeights[u][s]` — one row per unit, one column per input slot.
4. Different bookkeeping — objects carry a `Connection` per wire, the array form packs the same weights into rows. Identical arithmetic, identical numbers, to the last bit.

**Set C**

1. Card 1 is $[-1]$, card 0 is $[2]$; joined row $[-1, 2]$.
2. $z = 0 + (0.5)(-1) + (1)(2) = 1.5$; gated: $1.5$.
3. Scores $[(1)(1.5), \; (-1)(1.5)] = [1.5, -1.5]$. Softmax: subtract the max → $[0, -3]$; exponentiate → $[1, 0.0498]$; divide by $1.0498$ → $[0.9526, 0.0474]$.
4. $-\ln(0.0474) = 3.05$ — the model called the truth nearly impossible and paid for it. Had token 0 followed: $-\ln(0.9526) = 0.0486$, nearly free.

**Set D**

1. $\sqrt{(0.38 - (-0.07))^2 + (-0.01 - (-0.06))^2} = \sqrt{0.45^2 + 0.05^2} = \sqrt{0.205} = 0.4528$.
2. Adjusted: pineapple's and pizza's cards (the tokens in the context), the hidden weights and biases, the output weights and biases. A pepperoni-ending forecast flows through pizza's card, pepperoni's card, and *the same hidden and output layers* — so the flashcard sharpened most of the machinery pepperoni uses. In Chapter 4, that flashcard would have touched exactly one row that pepperoni's forecasts never read.
3. $1000 \cdot 16 + (48 \cdot 64 + 64) + (64 \cdot 1000 + 1000) = 16{,}000 + 3{,}136 + 65{,}000 = 84{,}136$ — about 12 times smaller than the table's $1{,}000{,}000$.
4. First, on this history the extra context carries no extra signal, so the network cannot beat the table's floor — capacity is not information. Second, the network's numbers are frozen mid-training: its gap above the table is unfinished training, not a verdict on the architecture — and closing that gap requires machinery this chapter deliberately lacks.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** An embedding is not an English definition of a token. It is a vector adjusted because it helps prediction — its slots have no names and no translation.

> **Misconception:** A mathematical "neuron" should not be treated as a biological simulation. It is a weighted sum and a gate, loosely inspired by biology and nothing more.

More traps worth defusing now:

| If you catch yourself thinking… | Remember |
|---|---|
| "The network multiplies by the token number." | The token number is an address. Card 2 is *fetched*, never computed — otherwise pepperoni would be forced to be twice pineapple, and pizza all zeros. |
| "ReLU throws information away, so it must hurt." | Silencing is the mechanism: which units wake depends on the input, which is exactly what a gateless stack cannot do — it collapses into one weighted sum. |
| "`forecast` slowly changes the network as it runs." | The forward pass is pure reading. A hundred forecasts leave the model bit-for-bit identical — the Tester proves it. |
| "The hidden slots mean things, like Chapter 3's `[topping, sweet, savory]`." | Chapter 3's slots were named by you. These were learned; they mean whatever made the loss fall, and nothing nameable. |
| "More parameters means better forecasts." | 49 lost to Chapter 4's 9 this week. Parameters are capacity; only *training* converts capacity into skill — and this chapter's training is frozen. |
| "The scratch rows (joined row, hidden sums, scores) are parameters too." | Parameters are the numbers training may change: the five frozen arrays. Scratch rows are created per forecast and discarded. |
| "The loss will nudge the weights, like last week." | Not this week. The grade is computed and nothing happens — the slope machinery for this machine does not exist until Chapter 6. |
| "Look-up failing on token 3 is a bug." | The binder has exactly $V$ cards. A token outside $[0, V)$ is a caller error, and the model must refuse it loudly. |

## <font color="#388bfd">Stretch Goals</font>

1. **Sigmoid gate** — $1 / (1 + e^{-z})$, squashing into $(0, 1)$; swap it into the practice network and re-trace.
2. **Hyperbolic tangent gate** — squashes into $(-1, 1)$; compare its silencing behavior with ReLU's.
3. **Leaky Rectified Linear Unit** — negatives keep a small slope instead of dying; when might a permanently silenced unit be a problem?
4. **Gaussian Error Linear Unit (GELU)** — the smooth gate the final transformer will prefer; plot it beside ReLU by hand at a few points.
5. **A second hidden layer** — extend `unrestrictedScores` to mix, gate, mix, gate, score; recount the parameters with the formula.
6. **Network-diagram exporter** — print any `Neuron` graph as text: every wire, weight, bias, and stored value.
7. **Nearest-neighbor explorer** — given any card, rank the other cards by distance; on the toy binder it finds the cousins instantly.
8. **One-hot versus learned cards** — replace the binder with fixed one-hot cards ($D = V$), recount parameters, and explain what was lost besides size.
9. **Train it by wiggling** — Chapter 4's finite difference, applied to all 49 parameters: nudge, re-evaluate, step downhill. Watch the training loss fall below $0.3957$ — then count the pipeline evaluations one step cost you, and feel exactly the pain Chapter 6 exists to remove.

---

The network can calculate sophisticated scores, but its weights are frozen. When it makes a poor prediction, nothing yet identifies which connections should change. The loss for `pizza pineapple pizza` flowed through two fetched cards — one of them used twice — seven weighted sums, a gate that silenced half the hidden layer, and a softmax; somewhere in those 49 numbers sit the ones most responsible, and this chapter can only stare at them. The machine needs a way to follow its own error backward.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you compute one unit's weighted sum and gated output by hand from its weights, bias, and inputs?
- [ ] Can you explain what the binder stores, what look-up does, and why look-up is not multiplication by the token number?
- [ ] Can you state what `rectify` does to a negative, zero, and positive weighted sum — and what a silenced unit contributes downstream?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you build the practice network from `Neuron` objects and match the $[-4, 6]$ trace exactly?
- [ ] Can you run all six pipeline steps by hand on the Set C miniature and land on $[0.9526, 0.0474]$?
- [ ] Can you say, for every array a forecast touches, whether it is read, created, or overwritten — and why calling `forecast` twice must return identical answers?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you demonstrate that object traversal and `weighAndAdd` compute the same numbers, and prove with algebra why a gateless stack collapses into one weighted sum?
- [ ] Can you explain the sharing mechanism precisely — which arrays are per-token, which are shared, and why Chapter 4's lonely rows had no equivalent?
- [ ] Can you use the parameter formula to compare this architecture against a $V^2$ table at archive scale, and give the two-part correction to "networks are worse than tables"?

---

[Assignment](ASSIGNMENT.md)

← [A Table That Learns](../TrainableBigram/) — Next: [Following the Error Backward](../ScalarAutograd/)
