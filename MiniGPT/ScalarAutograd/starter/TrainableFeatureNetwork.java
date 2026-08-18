import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

// Chapter 5's network, rebuilt from receipts — and finally trainable.
//
// The architecture is identical: a binder of stat cards, a hidden layer,
// a gate, an output layer. What changed is the material. Every one of the
// 49 numbers is now a Value — a leaf receipt — so every forecast leaves a
// paper trail from the loss all the way back into the binder, and
// backward() can follow it. Chapter 5 cloned its fetched cards so nothing
// could touch the binder; this chapter hands out the REAL cards, because
// blame reaching the binder is the whole point.
//
// State rules for the whole class — who reads, who writes:
//   - the constructor wraps the given numbers into parameter Values, once
//   - TODOs 8-11 (Forecast and Grade) CREATE receipts and write nothing
//     that exists — building a loss graph changes no parameter
//   - backward() (called by the Trainer) writes parameter GRADIENTS
//   - zeroGradients (TODO 12, Reset) writes gradients back to zero
//   - Value.setNumber (called by the Trainer's Nudge) is the only thing
//     anywhere that moves a parameter's NUMBER
public class TrainableFeatureNetwork {

    private final Value[][] statCards;      // one learned card per token: [token][slot]
    private final Value[][] hiddenWeights;  // [hiddenUnit][inputSlot]
    private final Value[] hiddenBiases;     // one per hidden unit
    private final Value[][] outputWeights;  // [vocabToken][hiddenUnit]
    private final Value[] outputBiases;     // one per vocabulary token
    private final int contextLength;        // how many earlier tokens each forecast reads
    private final List<Value> parameters = new ArrayList<>();

    // PROVIDED — checks the five shapes agree, then wraps every number
    // into a labeled parameter Value and collects all 49 into one list.
    public TrainableFeatureNetwork(double[][] statCards,
                                   double[][] hiddenWeights, double[] hiddenBiases,
                                   double[][] outputWeights, double[] outputBiases,
                                   int contextLength) {
        if (contextLength <= 0) {
            throw new IllegalArgumentException("Context length must be positive.");
        }
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
        requireLength(hiddenBiases, hiddenWeights.length, "One bias per hidden unit.");
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

        this.statCards = wrapTable(statCards, "card");
        this.hiddenWeights = wrapTable(hiddenWeights, "hiddenWeight");
        this.hiddenBiases = wrapRow(hiddenBiases, "hiddenBias");
        this.outputWeights = wrapTable(outputWeights, "outputWeight");
        this.outputBiases = wrapRow(outputBiases, "outputBias");
    }

    private Value[][] wrapTable(double[][] table, String name) {
        Value[][] wrapped = new Value[table.length][];
        for (int rowNumber = 0; rowNumber < table.length; rowNumber++) {
            wrapped[rowNumber] = new Value[table[rowNumber].length];
            for (int slot = 0; slot < table[rowNumber].length; slot++) {
                Value parameter = new Value(table[rowNumber][slot],
                        name + "[" + rowNumber + "][" + slot + "]");
                wrapped[rowNumber][slot] = parameter;
                parameters.add(parameter);
            }
        }
        return wrapped;
    }

    private Value[] wrapRow(double[] row, String name) {
        Value[] wrapped = new Value[row.length];
        for (int slot = 0; slot < row.length; slot++) {
            Value parameter = new Value(row[slot], name + "[" + slot + "]");
            wrapped[slot] = parameter;
            parameters.add(parameter);
        }
        return wrapped;
    }

    // PROVIDED — every number training is allowed to change, as live
    // Values. The Trainer's Nudge and your Reset both walk this list.
    public List<Value> parameters() {
        return Collections.unmodifiableList(parameters);
    }

    public int countParameters() {
        return parameters.size();
    }

    public int vocabularySize() {
        return statCards.length;
    }

    public int contextLength() {
        return contextLength;
    }

    // PROVIDED — live parameter Values, for the wiggle referee and the
    // punchlines. These are the real receipts, not copies.
    public Value statCardValue(int token, int slot) {
        requireToken(token);
        return statCards[token][slot];
    }

    public Value hiddenWeightValue(int unit, int slot) {
        return hiddenWeights[unit][slot];
    }

    public Value outputBiasValue(int token) {
        requireToken(token);
        return outputBiases[token];
    }

    // PROVIDED — plain-number snapshots (clones) for printing and for
    // comparing a trained network against the frozen fixture.
    public double[][] statCardNumbers() {
        return numbersOf(statCards);
    }

    public double[][] hiddenWeightNumbers() {
        return numbersOf(hiddenWeights);
    }

    public double[] hiddenBiasNumbers() {
        return numbersOf(hiddenBiases);
    }

    public double[][] outputWeightNumbers() {
        return numbersOf(outputWeights);
    }

