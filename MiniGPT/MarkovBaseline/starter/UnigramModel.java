import java.util.List;

public class UnigramModel implements LanguageModel {
    private final int vocabularySize;
    private final double alpha;
    private final long[] counts;
    private long totalCount;

    public UnigramModel(int vocabularySize, double alpha) {
        MarkovRevisited.requireVocabulary(vocabularySize);
        MarkovRevisited.requireAlpha(alpha);
        this.vocabularySize = vocabularySize;
        this.alpha = alpha;
        this.counts = new long[vocabularySize];
    }

    // TODO 1: count each token in the training documents.
    public void train(List<List<Integer>> trainingDocuments) {
        throw new UnsupportedOperationException("TODO 1: unigram training");
    }

    @Override
    public int vocabularySize() {
        return vocabularySize;
    }

    // TODO 2: return the additively smoothed unigram probability.
    @Override
    public double probability(int currentToken, int nextToken) {
        throw new UnsupportedOperationException("TODO 2: unigram probability");
    }
}