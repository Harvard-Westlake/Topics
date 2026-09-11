# Review — Hash Table Sizing Problems

*Originally covered in [File Hashing](../README.md)*

---

Everything from the hashing-commands review, plus:

| Step | Formula |
|---|---|
| Desired no-collision probability | $P = 1 - P(\text{collision})$ |
| Buckets needed | $N \geq \frac{-k(k-1)}{2\ln(P)}$ |
| Pick a hash function | smallest command whose $2^{\text{bits}} > N$ |

---

## Tasks

1. A school of 1,600 students assigns random locker numbers. Compute how many lockers keep the chance of a shared locker under 0.5%.
2. A website gives each of 50 million users a random session token. State a target collision probability, compute the required $N$, and name the smallest terminal hash function whose output space exceeds it.
3. Express your answer to task 2 as a power of two (compute $\log_2 N$) and confirm it is below the bit length of the hash function you chose.
4. Explain in two sentences why doubling $k$ roughly quadruples the required $N$.
