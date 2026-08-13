// PROVIDED — the contract every hand-written relevance rule follows.
// queryFeatures belongs to the current (asking) position; keyFeatures to a
// permitted position being scored. The positions are supplied so rules can
// use distance. A score may be any real number — softmax handles the rest.
public interface ScoreRule {
    double score(double[] queryFeatures, double[] keyFeatures,
                 int queryPosition, int keyPosition);
}
