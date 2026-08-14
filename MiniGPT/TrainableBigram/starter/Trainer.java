import java.util.Random;

// PROVIDED — the training loop and the experiment bench.
//
// You implement the physics inside the model (TODOs 1-7); this class only
// drives it, one training step at a time: reset, accumulate a batch,
// average, step. Run `java Trainer` after the Tester passes to produce the
// loss trace, the learned-versus-counted table, and the learning-rate
// experiment for your assignment writeup.
public class Trainer {

    // One training step = one parameter update built from `batchSize`
    // examples drawn at random from the log — the "stochastic" in
    // Stochastic Gradient Descent.
    public static void sgdStep(TrainableBigramModel model, int[] tokens,
                               int batchSize, double learningRate, Random random) {
        model.zeroGradients();
        for (int b = 0; b < batchSize; b++) {
            int t = random.nextInt(tokens.length - 1);
            model.backward(tokens[t], tokens[t + 1]);
        }
        model.step(learningRate);
    }

    // Run `steps` updates. When reportEvery > 0, print a CSV loss trace —
    // copy those lines into a .csv file for the assignment's evidence; no
    // plotting library is required. Everything is deterministic: the same
    // seeds must reproduce the same trace, digit for digit.
    public static void train(TrainableBigramModel model,
                             int[] trainTokens, int[] validationTokens,
                             int steps, int batchSize, double learningRate,
                             int reportEvery, long seed) {
        Random random = new Random(seed);
        if (reportEvery > 0) {
            System.out.println("step,training loss,validation loss");
            report(model, 0, trainTokens, validationTokens);
        }
        for (int step = 1; step <= steps; step++) {
            sgdStep(model, trainTokens, batchSize, learningRate, random);
            if (reportEvery > 0 && step % reportEvery == 0) {
                report(model, step, trainTokens, validationTokens);
            }
        }
    }

    private static void report(TrainableBigramModel model, int step,
                               int[] trainTokens, int[] validationTokens) {
        System.out.printf("%d,%.4f,%.4f%n",
                step, model.averageLoss(trainTokens), model.averageLoss(validationTokens));
    }

    // Print the learned table next to Chapter 2's count-derived table.
    // alpha = 0 here on purpose: raw frequencies are what gradient descent
    // converges toward.
    public static void printComparison(TrainableBigramModel model, int[] trainTokens) {
        long[][] counts = TrainingData.transitionCounts(trainTokens, model.vocabularySize());
        System.out.println();
        System.out.printf("  %-12s  %-28s  %s%n",
                "row", "learned from gradients", "counted from the log");
        for (int i = 0; i < model.vocabularySize(); i++) {
            System.out.printf("  %-12s  %-28s  %s%n",
                    TrainingData.VOCABULARY[i],
                    formatRow(model.probabilities(i)),
                    formatRow(TrainingData.countProbabilities(counts, i, 0.0)));
        }
        System.out.println();
    }

    private static String formatRow(double[] row) {
        StringBuilder builder = new StringBuilder("[");
        for (int j = 0; j < row.length; j++) {
            builder.append(String.format("%.3f", row[j]));
            if (j < row.length - 1) {
                builder.append(", ");
            }
        }
        return builder.append("]").toString();
    }

    // The full experiment for the assignment writeup.
    public static void main(String[] args) {
        int[] train = TrainingData.trainingTokens();
        int[] validation = TrainingData.validationTokens();

        System.out.println("=== The worked loss trace: 300 steps, batch 24, learning rate 0.5 ===");
        TrainableBigramModel model = new TrainableBigramModel(TrainingData.VOCABULARY.length, 7);
        train(model, train, validation, 300, 24, 0.5, 30, 42);
        printComparison(model, train);

        System.out.println("=== The learning-rate experiment: same seeds, 300 steps, batch 24 ===");
        for (double learningRate : new double[] {0.01, 0.5, 20.0}) {
            TrainableBigramModel fresh = new TrainableBigramModel(TrainingData.VOCABULARY.length, 7);
            train(fresh, train, validation, 300, 24, learningRate, 0, 42);
            System.out.printf("  learning rate %6.2f -> final training loss %.4f   validation loss %.4f%n",
                    learningRate, fresh.averageLoss(train), fresh.averageLoss(validation));
        }
    }
}
