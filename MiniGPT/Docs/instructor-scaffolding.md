<div align="center">

# Instructor Scaffolding by Chapter
*<font color="#8b949e">What is provided versus what students implement</font>*

</div>

---

Students write the intellectual core, but do not spend their time on unrelated infrastructure.

| Chapter | Instructor provides | Students implement |
|---|---|---|
| 1 | Starter class with file reading, byte-to-token conversion, vocabulary accessor, and merge-rule record | Pair counting, deterministic most-frequent-pair merging, merge-rule recording |
| 2 | Contiguous splitting, generation loop, uniform model, model interface, and evaluation records | Unigram and bigram counting, smoothed probabilities, held-out evaluation, categorical sampling |
| 3 | Tiny vector fixtures | Attention calculations and visualization |
| 4 | Worked loss trace | Softmax, loss, gradient, update |
| 5 | Network diagram and fixed weights | Object model and forward propagation |
| 6 | Complete example trace | Scalar graph and backward traversal |
| 7 | Required matrix API signatures | Numerical operations and explicit gradients |
| 8 | Backward formulas | Trainable single-head implementation |
| 9 | Block diagram and parameter worksheet | Multi-head block and normalization |
| 10 | Checkpoint file specification | Trainer, optimizer, generation |
| 11 | Experiment rubric | Corpus, training, analysis, report |

The distinction is important:

- Students should implement mechanisms that reveal how the model works.
- Students should not lose days inventing file formats, charting packages, or generic tensor abstractions.

← Back to [Docs](README.md)
