<div align="center">

# The Hand-Built Spotlight
*<font color="#8b949e">Causal self-attention with programmer-written rules — the central idea before any learning</font>*

<font color="#a371f7">Learning</font>

</div>

---

> Chapter 2 ended with receipts: generated text that loses the thread the moment the answer depends on anything farther back than one token. A sentence may contain thirty earlier tokens, but only one or two are useful for the next prediction. Remembering everything equally is not enough. The machine needs a spotlight: a way for the current position to examine earlier positions, assign each one an importance, and combine the useful information. This week, every rule controlling the spotlight is written by you.

## <font color="#388bfd">Question to Carry</font>

> **How can one position selectively use information from earlier positions?**

## <font color="#388bfd">Why Attention Appears This Early</font>

This chapter deliberately introduces self-attention before any neural-network training. You first learn **what attention computes**. You do not yet learn how its scoring rules are discovered — that prevents self-attention, gradients, parameter matrices, and optimization from arriving as one inseparable block. The reference implementation is tiny, slow, and inspectable, and nothing in it trains.

The chapter is two class periods. Each day ends with homework:

| Day | In class | Homework |
|---|---|---|
| 1 | The table of cards · Stage 1: remember everything equally · Stage 2: write the scores by hand · Softmax | [Assignment](ASSIGNMENT.md) Part 1 — TODOs 1–3 plus problem sets A and B on paper |
| 2 | The bridge: words become stat cards · Stage 3: the dot product · The causal mask · The complete pipeline · From loop to grid · the Classmate Matrix activity | [Assignment](ASSIGNMENT.md) Part 2 — TODOs 4–7 plus the concept questions |

## <font color="#388bfd">The Table of Cards — Read This First</font>

Everything in this chapter happens on one tiny, fixed example. Getting these ground rules straight now prevents every confusion that follows.

Someone has already handed you three cards from a stack of pizza orders, in this exact order:

```text
position 0:   PINEAPPLE   (the card carries: SWEET)
position 1:   PEPPERONI   (the card carries: SAVORY)
position 2:   PINEAPPLE   <- the current position, asking a question
```

Three ground rules:

1. **The sequence is given.** Nobody is generating these tokens. Chapter 2's sampler is switched off. We are *reading* a sequence that already exists — like holding a sentence that is already written on the page — and asking how position 2 can make use of positions 0 and 1.
2. **Position means order, nothing more.** Position 0 is simply the first card, position 1 the second, position 2 the third. No probabilities are attached to the order.
3. **The table is not the library.** The cards on the table are the **context window** — only the tokens of *this* sequence. They are not the training corpus, not the vocabulary, not everything the model has ever seen. In fact, this chapter has no training corpus at all: every number in it is written by hand.

Each card has two distinct things on it: the token written on its face (`PINEAPPLE`), and the information it carries (`SWEET`). Keep those separate — the face is how a card gets *found*; what it carries is what gets *used*. That split becomes the vocabulary of attention in Stage 2.

## <font color="#388bfd">Vocabulary — Day 1</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Context window | The maximum number of earlier tokens the model can examine. | The cards physically on the table |
| Causal | Restricted so a position may use only itself and earlier positions. | Reading left to right; no peeking ahead |
| Causal mask | A rule that removes future positions from consideration. | A hand covering the cards to the right |
| Attention | A calculation that assigns importance weights to available pieces of information and combines them. | Volume dials, one per card, then a mix |
| Self-attention | Attention in which a sequence attends to positions in that same sequence. | The cards examining each other |
| Attention score | A number representing how strongly one position matches another. Any real number. | Raw points scribbled on a scratchpad |
| Attention weight | A normalized, nonnegative importance value. Weights in a row sum to one. | A pie chart of the mix |
| Weighted sum | A sum in which each input is multiplied by an importance weight. | 96% of this card, 2% of that one |
| Query | What the current position is seeking. | The request slip position 2 fills out |
| Key | How a position announces itself for matching. | The label on each card's face |
| Value | The information a position contributes when it receives attention. | What the card carries inside |
| Softmax | A function converting arbitrary scores into positive values that sum to one. | The machine that turns points into pie slices |
| Attention matrix | A table whose row $i$ holds the attention weights used by position $i$. | One pie chart per row |

---

