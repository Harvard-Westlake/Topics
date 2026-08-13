import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A Byte Pair Encoding (BPE) tokenizer trainer.
 *
 * The pipeline is:   files  ->  bytes  ->  integer tokens  ->  merged tokens
 *
 * Every training document starts as a list of integers 0-255 (one per byte).
 * Training repeatedly finds the most frequent ADJACENT PAIR of tokens and
 * replaces it everywhere with a brand-new token id (256, then 257, ...).
 * Each replacement makes the documents shorter and the vocabulary larger.
 *
 * Tiny end-to-end example — a file containing the 7 characters "abab ab"
 * ('a'=97, 'b'=98, space=32) loads as:
 *
 *     [97, 98, 97, 98, 32, 97, 98]
 *
 * The pair (97, 98) appears 3 times, so merge #1 creates token 256 and the
 * document becomes:
 *
 *     [256, 256, 32, 256]        (7 tokens -> 4 tokens)
 *
 * After that no pair appears twice, so training stops.
 */
public class Tokenizer {

    // One inner list per file added. Documents are NEVER concatenated:
    // the last byte of one file and the first byte of the next were never
    // actually adjacent, so they must never be counted as a pair.
    private final List<List<Integer>> documents = new ArrayList<>();

    // The ordered log of every merge performed, oldest first. This list —
    // not the transformed documents — is the durable product of training:
    // it is what encode/decode will need later. See MergeRule below.
    private final List<MergeRule> mergeRules = new ArrayList<>();

    // The id the NEXT merge will claim. Ids 0-255 are taken by the raw
    // bytes, so the first merged token is 256, the second 257, and so on.
    private int nextTokenId = 256;

    /**
     * Two adjacent tokens, used as a HashMap key while counting.
     * Example: in [97, 98, 97], the adjacent pairs are
     * new Pair(97, 98) and new Pair(98, 97).
     *
     * Java records get equals() and hashCode() for free, which is exactly
     * what makes this usable as a HashMap key: two Pair objects with the
     * same left and right values count as the same key.
     */
    public record Pair(int left, int right) {}

    /**
     * One learned merge: the pair (left, right) became the new token `result`.
     *
     * Example: training on "abab ab" performs one merge, recorded as
     *
     *     new MergeRule(97, 98, 256)     // 'a','b'  ->  token 256
     *
     * If a later merge combined 256 with 32 (space), it would be recorded as
     *
     *     new MergeRule(256, 32, 257)
     *
     * Notice that rule #2 only makes sense AFTER rule #1 has run — token 256
     * does not exist until rule #1 creates it. That is why the rules are kept
     * in learned order: encoding new text must replay them in EXACTLY this
     * order, and decoding expands them in reverse.
     */
    public record MergeRule(int left, int right, int result) {}

    /**
     * PROVIDED — loads the corpus. Each file becomes one document.
     *
     * Two things are handled for you here:
     *   1. Files.readAllBytes reads the whole file in one call — no streams.
     *   2. Java's byte type is SIGNED (-128..127), so a byte like 0xE9
     *      (part of the UTF-8 encoding of 'é') would show up as -23.
     *      Byte.toUnsignedInt converts every byte to its true 0-255 value.
     *
     * Tokens are stored as int (not byte) because merged tokens (256+)
     * do not fit in a byte.
     */
    public void addFiles(Path... files) throws IOException {
        for (Path file : files) {
            byte[] bytes = Files.readAllBytes(file);
            List<Integer> tokens = new ArrayList<>(bytes.length);

            for (byte b : bytes) {
                tokens.add(Byte.toUnsignedInt(b));
            }

            documents.add(tokens);
        }
    }

