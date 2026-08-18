// The forecast pipeline, as arrays and loops.
//
// This is the same arithmetic as the Neuron objects, written the way real
// systems write it: a layer is a weight table plus a bias list, and one
// loop does what a whole row of neuron objects did. The model is five
// arrays — a binder of stat cards and two layers of weights and biases —
// and this chapter never changes any of them.
//
// State rules for the whole class — who reads, who writes:
//   - the constructor COPIES the five arrays it is given, once
//   - every other method only READS them and CREATES new arrays to return
//   - nothing is ever accumulated, and nothing is ever overwritten
// Chapter 4's bucket-and-step machinery is deliberately absent. The
// arrays that would learn have no way to change until Chapter 6.
public class FeatureNetwork {

    private final double[][] statCards;      // one learned card per token: [token][slot]
    private final double[][] hiddenWeights;  // [hiddenUnit][inputSlot]
    private final double[] hiddenBiases;     // one per hidden unit
    private final double[][] outputWeights;  // [vocabToken][hiddenUnit]
    private final double[] outputBiases;     // one per vocabulary token
    private final int contextLength;         // how many earlier tokens each forecast reads

    // PROVIDED — copies every array so the network's numbers are frozen at
    // construction, and checks that all five shapes agree.
    public FeatureNetwork(double[][] statCards,
                          double[][] hiddenWeights, double[] hiddenBiases,
                          double[][] outputWeights, double[] outputBiases,
                          int contextLength) {
        if (contextLength <= 0) {
            throw new IllegalArgumentException("Context length must be positive.");
        }
        this.statCards = deepCopy(statCards);
        this.hiddenWeights = deepCopy(hiddenWeights);
        this.hiddenBiases = hiddenBiases.clone();
        this.outputWeights = deepCopy(outputWeights);
        this.outputBiases = outputBiases.clone();
        this.contextLength = contextLength;

        int cardWidth = statCards[0].length;
        for (double[] card : statCards) {
            requireLength(card, cardWidth, "Every stat card needs the same number of slots.");
        }
        int joinedWidth = contextLength * cardWidth;
        for (double[] weightRow : hiddenWeights) {
            requireLength(weightRow, joinedWidth,
                    "Each hidden unit needs one weight per slot of the joined row.");
        }
        requireLength(hiddenBiases, hiddenWeights.length,
                "One bias per hidden unit.");
        for (double[] weightRow : outputWeights) {
            requireLength(weightRow, hiddenWeights.length,
                    "Each output unit needs one weight per hidden unit.");
        }
        requireLength(outputBiases, outputWeights.length, "One bias per output unit.");
        if (outputWeights.length != statCards.length) {
            throw new IllegalArgumentException(
                    "One output unit per vocabulary token: "
                            + statCards.length + " tokens but "
                            + outputWeights.length + " output units.");
        }
    }

    public int vocabularySize() {
        return statCards.length;
    }

    public int contextLength() {
        return contextLength;
    }

    // PROVIDED — Chapter 4's stable softmax, unchanged: subtract the max,
    // exponentiate, normalize. You built this last week; this week it is a
    // tool you are handed back. It READS its input and CREATES a new array.
    public static double[] stableSoftmax(double[] row) {
        double max = row[0];
        for (double entry : row) {
            max = Math.max(max, entry);
        }
        double[] shares = new double[row.length];
        double sum = 0.0;
        for (int position = 0; position < row.length; position++) {
            shares[position] = Math.exp(row[position] - max);
            sum += shares[position];
        }
        for (int position = 0; position < row.length; position++) {
            shares[position] /= sum;
        }
        return shares;
    }

