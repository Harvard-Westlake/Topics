public interface LanguageModel {
    int vocabularySize();
    double probability(int currentToken, int nextToken);
}