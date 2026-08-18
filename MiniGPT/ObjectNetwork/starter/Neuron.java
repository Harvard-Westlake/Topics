import java.util.ArrayList;
import java.util.List;

// One unit of the network, as an honest Java object.
//
// A neuron holds exactly one number (storedValue) and knows how to
// recompute it from the neurons wired into it. This object form is a
// bridge, not the final machinery: on Day 1 you trace signals through
// objects you can point at; by the end of Day 1 you will show that the
// same arithmetic is one loop over arrays (FeatureNetwork.weighAndAdd).
//
// State rules for this class — who reads, who writes:
//   - setValue        OVERWRITES storedValue (used only on input neurons)
//   - recomputeValue  OVERWRITES storedValue (the only other writer)
//   - everything else only READS
// The bias and the connection weights are never changed by any method.
public class Neuron {

    private final String name;
    private final double bias;
    private final boolean rectifies;
    private final List<Connection> incoming = new ArrayList<>();
    private double storedValue = 0.0;

    private Neuron(String name, double bias, boolean rectifies) {
        this.name = name;
        this.bias = bias;
        this.rectifies = rectifies;
    }

    // PROVIDED factories — the three kinds of unit this chapter uses.

    // An input neuron: no wires in, no bias, no gate. Its value is set
    // from outside with setValue.
    public static Neuron input(String name) {
        return new Neuron(name, 0.0, false);
    }

    // A linear unit: weighted sum plus bias, shown unchanged.
    public static Neuron linear(String name, double bias) {
        return new Neuron(name, bias, false);
    }

    // A rectified unit: weighted sum plus bias, then the ReLU gate —
    // negative results are silenced to zero.
    public static Neuron rectified(String name, double bias) {
        return new Neuron(name, bias, true);
    }

    // PROVIDED — wire another neuron into this one with a fixed weight.
    public void connectFrom(Neuron source, double weight) {
        incoming.add(new Connection(source, weight));
    }

    // PROVIDED — OVERWRITES storedValue. Used to load input neurons.
    public void setValue(double value) {
        this.storedValue = value;
    }

    // PROVIDED — READS storedValue. Never triggers any computation.
    public double value() {
        return storedValue;
    }

    public String name() {
        return name;
    }

    // TODO 1: weigh and add — one neuron reads its inputs.
    //
    // The question: several wires arrive at this neuron, each carrying a
    // number and each with its own strength. How do all of them boil down
    // to one number?
    // The answer: multiply each arriving value by its wire's weight, add
    // up the products, then add this neuron's own bias. That total is the
    // weighted sum. A heavy weight makes a wire loud; a zero weight makes
    // it invisible; a negative weight makes its source count against the
    // total.
    //
    // State: READS this.bias and, through every incoming connection, the
    // source neuron's stored value. Writes NOTHING — not even this
    // neuron's own storedValue. Calling this twice in a row must return
    // the same number and change nothing.
    //
    // Dimensions:
    // - incoming: this neuron's list of connections; each connection
    //             holds one source neuron and one weight.
    // - returns:  one double —
    //             bias + sum over every connection of
    //                    (connection.source.value() * connection.weight)
    //
    // Example from the lesson (the practice network's top hidden unit):
    //   bias 1.0, wire weight  1.0 from inputLeft  (holding 1.0),
    //             wire weight -2.0 from inputRight (holding 2.0)
    //   weighted sum = 1.0 + (1.0 * 1.0) + (-2.0 * 2.0) = -2.0
    public double weighAndAddInputs() {
        throw new UnsupportedOperationException("TODO 1: weighAndAddInputs");
    }

    // TODO 2: recompute — the only computing method that changes a neuron.
    //
    // The question: the weighted sum can be any number, including a
    // negative one. What does this neuron finally show the next layer —
    // and at what moment does its stored value actually change?
    // The answer: pass the weighted sum through the neuron's gate. A
    // rectified unit shows max(0, weightedSum) — a negative total is
    // silenced to zero, which is what lets layers bend instead of
    // collapsing into one straight weighted sum. A linear unit shows the
    // total unchanged. Then, and only then, OVERWRITE storedValue with
    // the result.
    //
    // State: READS the weighted sum (call weighAndAddInputs());
    // OVERWRITES this.storedValue with the gated result; returns it.
    // Call this on a layer only after every neuron it reads from is
    // up to date — inputs first, then hidden, then output.
    //
    // Dimensions:
    // - returns: one double — the gated weighted sum, which is also the
    //            new storedValue.
    //
    // Examples from the lesson (the practice network, inputs 1.0 and 2.0):
    //   top hidden unit:    weighted sum -2.0, rectified -> stores 0.0
    //   bottom hidden unit: weighted sum  4.0, rectified -> stores 4.0
    public double recomputeValue() {
        throw new UnsupportedOperationException("TODO 2: recomputeValue");
    }
}
