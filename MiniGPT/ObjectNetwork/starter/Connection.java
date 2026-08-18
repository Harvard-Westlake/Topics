// PROVIDED — one weighted wire into a neuron.
//
// A connection never computes anything. It is a label on a wire: which
// neuron the signal comes from, and how strongly this wire counts. Both
// fields are final — nothing in this chapter ever changes a weight after
// the network is built. The machinery that COULD change them arrives in
// Chapter 6.
public class Connection {

    public final Neuron source;
    public final double weight;

    public Connection(Neuron source, double weight) {
        if (source == null) {
            throw new IllegalArgumentException("A connection needs a source neuron.");
        }
        this.source = source;
        this.weight = weight;
    }
}
