// PROVIDED — every fixed number this chapter uses.
//
// Two starting points live here. The FROZEN start is Chapter 5's provided
// model, digit for digit — the network whose 49 numbers you could grade
// but not move. This week it is the starting line: training resumes from
// exactly where the offline run left off. The FRESH start is the same
// architecture at the numbers the offline run STARTED from, before its
// ten steps — printed here as literals so you can rerun that training
// yourself and check the handed-down weights were honestly produced.
// (The fresh numbers were originally drawn in Python; Java's random
// number generator produces different draws from the same seed, so the
// draws are frozen into this file rather than regenerated.)
public class AutogradFixtures {

    // The vocabulary, in identifier order — Chapter 4's, unchanged:
    //   0 = pizza   1 = pineapple   2 = pepperoni
    public static final String[] VOCABULARY = {"pizza", "pineapple", "pepperoni"};

    // Every forecast reads exactly this many earlier tokens.
    public static final int CONTEXT_LENGTH = 3;

    // ---------------------------------------------------------------
    // The FROZEN start — Chapter 5's provided model, unchanged.
    // ---------------------------------------------------------------

    public static double[][] statCards() {
        return new double[][] {
            {-1.12,  0.47},   // 0 pizza
            { 0.38, -0.01},   // 1 pineapple
            {-0.07, -0.06},   // 2 pepperoni
        };
    }

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

    // Chapter 5's model, wrapped into trainable Values.
    public static TrainableFeatureNetwork frozenStart() {
        return new TrainableFeatureNetwork(statCards(),
                hiddenWeights(), hiddenBiases(),
                outputWeights(), outputBiases(),
                CONTEXT_LENGTH);
    }

    // ---------------------------------------------------------------
    // The FRESH start — the exact numbers the offline training began
    // from: cards and weights drawn at 0.6 scale, hidden biases 0.1,
    // output biases 0.0. Ten full-batch steps at learning rate 0.5
    // from here, rounded to two decimals, ARE the frozen model above.
    // ---------------------------------------------------------------

    public static double[][] freshCards() {
        return new double[][] {
            {-0.15352817306856023,  0.30685890750990835},
            {-0.13565769886986281, -0.18904105339871125},
            {-0.5580109141936604,  -0.1279811684527222},
        };
    }

    public static double[][] freshHiddenWeights() {
        return new double[][] {
            { 0.6671504285917924,   0.2544880104755617,   0.6221274473337999,
              0.1493416365990548,   0.23686178076825465,  0.11119599625703926},
            {-0.9996375151871659,   0.5131505812588423,   0.30383090753683223,
              0.29929082289716635, -1.0148187311090535,  -1.046332870365362},
            {-0.5337692068841579,  -0.2809135654399407,   0.18326759509946441,
             -0.027547038307551213, 0.3125849390525412,  -0.38534084992469625},
            { 0.18522188952652865,  0.23649268611552604, -0.39668240851928543,
              1.0305181904002456,   0.3339656135204733,   0.7182031427874047},
        };
    }

    public static double[] freshHiddenBiases() {
        return new double[] {0.1, 0.1, 0.1, 0.1};
    }

    public static double[][] freshOutputWeights() {
        return new double[][] {
            {-0.37219974868970623, -0.44370953773486393, -0.20642800749790083, -0.06385279892312638},
            { 0.3792472470192893,   0.14905635214181528, -0.26841293713929926, -0.5741473881974231},
            {-0.31235418603992327,  0.7325527889399422,  -0.48476785698470126,  0.14685524838964512},
        };
    }

    public static double[] freshOutputBiases() {
        return new double[] {0.0, 0.0, 0.0};
    }

    public static TrainableFeatureNetwork freshStart() {
        return new TrainableFeatureNetwork(freshCards(),
                freshHiddenWeights(), freshHiddenBiases(),
                freshOutputWeights(), freshOutputBiases(),
                CONTEXT_LENGTH);
    }

    // ---------------------------------------------------------------
    // The order history — Chapters 4 and 5's, token for token.
    // ---------------------------------------------------------------

    // The TRAINING history: 122 tokens, holding 119 three-token-context
    // flashcards. Full-batch training grades every one on every step.
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

    // The VALIDATION history: 42 tokens, 39 flashcards. Chapter 2's
    // boundary rule is still law: this data is graded, never trained on.
    public static int[] validationTokens() {
        return new int[] {
            1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0,
            1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 2, 0,
            1, 0
        };
    }

    // A deliberately different pattern: 0, 1, 2 repeated — 30 tokens,
    // 27 flashcards, and every context has exactly one possible next
    // token. No mixture means the floor is zero: a machine that
    // memorizes the drumbeat can drive its loss as low as it likes.
    public static int[] drumbeatTokens() {
        int[] tokens = new int[30];
        for (int position = 0; position < tokens.length; position++) {
            tokens[position] = position % 3;
        }
        return tokens;
    }

    // Chapter 4's counted row for comparison: of the 60 training
    // transitions leaving pizza, 40 go to pineapple and 20 to pepperoni.
    public static double[] countedRowAfterPizza() {
        return new double[] {0.0, 40.0 / 60.0, 20.0 / 60.0};
    }

    // Straight-line distance between two stat cards — used to watch the
    // cousins during training.
    public static double cardDistance(double[] firstCard, double[] secondCard) {
        double total = 0.0;
        for (int slot = 0; slot < firstCard.length; slot++) {
            double difference = firstCard[slot] - secondCard[slot];
            total += difference * difference;
        }
        return Math.sqrt(total);
    }
}
