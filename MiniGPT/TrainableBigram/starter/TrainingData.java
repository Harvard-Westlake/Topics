// PROVIDED — the tokenized order log used throughout the chapter.
//
// Nothing here is random at run time. Both logs are fixed arrays, so every
// count quoted on the lesson page can be checked by eye. The vocabulary is
// deliberately tiny: with three tokens the entire model is nine numbers,
// and you can watch every one of them learn.
public class TrainingData {

    // The vocabulary, in identifier order:
    //   0 = pizza   1 = pineapple   2 = pepperoni
    public static final String[] VOCABULARY = {"pizza", "pineapple", "pepperoni"};

    // The TRAINING log: 122 tokens, 121 transitions. It reads as
    // "pineapple pizza pineapple pizza pepperoni pizza ..." — a topping,
    // the word pizza, another topping, and so on.
    //
    // Exact transition counts (check a few by eye):
    //   pizza     -> pineapple  40      pineapple -> pizza  41
    //   pizza     -> pepperoni  20      pepperoni -> pizza  20
    public static int[] trainingTokens() {
        return new int[] {
            1, 0, 1, 0, 2, 0, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0,
            1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 1, 0, 2, 0, 1, 0, 2, 0, 2, 0,
            1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0,
            1, 0, 2, 0, 2, 0, 1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 1, 0, 2, 0,
            2, 0, 1, 0, 1, 0, 2, 0, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0,
            1, 0
        };
    }

    // The VALIDATION log: 42 tokens, 41 transitions — a later stretch of the
    // same order log. Chapter 2's boundary rule applies unchanged: this data
    // is scored, never trained on. Of its 20 transitions leaving `pizza`,
    // 13 go to pineapple and 7 to pepperoni.
    public static int[] validationTokens() {
        return new int[] {
            1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0,
            1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 2, 0,
            1, 0
        };
    }

    // Chapter 2 review: count current -> next transitions in a token log.
    public static long[][] transitionCounts(int[] tokens, int vocabularySize) {
        long[][] counts = new long[vocabularySize][vocabularySize];
        for (int t = 0; t + 1 < tokens.length; t++) {
            counts[tokens[t]][tokens[t + 1]]++;
        }
        return counts;
    }

    // Chapter 2 review: one row of count-derived next-token probabilities,
    // with additive smoothing. alpha = 0.0 gives the raw observed
    // frequencies — the numbers gradient training converges toward.
    public static double[] countProbabilities(long[][] counts, int currentToken, double alpha) {
        int vocabularySize = counts.length;
        double rowTotal = 0.0;
        for (long count : counts[currentToken]) {
            rowTotal += count;
        }
        double denominator = rowTotal + alpha * vocabularySize;
        if (denominator <= 0.0) {
            throw new IllegalArgumentException(
                "Row " + currentToken + " has no counts and no smoothing.");
        }
        double[] probabilities = new double[vocabularySize];
        for (int j = 0; j < vocabularySize; j++) {
            probabilities[j] = (counts[currentToken][j] + alpha) / denominator;
        }
        return probabilities;
    }
}
