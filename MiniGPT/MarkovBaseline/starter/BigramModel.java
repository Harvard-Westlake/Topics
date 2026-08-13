import java.util.List;

public class BigramModel implements LanguageModel {
    private final int vocabularySize;
    private final double alpha;
    private final long[][] counts;
    private final long[] rowTotals;

    public BigramModel(int vocabularySize, double alpha) {
        MarkovRevisited.requireVocabulary(vocabularySize);
        MarkovRevisited.requireAlpha(alpha);
        this.vocabularySize = vocabularySize;
        this.alpha = alpha;
        this.counts = new long[vocabularySize][vocabularySize];
        this.rowTotals = new long[vocabularySize];
    }

    // TODO 3: count every training transition current -> next.
    public void train(List<List<Integer>> trainingDocuments) {
        throw new UnsupportedOperationException("TODO 3: bigram training");
    }

    @Override
    public int vocabularySize() {
        return vocabularySize;
    }

    // TODO 4: return P(next | current) with additive smoothing.
    @Override
    public double probability(int currentToken, int nextToken) {
        throw new UnsupportedOperationException("TODO 4: bigram probability");
    }
}