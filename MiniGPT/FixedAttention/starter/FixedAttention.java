// Every method here builds or serves ONE object: the attention matrix —
// (positions x positions), where row `queryPosition` holds the mixing
// weights that position uses. You will fill that same matrix THREE ways:
//
//   Filling 1 (TODO 1) — equal scores:       nobody chooses; every
//                                            permitted card speaks equally.
//   Filling 2 (TODO 5) — hand-rule scores:   you choose, via a ScoreRule.
//   Filling 3 (TODO 6) — dot-product scores: the numbers choose.
//
// The fillings REPLACE each other's scorers — they never stack. The rest of
// the pipeline (mask, softmax, blend) is shared machinery that never changes.
public class FixedAttention {

    // TODO 1: FILLING 1 of 3 — equal scores (Stage 1: uniform causal weights).
    //
    // The question: before a spotlight can choose what matters, information
    // has to travel forward at all. What is the fairest, simplest way to
    // listen to everything you have already seen — and why must the future
    // stay silent?
    // The answer: split your attention evenly. Standing at a card, you and
    // the earlier cards are the only ones you may hear, so each gets an
    // equal share. The future gets exactly 0 — not a small share, none —
    // because a reader moving left to right has not seen those cards yet.
    //
    // Builds the "remember everything equally" matrix: each position mixes
    // itself and every earlier position at equal volume.
    //
    // Dimensions:
    // - positions: an int, the number of cards on the table.
    // - returns:   (positions x positions) matrix of attention weights.
    //
    // Row queryPosition (the asking card) holds 1.0 / (queryPosition + 1)
    // in every column keyPosition <= queryPosition, and EXACTLY 0.0 in
    // every later column — the causal mask. Every row sums to 1.
    //
    // Example from the lesson (positions = 3):
    // [ 1.000,  0.000,  0.000 ]   (queryPosition 0: itself only)
    // [ 0.500,  0.500,  0.000 ]   (queryPosition 1: half each)
    // [ 0.333,  0.333,  0.333 ]   (queryPosition 2: a third each)
    //
    // Call requirePositions(positions) first.
    public static double[][] uniformCausalWeights(int positions) {
        throw new UnsupportedOperationException("TODO 1: uniform causal weights");
    }

    // TODO 2: stable softmax — scores in, mixing weights out.
    // SHARED MACHINERY: every filling sends its scores through this exact
    // method. Build it once, trust it everywhere.
    //
    // The question: scores can be any numbers at all — 4, 0, even negative.
    // How do you turn any pile of scores into fair shares that always add
    // up to 100%, without the math blowing up on big numbers?
    // The answer: exponentiate every score — now everything is positive,
    // and bigger scores earn disproportionately bigger shares — then divide
    // each by the total, so the shares sum to 1. Subtracting the max first
    // changes no share at all, but keeps Math.exp from overflowing.
    //
    // Dimensions:
    // - scores:  length-n vector; any real numbers.
    // - returns: NEW length-n vector — the input must not be mutated.
    //            Every entry positive (never exactly zero), summing to ~1.
    //
    // Three steps, always in this order:
    //   1. find the maximum score and subtract it from every score,
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
    // SHARED MACHINERY: works identically on a matrix from ANY filling —
    // it neither knows nor cares where the weights came from.
    //
    // The question: you have decided how loudly each card gets to speak.
    // What does the final mix sound like when every card contributes
    // exactly its share?
    // The answer: a weighted average, slot by slot. Each output slot is
    // every card's value in that slot, scaled by that card's volume, added
    // up. Cards with weight 0.0 — the future — are multiplied away to
    // nothing, so the mix can only contain the past.
    //
    // Computes the matrix multiplication: Outputs = AttentionWeights * Values.
    //
    // Dimensions:
    // - attentionWeights: (positions x positions) matrix from any filling.
    // - values:           (positions x slots) matrix — what each stat card
    //                     carries, one card per row.
    // - returns:          (positions x slots) matrix — the blended context.
    //
    // For every asking card queryPosition and every numerical slot, the new
    // value is a weighted sum of that slot across all cards keyPosition,
    // scaled by how much queryPosition attends to keyPosition:
    //
    //   outputs[queryPosition][slot] =
    //       sum over keyPosition of
    //           attentionWeights[queryPosition][keyPosition]
    //               * values[keyPosition][slot]
    //
    // Example from the lesson (Filling 3 weights on the three-card table;
    // slots: topping, sweet, savory, laundry):
    //
    // attentionWeights (3x3):               values (3x4):
    // [ 1.000, 0.000, 0.000 ] (pos 0)       [ 1.0, 1.0, 0.0, 0.0 ] (pos 0: PINEAPPLE)
    // [ 0.378, 0.622, 0.000 ] (pos 1)   X   [ 1.0, 0.0, 1.0, 0.0 ] (pos 1: PEPPERONI)
    // [ 0.384, 0.233, 0.384 ] (pos 2)       [ 1.0, 1.0, 0.0, 0.0 ] (pos 2: PINEAPPLE)
    //
    // outputs (3x4) — row 2 worked out:
    //   y2 = 0.384*[1,1,0,0] + 0.233*[1,0,1,0] + 0.384*[1,1,0,0]
    //      = [ 1.000, 0.767, 0.233, 0.000 ]
    public static double[][] applyWeights(double[][] attentionWeights, double[][] values) {
        throw new UnsupportedOperationException("TODO 3: apply weights");
    }