    /**
     * PART 1 (you implement):
     * Count every adjacent pair across all documents combined.
     *
     * Example — for a single document [97, 98, 97, 98] the result must be:
     *
     *     (97, 98) -> 2      (positions 0-1 and 2-3)
     *     (98, 97) -> 1      (positions 1-2)
     *
     * Counting is per-position: in [97, 97, 97] the pair (97, 97) counts
     * TWICE (positions 0-1 and 1-2), even though a later merge could only
     * replace one of those occurrences.
     *
     * Pairs never span documents: the last token of one document and the
     * first token of the next are NOT a pair.
     */
    private Map<Pair, Integer> countPairs() {
        // TODO
        return null;
    }

    /**
     * PART 2 (you implement):
     * Perform ONE merge. Returns true if a merge happened, false if not.
     *
     *   1. Count all pairs using Part 1.
     *   2. Pick the winner DETERMINISTICALLY. HashMap iteration order is
     *      unspecified, so "whichever came first" is not deterministic:
     *        - prefer the larger count;
     *        - if counts tie, prefer the smaller left token id;
     *        - if those also tie, prefer the smaller right token id.
     *   3. If no pair occurs at least TWICE, return false (nothing worth
     *      merging — this is what makes train() stop early).
     *   4. Claim the new token id with nextTokenId++.
     *   5. Record the merge: append a MergeRule to mergeRules.
     *   6. In EVERY document, replace each non-overlapping occurrence,
     *      scanning left to right.
     *   7. Return true.
     *
     * Example — if (97, 98) is the winner in [97, 98, 97, 98, 99], the
     * document becomes [256, 256, 99].
     *
     * Overlap example — merging (97, 97) in [97, 97, 97] produces
     * [256, 97], NOT [256, 256]: once the first two tokens are consumed,
     * the middle 97 is gone.
     *
     * Java pitfall: the lists hold Integer objects. Comparing a list element
     * to an int (like the winner's left value) unboxes correctly, but
     * comparing two list elements with == compares references — it happens
     * to work below 128 and silently fails above. Use int values or .equals.
     */
    private boolean mergeMostFrequentPair() {
        // TODO
        return false;
    }

    /**
     * PROVIDED — the training loop. Asks for up to `merges` merges but stops
     * early the moment mergeMostFrequentPair() reports there is nothing left
     * worth merging. So train(256) performs AT MOST 256 merges — possibly
     * fewer on a small corpus.
     */
    public void train(int merges) {
        for (int i = 0; i < merges; i++) {
            if (!mergeMostFrequentPair()) {
                break;
            }
        }
    }

    /**
     * PROVIDED — the ACTUAL vocabulary size: 256 byte tokens plus the merges
     * actually performed.
     *
     * Example: train(256) on a small corpus might stop after 240 merges,
     * leaving vocabularySize() == 496, not 512. Downstream code (like the
     * Chapter 2 models) must call this instead of assuming a number.
     */
    public int vocabularySize() {
        return nextTokenId;
    }

    /** PROVIDED — the documents in their current (post-merge) state. */
    public List<List<Integer>> getDocuments() {
        return documents;
    }

    /** PROVIDED — the ordered merge log, oldest rule first. */
    public List<MergeRule> getMergeRules() {
        return mergeRules;
    }

    /**
     * TODO (needed once experiments must avoid tokenizer leakage):
     * Tokenize NEW text the trainer never saw — a validation set, a test
     * set, or a user's prompt.
     *
     * Contract: convert the text to UTF-8 bytes, then apply every MergeRule
     * in learned order. After learning (97,98)->256, encode("ab") must
     * return [256]; text containing pairs no rule covers stays as raw bytes.
     */
    public List<Integer> encode(String text) {
        throw new UnsupportedOperationException("TODO: encode");
    }

    /**
     * TODO (stretch goal this week):
     * Reverse the merges back to bytes and rebuild the original text.
     *
     * Contract: for any text, decode(encode(text)).equals(text) must be
     * true — the round trip is exact, including spaces and newlines.
     * Hint: a merged token expands through its rule; expansion may need to
     * repeat, because a rule's left/right can themselves be merged tokens.
     */
    public String decode(List<Integer> tokens) {
        throw new UnsupportedOperationException("TODO: decode");
    }
}