    public double[] outputBiasNumbers() {
        return numbersOf(outputBiases);
    }

    private static double[][] numbersOf(Value[][] table) {
        double[][] numbers = new double[table.length][];
        for (int rowNumber = 0; rowNumber < table.length; rowNumber++) {
            numbers[rowNumber] = numbersOf(table[rowNumber]);
        }
        return numbers;
    }

    private static double[] numbersOf(Value[] row) {
        double[] numbers = new double[row.length];
        for (int slot = 0; slot < row.length; slot++) {
            numbers[slot] = row[slot].number();
        }
        return numbers;
    }

    // PROVIDED — Chapter 4's stable softmax, for reporting only. Training
    // never calls it: the loss below goes through the receipts instead.
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

    // PROVIDED — the forecast as plain probabilities, for printing and
    // punchlines. It builds score receipts and reads their numbers; the
    // receipts are simply never audited. Grading writes no parameter.
    public double[] forecast(int[] contextTokens) {
        return stableSoftmax(numbersOf(unrestrictedScoreValues(contextTokens)));
    }

    // TODO 8: weigh and add — Chapter 5's layer loop, third notation.
    //
    // The question: you wrote this loop with Neuron objects, then with
    // double arrays. What changes when the layer is made of Values?
    // The answer: nothing but the material. Each unit starts from its
    // bias and adds weight-times-input for every slot, in slot order —
    // except that + and * are now .add and .multiply, so every step of
    // the arithmetic writes a receipt. The numbers that come out are
    // identical to Chapter 5's to the last bit; the difference is that
    // these numbers remember where they came from.
    //
    // State: READS the ingredient Values; CREATES receipts; alters
    // nothing that exists.
    //
    // Dimensions:
    // - inputRow:     length-n row of incoming Values.
    // - layerWeights: one row per unit, each row length n —
    //                 layerWeights[unit][slot].
    // - layerBiases:  one bias Value per unit.
    // - returns:      NEW array, one weighted-sum Value per unit. For
    //                 each unit: start from layerBiases[unit], then for
    //                 each slot in ascending order
    //                   total = total.add(
    //                       layerWeights[unit][slot].multiply(inputRow[slot]))
    //
    // Example from the lesson: the frozen model's hidden layer over the
    // joined row for context [1, 0, 1] lands on weighted-sum numbers
    // [-0.1817, -1.1491, 0.3005, 1.8724] — Chapter 5's numbers exactly.
    //
    // Call requireMatchingShapes(inputRow, layerWeights, layerBiases)
    // first.
    public static Value[] weighAndAddValues(Value[] inputRow,
                                            Value[][] layerWeights, Value[] layerBiases) {
        throw new UnsupportedOperationException("TODO 8: weighAndAddValues");
    }

    // TODO 9: the pipeline up to the scores — fetch, join, mix, gate, score.
    //
    // The question: Chapter 5's pipeline cloned each fetched card so the
    // binder could never be touched. Why must this one do the opposite?
    // The answer: because the paper trail has to reach the binder. If the
    // joined row held copies, backward() would deliver blame to the
    // copies and the real cards would never learn. So the joined row's
    // entries ARE the parameter Values themselves — the same receipt can
    // sit in two row positions when a token appears twice, and that is
    // exactly how one card collects blame from both positions.
    //
    // The order, unchanged from Chapter 5:
    //   1. fetch    — joinedRow[cardNumber * cardWidth + slot]
    //                   = statCards[contextTokens[cardNumber]][slot]
    //                 (both loops; no clones, no new Values)
    //   2. mix      — weighAndAddValues(joinedRow, hiddenWeights, hiddenBiases)
    //   3. gate     — call .rectify() on each hidden sum, into a new array
    //   4. score    — weighAndAddValues(gated, outputWeights, outputBiases)
    //
    // State: READS the parameters; CREATES receipts; alters nothing.
    //
    // Dimensions:
    // - contextTokens: exactly contextLength token numbers, oldest first.
    // - returns:       NEW length-V array of score Values.
    //
    // Example from the lesson: context [1, 0, 1] scores
    // [1.5504, -1.6160, -1.1503] — the logits of Chapter 5, reborn as
    // receipts.
    //
    // Call requireContext(contextTokens) first. The card width is
    // statCards[0].length.
    public Value[] unrestrictedScoreValues(int[] contextTokens) {
        throw new UnsupportedOperationException("TODO 9: unrestrictedScoreValues");
    }

