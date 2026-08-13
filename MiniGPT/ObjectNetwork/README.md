<div align="center">

# From Exact Symbols to Features
*<font color="#8b949e">Token embeddings and an object-oriented neural network — forward pass only</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The trainable bigram table treats every token as a separate universe. If "basalt" and "granite" tend to appear in similar grammatical environments, the table has no direct way to share that discovery. The next machine will describe each token using a small collection of learned numerical features and combine those features through a network of connections.

## <font color="#388bfd">Question to Carry</font>

> **How can different tokens share useful predictive features?**

## <font color="#388bfd">Pedagogical Role</font>

You first represent a network as familiar objects, then discover that the same traversal is a dot product or matrix operation.

Object-oriented representation is a **concrete bridge**, not a permanent substitute for the mathematical structure.

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Representation | Numerical information used internally to stand for an input. |
| Embedding | A learned vector associated with a discrete item such as a token. |
| Embedding table | A table containing one embedding vector per token. |
| Neuron or unit | A mathematical component that combines inputs and produces one output. It is only loosely inspired by biology. |
| Connection | A weighted link from one unit to another. |
| Bias | A trainable constant added to a weighted sum. |
| Weighted sum | A sum of inputs multiplied by their associated weights. |
| Linear transformation | A weighted combination of numerical inputs. |
| Activation function | A function applied after a weighted sum. |
| Nonlinearity | A function that prevents the entire network from collapsing into one linear transformation. |
| Rectified Linear Unit, abbreviated ReLU | The function $\max(0,x)$. |
| Layer | A collection of units operating at the same conceptual stage. |
| Hidden layer | An internal layer between input and output. |
| Forward pass | Calculation from input through the network to its output. |
| Multi-Layer Perceptron, abbreviated MLP | A feed-forward neural network containing one or more learned layers. |
| Fixed context | A predetermined number of earlier tokens supplied to the model. |
| Concatenation | Joining vectors end to end. |
| Shape | The dimensions of an array or matrix. |

## <font color="#388bfd">Assignment Summary</font>

Build a fixed-context neural language model using explicit `Neuron`, `Connection`, and `Layer` objects.

This assignment performs only the forward pass. A small set of instructor-provided weights allows you to verify the computation before training is introduced.

## <font color="#388bfd">Proposed Architecture</font>

For context length three:

```text
token at t-3 ─┐
token at t-2 ─┼─ embedding lookup
token at t-1 ─┘
        ↓
concatenate embeddings
        ↓
hidden weighted layer
        ↓
Rectified Linear Unit
        ↓
output weighted layer
        ↓
one logit per vocabulary token
```

## <font color="#388bfd">Object-Oriented Representation</font>

```java
public final class Connection {
    private final Neuron source;
    private final Neuron destination;
    private double weight;
}

public final class Neuron {
    private double value;
    private double bias;
    private final List<Connection> incoming;
}
```

A neuron calculates:

$$z = b + \sum_i w_i x_i$$

and then:

$$a = \operatorname{ReLU}(z)$$

Trace this as object traversal before seeing the equivalent dot-product notation.

## <font color="#388bfd">Required Progression</font>

### <font color="#79c0ff">Part A: physical or diagram trace</font>

You receive a network with two inputs, two hidden units, two outputs, and small integer weights. Calculate every intermediate value.

### <font color="#79c0ff">Part B: object graph</font>

Instantiate the same network with Java objects and confirm that its output matches the hand trace.

### <font color="#79c0ff">Part C: token embeddings</font>

Each token identifier selects one row from an embedding table.

You must explicitly answer:

> Why is embedding lookup not the same operation as multiplying the token identifier by a number?

### <font color="#79c0ff">Part D: fixed-context forward model</font>

Concatenate several embeddings, calculate hidden values, and produce output logits.

## <font color="#388bfd">Detailed Requirements</font>

You must:

1. Implement `Neuron`, `Connection`, and `Layer`.
2. Prevent cycles in the feed-forward network.
3. Support linear and ReLU units.
4. Load deterministic instructor-provided weights.
5. Trace all intermediate values.
6. Implement token embedding lookup.
7. Concatenate context embeddings.
8. Produce one output logit per vocabulary item.
9. Apply the Chapter 4 softmax.
10. Evaluate the untrained or fixed-weight network on examples.
11. Show the numerical equivalence between object traversal and a dot product.
12. Count the network's parameters.

## <font color="#388bfd">Required Tests</font>

- Known neuron output
- Known two-layer network output
- ReLU behavior for negative, zero, and positive inputs
- Correct embedding lookup
- Correct concatenation order
- Shape validation
- Invalid connection detection
- Deterministic parameter count
- Forward output does not modify model parameters

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** An embedding is not an English definition of a token. It is a vector adjusted because it helps prediction.

> **Misconception:** A mathematical "neuron" should not be treated as a biological simulation.

## <font color="#388bfd">Stretch Goals</font>

1. Sigmoid activation, which maps values into the interval from zero to one
2. Hyperbolic tangent activation, which maps values into the interval from negative one to one
3. Leaky Rectified Linear Unit, which retains a small negative slope
4. Gaussian Error Linear Unit, abbreviated GELU, which smoothly gates inputs according to magnitude
5. Multiple hidden layers
6. Network-diagram exporter
7. Embedding nearest-neighbor explorer using cosine similarity
8. Comparison of one-hot input and learned embedding input

---

The network can calculate sophisticated scores, but its weights are frozen. When it makes a poor prediction, nothing yet identifies which connections should change.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you calculate a single neuron's output by hand given its weights, bias, and inputs?
- [ ] Can you explain what an embedding table stores and how a token identifier selects from it?
- [ ] Can you state what ReLU does for negative, zero, and positive inputs?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you build the two-input, two-hidden, two-output network in Java objects and match the hand trace exactly?
- [ ] Can you explain why embedding lookup is not multiplication of the token identifier by a number?
- [ ] Can you count the parameters of a fixed-context model from its architecture description?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you demonstrate that the object-graph traversal computes exactly the same numbers as a dot product?
- [ ] Can you explain why a network without a nonlinearity collapses into a single linear transformation?
- [ ] Can you explain how sharing an embedding table lets `basalt` and `granite` benefit from each other's training examples?

---

← [A Table That Learns](../TrainableBigram/) — Next: [Following the Error Backward](../ScalarAutograd/)
