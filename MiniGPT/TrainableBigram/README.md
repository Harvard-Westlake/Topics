<div align="center">

# A Table That Learns
*<font color="#8b949e">Softmax, cross-entropy loss, and gradient descent on a trainable bigram table</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The Markov model counts transitions. The attention program follows hand-written rules. Neither one changes its internal behavior by examining how wrong a prediction was. The next machine begins with random scores, measures its own surprise, and nudges those scores in a direction that makes the observed answer less surprising.

## <font color="#388bfd">Question to Carry</font>

> **How can a collection of numerical scores improve itself from examples?**

## <font color="#388bfd">Why This Chapter Is the Hinge</font>

Look at where the numbers inside your first two machines came from:

| Machine | Where its numbers came from | What it cannot do |
|---|---|---|
| Chapter 2 — the counter | Counting a training corpus | Improve beyond its counts |
| Chapter 3 — the spotlight | Rules you wrote by hand | Change a rule it was given |
| Chapter 4 — this table | A random start, then **its own gradient** | — this is the new ability |

The loop you build this week — *forecast, grade, measure the slope, nudge* — is the loop that trains every model for the rest of the course, including the transformer in Chapter 10. Later chapters make the machine being trained more elaborate; **the loop itself never changes again.** This is the only week it arrives one piece at a time, on a model small enough that you can watch all nine of its numbers move.

The chapter is two class periods. Each day ends with homework:

| Day | In class | Homework |
|---|---|---|
| 1 | The random table · one row as a forecast · grading one guess (loss and cross-entropy) · the wiggle experiment · the shortcut gradient · one step downhill | [Assignment](ASSIGNMENT.md) Part 1 — TODOs 1–4 plus problem sets A and B on paper |
| 2 | The order history as flashcards · the training loop: reset, accumulate, average, step · watching the loss fall · learning-rate experiments · the gradient check · reading the learned table | [Assignment](ASSIGNMENT.md) Part 2 — TODOs 5–7, the experiments, and the concept questions |

## <font color="#388bfd">The Order History — Read This First</font>

Everything in this chapter happens on one tiny, fixed world: the pizzeria's order history — the running record of what customers ordered, in order — already tokenized with a three-word vocabulary.

```text
token 0 = pizza      token 1 = pineapple      token 2 = pepperoni

the history reads:  pineapple pizza pineapple pizza pepperoni pizza ...
as tokens:          1, 0, 1, 0, 2, 0, ...
```

Three ground rules, mirroring Chapter 3's:

