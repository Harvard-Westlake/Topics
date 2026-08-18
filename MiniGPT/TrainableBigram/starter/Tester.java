import java.util.Arrays;
import java.util.Random;

// PROVIDED — reproduces every worked trace from the lesson page and runs the
// required tests. Complete the TODOs in order and rerun after each one:
// stages you have not implemented yet are reported as TODO, not FAIL.
public class Tester {

    public static void main(String[] args) {
        System.out.println("=== Part 1 (Day 1): softmax, probabilities, loss ===");
        testSoftmax();
        testProbabilities();
        testLoss();

        System.out.println("\n=== Part 2 (Day 2): gradient, update, training ===");
        testAccumulateGradients();
        testGradientCheck();
        testStep();
        testAccumulation();
        testReproducibility();
        testAverageLoss();
        testStochasticGradientDescentStep();
        runTraining();
    }

    // ----- Part 1 -----------------------------------------------------

    private static void testSoftmax() {
        try {
            double[] chapterThree = {2.0, 1.0, 0.0};
            double[] result = TrainableBigramModel.stableSoftmax(chapterThree);
            check("softmax: [2,1,0] -> [0.6652, 0.2447, 0.0900] (Chapter 3's trace)",
                    approxRow(result, 0.6652, 0.2447, 0.0900));
            check("softmax: input array was not mutated",
                    Arrays.equals(chapterThree, new double[] {2.0, 1.0, 0.0}));

            double[] newborn = TrainableBigramModel.stableSoftmax(new double[] {0.017, -0.023, 0.008});
            check("softmax: newborn row [0.017, -0.023, 0.008] -> [0.3388, 0.3255, 0.3357] — a shrug",
                    approxRow(newborn, 0.3388, 0.3255, 0.3357));

            double[] worked = TrainableBigramModel.stableSoftmax(new double[] {1.2, 0.1, -0.4});
            check("softmax: worked row [1.2, 0.1, -0.4] -> [0.6516, 0.2169, 0.1315]",
                    approxRow(worked, 0.6516, 0.2169, 0.1315));
            check("softmax: entries sum to one", approx(worked[0] + worked[1] + worked[2], 1.0));

            double[] huge = TrainableBigramModel.stableSoftmax(new double[] {1000.0, 999.0, 998.0});
            check("softmax: huge logits do not overflow — [1000,999,998] matches [2,1,0]",
                    approxRow(huge, 0.6652, 0.2447, 0.0900));

            double[] a = TrainableBigramModel.stableSoftmax(new double[] {5.0, 1.0, 1.0});
            double[] b = TrainableBigramModel.stableSoftmax(new double[] {9.0, 5.0, 5.0});
            check("softmax: adding a constant to every logit changes nothing",
                    approxRow(b, a[0], a[1], a[2]));

            double[] equal = TrainableBigramModel.stableSoftmax(new double[] {0.0, 0.0, 0.0});
            check("softmax: equal logits give the uniform model — a third each",
                    approxRow(equal, 1.0 / 3, 1.0 / 3, 1.0 / 3));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testProbabilities() {
        try {
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            boolean nearUniform = true;
            for (int currentToken = 0; currentToken < 3; currentToken++) {
                double[] p = model.probabilities(currentToken);
                check("probabilities: nearly empty row " + currentToken + " sums to one",
                        approx(p[0] + p[1] + p[2], 1.0));
                for (double entry : p) {
                    nearUniform &= Math.abs(entry - 1.0 / 3) < 0.03;
                }
            }
            check("probabilities: a nearly empty table is nearly uniform (every entry within 0.03 of 1/3)",
                    nearUniform);

            model.setRow(0, 1.2, 0.1, -0.4);
            check("probabilities: worked row reproduces [0.6516, 0.2169, 0.1315]",
                    approxRow(model.probabilities(0), 0.6516, 0.2169, 0.1315));
            check("probabilities: reading twice gives identical answers",
                    Arrays.equals(model.probabilities(0), model.probabilities(0)));
            check("probabilities: reading a prediction changed no logits",
                    Arrays.equals(model.logitRow(0), new double[] {1.2, 0.1, -0.4}));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testLoss() {
        try {
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            model.setRow(0, 1.2, 0.1, -0.4);
            check("loss: worked example — target pineapple costs 1.5284",
                    approx(model.loss(0, 1), 1.5284));

            model.setRow(0, 10.0, 0.0, 0.0);
            check("loss: near-certain and correct costs almost nothing (< 0.001)",
                    model.loss(0, 0) < 0.001);
            check("loss: near-zero probability on the truth costs enormously (> 9)",
                    model.loss(0, 1) > 9.0);

            model.setRow(0, 0.0, 0.0, 0.0);
            check("loss: a uniform row costs exactly ln(3) = 1.0986 — Chapter 2's anchor",
                    approx(model.loss(0, 2), Math.log(3)));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    // ----- Part 2 -----------------------------------------------------

    private static void testAccumulateGradients() {
        try {
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            model.setRow(0, 1.2, 0.1, -0.4);
            model.accumulateGradients(0, 1);

            double[] gradient = model.gradientRow(0);
            check("accumulateGradients: gradient is prediction minus one-hot — [0.6516, -0.7831, 0.1315]",
                    approxRow(gradient, 0.6516, -0.7831, 0.1315));
            check("accumulateGradients: gradient entries sum to zero",
                    Math.abs(gradient[0] + gradient[1] + gradient[2]) < 1e-9);
            check("accumulateGradients: only the current token's row received gradient",
                    allZero(model.gradientRow(1)) && allZero(model.gradientRow(2)));
            check("accumulateGradients: measuring changed no logits — accumulateGradients measures, step moves",
                    Arrays.equals(model.logitRow(0), new double[] {1.2, 0.1, -0.4}));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testGradientCheck() {
        try {
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            double[] base = {1.2, 0.1, -0.4};
            model.setRow(0, base);
            model.accumulateGradients(0, 1);
            double[] analytical = model.gradientRow(0);

            double h = 1e-4;
            double worstGap = 0.0;
            for (int nextToken = 0; nextToken < 3; nextToken++) {
                double[] up = base.clone();
                up[nextToken] += h;
                model.setRow(0, up);
                double lossUp = model.loss(0, 1);

                double[] down = base.clone();
                down[nextToken] -= h;
                model.setRow(0, down);
                double lossDown = model.loss(0, 1);

                model.setRow(0, base.clone());
                double numerical = (lossUp - lossDown) / (2 * h);
                worstGap = Math.max(worstGap, Math.abs(numerical - analytical[nextToken]));
            }
            System.out.printf(
                    "  INFO  gradient check — largest analytical-vs-wiggle gap: %.2e%n", worstGap);
            check("gradient check: the shortcut matches the wiggle experiment (gap < 1e-6)",
                    worstGap < 1e-6);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testStep() {
        try {
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            model.setRow(0, 1.2, 0.1, -0.4);
            double[] rowOneBefore = model.logitRow(1);
            double lossBefore = model.loss(0, 1);

            model.accumulateGradients(0, 1);
            model.step(0.5);

            check("step: worked row moved to [0.8742, 0.4916, -0.4658]",
                    approxRow(model.logitRow(0), 0.8742, 0.4916, -0.4658));
            check("step: one step lowered the loss — 1.5284 down to 1.0474",
                    approx(model.loss(0, 1), 1.0474) && model.loss(0, 1) < lossBefore);
            check("step: rows that accumulated no gradient did not move",
                    Arrays.equals(model.logitRow(1), rowOneBefore));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testAccumulation() {
        try {
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            model.setRow(0, 0.0, 0.0, 0.0);
            model.accumulateGradients(0, 1);
            model.accumulateGradients(0, 2);
            model.step(1.0);

            check("accumulate: two conflicting examples averaged — row is [-0.3333, 0.1667, 0.1667]",
                    approxRow(model.logitRow(0), -1.0 / 3, 1.0 / 6, 1.0 / 6));
            check("accumulate: both targets rose equally — probabilities [0.2327, 0.3837, 0.3837]",
                    approxRow(model.probabilities(0), 0.2327, 0.3837, 0.3837));

            model.zeroGradients();
            check("reset: zeroGradients cleared every accumulated slope",
                    allZero(model.gradientRow(0)) && allZero(model.gradientRow(1))
                            && allZero(model.gradientRow(2)));

            boolean refused = false;
            try {
                model.step(1.0);
            } catch (IllegalStateException expected) {
                refused = true;
            }
            check("reset: step with nothing accumulated is refused", refused);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testReproducibility() {
        try {
            TrainableBigramModel first = new TrainableBigramModel(3, 7);
            TrainableBigramModel second = new TrainableBigramModel(3, 7);
            TrainableBigramModel different = new TrainableBigramModel(3, 8);
            boolean same = true;
            for (int currentToken = 0; currentToken < 3; currentToken++) {
                same &= Arrays.equals(first.probabilities(currentToken),
                        second.probabilities(currentToken));
            }
            check("seed: the same seed reproduces the same starting table exactly", same);
            check("seed: a different seed produces a different table",
                    !Arrays.equals(first.probabilities(0), different.probabilities(0)));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testAverageLoss() {
        try {
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            double byHand = (model.loss(1, 0) + model.loss(0, 1)) / 2.0;
            check("averageLoss: a three-token history averages its two transitions",
                    Math.abs(model.averageLoss(new int[] {1, 0, 1}) - byHand) < 1e-9);

            double[][] logitsBefore = new double[3][];
            double[][] gradientsBefore = new double[3][];
            for (int row = 0; row < 3; row++) {
                logitsBefore[row] = model.logitRow(row);
                gradientsBefore[row] = model.gradientRow(row);
            }
            double nearlyEmptyLoss = model.averageLoss(TrainingData.trainingTokens());
            boolean untouched = true;
            for (int row = 0; row < 3; row++) {
                untouched &= Arrays.equals(model.logitRow(row), logitsBefore[row])
                        && Arrays.equals(model.gradientRow(row), gradientsBefore[row]);
            }
            check("averageLoss: grading moved no logits and touched no gradients — report cards only read",
                    untouched);
            System.out.printf(
                    "  INFO  nearly empty table, average training loss: %.4f   (ln 3 = %.4f)%n",
                    nearlyEmptyLoss, Math.log(3));
            check("averageLoss: a nearly empty table scores at Chapter 2's uniform anchor",
                    Math.abs(nearlyEmptyLoss - Math.log(3)) < 0.02);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testStochasticGradientDescentStep() {
        try {
            int[] trainingHistory = TrainingData.trainingTokens();
            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            double before = model.averageLoss(trainingHistory);

            Random random = new Random(42);
            Trainer.stochasticGradientDescentStep(model, trainingHistory, 24, 0.5, random);

            double after = model.averageLoss(trainingHistory);
            check("SGD step: one seeded step lowered the average training loss", after < before);
            check("SGD step: the worked run's first step lands on 1.0279", approx(after, 1.0279));
            check("SGD step: exactly one draw per flashcard — the 25th draw of seed 42 is 100",
                    random.nextInt(trainingHistory.length - 1) == 100);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void runTraining() {
        try {
            int[] trainingHistory = TrainingData.trainingTokens();
            int[] validationHistory = TrainingData.validationTokens();

            TrainableBigramModel model = new TrainableBigramModel(3, 7);
            double initial = model.averageLoss(trainingHistory);
            System.out.println("\n--- The worked loss trace: 300 steps, batch 24, learning rate 0.5 ---");
            Trainer.train(model, trainingHistory, validationHistory, 300, 24, 0.5, 30, 42);

            double finalTrain = model.averageLoss(trainingHistory);
            double finalValidation = model.averageLoss(validationHistory);
            check("training: loss fell — final training loss below the starting loss",
                    finalTrain < initial);
            check("training: final training loss reproduces 0.3300",
                    Math.abs(finalTrain - 0.3300) < 0.01);
            check("training: final validation loss reproduces 0.3311",
                    Math.abs(finalValidation - 0.3311) < 0.01);

            double[] pizzaRow = model.probabilities(0);
            check("training: learned P(pineapple | pizza) matches the counted 40/60 within 0.05",
                    Math.abs(pizzaRow[1] - 40.0 / 60.0) < 0.05);
            check("training: learned P(pizza | pizza) is tiny — the history never shows it",
                    pizzaRow[0] < 0.05);
            check("training: ...but never exactly zero — softmax cannot say never",
                    pizzaRow[0] > 0.0);

            double pineappleConfidence = model.probabilities(1)[0];
            double pepperoniConfidence = model.probabilities(2)[0];
            System.out.printf(
                    "  INFO  P(pizza | pineapple) = %.4f from 41 examples;"
                            + " P(pizza | pepperoni) = %.4f from 20 examples%n",
                    pineappleConfidence, pepperoniConfidence);
            check("training: the row with twice the examples is more confident — rows learn alone",
                    pineappleConfidence > pepperoniConfidence);

            TrainableBigramModel rerun = new TrainableBigramModel(3, 7);
            Trainer.train(rerun, trainingHistory, validationHistory, 300, 24, 0.5, 0, 42);
            check("training: the same seeds reproduce the same final loss exactly",
                    rerun.averageLoss(trainingHistory) == finalTrain);

            Trainer.printComparison(model, trainingHistory);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    // ----- helpers -----------------------------------------------------

    private static boolean approx(double actual, double expected) {
        return Math.abs(actual - expected) < 1e-3;
    }

    private static boolean approxRow(double[] actual, double... expected) {
        if (actual.length != expected.length) {
            return false;
        }
        for (int entry = 0; entry < expected.length; entry++) {
            if (!approx(actual[entry], expected[entry])) {
                return false;
            }
        }
        return true;
    }

    private static boolean allZero(double[] row) {
        for (double entry : row) {
            if (entry != 0.0) {
                return false;
            }
        }
        return true;
    }

    private static void check(String name, boolean ok) {
        System.out.println((ok ? "  PASS  " : "  FAIL  ") + name);
    }

    private static void todo(UnsupportedOperationException e) {
        System.out.println("  TODO  " + e.getMessage());
    }
}
