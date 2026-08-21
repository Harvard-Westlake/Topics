import java.util.HashSet;
import java.util.List;
import java.util.Set;

// PROVIDED — reproduces every worked trace from the lesson page and runs the
// required tests. Complete the TODOs in order and rerun after each one:
// stages you have not implemented yet are reported as TODO, not FAIL.
public class Ch6_ScalarAutograd_Tester {

    public static void main(String[] args) {
        System.out.println("=== Part 1 (Day 1): the receipts and the audit ===");
        testAddProvided();
        testMultiply();
        testSubtract();
        testRectify();
        testExponential();
        testNaturalLog();
        testLeafGuard();
        testTopologicalOrder();
        testBackwardFirstTrace();
        testBackwardReusedLeaf();
        testPracticeGraph();
        testDiamond();
        testWiggleRefereeComposite();

        System.out.println("\n=== Part 2 (Day 2): the network, audited and trained ===");
        testWeighAndAddValues();
        testScoresParity();
        testGradingWritesNothing();
        testLossParity();
        testShortcutRediscovered();
        testCardBlame();
        testWiggleRefereeNetwork();
        testAverageLoss();
        testZeroGradients();
        testGradientDescentStep();
        testTrainingRun();
        testOracle();
        testDrumbeat();
        testValidators();
        printPunchlines();
    }

    // ----- Part 1 -----------------------------------------------------

    private static void testAddProvided() {
        Value first = new Value(2.0, "a");
        Value second = new Value(3.0, "b");
        Value sum = first.add(second);
        check("add (provided): 2 + 3 makes a receipt holding 5",
                approx(sum.number(), 5.0));
        check("add (provided): the new receipt has two ingredients and is not a leaf",
                sum.parentValues().size() == 2 && !sum.isLeaf());
        check("add (provided): creating a receipt writes nothing — ingredients untouched",
                first.number() == 2.0 && first.gradient() == 0.0);
    }