1. **The corpus is back.** Chapter 3 deliberately had no training data — you wrote every number by hand. This week training data returns: a **training history** (122 tokens) and a **validation history** (42 tokens), provided in the starter fixtures. Chapter 2's boundary rule is still law: validation data is scored, never trained on.
2. **Nothing is written by hand this week.** The table starts as small random numbers — junk — and from that moment on, only the training loop touches it. Your job is to build the loop, not the numbers.
3. **This is training, not generation.** The sampler stays off. Training reads a transition that *already happened* in the history, measures how surprised the model was, and nudges. Nothing is being predicted into existence. (After training, the finished table could be handed straight to Chapter 2's sampler — but that is a different activity, on a different day.)

Why a three-word toy? Because $3 \times 3 = 9$: the entire model is nine numbers, and every claim this page makes can be checked by eye. The archive corpus returns when the machinery is trusted.

## <font color="#388bfd">Vocabulary — Day 1</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Parameter | A numerical value changed during training. | A number with a screwdriver resting next to it |
| Weight | A parameter that scales or combines information. | A dial the machine turns on itself |
| Logit | An unrestricted score assigned to a possible output, before softmax. | Chapter 3's raw scores, wearing their standard name |
| Prediction distribution | The probabilities assigned to all possible next tokens. | One row of the table, softmaxed into a pie chart |
| Target | The correct next token in a training example. | The back of the flashcard |
| One-hot vector | A vector with a single `1` and otherwise `0`, identifying one category. | An answer sheet with one box filled in |
| Loss | A number measuring how poor one prediction was. | The golf score for one guess |
| Cross-entropy loss | Negative logarithm of the probability assigned to the correct category. | Chapter 2's surprise penalty, charged to a single guess |
| Negative log-likelihood (NLL) | The sum of $-\ln(p_{\text{target}})$ penalties over every prediction in a text. | Cross-entropy losses, totaled over a whole history |
| Objective function | The quantity training attempts to minimize. | The number the whole machine exists to shrink |
| Derivative | A local rate of change of one quantity with respect to another. | Wiggle this number, watch that one respond |
| Partial derivative | A rate of change with respect to one input while the others are held fixed. | One knob turned, every other knob taped down |
| Gradient | The collection of partial derivatives for all parameters. | The full list of slopes, one per knob |
| Finite difference | Estimating a derivative by making a small change and measuring the result. | The wiggle experiment, performed literally |

---

## <font color="#388bfd">Day 1 — One Guess: Graded, Then Nudged</font>

## <font color="#388bfd">The Same Table, a Different Filling</font>

Run Chapter 2's counting over the training history and you get a familiar table — and this chapter's fixtures do exactly that, for comparison later:

```text
Chapter 2's table (counts)              Chapter 4's table (logits, at birth)

             pizza   pine   pepp                     pizza    pine     pepp
pizza           0     40     20         pizza        0.017   -0.023    0.008
pineapple      41      0      0         pineapple   -0.011    0.031   -0.006
pepperoni      20      0      0         pepperoni    0.004   -0.019    0.012
```

Same shape: one row per current token, one column per possible next token. But the filling is different in two ways. First, the numbers at birth are **small random values** (the ones above are illustrative) — the table knows nothing. Second, and more important: they are not counts and they are not probabilities. They are **logits**, and each of the nine is a **parameter** — a number the training loop is allowed to change. When a parameter's job is to scale or combine information, it is also called a **weight**; for this model the two words point at the same nine numbers.

Why not just store probabilities and nudge those? Because a probability wears handcuffs: it must stay between 0 and 1, and its row must sum to exactly 1. Training is about to shove these numbers up and down hundreds of times, and re-fastening handcuffs after every shove is misery. So the table stores unrestricted scores, and converts a row to probabilities *on demand*:

> **Note:** You have already met unrestricted scores whose destiny is to become well-behaved weights: Chapter 3's attention scores, and the softmax that converted them. **Logit** is the standard name for such a score. The softmax here is the exact same three-step machine you built last week — subtract the max, exponentiate, normalize. It is the single most reused tool in this course.

## <font color="#388bfd">One Row Is a Forecast</font>

Standing at the token `pizza`, the model reads exactly *one* row of the table — the row labeled `pizza`, the row that token owns — and softmaxes it. Do that to pizza's newborn row from the table above:

```text
row for pizza (logits):   [ 0.017,  -0.023,   0.008 ]
subtract max (0.017):     [ 0.000,  -0.040,  -0.009 ]
exponentiate:             [ 1.0000,  0.9608,  0.9910 ]
divide by sum 2.9518:     [ 0.3388,  0.3255,  0.3357 ]
```

Read as a forecast: after `pizza`, the model says 34% `pizza`, 33% `pineapple`, 34% `pepperoni` — a shrug. This is the **prediction distribution**, and exactly like Chapter 2's smoothed rows, it is positive everywhere and sums to one. A nearly empty table like this one can only shrug: logits that are random but nearly zero softmax to nearly $\frac{1}{3}$ each, whichever row you read. Hold that thought — it becomes a free correctness test on Day 2.

A shrug is honest, but it gives a grader almost nothing to push against. To watch grading and nudging do something visible, the rest of the day follows one deliberately opinionated row. Suppose the row for `pizza` instead held `[1.2, 0.1, -0.4]`:

```text
row for pizza (logits):   [ 1.2,     0.1,    -0.4  ]
subtract max (1.2):       [ 0.0,    -1.1,    -1.6  ]
exponentiate:             [ 1.0000,  0.3329,  0.2019]
divide by sum 1.5348:     [ 0.6516,  0.2169,  0.1315]
```

Now the forecast has an opinion: 65% `pizza`, 22% `pineapple`, 13% `pepperoni`. That forecast is nonsense — the history never once shows `pizza pizza` — but the table has no way to know that yet. This **worked row** is the row every calculation below follows, and your Tester reproduces each of its numbers.

## <font color="#388bfd">Grading One Guess: the Loss</font>

The order history knows what actually came next. At this point in the history, the next token is `pineapple` — index 1. The true next token is called the **target**, and it is often written as a **one-hot vector** — an answer sheet with one box filled in:

```text
forecast p:        [ 0.6516,  0.2169,  0.1315 ]
target (one-hot):  [ 0,       1,       0      ]
```

The grade looks at exactly one number: the probability the model gave the truth. The model said 0.2169, and the penalty is Chapter 2's — the negative natural log of that one probability:

$$L = -\ln(p_{\text{target}}) = -\ln(0.2169) = 1.5284$$

That number is the **loss**: the grade for a single guess, near zero when the model was confident in the truth, huge when it called the truth nearly impossible. The objective of training is to minimize the loss — to steer the logits toward forecasts that make the observed answer less surprising. Because the loss is the quantity the whole process works to minimize, it is also called the **objective function**.

This particular recipe for the loss has a formal name — the one Chapter 2 promised you would meet again: **cross-entropy loss**. *Entropy* is the mathematician's word for surprise, and the *cross* records that two distributions are being compared: the model's forecast against the one-hot answer sheet. It is one single term of the **negative log-likelihood (NLL)** you built in Chapter 2 — the sum of $-\ln(p_{\text{target}})$ penalties over every prediction in a whole text. Chapter 2 charged that total to finished models as a report card; this chapter charges one term of it mid-training, because the loss is about to become a *steering signal*, not just a grade.

The dial, for intuition:

| $p_{\text{target}}$ | Loss $-\ln p$ | Reading |
|---:|---:|---|
| 1.00 | 0.000 | Perfect confidence in the truth |
| 0.90 | 0.105 | Nearly sure, nearly free |
| 0.50 | 0.693 | A coin flip's worth of doubt |
| 0.33 | 1.099 | The uniform model's score when $V = 3$ — that is $\ln 3$ |
| 0.10 | 2.303 | Badly surprised |
| 0.01 | 4.605 | Arrogantly wrong |

One quiet gift of the architecture: Chapter 2 needed **smoothing** to dodge $-\ln(0) = \infty$. This table cannot produce that disaster at all, because softmax never outputs an exact zero — the same fact you proved about attention weights in Chapter 3. The loss is always finite.

### <font color="#79c0ff">Check yourself — Set A</font>

Answers are in the [Answer Key](#answer-key) below. Do these on paper before moving on.

1. A row of logits reads `[0, 0, 0]`. What forecast does it make, and what loss does it pay no matter which token the log shows next?
2. Can a logit be $-3.8$? Can a probability? Can a loss?
3. From Chapter 3 you already know softmax of `[2, 1, 0]` is `[0.6652, 0.2447, 0.0900]`. If the target is index 2, what is the loss?
4. One guess gave the truth $p = 0.5$; another gave it $p = 0.25$. Compute both losses. What pattern do you notice about halving?

## <font color="#388bfd">The Wiggle Experiment</font>

The loss is 1.5284, and the worked row's three logits `[1.2, 0.1, -0.4]` are the numbers responsible. Which direction should each move to shrink it? Do not philosophize — **measure**.

First, give the three logits names: write them $z_0, z_1, z_2$, one per column of the row —

```text
z0 = 1.2   pizza's logit
z1 = 0.1   pineapple's logit
z2 = -0.4  pepperoni's logit
```

The target was `pineapple`, so $z_1$ is the logit of the truth — and the experiment asks one question about it: *if $z_1$ were a touch bigger or a touch smaller, would the loss shrink?* You cannot answer that by staring. The number passes through softmax before it reaches the loss, and softmax stirs all three logits together. The only way to know is to try it, under two rules that keep the measurement honest:

- **Move one number at a time; freeze the rest.** $z_0$ and $z_2$ stay exactly where they are. If all three logits moved at once and the loss changed, you could not tell which mover deserved the credit or the blame. Freezing the others isolates $z_1$'s private effect on the loss — and each logit will get its own turn.
- **Nudge tiny, in both directions.** Raise $z_1$ by $0.01$ and recompute the entire pipeline — softmax, then loss. Put it back, lower it by $0.01$, and recompute again. Comparing the two runs gives both the direction and the rate of the response, and keeping the nudge tiny keeps the answer about *this* spot — the response can be different somewhere else.

```text
z1 = 0.11  ->  softmax  ->  loss = 1.52056     (raising z1 helped)
z1 = 0.09  ->  softmax  ->  loss = 1.53622     (lowering z1 hurt)

slope at z1  =  (1.52056 - 1.53622) / 0.02  =  -0.783
```

The loss falls about $0.783$ per unit of raise, *at this location*. Now give $z_0$ (the `pizza` logit) its turn — $z_1$ and $z_2$ frozen this time: its slope comes out to $+0.6516$ — raising it makes things worse. Every number now has a measured direction.

Names, now that you have done the thing:

- A **derivative** is that local rate of change — wiggle one number, watch another respond.
- A **partial derivative** is a derivative taken while every *other* knob is taped down, exactly as you just did. Written $\frac{\partial L}{\partial z_1}$, read "the partial of $L$ with respect to $z_1$".
- The **gradient** is the whole list of slopes, one per parameter: here, $[+0.6516, -0.783, +0.132]$.
- Measuring a slope by literally nudging and recomputing is a **finite difference**.

Notice what the slope did **not** tell you. It never said "the answer is pineapple." It said: *if this one number moves a little, here is how the loss responds.* That is all a gradient ever says.

And notice the cost. Three knobs took six full recomputations. A GPT-class model has hundreds of billions of knobs; two full evaluations per knob per example is impossible. The slopes have to come from a formula.

## <font color="#388bfd">The Shortcut: Prediction Minus Answer Sheet</font>

For this exact pipeline — one row of logits, softmax, cross-entropy — the slope of the loss with respect to each logit in the used row has a closed form, and it is almost insultingly simple:

$$\frac{\partial L}{\partial z_i} = p_i - \mathbf{1}[i = y]$$

Here $y$ is the target's index, and $\mathbf{1}[i=y]$ is $1$ when $i$ is the target and $0$ otherwise — which is precisely the one-hot answer sheet. In words: **the gradient is the prediction distribution minus the one-hot target.** Apply it to the worked row, target index 1:

```text
prediction p:      [ 0.6516,   0.2169,   0.1315 ]
one-hot target:    [ 0,        1,        0      ]
gradient p - 1:    [ 0.6516,  -0.7831,   0.1315 ]
```

Compare with the wiggle experiment: $-0.783$ and $+0.6516$, reproduced exactly, with no wiggling. Read the formula out loud:

> **The correct logit is pushed upward unless its probability is already one. Incorrect logits are pushed downward in proportion to their current probability.**

Three things worth saying about it:

- **The signs are the story.** The target's entry is $p_y - 1$, which is negative until $p_y = 1$ — and you are about to *subtract* the gradient, so a negative slope means that logit gets raised. Wrong answers carry $p_i > 0$, so they always get pushed down — hardest when the model was most confident in them.
- **The entries sum to zero.** The $p_i$ sum to 1, and you subtract a single 1. Belief is conserved: whatever the wrong answers lose, the right answer gains.
- **Only the used row gets slopes.** The other rows never touched this prediction, so this example says nothing about them. Hold that thought too.

Where does the formula come from? Calculus — the chain rule pushed through the logarithm and the softmax. Deriving it is a stretch goal, not a requirement; *using* it requires no calculus at all. But you should not take a formula on faith: on Day 2 you will make the wiggle experiment the **referee**, and require the two to agree to six decimal places. That referee has a name — the gradient check — and it is a required test.

## <font color="#388bfd">One Step Downhill</font>

A slope plus a direction is an instruction. Move every logit a small step *against* its slope:

```java
newLogit = oldLogit - learningRate * slope;
```

This is **gradient descent**, and the multiplier is the **learning rate** — the stride length. Take one step on the worked row with learning rate $0.5$:

```text
old row:        [ 1.2,      0.1,      -0.4    ]
gradient:       [ 0.6516,  -0.7831,    0.1315 ]
step (lr 0.5):  [ 1.2 - 0.3258,  0.1 + 0.3916,  -0.4 - 0.0658 ]
new row:        [ 0.8742,   0.4916,   -0.4658 ]

new forecast:   [ 0.5144,   0.3509,    0.1347 ]
new loss:       -ln(0.3509) = 1.0474
```

The loss fell: $1.5284 \rightarrow 1.0474$. Look closely at what one step did and did not do. The truth's probability rose from $0.2169$ to $0.3509$ — but `pizza` still leads the forecast. **A step is a nudge, not a correction.** The model was not told the answer and did not jump to it; it moved every number a little in the direction that made the observed answer less surprising. Training is thousands of such nudges.

The learning rate is a number *you* choose — Chapter 2 gave you the word for that: a **hyperparameter**, tuned on validation data, never on test data. Day 2 shows exactly what happens when you choose it badly.

### <font color="#79c0ff">Check yourself — Set B</font>

1. A row's forecast is $[0.6516, 0.2169, 0.1315]$ and the target is index 1. Write the gradient without computing anything new.
2. In your answer to problem 1, why is entry 1 the only negative number? What will *subtracting* a negative slope do to that logit?
3. Add up the three gradient entries. What total must they always give, and why?
4. A different guess put $p = 0.98$ on the truth. What is the target's slope, and what does its small size mean the update will do?
5. Wiggle time: with the worked row, nudging $z_2$ gives $L(z_2 + 0.01) = 1.52970$ and $L(z_2 - 0.01) = 1.52707$. Compute the slope. Which entry of the shortcut formula did you just confirm?

**Day 1 homework:** [Assignment](ASSIGNMENT.md) Part 1 — implement the stable softmax, the forecast, the loss, and the gradient (TODOs 1–4), and bring problem sets A and B worked on paper.

---

## <font color="#388bfd">Vocabulary — Day 2</font>

| Term | Definition | Picture to hold |
|---|---|---|
| Gradient descent | Updating parameters in the direction that reduces loss. | Walking downhill in fog, one small step at a time |
| Learning rate | The multiplier controlling update size. | Stride length |
| Training step | One parameter-update operation. | One turn of the crank |
| Batch | The set of examples contributing to one update. | A handful of flashcards graded together |
| Gradient accumulation | Adding each example's gradient into a running total before updating. | Slopes poured into one bucket, then averaged |
| Backward pass | Computing the gradient by walking from the loss back to the parameters. | The forward pipeline, traveled in reverse to assign blame |
| Epoch | One conceptual pass through all training examples. | Once through the whole deck |
| Stochastic Gradient Descent (SGD) | Gradient descent using a random example or small batch per update. | Descent steered by random handfuls |
| Gradient check | Comparing an implemented gradient against a finite-difference estimate. | The wiggle experiment, hired as referee |
| Numerical stability | Avoiding invalid or inaccurate floating-point results. | No `Infinity`, no `NaN`, no overflow |

## <font color="#388bfd">Day 2 — A Hundred Guesses: The Training Loop</font>

## <font color="#388bfd">Every Adjacent Pair Is a Flashcard</font>

Day 1 processed one example. The training history contains 122 tokens, and **every adjacent pair is one training example**: the current token is the front of a flashcard, the target is the back. That is 121 flashcards — and the validation history holds 41 more that the table is never allowed to learn from.

The deck is not balanced, and that matters later:

| Flashcard front | How many cards | The backs |
|---|---:|---|
| `pizza` | 60 | `pineapple` 40 times, `pepperoni` 20 times |
| `pineapple` | 41 | `pizza` every time |
| `pepperoni` | 20 | `pizza` every time |

Notice `pizza`'s cards *disagree with each other* — forty say one thing, twenty say another. No table can be right every time; the best any model can do on this deck is match the mixture. Remember that when you watch the loss refuse to reach zero.

## <font color="#388bfd">The Loop: Reset, Accumulate, Average, Step</font>

One **training step** has a five-beat rhythm, built entirely from your TODOs — and in this chapter the trainer is yours to write as well: one pass through the rhythm is `stochasticGradientDescentStep` (TODO 8), and the `repeat 300 times` around it is the loop you write inside `train` (TODO 9):

```text
repeat 300 times:
    zeroGradients()                              reset      - wipe the gradient bucket
    24 times:                                    batch      - 24 flashcards graded together
        draw a random flashcard                               (a current token and its target)
        accumulateGradients(current, target)     accumulate - add this card's gradient,
                                                              p minus one-hot, to the bucket
    step(learningRate)                           average    - divide the bucket by 24, then
                                                 step       - stride downhill against the slope
```

One function in there deserves a gloss: `accumulateGradients` computes Day 1's shortcut gradient — `p` minus one-hot — for a single flashcard and adds it to the bucket. The name says exactly what the method does, but the operation also has a standard name worth learning now. Computing the loss runs the pipeline *forward*: row → softmax → probability of the target → loss. Computing the gradient walks the same road in reverse — from the loss back to the logits that caused it — so every training library calls this the **backward pass** and names the method `backward`; Chapter 6 will use that name. Forward makes the prediction; backward finds out what to blame.

The 24 flashcards graded together are a **batch**, and pouring their gradients into one running total is **gradient accumulation**. Because the flashcards are drawn *at random*, this is **Stochastic Gradient Descent** — stochastic is a formal word for random. With 121 flashcards and 24 per step, about five steps consume one deck's worth — one **epoch**, though with random draws the term is a unit of accounting rather than a strict pass.

Two design choices in the loop deserve a *why*:

- **Why divide by the number of examples before stepping?** The batch votes. Twenty-four gradients summed would be one gradient roughly 24 times louder — and then changing the batch size would secretly change the stride length. Averaging keeps the learning rate meaning what it says, whatever the batch size. (Your `step` does this division; the Tester checks it.)
- **Why reset to zero after every update?** A gradient is a snapshot: it describes the table *as it was* when `accumulateGradients` ran. The moment `step` moves the logits, every accumulated slope is stale. Forgetting `zeroGradients` is the classic training bug — old slopes contaminate every future step, and the loss chart goes haywire while each individual method still looks correct.

### <font color="#79c0ff">Check yourself — Set C</font>

One full training step by hand, on a one-card batch. An empty row for `pizza` reads `[0, 0, 0]`; the flashcard says `pizza -> pepperoni` (index 2); the learning rate is $0.3$.

1. What is the forecast, and what loss does the card charge?
2. Write the gradient.
3. Write the row after the step.
4. Compute the new forecast and the new loss, and confirm the step helped.

## <font color="#388bfd">Watching It Learn</font>

The `Trainer` prints a loss trace as it works — two loss columns every 30 steps, in CSV form (Comma-Separated Values: a plain-text table with commas between the columns; paste it into any spreadsheet, no plotting library required).

The two columns are the same measurement pointed at two different decks — a Chapter 2 distinction worth restating before the numbers. Your `averageLoss` (TODO 7) grades every adjacent pair in a history and averages the charges. Aimed at the training history — the 121 flashcards the loop practices on — it produces the **training loss**. Aimed at the validation history — the 41 flashcards the table is never allowed to learn from — it produces the **validation loss**. Training loss answers *how well does the table fit the cards it practices on?* Validation loss answers the question that actually matters: *does that learning hold on orders it has never seen?* Practice test, then real exam — and Chapter 2's boundary rule is what keeps the exam honest: validation data is scored, never trained on.

Everything is seeded, so this is not *an example* of the output — it is *the* output. Your run must reproduce it digit for digit:

```text
step,training loss,validation loss
0,1.0987,1.0990
30,0.4645,0.4668
60,0.3911,0.3932
90,0.3662,0.3681
120,0.3536,0.3556
150,0.3448,0.3454
180,0.3404,0.3422
210,0.3381,0.3373
240,0.3339,0.3354
270,0.3316,0.3317
300,0.3300,0.3311
```

Three observations, each load-bearing:

1. **Step 0 is $\ln 3$.** Before any training, the loss is $1.0987 \approx \ln 3 = 1.0986$. A nearly empty table's near-zero random logits softmax to nearly uniform rows — **a nearly empty table is the uniform model in disguise**, and Chapter 2 told you exactly what the uniform model scores: $\ln V$, perplexity $V$. This is a free correctness test. If your step-0 line prints anything else, the bug is in your code, not in the randomness.
2. **The loss falls fast, then flattens near 0.33 — not near 0.** The floor is real: `pizza`'s flashcards genuinely disagree (40 vs 20), so the best possible average loss on this history is about $0.3156$. The remaining loss is the deck's own uncertainty, and no model, however trained, can go below it. Zero loss is not the goal — the floor is. (The same is true of every real language model: English itself has a floor.)
3. **The validation column hugs the training column.** Both histories come from the same tiny process, so a table that learns one fits the other. Keep this pair of columns in mind: in Chapter 11, watching them *separate* becomes the most important diagnostic in the course — the sign that a model has begun memorizing its training data instead of learning the process behind it.

## <font color="#388bfd">Learning-Rate Sensitivity</font>

Every run above used learning rate $0.5$. How much did that choice matter? This section's point: **with the model, the data, and the code all held fixed, the learning rate alone decides whether training crawls, converges, or thrashes.** The provided bench in `Trainer` demonstrates it by rerunning the same 300 steps at three settings — same table, same flashcards, same seeds; only the stride changes:

| Learning rate | Final training loss | What the trace looks like |
|---:|---:|---|
| 0.01 | 0.7855 | Too cold: a smooth crawl — after 300 steps, still miles above the floor |
| 0.5 | 0.3300 | Settles onto the floor |
| 20 | 0.4992 | Too hot: chaos — 0.67 → 0.81 → 1.18 → 0.37 → … → 1.82 → 0.50 — never settles |

Too cold costs nothing but your afternoon: every step is correct, just tiny. Too hot is the failure worth understanding — the loss *bounces*, sometimes landing worse than the untrained table. Here is the failure in miniature, computable by hand. An empty row `[0, 0, 0]`, one flashcard `pizza -> pineapple`, learning rate 20:

```text
gradient:            [ 1/3,  -2/3,   1/3 ]
one giant step:      [ -6.67,  13.33,  -6.67 ]
new forecast:        [ ~0.000000002,  ~0.999999996,  ~0.000000002 ]
```

One example, and the table is now more certain that `pineapple` follows `pizza` than you are that the sun will rise. The very next flashcard that says `pizza -> pepperoni` — a third of them do — is charged $-\ln(0.000000002) \approx 20.0$. An untrained table would have paid $1.0986$. The giant stride replaced honest ignorance with confident error, and the next conflicting example punishes it savagely; repeat forever and the row lurches from one overconfidence to the other. That is the bouncing in the table above.

## <font color="#388bfd">The Referee: the Gradient Check</font>

Here is an unsettling fact about training bugs: an `accumulateGradients` with a wrong sign, a swapped index, or a forgotten term often *still sort of trains* — the loss drifts down, slowly and mysteriously badly, and nothing crashes. Silent wrongness is the default failure mode of gradient code everywhere.

The referee is the wiggle experiment from Day 1, applied automatically. For every logit in the worked row, the Tester nudges by $h = 0.0001$ in both directions, recomputes the loss, forms the finite-difference slope, and compares it against what your `accumulateGradients` computed:

$$\text{numerical slope} = \frac{L(z_i + h) - L(z_i - h)}{2h}$$

Formula and experiment must agree to within $10^{-6}$; a correct implementation lands near $10^{-10}$. This **gradient check** is a required test, and the habit generalizes: every serious training system ever built includes one.

> **Warning:** A passing gradient check certifies exactly one thing — that your slope formula matches reality. It says nothing about whether the model is good, the learning rate sane, or the data sensible. It is a referee, not a coach.

## <font color="#388bfd">The Table It Learns</font>

After 300 steps, the Tester prints the learned table beside Chapter 2's counting, and this is the punchline of the week:

```text
row           learned from gradients        counted from the history
pizza         [0.009, 0.676, 0.315]         [0.000, 0.667, 0.333]
pineapple     [0.986, 0.007, 0.007]         [1.000, 0.000, 0.000]
pepperoni     [0.970, 0.015, 0.015]         [1.000, 0.000, 0.000]
```

**Gradient descent rediscovered counting.** Nobody counted — the table never saw two flashcards at once, never kept a tally, and was steered by nothing but *nudge away from surprise*, 300 times. Yet it converged to the same forecasts Chapter 2 computed with division. For this simple model, the count frequencies genuinely are the loss-minimizing answer, and the gradient walked straight to them.

Two details in the comparison reward a close look:

- **No exact zeros, no exact ones.** The counted table says `pizza -> pizza` is *impossible* — probability $0.000$, the very overconfidence Chapter 2 needed smoothing to repair. The learned table says $0.009$: rare, not impossible. Softmax cannot output an exact zero (Chapter 3's fact, now doing Chapter 2's job), so a trained table arrives *pre-hedged*. To push a probability all the way to 0 or 1, a logit would have to reach infinity.
- **If counting gives the same answer, why bother with gradients?** Because counting worked only because this model *is* a lookup table — every parameter maps to one countable event. Chapter 5's network computes its forecasts through shared internal machinery, and no count on Earth fills in those numbers. Gradient descent does not care what the machine looks like inside, so long as slopes exist. **This is the last model in the course simple enough to check against a count — which is exactly why it is the right place to build trust in the method.**

## <font color="#388bfd">Every Row Learns Alone</font>

One more experiment is hiding in that comparison table. Both topping rows learned the same true rule — `pizza` always follows. But look at the confidence:

```text
P(pizza | pineapple) = 0.986     learned from 41 flashcards
P(pizza | pepperoni) = 0.970     learned from 20 flashcards
```

Same rule, same training run, different certainty — because `pepperoni`'s row received half as many nudges. **Nothing either row learned helped the other, ever.** A row is updated only when its token is the *front* of the flashcard; appearing on the back teaches a row nothing (problem D1 makes you prove this to yourself).

Now scale the flaw. A real vocabulary has 50,000 tokens, so this table would need $50{,}000^2 = 2.5$ **billion** parameters — and a rare word's row, seen a handful of times, would stay nearly random forever, no matter how many times its close cousins were trained. The table has no concept of *cousins*. That missing concept is where the course goes next.

### <font color="#79c0ff">Check yourself — Set D</font>

1. A batch contains three flashcards: `pizza -> pineapple`, `pineapple -> pizza`, `pizza -> pepperoni`. Which rows of the gradient table are nonzero when `step` runs, and why is `pepperoni`'s row *not* one of them?
2. A row is trained forever on a deck where two thirds of its flashcards say `pineapple` and one third say `pepperoni`. Where do its probabilities settle, and why can its loss never reach zero?
3. With 121 flashcards and a batch of 24, roughly how many steps make one epoch — and why is "epoch" only approximate in our loop?
4. A classmate reports final training loss $0.0001$ on this order history. Without reading a line of their code, what do you know, and what is the likeliest kind of bug?

**Day 2 homework:** [Assignment](ASSIGNMENT.md) Part 2 — implement the update, the reset, and the evaluation (TODOs 5–7), run the training and learning-rate experiments, and answer the concept questions.

---

## <font color="#388bfd">What You Are Given</font>

The starter code is in [starter/](starter/) — four files. Two contain TODOs; the rest are complete:

| File | Status | Role |
|---|---|---|
| [TrainableBigramModel.java](starter/TrainableBigramModel.java) | **TODO 1–7** | The table: its forecasts, its loss, its gradient, its update |
| [TrainingData.java](starter/TrainingData.java) | Complete | The training and validation histories, plus Chapter 2's counting for the comparison |
| [Trainer.java](starter/Trainer.java) | **TODO 8–9** | The training itself: one SGD step and the loop that repeats it (the reporting and the experiment bench are provided — run `java Trainer` once the Tester passes) |
| [Tester.java](starter/Tester.java) | Complete | Reproduces every worked trace on this page and runs the required tests |

The model's TODOs follow one flashcard through its life, in the order the chapter taught it — **Forecast** the next token, **Grade** the guess, **Measure** the slope, **Nudge** the table — plus the machinery around them. Each stage is strict about what it may touch: Forecast, Grade, and the Report card only *read* the table; Measure writes only the gradient bucket; Nudge is the only method that moves a logit. The Tester checks those boundaries as seriously as the arithmetic.

Implement the TODOs in order, rerunning `Tester` after each — unimplemented stages report as `TODO`, not `FAIL`:

1. `stableSoftmax` — shared machinery: Chapter 3's three steps, rebuilt here (Day 1)
2. `probabilities` — Forecast: one row, read as a prediction (Day 1)
3. `loss` — Grade: cross-entropy for one flashcard (Day 1)
4. `accumulateGradients` — Measure: pour `p` minus one-hot into the used row (Day 1)
5. `step` — Nudge: average the accumulated gradients, stride downhill (Day 2)
6. `zeroGradients` — Reset: wipe the bucket between updates (Day 2)
7. `averageLoss` — Report: grade a whole history without training on it (Day 2)
8. `stochasticGradientDescentStep` — in `Trainer`: Reset, Measure a random batch, one averaged Nudge (Day 2)
9. the loop in `train` — repeat the step, reporting the CSV trace on schedule (Day 2)

## <font color="#388bfd">Evidence Checkpoint</font>

Five observations your finished code must produce:

1. **The worked row reproduces.** Softmax `[0.6516, 0.2169, 0.1315]`, loss `1.5284`, gradient `[0.6516, -0.7831, 0.1315]`, and one step at learning rate 0.5 landing on loss `1.0474`.
2. **The anchor holds.** A nearly empty table (seed 7) scores average training loss `1.0987` — $\ln 3$ to three decimals — before any training.
3. **The trace reproduces.** Your CSV matches the lesson's digit for digit, both columns falling from `1.0987 / 1.0990` to `0.3300 / 0.3311`.
4. **The tables converge.** Learned probabilities land within a few hundredths of the counted frequencies — with no exact zeros anywhere.
5. **The referee is satisfied.** The gradient check's worst analytical-versus-wiggle gap prints below $10^{-6}$.

## <font color="#388bfd">Required Tests</font>

`Tester` covers all of these — confirm every one reports `PASS`:

- Softmax sums to one, survives huge logits without overflow, and is unchanged by adding a constant to every logit.
- Cross-entropy is near zero for a near-certain correct prediction, and large when the truth was called nearly impossible.
- Analytical and finite-difference gradients agree at every logit.
- Gradient entries sum to zero, and only the current token's row receives them.
- `accumulateGradients` changes no logits; `step` moves no row that accumulated nothing.
- Accumulated gradients are averaged, not summed — and `step` with nothing accumulated is refused.
- One gradient step lowers the loss on a one-example dataset.
- `averageLoss` moves no logits and touches no gradients — grading is not training.
- One seeded SGD step makes exactly one draw per flashcard and lands the average training loss on `1.0279`.
- Training reduces both training and validation loss, and the learned table matches the counted one.
- A fixed seed reproduces the initial table and the entire training run exactly.

## <font color="#388bfd">Answer Key</font>

**Set A**

1. The uniform forecast $[\frac{1}{3}, \frac{1}{3}, \frac{1}{3}]$; loss $\ln 3 = 1.0986$ no matter which target the history shows.
2. A logit can be any real number, so yes. A probability cannot leave $[0, 1]$. A loss is $-\ln p$ with $p \le 1$, so it can never be negative — it runs from 0 upward.
3. $-\ln(0.0900) = 2.41$.
4. $-\ln(0.5) = 0.693$ and $-\ln(0.25) = 1.386$ — halving the truth's probability *adds* a constant $0.693$ to the loss; logarithms turn ratios into sums.

**Set B**

1. $[0.6516, -0.7831, 0.1315]$ — the forecast with 1 subtracted at the target.
2. It is the only entry where the answer sheet holds a 1, and $p - 1 < 0$; subtracting a negative slope *raises* that logit.
3. Zero, always — the $p_i$ sum to 1 and exactly one 1 is subtracted.
4. $0.98 - 1 = -0.02$; the update will barely move it — a nearly satisfied prediction generates almost no pressure.
5. $(1.52970 - 1.52707) / 0.02 = 0.1315$ — the third entry, confirming that a wrong answer's slope equals its probability.

**Set C**

1. Forecast $[\frac{1}{3}, \frac{1}{3}, \frac{1}{3}]$; loss $\ln 3 = 1.0986$.
2. $[\frac{1}{3}, \frac{1}{3}, -\frac{2}{3}]$.
3. $[-0.1, -0.1, 0.2]$.
4. New forecast $[0.2985, 0.2985, 0.4030]$; new loss $-\ln(0.4030) = 0.9089 < 1.0986$ — the step helped.

**Set D**

1. Rows `pizza` and `pineapple` — they appeared as flashcard *fronts*. `pepperoni` appeared only as a back (a target), and targets receive no row update; the gradient lands in the row that made the prediction.
2. At the mixture $[\,0, \frac{2}{3}, \frac{1}{3}]$ (approached, never exactly reached); the loss floor is the deck's own disagreement — no single forecast can satisfy conflicting cards.
3. About 5 steps ($121 / 24$); the loop draws cards at random, so some cards repeat and others are skipped in any given "pass".
4. The number is impossible — the deck's disagreement sets a floor near $0.3156$, so a loss of $0.0001$ means the *measurement* is broken (evaluating the wrong thing, scoring the current token instead of the next, or training on the data being scored), not that the model is brilliant.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** The gradient does not tell the program the correct answer. It tells the program how a small parameter change would affect the measured loss. The target enters through the loss; the gradient is its messenger, not an answer key.

More traps worth defusing now:

| If you catch yourself thinking… | Remember |
|---|---|
| "Logits are just probabilities before rounding." | Logits are unrestricted scores — any real number. Only softmax turns a row into a distribution. |
| "Training rewrites the whole table each step." | Only rows that appeared as a flashcard *front* in the batch move. Everything else is untouched. |
| "A bigger batch means bigger steps." | `step` divides by the example count. Averaging keeps the stride independent of batch size. |
| "The goal is loss zero." | The deck's own disagreement sets a floor (0.3156 here). Below-floor numbers mean broken measurement, not brilliance. |
| "The learned table should exactly equal the count table." | It converges *toward* raw frequencies but softmax can never emit an exact 0 or 1 — the table arrives pre-hedged. |
| "The gradient check passed, so the model is good." | It certifies the slope formula only — not the learning rate, the data, or the model. |
| "This chapter is generating pizza orders." | The sampler is off. Training reads transitions that already happened and adjusts numbers. |
| "Epoch and step are the same thing." | A step is one update; an epoch is one deck's worth of examples — here about five steps. |
| "Evaluating the model runs the whole lifecycle — forecast, grade, measure, nudge." | `averageLoss` only grades. Measuring slopes or nudging logits while evaluating would train on the validation history — exactly what Chapter 2's boundary rule forbids. |

## <font color="#388bfd">Stretch Goals</font>

1. **Momentum** — an update that retains a fraction of the previous update's direction; watch it smooth the too-hot trace.
2. **Learning-rate decay** — start bold, finish careful; can you beat 0.3300 in 300 steps?
3. **Batch-size study** — rerun with batch 1 and batch 121 (the full deck); compare the traces' noisiness and explain it.
4. **Factorized table** — replace the $V \times V$ table with two skinny matrices $W \approx E\,O$ and count the parameters; you have just invented the reason for Chapter 5.
5. **Regularization** — add a penalty that discourages extreme logits, and watch what it does to the near-zero entries.
6. **Convergence race** — how many training steps until every learned probability is within 0.01 of the counted one?
7. **A training debugger** — halt the instant any logit, gradient, or loss becomes `NaN` or infinite, and report where.
8. **Derive the shortcut** — push the chain rule through $-\ln(\text{softmax})$ and prove $p_i - \mathbf{1}[i=y]$.
9. **Close the loop** — hand your trained table to Chapter 2's sampler and generate a fresh order history with a fixed seed.

---

The table can learn, but every current token owns an isolated row. `pineapple` and `pepperoni` both demand `pizza` next, yet each row had to discover that separately, and the one with fewer flashcards will always know it less well. In the archive's full vocabulary the same isolation strikes `mushroom` and `olive` — twins that appear in near-identical sentences ("extra mushroom, light sauce" / "extra olive, light sauce") and can share nothing. The machine needs shared internal features.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain the difference between a logit and a probability, and why the table stores the unrestricted one?
- [ ] Can you compute the worked example by hand — softmax of `[1.2, 0.1, -0.4]`, then the loss for target `pineapple` — and land on 1.5284?
- [ ] Can you state what the learning rate controls, and describe what the loss trace looks like when it is far too small and far too large?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you write the gradient $p_i - \mathbf{1}[i=y]$ for any row and target, explain each entry's sign, and say why the entries always sum to zero?
- [ ] Can you verify an analytical gradient with a finite-difference wiggle — and state precisely what a passing gradient check does and does not certify?
- [ ] Can you execute one full training step by hand (Set C) and show the loss fell?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why only the current token's row receives gradient, and what that means for rare tokens in a 50,000-word vocabulary?
- [ ] Can you explain the relationship between the converged table and the count-based table — including why the learned one can never contain an exact zero, and which Chapter 2 and Chapter 3 facts that echoes?
- [ ] Can you explain why a fresh random table's loss must be $\ln V$, and use the loss-floor argument to debunk an impossibly good loss report?

---

[Assignment](ASSIGNMENT.md)

← [The Hand-Built Spotlight](../FixedAttention/) — Next: [From Exact Symbols to Features](../ObjectNetwork/)
