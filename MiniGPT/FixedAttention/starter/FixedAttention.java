public class FixedAttention {

    // TODO 1: Stage 1 — uniform causal weights.
    // Builds the "remember everything equally" matrix: each position mixes
    // itself and every earlier position at equal volume.
    //
    // Dimensions:
    // - positions: an int, the number of cards on the table.
    // - returns:   (positions x positions) matrix of attention weights.
    //
    // Row i holds 1.0 / (i + 1) at columns 0..i, and EXACTLY 0.0 at every
    // column after i — the causal mask. Every row sums to 1.
    //
    // Example from the lesson (positions = 3):
    // [ 1.000,  0.000,  0.000 ]   (pos 0: nothing earlier — itself only)
    // [ 0.500,  0.500,  0.000 ]   (pos 1: half pos 0, half itself)
    // [ 0.333,  0.333,  0.333 ]   (pos 2: a third each)
    //
    // Call requirePositions(positions) first.
    public static double[][] uniformCausalWeights(int positions) {
        throw new UnsupportedOperationException("TODO 1: uniform causal weights");
    }

    // TODO 2: stable softmax — scores in, mixing weights out.
    // Converts any list of scores into weights that can run a mixture:
    // every entry positive (never exactly zero), all entries summing to ~1.
    //
    // Dimensions:
    // - scores:  length-n vector; any real numbers.
    // - returns: NEW length-n vector — the input must not be mutated.
    //
    // Three steps, always in this order:
    //   1. find the maximum score and subtract it from every score
    //      (prevents Math.exp from overflowing; changes nothing else),
    //   2. exponentiate each shifted score with Math.exp,
    //   3. divide each result by the sum of all the results.
    //
    // Example from the lesson: scores [2.0, 1.0, 0.0]
    //   subtract max (2.0):   [ 0.0,    -1.0,    -2.0  ]
    //   exponentiate:         [ 1.0000,  0.3679,  0.1353]
    //   divide by sum 1.5032: [ 0.6652,  0.2447,  0.0900]
    //
    // Call requireVector(scores) first.
    public static double[] stableSoftmax(double[] scores) {
        throw new UnsupportedOperationException("TODO 2: stable softmax");
    }

    // TODO 3: blend values with an attention matrix.
    // Computes the matrix multiplication: Outputs = Weights * Values.
    //
    // Dimensions:
    // - weights: (positions x positions) matrix of attention weights.
    // - values:  (positions x slots) matrix of what the stat cards carry.
    // - returns: (positions x slots) matrix — the new blended context.
    //
    // For every card position i and numerical slot s, the new value is a
    // weighted sum of slot s across all cards j, scaled by how much
    // position i attends to position j:
    //   outputs[i][s] = sum over j of weights[i][j] * values[j][s]
    // Future positions carry weight exactly 0.0, so they contribute nothing.
    //
    // Example from the lesson (dot-product weights on the three-card table;
    // slots: topping, sweet, savory, laundry):
    //
    // weights (3x3):                        values (3x4):
    // [ 1.000, 0.000, 0.000 ] (pos 0)       [ 1.0, 1.0, 0.0, 0.0 ] (pos 0: PINEAPPLE)
    // [ 0.378, 0.622, 0.000 ] (pos 1)   X   [ 1.0, 0.0, 1.0, 0.0 ] (pos 1: PEPPERONI)
    // [ 0.384, 0.233, 0.384 ] (pos 2)       [ 1.0, 1.0, 0.0, 0.0 ] (pos 2: PINEAPPLE)
    //
    // outputs (3x4) — row 2 worked out:
    //   y2 = 0.384*[1,1,0,0] + 0.233*[1,0,1,0] + 0.384*[1,1,0,0]
    //      = [ 1.000, 0.767, 0.233, 0.000 ]
    public static double[][] applyWeights(double[][] weights, double[][] values) {
        throw new UnsupportedOperationException("TODO 3: apply weights");
    }

    // TODO 4: dot product — the matching loop from the lesson.
    // Measures how strongly two stat cards match, slot by slot.
    //
    // Dimensions:
    // - left, right: two vectors of the same length d.
    // - returns:     one double — the match score.
    //
    //   total = sum over each slot s of left[s] * right[s]
    //
    // A slot only adds to the score when BOTH cards have something in it
    // (1.0 * 0.0 contributes nothing); a negative entry subtracts.
    //
    // Examples from the lesson (slots: topping, sweet, savory, laundry):
    //   PINEAPPLE . PINEAPPLE   [1,1,0,0].[1,1,0,0] = 2.0   (perfect match)
    //   PINEAPPLE . PEPPERONI   [1,1,0,0].[1,0,1,0] = 1.0   (topping only)
    //   PINEAPPLE . GYM SOCK    [1,1,0,0].[0,0,0,1] = 0.0   (nothing shared)
    //
    // Call requireSameLength(left, right) first.
    public static double dotProduct(double[] left, double[] right) {
        throw new UnsupportedOperationException("TODO 4: dot product");
    }

    // TODO 5: Stage 2 — rule-based causal attention.
    // Builds a full attention matrix whose scores come from a hand-written
    // ScoreRule instead of arithmetic on the cards.
    //
    // Dimensions:
    // - features: (positions x slots) matrix — one stat card per row.
    // - rule:     the ScoreRule consulted for every (query, key) pair.
    // - returns:  (positions x positions) attention matrix.
    //
    // For each row i (the asking position):
    //   1. score the permitted positions j = 0..i with
    //      rule.score(features[i], features[j], i, j)  — that is i+1 scores,
    //   2. softmax those i+1 scores (TODO 2),
    //   3. place the results in columns 0..i; columns after i stay EXACTLY
    //      0.0 — the mask removes the future before softmax ever runs.
    //
    // Example from the lesson: MATCH_RULE on the three-card table, row 2.
    //   scores for j = 0..2:  [4.0, 0.0, 0.0]  (+4 earlier face match, self 0)
    //   softmax:              [0.9647, 0.0177, 0.0177]
    // so row 2 of the returned matrix is [0.9647, 0.0177, 0.0177].
    //
    // Call requireSequence(features) first.
    public static double[][] ruleBasedCausalWeights(double[][] features, ScoreRule rule) {
        throw new UnsupportedOperationException("TODO 5: rule-based causal weights");
    }

    // TODO 6: Stage 3 — fixed scaled dot-product causal self-attention.
    // The complete pipeline — score, mask, softmax — with the scores now
    // computed from the cards themselves. This week query = key = input:
    // each card's one stat card plays every role.
    //
    // Dimensions:
    // - sequence: (positions x d) matrix — one stat card per row, where d
    //             is the number of slots per card.
    // - returns:  (positions x positions) attention matrix.
    //
    // For each row i (the asking position):
    //   1. score the permitted positions j = 0..i with
    //      dotProduct(sequence[i], sequence[j]) / Math.sqrt(d),
    //   2. softmax those i+1 scores,
    //   3. columns after i stay EXACTLY 0.0, exactly as in TODO 5.
    //
    // Example from the lesson: the three-card table, row 2 (d = 4, sqrt(d) = 2):
    //   raw dot products:  [2.0, 1.0, 2.0]
    //   scaled by sqrt(d): [1.0, 0.5, 1.0]
    //   softmax:           [0.3837, 0.2327, 0.3837]
    //
    // Full expected matrix for the three-card table:
    //   [ 1.0000, 0.0000, 0.0000 ]
    //   [ 0.3775, 0.6225, 0.0000 ]
    //   [ 0.3837, 0.2327, 0.3837 ]
    //
    // Call requireSequence(sequence) first.
    public static double[][] dotProductCausalWeights(double[][] sequence) {
        throw new UnsupportedOperationException("TODO 6: dot-product causal weights");
    }

    // TODO 7: the labeled ASCII attention matrix.
    // Turns a weights matrix into the lesson's printed table.
    //
    // Dimensions:
    // - weights: (positions x positions) attention matrix.
    // - returns: ONE String containing the whole table (rows separated by
    //            newlines), matching the lesson's format:
    //
    //                  pos0    pos1    pos2
    // position 0      1.000   0.000   0.000
    // position 1      0.378   0.622   0.000
    // position 2      0.384   0.233   0.384
    //
    // A header line names the columns; then row i prints "position i"
    // followed by every weight in that row to three decimal places.
    // String.format("%.3f", ...) handles the digits; pick column widths
    // that keep the numbers aligned under their headers.
    public static String formatMatrix(double[][] weights) {
        throw new UnsupportedOperationException("TODO 7: attention matrix visualization");
    }

    // ---------------------------------------------------------------
    // PROVIDED validators — call these at the top of your methods.
    // ---------------------------------------------------------------

    public static void requirePositions(int positions) {
        if (positions <= 0) {
            throw new IllegalArgumentException("Need at least one position.");
        }
    }

    public static void requireVector(double[] vector) {
        if (vector == null || vector.length == 0) {
            throw new IllegalArgumentException("Vector must contain at least one entry.");
        }
    }

    public static void requireSameLength(double[] left, double[] right) {
        requireVector(left);
        requireVector(right);
        if (left.length != right.length) {
            throw new IllegalArgumentException(
                "Vector lengths differ: " + left.length + " vs " + right.length);
        }
    }

    public static void requireSequence(double[][] sequence) {
        if (sequence == null || sequence.length == 0) {
            throw new IllegalArgumentException("Sequence must contain at least one position.");
        }
        int dimension = -1;
        for (double[] row : sequence) {
            requireVector(row);
            if (dimension == -1) {
                dimension = row.length;
            } else if (row.length != dimension) {
                throw new IllegalArgumentException("Every position must have the same dimension.");
            }
        }
    }
}