    // TODO 10: the loss, written for the audit.
    //
    // The question: Chapter 4's grade was -ln(p_target), computed through
    // softmax. Softmax needs division, which Value does not have. How is
    // the same grade built from the receipts you own?
    // The answer: algebra first. -ln of exp(z_t - m) / sumOfExponentials
    // is ln(sumOfExponentials) minus (z_t - m) — the division dissolves
    // into a subtraction of logarithms. So:
    //
    //   1. Find m, the largest score NUMBER, with a plain double loop —
    //      bookkeeping, not blamable arithmetic. Wrap it once:
    //      new Value(m, "maxShift"). Chapter 4 proved the shift changes
    //      no share; treating it as a constant leaf keeps the receipts
    //      honest and the exponentials safe from overflow.
    //   2. shifted[k] = scoreValues[k].subtract(maxShift) for every k.
    //   3. sumOfExponentials = shifted[0].exponential(), then .add each
    //      later shifted[k].exponential() in order.
    //   4. return sumOfExponentials.naturalLog()
    //                 .subtract(shifted[targetToken]);
    //
    // State: READS the score Values; CREATES receipts; alters nothing.
    //
    // Dimensions:
    // - scoreValues: one score Value per vocabulary token.
    // - targetToken: the flashcard's back — what the history shows next.
    // - returns:     one Value whose number is the loss.
    //
    // Example from the lesson: the scores for [1, 0, 1] with target
    // pizza give loss 0.1037 — Chapter 5's number, now with a paper
    // trail. After backward(), the score receipts read
    // [-0.0985, 0.0380, 0.0605]: the forecast minus one-hot. Chapter 4's
    // shortcut, rediscovered by the audit.
    //
    // Call requireToken(targetToken) first.
    public Value lossValueFromScores(Value[] scoreValues, int targetToken) {
        throw new UnsupportedOperationException("TODO 10: lossValueFromScores");
    }

    // PROVIDED — the grade for one flashcard, front to back.
    public Value lossValue(int[] contextTokens, int targetToken) {
        return lossValueFromScores(unrestrictedScoreValues(contextTokens), targetToken);
    }

    // TODO 11: the report card — one graph for a whole history.
    //
    // The question: Chapter 4 poured each flashcard's slope into a bucket
    // and averaged. Where did the bucket go?
    // The answer: into the graph. Grade every flashcard, chain the grades
    // together with .add, and multiply the total by one over the
    // flashcard count (a constant leaf: new Value(1.0 / flashcardCount)).
    // The result is ONE receipt for the whole history's average loss —
    // audit it once and every parameter receives its averaged blame in a
    // single backward pass. The accumulation Chapter 4 wrote by hand is
    // now just += doing its job across 119 subgraphs.
    //
    // Flashcards work exactly as in Chapter 5: the first gradable
    // position is contextLength, so a history of n tokens holds
    // n - contextLength flashcards — 122 training tokens hold 119.
    //
    // State: READS the parameters; CREATES receipts; alters nothing.
    //
    // Dimensions:
    // - tokens:  a history of at least contextLength + 1 tokens.
    // - returns: one Value — the mean of lossValue over every flashcard,
    //            built as (sum of losses).multiply(1/flashcardCount).
    //
    // Examples from the lesson: the frozen start scores 0.3957 on the
    // training history and 0.4013 on validation — Chapter 5's report
    // card, reproduced by a graph you can audit.
    //
    // Call requireHistory(tokens) first.
    public Value averageLossValue(int[] tokens) {
        throw new UnsupportedOperationException("TODO 11: averageLossValue");
    }

    // PROVIDED — the report card as a plain number, for printing. It
    // builds the graph and reads one number; the receipts go unaudited.
    public double averageLossNumber(int[] tokens) {
        return averageLossValue(tokens).number();
    }

    // TODO 12: Reset — wipe every parameter's accumulated blame.
    //
    // The question: each training step builds a FRESH graph, so the
    // scratch receipts are born with zero gradient. What still carries
    // blame over from last step?
    // The answer: the parameters — the 49 leaves that survive from graph
    // to graph. Without a Reset, Monday's audit and Tuesday's audit add
    // together, and the Nudge strides down a slope that belongs to no
    // single step. Loop over parameters() and call zeroGradient() on
    // each.
    //
    // State: WRITES every parameter's gradient to 0.0; numbers untouched.
    //
    // Machine-verified: audit the flashcard [1, 0, 1] -> pizza once and
    // pineapple's slot 0 reads -0.0597; audit a second fresh graph
    // without Reset and it reads -0.1193; Reset and a fresh audit reads
    // -0.0597 again.
    public void zeroGradients() {
        throw new UnsupportedOperationException("TODO 12: zeroGradients");
    }

    // ---------------------------------------------------------------
    // PROVIDED validators — call these where the TODO comments say to.
    // ---------------------------------------------------------------

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

    public static void requireMatchingShapes(Value[] inputRow,
                                             Value[][] layerWeights, Value[] layerBiases) {
        if (layerWeights.length != layerBiases.length) {
            throw new IllegalArgumentException(
                    layerWeights.length + " weight rows but "
                            + layerBiases.length + " biases — one bias per unit.");
        }
        for (Value[] weightRow : layerWeights) {
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
}
