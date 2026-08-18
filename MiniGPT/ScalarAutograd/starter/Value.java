import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

// One number that remembers how it was made.
//
// A Value is a receipt: the result of one arithmetic operation, plus which
// earlier Values were its ingredients, plus how sensitive the result is to
// each ingredient — the LOCAL DERIVATIVE, written on the receipt at the
// moment of creation. Chain enough receipts together and you get the
// computation graph of a whole forecast; run backward() on the final loss
// and blame flows to every ingredient, exactly as the lesson page traces.
//
// State rules for this class — who reads, who writes:
//   - every operation (add, multiply, ...)  CREATES one new receipt;
//     it reads its ingredients' numbers and changes nothing that exists
//   - backward()       WRITES gradient on every receipt in the graph
//                      (always with +=, never = — blame accumulates)
//   - zeroGradient()   WRITES gradient back to 0.0 (the Reset beat)
//   - setNumber()      WRITES number — leaves only (the Nudge beat)
//   - everything else only READS
public class Value {

    // The forward result. Written once at creation; after that, only
    // setNumber may move it — and only on a leaf, during the Nudge.
    private double number;

    // The accumulated blame: how much the audited loss would change per
    // tiny change in this number. Written only by backward (+=) and
    // zeroGradient (=0).
    private double gradient = 0.0;

    // The ingredients this receipt was computed from. A leaf (a parameter
    // or a plain input) has no ingredients: an empty array.
    private final Value[] parents;

    // One local derivative per ingredient, recorded at creation: how
    // sensitive this receipt's number is to that ingredient's number.
    private final double[] localDerivatives;

    // A short name for printing and debugging — never used in arithmetic.
    private final String label;

    // PROVIDED — a leaf: an original number with no ingredients.
    // Parameters and plain inputs enter the graph through this door.
    public Value(double number, String label) {
        this.number = number;
        this.label = label;
        this.parents = new Value[0];
        this.localDerivatives = new double[0];
    }

    // PROVIDED — an unlabeled leaf.
    public Value(double number) {
        this(number, "");
    }

    // PROVIDED — the receipt constructor every operation uses: the computed
    // result, a name, the ingredients, and one sensitivity per ingredient.
    // Private on purpose: only operations may mint non-leaf receipts.
    private Value(double number, String label, Value[] parents, double[] localDerivatives) {
        this.number = number;
        this.label = label;
        this.parents = parents;
        this.localDerivatives = localDerivatives;
    }

    // PROVIDED — accessors. Reading is never writing.

    public double number() {
        return number;
    }

    public double gradient() {
        return gradient;
    }

    public String label() {
        return label;
    }

    public boolean isLeaf() {
        return parents.length == 0;
    }

    // PROVIDED — a copy of the ingredient list, for tests and printing.
    public List<Value> parentValues() {
        List<Value> copy = new ArrayList<>();
        for (Value parent : parents) {
            copy.add(parent);
        }
        return copy;
    }

    // PROVIDED — the Nudge writer: overwrite a leaf's number. Refuses to
    // move a computed receipt — its number came from its ingredients, and
    // rewriting it would make the receipt a lie.
    public void setNumber(double newNumber) {
        if (parents.length > 0) {
            throw new IllegalStateException(
                    "Only a leaf may be moved — this receipt was computed from "
                            + parents.length + " ingredient(s).");
        }
        this.number = newNumber;
    }

    // PROVIDED — the Reset writer: wipe this receipt's accumulated blame.
    public void zeroGradient() {
        this.gradient = 0.0;
    }

    // ---------------------------------------------------------------
    // The operations. Each one CREATES a new receipt and writes the
    // local derivatives on it at creation time. `add` is provided as
    // the worked example — read it closely before writing the rest.
    // ---------------------------------------------------------------

    // PROVIDED — the worked example operation: addition.
    //
    // result = this.number + other.number. Wiggle either ingredient by a
    // tiny amount and the sum moves by exactly that amount — so the
    // sensitivity to EACH ingredient is 1.0. Two ingredients, two local
    // derivatives, recorded in the same order as the parents array.
    public Value add(Value other) {
        return new Value(this.number + other.number, "+",
                new Value[] {this, other}, new double[] {1.0, 1.0});
    }

