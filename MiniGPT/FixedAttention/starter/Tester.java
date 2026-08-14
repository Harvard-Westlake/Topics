import java.util.Arrays;

// PROVIDED — reproduces every worked trace from the lesson page and runs the
// required tests. Complete the TODOs in order and rerun after each one:
// stages you have not implemented yet are reported as TODO, not FAIL.
public class Tester {

    public static void main(String[] args) {
        System.out.println("=== Part 1 (Day 1): uniform weights, softmax, blending ===");
        testUniformWeights();
        testSoftmax();
        testApplyWeights();

        System.out.println("\n=== Part 2 (Day 2): dot product, rules, full pipeline ===");
        testDotProduct();
        testRuleBasedAttention();
        testDotProductAttention();
        testCausality();
        testRetrieval();
        printMatrices();
    }

    // ----- Part 1 -----------------------------------------------------

    private static void testUniformWeights() {
        try {
            double[][] w = FixedAttention.uniformCausalWeights(3);
            check("uniform: row 2 is a third each",
                    approx(w[2][0], 1.0 / 3) && approx(w[2][1], 1.0 / 3) && approx(w[2][2], 1.0 / 3));
            check("uniform: every row sums to one", rowsSumToOne(w));
            check("uniform: future weights are EXACTLY zero",
                    w[0][1] == 0.0 && w[0][2] == 0.0 && w[1][2] == 0.0);
            check("uniform: one-token sequence gives one valid row",
                    FixedAttention.uniformCausalWeights(1).length == 1
                            && FixedAttention.uniformCausalWeights(1)[0][0] == 1.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testSoftmax() {
        try {
            double[] lessonTrace = {2.0, 1.0, 0.0};
            double[] result = FixedAttention.stableSoftmax(lessonTrace);
            check("softmax: [2,1,0] -> [0.6652, 0.2447, 0.0900]",
                    approx(result[0], 0.6652) && approx(result[1], 0.2447) && approx(result[2], 0.0900));
            check("softmax: input array was not mutated",
                    Arrays.equals(lessonTrace, new double[] {2.0, 1.0, 0.0}));

            double[] handRule = FixedAttention.stableSoftmax(new double[] {4.0, 0.0, 0.0});
            check("softmax: [4,0,0] -> [0.9647, 0.0177, 0.0177]",
                    approx(handRule[0], 0.9647) && approx(handRule[1], 0.0177) && approx(handRule[2], 0.0177));

            double[] equal = FixedAttention.stableSoftmax(new double[] {0.0, 0.0, 0.0});
            check("softmax: equal scores give equal weights (Stage 1!)",
                    approx(equal[0], 1.0 / 3) && approx(equal[1], 1.0 / 3) && approx(equal[2], 1.0 / 3));

            double[] a = FixedAttention.stableSoftmax(new double[] {5.0, 1.0, 1.0});
            double[] b = FixedAttention.stableSoftmax(new double[] {9.0, 5.0, 5.0});
            check("softmax: adding a constant to all scores changes nothing",
                    approx(a[0], b[0]) && approx(a[1], b[1]) && approx(a[2], b[2]));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testApplyWeights() {
        try {
            double[][] uniform = FixedAttention.uniformCausalWeights(3);
            double[][] outputs = FixedAttention.applyWeights(uniform, AttentionFixtures.threeCards());
            check("blend: uniform y1 = [1.0, 0.5, 0.5, 0.0]",
                    approxRow(outputs[1], 1.0, 0.5, 0.5, 0.0));
            check("blend: uniform y2 = [1.0, 0.6667, 0.3333, 0.0]",
                    approxRow(outputs[2], 1.0, 2.0 / 3, 1.0 / 3, 0.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    // ----- Part 2 -----------------------------------------------------

    private static void testDotProduct() {
        try {
            double[][] cards = AttentionFixtures.threeCards();
            check("dot: PINEAPPLE . PINEAPPLE = 2.0 (perfect match)",
                    approx(FixedAttention.dotProduct(cards[0], cards[2]), 2.0));
            check("dot: PINEAPPLE . PEPPERONI = 1.0 (partial match)",
                    approx(FixedAttention.dotProduct(cards[0], cards[1]), 1.0));
            check("dot: PINEAPPLE . GYM SOCK = 0.0 (complete mismatch)",
                    approx(FixedAttention.dotProduct(cards[0], AttentionFixtures.gymSock()), 0.0));
            check("dot: [2,1,0,0] . [1,1,0,0] = 3.0 (known vectors)",
                    approx(FixedAttention.dotProduct(
                            new double[] {2.0, 1.0, 0.0, 0.0}, new double[] {1.0, 1.0, 0.0, 0.0}), 3.0));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testRuleBasedAttention() {
        try {
            double[][] w = FixedAttention.ruleBasedCausalWeights(
                    AttentionFixtures.threeCards(), AttentionFixtures.MATCH_RULE);
            check("rule: Day 1 trace reproduced — row 2 = [0.9647, 0.0177, 0.0177]",
                    approx(w[2][0], 0.9647) && approx(w[2][1], 0.0177) && approx(w[2][2], 0.0177));
            check("rule: every row sums to one", rowsSumToOne(w));
            check("rule: future weights are EXACTLY zero", w[0][1] == 0.0 && w[1][2] == 0.0);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testDotProductAttention() {
        try {
            double[][] cards = AttentionFixtures.threeCards();
            double[][] w = FixedAttention.dotProductCausalWeights(cards);
            check("pipeline: row 1 weights = [0.3775, 0.6225]",
                    approx(w[1][0], 0.3775) && approx(w[1][1], 0.6225) && w[1][2] == 0.0);
            check("pipeline: row 2 weights = [0.3837, 0.2327, 0.3837]",
                    approx(w[2][0], 0.3837) && approx(w[2][1], 0.2327) && approx(w[2][2], 0.3837));
            check("pipeline: every row sums to one", rowsSumToOne(w));

            double[][] y = FixedAttention.applyWeights(w, cards);
            check("pipeline: y2 = [1.0, 0.7673, 0.2327, 0.0]",
                    approxRow(y[2], 1.0, 0.7673, 0.2327, 0.0));

            double[][] uniformY = FixedAttention.applyWeights(
                    FixedAttention.uniformCausalWeights(3), cards);
            System.out.printf(
                    "  INFO  sweet feature at position 2 — uniform: %.3f   dot product: %.3f%n",
                    uniformY[2][1], y[2][1]);
            check("pipeline: the spotlight beats the blur (0.767 > 0.667)",
                    y[2][1] > uniformY[2][1]);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testCausality() {
        try {
            double[][] original = AttentionFixtures.threeCards();
            double[][] originalOutputs = FixedAttention.applyWeights(
                    FixedAttention.dotProductCausalWeights(original), original);

            // Replace the FUTURE (the last card) and recompute everything.
            double[][] tampered = AttentionFixtures.threeCards();
            tampered[2] = AttentionFixtures.gymSock();
            double[][] tamperedOutputs = FixedAttention.applyWeights(
                    FixedAttention.dotProductCausalWeights(tampered), tampered);

            check("causality: changing the future left y0 and y1 identical",
                    Arrays.equals(originalOutputs[0], tamperedOutputs[0])
                            && Arrays.equals(originalOutputs[1], tamperedOutputs[1]));

            double[][] untouched = AttentionFixtures.threeCards();
            FixedAttention.dotProductCausalWeights(untouched);
            check("causality: the input sequence was not mutated",
                    Arrays.deepEquals(untouched, AttentionFixtures.threeCards()));
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void testRetrieval() {
        try {
            double[][] w = FixedAttention.ruleBasedCausalWeights(
                    AttentionFixtures.retrievalSequence(), AttentionFixtures.ORDER_RULE);
            int last = w.length - 1;
            double orderACards = w[last][0] + w[last][1];   // "OrderA" and "pineapple"
            double orderBCards = w[last][2] + w[last][3] + w[last][4];
            check("retrieval: the spotlight found Order A's pineapple, not Order B's pepperoni",
                    orderACards > 10 * orderBCards);
            System.out.printf(
                    "  INFO  final-row weight on the Order A cards: %.3f   on everything else earlier: %.3f%n",
                    orderACards, orderBCards);
        } catch (UnsupportedOperationException e) {
            todo(e);
        }
    }

    private static void printMatrices() {
        try {
            double[][] cards = AttentionFixtures.threeCards();
            System.out.println("\n--- Uniform causal attention (three-card table) ---");
            System.out.println(FixedAttention.formatMatrix(FixedAttention.uniformCausalWeights(3)));
            System.out.println("--- Rule-based attention, MATCH_RULE ---");
            System.out.println(FixedAttention.formatMatrix(
                    FixedAttention.ruleBasedCausalWeights(cards, AttentionFixtures.MATCH_RULE)));
            System.out.println("--- Fixed dot-product attention ---");
            System.out.println(FixedAttention.formatMatrix(
                    FixedAttention.dotProductCausalWeights(cards)));
            System.out.println("--- Rule-based attention, ORDER_RULE on the retrieval fixture ---");
            System.out.println(FixedAttention.formatMatrix(FixedAttention.ruleBasedCausalWeights(
                    AttentionFixtures.retrievalSequence(), AttentionFixtures.ORDER_RULE)));
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
        for (int i = 0; i < expected.length; i++) {
            if (!approx(actual[i], expected[i])) {
                return false;
            }
        }
        return true;
    }

    private static boolean rowsSumToOne(double[][] weights) {
        for (double[] row : weights) {
            double sum = 0.0;
            for (double entry : row) {
                sum += entry;
            }
            if (!approx(sum, 1.0)) {
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
