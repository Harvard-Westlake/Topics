<div align="center">

# Following the Error Backward
*<font color="#8b949e">Backpropagation and a scalar automatic-differentiation engine</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The model predicts the wrong token. Thousands of calculations contributed to that decision. Which weight deserves responsibility? Some weights increased the error. Others reduced it. Some influenced the result along several separate paths. The machine must trace the final loss backward through its own history of calculations.

## <font color="#388bfd">Question to Carry</font>

> **How can the model determine how each internal number affected its final error?**

## <font color="#388bfd">Pedagogical Method</font>

This chapter is trace-driven, but implementation follows the trace. The order is:

1. Study a complete worked trace.
2. Predict the sign of selected gradients.
3. Calculate a tiny graph by hand.
4. Implement scalar automatic differentiation.
5. Train a very small network.

This preserves conceptual rigor without asking you to discover reverse-mode differentiation unaided.

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Computation graph | A graph recording mathematical operations and their dependencies. |
| Node | One value or operation in a computation graph. |
| Directed Acyclic Graph, abbreviated DAG | A directed graph containing no directed cycles. |
| Parent | An earlier value used to calculate another value. |
| Local derivative | The derivative of one operation's output with respect to one direct input. |
| Chain rule | A rule for combining rates of change through composed operations. |
| Backpropagation | Calculating gradients by moving backward from the loss through the computation graph. |
| Automatic differentiation | Programmatically calculating exact derivatives by recording operations and applying derivative rules. |
| Autograd | A common shortened name for automatic differentiation. |
| Reverse mode | Automatic differentiation that begins with one output and computes effects on many inputs. |
| Topological order | An ordering in which every dependency appears before the value that depends on it. |
| Upstream gradient | The gradient arriving from later calculations. |
| Gradient accumulation | Adding gradient contributions from multiple graph paths. |
| Leaf node | A graph node representing an original input or parameter. |
| Overfit | Fit training examples extremely well, often more closely than unseen examples. |
| Reference implementation | A simple implementation used to establish correctness rather than performance. |

A [scalar automatic-differentiation engine](https://karpathy.github.io/2026/02/12/microgpt/) can express the entire learning algorithm in a highly inspectable form. It is algorithmically representative of tensor-based differentiation but much less efficient, making it suitable as a correctness reference rather than the final book-scale engine.

## <font color="#388bfd">First Worked Trace</font>

Use:

$$c = ab \qquad L = c + a$$

with:

```text
a = 2
b = 3
c = 6
L = 8
```

The derivative of $L$ with respect to $a$ is:

```text
path through c: b = 3
direct path:     1
total:           4
```

This example demonstrates why gradients must be accumulated with addition.

## <font color="#388bfd">Assignment Summary</font>

Implement a `Value` class representing one scalar number and its place in a computation graph. Then rebuild the Chapter 5 fixed-context network using `Value` objects and train it on a tiny corpus.

## <font color="#388bfd">Suggested Design</font>

```java
public final class Value {
    private double data;
    private double grad;
    private final List<Value> parents;
    private final BackwardOperation backwardOperation;

    public Value add(Value other);
    public Value multiply(Value other);
    public Value exp();
    public Value log();
    public Value relu();

    public void backward();
}
```

## <font color="#388bfd">Detailed Requirements</font>

You must:

1. Store scalar value and gradient.
2. Store parent references.
3. Record the local derivative associated with each parent.
4. Build a topological ordering.
5. Traverse the ordering backward.
6. Initialize the loss gradient to one.
7. Accumulate, rather than overwrite, gradients.
8. Implement: addition, multiplication, negation, subtraction, division, integer power, exponential, natural logarithm, and Rectified Linear Unit.
9. Implement `zeroGradients`.
10. Rebuild a tiny fixed-context neural model.
11. Calculate cross-entropy loss.
12. Train on a very small dataset.
13. Deliberately overfit a tiny sample.

## <font color="#388bfd">Required Gradient Checks</font>

For selected parameter $\theta$:

$$\frac{\partial L}{\partial \theta} \approx \frac{L(\theta+\epsilon)-L(\theta-\epsilon)}{2\epsilon}$$

A typical $\epsilon$ is approximately $10^{-5}$, though you should test sensitivity.

## <font color="#388bfd">Required Tests</font>

- Addition gradient
- Multiplication gradient
- Branching graph gradient accumulation
- Shared parameter used multiple times
- Exponential gradient
- Logarithm gradient
- ReLU positive and negative cases
- Topological-order correctness
- Finite-difference agreement
- Gradients reset between steps
- Loss decreases on a tiny dataset
- Network can memorize 20–100 examples

## <font color="#388bfd">Required Trace Artifact</font>

Submit a table containing:

```text
node
forward value
local derivative
upstream gradient
final accumulated gradient
```

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** Backpropagation is not a separate intelligent process. It is repeated application of local derivative rules and the chain rule.

## <font color="#388bfd">Stretch Goals</font>

1. Hyperbolic tangent operation and derivative
2. Sigmoid operation and derivative
3. Gaussian Error Linear Unit approximation and derivative
4. Graph exporter using the Graphviz DOT text format
5. Retained-graph versus discarded-graph memory experiment
6. Automatic finite-difference test generator
7. Detection of accidental gradient replacement
8. Higher-order derivative experiment

---

The model now learns, but every arithmetic operation creates a Java object. The glass-box engine is excellent for inspection and poor for processing books. You must preserve the mathematics while replacing the representation.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you compute the gradient of $L$ with respect to $a$ in the worked trace $c = ab$, $L = c + a$, and explain where the 4 comes from?
- [ ] Can you explain what a topological ordering guarantees and why the backward pass needs one?
- [ ] Can you state why the loss node's gradient is initialized to one?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement `Value.add` and `Value.multiply` with correct local derivatives, verified by finite differences?
- [ ] Can you build a branching graph where one parameter feeds two paths and show the gradients add?
- [ ] Can you explain why gradients must be zeroed between training steps and what silently breaks otherwise?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you rebuild the Chapter 5 fixed-context network from `Value` objects and overfit 20–100 examples?
- [ ] Can you explain reverse-mode automatic differentiation and why it is efficient when one output depends on many inputs?
- [ ] Can you produce and interpret a complete trace table — forward value, local derivative, upstream gradient, accumulated gradient — for a graph of your own design?

---

← [From Exact Symbols to Features](../ObjectNetwork/) — Next: [From Glass Box to Engine](../DenseEngine/)
