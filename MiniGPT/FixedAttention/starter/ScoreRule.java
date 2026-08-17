// PROVIDED — the contract every hand-written relevance rule follows.
//
// A "card" here is one stat card from the lesson: a feature vector holding
// one double per slot. queryCard belongs to the current (asking) position;
// keyCard to a permitted earlier position being scored. The positions are
// supplied as well so a rule can also use order and distance. A score may
// be any real number — softmax handles the rest.
public interface ScoreRule {
    double score(double[] queryCard, double[] keyCard,
                 int queryPosition, int keyPosition);
}
