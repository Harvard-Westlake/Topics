<div align="center">

# The Machine Writes
*<font color="#8b949e">End-to-end training, an adaptive optimizer, checkpointing, and text generation</font>*

<font color="#a371f7">Learning</font>

</div>

---

> The archive machine finally contains every essential cognitive mechanism, but it is still a laboratory apparatus. It needs a training schedule, a way to sample passages, a way to recover after the program closes, and a disciplined method for turning output scores into generated text. This chapter transforms a network into a complete system.

## <font color="#388bfd">Question to Carry</font>

> **How does a complete language model move from raw documents to trained, reproducible generation?**

## <font color="#388bfd">Vocabulary</font>

| Term | Definition |
|---|---|
| Autoregressive | Producing one output at a time while treating previous outputs as new input. |
| Training loop | Repeatedly selecting examples, calculating loss, computing gradients, and updating parameters. |
| Sequence window | A contiguous subsection of tokenized text used as one training example. |
| Input-target shift | Using tokens $t_0 \ldots t_{n-1}$ as inputs and $t_1 \ldots t_n$ as targets. |
| Optimizer | An algorithm that uses gradients to update parameters. |
| Adaptive Moment Estimation, commonly called Adam | An optimizer maintaining moving averages of gradients and squared gradients. |
| Moment estimate | A running statistical summary used by an optimizer. |
| Bias correction | Adjustment compensating for optimizer buffers beginning at zero. |
| Gradient clipping | Limiting gradient magnitude to reduce unstable updates. |
| Global gradient norm | The combined magnitude of every parameter gradient. |
| Learning-rate schedule | A rule changing learning rate during training. |
| Checkpoint | A saved model, tokenizer, configuration, and training state. |
| Serialization | Converting program state into a storable format. |
| Inference | Using a trained model without calculating training gradients. |
| Greedy decoding | Always selecting the token with the highest predicted probability. |
| Temperature | A value rescaling logits before sampling. |
| Top-k sampling | Sampling only among the `k` highest-scoring tokens. |
| Nucleus sampling or top-p sampling | Sampling from the smallest set of tokens whose cumulative probability reaches a threshold `p`. |
| Beam search | Retaining several high-scoring partial sequences during generation. |
| Random seed | An initial value making pseudorandom behavior reproducible. |
| Early stopping | Ending training when validation performance ceases to improve. |
| Key–Value cache, abbreviated KV cache | Stored attention keys and values from earlier positions, reused during generation. |
| Command-Line Interface, abbreviated CLI | A program operated through typed terminal arguments. |
| Memorization | Reproducing training passages rather than learning patterns that generalize. |
| Generalization | Performing well on examples not used for parameter updates. |

