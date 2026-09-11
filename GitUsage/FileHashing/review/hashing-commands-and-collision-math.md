# Review — Hashing Commands and Collision Math

*Originally covered in [File Hashing](../README.md)*

---

| Command / Formula | What it is |
|---|---|
| `sum file` | 16-bit checksum, $2^{16} = 65{,}536$ outputs |
| `crc32 file` | 32-bit checksum, $2^{32} \approx 4.29 \times 10^{9}$ outputs |
| `md5sum file` (macOS: `md5 file`) | 128-bit hash, 32 hex chars, $2^{128}$ outputs |
| `sha1sum file` (macOS: `shasum -a 1 file`) | 160-bit hash, 40 hex chars, $2^{160}$ outputs |
| `sha256sum file` (macOS: `shasum -a 256 file`) | 256-bit hash, 64 hex chars, $2^{256}$ outputs |
| `sha512sum file` (macOS: `shasum -a 512 file`) | 512-bit hash, 128 hex chars, $2^{512}$ outputs |
| $P(\text{collision}) \approx 1 - e^{-\frac{k(k-1)}{2N}}$ | Chance that $k$ items collide in $N$ buckets |
| $N \geq \frac{-k(k-1)}{2\ln(P)}$ | Buckets needed for a no-collision probability of $P$ |

---

## Tasks

1. Create a file containing your first name and hash it with `sum`, `md5sum`, and `sha256sum` (or the macOS equivalents). Count the characters in each output.
2. State how many possible outputs each of those three commands has, and by roughly what factor `sha256sum` beats `md5sum`.
3. Compute the collision probability for 50 items hashed into 1,000 buckets. Is a collision likely or unlikely?
4. Compute how many buckets 50 items need for a collision chance under 1%.
