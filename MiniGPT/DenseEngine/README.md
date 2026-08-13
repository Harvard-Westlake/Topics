<div align="center">

# From Glass Box to Engine
*<font color="#8b949e">The same mathematics on dense primitive arrays, verified against the scalar reference</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

> The transparent model works, but a single training step creates an enormous pile of tiny objects. The archive contains millions of token positions. To train on it, the same computations must be performed using compact primitive arrays and predictable loops — without losing the ability to prove that the results are correct.

## <font color="#388bfd">Question to Carry</font>

> **How can the same learning algorithm be represented efficiently without hiding what it does?**

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Scalar | One numerical value. |
| Vector | An ordered one-dimensional collection of numerical values. |
| Matrix | A rectangular collection of numerical values arranged in rows and columns. |
| Row | A horizontal sequence in a matrix. |
| Column | A vertical sequence in a matrix. |
| Matrix shape | The number of rows and columns. |
| Matrix-vector multiplication | Producing a vector by taking one dot product per matrix row. |
| Matrix multiplication | Combining two matrices through row-column dot products. |
| Transpose | Exchanging matrix rows and columns. |
| Row-major storage | Storing all values from one row contiguously before the next row. |
| Primitive array | A Java array containing values such as `double` rather than objects such as `Double`. |
| Allocation | Reserving memory for a new object or array. |
| Aliasing | Two references unexpectedly referring to the same mutable data. |
| Module | A reusable model component with forward and backward behavior. |
| Forward cache | Intermediate information saved because the backward calculation will need it. |
| Explicit backward method | A manually written method calculating input and parameter gradients. |
| Batch | A collection of training examples processed together. |
| Gradient accumulation | Sequentially adding gradients from several examples before one update. |
| Benchmark | A repeatable measurement of execution time or resource use. |

## <font color="#388bfd">Assignment Summary</font>

Build a deliberately narrow numerical engine using flat `double[]` arrays. You do not build arbitrary-rank tensors, broadcasting, views, or a general scientific-computing package.

The Chapter 6 scalar model becomes the correctness oracle.

## <font color="#388bfd">Required Core Classes</font>

```java
public final class Matrix {
    private final int rows;
    private final int columns;
    private final double[] data;
}

public final class Parameter {
    private final Matrix values;
    private final Matrix gradients;
}
```

Required modules:

- `Embedding`
- `Linear`
- `ReLU`
- `SoftmaxCrossEntropy`

## <font color="#388bfd">Conceptual Bridge</font>

The object-oriented Chapter 5 calculation:

```text
for each incoming connection:
    sum += connection.weight * connection.source.value
```

becomes:

$$y = Wx$$

The equation is not a new operation. It is a compact name for the same repeated multiply-and-add traversal.

## <font color="#388bfd">Detailed Requirements</font>

You must implement:

1. Flat row-major indexing
2. Bounds checking in development mode
3. Vector dot product
4. Matrix-vector multiplication
5. Matrix transpose
6. Matrix-matrix multiplication where needed
7. Elementwise addition
8. Scalar multiplication
9. Embedding forward and backward
10. Linear-layer forward and backward
11. Rectified Linear Unit forward and backward
12. Softmax cross-entropy forward and backward
13. Gradient zeroing
14. Parameter enumeration
15. Shape validation
16. A dense version of the fixed-context model

## <font color="#388bfd">Single-Sequence Training</font>

The required final engine should avoid a batch dimension in model code. Instead:

```java
zeroGradients();

for (int i = 0; i < accumulationSteps; i++) {
    TrainingExample example = dataset.sample(random);
    model.forwardBackward(example);
}

scaleGradients(1.0 / accumulationSteps);
optimizer.step();
```

This prevents you from immediately confronting four-dimensional arrays.

## <font color="#388bfd">Reference Equivalence Requirement</font>

For a tiny deterministic model, compare:

- Forward logits
- Loss
- Input gradients
- Embedding gradients
- Linear weights
- Weight gradients

between:

1. The scalar automatic-differentiation implementation
2. The dense-array implementation

## <font color="#388bfd">Required Tests</font>

- Index conversion
- Matrix shape errors
- Known matrix-vector product
- Known transpose
- Known linear forward pass
- Known linear backward pass
- Embedding rows receive correct accumulated gradients
- Rectified Linear Unit mask
- Softmax cross-entropy equivalence
- Scalar and dense models agree within tolerance
- No hidden object allocation in innermost numeric loops
- Dense model runs measurably faster than scalar reference

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** The matrix implementation is not a different model. It is a more compact execution strategy for the same arithmetic.

## <font color="#388bfd">Stretch Goals</font>

1. Reusable workspace arrays that reduce allocation
2. Multi-threaded processing of independent training examples
3. Parallel batch accumulation with deterministic gradient reduction
4. `float` storage instead of `double`
5. **Mixed precision**, meaning different numerical precisions are used for storage and calculation
6. Cache-aware loop ordering
7. Department-supported vector instructions
8. Sparse embedding-gradient storage
9. Runtime profiler report

Mixed precision should remain an engineering experiment, not a core requirement. Numerical differences must be documented.

---

You now possess a trainable and sufficiently efficient neural engine. Next you return to the attention mechanism from Chapter 3, replacing programmer-written similarity rules with learned projections.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you convert a (row, column) pair into a flat row-major array index and back?
- [ ] Can you explain why $y = Wx$ is the same calculation as the Chapter 5 connection-traversal loop?
- [ ] Can you explain what a forward cache stores and why the backward pass needs it?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement `Linear` forward and backward and pass a known-value test for both?
- [ ] Can you show that embedding rows accumulate gradients correctly when the same token appears twice in one context?
- [ ] Can you run the reference-equivalence comparison and get scalar and dense models to agree within tolerance?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you find and eliminate a hidden object allocation inside an innermost numeric loop?
- [ ] Can you benchmark the dense model against the scalar reference and explain where the speedup comes from?
- [ ] Can you explain the aliasing bug class and construct a test that would catch one in your `Matrix` class?

---

← [Following the Error Backward](../ScalarAutograd/) — Next: [Learning What to Look For](../SingleHeadAttention/)
