<div align="center">

# Common Acceptance Tests
*<font color="#8b949e">The permanent test suite — these must keep passing as the project grows</font>*

</div>

---

These tests remain in the suite across the entire eleven-chapter sequence:

1. Tokenizer training on a tiny fixture reproduces the expected merges and final tokens exactly.
2. Every probability distribution sums to one.
3. Stable softmax is invariant to adding a constant.
4. Initial random loss is near the uniform-prediction loss.
5. Analytical gradients match finite differences.
6. Gradient contributions from multiple paths are added.
7. Future tokens cannot affect earlier outputs.
8. Multi-head attention with one head matches single-head attention.
9. A tiny model can overfit a tiny corpus.
10. Dense operations match scalar reference operations.
11. Every parameter receives a finite gradient.
12. Checkpoint reload reproduces logits exactly.
13. Fixed seed reproduces sampled generation.
14. Validation does not alter model parameters.
15. The final comparison uses an untouched test set.

← Back to [Docs](README.md)