    // TODO 3: weigh and add — one whole layer, one loop.
    //
    // The question: a row of neuron objects each did weigh-and-add over
    // the same inputs. What does that look like when the layer is a
    // weight table instead of objects?
    // The answer: one loop per unit. Each unit owns one row of the weight
    // table and one bias; its weighted sum is bias plus every input slot
    // multiplied by that unit's weight for the slot. The unit-by-unit
    // arithmetic is identical to Neuron.weighAndAddInputs — the Tester
    // proves it to fifteen decimal places.
    //
    // State: READS inputRow, layerWeights, and layerBiases; CREATES and
    // returns a new array; alters nothing.
    //
    // Dimensions:
    // - inputRow:     length-n row of incoming values.
    // - layerWeights: one row per unit, each row length n —
    //                 layerWeights[unit][slot].
    // - layerBiases:  one bias per unit.
    // - returns:      NEW array, one weighted sum per unit:
    //                 result[unit] = layerBiases[unit]
    //                     + sum over every slot of
    //                       layerWeights[unit][slot] * inputRow[slot]
    //
    // Example from the lesson (the practice network's hidden layer):
    //   inputRow [1, 2], weights [[1, -2], [3, 1]], biases [1, -1]
    //   -> [ 1 + 1*1 + (-2)*2,  -1 + 3*1 + 1*2 ]  =  [-2, 4]
    //
    // Call requireMatchingShapes(inputRow, layerWeights, layerBiases) first.
    public static double[] weighAndAdd(double[] inputRow,
                                       double[][] layerWeights, double[] layerBiases) {
        throw new UnsupportedOperationException("TODO 3: weighAndAdd");
    }

    // TODO 4: rectify — the gate, applied to a whole layer.
    //
    // The question: why not feed weighted sums straight into the next
    // layer of weighted sums?
    // The answer: because two weigh-and-adds back to back collapse into
    // one — problem B2 makes you prove it. The gate breaks the collapse:
    // silence every negative weighted sum to zero, pass the rest through
    // unchanged. A silenced unit contributes nothing downstream, so which
    // units are awake depends on the input — that is what lets the same
    // weights answer differently for different contexts.
    //
    // State: READS weightedSums; CREATES and returns a new array; the
    // input array must come back from this call unchanged.
    //
    // Dimensions:
    // - weightedSums: one weighted sum per unit.
    // - returns:      NEW array of the same length —
    //                 result[unit] = Math.max(0.0, weightedSums[unit])
    //
    // Example from the lesson: [-2, 4] -> [0, 4] — the top practice unit
    // is silenced, the bottom one passes through.
    public static double[] rectify(double[] weightedSums) {
        throw new UnsupportedOperationException("TODO 4: rectify");
    }

    // TODO 5: look up — every context token fetches its stat card.
    //
    // The question: the network computes with slots full of decimals, but
    // a context arrives as bare token numbers like [1, 0, 1]. How does a
    // token number become numbers a layer can weigh?
    // The answer: it doesn't get computed — it gets FETCHED. Token 1 means
    // "hand me card 1 from the binder," nothing more. The number 1 never
    // enters any arithmetic; it is an address. (That is why look-up is not
    // multiplication: doubling the token number fetches a different card,
    // it does not double anything.)
    //
    // State: READS statCards; CREATES and returns clones of the fetched
    // cards, so no caller can reach into the binder and alter it.
    //
    // Dimensions:
    // - contextTokens: exactly contextLength token numbers, oldest first.
    // - returns:       NEW array of contextLength cards; entry number
    //                  cardNumber is a CLONE of
    //                  statCards[contextTokens[cardNumber]].
    //
    // Example from the lesson: context [1, 0, 1] fetches
    //   card 1 (pineapple) [ 0.38, -0.01]
    //   card 0 (pizza)     [-1.12,  0.47]
    //   card 1 (pineapple) [ 0.38, -0.01]   — the same card, fetched twice.
    //
    // Call requireContext(contextTokens) first.
    public double[][] lookUpStatCards(int[] contextTokens) {
        throw new UnsupportedOperationException("TODO 5: lookUpStatCards");
    }

    // TODO 6: join — the fetched cards become one row.
    //
    // The question: the hidden layer wants one flat row of input slots,
    // but look-up produced a stack of cards. How do they meet?
    // The answer: glue the cards end to end, in context order. Card 0's
    // slots come first, then card 1's, and so on. Order is meaning here:
    // the hidden layer's weight for slot 4 is a weight for "slot 0 of the
    // card two positions back," so shuffling the cards would silently
    // change what every weight means.
    //
    // State: READS cards; CREATES and returns a new row; alters nothing.
    //
    // Dimensions:
    // - cards:   contextLength cards, each cardWidth slots.
    // - returns: NEW row of contextLength * cardWidth slots —
    //            result[cardNumber * cardWidth + slot]
    //                = cards[cardNumber][slot]
    //
    // Example from the lesson: the three cards fetched for [1, 0, 1] join
    // into the six-slot row
    //   [ 0.38, -0.01, -1.12, 0.47, 0.38, -0.01 ]
    public static double[] joinCards(double[][] cards) {
        throw new UnsupportedOperationException("TODO 6: joinCards");
    }

