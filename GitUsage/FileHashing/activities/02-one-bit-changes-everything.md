# Activity — One Bit Changes Everything

*Concept: Hashes are deterministic (same content → same hash, on any machine) yet avalanche completely when even one character changes.*

![Diagram of the avalanche effect: two input sentences differing only in the case of one letter flow into SHA-256 and come out as two 64-character hashes that share nothing — the real values f2ad2d87... and 919f031a... that this activity's commands produce on any machine.](../assets/one-bit-avalanche.svg)

## Task

1. In your terminal, create a file and hash it (macOS: use `shasum -a 256` instead of `sha256sum`):
   ```bash
   echo "Git is a content tracker" > message.txt
   sha256sum message.txt
   ```
2. Copy the 64-character hash somewhere you can compare against — it should match the top hash in the diagram exactly.
3. Change exactly one character — capitalize the `g`:
   ```bash
   echo "git is a content tracker" > message.txt
   sha256sum message.txt
   ```
   Compare the two hashes. Count how many characters they share in the same positions — it should look like a completely unrelated string, and match the bottom hash in the diagram.
4. Restore the original text, rehash, and confirm you get **exactly** the original hash back — determinism.
5. Hash an empty file:
   ```bash
   touch empty.txt
   sha256sum empty.txt
   ```
   Compare with a neighbor. Every empty file on every machine on Earth hashes to the same value (it starts `e3b0c442...`). Write one sentence on why that must be true.
