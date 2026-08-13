import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class MarkovRevisited {

    // PROVIDED: split each document into contiguous 80/10/10 sections.
    public static CorpusSplit splitDocuments(List<List<Integer>> documents) {
        List<List<Integer>> training = new ArrayList<>();
        List<List<Integer>> validation = new ArrayList<>();
        List<List<Integer>> test = new ArrayList<>();

        for (List<Integer> document : documents) {
            int n = document.size();
            int trainEnd = (int) Math.floor(n * 0.80);
            int validationEnd = (int) Math.floor(n * 0.90);

            training.add(copyRange(document, 0, trainEnd));
            validation.add(copyRange(document, trainEnd, validationEnd));
            test.add(copyRange(document, validationEnd, n));
        }

        return new CorpusSplit(training, validation, test);
    }

    private static List<Integer> copyRange(List<Integer> source, int from, int to) {
        return new ArrayList<>(source.subList(from, to));
    }

    // TODO 5: compute negative log-likelihood on held-out documents.
    // Use positions 1..n-1 so all three models are evaluated on the same targets.
    public static EvaluationResult evaluate(
            LanguageModel model,
            List<List<Integer>> documents) {

        throw new UnsupportedOperationException("TODO 5: evaluation");
    }

    // TODO 6: draw one token from the categorical next-token distribution.
    public static int sampleNext(LanguageModel model, int currentToken, Random random) {
        throw new UnsupportedOperationException("TODO 6: categorical sampling");
    }

    // PROVIDED: generation repeatedly samples from the final token in the prompt.
    public static List<Integer> generate(
            LanguageModel model,
            List<Integer> prompt,
            int newTokens,
            long seed) {

        if (prompt.isEmpty()) {
            throw new IllegalArgumentException("Prompt must contain at least one token.");
        }
        if (newTokens < 0) {
            throw new IllegalArgumentException("newTokens must be nonnegative.");
        }

        List<Integer> output = new ArrayList<>(prompt);
        Random random = new Random(seed);

        for (int i = 0; i < newTokens; i++) {
            int current = output.get(output.size() - 1);
            int next = sampleNext(model, current, random);
            output.add(next);
        }

        return output;
    }

    public static void requireVocabulary(int vocabularySize) {
        if (vocabularySize <= 0) {
            throw new IllegalArgumentException("Vocabulary size must be positive.");
        }
    }

    public static void requireAlpha(double alpha) {
        if (alpha <= 0.0) {
            throw new IllegalArgumentException("alpha must be greater than zero.");
        }
    }

    public static void requireToken(int token, int vocabularySize) {
        if (token < 0 || token >= vocabularySize) {
            throw new IllegalArgumentException("Invalid token ID: " + token);
        }
    }
}