# Review — Hashing Commands and Collision Math

*Originally covered in [File Hashing and Integrity](../README.md)*

---

| Command / Formula | What it does |
|---|---|
| `sha256sum file` (macOS: `shasum -a 256 file`) | 256-bit hash, 64 hex chars |
| `md5sum file` (macOS: `md5 file`) | 128-bit hash, 32 hex chars — broken for security |
| `sum file` | 16-bit checksum — only 65,536 possible values |
| `git hash-object file` | The hash Git uses to name the file's content |
| $P = 1 - e^{-\frac{k(k-1)}{2N}}$ | Probability of a collision among $k$ items in $N$ slots |
| $N \geq \frac{-k(k-1)}{2\ln(P)}$ | Slots needed for no-collision probability $P$ |

---

## Tasks

1. Create a file containing your first name and hash it with `sha256sum` (or `shasum -a 256`).
2. Hash the same file with `md5sum` and count the hex characters in each output. State which has more possible values and by roughly what factor.
3. Change one letter of your name in the file, rehash with `sha256sum`, and confirm the output shares essentially nothing with the original.
4. Compute the collision probability for 50 items hashed into 1,000 slots. Is a collision likely or unlikely?
5. Compute how many slots 50 items need for a collision chance under 1%.
