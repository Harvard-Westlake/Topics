<div align="center">

# Design Rationale
*<font color="#8b949e">Why Project Strata is sequenced this way</font>*

</div>

---

This curriculum treats the course as a **student-facing intellectual journey**: every chapter begins with a concrete failure in the current model, introduces only the vocabulary needed to understand that failure, and ends with a visibly more capable system.

The [linked repository](https://github.com/andrewtheiss/llm-from-scratch) remains the architectural destination: tokenization, transformer architecture, training, and generation. However, that repository compresses those ideas into a workshop-sized sequence and relies on PyTorch for tensor operations, automatic differentiation, optimization, and hardware acceleration. Its reference configurations range from roughly half a million to ten million parameters. That is appropriate for a framework-backed workshop, but not for a first encounter implemented with the Java standard library.

## <font color="#388bfd">The Instructional Hazards Being Avoided</font>

Three major hazards shaped this design:

1. An abrupt jump from discrete data structures to abstract matrix mathematics.
2. A "backpropagation cliff" in which Java indexing, computation graphs, and multivariable calculus arrive simultaneously.
3. A technically competent but socially and personally sterile curriculum.

The audience is students who have completed Data Structures and Design and already understand Markov chains, hash maps, arrays, graphs, and object-oriented design. The synthesis:

| Recommendation | Adaptation for this course |
|---|---|
| Replace matrix mathematics with objects | **Begin with objects, then reveal the equivalent vector and matrix operation.** Students need the mathematics eventually, but not before they have a concrete model. |
| Replace backpropagation implementation with trace analysis | **Trace first, implement second.** Students analyze complete worked traces before implementing a deliberately tiny automatic-differentiation engine. |
| Use culturally and personally meaningful data | **Keep the task textual, but make the default archive one everyone has opinions about.** The pizzeria's order tickets, recipes, and reviews are commonplace and mildly controversial — pineapple on pizza starts an argument in any room — which keeps attention on the prediction question. Campus history, public oral histories, and community documents can all serve as alternative corpora. |
| Avoid excessive low-level complexity | **Build only narrow numerical tools.** Students do not build a general tensor library. |
| Show a working system early | **Introduce non-learning attention in Chapter 3.** Students see the central idea before they possess the machinery required to train it. |
| Preserve rigor through analysis | **Require both analysis and implementation.** Every assignment includes traces, invariants, tests, and an explanation of observed behavior. |

## <font color="#388bfd">Why This Sequence Works</font>

### <font color="#79c0ff">It presents the destination early without hiding it</font>

The linked repository's strength is that learners quickly see the complete pipeline. Its weakness for this audience is that the framework performs most difficult numerical work. This curriculum preserves the early sense of destination by introducing conceptual attention in Chapter 3, but the implementation remains transparent.

### <font color="#79c0ff">It uses objects as a bridge rather than a permanent detour</font>

Students understand objects and traversals more readily than unexplained matrix notation. The course therefore begins neural computation with `Neuron` and `Connection`, then explicitly proves that the object traversal and dot product are the same calculation.

### <font color="#79c0ff">It uses traces without removing implementation</font>

A blank-page backpropagation assignment invites copying rather than understanding. Students therefore study and annotate complete traces first. Because they have graph and recursion experience, they then implement the computation graph themselves.

### <font color="#79c0ff">It introduces attention as a recurring idea</font>

Self-attention is not confined to one enormous transformer assignment:

1. Uniform causal aggregation
2. Rule-based selective attention
3. Fixed dot-product attention
4. Learned single-head attention
5. Multi-head attention
6. Stacked transformer attention
7. Cached attention during generation

Each version answers one new question.

### <font color="#79c0ff">It keeps every model for comparison</font>

Students see exactly what each new mechanism contributes. The Markov model is not forgotten after Week 2. The scalar engine is not discarded after the dense engine appears. Each model becomes a reference point — see the [Model Museum](model-museum.md).

### <font color="#79c0ff">It connects rigor to evidence</font>

Students prove their work through invariants, gradient checks, tiny overfitting, reference equivalence, held-out evaluation, reproducible checkpoints, and ablation studies. The result is more rigorous than either merely copying a framework implementation or merely producing attractive generated text.

### <font color="#79c0ff">It incorporates relevance without sacrificing technical unity</font>

Students may train on food writing, local history, public archives, or another approved corpus. The final task remains next-token language modeling for everyone, so class discussion and grading remain coherent. Moving the final project to unrelated civic prediction data would break the language-modeling throughline; using civic and community **text** preserves both relevance and architectural continuity.

## <font color="#388bfd">Key Sources</font>

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — the original transformer architecture
- [Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/) — Byte Pair Encoding for text
- [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) — the normalization used in the required model
- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — the adaptive optimizer
- [microgpt](https://karpathy.github.io/2026/02/12/microgpt/) — scalar automatic differentiation as a correctness reference
- [llm-from-scratch](https://github.com/andrewtheiss/llm-from-scratch) — the framework-backed companion sequence

← Back to [Docs](README.md)