## <font color="#388bfd">Day 1 — What the Spotlight Computes</font>

## <font color="#388bfd">Stage 1: Remember Everything Equally</font>

Before the spotlight can be *selective*, information has to be able to travel from earlier positions to later ones at all. Stage 1 builds that plumbing with the dumbest possible rule:

> At each position, mix together the current card and **every earlier card in this sequence**, all with equal weight.

Apply it to the table, position by position:

| Standing at | Cards mixed | Weight each |
|---|---|---|
| position 0 | PINEAPPLE | $1$ |
| position 1 | PINEAPPLE, PEPPERONI | $\frac{1}{2}, \frac{1}{2}$ |
| position 2 | PINEAPPLE, PEPPERONI, PINEAPPLE | $\frac{1}{3}, \frac{1}{3}, \frac{1}{3}$ |

Position 0 has no past, so its mixture is itself. Position 1 mixes two cards at half volume each. Position 2 mixes all three at a third each. No position ever receives information from its future — that restriction is the word **causal**.

Only after the numbers make sense, here is the same rule in notation. For input vectors $x_0, x_1, \ldots$, the output at position $i$ is:

$$y_i = \frac{1}{i+1} \sum_{j=0}^{i} x_j$$

### <font color="#79c0ff">Check yourself — Set A</font>

Answers are in the [Answer Key](#answer-key) below. Do these on paper before moving on.

1. A sequence has five positions. Standing at position 3, which positions are mixed, and what weight does each get?
2. Standing at position 0 of any sequence, what is the mixture?
3. For the sequence `OLIVE, ONION, OLIVE, BACON`: what fraction of the mixture at position 2 comes from cards whose face reads `OLIVE`?
4. The card at position 3 is swapped for a completely different one. Does the mixture at position 1 change? Why or why not?

### <font color="#79c0ff">Why this stage matters — and how it fails</font>

Stage 1 proves information can flow forward. It also creates the next failure on purpose: treating every previous position as equally important **blurs** useful and irrelevant information together. At position 2, the one card that matters (the earlier `PINEAPPLE`, carrying `SWEET`) speaks at exactly the same volume as everything else. The fix is not more mixing — it is *unequal* mixing.

## <font color="#388bfd">Stage 2: Write the Scores by Hand</font>

Here is the reasoning, in plain words: *standing at position 2, if an earlier card looks useful for what happens next, I want to turn its volume up; if it looks irrelevant, I want to turn its volume down.* Stage 2 does exactly that with a rule simple enough to write on an index card:

- If an earlier card's face matches what the current card is looking for: **+4 points**.
- If it does not match: **0 points**.
- The asking card itself: 0 points — it is the one asking; it already has its own information.
- Future cards: masked. They never receive points at all.

The current card's face reads `PINEAPPLE`, so that is what it looks for. Applying the rule:

| Position | Card | Score |
|---|---|---:|
| 0 | PINEAPPLE (carries SWEET) | 4 |
| 1 | PEPPERONI (carries SAVORY) | 0 |
| 2 | PINEAPPLE — the asker | 0 |

Two things to say out loud about those numbers:

- **The 4 is arbitrary.** It could have been +100, or +4 and −50. Stage 2's entire job is to separate *what we want* (relevant cards speak louder) from *how a machine calculates it* (Stage 3's math). The specific points do not matter yet; the *ranking* does.
- **A score is not a probability.** Scores can be any real number — 4, 0, −2.7. They do not sum to anything in particular, so they cannot be volume settings yet. Compare Stage 1, where the weights $\frac{1}{3}, \frac{1}{3}, \frac{1}{3}$ summed to exactly 1.

### <font color="#79c0ff">Naming the three roles</font>

You have already been using three ideas without names. Attach the names now, while the example is small:

- When position 2 asks *"who back there matches PINEAPPLE?"* — that request is the **query**. The query is produced by the **current position alone**. One card asks; the question comes from nowhere else.
- Each card's face — `PINEAPPLE`, `PEPPERONI` — is how the card announces itself for matching. That is its **key**. Every permitted card holds one up. **One query is compared against many keys.**
- What each card carries — `SWEET`, `SAVORY` — is what gets pulled into the mix if the card is chosen. That is its **value**.

