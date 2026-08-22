<div align="center">

# The Trial of the Archive
*<font color="#8b949e">The capstone experiment: prove, with evidence, that the transformer beat the baseline</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

> The machine now produces plausible passages. That is visually impressive and scientifically weak evidence. A persuasive experiment requires a held-out test, a baseline, a hypothesis, repeatable conditions, and an honest description of failure. The archive machine must now stand trial.

## <font color="#388bfd">Question to Carry</font>

> **Did the transformer learn patterns that genuinely improve prediction beyond a Markov chain?**

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Hypothesis | A precise claim that can be tested with evidence. |
| Experiment | A controlled procedure used to evaluate a hypothesis. |
| Control | A comparison condition intended to isolate the effect being studied. |
| Independent variable | The factor deliberately changed in an experiment. |
| Dependent variable | The outcome measured in response. |
| Hyperparameter | A setting selected by the programmer rather than learned directly. |
| Ablation study | An experiment removing or changing one model component to measure its contribution. |
| Held-out evaluation | Evaluation on data excluded from training. |
| Benchmark | A standardized task or measurement used for comparison. |
| Error analysis | Systematic examination of where and how a model fails. |
| Data provenance | The origin and history of a dataset. |
| License | The legal terms governing use and redistribution. |
| Consent | Permission from people whose data or expression may be used. |
| Data card | A structured description of a dataset, its source, composition, use, and limitations. |
| Model card | A structured description of a model, intended uses, evaluation, and limitations. |
| Representational bias | Uneven or distorted representation of people, language, topics, or perspectives. |
| Hallucination | Generated content presented fluently despite lacking factual support. |
| Reproducibility | The ability to repeat an experiment and obtain consistent results. |
| Quantization | Representing model values with fewer numerical levels or bits. |
| Graphics Processing Unit, abbreviated GPU | Hardware designed for highly parallel numerical operations. |
| FlashAttention | An attention-computation strategy designed to reduce expensive memory movement by processing attention in tiles. |

## <font color="#388bfd">Dataset Choices</font>

The default is three public-domain cookbooks or other food writing — historic cookbooks are plentiful in the public domain, and they keep the pizzeria story running to the final page. Approved alternatives may include:

- Public-domain novels or short stories
- Environmental field reports
- Campus history archives
- Public municipal planning documents
- Publicly licensed oral histories
- Historical newspapers
- Museum collection descriptions
- Public environmental-justice reports
- Bilingual public archives

You should not be pressured to provide personal cultural material. Do not use private messages, identifiable student data, or text for which you lack permission. Choice, provenance, critical interpretation, and responsible use are the point — text prediction remains the common technical task so class discussion and grading stay coherent.

## <font color="#388bfd">Required Hypothesis</font>

A suitable primary hypothesis is:

> A one-block causal transformer using a context window of 32 tokens will achieve lower validation loss than an order-one Markov model trained on the same tokenized corpus.

## <font color="#388bfd">Required Models</font>

Train and evaluate:

1. Uniform baseline
2. Unigram baseline
3. Bigram Markov baseline
4. Fixed-context neural model
5. Single-head attention model
6. Multi-head transformer
7. One selected variation

## <font color="#388bfd">Required Experimental Table</font>

| Model | Parameters | Context length | Training steps | Training loss | Validation loss | Test loss |
|---|---:|---:|---:|---:|---:|---:|
| Bigram Markov | | 1 | — | | | |
| Fixed-context neural model | | | | | | |
| Single-head attention | | | | | | |
| Multi-head transformer | | | | | | |

## <font color="#388bfd">Required Ablation</font>

Change one variable while holding others as constant as practical. Approved comparisons include:

- No position embeddings versus learned position embeddings
- One attention head versus four
- Attention without feed-forward network versus full block
- No residual connection versus residual connection
- Character tokenization versus small Byte Pair Encoding
- Context length 8 versus 32
- One transformer block versus two
- Rectified Linear Unit versus Gaussian Error Linear Unit
- Root Mean Square Normalization versus full Layer Normalization

## <font color="#388bfd">Required Corpus Report</font>

Document:

- Corpus title
- Source
- License
- Number of documents
- Original bytes
- Tokens
- Vocabulary size
- Cleaning decisions
- Removed headers, indexes, or scanning artifacts
- Document boundaries
- Training, validation, and test division
- Known representational limitations

## <font color="#388bfd">Required Evaluation</font>

### <font color="#79c0ff">Quantitative</font>

- Training loss
- Validation loss
- Final test loss
- Bits per byte when tokenizers differ
- Parameter count
- Training steps
- Runtime
- Best validation step
- At least three random seeds for the standard model, where computationally feasible

### <font color="#79c0ff">Qualitative</font>

- Fixed prompts
- Fixed seeds
- Multiple sampling temperatures
- Examples of coherent output
- Examples of failure
- Examples resembling memorized training material
- Comparison with Markov output

## <font color="#388bfd">Required Critical Analysis</font>

Answer:

1. What patterns did the model clearly learn?
2. What kinds of context remain difficult?
3. Did the transformer outperform the bigram model?
4. Which component contributed most?
5. Did the model memorize any training passages?
6. Which corpus voices or topics were overrepresented?
7. What uses would be inappropriate?
8. How could generated text misrepresent the source community or scientific domain?
9. What evidence would be required before treating output as factual?
10. How did tokenization affect what the model could learn?

## <font color="#388bfd">Grading Caution</font>

Beating the bigram baseline is the engineering target, but it does not determine the entire grade. A correct implementation may miss the target because of a poor learning rate, too few training steps, unfortunate initialization, corpus noise, inadequate model width, or validation variance. See [Grading](../Docs/grading.md) for the capstone weighting.

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** Better next-token prediction is evidence of improved statistical modeling. It is not proof of reasoning, factual reliability, consciousness, or general intelligence.

## <font color="#388bfd">Stretch Goals</font>

1. Larger Byte Pair Encoding vocabularies
2. Two or more transformer blocks
3. Wider model representations
4. Longer context
5. Weight tying
6. Rotary Position Embedding
7. Nucleus sampling
8. Key–Value cache
9. Mixed-precision experiment
10. Parameter quantization
11. Optional Graphics Processing Unit integration
12. FlashAttention-inspired tiled calculation
13. CPU-versus-GPU benchmark
14. Model compression
15. Distillation, meaning training a smaller model to imitate a larger one
16. Cross-domain transfer experiment
17. Retrieval-assisted prompting using a simple search index
18. Student-designed ablation approved before training

Graphics Processing Unit integration and FlashAttention are advanced systems extensions, not required course components. They may require optional dependencies or hardware unavailable to all students.

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] State the required hypothesis precisely, naming its independent and dependent variables.
- [ ] Explain why held-out evaluation requires a test set no experiment touched during development.
- [ ] List what a corpus report must document and why provenance and license matter.

### <font color="#79c0ff">Intermediate</font>

- [ ] Design an ablation that isolates one component's contribution while holding everything else constant.
- [ ] Fill in the full experimental table for all required models on the same corpus.
- [ ] Find and document one generated passage that resembles memorized training material.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why at least three random seeds are required before trusting a small loss difference.
- [ ] Write an error analysis identifying which kinds of context the transformer still fails to use.
- [ ] Argue, with evidence from your own results, what would be required before treating model output as factual.

---

← [The Machine Writes](../TrainingAndGeneration/) — Back to [Project Strata](../)
