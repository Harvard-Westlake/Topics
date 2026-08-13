<div align="center">

# A Team of Readers
*<font color="#8b949e">Multi-head attention, a feed-forward network, and a complete transformer block</font>*

<font color="#a371f7">Learning</font>

</div>

---

> One reader may track which sample is being discussed. Another may track punctuation. Another may prefer the immediately previous token. Another may recognize repeated phrases. No single attention pattern must solve every relationship. The machine will now divide its internal representation among several specialist readers, then combine their findings.

## <font color="#388bfd">Question to Carry</font>

> **How can multiple attention processes communicate while preserving a stable representation?**

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Multi-head attention | Several attention heads operating in parallel on different portions or projections of the representation. |
| Concatenation | Joining head outputs into one longer vector. |
| Feed-Forward Network, abbreviated FFN | A small neural network applied independently to each sequence position. |
| Position-wise | Applied separately at every token position using the same parameters. |
| Residual connection | Directly adding a sublayer's input to its output. |
| Skip connection | Another name for a residual connection. |
| Normalization | Rescaling internal values to maintain stable magnitudes. |
| Root Mean Square Normalization, abbreviated RMSNorm | Rescaling a vector according to the square root of its mean squared value. |
| Layer Normalization, abbreviated LayerNorm | Normalization using both mean and variance across features. |
| Pre-normalization | Applying normalization before attention or the feed-forward network. |
| Transformer block | A repeated unit containing attention, local feed-forward computation, residual paths, and normalization. |
| Model width | The dimensionality of each token's internal representation. |
| Depth | The number of stacked processing blocks. |
| Parameter count | The total number of trainable numerical values. |
| Dropout | Randomly setting selected activations to zero during training as a regularization method. |
| Weight tying | Reusing the same parameter matrix for two conceptual roles. |
| Rotary Position Embedding, abbreviated RoPE | A position method that rotates query and key components according to position. |

[Root Mean Square Normalization](https://arxiv.org/abs/1910.07467) is selected for the required model because it provides a simpler rescaling operation than full Layer Normalization while retaining the pedagogical role of stabilizing magnitudes.

## <font color="#388bfd">Assignment Summary</font>

Create a complete one-block transformer:

```text
token representation
        ↓
Root Mean Square Normalization
        ↓
multi-head causal self-attention
        ↓
residual addition
        ↓
Root Mean Square Normalization
        ↓
position-wise feed-forward network
        ↓
residual addition
```

## <font color="#388bfd">Multi-Head Structure</font>

Require:

```text
modelWidth % numberOfHeads == 0
```

For a width of 32 and four heads:

```text
headDimension = 8
```

The simplest Java representation is:

```java
List<AttentionHead> heads;
```

Each head returns:

```text
[time][headDimension]
```

Outputs are concatenated into:

```text
[time][modelWidth]
```

This avoids a four-dimensional batch-head-time-feature array.

## <font color="#388bfd">Feed-Forward Structure</font>

For every position independently:

$$h = \operatorname{ReLU}(xW_1) \qquad y = hW_2$$

The required hidden width can be twice the model width:

```text
feedForwardWidth = 2 × modelWidth
```

A four-times expansion is a stretch goal.

## <font color="#388bfd">Root Mean Square Normalization</font>

For vector $x$ of dimension $d$:

$$\operatorname{rms}(x) = \sqrt{\frac{1}{d}\sum_i x_i^2 + \epsilon}$$

$$y_i = \frac{x_i}{\operatorname{rms}(x)}$$

An optional learned scale vector may multiply the result.

## <font color="#388bfd">Detailed Requirements</font>

You must:

1. Create a configurable number of attention heads.
2. Validate divisibility of model width by head count.
3. Concatenate head outputs deterministically.
4. Apply one shared output projection.
5. Implement the position-wise feed-forward network.
6. Implement residual additions.
7. Implement Root Mean Square Normalization.
8. Implement all required backward methods.
9. Count parameters by component.
10. Verify that one head reproduces Chapter 8 behavior.
11. Verify that the feed-forward network does not directly mix positions.
12. Overfit a tiny corpus with one transformer block.

## <font color="#388bfd">Required Tests</font>

- One-head equivalence
- Head concatenation order
- Invalid head configuration rejection
- Every head receives gradients
- Feed-forward independence across positions
- Residual addition forward and backward
- Root Mean Square Normalization forward
- Root Mean Square Normalization gradient check
- Parameter-count agreement
- Tiny-corpus overfit
- Finite values throughout training

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** Attention performs communication among token positions. The feed-forward network performs local computation at each position. They serve different roles.

## <font color="#388bfd">Stretch Goals</font>

1. Full Layer Normalization
2. Gaussian Error Linear Unit in place of Rectified Linear Unit
3. Dropout after attention and feed-forward sublayers
4. Learned normalization scale
5. Four-times feed-forward expansion
6. Weight tying between token embedding and vocabulary output matrices
7. Rotary Position Embedding
8. More attention heads at fixed model width
9. Two or more transformer blocks
10. Head-removal experiment to determine whether all heads contribute equally

---

You now possess the central block of a transformer. The final engineering chapter turns that block into a complete language-modeling system that can train, stop, save itself, reload, and generate text.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain why model width must be divisible by the number of heads?
- [ ] Can you trace a token representation through the block diagram, naming each stage?
- [ ] Can you state the different roles of attention and the feed-forward network in one sentence each?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement Root Mean Square Normalization and pass a numerical gradient check?
- [ ] Can you verify that a one-head configuration exactly reproduces your Chapter 8 model?
- [ ] Can you design a test proving the feed-forward network never mixes information across positions?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you count the block's parameters by component and reconcile the total against the enumerated parameters?
- [ ] Can you explain what residual connections contribute to gradient flow through the block?
- [ ] Can you run a head-removal experiment and interpret whether all heads contribute equally?

---

← [Learning What to Look For](../SingleHeadAttention/) — Next: [The Machine Writes](../TrainingAndGeneration/)
