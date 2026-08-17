import java.util.Arrays;

// PROVIDED — the hand-written stat cards used throughout the chapter.
// Every number here was chosen by a person. Nothing is learned this week.
public class AttentionFixtures {

    // Feature slots for the three-card table, in order:
    //   [0] topping   [1] sweet   [2] savory   [3] laundry
    public static final String[] CARD_FEATURES = {"topping", "sweet", "savory", "laundry"};

    // The three-card table from the lesson:
    //   position 0: PINEAPPLE   (carries SWEET)
    //   position 1: PEPPERONI   (carries SAVORY)
    //   position 2: PINEAPPLE   (the current position, asking)
    public static double[][] threeCards() {
        return new double[][] {
            {1.0, 1.0, 0.0, 0.0},   // PINEAPPLE
            {1.0, 0.0, 1.0, 0.0},   // PEPPERONI
            {1.0, 1.0, 0.0, 0.0},   // PINEAPPLE
        };
    }

    // A card that shares no features with any topping — the complete mismatch.
    public static double[] gymSock() {
        return new double[] {0.0, 0.0, 0.0, 1.0};
    }

    // ---------------------------------------------------------------
    // The retrieval fixture — the pizza-order diagnostic as stat cards.
    //
    //   Order A was topped with pineapple.
    //   Order B was topped with pepperoni.
    //   The topping on Order A was ______.
    //
    // Feature slots:
    //   [0] category  (1 = order name, 2 = topping, 3 = filler)
    //   [1] order identifier (1 = Order A, 2 = Order B, 0 = none)
    //   [2] position, stored as a number
    // ---------------------------------------------------------------
    public static final String[] RETRIEVAL_FEATURES = {"category", "orderId", "position"};

    public static final String[] RETRIEVAL_LABELS = {
        "OrderA", "pineapple", "OrderB", "pepperoni", "filler", "OrderA"
    };

    public static double[][] retrievalSequence() {
        return new double[][] {
            {1.0, 1.0, 0.0},   // position 0: Order A    (the name)
            {2.0, 1.0, 1.0},   // position 1: pineapple  (the topping on Order A)
            {1.0, 2.0, 2.0},   // position 2: Order B
            {2.0, 2.0, 3.0},   // position 3: pepperoni  (the topping on Order B)
            {3.0, 0.0, 4.0},   // position 4: filler
            {1.0, 1.0, 5.0},   // position 5: Order A again — the question
        };
    }

    // ---------------------------------------------------------------
    // Two example rules. Both point values are choices, not truths —
    // Stage 2's entire point is that a person picked them.
    // ---------------------------------------------------------------

    // The Day 1 rule, translated to stat cards: an earlier card whose entire
    // card matches the asker's card earns +4; everything else earns 0.
    public static final ScoreRule MATCH_RULE = (queryCard, keyCard, queryPosition, keyPosition) -> {
        if (keyPosition == queryPosition) {
            return 0.0;   // the asker itself
        }
        return Arrays.equals(queryCard, keyCard) ? 4.0 : 0.0;
    };

    // The lesson's retrieval rule: order identifiers speak loudest, categories
    // help a little, and distance costs a little. Note that scores can go negative.
    public static final ScoreRule ORDER_RULE = (queryCard, keyCard, queryPosition, keyPosition) -> {
        double score = 0.0;
        if (queryCard[1] != 0.0 && queryCard[1] == keyCard[1]) {
            score += 3.0;   // same order identifier
        }
        if (queryCard[0] == keyCard[0]) {
            score += 1.0;   // same category
        }
        score -= 0.1 * (queryPosition - keyPosition);   // distance penalty
        return score;
    };
}