    // TODO 1: multiply — the receipt where sensitivities cross over.
    //
    // The question: c = a * b. Wiggle a by a tiny amount — how much does
    // c move?
    // The answer: by b times that amount. If b is 3, every wiggle of a is
    // tripled on its way into c. So the sensitivity to each ingredient is
    // the OTHER ingredient's number: local derivative b for a, and a for
    // b. That crossover is the whole multiplication rule.
    //
    // State: READS both numbers; CREATES one new receipt; alters nothing.
    //
    // Dimensions:
    // - this, other: the two ingredients.
    // - returns:     one NEW receipt —
    //                number            this.number * other.number
    //                parents           {this, other}
    //                localDerivatives  {other.number, this.number}
    //
    // Example from the lesson's first trace (a = 2, b = 3):
    //   a.multiply(b) has number 6, and records sensitivity 3 for a
    //   and 2 for b — each ingredient's wiggle scaled by the other.
    public Value multiply(Value other) {
        throw new UnsupportedOperationException("TODO 1: multiply");
    }

    // TODO 2: subtract — addition's twin, with one sign flipped.
    //
    // The question: d = a - b. Wiggle a and d follows; wiggle b and d
    // moves the OPPOSITE way. How does the receipt record that?
    // The answer: sensitivity 1.0 for the first ingredient, -1.0 for the
    // second. The minus sign is the entire difference from add — blame
    // flowing through a subtraction's second door comes out negated.
    //
    // State: READS both numbers; CREATES one new receipt; alters nothing.
    //
    // Dimensions:
    // - this, other: the two ingredients, in this order — this minus other.
    // - returns:     one NEW receipt —
    //                number            this.number - other.number
    //                parents           {this, other}
    //                localDerivatives  {1.0, -1.0}
    //
    // Example: the loss on Day 2 computes score minus maxShift; the
    // score's door carries sensitivity 1.0, the shift's carries -1.0.
    public Value subtract(Value other) {
        throw new UnsupportedOperationException("TODO 2: subtract");
    }

    // TODO 3: rectify — Chapter 5's gate, now with a blame policy.
    //
    // The question: the gate shows max(0, number). When blame later
    // arrives at the gate's output, how much passes through to the
    // ingredient?
    // The answer: all of it, or none of it. An awake gate (positive
    // input) passes its input unchanged, so its sensitivity is 1.0 — a
    // wiggle walks straight through. A silenced gate (negative input)
    // outputs 0.0 no matter how the input wiggles, so its sensitivity is
    // 0.0 — blame arriving here is marked return-to-sender. At exactly
    // zero this course's gate stays closed: sensitivity 0.0, matching
    // Chapter 5's convention that a weighted sum of exactly zero shows
    // zero.
    //
    // State: READS this.number; CREATES one new receipt; alters nothing.
    //
    // Dimensions:
    // - returns: one NEW receipt —
    //            number            Math.max(0.0, this.number)
    //            parents           {this}
    //            localDerivatives  {1.0 if this.number > 0.0, else 0.0}
    //
    // Examples from the practice graph: z = 1 gates to 1 with
    // sensitivity 1 (awake); the silenced variant's z = -1 gates to 0
    // with sensitivity 0 — and every gradient behind it dies at 0.
    public Value rectify() {
        throw new UnsupportedOperationException("TODO 3: rectify");
    }

    // TODO 4: exponential — the receipt whose result IS its sensitivity.
    //
    // The question: r = e^x. How sensitive is r to x?
    // The answer: exactly r. The exponential function is its own rate of
    // change — the one fact from calculus this chapter asks you to take
    // as given (the wiggle referee will verify it numerically). So
    // compute the result once, then write that same number down as the
    // local derivative.
    //
    // State: READS this.number; CREATES one new receipt; alters nothing.
    //
    // Dimensions:
    // - returns: one NEW receipt —
    //            number            Math.exp(this.number)
    //            parents           {this}
    //            localDerivatives  {the result you just computed}
    //
    // Examples: e^0 = 1 with sensitivity 1; e^1 = 2.71828... with
    // sensitivity 2.71828... — the receipt's own number, both times.
    public Value exponential() {
        throw new UnsupportedOperationException("TODO 4: exponential");
    }

    // TODO 5: naturalLog — the exponential's undo, sensitivity inverted.
    //
    // The question: r = ln(x). How sensitive is r to x?
    // The answer: 1 / x. The natural logarithm grows quickly near zero
    // and barely at all for large x — sensitivity 1/x says exactly that
    // (take it as given; the referee checks it too). The logarithm of
    // zero or a negative number is not a number at all, so this
    // operation must refuse such an ingredient loudly.
    //
    // State: READS this.number; CREATES one new receipt; alters nothing.
    //
    // Dimensions:
    // - returns: one NEW receipt —
    //            number            Math.log(this.number)
    //            parents           {this}
    //            localDerivatives  {1.0 / this.number}
    //
    // Refuse first: if this.number <= 0.0, throw IllegalArgumentException
    // with a message naming the bad number.
    //
    // Example: ln(2) = 0.6931 with sensitivity 1/2 = 0.5. On Day 2 the
    // loss takes the naturalLog of a sum of exponentials — always
    // positive, so the refusal never fires in a correct pipeline.
    public Value naturalLog() {
        throw new UnsupportedOperationException("TODO 5: naturalLog");
    }

