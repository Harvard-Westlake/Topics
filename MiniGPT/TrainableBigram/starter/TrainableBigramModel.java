import java.util.Random;

// The first machine in this course that changes its own numbers.
//
// The entire model is one table of logits — logits[currentToken][nextToken].
// A second table of the same shape accumulates gradients between updates.
// Chapter 2's bigram table held counts; Chapter 3's spotlight followed rules
// you wrote. Every number in THIS table is adjusted by the training loop,
// using nothing but the gradient of the model's own loss.
//
// The methods you write follow one flashcard through its life, in the order
// the lesson taught them — and each stage is strict about what it may touch:
//
//   stage      method                  reads                 writes
//   Forecast   probabilities()         one logits row        nothing
//   Grade      loss()                  one logits row        nothing
//   Measure    accumulateGradients()   one logits row        one gradients row
//   Nudge      step()                  the gradient bucket   every logit
//   Reset      zeroGradients()         nothing               wipes the bucket
//   Report     averageLoss()           the logits            nothing
//
// Forecast, Grade, and Report only READ the table. Measure writes only the
// gradient bucket. Nudge is the one method allowed to move a logit. The
// Tester checks these boundaries — a method that touches what it shouldn't
// fails even when its arithmetic is right.
public class TrainableBigramModel {

    private final int vocabularySize;
    private final double[][] logits;
    private final double[][] gradients;
    private int examplesSinceReset = 0;

    // PROVIDED — every logit starts as a small random number near zero.
    // Small matters: near-equal logits make each row's softmax nearly
    // uniform, so a nearly empty table's average loss sits right at ln(V) —
    // Chapter 2's uniform anchor, and the Tester's first training check.
    public TrainableBigramModel(int vocabularySize, long seed) {
        if (vocabularySize <= 0) {
            throw new IllegalArgumentException("Vocabulary size must be positive.");
        }
        this.vocabularySize = vocabularySize;
        this.logits = new double[vocabularySize][vocabularySize];
        this.gradients = new double[vocabularySize][vocabularySize];
        Random random = new Random(seed);
        for (int currentToken = 0; currentToken < vocabularySize; currentToken++) {
            for (int nextToken = 0; nextToken < vocabularySize; nextToken++) {
                logits[currentToken][nextToken] = 0.02 * random.nextGaussian();
            }
        }
    }

    public int vocabularySize() {
        return vocabularySize;
    }

    // TODO 1 — shared machinery: the stable softmax, the same three steps
    // you built in Chapter 3, rebuilt here so this class stands alone.
    // Every stage below that reads the table calls this to do it.
    //
    // The question: the table's numbers are free to be anything. How do you
    // turn one row of free numbers into an honest forecast that adds up to
    // 100% — every time, no matter how wild the numbers get?
    // The answer: exponentiate every entry — now everything is positive,
    // and bigger entries earn disproportionately bigger shares — then
    // divide each by the total, so the shares sum to 1. Subtracting the
    // max first changes no share, but stops Math.exp from overflowing.
    //
    // Dimensions:
    // - row:     length-n vector of logits; any real numbers.
    // - returns: NEW length-n vector — the input must not be mutated.
    //            Every entry positive (never exactly zero), summing to ~1.
    //
    // Three steps, always in this order:
    //   1. find the maximum entry and subtract it from every entry
    //      (prevents Math.exp from overflowing; changes nothing else),
    //   2. exponentiate each shifted entry with Math.exp,
    //   3. divide each result by the sum of all the results.
    //
    // Example from the lesson: the worked row [1.2, 0.1, -0.4]
    //   subtract max (1.2):   [ 0.0,    -1.1,    -1.6  ]
    //   exponentiate:         [ 1.0000,  0.3329,  0.2019]
    //   divide by sum 1.5348: [ 0.6516,  0.2169,  0.1315]
    public static double[] stableSoftmax(double[] row) {
        throw new UnsupportedOperationException("TODO 1: stable softmax");
    }

    // TODO 2 — the Forecast stage: one row of the table, read as a
    // prediction distribution. Reads the table; writes nothing.
    //
    // The question: when you ask the table "what comes next?", which
    // numbers answer — and why must the asking never change them?
    // The answer: one row answers — the row belonging to the current
    // token, softmaxed into a forecast. And reading must never write:
    // training will read this forecast thousands of times mid-flight, and
    // a table that shifts whenever it is looked at can never be measured.
    //
    // Dimensions:
    // - currentToken: an int in [0, vocabularySize) — which row to read.
    // - returns:      NEW length-V vector of next-token probabilities.
    //
    // Return the stable softmax of logits[currentToken]. Reading a
    // prediction must never change the table: no logit moves, and calling
    // this twice returns identical answers.
    //
    // Example from the lesson: if the row for pizza (token 0) holds
    // [1.2, 0.1, -0.4], then probabilities(0) forecasts
    // [0.6516, 0.2169, 0.1315] — 65% pizza, 22% pineapple, 13% pepperoni.
    //
    // Call requireToken(currentToken) first.
    public double[] probabilities(int currentToken) {
        throw new UnsupportedOperationException("TODO 2: probabilities");
    }

