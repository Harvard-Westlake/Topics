import java.nio.file.Path;

// Requires your completed Chapter 1 Tokenizer.java in the same folder.
// Replace textfile.txt / textfile2.txt with your own archive text files.
public class Ch2_MarkovBaseline_Tester {
    public static void main(String[] args) {

        // ----- Chapter 1: tokenize the archive -----
        Tokenizer tokenizer = new Tokenizer();
        Path firstFile = Path.of("./textfile.txt");
        Path secondFile = Path.of("./textfile2.txt");

        try {
            tokenizer.addFiles(firstFile, secondFile);
        } catch (Exception exception) {
            System.out.println("Error adding files to tokenizer");
            return;
        }

        // Use train(256) for a BPE run (V = 512), or train(0) to stay
        // with raw bytes (V = 256) — readable generation, no merge rules.
        tokenizer.train(256);
        // tokenizer.printTokenCounts(); // You might want to comment this out so it doesn't flood your console

        System.out.println("\n--- Testing Uniform Model ---");

        // 1. Ask the tokenizer for its ACTUAL vocabulary size.
        //    train(256) does not guarantee 512 tokens — merging stops early when
        //    no pair occurs at least twice — so hard-coding 512 would be wrong.
        int finalVocabularySize = tokenizer.vocabularySize();

        // 2. Instantiate the Uniform Model
        UniformModel uniformModel = new UniformModel(finalVocabularySize);

        System.out.println("Model Vocabulary Size: " + uniformModel.vocabularySize());

        // 3. Test probabilities
        // Let's pretend token 65 ('A') is the current token, and we want to know
        // the probability of token 66 ('B') coming next.
        double prob1 = uniformModel.probability(65, 66);
        System.out.println("Probability of 66 following 65: " + prob1);

        // Now a totally different combination — the last token in the vocabulary,
        // so this works whatever vocabularySize() turned out to be.
        int lastToken = finalVocabularySize - 1;
        double prob2 = uniformModel.probability(12, lastToken);
        System.out.println("Probability of " + lastToken + " following 12: " + prob2);

        // Prove they are exactly the same
        if (prob1 == prob2) {
            System.out.println("Success! The probabilities are perfectly uniform (1/"
                    + finalVocabularySize + ").");
        }
    }
}