[Adam](https://arxiv.org/abs/1412.6980) uses adaptive estimates of gradient moments and is computationally straightforward, making it suitable after you have already implemented ordinary gradient descent. [Autoregressive generation](https://github.com/andrewtheiss/llm-from-scratch/blob/main/docs/04-text-generation.md) repeatedly predicts one token, appends it, and predicts again; temperature and top-k filtering alter how the next token is sampled from model logits.

## <font color="#388bfd">Assignment Summary</font>

Integrate the tokenizer, dataset loader, transformer model, loss, optimizer, validation, checkpointing, and generation. The result is a runnable Java application.

## <font color="#388bfd">Training Example</font>

Given:

```text
tokens = [t0, t1, t2, t3, t4]
```

use:

```text
input  = [t0, t1, t2, t3]
target = [t1, t2, t3, t4]
```

Every position predicts its following token.

## <font color="#388bfd">Training Loop</font>

```java
for (int step = 0; step < maxSteps; step++) {
    model.zeroGradients();

    double totalLoss = 0.0;

    for (int i = 0; i < accumulationSteps; i++) {
        SequenceWindow window = dataset.sampleTrainingWindow(random);
        totalLoss += model.forwardBackward(window);
    }

    model.scaleGradients(1.0 / accumulationSteps);
    clipGlobalGradientNorm(model.parameters(), maxNorm);
    optimizer.step();

    if (step % validationInterval == 0) {
        evaluateValidationLoss();
    }

    if (step % checkpointInterval == 0) {
        saveCheckpoint();
    }
}
```

## <font color="#388bfd">Optimizer Progression</font>

First prove that ordinary Stochastic Gradient Descent works on a tiny example. Then implement Adam with:

- First-moment buffer
- Second-moment buffer
- Bias correction
- Numerical epsilon
- Per-parameter update
- Gradient reset

## <font color="#388bfd">Checkpoint Contents</font>

Use `DataOutputStream` and `DataInputStream`. The file should contain:

1. File-format version
2. Model configuration
3. Tokenizer vocabulary
4. Byte Pair Encoding merge rules
5. Special-token identifiers
6. Parameter names
7. Parameter shapes
8. Parameter values
9. Adam optimizer buffers
10. Training step
11. Best validation loss
12. Random seed where practical

## <font color="#388bfd">Required Generation Modes</font>

### <font color="#79c0ff">1. Greedy</font>

Choose the greatest logit.

### <font color="#79c0ff">2. Temperature</font>

Divide logits by temperature before softmax:

- Low temperature produces a sharper distribution.
- High temperature produces a flatter distribution.

### <font color="#79c0ff">3. Top-k</font>

Keep only the `k` largest logits.

### <font color="#79c0ff">4. Random categorical sampling</font>

Choose according to resulting probabilities.

## <font color="#388bfd">Suggested Command-Line Interface</font>

```text
java Train \
    --corpus pizzeria/ \
    --merges 128 \
    --context 32 \
    --width 32 \
    --heads 4 \
    --layers 1 \
    --steps 20000 \
    --seed 42
```

```text
java Generate \
    --checkpoint model.bin \
    --prompt "The dough must rest" \
    --tokens 250 \
    --temperature 0.8 \
    --top-k 30 \
    --seed 42
```

## <font color="#388bfd">Detailed Requirements</font>

You must:

1. Sample only from the training split.
2. Prevent sequence windows from silently crossing document boundaries.
3. Build shifted input-target pairs.
4. Accumulate gradients.
5. Apply gradient clipping.
6. Implement ordinary gradient descent.
7. Implement Adam.
8. Measure validation loss periodically.
9. Preserve the best checkpoint.
10. Reload checkpoints.
11. Generate with greedy decoding.
12. Generate with temperature and top-k.
13. Guarantee fixed-seed reproducibility.
14. Compare transformer, bigram, and fixed-context neural model losses.
15. Detect and report non-finite values immediately.

## <font color="#388bfd">Required Tests</font>

- Input-target shift
- Window boundary
- Gradient clipping
- One Adam update against a known calculation
- Checkpoint round-trip
- Identical logits before and after loading
- Identical generated output with same seed
- Different seeds can produce different sampled output
- Greedy decoding is deterministic
- Temperature validation
- Top-k excludes all other tokens
- Validation does not update parameters
- Best-checkpoint selection

## <font color="#388bfd">Misconception Checkpoint</font>

> **Misconception:** Generated fluency is not evidence that the model understands cooking or that its statements are factually correct. A model that writes "bake at 900 degrees for an hour" writes it fluently.

## <font color="#388bfd">Stretch Goals</font>

1. **AdamW:** Adam with decoupled weight decay
2. Linear learning-rate decay
3. Cosine learning-rate schedule
4. Warmup period
5. Early stopping
6. Nucleus sampling
7. Beam search
8. Key–Value cache
9. Weight tying
10. Rotary Position Embedding
11. Multiple transformer blocks
12. Parallel processing of independent sequence windows
13. Generation repetition penalty
14. Model-size and training-step configuration files
15. Interactive terminal generation

---

The machine can now write. The final chapter asks the more important scientific question: does it make better predictions than simpler systems, and what exactly has it learned from the selected archive?

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you construct the shifted input-target pair for a five-token sequence by hand?
- [ ] Can you explain what a checkpoint must contain for generation to be exactly reproducible after reload?
- [ ] Can you describe how temperature changes the sampling distribution at values below and above one?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement one Adam update and verify it against a hand-calculated known result?
- [ ] Can you prevent a sequence window from silently crossing a document boundary and test for it?
- [ ] Can you demonstrate that the same seed reproduces identical generated output across two program runs?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why gradient clipping uses the global norm across all parameters rather than clipping each value independently?
- [ ] Can you explain bias correction in Adam and what would happen in early steps without it?
- [ ] Can you design a check that detects memorized training passages in generated output?

---

← [A Team of Readers](../TransformerBlock/) — Next: [The Trial of the Archive](../Capstone/)
