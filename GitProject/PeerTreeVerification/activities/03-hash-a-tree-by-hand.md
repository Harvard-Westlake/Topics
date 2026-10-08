# Activity — Hash a Tree by Hand

*Concept: A tree's filename is the SHA-1 of its exact text, so you can write the tree file yourself, hash it in the terminal, and know the right answer before you run a classmate's code.*

![Diagram of a tree hashed by hand: two blob lines for hello.txt and world.txt, joined by one newline and with no newline after the last line, go into shasum and produce d5ff240dd607e36048326aaf7982a025debb0cd7, the docs tree. That hash becomes the line tree d5ff240d… docs, which joins blob 3add7b96… notes.txt and hashes to 54c35b48b2551e71b9bc43f0d44264807fbf6cc9, the tree-test tree. Two red near-misses show what a wrong answer looks like: a trailing newline gives aa4c9c79…, and writing full paths instead of names gives 04886484….](../assets/hash-a-tree-by-hand.svg)

## Task

1. In your terminal, at the root of the fork, build the test folder. `printf` writes the exact bytes with no newline at the end, and `scratch.txt` is the file you will never stage:
   ```bash
   mkdir -p tree-test/docs
   printf 'hello' > tree-test/docs/hello.txt
   printf 'world' > tree-test/docs/world.txt
   printf 'notes' > tree-test/notes.txt
   printf 'scratch' > tree-test/scratch.txt
   ```
2. Hash the three blobs you will stage, and keep the output on screen:
   ```bash
   shasum tree-test/docs/hello.txt tree-test/docs/world.txt tree-test/notes.txt    # macOS
   sha1sum tree-test/docs/hello.txt tree-test/docs/world.txt tree-test/notes.txt   # Linux / WSL
   ```
   Expected: `aaf4c61d…434d` for hello, `7c211433…bf43` for world, `3add7b96…c24d` for notes.
3. Write the `docs` tree by hand and hash it. Its lines are sorted by name, they use the final name only, and there is no newline after the last line:
   ```bash
   printf 'blob aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d hello.txt\nblob 7c211433f02071597741e6ff5a8ea34789abbf43 world.txt' | shasum
   ```
   Expected: `d5ff240dd607e36048326aaf7982a025debb0cd7`. Use `sha1sum` instead of `shasum` on Linux or WSL.
4. Use that hash to write the `tree-test` tree, then hash it:
   ```bash
   printf 'tree d5ff240dd607e36048326aaf7982a025debb0cd7 docs\nblob 3add7b9612102f2a7dbe4ed4fe886e07e847c24d notes.txt' | shasum
   ```
   Expected: `54c35b48b2551e71b9bc43f0d44264807fbf6cc9`. `scratch.txt` is not in this tree, because it was never staged.
5. See the two near-misses. A trailing newline and full paths each change every character:
   ```bash
   printf 'blob aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d hello.txt\nblob 7c211433f02071597741e6ff5a8ea34789abbf43 world.txt\n' | shasum
   printf 'blob aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d tree-test/docs/hello.txt\nblob 7c211433f02071597741e6ff5a8ea34789abbf43 tree-test/docs/world.txt' | shasum
   ```
   Expected: `aa4c9c79…3e21` and `04886484…3422`. If one of these names shows up in their `git/objects/`, you know exactly which rule they broke.
6. Run the classmate's code: init, stage `hello.txt`, `world.txt`, and `notes.txt` (not `scratch.txt`), then build the root tree. Check the result:
   ```bash
   ls git/objects | grep -E 'd5ff240d|54c35b48|aa4c9c79|04886484|93309814'
   cat git/objects/d5ff240dd607e36048326aaf7982a025debb0cd7
   ```
   `93309814…` means `scratch.txt` leaked into the tree, so their code read the folder instead of the index.