    // TODO 7: the full pipeline up to the scores.
    //
    // The question: five machines are built — look up, join, weigh and
    // add, rectify, weigh and add again. What order do they run in?
    // The answer: exactly that order, each one's output feeding the next:
    //
    //   1. lookUpStatCards(contextTokens)                    fetch
    //   2. joinCards(...)                                    glue
    //   3. weighAndAdd(..., hiddenWeights, hiddenBiases)     mix
    //   4. rectify(...)                                      gate
    //   5. weighAndAdd(..., outputWeights, outputBiases)     score
    //
    // The result is one unrestricted score per vocabulary token — any
    // real number, positive or negative. You met these in Chapter 4
    // under their standard name: logits. Last week a logit was read
    // straight out of a table row; this week it is COMPUTED from
    // features. Softmax neither knows nor cares which.
    //
    // State: READS the five frozen arrays; CREATES intermediate rows and
    // returns the final one; alters nothing.
    //
    // Dimensions:
    // - contextTokens: exactly contextLength token numbers, oldest first.
    // - returns:       NEW length-V row of unrestricted scores.
    //
    // Example from the lesson: context [1, 0, 1] (pineapple pizza
    // pineapple) flows
    //   joined row [0.38, -0.01, -1.12, 0.47, 0.38, -0.01]
    //   -> hidden weighted sums [-0.1817, -1.1491,  0.3005,  1.8724]
    //   -> after the gate       [ 0.0,     0.0,     0.3005,  1.8724]
    //   -> scores               [ 1.5504, -1.6160, -1.1503]
    //
    // Call requireContext(contextTokens) first.
    public double[] unrestrictedScores(int[] contextTokens) {
        throw new UnsupportedOperationException("TODO 7: unrestrictedScores");
    }

    // TODO 8: the forecast — scores become a probability distribution.
    //
    // The question: the scores [1.5504, -1.6160, -1.1503] are not yet a
    // forecast. What turns them into one?
    // The answer: Chapter 4's answer, unchanged — the stable softmax.
    // The pipeline before softmax is completely different from last
    // week's table row, and softmax cannot tell: it takes a row of
    // unrestricted scores and returns shares that sum to one.
    //
    // State: READS the frozen arrays (through unrestrictedScores);
    // CREATES and returns a new row. Forecasting a thousand times leaves
    // the network bit-for-bit identical — the Tester checks.
    //
    // Dimensions:
    // - contextTokens: exactly contextLength token numbers, oldest first.
    // - returns:       NEW length-V probability row, positive everywhere,
    //                  summing to one.
    //
    // Example from the lesson: context [1, 0, 1] forecasts
    //   [0.9015, 0.0380, 0.0605]
    // — 90% pizza, 4% pineapple, 6% pepperoni.
    public double[] forecast(int[] contextTokens) {
        throw new UnsupportedOperationException("TODO 8: forecast");
    }

    // TODO 9: the grade — Chapter 4's loss, charged to this pipeline.
    //
    // The question: does a fancier forecaster need a fancier grade?
    // The answer: no. The grade never looks at the machinery — only at
    // the probability the forecast gave the truth. Charge the negative
    // natural log of that one number, exactly as in Chapter 4.
    //
    //   loss = -Math.log( forecast(contextTokens)[targetToken] )
    //
    // State: READS only; returns one double; alters nothing. In Chapter 4
    // this grade fed a gradient. This week the grade is computed and then
    // NOTHING HAPPENS — there is no bucket to pour a slope into.
    //
    // Dimensions:
    // - contextTokens: the flashcard's front — contextLength tokens.
    // - targetToken:   the flashcard's back — what the history shows next.
    // - returns:       one double, 0 for certainty in the truth, growing
    //                  as the model is more surprised.
    //
    // Examples from the lesson:
    //   loss([1, 0, 1], 0) = -ln(0.9015) = 0.1037   (a good forecast)
    //   loss([0, 1, 0], 2) = -ln(0.3206) = 1.1377   (an honest mixture)
    //
    // Call requireContext(contextTokens) and requireToken(targetToken)
    // first.
    public double loss(int[] contextTokens, int targetToken) {
        throw new UnsupportedOperationException("TODO 9: loss");
    }

