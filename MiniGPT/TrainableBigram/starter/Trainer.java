import java.util.Random;

// STARTER — the training loop and the experiment bench.
//
// The model (TODOs 1-7) knows how to forecast, grade one flashcard, record
// a slope, and take one averaged stride. None of that is training yet.
// Training happens HERE, and it is yours to write: TODO 8 assembles one
// step of Stochastic Gradient Descent out of the model's parts, and TODO 9
// is the loop that repeats it until the table has learned. The reporting,
// the learned-versus-counted table, and the experiment bench in main are
// provided — run `java Trainer` once the Tester passes to produce the loss
// trace and the learning-rate experiment for your assignment writeup.
public class Trainer {

    // TODO 8: one training step of Stochastic Gradient Descent.
    //
    // The question: the model can grade one flashcard and remember one
    // slope. How do single grades become one careful update to the table?
    // The answer: the five-beat rhythm from the lesson page — wipe the
    // bucket, pour in a small random handful of grades, take one averaged
    // stride. The handful is the batch, and drawing it at random is the
    // "stochastic" in Stochastic Gradient Descent: no single step sees the
    // whole deck, but the average over many steps points downhill.
    //
    // Dimensions:
    // - model:           the table being trained — the ONLY thing this
    //                    method alters; its TODOs 1-7 do the physics
    // - trainingHistory: the token history to learn from — read, never
    //                    changed; length n holds n - 1 flashcards, and the
    //                    flashcard starting at position f is the pair
    //                    (trainingHistory[f], trainingHistory[f + 1])
    // - batchSize:       how many flashcards to grade into this one update
    // - learningRate:    handed straight to model.step
    // - random:          the run's ONE random number source — draw from it,
    //                    never create your own
    //
    // The recipe, in order — each beat is a lifecycle stage you already
    // built in the model:
    //
    //   1. model.zeroGradients()                     Reset           (TODO 6)
    //   2. batchSize times:                          Measure         (TODO 4)
    //        int flashcardStart = random.nextInt(trainingHistory.length - 1);
    //        model.accumulateGradients(trainingHistory[flashcardStart],
    //                                  trainingHistory[flashcardStart + 1]);
    //   3. model.step(learningRate)                  average + Nudge (TODO 5)
    //
    // Why `trainingHistory.length - 1`: the last token has no next-door
    // neighbor, so it cannot start a flashcard — 122 training tokens hold
    // 121 flashcards, at starts 0 through 120.
    //
    // Determinism warning: exactly ONE random.nextInt call per flashcard, in
    // this order. The whole run is seeded, and the Tester checks the loss
    // trace digit for digit — an extra, missing, or reordered draw produces
    // a plausible-looking trace that is wrong everywhere.
    //
    // Machine-verified example, from the worked run (model seed 7, training
    // seed 42, batch 24, learning rate 0.5): the first three draws are
    // flashcardStart 117, 15, 96 — the flashcards pizza -> pepperoni,
    // pizza -> pepperoni, pineapple -> pizza — and after this one step the
    // average training loss has already fallen 1.0987 -> 1.0279.
    public static void stochasticGradientDescentStep(
            TrainableBigramModel model, int[] trainingHistory,
            int batchSize, double learningRate, Random random) {
        throw new UnsupportedOperationException("TODO 8: stochasticGradientDescentStep");
    }

