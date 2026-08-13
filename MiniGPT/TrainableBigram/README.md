<div align="center">

# A Table That Learns
*<font color="#8b949e">Softmax, cross-entropy loss, and gradient descent on a trainable bigram table</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The Markov model counts transitions. The attention program follows hand-written rules. Neither one changes its internal behavior by examining how wrong a prediction was. The next machine begins with random scores, measures its own surprise, and nudges those scores in a direction that makes the observed answer less surprising.

## <font color="#388bfd">Question to Carry</font>

> **How can a collection of numerical scores improve itself from examples?**

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Parameter | A numerical value changed during training. |
| Weight | A parameter that scales or combines information. |
| Logit | An unrestricted score assigned to a possible output before softmax. |
| One-hot vector | A vector containing one `1` and otherwise `0`, used to identify one category. |
| Prediction distribution | The probabilities assigned to all possible next tokens. |
| Target | The correct next token in a training example. |
| Loss | A number measuring how poor a prediction was. |
| Cross-entropy loss | Negative logarithm of the probability assigned to the correct category. |
| Objective function | The quantity training attempts to minimize or maximize. |
| Derivative | A local rate of change of one quantity with respect to another. |
| Partial derivative | A rate of change with respect to one input while other inputs are treated as fixed. |
| Gradient | The collection of partial derivatives for all parameters. |
| Gradient descent | Updating parameters in the direction that reduces loss. |
| Learning rate | The multiplier controlling update size. |
| Stochastic Gradient Descent, abbreviated SGD | Gradient descent using one example or a small sample at each update. |
| Training step | One parameter-update operation. |
| Epoch | One conceptual pass through all training examples. |
| Numerical stability | Avoiding invalid or inaccurate floating-point calculations. |
| Finite difference | Estimating a derivative by making a small numerical change and measuring the result. |
| Gradient check | Comparing an implemented gradient with a finite-difference estimate. |

## <font color="#388bfd">Assignment Summary</font>

Replace the count-based bigram table with a trainable matrix:

$$W[\text{current token}][\text{possible next token}]$$

Each row contains logits. Softmax converts the row into probabilities. Cross-entropy measures the error. You implement the exact gradient for this simple model and train it using Stochastic Gradient Descent.

## <font color="#388bfd">Worked Narrative Example</font>

Suppose the current token is `rock`, and the vocabulary contains:

```text
[hard, layer, blue]
```

The model produces logits:

```text
[1.2, 0.1, -0.4]
```

After softmax:

```text
[0.659, 0.219, 0.122]
```

If the observed next token is `layer`, the model assigned only 0.219 probability to the correct answer.

The loss is:

$$-\log(0.219)$$

Training should reduce the `rock → layer` loss while considering all other possibilities.

## <font color="#388bfd">Core Gradient</font>

For output probability $p_i$ and target category $y$:

$$\frac{\partial L}{\partial z_i} = p_i - \mathbf{1}[i=y]$$

In plain language:

- The correct logit is pushed upward unless its probability is already one.
- Incorrect logits are pushed downward in proportion to their current probability.

## <font color="#388bfd">Detailed Requirements</font>

You must:

1. Initialize a logit matrix with small random values.
2. Retrieve one row for the current token.
3. Apply stable softmax.
4. Calculate cross-entropy loss.
5. Calculate the gradient of every logit in the selected row.
6. Accumulate gradients across a configurable number of examples.
7. Divide accumulated gradients by the number of examples.
8. Apply a learning-rate-controlled update.
9. Reset gradients after the update.
10. Report training and validation loss.
11. Compare learned probabilities with count-derived Markov probabilities.
12. Run numerical gradient checks.

## <font color="#388bfd">Suggested Interface</font>

```java
public final class TrainableBigramModel {
    private final double[][] logits;
    private final double[][] gradients;

    public double[] probabilities(int currentToken);
    public double loss(int currentToken, int targetToken);
    public void backward(int currentToken, int targetToken);
    public void step(double learningRate);
    public void zeroGradients();
}
```

## <font color="#388bfd">Required Tests</font>

- Softmax sums to one.
- Softmax is unchanged by adding a constant to every logit.
- Cross-entropy is near zero for a near-certain correct prediction.
- Loss is high for a near-zero correct probability.
- Analytical and finite-difference gradients agree.
- Only the selected row receives gradients.
- One gradient step lowers loss on a one-example dataset.
- Repeated training reduces average training loss.
- Fixed seed reproduces initialization and training results.

## <font color="#388bfd">Evidence Requirement</font>

Plot or tabulate:

```text
training step, training loss, validation loss
```

A Comma-Separated Values file, abbreviated **CSV**, is a plain text table in which values are separated by commas. You may export the trace as a CSV file without using a plotting library.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** The gradient does not directly tell the program the correct answer. It tells the program how a small parameter change would affect the measured loss.

## <font color="#388bfd">Stretch Goals</font>

1. Momentum, meaning an update that retains part of the previous update direction
2. Learning-rate decay
3. Mini-batch training, meaning simultaneous averaging over a small set of examples
4. Factorized bigram matrix: $W \approx EO$
5. Regularization, meaning an additional objective that discourages undesirable parameter values
6. Comparison of count-based and trainable bigram convergence
7. A training debugger that stops immediately on non-finite numbers

---

The table can learn, but every current token owns an isolated row. Knowledge learned for `basalt` does not help `granite`, even when the two appear in similar contexts. The machine needs shared internal features.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain the difference between a logit and a probability?
- [ ] Can you compute the cross-entropy loss by hand for the `rock → layer` worked example?
- [ ] Can you state what the learning rate controls and what happens when it is far too large?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement the softmax cross-entropy gradient $p_i - \mathbf{1}[i=y]$ and explain each term's sign?
- [ ] Can you verify your analytical gradient against a finite-difference estimate?
- [ ] Can you show that one gradient step lowers the loss on a one-example dataset?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why only the current token's row receives gradient in this model?
- [ ] Can you compare the converged trainable bigram's probabilities with the smoothed count-based probabilities and explain the relationship?
- [ ] Can you explain why gradient accumulation divides by the number of examples before the update?

---

← [The Hand-Built Spotlight](../FixedAttention/) — Next: [From Exact Symbols to Features](../ObjectNetwork/)