So the entire Stage 2 rule, restated in the new vocabulary: *compare the query against every permitted key; give matching keys high scores; the scores will decide how much of each value flows into the mixture.*

> **Note:** In diagrams you will sometimes see the current card written as "QUERY PINEAPPLE". The word QUERY is a **role label**, like writing "(goalie)" next to a player's name. The token on the card is just `PINEAPPLE`; "query" describes the job that card is doing at this moment.

Why do keys matter at all — why not just look at the query? Because the same query means different things in different company. If the query is `pineapple` and the surrounding keys are `pizza`, `oven`, `mozzarella`, the useful values are about dinner. If the keys are `smoothie`, `beach`, `piña colada`, the useful values are about a vacation drink. The keys are what let one word find the right context.

## <font color="#388bfd">Softmax: Scores Become Weights</font>

The scores are `[4, 0, 0]`. To mix values we need volume settings — numbers that are nonnegative and sum to exactly 1, like Stage 1's thirds. **Softmax** is the machine that converts any list of scores into exactly that. Three steps, always in this order:

1. **Subtract the maximum score from every score.** This prevents `Math.exp` from overflowing on large scores and — as you will prove in the tests — changes nothing about the final answer.
2. **Exponentiate each result** ($e^s$). This makes every entry positive and stretches gaps: higher scores end up disproportionately larger.
3. **Divide each entry by the sum of all entries.** Now they sum to 1.

Worked example with scores `[2.0, 1.0, 0.0]`:

```text
subtract max (2.0):   [ 0.0,    -1.0,    -2.0  ]
exponentiate:         [ 1.0000,  0.3679,  0.1353]
divide by sum 1.5032: [ 0.6652,  0.2447,  0.0900]
```

Now the Stage 2 scores `[4, 0, 0]`:

```text
subtract max (4.0):   [ 0.0,    -4.0,    -4.0  ]
exponentiate:         [ 1.0000,  0.0183,  0.0183]
divide by sum 1.0366: [ 0.9647,  0.0177,  0.0177]
```

The mixture at position 2 is now roughly **96% what the pineapple card carries** and about 2% each of the others. Compare Stage 1's blur of a third each. That is the spotlight.

One connection ties the whole day together: run softmax on all-equal scores `[0, 0, 0]`:

```text
subtract max:  [0, 0, 0]  ->  exponentiate: [1, 1, 1]  ->  normalize: [1/3, 1/3, 1/3]
```

**Stage 1 is not a different mechanism — it is attention in which every permitted score is equal.** Uniform averaging is the special case; scoring is what got added.

Notice also what softmax refuses to do: no permitted position ever gets weight *exactly* zero — PEPPERONI kept 0.0177, not 0. Softmax can turn volumes far down, never fully off. The only exact zeros in this chapter come from the causal mask, which removes future positions *before* softmax ever sees them.

### <font color="#79c0ff">Check yourself — Set B</font>

1. The sequence is `MUSHROOM, SAUSAGE, MUSHROOM, MUSHROOM` and you are standing at position 3 (the last `MUSHROOM`, asking). Apply the Stage 2 rule (+4 earlier match, 0 otherwise, self 0). What are the four scores?
2. Run softmax on your scores from problem 1, showing the three steps.
3. Softmax of `[0, 0, 0, 0]`? Which stage does that reproduce?
4. Without computing: softmax of `[5, 1, 1]` versus softmax of `[9, 5, 5]` — same or different? Why?
5. Can an attention score be −2.7? Can an attention weight be −2.7?

**Day 1 homework:** [Assignment](ASSIGNMENT.md) Part 1 — implement uniform causal weights, stable softmax, and the weighted blend (TODOs 1–3), and bring problem sets A and B worked on paper.

---

## <font color="#388bfd">Vocabulary — Day 2</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Feature | One numerical property used to represent an item. | One slot on a stat card |
| Feature vector | An ordered list of numerical features. | The whole stat card |
| Vector dimension | The number of values in a vector. | How many slots the card has |
| Dot product | The sum of products of corresponding vector entries. | Compare cards slot by slot, add it up |
| Similarity | A numerical estimate of how strongly two representations match. | A bigger dot product |

## <font color="#388bfd">Day 2 — How a Machine Computes the Spotlight</font>

