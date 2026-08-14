import java.util.Random;

// The first machine in this course that changes its own numbers.
//
// The entire model is one table of logits — logits[currentToken][nextToken].
// A second table of the same shape accumulates gradients between updates.
// Chapter 2's bigram table held counts; Chapter 3's spotlight followed rules
// you wrote. Every number in THIS table is adjusted by the training loop,
// using nothing but the gradient of the model's own loss.
public class TrainableBigramModel {

    private final int vocabularySize;
    private final double[][] logits;
    private final double[][] gradients;
    private int examplesSinceReset = 0;

    // PROVIDED — every logit starts as a small random number near zero.
    // Small matters: near-equal logits make each row's softmax nearly
    // uniform, so a fresh table's average loss sits right at ln(V) —
    // Chapter 2's uniform anchor, and the Tester's first training check.
    public TrainableBigramModel(int vocabularySize, long seed) {
        if (vocabularySize <= 0) {
            throw new IllegalArgumentException("Vocabulary size must be positive.");
        }
        this.vocabularySize = vocabularySize;
        this.logits = new double[vocabularySize][vocabularySize];
        this.gradients = new double[vocabularySize][vocabularySize];
        Random random = new Random(seed);
        for (int i = 0; i < vocabularySize; i++) {
            for (int j = 0; j < vocabularySize; j++) {
                logits[i][j] = 0.02 * random.nextGaussian();
            }
        }
    }

    public int vocabularySize() {
        return vocabularySize;
    }

    // TODO 1: stable softmax — the same three steps you built in Chapter 3,
    // rebuilt here so this class stands alone.
    //
    // Dimensions:
    // - row:     length-n vector of logits; any real numbers.
    // - returns: NEW length-n vector — the input must not be mutated.
    //            Every entry positive (never exactly zero), summing to ~1.
    //
    // Three steps, always in this order:
    //   1. find the maximum entry and subtract it from every entry
    //      (prevents Math.exp from overflowing; changes nothing else),
    //   2. exponentiate each shifted entry with Math.exp,
    //   3. divide each result by the sum of all the results.
    //
    // Example from the lesson: the worked row [1.2, 0.1, -0.4]
    //   subtract max (1.2):   [ 0.0,    -1.1,    -1.6  ]
    //   exponentiate:         [ 1.0000,  0.3329,  0.2019]
    //   divide by sum 1.5348: [ 0.6516,  0.2169,  0.1315]
    public static double[] stableSoftmax(double[] row) {
        throw new UnsupportedOperationException("TODO 1: stable softmax");
    }

    // TODO 2: one row of the table, read as a prediction distribution.
    //
    // Dimensions:
    // - currentToken: an int in [0, vocabularySize) — which row to read.
    // - returns:      NEW length-V vector of next-token probabilities.
    //
    // Return the stable softmax of logits[currentToken]. Reading a
    // prediction must never change the table: no logit moves, and calling
    // this twice returns identical answers.
    //
    // Example from the lesson: if the row for pizza (token 0) holds
    // [1.2, 0.1, -0.4], then probabilities(0) forecasts
    // [0.6516, 0.2169, 0.1315] — 65% pizza, 22% pineapple, 13% pepperoni.
    //
    // Call requireToken(currentToken) first.
    public double[] probabilities(int currentToken) {
        throw new UnsupportedOperationException("TODO 2: probabilities");
    }

    // TODO 3: cross-entropy loss for one example — Chapter 2's penalty,
    // charged to a single prediction.
    //
    // Dimensions:
    // - currentToken: the flashcard's front — which row made the forecast.
    // - targetToken:  the flashcard's back — what the log actually showed.
    // - returns:      one double, 0 for certainty in the truth and growing
    //                 as the model is more surprised.
    //
    //   loss = -Math.log( probabilities(currentToken)[targetToken] )
    //
    // Examples from the lesson:
    //   row [1.2, 0.1, -0.4], target pineapple (1): -ln(0.2169) = 1.5284
    //   row [0, 0, 0], any target: -ln(1/3) = 1.0986 — the ln(V) anchor
    //
    // Call requireToken on both tokens first.
    public double loss(int currentToken, int targetToken) {
        throw new UnsupportedOperationException("TODO 3: loss");
    }

