# Activity — Hash It by Hand

*Concept: A blob's filename is the SHA-1 of its exact bytes — you can compute that hash yourself in the terminal and compare it to what the classmate's program produced.*

![Diagram comparing two hashes of the same word: the top path creates sha1test.txt with printf, eight bytes and no newline, runs shasum, and gets 12c4c60ee087ae0f12dc6abc88495e459f6f2654, which matches the blob filename in git/objects with a green check. The bottom path uses echo without -n, nine bytes ending in a newline, and gets a completely different hash starting c06872ab, marked with a red cross — one invisible byte changes every character.](../assets/hash-it-by-hand.svg)

## Task

1. In your terminal, inside the fork, create a test file containing exactly the text `sha1test` with **no newline** at the end, and count its bytes:
   ```bash
   printf 'sha1test' > sha1test.txt
   wc -c sha1test.txt
   ```
   `wc -c` must report `8`. If it says `9`, a newline sneaked in — recreate the file.
2. Hash it yourself:
   ```bash
   shasum sha1test.txt        # macOS — SHA-1 is shasum's default
   sha1sum sha1test.txt       # Linux / WSL
   ```
   Expected: `12c4c60ee087ae0f12dc6abc88495e459f6f2654`.
3. See the trap. Hash the same word with and without a trailing newline:
   ```bash
   echo "sha1test" | shasum
   echo -n "sha1test" | shasum
   ```
   Only the `-n` version matches. One invisible byte changes every character of the hash — remember this when a classmate's hash is "almost right".
4. Run the classmate's program so it stages `sha1test.txt` (use your `Verify.java` driver if their `main` does nothing), then list the blobs:
   ```bash
   ls git/objects
   ```
   Record whether a file named `12c4c60ee087ae0f12dc6abc88495e459f6f2654` appeared. A different 40-character name means their hash is wrong, or they hashed something other than the raw bytes — a newline, the path, or a header.
5. Confirm the content survived byte for byte:
   ```bash
   diff sha1test.txt git/objects/12c4c60ee087ae0f12dc6abc88495e459f6f2654 && echo IDENTICAL
   ```
   If `diff` prints anything, the blob is not a faithful copy — note exactly what differs.
