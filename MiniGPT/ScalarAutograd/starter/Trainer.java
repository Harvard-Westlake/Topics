// STARTER — the training loop and the experiment bench.
//
// The network (TODOs 8-12) knows how to build a loss graph and wipe its
// parameters' blame. The Value engine (TODOs 1-7) knows how to audit a
// graph. Training happens HERE, and it is yours to write: TODO 13
// assembles one full-batch step out of those parts, and TODO 14 is the
// loop that repeats it. The reporting and the three experiments in main
// are provided — run `java Trainer` once the Tester passes to produce the
// loss trace, the oracle reproduction, and the drumbeat for your
// assignment writeup.
//
// Nothing is random this week. Full-batch training grades every flashcard
// on every step, so there is nothing to draw, no seed to pass, and every
// machine prints the same trace to the last digit.
public class Trainer {

    // TODO 13: one full-batch step of gradient descent.
    //
    // The question: Chapter 4's step drew a random batch. Where did the
    // randomness go?
    // The answer: nowhere it is needed. This week's deck is small enough
    // to grade whole — every step reads all 119 flashcards — so the batch
    // IS the deck. What remains is the lifecycle, in the only order that
    // works:
    //
    //   1. network.zeroGradients()                       Reset   (TODO 12)
    //   2. Value averageLoss =
    //          network.averageLossValue(trainingHistory) Forecast + Grade
    //   3. averageLoss.backward()                        Measure (TODO 7)
    //   4. for each parameter in network.parameters():   Nudge
    //          parameter.setNumber(parameter.number()
    //              - learningRate * parameter.gradient());
    //   5. return averageLoss.number();
    //
    // Why that return value: the graph's number was computed BEFORE the
    // nudge, so a step reports the loss it stood on, not the loss it
    // stepped to. The Tester checks exactly that.
    //
    // Dimensions:
    // - network:         the model being trained — the only thing altered
    // - trainingHistory: the token history to learn from — read only
    // - learningRate:    Chapter 4's stride, unchanged
    // - returns:         the average loss the step was computed at
    //
    // Machine-verified: from the frozen start with learning rate 0.5,
    // this returns 0.3957, and the training loss immediately after is
    // 0.3754.
    public static double gradientDescentStep(TrainableFeatureNetwork network,
                                             int[] trainingHistory, double learningRate) {
        throw new UnsupportedOperationException("TODO 13: gradientDescentStep");
    }

    // Run `steps` full-batch updates. When reportEvery > 0, print a CSV
    // loss trace — copy those lines into a .csv file for the assignment's
    // evidence; no plotting library is required.
    //
    // The two histories play different roles: trainingHistory is learned
    // on; validationHistory is only ever handed to report(), which only
    // grades — Chapter 2's boundary rule, kept by the code's shape itself.
    public static void train(TrainableFeatureNetwork network,
                             int[] trainingHistory, int[] validationHistory,
                             int steps, double learningRate, int reportEvery) {
        // PROVIDED — the step-0 report: where the network stands before
        // any training.
        if (reportEvery > 0) {
            System.out.println("step,training loss,validation loss");
            report(network, 0, trainingHistory, validationHistory);
        }

        // TODO 14: the main training loop.
        //
        // The question: one step lowers the loss a little. Where does the
        // actual learning live?
        // The answer: nowhere else — learning IS this loop. The same
        // step, repeated, each one starting from wherever the last one
        // left the 49 numbers.
        //
        // For step = 1 up to and including `steps`:
        //   1. take one gradientDescentStep on trainingHistory with this
        //      method's learningRate
        //   2. if reportEvery > 0 and step is a multiple of reportEvery
        //      (step % reportEvery == 0), print one trace line with
        //      report(network, step, trainingHistory, validationHistory)
        //
        // Machine-verified: from the frozen start (120 steps, learning
        // rate 0.5, reportEvery 10) the trace the step-0 line began
        // continues  10,0.3301,0.3345  — a hair above Chapter 4's table —
        // and ends  120,0.3181,0.3222  — past the table, at the floor.
        throw new UnsupportedOperationException("TODO 14: the training loop in train");
    }

    // PROVIDED — one CSV line of the loss trace. Grading only: it builds
    // graphs and reads their numbers, and no receipt is ever audited.
    private static void report(TrainableFeatureNetwork network, int step,
                               int[] trainingHistory, int[] validationHistory) {
        System.out.printf("%d,%.4f,%.4f%n",
                step, network.averageLossNumber(trainingHistory),
                network.averageLossNumber(validationHistory));
    }