    // TODO 4: dot product — the matching loop from the lesson.
    // This is Filling 3's scorer, met on its own first: one query card
    // against one key card, no matrix in sight.
    //
    // The question: a computer cannot ask whether two words match. How can
    // multiply-and-add, slot by slot, make "these two are alike" fall out
    // of plain numbers?
    // The answer: a product only survives when BOTH sides have something
    // there — 1.0 * 1.0 adds to the total, 1.0 * 0.0 adds nothing. Walk
    // the slots, multiply the pairs, add them up: the total counts what
    // the two cards share, and sharing is what "alike" means.
    //
    // Dimensions:
    // - queryCard: the asking position's stat card (one double per slot).
    // - keyCard:   the stat card of an earlier card being considered.
    // - returns:   one double — the match score.
    //
    //   total = sum over each slot of queryCard[slot] * keyCard[slot]
    //
    // A slot only adds to the score when BOTH cards have something in it;
    // a negative entry subtracts.
    //
    // Examples from the lesson (slots: topping, sweet, savory, laundry):
    //   PINEAPPLE . PINEAPPLE   [1,1,0,0].[1,1,0,0] = 2.0   (perfect match)
    //   PINEAPPLE . PEPPERONI   [1,1,0,0].[1,0,1,0] = 1.0   (topping only)
    //   PINEAPPLE . GYM SOCK    [1,1,0,0].[0,0,0,1] = 0.0   (nothing shared)
    //
    // Call requireSameLength(queryCard, keyCard) first.
    public static double dotProduct(double[] queryCard, double[] keyCard) {
        throw new UnsupportedOperationException("TODO 4: dot product");
    }

    // TODO 5: FILLING 2 of 3 — hand-rule scores (Stage 2: rule-based causal
    // attention). Same matrix as Filling 1; the equal scores are replaced
    // by scores from a rule a person wrote.
    //
    // The question: you wrote a rule for what deserves attention — plus
    // this, minus that. Can the machine apply your judgment consistently,
    // at every position, all at once?
    // The answer: yes, and that is all this method is. At each position,
    // ask your rule to score every card that position is allowed to see,
    // then let softmax turn those opinions into shares. The machine adds
    // nothing of its own — it just runs your judgment on every row,
    // without getting tired or inconsistent.
    //
    // Dimensions:
    // - statCards: (positions x slots) matrix — one stat card per position.
    // - rule:      the ScoreRule consulted for every (query, key) pair.
    // - returns:   (positions x positions) attention matrix.
    //
    // For each row queryPosition (the asking position):
    //   1. score the permitted positions keyPosition = 0..queryPosition with
    //      rule.score(statCards[queryPosition], statCards[keyPosition],
    //                 queryPosition, keyPosition)
    //      — that is queryPosition + 1 scores, and ONLY those: the mask
    //      removes the future before softmax ever runs,
    //   2. softmax those permitted scores (TODO 2),
    //   3. copy the results into columns 0..queryPosition; every later
    //      column keeps the EXACT 0.0 it was born with.
    //
    // Example from the lesson: MATCH_RULE on the three-card table, row 2.
    //   permitted scores:  [4.0, 0.0, 0.0]  (+4 earlier face match, self 0)
    //   softmax:           [0.9647, 0.0177, 0.0177]
    // so row 2 of the returned matrix is [0.9647, 0.0177, 0.0177].
    //
    // Call requireSequence(statCards) first.
    public static double[][] ruleBasedCausalWeights(double[][] statCards, ScoreRule rule) {
        throw new UnsupportedOperationException("TODO 5: rule-based causal weights");
    }

