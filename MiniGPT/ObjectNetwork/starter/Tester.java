import java.util.Arrays;

// PROVIDED — reproduces every worked trace from the lesson page and runs the
// required tests. Complete the TODOs in order and rerun after each one:
// stages you have not implemented yet are reported as TODO, not FAIL.
public class Tester {

    public static void main(String[] args) {
        System.out.println("=== Part 1 (Day 1): neurons, layers, the gate ===");
        testNeuronWeighAndAdd();
        testNeuronRecompute();
        testPracticeNetworkObjects();
        testWeighAndAddLayer();
        testRectify();
        testCollapseWithoutGate();
        testObjectVersusArray();

        System.out.println("\n=== Part 2 (Day 2): the forecast pipeline ===");
        testLookUpStatCards();
        testJoinCards();
        testUnrestrictedScores();
        testForecast();
        testLoss();
        testAverageLoss();
        testCousins();
        testAfterPizza();
        testNothingChanges();
        testParameterCount();
        testShapeValidation();
        printPunchlines();
    }

    // ----- Part 1 -----------------------------------------------------

    private static void testNeuronWeighAndAdd() {
        try {
            Neuron inputLeft = Neuron.input("inputLeft");
            Neuron inputRight = Neuron.input("inputRight");
            inputLeft.setValue(1.0);
            inputRight.setValue(2.0);

            Neuron hiddenTop = Neuron.rectified("hiddenTop", 1.0);
            hiddenTop.connectFrom(inputLeft, 1.0);
            hiddenTop.connectFrom(inputRight, -2.0);
            check("weighAndAddInputs: top practice unit totals 1 + 1*1 + (-2)*2 = -2",
                    approx(hiddenTop.weighAndAddInputs(), -2.0));
            check("weighAndAddInputs: reading is not writing — storedValue is untouched",
                    hiddenTop.value() == 0.0);
            check("weighAndAddInputs: asking twice gives the same answer",
                    hiddenTop.weighAndAddInputs() == hiddenTop.weighAndAddInputs());

            Neuron hiddenBottom = Neuron.rectified("hiddenBottom", -1.0);
            hiddenBottom.connectFrom(inputLeft, 3.0);
            hiddenBottom.connectFrom(inputRight, 1.0);
            check("weighAndAddInputs: bottom practice unit totals -1 + 3*1 + 1*2 = 4",
                    approx(hiddenBottom.weighAndAddInputs(), 4.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testNeuronRecompute() {
        try {
            Neuron inputLeft = Neuron.input("inputLeft");
            Neuron inputRight = Neuron.input("inputRight");
            inputLeft.setValue(1.0);
            inputRight.setValue(2.0);

            Neuron hiddenTop = Neuron.rectified("hiddenTop", 1.0);
            hiddenTop.connectFrom(inputLeft, 1.0);
            hiddenTop.connectFrom(inputRight, -2.0);
            hiddenTop.setValue(99.0);
            double gated = hiddenTop.recomputeValue();
            check("recomputeValue: the gate silences the negative total — -2 becomes 0",
                    gated == 0.0);
            check("recomputeValue: storedValue was OVERWRITTEN — 99 is gone",
                    hiddenTop.value() == 0.0);

            Neuron hiddenBottom = Neuron.rectified("hiddenBottom", -1.0);
            hiddenBottom.connectFrom(inputLeft, 3.0);
            hiddenBottom.connectFrom(inputRight, 1.0);
            check("recomputeValue: a positive total passes the gate — 4 stays 4",
                    approx(hiddenBottom.recomputeValue(), 4.0));

            check("recomputeValue: rectified unit at exactly zero shows zero",
                    Neuron.rectified("zeroUnit", 0.0).recomputeValue() == 0.0);
            check("recomputeValue: a linear unit keeps its negative total",
                    approx(Neuron.linear("linearUnit", -5.0).recomputeValue(), -5.0));
            check("recomputeValue: a rectified unit silences the same total",
                    Neuron.rectified("gatedUnit", -5.0).recomputeValue() == 0.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testPracticeNetworkObjects() {
        try {
            Neuron inputLeft = Neuron.input("inputLeft");
            Neuron inputRight = Neuron.input("inputRight");
            inputLeft.setValue(1.0);
            inputRight.setValue(2.0);

            Neuron hiddenTop = Neuron.rectified("hiddenTop", 1.0);
            hiddenTop.connectFrom(inputLeft, 1.0);
            hiddenTop.connectFrom(inputRight, -2.0);
            Neuron hiddenBottom = Neuron.rectified("hiddenBottom", -1.0);
            hiddenBottom.connectFrom(inputLeft, 3.0);
            hiddenBottom.connectFrom(inputRight, 1.0);

            Neuron outputFirst = Neuron.linear("outputFirst", 0.0);
            outputFirst.connectFrom(hiddenTop, 2.0);
            outputFirst.connectFrom(hiddenBottom, -1.0);
            Neuron outputSecond = Neuron.linear("outputSecond", 2.0);
            outputSecond.connectFrom(hiddenTop, 1.0);
            outputSecond.connectFrom(hiddenBottom, 1.0);

            // Layer order: hidden before output — a neuron reads only
            // neurons that are already up to date.
            hiddenTop.recomputeValue();
            hiddenBottom.recomputeValue();
            check("practice network: object trace lands on outputs [-4, 6]",
                    approx(outputFirst.recomputeValue(), -4.0)
                            && approx(outputSecond.recomputeValue(), 6.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testWeighAndAddLayer() {
        try {
            double[] practiceInputs = NetworkFixtures.practiceInputs();
            double[] hiddenSums = FeatureNetwork.weighAndAdd(practiceInputs,
                    NetworkFixtures.practiceHiddenWeights(),
                    NetworkFixtures.practiceHiddenBiases());
            check("weighAndAdd: practice hidden layer is [-2, 4]",
                    approxRow(hiddenSums, -2.0, 4.0));
            check("weighAndAdd: the input row came back unchanged",
                    Arrays.equals(practiceInputs, new double[] {1.0, 2.0}));

            double[] outputs = FeatureNetwork.weighAndAdd(new double[] {0.0, 4.0},
                    NetworkFixtures.practiceOutputWeights(),
                    NetworkFixtures.practiceOutputBiases());
            check("weighAndAdd: practice output layer from [0, 4] is [-4, 6]",
                    approxRow(outputs, -4.0, 6.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testRectify() {
        try {
            double[] weightedSums = {-2.0, 0.0, 4.0};
            double[] gated = FeatureNetwork.rectify(weightedSums);
            check("rectify: [-2, 0, 4] gates to [0, 0, 4]",
                    approxRow(gated, 0.0, 0.0, 4.0));
            check("rectify: a NEW array is created — the input is not reused",
                    gated != weightedSums);
            check("rectify: the input array came back unchanged",
                    Arrays.equals(weightedSums, new double[] {-2.0, 0.0, 4.0}));
            check("rectify: silenced entries are exactly 0.0, not merely small",
                    gated[0] == 0.0 && gated[1] == 0.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testCollapseWithoutGate() {
        try {
            // Skip the gate and the two practice layers collapse into one:
            // problem B2's algebra says the gateless machine IS the single
            // weighted sums  3 - 1*x0 - 5*x1  and  2 + 4*x0 - 1*x1.
            double[] inputs = NetworkFixtures.practiceInputs();
            double[] hiddenSums = FeatureNetwork.weighAndAdd(inputs,
                    NetworkFixtures.practiceHiddenWeights(),
                    NetworkFixtures.practiceHiddenBiases());
            double[] gatelessOutputs = FeatureNetwork.weighAndAdd(hiddenSums,
                    NetworkFixtures.practiceOutputWeights(),
                    NetworkFixtures.practiceOutputBiases());

            double[] collapsed = FeatureNetwork.weighAndAdd(inputs,
                    new double[][] {{-1.0, -5.0}, {4.0, -1.0}},
                    new double[] {3.0, 2.0});
            check("collapse: without the gate, two layers equal one weighted sum — [-8, 4] twice",
                    approxRow(gatelessOutputs, -8.0, 4.0)
                            && approxRow(collapsed, -8.0, 4.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testObjectVersusArray() {
        try {
            // Hidden unit 3 of the PROVIDED model, built both ways from the
            // joined row for context pineapple pizza pineapple.
            double[] joinedRow = {0.38, -0.01, -1.12, 0.47, 0.38, -0.01};
            double[][] hiddenWeights = NetworkFixtures.hiddenWeights();
            double[] hiddenBiases = NetworkFixtures.hiddenBiases();

            Neuron unitThree = Neuron.rectified("hiddenUnit3", hiddenBiases[3]);
            for (int slot = 0; slot < joinedRow.length; slot++) {
                Neuron inputSlot = Neuron.input("slot" + slot);
                inputSlot.setValue(joinedRow[slot]);
                unitThree.connectFrom(inputSlot, hiddenWeights[3][slot]);
            }
            double objectAnswer = unitThree.recomputeValue();
            double arrayAnswer = FeatureNetwork.rectify(
                    FeatureNetwork.weighAndAdd(joinedRow, hiddenWeights, hiddenBiases))[3];

            check("objects vs arrays: the same unit computed both ways agrees to 1e-9",
                    Math.abs(objectAnswer - arrayAnswer) < 1e-9);
            check("objects vs arrays: and both land on the lesson's 1.8724",
                    approx(objectAnswer, 1.8724));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    // ----- Part 2 -----------------------------------------------------

    private static void testLookUpStatCards() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            double[][] cards = model.lookUpStatCards(new int[] {1, 0, 1});
            check("lookUp: context [1, 0, 1] fetches pineapple, pizza, pineapple",
                    approxRow(cards[0], 0.38, -0.01)
                            && approxRow(cards[1], -1.12, 0.47)
                            && approxRow(cards[2], 0.38, -0.01));

            cards[0][0] = 999.0;
            check("lookUp: cards are CLONES — scribbling on one leaves the binder clean",
                    approxRow(model.statCardFor(1), 0.38, -0.01)
                            && approxRow(model.lookUpStatCards(new int[] {1, 0, 1})[0], 0.38, -0.01));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testJoinCards() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            double[] joinedRow = FeatureNetwork.joinCards(
                    model.lookUpStatCards(new int[] {1, 0, 1}));
            check("join: the three cards glue into the six-slot row from the lesson",
                    approxRow(joinedRow, 0.38, -0.01, -1.12, 0.47, 0.38, -0.01));
            check("join: order is meaning — [1, 0, 2] and [2, 0, 1] join differently",
                    !Arrays.equals(
                            FeatureNetwork.joinCards(model.lookUpStatCards(new int[] {1, 0, 2})),
                            FeatureNetwork.joinCards(model.lookUpStatCards(new int[] {2, 0, 1}))));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testUnrestrictedScores() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();

            double[] joinedRow = FeatureNetwork.joinCards(
                    model.lookUpStatCards(new int[] {1, 0, 1}));
            double[] hiddenSums = FeatureNetwork.weighAndAdd(joinedRow,
                    NetworkFixtures.hiddenWeights(), NetworkFixtures.hiddenBiases());
            check("pipeline: hidden weighted sums are [-0.1817, -1.1491, 0.3005, 1.8724]",
                    approxRow(hiddenSums, -0.1817, -1.1491, 0.3005, 1.8724));
            check("pipeline: the gate silences units 0 and 1",
                    approxRow(FeatureNetwork.rectify(hiddenSums), 0.0, 0.0, 0.3005, 1.8724));

            check("scores: context [1, 0, 1] scores [1.5504, -1.6160, -1.1503]",
                    approxRow(model.unrestrictedScores(new int[] {1, 0, 1}),
                            1.5504, -1.6160, -1.1503));
            check("scores: context [0, 1, 0] scores [-1.3026, 1.5619, 0.8662]",
                    approxRow(model.unrestrictedScores(new int[] {0, 1, 0}),
                            -1.3026, 1.5619, 0.8662));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testForecast() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            double[] forecast = model.forecast(new int[] {1, 0, 1});
            check("forecast: context [1, 0, 1] forecasts [0.9015, 0.0380, 0.0605]",
                    approxRow(forecast, 0.9015, 0.0380, 0.0605));
            check("forecast: entries sum to one",
                    approx(forecast[0] + forecast[1] + forecast[2], 1.0));
            check("forecast: no entry is exactly zero — softmax still cannot say never",
                    forecast[0] > 0.0 && forecast[1] > 0.0 && forecast[2] > 0.0);
            check("forecast: asking twice gives identical answers",
                    Arrays.equals(model.forecast(new int[] {1, 0, 1}),
                            model.forecast(new int[] {1, 0, 1})));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testLoss() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            check("loss: the real flashcard [1, 0, 1] -> pizza charges 0.1037",
                    approx(model.loss(new int[] {1, 0, 1}, 0), 0.1037));
            check("loss: the honest mixture [0, 1, 0] -> pepperoni charges 1.1377",
                    approx(model.loss(new int[] {0, 1, 0}, 2), 1.1377));
            check("loss: charging a nearly-impossible outcome costs over 3",
                    model.loss(new int[] {0, 1, 0}, 0) > 3.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testAverageLoss() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            check("averageLoss: a four-token history holds exactly ONE flashcard",
                    Math.abs(model.averageLoss(new int[] {1, 0, 1, 0})
                            - model.loss(new int[] {1, 0, 1}, 0)) < 1e-9);

            double trainingLoss = model.averageLoss(NetworkFixtures.trainingTokens());
            double validationLoss = model.averageLoss(NetworkFixtures.validationTokens());
            System.out.printf(
                    "  INFO  provided model — training loss %.4f over 119 flashcards,"
                            + " validation loss %.4f over 39%n",
                    trainingLoss, validationLoss);
            check("averageLoss: the provided model scores 0.3957 on the training history",
                    approx(trainingLoss, 0.3957));
            check("averageLoss: and 0.4013 on the validation history",
                    approx(validationLoss, 0.4013));

            double anchor = NetworkFixtures.nearlyEmpty(7).averageLoss(
                    NetworkFixtures.trainingTokens());
            System.out.printf(
                    "  INFO  nearly empty network (seed 7) — average training loss %.4f"
                            + "   (ln 3 = %.4f)%n", anchor, Math.log(3));
            check("averageLoss: a nearly empty NETWORK still lands on Chapter 2's ln(V) anchor",
                    Math.abs(anchor - Math.log(3)) < 0.02);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testCousins() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            double toppingGap = NetworkFixtures.cardDistance(
                    model.statCardFor(1), model.statCardFor(2));
            double pizzaToPineapple = NetworkFixtures.cardDistance(
                    model.statCardFor(0), model.statCardFor(1));
            double pizzaToPepperoni = NetworkFixtures.cardDistance(
                    model.statCardFor(0), model.statCardFor(2));
            System.out.printf(
                    "  INFO  card distances — pineapple-pepperoni %.4f,"
                            + " pizza-pineapple %.4f, pizza-pepperoni %.4f%n",
                    toppingGap, pizzaToPineapple, pizzaToPepperoni);
            check("cousins: the topping cards sit far closer to each other than to pizza's",
                    toppingGap < pizzaToPineapple && toppingGap < pizzaToPepperoni);

            double afterPineapple = model.forecast(new int[] {1, 0, 1})[0];
            double afterPepperoni = model.forecast(new int[] {1, 0, 2})[0];
            check("cousins: both topping-ending contexts forecast pizza above 85%",
                    afterPineapple > 0.85 && afterPepperoni > 0.85);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testAfterPizza() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            double[] forecast = model.forecast(new int[] {0, 1, 0});
            double[] counted = NetworkFixtures.countedRowAfterPizza();
            check("after pizza: the network forecasts [0.0366, 0.6428, 0.3206]",
                    approxRow(forecast, 0.0366, 0.6428, 0.3206));
            check("after pizza: pineapple's share sits within 0.05 of the counted 40/60",
                    Math.abs(forecast[1] - counted[1]) < 0.05);
            check("after pizza: pizza-after-pizza is tiny but not zero",
                    forecast[0] < 0.05 && forecast[0] > 0.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testNothingChanges() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            double[][] cardsBefore = {
                model.statCardFor(0), model.statCardFor(1), model.statCardFor(2)
            };
            for (int repetition = 0; repetition < 100; repetition++) {
                model.forecast(new int[] {1, 0, 1});
                model.loss(new int[] {0, 1, 0}, 2);
            }
            model.averageLoss(NetworkFixtures.trainingTokens());
            check("read-only: a hundred forecasts and grades changed no stat card",
                    Arrays.equals(model.statCardFor(0), cardsBefore[0])
                            && Arrays.equals(model.statCardFor(1), cardsBefore[1])
                            && Arrays.equals(model.statCardFor(2), cardsBefore[2]));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testParameterCount() {
        check("parameters: the provided model holds exactly 49 trainable numbers",
                NetworkFixtures.providedModel().countParameters() == 49);
    }

    private static void testShapeValidation() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            boolean shortContextRefused = false;
            try {
                model.forecast(new int[] {1, 0});
            } catch (IllegalArgumentException expected) {
                shortContextRefused = true;
            }
            check("shapes: a two-token context is refused — this model reads exactly three",
                    shortContextRefused);

            boolean badTokenRefused = false;
            try {
                model.forecast(new int[] {1, 0, 3});
            } catch (IllegalArgumentException expected) {
                badTokenRefused = true;
            }
            check("shapes: token 3 is refused — the binder has cards 0 through 2",
                    badTokenRefused);

            boolean tinyHistoryRefused = false;
            try {
                model.averageLoss(new int[] {1, 0, 1});
            } catch (IllegalArgumentException expected) {
                tinyHistoryRefused = true;
            }
            check("shapes: a three-token history is refused — it holds no flashcard",
                    tinyHistoryRefused);

            boolean mismatchRefused = false;
            try {
                FeatureNetwork.weighAndAdd(new double[] {1.0, 2.0, 3.0},
                        NetworkFixtures.practiceHiddenWeights(),
                        NetworkFixtures.practiceHiddenBiases());
            } catch (IllegalArgumentException expected) {
                mismatchRefused = true;
            }
            check("shapes: weighAndAdd refuses a row that does not match the weights",
                    mismatchRefused);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void printPunchlines() {
        try {
            FeatureNetwork model = NetworkFixtures.providedModel();
            System.out.println("\n--- The punchlines ---");
            System.out.printf("  after pizza:      network %s   counted from the history %s%n",
                    formatRow(model.forecast(new int[] {0, 1, 0})),
                    formatRow(NetworkFixtures.countedRowAfterPizza()));
            System.out.printf("  after pineapple:  network %s%n",
                    formatRow(model.forecast(new int[] {1, 0, 1})));
            System.out.printf("  after pepperoni:  network %s   — near-twins, from shared machinery%n",
                    formatRow(model.forecast(new int[] {1, 0, 2})));
            System.out.printf("  card distances:   pineapple-pepperoni %.2f   pizza-pineapple %.2f"
                            + "   pizza-pepperoni %.2f%n",
                    NetworkFixtures.cardDistance(model.statCardFor(1), model.statCardFor(2)),
                    NetworkFixtures.cardDistance(model.statCardFor(0), model.statCardFor(1)),
                    NetworkFixtures.cardDistance(model.statCardFor(0), model.statCardFor(2)));
            System.out.printf("  average loss:     %.4f training / %.4f validation"
                            + "   (Chapter 4's trained table: 0.3300 / 0.3311)%n",
                    model.averageLoss(NetworkFixtures.trainingTokens()),
                    model.averageLoss(NetworkFixtures.validationTokens()));
            System.out.println("  The gap to Chapter 4 is not the data's fault — these 49 numbers"
                    + " simply stopped training early,");
            System.out.println("  and nothing in this chapter can move them. Finding which number"
                    + " to move, and how, is Chapter 6.");
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

    private static String formatRow(double[] row) {
        StringBuilder builder = new StringBuilder("[");
        for (int entry = 0; entry < row.length; entry++) {
            builder.append(String.format("%.3f", row[entry]));
            if (entry < row.length - 1) {
                builder.append(", ");
            }
        }
        return builder.append("]").toString();
    }

    private static void check(String name, boolean ok) {
        System.out.println((ok ? "  PASS  " : "  FAIL  ") + name);
    }

    private static void todo(UnsupportedOperationException e) {
        System.out.println("  TODO  " + e.getMessage());
    }
}
