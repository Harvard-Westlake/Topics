import java.util.Random;

// PROVIDED — every fixed number this chapter uses.
//
// Two models live here. The PRACTICE network is the integer machine you
// trace by hand on Day 1. The PROVIDED model is a real (tiny) language
// model: its 49 numbers arrive pre-trained — gradient descent was run on
// this very order history ahead of time, and the results were rounded to
// two decimals and frozen into this file. The tools that training
// required have not been built in this course yet; that is Chapter 6's
// job. This week you are given the trained numbers, not the training.
public class NetworkFixtures {

    // The vocabulary, in identifier order — Chapter 4's, unchanged:
    //   0 = pizza   1 = pineapple   2 = pepperoni
    public static final String[] VOCABULARY = {"pizza", "pineapple", "pepperoni"};

    // Every forecast reads exactly this many earlier tokens.
    public static final int CONTEXT_LENGTH = 3;

    // ---------------------------------------------------------------
    // The PRACTICE network — Day 1's hand-trace machine.
    // Two inputs, two rectified hidden units, two linear outputs.
    // ---------------------------------------------------------------

    public static double[] practiceInputs() {
        return new double[] {1.0, 2.0};
    }

    public static double[][] practiceHiddenWeights() {
        return new double[][] {
            {1.0, -2.0},   // top hidden unit
            {3.0,  1.0},   // bottom hidden unit
        };
    }

    public static double[] practiceHiddenBiases() {
        return new double[] {1.0, -1.0};
    }

    public static double[][] practiceOutputWeights() {
        return new double[][] {
            {2.0, -1.0},   // first output unit
            {1.0,  1.0},   // second output unit
        };
    }

    public static double[] practiceOutputBiases() {
        return new double[] {0.0, 2.0};
    }

    // ---------------------------------------------------------------
    // The PROVIDED model — trained offline, rounded, frozen.
    // Vocabulary 3, card width 2, context 3, hidden units 4: 49 numbers.
    // ---------------------------------------------------------------

    // The binder of learned stat cards, one per token, two slots each.
    // Unlike Chapter 3's hand-written cards, no slot has a name: each
    // holds whatever value made forecasts better during training.
    // Worth noticing before any code runs: the two topping cards are
    // near-copies of each other, and far from pizza's card.
    public static double[][] statCards() {
        return new double[][] {
            {-1.12,  0.47},   // 0 pizza
            { 0.38, -0.01},   // 1 pineapple
            {-0.07, -0.06},   // 2 pepperoni
        };
    }

    // Hidden layer: 4 units, each with one weight per slot of the joined
    // six-slot row (three cards, two slots each) plus a bias.
    public static double[][] hiddenWeights() {
        return new double[][] {
            { 0.67,  0.25,  0.62,  0.15,  0.24,  0.11},
            {-1.11,  0.65,  0.42,  0.17, -1.13, -0.91},
            {-0.48, -0.33,  0.01,  0.06,  0.39, -0.44},
            { 0.26,  0.17, -0.63,  1.15,  0.41,  0.66},
        };
    }

    public static double[] hiddenBiases() {
        return new double[] {0.10, 0.09, 0.31, 0.38};
    }

    // Output layer: one unit per vocabulary token, each with one weight
    // per hidden unit plus a bias.
    public static double[][] outputWeights() {
        return new double[][] {
            {-0.37, -0.71, -0.04,  0.53},   // scores pizza
            { 0.38,  0.58, -0.31, -0.84},   // scores pineapple
            {-0.31,  0.58, -0.61, -0.18},   // scores pepperoni
        };
    }

    public static double[] outputBiases() {
        return new double[] {0.57, 0.05, -0.63};
    }

    // The provided model, assembled and frozen.
    public static FeatureNetwork providedModel() {
        return new FeatureNetwork(statCards(),
                hiddenWeights(), hiddenBiases(),
                outputWeights(), outputBiases(),
                CONTEXT_LENGTH);
    }

    // A nearly empty network: every card slot and weight is a small
    // random number near zero, every bias exactly zero. Near-zero
    // weights make near-zero scores, so every forecast is nearly
    // uniform — Chapter 4's ln(V) anchor holds for networks too, and the
    // Tester checks it.
    public static FeatureNetwork nearlyEmpty(long seed) {
        Random random = new Random(seed);
        int vocabularySize = VOCABULARY.length;
        int cardWidth = 2;
        int hiddenUnits = 4;
        int joinedWidth = CONTEXT_LENGTH * cardWidth;

        double[][] cards = new double[vocabularySize][cardWidth];
        for (int token = 0; token < vocabularySize; token++) {
            for (int slot = 0; slot < cardWidth; slot++) {
                cards[token][slot] = 0.02 * random.nextGaussian();
            }
        }
        double[][] hidden = new double[hiddenUnits][joinedWidth];
        for (int unit = 0; unit < hiddenUnits; unit++) {
            for (int slot = 0; slot < joinedWidth; slot++) {
                hidden[unit][slot] = 0.02 * random.nextGaussian();
            }
        }
        double[][] output = new double[vocabularySize][hiddenUnits];
        for (int token = 0; token < vocabularySize; token++) {
            for (int unit = 0; unit < hiddenUnits; unit++) {
                output[token][unit] = 0.02 * random.nextGaussian();
            }
        }
        return new FeatureNetwork(cards,
                hidden, new double[hiddenUnits],
                output, new double[vocabularySize],
                CONTEXT_LENGTH);
    }

    // ---------------------------------------------------------------
    // The order history — Chapter 4's, token for token.
    // ---------------------------------------------------------------

    // The TRAINING history: 122 tokens. Chapter 4's table read it as 121
    // adjacent-pair flashcards; this network needs three tokens of
    // context, so the same history holds 119 flashcards.
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

    // The VALIDATION history: 42 tokens, holding 39 three-token-context
    // flashcards. Chapter 2's boundary rule is still law: this data is
    // scored, never trained on — even offline.
    public static int[] validationTokens() {
        return new int[] {
            1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0,
            1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 2, 0,
            1, 0
        };
    }

    // Chapter 4's counted row for comparison: of the 60 training
    // transitions leaving pizza, 40 go to pineapple and 20 to pepperoni.
    public static double[] countedRowAfterPizza() {
        return new double[] {0.0, 40.0 / 60.0, 20.0 / 60.0};
    }

    // Straight-line distance between two stat cards — used by the Tester
    // to measure how close the learned cards ended up.
    public static double cardDistance(double[] firstCard, double[] secondCard) {
        double total = 0.0;
        for (int slot = 0; slot < firstCard.length; slot++) {
            double difference = firstCard[slot] - secondCard[slot];
            total += difference * difference;
        }
        return Math.sqrt(total);
    }
}
