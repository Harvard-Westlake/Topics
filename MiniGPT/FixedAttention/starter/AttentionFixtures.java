import java.util.Arrays;

// PROVIDED — the hand-written stat cards used throughout the chapter.
// Every number here was chosen by a person. Nothing is learned this week.
public class AttentionFixtures {

    // Feature slots for the three-card table, in order:
    //   [0] rock   [1] dark   [2] pale   [3] animal
    public static final String[] CARD_FEATURES = {"rock", "dark", "pale", "animal"};

    // The three-card table from the lesson:
    //   position 0: BASALT      (carries DARK)
    //   position 1: LIMESTONE   (carries PALE)
    //   position 2: BASALT      (the current position, asking)
    public static double[][] threeCards() {
        return new double[][] {
            {1.0, 1.0, 0.0, 0.0},   // BASALT
            {1.0, 0.0, 1.0, 0.0},   // LIMESTONE
            {1.0, 1.0, 0.0, 0.0},   // BASALT
        };
    }

    // A card that shares no features with any rock — the complete mismatch.
    public static double[] pikachu() {
        return new double[] {0.0, 0.0, 0.0, 1.0};
    }

    // ---------------------------------------------------------------
    // The retrieval fixture — the "Sample A" diagnostic as stat cards.
    //
    //   Sample A was collected beside the basalt flow.
    //   Sample B was collected from a pale limestone layer.
    //   The rock associated with Sample A was ______.
    //
    // Feature slots:
    //   [0] category  (1 = sample name, 2 = rock type, 3 = filler)
    //   [1] sample identifier (1 = Sample A, 2 = Sample B, 0 = none)
    //   [2] position, stored as a number
    // ---------------------------------------------------------------
    public static final String[] RETRIEVAL_FEATURES = {"category", "sampleId", "position"};

    public static final String[] RETRIEVAL_LABELS = {
        "SampleA", "basalt", "SampleB", "limestone", "filler", "SampleA"
    };

    public static double[][] retrievalSequence() {
        return new double[][] {
            {1.0, 1.0, 0.0},   // position 0: Sample A  (the name)
            {2.0, 1.0, 1.0},   // position 1: basalt    (the rock tied to Sample A)
            {1.0, 2.0, 2.0},   // position 2: Sample B
            {2.0, 2.0, 3.0},   // position 3: limestone (the rock tied to Sample B)
            {3.0, 0.0, 4.0},   // position 4: filler
            {1.0, 1.0, 5.0},   // position 5: Sample A again — the question
        };
    }

    // ---------------------------------------------------------------
    // Two example rules. Both point values are choices, not truths —
    // Stage 2's entire point is that a person picked them.
    // ---------------------------------------------------------------

    // The Day 1 rule, translated to stat cards: an earlier card whose entire
    // card matches the asker's card earns +4; everything else earns 0.
    public static final ScoreRule MATCH_RULE = (query, key, queryPos, keyPos) -> {
        if (keyPos == queryPos) {
            return 0.0;   // the asker itself
        }
        return Arrays.equals(query, key) ? 4.0 : 0.0;
    };

    // The lesson's retrieval rule: identifiers speak loudest, categories help
    // a little, and distance costs a little. Note that scores can go negative.
    public static final ScoreRule SAMPLE_RULE = (query, key, queryPos, keyPos) -> {
        double score = 0.0;
        if (query[1] != 0.0 && query[1] == key[1]) {
            score += 3.0;   // same sample identifier
        }
        if (query[0] == key[0]) {
            score += 1.0;   // same category
        }
        score -= 0.1 * (queryPos - keyPos);   // distance penalty
        return score;
    };
}