    // TODO 4: the shortcut gradient, accumulated.
    // Computes "prediction minus one-hot" for one flashcard and pours it
    // into the gradient bucket. Backward measures; step moves.
    //
    // Dimensions:
    // - gradients is (V x V), same shape as logits — but this method
    //   touches ONE row of it: gradients[currentToken]. No other row of
    //   the loss depends on this flashcard, and no logit changes here.
    //
    // With p = probabilities(currentToken), for every column j:
    //   gradients[currentToken][j] += p[j] - (j == targetToken ? 1.0 : 0.0)
    // then increment examplesSinceReset. The += is the accumulation: a
    // batch calls backward many times before one step.
    //
    // Example from the lesson: row [1.2, 0.1, -0.4], target pineapple (1)
    //   p:              [ 0.6516,   0.2169,   0.1315 ]
    //   one-hot target: [ 0,        1,        0      ]
    //   added to row:   [ 0.6516,  -0.7831,   0.1315 ]   (sums to zero)
    //
    // Call requireToken on both tokens first.
    public void backward(int currentToken, int targetToken) {
        throw new UnsupportedOperationException("TODO 4: backward");
    }

    // TODO 5: the update — one stride of gradient descent.
    // Averages the accumulated gradients and moves every logit against
    // its slope.
    //
    // For every entry of the table:
    //   logits[i][j] -= learningRate * gradients[i][j] / examplesSinceReset
    //
    // The division averages the batch: 24 accumulated flashcards summed
    // would be one gradient ~24 times louder, and batch size would secretly
    // scale the stride. Rows that accumulated nothing hold gradient 0.0
    // and therefore do not move. Do not reset anything here — resetting is
    // zeroGradients' job, and the Trainer calls the two separately.
    //
    // Example from the lesson: after one backward on the worked row,
    // step(0.5) moves it
    //   [1.2, 0.1, -0.4]  ->  [0.8742, 0.4916, -0.4658]
    // and the loss falls 1.5284 -> 1.0474.
    //
    // Call requireExamples() first.
    public void step(double learningRate) {
        throw new UnsupportedOperationException("TODO 5: step");
    }

    // TODO 6: reset — wipe the bucket between updates.
    // Set every entry of gradients to 0.0 and examplesSinceReset to 0.
    //
    // Why this exists: a gradient is a snapshot of the table AS IT WAS
    // when backward ran. The moment step moves the logits, every
    // accumulated slope is stale. Forgetting this reset is the classic
    // silent training bug — old slopes contaminate every later step.
    public void zeroGradients() {
        throw new UnsupportedOperationException("TODO 6: zero gradients");
    }

    // TODO 7: Chapter 2's evaluation, one method.
    //
    // Dimensions:
    // - tokens:  a log of n tokens — which contains n - 1 flashcards,
    //            one per adjacent pair.
    // - returns: the mean of loss(tokens[t], tokens[t + 1]) over
    //            t = 0 .. tokens.length - 2.
    //
    // Examples from the lesson:
    //   {1, 0, 1} averages exactly two losses: loss(1,0) and loss(0,1).
    //   A fresh table (seed 7) on the full training log scores 1.0987 —
    //   ln(3) to three decimals, Chapter 2's uniform anchor.
    //
    // Call requireLog(tokens) first.
    public double averageLoss(int[] tokens) {
        throw new UnsupportedOperationException("TODO 7: average loss");
    }

    // ---------------------------------------------------------------
    // PROVIDED helpers — used by the Tester; do not modify.
    // ---------------------------------------------------------------

    // Overwrite one row of logits. The Tester uses this to reproduce the
    // lesson's worked traces exactly; your training code never needs it.
    public void setRow(int currentToken, double... row) {
        requireToken(currentToken);
        if (row.length != vocabularySize) {
            throw new IllegalArgumentException(
                "Row needs " + vocabularySize + " entries, got " + row.length);
        }
        logits[currentToken] = row.clone();
    }

    // Defensive copies for tests and printing.
    public double[] logitRow(int currentToken) {
        requireToken(currentToken);
        return logits[currentToken].clone();
    }

    public double[] gradientRow(int currentToken) {
        requireToken(currentToken);
        return gradients[currentToken].clone();
    }

    // PROVIDED validators — call these where the TODO comments say to.

    public void requireToken(int token) {
        if (token < 0 || token >= vocabularySize) {
            throw new IllegalArgumentException(
                "Token " + token + " is outside [0, " + vocabularySize + ").");
        }
    }

    public void requireExamples() {
        if (examplesSinceReset == 0) {
            throw new IllegalStateException(
                "step called with no accumulated examples — call backward first.");
        }
    }

    public static void requireLog(int[] tokens) {
        if (tokens == null || tokens.length < 2) {
            throw new IllegalArgumentException(
                "A token log needs at least two tokens to form one transition.");
        }
    }
}