    // TODO 3 — the Grade stage: cross-entropy loss for one example —
    // Chapter 2's penalty, charged to a single prediction. Reads only.
    //
    // The question: the order history knows what actually came next. How do you grade
    // one guess with one fair number — gentle on a near-miss, brutal on
    // confident nonsense?
    // The answer: look only at the probability the model gave the truth,
    // and charge -ln of it. Truth at 90% costs 0.105; truth at 1% costs
    // 4.6. The logarithm is what makes the grading fair: every halving of
    // the truth's probability adds the same fixed penalty.
    //
    // Dimensions:
    // - currentToken: the flashcard's front — which row made the forecast.
    // - targetToken:  the flashcard's back — what the history actually showed.
    // - returns:      one double, 0 for certainty in the truth and growing
    //                 as the model is more surprised.
    //
    //   loss = -Math.log( probabilities(currentToken)[targetToken] )
    //
    // Examples from the lesson:
    //   row [1.2, 0.1, -0.4], target pineapple (1): -ln(0.2169) = 1.5284
    //   row [0, 0, 0], any target: -ln(1/3) = 1.0986 — the ln(V) anchor
    //
    // Call requireToken on both tokens first.
    public double loss(int currentToken, int targetToken) {
        throw new UnsupportedOperationException("TODO 3: loss");
    }

    // TODO 4 — the Measure stage: the shortcut gradient, accumulated.
    // Writes ONLY the gradient bucket — never a logit.
    //
    // The question: the grade says how wrong you were. How do you learn
    // which direction each number should move — without ever being handed
    // the right answer?
    // The answer: subtract the answer sheet from the forecast — p minus
    // one-hot. The truth's entry comes out negative (that logit gets
    // pushed up), every other entry comes out positive, sized by its own
    // confidence (pushed down that hard). It is a direction, not an
    // answer: the right answer only ever entered through the grade.
    //
    // Computes "prediction minus one-hot" for one flashcard and pours it
    // into the gradient bucket. This method measures; step moves.
    //
    // Dimensions:
    // - gradients is (V x V), same shape as logits — but this method
    //   touches ONE row of it: gradients[currentToken]. No other row of
    //   the loss depends on this flashcard, and no logit changes here.
    //
    // With p = probabilities(currentToken), for every possible next token
    // (every column of that one row):
    //   gradients[currentToken][nextToken] +=
    //       p[nextToken] - (nextToken == targetToken ? 1.0 : 0.0)
    // then increment examplesSinceReset. The += is the accumulation: a
    // batch calls accumulateGradients many times before one step.
    //
    // Example from the lesson: row [1.2, 0.1, -0.4], target pineapple (1)
    //   p:              [ 0.6516,   0.2169,   0.1315 ]
    //   one-hot target: [ 0,        1,        0      ]
    //   added to row:   [ 0.6516,  -0.7831,   0.1315 ]   (sums to zero)
    //
    // Call requireToken on both tokens first.
    public void accumulateGradients(int currentToken, int targetToken) {
        throw new UnsupportedOperationException("TODO 4: accumulateGradients");
    }

    // TODO 5 — the Nudge stage: the update, one stride of gradient descent.
    // The ONLY method in this class allowed to move a logit.
    //
    // The question: every number has a direction now. How far do you dare
    // move — and why should grading a bigger handful of examples NOT mean
    // taking a bigger leap?
    // The answer: move each logit a small stride against its slope — the
    // learning rate sets the stride. And divide the accumulated slopes by
    // how many examples poured in: a batch is a vote, an averaged opinion,
    // and 24 voters should not shove 24 times harder than one.
    //
    // Averages the accumulated gradients and moves every logit against
    // its slope.
    //
    // For every entry of the table — every currentToken row, every
    // nextToken column:
    //   logits[currentToken][nextToken] -=
    //       learningRate * gradients[currentToken][nextToken]
    //           / examplesSinceReset
    //
    // The division averages the batch: 24 accumulated flashcards summed
    // would be one gradient ~24 times louder, and batch size would secretly
    // scale the stride. Rows that accumulated nothing hold gradient 0.0
    // and therefore do not move. Do not reset anything here — resetting is
    // zeroGradients' job, and the Trainer calls the two separately.
    //
    // Example from the lesson: after one accumulateGradients call on the
    // worked row,
    // step(0.5) moves it
    //   [1.2, 0.1, -0.4]  ->  [0.8742, 0.4916, -0.4658]
    // and the loss falls 1.5284 -> 1.0474.
    //
    // Call requireExamples() first.
    public void step(double learningRate) {
        throw new UnsupportedOperationException("TODO 5: step");
    }

