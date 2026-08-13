<div align="center">

# Common Java Architecture
*<font color="#8b949e">The cumulative package structure and the shared interfaces frozen early</font>*

</div>

---

## <font color="#388bfd">Package Structure</font>

A cumulative package structure for the whole course:

```text
src/main/java/strata/
├── corpus/
│   ├── Corpus.java
│   ├── Document.java
│   ├── CorpusSplit.java
│   └── DataCard.java
├── tokenizer/
│   └── Tokenizer.java
├── baseline/
│   ├── LanguageModel.java
│   ├── UniformModel.java
│   ├── UnigramModel.java
│   ├── BigramModel.java
│   ├── MarkovRevisited.java
│   └── EvaluationResult.java
├── reference/
│   ├── attention/
│   │   ├── UniformAttention.java
│   │   ├── RuleBasedAttention.java
│   │   └── DotProductAttention.java
│   ├── network/
│   │   ├── Neuron.java
│   │   ├── Connection.java
│   │   └── Layer.java
│   └── autodiff/
│       └── Value.java
├── math/
│   ├── Matrix.java
│   ├── Parameter.java
│   └── MathOps.java
├── neural/
│   ├── Embedding.java
│   ├── Linear.java
│   ├── ReLU.java
│   ├── RmsNorm.java
│   ├── AttentionHead.java
│   ├── MultiHeadAttention.java
│   ├── FeedForward.java
│   ├── TransformerBlock.java
│   └── TinyTransformer.java
├── training/
│   ├── SoftmaxCrossEntropy.java
│   ├── GradientDescent.java
│   ├── Adam.java
│   ├── Trainer.java
│   └── Checkpoint.java
├── generation/
│   └── Generator.java
└── app/
    ├── Train.java
    ├── Evaluate.java
    └── Generate.java
```

## <font color="#388bfd">Shared Interfaces</font>

An **Application Programming Interface**, abbreviated **API**, is the declared set of classes and methods through which components interact. The cumulative APIs should be frozen early enough that later work connects without repeatedly rewriting prior assignments.

A useful common model interface:

```java
public interface NextTokenModel {
    double[] nextTokenLogits(int[] context);
}
```

Trainable models extend the idea:

```java
public interface TrainableSequenceModel {
    double forwardBackward(int[] input, int[] target);
    List<Parameter> parameters();
    void zeroGradients();
}
```

← Back to [Docs](README.md)