    // PROVIDED — the largest distance between this network's numbers and
    // the frozen Chapter 5 fixture, across all 49 parameters. Used by the
    // oracle experiment: rounding to two decimals moves a number at most
    // 0.005, so reproducing the oracle means landing within that of every
    // frozen value.
    public static double maxGapToFrozen(TrainableFeatureNetwork network) {
        double gap = 0.0;
        gap = Math.max(gap, maxGap(network.statCardNumbers(), AutogradFixtures.statCards()));
        gap = Math.max(gap, maxGap(network.hiddenWeightNumbers(), AutogradFixtures.hiddenWeights()));
        gap = Math.max(gap, maxGap(new double[][] {network.hiddenBiasNumbers()},
                new double[][] {AutogradFixtures.hiddenBiases()}));
        gap = Math.max(gap, maxGap(network.outputWeightNumbers(), AutogradFixtures.outputWeights()));
        gap = Math.max(gap, maxGap(new double[][] {network.outputBiasNumbers()},
                new double[][] {AutogradFixtures.outputBiases()}));
        return gap;
    }

    private static double maxGap(double[][] trained, double[][] frozen) {
        double gap = 0.0;
        for (int rowNumber = 0; rowNumber < trained.length; rowNumber++) {
            for (int slot = 0; slot < trained[rowNumber].length; slot++) {
                gap = Math.max(gap, Math.abs(trained[rowNumber][slot] - frozen[rowNumber][slot]));
            }
        }
        return gap;
    }

    private static String formatRow(double[] row) {
        StringBuilder builder = new StringBuilder("[");
        for (int entry = 0; entry < row.length; entry++) {
            builder.append(String.format("%.4f", row[entry]));
            if (entry < row.length - 1) {
                builder.append(", ");
            }
        }
        return builder.append("]").toString();
    }

    // PROVIDED — the three experiments for the assignment writeup.
    public static void main(String[] args) {
        int[] trainingHistory = AutogradFixtures.trainingTokens();
        int[] validationHistory = AutogradFixtures.validationTokens();

        System.out.println("=== The worked run: 120 full-batch steps from the frozen weights, learning rate 0.5 ===");
        TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
        train(network, trainingHistory, validationHistory, 120, 0.5, 10);
        System.out.printf("after pizza:      %s   counted: %s%n",
                formatRow(network.forecast(new int[] {0, 1, 0})),
                formatRow(AutogradFixtures.countedRowAfterPizza()));
        System.out.printf("cards now: pizza %s pineapple %s pepperoni %s%n",
                formatRow(network.statCardNumbers()[0]),
                formatRow(network.statCardNumbers()[1]),
                formatRow(network.statCardNumbers()[2]));

        System.out.println("\n=== Reproduce the oracle: 10 steps from the fresh offline start ===");
        TrainableFeatureNetwork fresh = AutogradFixtures.freshStart();
        System.out.printf("fresh init loss: %.4f   (worse than the empty network's 1.0986)%n",
                fresh.averageLossNumber(trainingHistory));
        train(fresh, trainingHistory, validationHistory, 10, 0.5, 0);
        System.out.printf("after 10 steps:  %.4f%n", fresh.averageLossNumber(trainingHistory));
        System.out.printf("largest gap to any frozen Chapter 5 number: %.6f   (rounding bound: 0.005)%n",
                maxGapToFrozen(fresh));

        System.out.println("\n=== The drumbeat: retrain the frozen network on 0,1,2 repeated ===");
        int[] drumbeat = AutogradFixtures.drumbeatTokens();
        TrainableFeatureNetwork drummer = AutogradFixtures.frozenStart();
        System.out.printf("drumbeat loss before: %.4f%n", drummer.averageLossNumber(drumbeat));
        train(drummer, drumbeat, drumbeat, 50, 0.5, 0);
        System.out.printf("drumbeat loss after 50 steps: %.4f   pizzeria training loss now: %.4f%n",
                drummer.averageLossNumber(drumbeat), drummer.averageLossNumber(trainingHistory));
        System.out.printf("forecast after [0,1,2]: %s%n",
                formatRow(drummer.forecast(new int[] {0, 1, 2})));
    }
}