> **Demo:** Keep [The Spotlight Bench](https://harvard-westlake.github.io/Topics/MiniGPT/FixedAttention/demos/spotlight-bench.html) ([source](demos/spotlight-bench.html)) projected through this day — every table below is computed live in it, and any card can be swapped mid-discussion. The button in the top corner switches to a Pop-vs-Rap card set with messier, blended feature values — a second pass for students who want the training wheels off.

## <font color="#388bfd">The Bridge: Computers Cannot Compare Words</font>

Stage 2's rule was *"does this card's face match the word PINEAPPLE?"* — a string comparison a human performs instantly. The machine needs the score to come out of **arithmetic**, because arithmetic is what Chapter 6 will eventually learn to adjust. So before any formula: what must happen to the words `PINEAPPLE` and `PEPPERONI` so a numeric loop can process them?

**First idea: use the token identifiers from Chapter 1.** `PINEAPPLE` might be token 301, `PEPPERONI` token 17. Multiply them? $301 \times 17$ says nothing about pizza. Chapter 1's misconception checkpoint already warned you: **identifiers are labels.** Token 301 is not "more" than token 17, and no arithmetic on labels produces meaning. One number per word cannot hold what a word means.

**The fix: give every token a list of numbers instead of one number.** Think of it as a **stat card** from a game. Each slot on the card is a **feature** — one measurable property. The whole list is a **feature vector**, and the number of slots is its **dimension**. With four features `[topping, sweet, savory, laundry]`:

| Card | topping | sweet | savory | laundry |
|---|---:|---:|---:|---:|
| PINEAPPLE | 1.0 | 1.0 | 0.0 | 0.0 |
| PEPPERONI | 1.0 | 0.0 | 1.0 | 0.0 |
| GYM SOCK | 0.0 | 0.0 | 0.0 | 1.0 |

Now `PINEAPPLE` and `PEPPERONI` genuinely share something a machine can find — both have 1.0 in the `topping` slot — while `GYM SOCK` shares nothing with either.

> **Note:** Where do these numbers come from? This week, you write them by hand — they live in the provided fixtures. In Chapter 5 the model begins *learning* its own feature vectors, and by Chapter 8 it learns separate query, key, and value versions of them. Nothing about today's math changes when that happens; only the origin of the numbers does.

## <font color="#388bfd">Stage 3: The Dot Product Scores the Match</font>

Here is the entire matching machine, as a loop — meet it as code before any notation:

```java
double total = 0.0;
for (int feature = 0; feature < left.length; feature++) {
    total += left[feature] * right[feature];
}
```

`left` is the query's stat card; `right` is one key's stat card. The loop walks the slots in parallel, multiplies each pair, and adds everything up. Why is multiply-then-add a *matching* calculation and not just arithmetic? Because of what multiplication does to each slot:

- Both cards have the feature (`1.0 × 1.0 = 1.0`): the slot **adds to the score**.
- Either card lacks it (`1.0 × 0.0 = 0.0`): the slot **contributes nothing**.

A feature only scores when **both** sides have it. Watch it run on all three scenarios, every number visible:

**Scenario 1 — perfect match.** Query PINEAPPLE `[1, 1, 0, 0]` against key PINEAPPLE `[1, 1, 0, 0]`:

| Feature | left (query) | right (key) | product |
|---|---:|---:|---:|
| topping | 1.0 | 1.0 | 1.0 |
| sweet | 1.0 | 1.0 | 1.0 |
| savory | 0.0 | 0.0 | 0.0 |
| laundry | 0.0 | 0.0 | 0.0 |
| **total** | | | **2.0** |

**Scenario 2 — partial match.** Query PINEAPPLE against key PEPPERONI `[1, 0, 1, 0]`:

| Feature | left (query) | right (key) | product |
|---|---:|---:|---:|
| topping | 1.0 | 1.0 | 1.0 |
| sweet | 1.0 | 0.0 | 0.0 |
| savory | 0.0 | 1.0 | 0.0 |
| laundry | 0.0 | 0.0 | 0.0 |
| **total** | | | **1.0** |

**Scenario 3 — complete mismatch.** Query PINEAPPLE against key GYM SOCK `[0, 0, 0, 1]`:

| Feature | left (query) | right (key) | product |
|---|---:|---:|---:|
| topping | 1.0 | 0.0 | 0.0 |
| sweet | 1.0 | 0.0 | 0.0 |
| savory | 0.0 | 0.0 | 0.0 |
| laundry | 0.0 | 1.0 | 0.0 |
| **total** | | | **0.0** |

The scores 2.0 / 1.0 / 0.0 rank the cards exactly the way Stage 2's hand rule did — except no rule about words exists anywhere. The ranking **emerged from the numbers**. That is the jump from Stage 2 to Stage 3, and it is the whole trick.

In notation, for vectors $a$ and $b$ of dimension $d$:

$$a \cdot b = \sum_{k=0}^{d-1} a_k b_k$$

### <font color="#79c0ff">Check yourself — Set C</font>

Feature slots are `[topping, sweet, savory, laundry]` throughout.

1. `[1, 1, 0, 0] · [1, 0, 1, 0]` = ?
2. `[1, 1, 0, 0] · [0, 0, 0, 1]` = ?
3. `[2, 1, 0, 0] · [1, 1, 0, 0]` = ? (Features are not restricted to 0 and 1.)
4. `[1, 1, 0, 0] · [1, −1, 0, 0]` = ? What did the negative feature do to the score?
5. With $d = 4$, what is the *scaled* score for problem 3? (Read the next section first.)

### <font color="#79c0ff">Two small print items</font>

**Scaling.** Two shared slots produced a score of 2.0. If stat cards had 400 slots, raw totals would grow large just because the cards got longer — and softmax would then slam almost all weight onto one position. Dividing every score by $\sqrt{d}$ keeps scores comparable across dimensions. For position $i$ querying position $j$:

$$s_{ij} = \frac{q_i \cdot k_j}{\sqrt{d}}$$

**Who plays which role this week.** Stage 3 uses `query = key = value = input`: the card's one stat card plays all three roles. That has an honest consequence — every card matches *itself* perfectly, so the current position always attends to itself substantially. Expected, not a bug. Chapter 8 gives each role its own learned vector, which is when the roles genuinely separate.

## <font color="#388bfd">The Causal Mask</font>

Standing at position $i$, only positions $0$ through $i$ may be scored. Future positions are not "scored low" — they are **removed before softmax runs**, and their weights are recorded as exactly `0.0`. That is why a future weight is the only exact zero in an attention row, and it makes a testable promise: **changing a future token cannot change any earlier output.** Your Tester proves it by swapping the last card for `GYM SOCK` and confirming positions 0 and 1 produce identical outputs, bit for bit.

## <font color="#388bfd">The Complete Pipeline at One Position</font>

Every piece is built. Run the whole machine at position 2 of the table — query, keys, and values all drawn from the stat cards, $d = 4$, $\sqrt{d} = 2$:

**Step 1 — score.** The query is position 2's own card, `[1, 1, 0, 0]`:

```text
s(2,0) = ([1,1,0,0] . [1,1,0,0]) / 2 = 2.0 / 2 = 1.0     (PINEAPPLE)
s(2,1) = ([1,1,0,0] . [1,0,1,0]) / 2 = 1.0 / 2 = 0.5     (PEPPERONI)
s(2,2) = ([1,1,0,0] . [1,1,0,0]) / 2 = 2.0 / 2 = 1.0     (itself)
```

**Step 2 — mask.** Position 2 is the last position; nothing to remove. (At position 1, the score for position 2 would never have been computed.)

**Step 3 — softmax.** `[1.0, 0.5, 1.0]` becomes:

```text
subtract max (1.0):   [ 0.0,    -0.5,     0.0  ]
exponentiate:         [ 1.0000,  0.6065,  1.0000]
divide by sum 2.6065: [ 0.3837,  0.2327,  0.3837]
```

**Step 4 — blend the values.** Multiply each card's value vector by its weight and add, slot by slot:

$$y_i = \sum_{j=0}^{i} a_{ij} v_j$$

```text
y2 = 0.3837*[1,1,0,0] + 0.2327*[1,0,1,0] + 0.3837*[1,1,0,0]
   = [1.0000, 0.7673, 0.2327, 0.0000]
```

Put that next to Stage 1's equal mixture at the same position:

| Mixture at position 2 | topping | sweet | savory | laundry |
|---|---:|---:|---:|---:|
| Stage 1 — uniform | 1.000 | 0.667 | 0.333 | 0.000 |
| Stage 3 — dot product | 1.000 | **0.767** | **0.233** | 0.000 |

The `sweet` feature rose and `savory` fell, because the query found the pineapple cards — and **no line of code anywhere mentions the word "pineapple."** The selectivity came entirely from multiply-and-add over feature slots.

## <font color="#388bfd">From Loop to Grid</font>

You have been comparing one query against one key per loop call. A real context window has dozens of positions, so stack every key vector as one **row** of a grid:

```text
                 topping  sweet  savory  laundry
row 0  PINEAPPLE   1.0     1.0    0.0     0.0
row 1  PEPPERONI   1.0     0.0    1.0     0.0
row 2  PINEAPPLE   1.0     1.0    0.0     0.0
```

A stack of vectors is all a **matrix** is. Running your dot-product loop once per row — one query against the whole stack — produces one score per row in a single sweep; mathematicians call that sweep a matrix multiplication. **Compact matrix notation is bookkeeping for the loop you already wrote, not new math.** This course keeps the loops; Chapter 7 makes them fast.

Do that for *every* position's query and collect each resulting weight row into a table: that table is the **attention matrix** your code must print. Row $i$ = the pie chart position $i$ used. A 4-position example in the required format:

```text
                 pos0    pos1    pos2    pos3
position 0      1.000   0.000   0.000   0.000
position 1      0.420   0.580   0.000   0.000
position 2      0.110   0.190   0.700   0.000
position 3      0.080   0.690   0.100   0.130
```

Every row sums to 1. Everything above the diagonal is exactly 0 — the mask's staircase.

## <font color="#388bfd">What Changed Since Chapter 2</font>

```text
Chapter 2 - the bigram reader           Chapter 3 - the spotlight reader

one current token                       one current position
        |                                       |
look up ONE row of                      compare its query against the key of
transition counts                       EVERY permitted position (itself + earlier)
        |                                       |
next-token probabilities                one score per permitted position
                                                |
                                        softmax: scores -> weights (sum to 1)
                                                |
                                        weighted blend of those positions' values
```

The bigram reader's entire context was one token — one table lookup. The spotlight reader's context is every permitted position, weighted by earned relevance.

One workflow question students always ask: *is this part of training, or evaluation, or generation?* It is the **engine all of them call**. Whether a model is training on a corpus, being evaluated on held-out text, or generating for a user, this exact score → mask → softmax → blend computation is how it reads context. And in this chapter, nothing is trained at all — every number was written by hand, which is precisely why the mechanism is visible.

### <font color="#79c0ff">Check yourself — Set D</font>

1. At position 1 of the table of cards, compute the scaled scores, the softmax weights, and the blended output $y_1$.
2. The card at position 2 is replaced with GYM SOCK. Which of $y_0, y_1, y_2$ change?
3. In the 4-position example matrix above, why is the entry at row 1, column pos3 exactly 0.000 rather than merely small?
4. What must each row of any attention matrix sum to, and which required test checks it?

## <font color="#388bfd">In-Class Activity: The Classmate Matrix</font>

Feature vectors feel abstract until the vector is *you*. In this activity the class builds a real attention matrix over itself, using [The Classmate Matrix](https://harvard-westlake.github.io/Topics/MiniGPT/FixedAttention/demos/classmate-matrix.html) ([source](demos/classmate-matrix.html)). Nothing typed into the page leaves the browser.

1. **Choose the feature slots together.** As a class, pick six to nine qualities — for example: stressed, happy, overworked, friendly, skilled at cooking, athletic, funny, charismatic, frugal.
2. **Fill in your stat card.** Rank yourself 0–10 on every quality. A nickname or an invented persona works exactly as well as your real name — the math cannot tell the difference, which is itself a lesson in what a feature vector does and does not know.
3. **One dot product by hand first.** Pair up. Pick three of the qualities ($d = 3$), divide each ranking by 10 so the features live between 0 and 1, and compute your score against your partner's card: multiply slot by slot, add, divide by $\sqrt{3}$. This is exactly TODO 4 with people instead of rocks.
4. **Enter the roster.** Type or paste everyone's rankings into the page. It normalizes the features, scores every pair, and softmaxes each row into the class attention matrix.
5. **Read the matrix.** Row $i$ is student $i$'s attention. Whose row concentrates on one or two classmates? Whose spreads out almost evenly — and what would that row have looked like in Stage 1?
6. **Run a retrieval query.** Switch the spotlight to a custom request — "looking for a study partner: happy 9, funny 7, overworked 2" — and see whom the weights land on. A query does not have to be one of the keys.
7. **Turn on the causal mask.** Mask by roster order: student 0 may attend only to themselves, and the last student may attend to everyone. Same cards, same math — only the permission rule changed.

> **Warning:** Say this out loud before showing the matrix: a dark cell between two students is a statement about a handful of self-reported numbers — not about friendship, compatibility, or worth. It is the same reason a large attention weight is never a complete explanation of a model's decision.

**Day 2 homework:** [Assignment](ASSIGNMENT.md) Part 2 — implement the dot product, rule-based attention, fixed dot-product attention, and the visualization (TODOs 4–7), then answer the concept questions.

---

## <font color="#388bfd">What You Are Given</font>

The starter code is in [starter/](starter/) — four files. One contains all the TODOs; the rest are complete:

| File | Status | Role |
|---|---|---|
| [FixedAttention.java](starter/FixedAttention.java) | **TODO 1–7** | Every attention calculation in the chapter, plus provided validators |
| [AttentionFixtures.java](starter/AttentionFixtures.java) | Complete | The hand-written stat cards: the three-card table, GYM SOCK, the Order A retrieval sequence, and two example scoring rules |
| [ScoreRule.java](starter/ScoreRule.java) | Complete | The one-method interface a hand-written scoring rule implements |
| [Tester.java](starter/Tester.java) | Complete | Reproduces every worked trace on this page and runs the required tests |

Implement the TODOs in order, rerunning `Tester` after each — it reports each stage as it comes alive:

1. `uniformCausalWeights` — Stage 1's equal mixing (Day 1)
2. `stableSoftmax` — subtract max, exponentiate, normalize (Day 1)
3. `applyWeights` — the weighted blend of values (Day 1)
4. `dotProduct` — the matching loop (Day 2)
5. `ruleBasedCausalWeights` — Stage 2 with a `ScoreRule` (Day 2)
6. `dotProductCausalWeights` — Stage 3: scale, mask, softmax (Day 2)
7. `formatMatrix` — the labeled ASCII attention matrix (Day 2)

## <font color="#388bfd">Evidence Checkpoint</font>

Four observations your finished code must produce:

1. **Three matrices, one fixture.** Print uniform, rule-based, and dot-product attention matrices for the three-card table. Every row sums to approximately 1; every future entry is exactly 0.000.
2. **The spotlight beats the blur.** At position 2, the `sweet` feature is 0.667 under uniform mixing and 0.767 under dot-product attention. Print both.
3. **Retrieval works.** On the provided Order A retrieval sequence, your rule-based attention concentrates the earlier-position weight on the `Order A` / `pineapple` cards, not the `Order B` / `pepperoni` cards.
4. **The future is powerless.** Replacing the last card with GYM SOCK leaves the outputs at positions 0 and 1 identical.

## <font color="#388bfd">Required Tests</font>

- Each attention-matrix row sums to approximately one.
- All future-position weights are exactly zero.
- A one-token sequence returns a valid one-row matrix.
- Equal scores produce equal permitted weights.
- Adding the same constant to all permitted scores leaves softmax unchanged.
- A future input change leaves previous outputs unchanged.
- Known vectors produce known dot products.
- No input array is mutated.

## <font color="#388bfd">Answer Key</font>

**Set A.** 1: positions 0–3, each weighted $\frac{1}{4}$. 2: the position's own vector, weight 1. 3: each of the three cards gets $\frac{1}{3}$; two read `OLIVE`, so $\frac{2}{3}$. 4: no — position 3 is in position 1's future, and the mask removes it before anything is computed.

**Set B.** 1: `[4, 0, 4, 0]` (positions 0 and 2 match; position 1 differs; self is 0). 2: subtract 4 → `[0, −4, 0, −4]`; exponentiate → `[1, 0.0183, 1, 0.0183]`; normalize by 2.0366 → `[0.491, 0.009, 0.491, 0.009]`. 3: `[1/4, 1/4, 1/4, 1/4]` — Stage 1. 4: identical — the second list is the first plus 4, and softmax subtracts the max away. 5: a score can be any real number, so yes; a weight cannot — weights are nonnegative and sum to 1.

**Set C.** 1: 1.0 (only `topping` is shared). 2: 0.0. 3: 3.0. 4: 0.0 — the shared `sweet` slot contributed $1 \times (−1) = −1$, cancelling the `topping` slot; features can subtract as well as add. 5: $3.0 / \sqrt{4} = 1.5$.

**Set D.** 1: scaled scores `[0.5, 1.0]`; softmax → `[0.3775, 0.6225]`; $y_1 = [1.0, 0.3775, 0.6225, 0.0]$. 2: only $y_2$ — positions 0 and 1 never see position 2. 3: position 3 is position 1's future; the mask removed it before softmax, so it was never a small score — it was no score at all. 4: exactly 1 (approximately, in floating point); the row-sum required test.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** Attention is not a human act of noticing or understanding. It is a weighted data-routing calculation.

> **Misconception:** A large attention weight is not automatically a complete explanation of a model's decision.

More traps worth defusing now — each one caught a real learner:

| If you catch yourself thinking… | Remember |
|---|---|
| "The positions are being generated as we go." | The sequence is given. Attention reads; Chapter 2's sampler is off. |
| "All previous positions means everything in the training corpus." | Only the cards on the table — the context window. This chapter has no corpus at all. |
| "The query is built from the whole sentence." | The query comes from the current position alone; it is *compared against* every permitted key. |
| "A score of 4 means a probability of 4." | Scores are arbitrary real numbers. Only after softmax do they become weights summing to 1. |
| "Just dot the token identifiers from Chapter 1." | Identifiers are labels. Only feature vectors carry comparable meaning. |
| "Softmax gave PEPPERONI weight zero." | Softmax never outputs an exact zero for a permitted position. Exact zeros come only from the mask. |
| "Matrices are new math I haven't learned." | A matrix here is stacked stat cards; matrix multiplication is your dot-product loop run once per row. |

## <font color="#388bfd">Stretch Goals</font>

1. Interactive HTML attention heat map — color each attention-matrix cell by its weight. (The [Classmate Matrix](demos/classmate-matrix.html) source is a worked example; build yours from your own attention code.)
2. Distance-based attention penalty added to a `ScoreRule`.
3. Local attention that considers only the most recent `k` positions.
4. Attention temperature — a divisor that makes weight rows flatter or sharper.
5. Comparison between masked and unmasked attention on the same sequence.
6. Entropy measurement — a number describing how concentrated or diffuse each attention row is.
7. Rule-based retrieval challenge using synthetic sequences you author for a classmate.

---

You have built a useful spotlight, but every rule was written manually — you chose the +4, you chose the feature slots, you decided toppings matter. Modern models receive none of that. The next question is how numbers like these can adjust *themselves*, and it begins with a table that learns.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain what "position" means in this chapter, and why the three-card table involves no sampling and no training corpus?
- [ ] Can you compute the uniform causal weights at every position of a four-token sequence, and name which cards are mixed at position 2?
- [ ] Can you explain query, key, and value in one sentence each using the request slip, card face, and card contents — and say which single position the query comes from?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you run softmax on `[4.0, 0.0, 0.0]` by hand, including the max-subtraction step, and explain why the result — unlike the raw scores — can serve as mixing weights?
- [ ] Can you explain why token identifiers cannot be fed to the dot product but feature vectors can, using Chapter 1's identifiers-are-labels misconception?
- [ ] Can you compute the dot product of two labeled stat cards by hand and explain why a slot contributes only when both cards have something in it?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you trace the complete pipeline at position 2 of the three-card table — scaled scores, softmax, weighted blend — and show the `sweet` feature rising from 0.667 to 0.767 relative to uniform mixing?
- [ ] Can you prove that adding a constant to all permitted scores leaves softmax unchanged, and explain why all-equal scores reproduce Stage 1 exactly?
- [ ] Can you explain why raw dot products grow with vector dimension and how dividing by $\sqrt{d}$ repairs the problem before softmax?

---

[Assignment](ASSIGNMENT.md)

← [The Reader with One-Step Memory](../MarkovBaseline/) — Next: [A Table That Learns](../TrainableBigram/)