    // Run `steps` updates. When reportEvery > 0, print a CSV loss trace —
    // copy those lines into a .csv file for the assignment's evidence; no
    // plotting library is required. Everything is deterministic: the same
    // seeds must reproduce the same trace, digit for digit.
    //
    // The two histories play different roles: trainingHistory is drawn from
    // and learned on; validationHistory is only ever handed to report(),
    // which only grades — Chapter 2's boundary rule, kept by the code's
    // shape itself.
    public static void train(TrainableBigramModel model,
                             int[] trainingHistory, int[] validationHistory,
                             int steps, int batchSize, double learningRate,
                             int reportEvery, long seed) {
        // PROVIDED — one Random for the WHOLE run, born from the seed and
        // threaded through every step. That single shared source is what
        // makes the run reproducible; a fresh Random inside the loop would
        // restart the sequence and feed every step the same flashcards.
        Random random = new Random(seed);

        // PROVIDED — the step-0 report: the untrained table's ln(V) anchor,
        // printed before any training has happened.
        if (reportEvery > 0) {
            System.out.println("step,training loss,validation loss");
            report(model, 0, trainingHistory, validationHistory);
        }

        // TODO 9: the main training loop.
        //
        // The question: one step barely moves the table. Where does the
        // actual learning live?
        // The answer: nowhere else — learning IS this loop. There is no
        // extra cleverness above the step: the same small update, repeated,
        // each step starting from wherever the last one left the table.
        //
        // For step = 1 up to and including `steps`:
        //   1. take one stochasticGradientDescentStep on trainingHistory,
        //      passing this method's batchSize and learningRate and the
        //      SAME `random` created above
        //   2. if reportEvery > 0 and step is a multiple of reportEvery
        //      (step % reportEvery == 0), print one trace line with
        //      report(model, step, trainingHistory, validationHistory)
        //
        // Machine-verified: the worked run (300 steps, batch 24, learning
        // rate 0.5, model seed 7, training seed 42) continues the trace the
        // step-0 line began — its first reported line is  30,0.4645,0.4668
        // and its last is  300,0.3300,0.3311  — matching the lesson page
        // digit for digit.
        throw new UnsupportedOperationException("TODO 9: the training loop in train");
    }

    // PROVIDED — one CSV line of the loss trace. Grading only: averageLoss
    // reads the table and changes nothing, so reporting never trains.
    private static void report(TrainableBigramModel model, int step,
                               int[] trainingHistory, int[] validationHistory) {
        System.out.printf("%d,%.4f,%.4f%n",
                step, model.averageLoss(trainingHistory), model.averageLoss(validationHistory));
    }

    // PROVIDED — print the learned table next to Chapter 2's count-derived
    // table. alpha = 0 here on purpose: raw frequencies are what gradient
    // descent converges toward.
    public static void printComparison(TrainableBigramModel model, int[] trainingHistory) {
        long[][] counts = TrainingData.transitionCounts(trainingHistory, model.vocabularySize());
        System.out.println();
        System.out.printf("  %-12s  %-28s  %s%n",
                "row", "learned from gradients", "counted from the history");
        for (int currentToken = 0; currentToken < model.vocabularySize(); currentToken++) {
            System.out.printf("  %-12s  %-28s  %s%n",
                    TrainingData.VOCABULARY[currentToken],
                    formatRow(model.probabilities(currentToken)),
                    formatRow(TrainingData.countProbabilities(counts, currentToken, 0.0)));
        }
        System.out.println();
    }

    private static String formatRow(double[] row) {
        StringBuilder builder = new StringBuilder("[");
        for (int nextToken = 0; nextToken < row.length; nextToken++) {
            builder.append(String.format("%.3f", row[nextToken]));
            if (nextToken < row.length - 1) {
                builder.append(", ");
            }
        }
        return builder.append("]").toString();
    }

    // PROVIDED — the full experiment for the assignment writeup.
    public static void main(String[] args) {
        int[] trainingHistory = TrainingData.trainingTokens();
        int[] validationHistory = TrainingData.validationTokens();

        System.out.println("=== The worked loss trace: 300 steps, batch 24, learning rate 0.5 ===");
        TrainableBigramModel model = new TrainableBigramModel(TrainingData.VOCABULARY.length, 7);
        train(model, trainingHistory, validationHistory, 300, 24, 0.5, 30, 42);
        printComparison(model, trainingHistory);

        System.out.println("=== The learning-rate experiment: same seeds, 300 steps, batch 24 ===");
        for (double learningRate : new double[] {0.01, 0.5, 20.0}) {
            TrainableBigramModel retrained = new TrainableBigramModel(TrainingData.VOCABULARY.length, 7);
            train(retrained, trainingHistory, validationHistory, 300, 24, learningRate, 0, 42);
            System.out.printf("  learning rate %6.2f -> final training loss %.4f   validation loss %.4f%n",
                    learningRate, retrained.averageLoss(trainingHistory),
                    retrained.averageLoss(validationHistory));
        }
    }
}