    // TODO 6: FILLING 3 of 3 — dot-product scores (Stage 3: fixed scaled
    // dot-product causal self-attention).
    //
    // This is TODO 5's skeleton with ONE line changed: the scorer. The
    // hand-written rule is replaced by arithmetic on the cards. Do NOT use
    // TODO 1's uniform matrix anywhere here — fillings replace each other's
    // scorers, they never stack.
    //
    // The question: can the whole spotlight run with no rules about words
    // anywhere — nothing but arithmetic on the cards — and still find the
    // right card?
    // The answer: yes. Score each permitted pair with TODO 4's dot product
    // and "what matters" emerges from the numbers alone. Divide every score
    // by the square root of the card length so longer cards do not shout
    // louder just by having more slots. Then the same mask-and-softmax as
    // TODO 5. No line of it mentions a word — which is exactly what makes
    // it learnable later.
    //
    // Dimensions:
    // - statCards: (positions x slotsPerCard) matrix — one stat card per
    //              position. This week query = key = value = the card
    //              itself: one stat card plays every role.
    // - returns:   (positions x positions) attention matrix.
    //
    // Let slotsPerCard = statCards[0].length — the "d" in the lesson's
    // formula. It measures how long the cards are; it NEVER depends on the
    // scores themselves. For each row queryPosition:
    //   1. score the permitted positions keyPosition = 0..queryPosition with
    //      dotProduct(statCards[queryPosition], statCards[keyPosition])
    //          / Math.sqrt(slotsPerCard)
    //   2. softmax those permitted scores,
    //   3. every column after queryPosition keeps its EXACT 0.0.
    //
    // Example from the lesson: the three-card table, row 2
    // (slotsPerCard = 4, so divide by 2):
    //   raw dot products:  [2.0, 1.0, 2.0]
    //   divided by 2:      [1.0, 0.5, 1.0]
    //   softmax:           [0.3837, 0.2327, 0.3837]
    //
    // Full expected matrix for the three-card table:
    //   [ 1.0000, 0.0000, 0.0000 ]
    //   [ 0.3775, 0.6225, 0.0000 ]
    //   [ 0.3837, 0.2327, 0.3837 ]
    //
    // Call requireSequence(statCards) first.
    public static double[][] dotProductCausalWeights(double[][] statCards) {
        throw new UnsupportedOperationException("TODO 6: dot-product causal weights");
    }

    // TODO 7: the labeled ASCII attention matrix.
    // SHARED MACHINERY: prints a matrix from any filling — the printed
    // shape is how you SEE that all three fillings built the same object.
    //
    // The question: attention is invisible while it works. What does it
    // look like on paper — where was each position looking — and which two
    // patterns must always show up in the picture?
    // The answer: a table where each row is one position's pie chart of
    // attention. The two patterns that must always appear: every row sums
    // to 1.000, and everything above the diagonal is exactly 0.000 — the
    // staircase of zeros left by the causal mask. If either pattern is
    // missing, the picture is diagnosing a bug.
    //
    // Dimensions:
    // - attentionWeights: (positions x positions) matrix from any filling.
    // - returns:          ONE String containing the whole table (rows
    //                     separated by newlines), matching this format:
    //
    //                  pos0    pos1    pos2
    // position 0      1.000   0.000   0.000
    // position 1      0.378   0.622   0.000
    // position 2      0.384   0.233   0.384
    //
    // A header line names the columns; then each row prints "position i"
    // followed by every weight in that row to three decimal places.
    // String.format("%.3f", ...) handles the digits; pick column widths
    // that keep the numbers aligned under their headers.
    public static String formatMatrix(double[][] attentionWeights) {
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

    public static void requireSameLength(double[] firstCard, double[] secondCard) {
        requireVector(firstCard);
        requireVector(secondCard);
        if (firstCard.length != secondCard.length) {
            throw new IllegalArgumentException(
                "Stat cards have different slot counts: "
                    + firstCard.length + " vs " + secondCard.length);
        }
    }

    public static void requireSequence(double[][] statCards) {
        if (statCards == null || statCards.length == 0) {
            throw new IllegalArgumentException("Need at least one stat card.");
        }
        int slotsPerCard = -1;
        for (double[] card : statCards) {
            requireVector(card);
            if (slotsPerCard == -1) {
                slotsPerCard = card.length;
            } else if (card.length != slotsPerCard) {
                throw new IllegalArgumentException(
                    "Every stat card must have the same number of slots.");
            }
        }
    }
}