    private static void testMultiply() {
        try {
            Value first = new Value(2.0, "a");
            Value second = new Value(3.0, "b");
            Value product = first.multiply(second);
            check("multiply: 2 * 3 makes a receipt holding 6",
                    approx(product.number(), 6.0));
            check("multiply: ingredients untouched, no blame yet",
                    first.number() == 2.0 && first.gradient() == 0.0
                            && second.gradient() == 0.0);
            check("multiply: asking twice mints two different receipts",
                    first.multiply(second) != product);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testSubtract() {
        try {
            Value first = new Value(2.0, "a");
            Value second = new Value(3.0, "b");
            check("subtract: 2 - 3 makes a receipt holding -1",
                    approx(first.subtract(second).number(), -1.0));
            check("subtract: 3 - 2 makes a receipt holding 1 — order matters",
                    approx(second.subtract(first).number(), 1.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testRectify() {
        try {
            check("rectify: -2 gates to exactly 0.0",
                    new Value(-2.0).rectify().number() == 0.0);
            check("rectify: 4 passes through unchanged",
                    approx(new Value(4.0).rectify().number(), 4.0));
            check("rectify: exactly 0 stays 0 — the gate is closed at zero",
                    new Value(0.0).rectify().number() == 0.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testExponential() {
        try {
            check("exponential: e^0 = 1",
                    approx(new Value(0.0).exponential().number(), 1.0));
            check("exponential: e^1 = 2.71828...",
                    approx(new Value(1.0).exponential().number(), Math.exp(1.0)));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testNaturalLog() {
        try {
            check("naturalLog: ln(2) = 0.6931",
                    approx(new Value(2.0).naturalLog().number(), 0.6931));
            boolean zeroRefused = false;
            try {
                new Value(0.0).naturalLog();
            } catch (IllegalArgumentException expected) {
                zeroRefused = true;
            }
            boolean negativeRefused = false;
            try {
                new Value(-1.0).naturalLog();
            } catch (IllegalArgumentException expected) {
                negativeRefused = true;
            }
            check("naturalLog: zero and negative ingredients are refused loudly",
                    zeroRefused && negativeRefused);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testLeafGuard() {
        Value leaf = new Value(1.0, "leaf");
        leaf.setNumber(2.0);
        check("setNumber: a leaf may be moved — the Nudge's door",
                leaf.number() == 2.0);
        Value computed = leaf.add(new Value(1.0));
        boolean refused = false;
        try {
            computed.setNumber(99.0);
        } catch (IllegalStateException expected) {
            refused = true;
        }
        check("setNumber: a computed receipt refuses to be rewritten",
                refused);
    }

    private static void testTopologicalOrder() {
        try {
            Value first = new Value(2.0, "a");
            Value second = new Value(3.0, "b");
            Value product = first.multiply(second);
            Value loss = product.add(first);
            List<Value> order = loss.topologicalOrder();
            check("topologicalOrder: the first trace has exactly 4 receipts, no repeats",
                    order.size() == 4 && new HashSet<>(order).size() == 4);
            check("topologicalOrder: the audited receipt itself comes last",
                    order.get(order.size() - 1) == loss);
            check("topologicalOrder: every receipt appears after all of its ingredients",
                    parentsFirst(order));

            Value diamondLoss = first.add(second).multiply(first.multiply(second));
            List<Value> diamondOrder = diamondLoss.topologicalOrder();
            check("topologicalOrder: the diamond graph lists 5 receipts, ingredients first",
                    diamondOrder.size() == 5 && parentsFirst(diamondOrder));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static boolean parentsFirst(List<Value> order) {
        for (int position = 0; position < order.size(); position++) {
            for (Value parent : order.get(position).parentValues()) {
                int parentPosition = -1;
                for (int earlier = 0; earlier < order.size(); earlier++) {
                    if (order.get(earlier) == parent) {
                        parentPosition = earlier;
                        break;
                    }
                }
                if (parentPosition < 0 || parentPosition >= position) {
                    return false;
                }
            }
        }
        return true;
    }

    private static void testBackwardFirstTrace() {
        try {
            Value first = new Value(2.0, "a");
            Value second = new Value(3.0, "b");
            Value product = first.multiply(second);
            Value loss = product.add(first);
            loss.backward();
            check("backward: first trace — dL/da = 4 (3 through the product, plus 1 direct)",
                    approx(first.gradient(), 4.0));
            check("backward: first trace — dL/db = 2 and the product's receipt reads 1",
                    approx(second.gradient(), 2.0) && approx(product.gradient(), 1.0));
            check("backward: the loss's own gradient is seeded to exactly 1",
                    loss.gradient() == 1.0);
            check("backward: the audit moved no forward number",
                    loss.number() == 8.0 && product.number() == 6.0 && first.number() == 2.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testBackwardReusedLeaf() {
        try {
            Value reused = new Value(3.0, "a");
            Value square = reused.multiply(reused);
            square.backward();
            check("backward: a * a delivers blame through both doors — dL/da = 6",
                    approx(reused.gradient(), 6.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testPracticeGraph() {
        try {
            Value weight = new Value(2.0, "w");
            Value input = new Value(3.0, "x");
            Value bias = new Value(-5.0, "b");
            Value gated = weight.multiply(input).add(bias).rectify();
            Value loss = gated.multiply(gated);
            loss.backward();
            check("practice graph: forward lands on L = 1",
                    approx(loss.number(), 1.0));
            check("practice graph: dL/dw = 6, dL/dx = 4, dL/db = 2",
                    approx(weight.gradient(), 6.0) && approx(input.gradient(), 4.0)
                            && approx(bias.gradient(), 2.0));

            Value silencedWeight = new Value(2.0, "w");
            Value silencedInput = new Value(3.0, "x");
            Value silencedBias = new Value(-7.0, "b");
            Value silencedGated = silencedWeight.multiply(silencedInput)
                    .add(silencedBias).rectify();
            Value silencedLoss = silencedGated.multiply(silencedGated);
            silencedLoss.backward();
            check("practice graph, silenced: the closed gate returns every parcel — all leaf blame exactly 0",
                    silencedWeight.gradient() == 0.0 && silencedInput.gradient() == 0.0
                            && silencedBias.gradient() == 0.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testDiamond() {
        try {
            Value first = new Value(2.0, "a");
            Value second = new Value(3.0, "b");
            Value loss = first.add(second).multiply(first.multiply(second));
            loss.backward();
            check("diamond: two paths add — dL/da = 21, dL/db = 16",
                    approx(first.gradient(), 21.0) && approx(second.gradient(), 16.0));
            loss.backward();
            check("diamond: a second audit of the SAME graph corrupts — dL/da reads 63, not 21",
                    approx(first.gradient(), 63.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testWiggleRefereeComposite() {
        try {
            double[] leaves = {0.5, -1.2, 2.0};
            Value first = new Value(leaves[0], "a");
            Value second = new Value(leaves[1], "b");
            Value third = new Value(leaves[2], "c");
            Value loss = compositeGraph(first, second, third);
            check("referee graph: L = ln(e^(a*b) + rectify(c - a)) = 0.7173",
                    approx(loss.number(), 0.7173));
            loss.backward();
            double[] audited = {first.gradient(), second.gradient(), third.gradient()};
            check("referee graph: backward says a -0.8095, b 0.1339, c 0.4881",
                    approx(audited[0], -0.809530) && approx(audited[1], 0.133934)
                            && approx(audited[2], 0.488088));

            double epsilon = 1e-5;
            boolean allAgree = true;
            for (int leaf = 0; leaf < 3; leaf++) {
                double[] up = leaves.clone();
                double[] down = leaves.clone();
                up[leaf] += epsilon;
                down[leaf] -= epsilon;
                double wiggle = (compositeNumber(up) - compositeNumber(down)) / (2 * epsilon);
                allAgree &= Math.abs(wiggle - audited[leaf]) < 1e-6;
            }
            check("referee graph: the wiggle experiment agrees with every audit to 1e-6",
                    allAgree);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static Value compositeGraph(Value first, Value second, Value third) {
        return first.multiply(second).exponential()
                .add(third.subtract(first).rectify()).naturalLog();
    }

    private static double compositeNumber(double[] leaves) {
        return compositeGraph(new Value(leaves[0]), new Value(leaves[1]),
                new Value(leaves[2])).number();
    }

    // ----- Part 2 -----------------------------------------------------

    private static void testWeighAndAddValues() {
        try {
            Value[] inputRow = {new Value(1.0), new Value(2.0)};
            Value[][] layerWeights = {
                {new Value(1.0), new Value(-2.0)},
                {new Value(3.0), new Value(1.0)},
            };
            Value[] layerBiases = {new Value(1.0), new Value(-1.0)};
            Value[] weightedSums = TrainableFeatureNetwork.weighAndAddValues(
                    inputRow, layerWeights, layerBiases);
            check("weighAndAddValues: the practice hidden layer is [-2, 4] — Chapter 5's numbers",
                    approx(weightedSums[0].number(), -2.0)
                            && approx(weightedSums[1].number(), 4.0));
            check("weighAndAddValues: building the layer moved no ingredient",
                    inputRow[0].number() == 1.0 && layerBiases[0].number() == 1.0);

            boolean mismatchRefused = false;
            try {
                TrainableFeatureNetwork.weighAndAddValues(
                        new Value[] {new Value(1.0)}, layerWeights, layerBiases);
            } catch (IllegalArgumentException expected) {
                mismatchRefused = true;
            }
            check("weighAndAddValues: a row that does not match the weights is refused",
                    mismatchRefused);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testScoresParity() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            Value[] scores = network.unrestrictedScoreValues(new int[] {1, 0, 1});
            check("scores: context [1, 0, 1] scores [1.5504, -1.6160, -1.1503] — Chapter 5, reborn",
                    approx(scores[0].number(), 1.5504) && approx(scores[1].number(), -1.6160)
                            && approx(scores[2].number(), -1.1503));
            Value[] pizzaScores = network.unrestrictedScoreValues(new int[] {0, 1, 0});
            check("scores: context [0, 1, 0] scores [-1.3026, 1.5619, 0.8662]",
                    approx(pizzaScores[0].number(), -1.3026)
                            && approx(pizzaScores[1].number(), 1.5619)
                            && approx(pizzaScores[2].number(), 0.8662));
            double[] forecast = network.forecast(new int[] {1, 0, 1});
            check("forecast: [0.9015, 0.0380, 0.0605], summing to one",
                    approx(forecast[0], 0.9015) && approx(forecast[1], 0.0380)
                            && approx(forecast[2], 0.0605)
                            && approx(forecast[0] + forecast[1] + forecast[2], 1.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testGradingWritesNothing() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            double[][] cardsBefore = network.statCardNumbers();
            for (int repetition = 0; repetition < 100; repetition++) {
                network.forecast(new int[] {1, 0, 1});
                network.lossValue(new int[] {0, 1, 0}, 2);
            }
            double[][] cardsAfter = network.statCardNumbers();
            boolean unchanged = true;
            for (int token = 0; token < cardsBefore.length; token++) {
                for (int slot = 0; slot < cardsBefore[token].length; slot++) {
                    unchanged &= cardsBefore[token][slot] == cardsAfter[token][slot];
                }
            }
            check("grading writes nothing: a hundred forecasts and grades moved no parameter",
                    unchanged);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testLossParity() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            check("loss: the real flashcard [1, 0, 1] -> pizza charges 0.1037",
                    approx(network.lossValue(new int[] {1, 0, 1}, 0).number(), 0.1037));
            check("loss: the honest mixture [0, 1, 0] -> pepperoni charges 1.1377",
                    approx(network.lossValue(new int[] {0, 1, 0}, 2).number(), 1.1377));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testShortcutRediscovered() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            double[] forecast = network.forecast(new int[] {1, 0, 1});
            Value[] scores = network.unrestrictedScoreValues(new int[] {1, 0, 1});
            network.lossValueFromScores(scores, 0).backward();
            check("the shortcut, rediscovered: score gradients are exactly forecast minus one-hot",
                    Math.abs(scores[0].gradient() - (forecast[0] - 1.0)) < 1e-9
                            && Math.abs(scores[1].gradient() - forecast[1]) < 1e-9
                            && Math.abs(scores[2].gradient() - forecast[2]) < 1e-9);
            check("the shortcut, in numbers: [-0.0985, 0.0380, 0.0605]",
                    approx(scores[0].gradient(), -0.0985)
                            && approx(scores[1].gradient(), 0.0380)
                            && approx(scores[2].gradient(), 0.0605));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testCardBlame() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            network.lossValue(new int[] {1, 0, 1}, 0).backward();
            check("card blame: pineapple's slots read [-0.0597, -0.0444] — two positions, added",
                    approx(network.statCardValue(1, 0).gradient(), -0.0597)
                            && approx(network.statCardValue(1, 1).gradient(), -0.0444));
            check("card blame: pizza's slots read [0.0594, -0.1120]",
                    approx(network.statCardValue(0, 0).gradient(), 0.0594)
                            && approx(network.statCardValue(0, 1).gradient(), -0.1120));
            check("card blame: pepperoni was not in the context — its blame is exactly 0.0",
                    network.statCardValue(2, 0).gradient() == 0.0
                            && network.statCardValue(2, 1).gradient() == 0.0);
            check("deeper blame: hiddenWeight[3][0] reads -0.0361, and each output bias reads its score's gradient",
                    approx(network.hiddenWeightValue(3, 0).gradient(), -0.0361)
                            && approx(network.outputBiasValue(0).gradient(), -0.0985)
                            && approx(network.outputBiasValue(1).gradient(), 0.0380)
                            && approx(network.outputBiasValue(2).gradient(), 0.0605));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testWiggleRefereeNetwork() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            network.lossValue(new int[] {1, 0, 1}, 0).backward();
            Value[] refereed = {
                network.statCardValue(1, 0),
                network.hiddenWeightValue(3, 0),
                network.outputBiasValue(2),
            };
            double epsilon = 1e-5;
            boolean allAgree = true;
            double worstGap = 0.0;
            for (Value parameter : refereed) {
                double audited = parameter.gradient();
                double original = parameter.number();
                parameter.setNumber(original + epsilon);
                double lossUp = network.lossValue(new int[] {1, 0, 1}, 0).number();
                parameter.setNumber(original - epsilon);
                double lossDown = network.lossValue(new int[] {1, 0, 1}, 0).number();
                parameter.setNumber(original);
                double wiggle = (lossUp - lossDown) / (2 * epsilon);
                worstGap = Math.max(worstGap, Math.abs(wiggle - audited));
                allAgree &= Math.abs(wiggle - audited) < 1e-5;
            }
            System.out.printf(
                    "  INFO  referee on the network — worst audit-versus-wiggle gap %.2e%n",
                    worstGap);
            check("referee on the network: three parameters, audit and wiggle agree",
                    allAgree);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testAverageLoss() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            check("averageLoss: a four-token history holds exactly ONE flashcard",
                    Math.abs(network.averageLossNumber(new int[] {1, 0, 1, 0})
                            - network.lossValue(new int[] {1, 0, 1}, 0).number()) < 1e-9);
            double trainingLoss = network.averageLossNumber(AutogradFixtures.trainingTokens());
            double validationLoss = network.averageLossNumber(AutogradFixtures.validationTokens());
            System.out.printf(
                    "  INFO  frozen start — training loss %.4f over 119 flashcards,"
                            + " validation loss %.4f over 39%n",
                    trainingLoss, validationLoss);
            check("averageLoss: the frozen start scores 0.3957 / 0.4013 — Chapter 5's report card",
                    approx(trainingLoss, 0.3957) && approx(validationLoss, 0.4013));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testZeroGradients() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            network.lossValue(new int[] {1, 0, 1}, 0).backward();
            check("Reset: one audit leaves pineapple slot 0 at -0.0597",
                    approx(network.statCardValue(1, 0).gradient(), -0.0597));
            network.lossValue(new int[] {1, 0, 1}, 0).backward();
            check("Reset: a second fresh graph WITHOUT Reset accumulates — -0.1193",
                    approx(network.statCardValue(1, 0).gradient(), -0.1193));
            network.zeroGradients();
            check("Reset: zeroGradients wipes every parameter's blame to exactly 0.0",
                    network.statCardValue(1, 0).gradient() == 0.0
                            && network.outputBiasValue(0).gradient() == 0.0);
            network.lossValue(new int[] {1, 0, 1}, 0).backward();
            check("Reset: after the wipe, a fresh audit reads -0.0597 again",
                    approx(network.statCardValue(1, 0).gradient(), -0.0597));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testGradientDescentStep() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            double reported = Trainer.gradientDescentStep(network,
                    AutogradFixtures.trainingTokens(), 0.5);
            check("gradientDescentStep: reports the loss it stood on — 0.3957",
                    approx(reported, 0.3957));
            check("gradientDescentStep: one step lands at 0.3754 training / 0.3806 validation",
                    approx(network.averageLossNumber(AutogradFixtures.trainingTokens()), 0.3754)
                            && approx(network.averageLossNumber(
                                    AutogradFixtures.validationTokens()), 0.3806));
            check("gradientDescentStep: the Nudge actually moved the binder",
                    network.statCardNumbers()[1][0] != 0.38);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testTrainingRun() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            Trainer.train(network, AutogradFixtures.trainingTokens(),
                    AutogradFixtures.validationTokens(), 30, 0.5, 0);
            double trainingLoss = network.averageLossNumber(AutogradFixtures.trainingTokens());
            double validationLoss = network.averageLossNumber(AutogradFixtures.validationTokens());
            System.out.printf(
                    "  INFO  30 steps from the frozen start — %.4f training / %.4f validation"
                            + "   (Chapter 4's table: 0.3300 / 0.3311)%n",
                    trainingLoss, validationLoss);
            check("training: 30 steps land at 0.3210 / 0.3252",
                    approx(trainingLoss, 0.3210) && approx(validationLoss, 0.3252));
            check("training: the gap is closed — past Chapter 4's table on both histories",
                    trainingLoss < 0.3300 && validationLoss < 0.3311);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testOracle() {
        try {
            TrainableFeatureNetwork fresh = AutogradFixtures.freshStart();
            double initLoss = fresh.averageLossNumber(AutogradFixtures.trainingTokens());
            System.out.printf(
                    "  INFO  fresh offline start — loss %.4f before training"
                            + "   (the empty network's anchor: ln 3 = 1.0986)%n", initLoss);
            check("oracle: the fresh start grades 1.3626 — an opinionated random machine loses to an ignorant one",
                    approx(initLoss, 1.3626));
            Trainer.train(fresh, AutogradFixtures.trainingTokens(),
                    AutogradFixtures.validationTokens(), 10, 0.5, 0);
            double trainedLoss = fresh.averageLossNumber(AutogradFixtures.trainingTokens());
            double gap = Trainer.maxGapToFrozen(fresh);
            System.out.printf(
                    "  INFO  10 steps at learning rate 0.5 — loss %.4f, largest gap to any"
                            + " frozen number %.6f%n", trainedLoss, gap);
            check("oracle: ten steps land at 0.3958, within rounding (0.005) of every frozen number",
                    approx(trainedLoss, 0.3958) && gap < 0.00505);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testDrumbeat() {
        try {
            TrainableFeatureNetwork drummer = AutogradFixtures.frozenStart();
            int[] drumbeat = AutogradFixtures.drumbeatTokens();
            Trainer.train(drummer, drumbeat, drumbeat, 50, 0.5, 0);
            double drumbeatLoss = drummer.averageLossNumber(drumbeat);
            double pizzeriaLoss = drummer.averageLossNumber(AutogradFixtures.trainingTokens());
            System.out.printf(
                    "  INFO  drumbeat after 50 steps — %.4f on the drumbeat,"
                            + " %.4f on the pizzeria it forgot%n",
                    drumbeatLoss, pizzeriaLoss);
            check("drumbeat: fifty steps memorize the pattern — loss below 0.005",
                    drumbeatLoss < 0.005);
            check("drumbeat: forecast after [0, 1, 2] gives token 0 above 99%",
                    drummer.forecast(new int[] {0, 1, 2})[0] > 0.99);
            check("drumbeat: the pizzeria is forgotten — its loss now above 2",
                    pizzeriaLoss > 2.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testValidators() {
        try {
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            boolean shortContextRefused = false;
            try {
                network.unrestrictedScoreValues(new int[] {1, 0});
            } catch (IllegalArgumentException expected) {
                shortContextRefused = true;
            }
            check("shapes: a two-token context is refused — this model reads exactly three",
                    shortContextRefused);

            boolean badTokenRefused = false;
            try {
                network.unrestrictedScoreValues(new int[] {1, 0, 3});
            } catch (IllegalArgumentException expected) {
                badTokenRefused = true;
            }
            check("shapes: token 3 is refused — the binder has cards 0 through 2",
                    badTokenRefused);

            boolean tinyHistoryRefused = false;
            try {
                network.averageLossValue(new int[] {1, 0, 1});
            } catch (IllegalArgumentException expected) {
                tinyHistoryRefused = true;
            }
            check("shapes: a three-token history is refused — it holds no flashcard",
                    tinyHistoryRefused);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void printPunchlines() {
        try {
            System.out.println("\n--- The punchlines ---");
            TrainableFeatureNetwork network = AutogradFixtures.frozenStart();
            double[] forecast = network.forecast(new int[] {1, 0, 1});
            Value[] scores = network.unrestrictedScoreValues(new int[] {1, 0, 1});
            network.lossValueFromScores(scores, 0).backward();
            System.out.printf("  the forecast:        [%.4f, %.4f, %.4f]   truth: pizza%n",
                    forecast[0], forecast[1], forecast[2]);
            System.out.printf("  score gradients:     [%.4f, %.4f, %.4f]   = forecast minus one-hot:"
                            + " Chapter 4's shortcut, rediscovered by the audit%n",
                    scores[0].gradient(), scores[1].gradient(), scores[2].gradient());
            System.out.printf("  binder blame:        pineapple [%.4f, %.4f] (used twice, envelopes added)"
                            + "   pepperoni [%.1f, %.1f] (not consulted, no blame)%n",
                    network.statCardValue(1, 0).gradient(),
                    network.statCardValue(1, 1).gradient(),
                    network.statCardValue(2, 0).gradient(),
                    network.statCardValue(2, 1).gradient());

            TrainableFeatureNetwork runner = AutogradFixtures.frozenStart();
            Trainer.train(runner, AutogradFixtures.trainingTokens(),
                    AutogradFixtures.validationTokens(), 30, 0.5, 0);
            System.out.println("  the leaderboard:     uniform anchor 1.0986 | frozen start 0.3957 / 0.4013");
            System.out.printf("                       30 steps later %.4f / %.4f | Chapter 4's table"
                            + " 0.3300 / 0.3311 | the data's floor ~0.3174%n",
                    runner.averageLossNumber(AutogradFixtures.trainingTokens()),
                    runner.averageLossNumber(AutogradFixtures.validationTokens()));
            System.out.println("  The gap Chapter 5 could only stare at closed in thirty steps of the");
            System.out.println("  loop you built. Run `java Trainer` for the 120-step trace, the oracle");
            System.out.println("  reproduction, and the drumbeat.");
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    // ----- helpers -----------------------------------------------------

    private static boolean approx(double actual, double expected) {
        return Math.abs(actual - expected) < 1e-3;
    }

    private static void check(String name, boolean ok) {
        System.out.println((ok ? "  PASS  " : "  FAIL  ") + name);
    }

    private static void todo(UnsupportedOperationException e) {
        System.out.println("  TODO  " + e.getMessage());
    }
}
