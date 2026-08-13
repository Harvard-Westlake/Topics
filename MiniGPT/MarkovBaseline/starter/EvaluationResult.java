public record EvaluationResult(double totalNll, long predictions) {
    public double averageLoss() {
        return predictions == 0 ? Double.NaN : totalNll / predictions;
    }

    public double perplexity() {
        return Math.exp(averageLoss());
    }

    public double bitsPerByte(long originalByteCount) {
        if (originalByteCount <= 0) {
            return Double.NaN;
        }
        return totalNll / (Math.log(2.0) * originalByteCount);
    }
}