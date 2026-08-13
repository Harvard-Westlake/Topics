public class UniformModel implements LanguageModel {
    private final int vocabularySize;

    public UniformModel(int vocabularySize) {
        MarkovRevisited.requireVocabulary(vocabularySize);
        this.vocabularySize = vocabularySize;
    }

    @Override
    public int vocabularySize() {
        return vocabularySize;
    }

    @Override
    public double probability(int currentToken, int nextToken) {
        MarkovRevisited.requireToken(nextToken, vocabularySize);
        return 1.0 / vocabularySize;
    }
}