    // ---------------------------------------------------------------
    // The audit machinery: order the receipts, then walk them backward.
    // ---------------------------------------------------------------

    // TODO 6: topologicalOrder — every ingredient before its dish.
    //
    // The question: the audit must grade a receipt only after every
    // receipt that USED it has reported. What order guarantees that?
    // The answer: a topological order — a list where every receipt
    // appears after all of its ingredients. Build it depth-first: to
    // place a receipt, first place its ingredients (recursively), then
    // append the receipt itself. A visited set keeps a receipt that
    // feeds two dishes from being listed twice.
    //
    // The recipe:
    //   1. Create an empty list `order` and an empty HashSet `visited`.
    //   2. Write a private recursive helper — appendAfterParents(current,
    //      visited, order) — that returns immediately if current is in
    //      visited; otherwise marks it visited, recurses into each of
    //      current.parents, and only THEN appends current to order.
    //   3. Call the helper on `this` and return the list.
    //
    // A detail worth understanding: Value never overrides equals, so the
    // HashSet compares receipts by identity. That is correct — two
    // receipts that both happen to hold 6.0 are different pieces of
    // paper, and the audit must visit both.
    //
    // State: READS the graph; CREATES a list; alters nothing.
    //
    // Dimensions:
    // - returns: a List containing every receipt reachable from this one
    //            (including this one, which is always last), each exactly
    //            once, every receipt after all of its ingredients.
    //
    // Example from the lesson's first trace — L = (a.multiply(b)).add(a):
    // four receipts; [a, b, product, L] and [b, a, product, L] are both
    // valid orders. The property is what matters, not the tie-breaks.
    public List<Value> topologicalOrder() {
        throw new UnsupportedOperationException("TODO 6: topologicalOrder");
    }

    // TODO 7: backward — the audit itself. Call it on the loss.
    //
    // The question: thousands of receipts, one verdict. How does blame
    // reach every ingredient in one pass?
    // The answer: seed this receipt's gradient with 1.0 (the loss is
    // perfectly sensitive to itself), then walk the topological order in
    // REVERSE — dish before ingredients — and at each receipt hand blame
    // through every door:
    //
    //   parent.gradient  +=  localDerivative for that parent
    //                          * this receipt's gradient
    //
    // That one line is the chain rule (multiply along the path) and
    // gradient accumulation (add across paths) at once. The += is
    // load-bearing: a receipt used by two later receipts receives two
    // deliveries, and they must add. Write = instead of += and the
    // second delivery erases the first — the classic silent bug.
    //
    // The recipe:
    //   1. List<Value> order = topologicalOrder();
    //   2. this.gradient = 1.0;
    //   3. Walk `order` from the last position down to the first; for the
    //      receipt at each position, loop over its parents by index and
    //      apply the += line above using the matching localDerivatives
    //      entry.
    //
    // State: WRITES gradient on every receipt in the graph; every number
    // stays untouched — the audit reads the forward pass, it never redoes
    // it.
    //
    // One audit per graph: backward assumes the graph's gradients start
    // at zero (fresh receipts are born that way). Auditing the same graph
    // twice re-walks receipts whose gradients already hold blame — on the
    // lesson's diamond graph a second backward turns dL/da = 21 into 63,
    // not 42. Build a fresh graph for each audit; parameters, the shared
    // leaves, are cleared between steps by the network's Reset.
    //
    // Machine-verified examples (the Tester checks all of them):
    //   first trace   L = (a*b) + a, a=2, b=3:  dL/da = 4  (3 + 1),
    //                 dL/db = 2, and the product's gradient is 1
    //   practice      L = a*a where a = rectify(w*x + b), w=2, x=3, b=-5:
    //                 dL/dw = 6, dL/dx = 4, dL/db = 2
    //   silenced      same graph with b = -7: every leaf gradient 0.0
    //   diamond       L = (a+b) * (a*b), a=2, b=3: dL/da = 21, dL/db = 16
    public void backward() {
        throw new UnsupportedOperationException("TODO 7: backward");
    }
}
