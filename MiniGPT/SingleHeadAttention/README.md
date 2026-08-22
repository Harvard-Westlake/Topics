<div align="center">

# Learning What to Look For
*<font color="#8b949e">A trainable single-head causal attention mechanism, proven on synthetic tasks</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The hand-built spotlight could select earlier information, but only because the programmer defined what counted as a match. A real model must discover its own questions. It must learn what the current token is seeking, how earlier tokens advertise what they contain, and what information each earlier token should contribute.

## <font color="#388bfd">Question to Carry</font>

> **How can the attention mechanism learn its own matching rules?**

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Projection | A learned transformation from one vector representation to another. |
| Query projection | The learned transformation producing what a position seeks. |
| Key projection | The learned transformation producing how a position may be matched. |
| Value projection | The learned transformation producing what information a position offers. |
| Attention head | One independently parameterized attention mechanism. |
| Head dimension | The width of the vectors used by one attention head. |
| Scaled dot-product attention | Dot-product attention divided by the square root of head dimension. |
| Masked softmax | Softmax applied only to permitted positions. |
| Token embedding | A learned representation of token identity. |
| Position embedding | A learned representation of sequence position. |
| Output projection | A learned transformation applied after weighted value combination. |
| Residual connection | Addition of a component's input directly to its output. |
| Causal self-attention | Self-attention restricted to the current and earlier positions. |
| Decoder-only model | A model that predicts following tokens using prior context. |
| Synthetic task | An artificially constructed dataset designed to test one capability clearly. |

## <font color="#388bfd">Assignment Summary</font>

Implement one trainable causal attention head:

$$Q = XW_Q \qquad K = XW_K \qquad V = XW_V$$

$$A = \operatorname{softmax}\left(\operatorname{causalMask}\left(\frac{QK^\top}{\sqrt{d}}\right)\right)$$

$$Y = AV \qquad O = YW_O$$

Add learned token and position embeddings and train the model on small synthetic tasks before attempting natural text.

## <font color="#388bfd">Why Synthetic Tasks Come First</font>

Natural-language loss can fall for many reasons. A synthetic task exposes whether attention itself works.

### <font color="#79c0ff">Task A: previous matching marker</font>

```text
A red B blue A ?
```

Target:

```text
red
```

### <font color="#79c0ff">Task B: delayed copy</font>

```text
start pineapple filler filler recall
```

Target after `recall`:

```text
pineapple
```

### <font color="#79c0ff">Task C: paired order lookup</font>

```text
orderA pineapple orderB pepperoni query orderA
```

Target:

```text
pineapple
```

Task C is Chapter 3's diagnostic passage — *the topping on Order A was ______* — stripped to bare tokens. In Chapter 3 you wrote the matching rule by hand; here the head must discover it.

## <font color="#388bfd">Detailed Requirements</font>

You must:

1. Add token embeddings.
2. Add learned position embeddings.
3. Implement query, key, and value linear projections.
4. Implement scaled dot-product scores.
5. Apply causal masking before softmax.
6. Calculate weighted value combinations.
7. Apply the output projection.
8. Add one residual connection.
9. Produce next-token logits.
10. Implement backward methods for all operations.
11. Run numerical gradient checks with tiny dimensions.
12. Overfit a synthetic retrieval dataset.
13. Visualize learned attention weights.
14. Compare learned attention with Chapter 3 fixed attention.

## <font color="#388bfd">Backward Equations (Provided)</font>

The backward equations are supplied — implement and verify them; you are not required to derive every matrix derivative independently.

Given output gradient $dO$:

$$dW_O = Y^\top dO \qquad dY = dO\,W_O^\top$$

$$dA = dY\,V^\top \qquad dV = A^\top dY$$

For each softmax row:

$$dS_i = A_i \odot \left(dA_i - \operatorname{dot}(dA_i, A_i)\right)$$

Masked locations receive zero gradient. Then:

$$dQ = \frac{dS\,K}{\sqrt{d}} \qquad dK = \frac{dS^\top Q}{\sqrt{d}}$$

## <font color="#388bfd">Required Tests</font>

- Future-token invariance
- Masked positions have zero attention weight
- Masked positions receive zero score gradient
- Query projection gradient check
- Key projection gradient check
- Value projection gradient check
- Output projection gradient check
- Position embeddings receive gradients
- Token embeddings receive accumulated gradients
- Residual gradient contains both paths
- Synthetic task can be memorized
- One-token context behaves correctly

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** Query, key, and value vectors are not stored questions, dictionary keys, or literal values. They are learned numerical roles within the matching calculation.

## <font color="#388bfd">Stretch Goals</font>

1. Relative-position bias, meaning a learned preference based on distance
2. Local attention window
3. Attention-weight entropy report
4. Separate positional features for query and key
5. Attention dropout, meaning randomly suppressing some attention weights during training
6. Learned versus fixed attention comparison
7. Head-dimension experiment
8. Attention map viewer with token labels

---

One attention head can learn one style of retrieval. Language contains many simultaneous relationships: nearby spelling patterns, punctuation structure, topic references, repeated labels, and longer-range dependencies. The next model uses several attention processes in parallel.

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain what changed between Chapter 3's fixed attention and this chapter's learned attention.
- [ ] Explain why the model needs position embeddings in addition to token embeddings.
- [ ] Describe what each synthetic task (matching marker, delayed copy, paired lookup) proves about the mechanism.

### <font color="#79c0ff">Intermediate</font>

- [ ] Implement the $Q$, $K$, $V$ projections and verify each with a numerical gradient check.
- [ ] Overfit the paired order lookup task and show the attention matrix retrieving the correct position.
- [ ] Verify that masked positions receive zero attention weight and zero score gradient.

### <font color="#79c0ff">Advanced</font>

- [ ] Implement the softmax-row backward equation and explain the role of the $\operatorname{dot}(dA_i, A_i)$ term.
- [ ] Show that the residual connection's gradient contains contributions from both paths.
- [ ] Explain a training failure mode a synthetic task would expose that natural-text loss would hide.

---

← [From Glass Box to Engine](../DenseEngine/) — Next: [A Team of Readers](../TransformerBlock/)
