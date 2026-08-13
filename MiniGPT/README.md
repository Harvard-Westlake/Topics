<div align="center">

# Project Strata
*<font color="#8b949e">Build a tiny transformer language model in Java from first principles</font>*

<font color="#a371f7">Learning</font>

</div>

---

A university archive has obtained a collection of geology books, field reports, and notebooks. Much of the collection has been digitized, but sections are damaged or missing.

Your task is not to build a chatbot. It is to build a transparent statistical instrument that answers one precise question:

> **Given everything the machine has read so far, what is likely to come next?**

At the beginning, the machine cannot even distinguish a word from a newline. Over eleven chapters it will gradually acquire:

1. A symbol system.
2. One-step memory.
3. Selective access to earlier text.
4. Adjustable numerical parameters.
5. Internal representations.
6. The ability to learn from error.
7. Efficient numerical machinery.
8. Learned self-attention.
9. Multiple attention specialists.
10. A complete training and generation system.
11. The ability to demonstrate, with evidence, that it improves over a Markov baseline.

The geology archive is the shared default because it provides a coherent continuing example. You may later replace it with another approved archive. The story is not fictional decoration — every narrative event exposes a real technical limitation. For example, the course repeatedly uses a diagnostic passage such as:

```text
Sample A was collected beside the basalt flow.
Sample B was collected from a pale limestone layer.
The rock associated with Sample A was ______.
```

A one-token Markov model cannot reliably connect the blank with "basalt." A fixed-window model may succeed only when the relevant phrase is nearby. An attention-based model has a mechanism for selecting the earlier mention of "Sample A."

---

## <font color="#388bfd">The Pattern Every Chapter Follows</font>

Every chapter uses the same recognizable structure:

| Stage | What happens |
|---|---|
| **Opening scene** | A short narrative shows the existing model failing. You see the failure before receiving the solution. |
| **Question to carry** | One persistent question you should be able to repeat while programming. |
| **Vocabulary before notation** | Every new term is defined before it appears in an equation, diagram, method name, or assignment specification. Acronyms are written in full before abbreviated forms appear. |
| **Worked trace** | A tiny complete example with numbers small enough to calculate by hand. Early chapters provide complete traces; middle chapters leave selected cells blank; later chapters require you to generate and interpret your own. |
| **Reference implementation** | The concept in its most inspectable form, even when that form is slow — an object-per-connection network, a scalar computation graph, a triple-loop attention implementation, an ASCII attention table. |
| **Efficient implementation** | Only after the concept is stable do you build the denser version used by the final model. |
| **Evidence checkpoint** | Observable proof: a test passes, a distribution sums to one, a model overfits a tiny dataset, a gradient matches a numerical approximation, a loss falls, a saved model reproduces its output exactly. |
| **Misconception checkpoint** | Each chapter explicitly confronts one misleading interpretation. |
| **Stretch ladder** | Optional extensions. The core is always implementable with the Java Development Kit (JDK) alone — access to stronger hardware never affects the required grade. |

---

## <font color="#388bfd">Who This Course Is For</font>

You should enter with:

- Java classes, interfaces, and inheritance
- Arrays and `ArrayList`
- `HashMap` and hashing
- File input and output
- Recursion
- Basic graph traversal
- Markov chains
- Probability frequencies
- Algebraic manipulation

Calculus and formal linear algebra are **not assumed**. Necessary mathematics is introduced just in time.

## <font color="#388bfd">Core Software Restriction</font>

The required implementation may use:

- Java standard-library classes
- `java.lang.Math`, `java.util`, `java.io`, `java.nio.file`
- JUnit for tests

It may **not** use:

- PyTorch, TensorFlow, or Deep Java Library
- General matrix packages
- Automatic-differentiation packages
- Tokenizer packages
- Pretrained models

## <font color="#388bfd">The Final Model</font>

You will build a small **decoder-only transformer language model**. "Decoder-only" means the model processes previous tokens and predicts the next token; it does not contain a separate input encoder. A reasonable standard configuration:

| Setting | Standard value |
|---|---:|
| Vocabulary size | 320–384 tokens |
| Context length | 32 tokens |
| Internal vector width | 32 numbers |
| Attention heads | 4 |
| Transformer blocks | 1 |
| Feed-forward width | 64 |
| Approximate parameters | 34,000 |

With a vocabulary of 384 tokens, width 32, one block, and an untied output matrix, the model contains approximately 33,900 trainable numbers. That is large enough to demonstrate the complete algorithm but small enough to inspect and train using ordinary processor code. It is a **tiny transformer**, not a modern large language model.

**Final success criterion.** Using the same training and held-out text:

$$\text{transformer validation loss} < \text{order-one Markov validation loss}$$

The transformer must make measurably better held-out next-token predictions than a bigram model.

---

## <font color="#388bfd">The Eleven Chapters at a Glance</font>