    // TODO 10: the report card — average loss over a whole history.
    //
    // The question: Chapter 4 graded every adjacent pair. What changes
    // now that a forecast needs contextLength tokens of context instead
    // of one?
    // The answer: the first few tokens of a history cannot be predicted —
    // there is not enough context in front of them. The first gradable
    // position is contextLength, so a history of n tokens holds
    // n - contextLength flashcards, not n - 1. The 122-token training
    // history that gave Chapter 4's table 121 flashcards gives this
    // network 119.
    //
    // State: READS only; returns one double; alters nothing.
    //
    // Dimensions:
    // - tokens:  a history of at least contextLength + 1 tokens.
    // - returns: the mean of
    //            loss(tokens[position - contextLength .. position - 1],
    //                 tokens[position])
    //            over position = contextLength .. tokens.length - 1.
    //
    // Examples from the lesson:
    //   {1, 0, 1, 0} holds exactly one flashcard: context [1, 0, 1],
    //     target 0 — so its average loss equals loss([1, 0, 1], 0).
    //   The provided model scores 0.3957 on the training history and
    //     0.4013 on the validation history.
    //
    // Call requireHistory(tokens) first.
    public double averageLoss(int[] tokens) {
        throw new UnsupportedOperationException("TODO 10: averageLoss");
    }

    // ---------------------------------------------------------------
    // PROVIDED helpers — used by the Tester; do not modify.
    // ---------------------------------------------------------------

    // Count every number training would be allowed to change. Walk the
    // arithmetic before you run it (problem D3 asks you to):
    //   stat cards      V * D             3 * 2      =  6
    //   hidden layer    (C*D) * H + H     6 * 4 + 4  = 28
    //   output layer    H * V + V         4 * 3 + 3  = 15
    //   total                                          49
    public int countParameters() {
        int cardNumbers = statCards.length * statCards[0].length;
        int hiddenNumbers = hiddenWeights.length * hiddenWeights[0].length
                + hiddenBiases.length;
        int outputNumbers = outputWeights.length * outputWeights[0].length
                + outputBiases.length;
        return cardNumbers + hiddenNumbers + outputNumbers;
    }

    // Defensive copy for tests and printing — READS the binder, hands
    // back a clone.
    public double[] statCardFor(int token) {
        requireToken(token);
        return statCards[token].clone();
    }

    // PROVIDED validators — call these where the TODO comments say to.

    public void requireContext(int[] contextTokens) {
        if (contextTokens == null || contextTokens.length != contextLength) {
            throw new IllegalArgumentException(
                    "A context needs exactly " + contextLength + " tokens.");
        }
        for (int token : contextTokens) {
            requireToken(token);
        }
    }

    public void requireToken(int token) {
        if (token < 0 || token >= statCards.length) {
            throw new IllegalArgumentException(
                    "Token " + token + " is outside [0, " + statCards.length + ").");
        }
    }

    public void requireHistory(int[] tokens) {
        if (tokens == null || tokens.length < contextLength + 1) {
            throw new IllegalArgumentException(
                    "A history needs at least " + (contextLength + 1)
                            + " tokens to hold one flashcard.");
        }
        for (int token : tokens) {
            requireToken(token);
        }
    }

    public static void requireMatchingShapes(double[] inputRow,
                                             double[][] layerWeights, double[] layerBiases) {
        if (layerWeights.length != layerBiases.length) {
            throw new IllegalArgumentException(
                    layerWeights.length + " weight rows but "
                            + layerBiases.length + " biases — one bias per unit.");
        }
        for (double[] weightRow : layerWeights) {
            if (weightRow.length != inputRow.length) {
                throw new IllegalArgumentException(
                        "A unit has " + weightRow.length + " weights but the input row has "
                                + inputRow.length + " slots — one weight per slot.");
            }
        }
    }

    private static void requireLength(double[] row, int expected, String message) {
        if (row.length != expected) {
            throw new IllegalArgumentException(
                    message + " (expected " + expected + ", got " + row.length + ")");
        }
    }

    private static double[][] deepCopy(double[][] table) {
        double[][] copy = new double[table.length][];
        for (int rowNumber = 0; rowNumber < table.length; rowNumber++) {
            copy[rowNumber] = table[rowNumber].clone();
        }
        return copy;
    }
}