    // TODO 6 — the Reset stage: wipe the bucket between updates.
    //
    // The question: yesterday's directions were measured on a table that
    // no longer exists. Why must the slate be wiped before the next
    // handful?
    // The answer: a slope is a snapshot — it says which way was downhill
    // from where the table STOOD. The moment step moves the table, those
    // readings describe a place it already left. Wipe them, or every
    // future step is steered partly by ghosts. Forgetting this reset is
    // the classic silent training bug.
    //
    // Set every entry of gradients to 0.0 and examplesSinceReset to 0.
    public void zeroGradients() {
        throw new UnsupportedOperationException("TODO 6: zero gradients");
    }

    // TODO 7 — the Report stage: Chapter 2's evaluation, one method.
    // Reads the table; writes nothing.
    //
    // The question: one guess earned one grade. What is the report card
    // for the whole history — and what score must a table that knows nothing
    // always receive?
    // The answer: grade every adjacent pair and average the charges. A
    // know-nothing table forecasts a third for everything and pays
    // -ln(1/3) = 1.0986 on every single card — so a step-0 loss of 1.0987
    // is proof the pipeline works, not a disappointment.
    //
    // Dimensions:
    // - historyToGrade: a history of n tokens — which contains n - 1
    //                   flashcards, one per adjacent pair. Sometimes the
    //                   training history, sometimes the validation history:
    //                   this method grades whichever it is handed, and
    //                   trains on neither.
    // - returns: the mean of
    //            loss(historyToGrade[position], historyToGrade[position + 1])
    //            over position = 0 .. historyToGrade.length - 2.
    //
    // The trap: grading is not training. The only lifecycle stage this
    // method runs is Grade — your own loss(), once per adjacent pair. No
    // Measure, no Nudge: a report card that changes the student mid-exam
    // measures nothing, and nudging during evaluation would train on the
    // validation history — the one thing Chapter 2's boundary rule forbids.
    // (The Tester checks that this method moves no logit and touches no
    // gradient.)
    //
    // Examples from the lesson:
    //   {1, 0, 1} averages exactly two losses: loss(1,0) and loss(0,1).
    //   A nearly empty table (seed 7) on the full training history scores 1.0987 —
    //   ln(3) to three decimals, Chapter 2's uniform anchor.
    //
    // Call requireHistory(historyToGrade) first.
    public double averageLoss(int[] historyToGrade) {
        throw new UnsupportedOperationException("TODO 7: average loss");
    }

    // ---------------------------------------------------------------
    // PROVIDED helpers — used by the Tester; do not modify.
    // ---------------------------------------------------------------

    // Overwrite one row of logits. The Tester uses this to reproduce the
    // lesson's worked traces exactly; your training code never needs it.
    public void setRow(int currentToken, double... row) {
        requireToken(currentToken);
        if (row.length != vocabularySize) {
            throw new IllegalArgumentException(
                "Row needs " + vocabularySize + " entries, got " + row.length);
        }
        logits[currentToken] = row.clone();
    }

    // Defensive copies for tests and printing.
    public double[] logitRow(int currentToken) {
        requireToken(currentToken);
        return logits[currentToken].clone();
    }

    public double[] gradientRow(int currentToken) {
        requireToken(currentToken);
        return gradients[currentToken].clone();
    }

    // PROVIDED validators — call these where the TODO comments say to.

    public void requireToken(int token) {
        if (token < 0 || token >= vocabularySize) {
            throw new IllegalArgumentException(
                "Token " + token + " is outside [0, " + vocabularySize + ").");
        }
    }

    public void requireExamples() {
        if (examplesSinceReset == 0) {
            throw new IllegalStateException(
                "step called with no accumulated examples — call accumulateGradients first.");
        }
    }

    public static void requireHistory(int[] history) {
        if (history == null || history.length < 2) {
            throw new IllegalArgumentException(
                "A token history needs at least two tokens to form one transition.");
        }
    }
}