| Chapter | Title | Persistent question | Capability gained |
|---|---|---|---|
| 1 | [Patterns Become Tokens](Tokenizer/) | What should count as one symbol? | Byte-level tokens and learned Byte Pair Encoding merges |
| 2 | [The Reader with One-Step Memory](MarkovBaseline/) | What can be predicted from only the previous token? | Markov baseline and rigorous evaluation |
| 3 | [The Hand-Built Spotlight](FixedAttention/) | How can a token selectively use earlier information? | Conceptual causal self-attention without learning |
| 4 | [A Table That Learns](TrainableBigram/) | How can probabilities improve themselves? | Softmax, loss, gradients, and trainable bigram |
| 5 | [From Exact Symbols to Features](ObjectNetwork/) | How can similar patterns share knowledge? | Object-oriented neural network and forward propagation |
| 6 | [Following the Error Backward](ScalarAutograd/) | Which parameters caused a mistake? | Backpropagation and scalar automatic differentiation |
| 7 | [From Glass Box to Engine](DenseEngine/) | How can the same model run efficiently? | Dense arrays and explicit module gradients |
| 8 | [Learning What to Look For](SingleHeadAttention/) | How can attention discover useful relationships? | Trainable single-head causal attention |
| 9 | [A Team of Readers](TransformerBlock/) | How can several attention processes cooperate? | Multi-head attention and a complete transformer block |
| 10 | [The Machine Writes](TrainingAndGeneration/) | How does the complete system train, save, and generate? | End-to-end transformer training and inference |
| 11 | [The Trial of the Archive](Capstone/) | Did the model actually learn something useful? | Domain experiment, comparison, and responsible evaluation |

This is a spiral curriculum. Attention appears first in a simple, non-learning form, then returns as learned single-head attention, multi-head attention, and finally stacked transformer computation. The [original transformer paper](https://arxiv.org/abs/1706.03762) introduced a network architecture based primarily on attention mechanisms; this course exposes that mechanism progressively instead of presenting the entire architecture at once. The [companion repository](https://github.com/andrewtheiss/llm-from-scratch) covers the same architectural destination — tokenization, transformer architecture, training, and generation — in a framework-backed, workshop-sized sequence.

---

## <font color="#388bfd">Reference Documentation</font>

Cross-cutting references consulted throughout the course:

| Document | Covers |
|---|---|
| [Model Museum](Docs/model-museum.md) | The cumulative comparison directory every assignment contributes to |
| [Ethics and Context Strand](Docs/ethics-and-context.md) | The per-chapter social-context questions |
| [Java Architecture](Docs/java-architecture.md) | The common cumulative package structure and shared interfaces |
| [Instructor Scaffolding](Docs/instructor-scaffolding.md) | What is provided versus what you implement, per chapter |
| [Acceptance Tests](Docs/acceptance-tests.md) | The permanent test suite that must keep passing as the project grows |
| [Grading](Docs/grading.md) | Assignment and capstone grading patterns |
| [Design Rationale](Docs/design-rationale.md) | Why the course is sequenced this way |

---

## <font color="#388bfd">Lessons</font>

| Week | Lesson | What you'll build |
|---|---|---|
| 1 | [Patterns Become Tokens](Tokenizer/) | Byte Pair Encoding trainer: count adjacent pairs, merge the most frequent |
| 2 | [The Reader with One-Step Memory](MarkovBaseline/) | Uniform, unigram, and bigram models with held-out evaluation |
| 3 | [The Hand-Built Spotlight](FixedAttention/) | Three non-learning causal attention mechanisms |
| 4 | [A Table That Learns](TrainableBigram/) | Trainable bigram with softmax, cross-entropy, and gradient descent |
| 5 | [From Exact Symbols to Features](ObjectNetwork/) | Object-oriented fixed-context neural network, forward pass |
| 6–7 | [Following the Error Backward](ScalarAutograd/) | Scalar automatic-differentiation engine and a trained tiny network |
| 8 | [From Glass Box to Engine](DenseEngine/) | Dense-array numerical engine verified against the scalar reference |
| 9 | [Learning What to Look For](SingleHeadAttention/) | Trainable single-head causal attention on synthetic tasks |
| 10 | [A Team of Readers](TransformerBlock/) | Multi-head attention, feed-forward network, and a full transformer block |
| 11–12 | [The Machine Writes](TrainingAndGeneration/) | Training loop, Adam, checkpointing, and text generation |
| 13–15 | [The Trial of the Archive](Capstone/) | Capstone experiment, ablation, and evaluation report |

Chapter 6 receives extra time because backpropagation is the largest conceptual transition. Chapter 10 receives extra time because integration bugs differ from algorithmic bugs. The capstone receives several weeks because training, evaluation, and writing cannot be compressed into one programming night.

---

## <font color="#388bfd">The Course Promise</font>

By the end of Project Strata you will have personally implemented and connected: a learned tokenizer, a Markov baseline, softmax probabilities, cross-entropy loss, gradient descent, neural embeddings, forward propagation, backpropagation, scalar automatic differentiation, dense numerical operations, causal self-attention, learned queries, keys, and values, multi-head attention, feed-forward computation, residual connections, normalization, an adaptive optimizer, checkpointing, autoregressive generation, controlled evaluation, and data and model documentation.

Most importantly, the story remains focused from the first page to the last:

> **How does a machine progress from counting what usually follows one symbol to selectively using an entire context — and how can we prove that the resulting system actually learned?**

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you state the one precise question the archive machine is built to answer?
- [ ] Can you name the eleven capabilities the machine acquires, in order, and say which chapter delivers each one?
- [ ] Can you explain why the diagnostic "Sample A" passage defeats a one-token Markov model?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain what "decoder-only" means and why this course's final model qualifies?
- [ ] Can you state the final success criterion as a comparison between two measured quantities?
- [ ] Can you explain why the course forbids matrix, tokenizer, and automatic-differentiation packages?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why attention is introduced in Chapter 3, before any training machinery exists?
- [ ] Can you estimate the parameter count of the standard configuration from its settings table?
- [ ] Can you defend why beating the bigram baseline is the engineering target but not the entire grade?
