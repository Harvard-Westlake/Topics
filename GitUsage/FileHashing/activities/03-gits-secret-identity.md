# Activity — Git's Secret Identity

*Concept: Git names every object by the hash of its content — identical content produces identical IDs on any machine, and any change is instantly detectable.*

![Diagram of two different laptops each creating a file containing hello git and running git hash-object on it. Both machines produce the identical ID 8d0e41234f24b6da002d962a26c2495ea16a425f without ever communicating — because the ID is computed from the content, not assigned to it. This is exactly how commit IDs work.](../assets/gits-secret-identity.svg)

## Task

1. In your terminal, in any folder, create a file with **exactly** this content and ask Git to hash it (this works even outside a repository):
   ```bash
   echo "hello git" > secret.txt
   git hash-object secret.txt
   ```
2. Compare the 40-character ID with a classmate who ran the same commands — and with the diagram. All three match: different machines, zero communication, identical ID. Write one sentence explaining how that is possible.
3. Change the content by one character, rerun `git hash-object secret.txt`, and confirm the ID is completely different.
4. Now connect it to real history: in your terminal, inside the `git-detective` repository from Day 1 (or any repo), run:
   ```bash
   git log --oneline -3
   ```
   Those short IDs on the left are abbreviations of full 40-character hashes, each one covering the commit's content *and* its parent's hash.
5. In one sentence: why does hashing each commit's parent make it hard to secretly rewrite old history?
