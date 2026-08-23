<div align="center">

# File Hashing and Integrity
*<font color="#8b949e">What those 40-character commit IDs really are — hash functions, collisions, and files in Java</font>*

<font color="#a371f7">Learning</font>

</div>

---

For three days you have been staring at strings like `d30f6e0a91c2...` every time you commit. They are not random, and they are not sequential — Git did not count "commit #1, commit #2." Today you learn what they actually are: **hashes** — mathematical fingerprints of your content. By the end of this lesson you will understand how a function can fingerprint any file, why two files almost never share a fingerprint, and how to compute these fingerprints yourself — in the terminal and in Java.

## <font color="#388bfd">Table of Contents</font>

1. [See what a hash function is and why Git needs one](#what-is-a-hash-function)
2. [Understand buckets, hash tables, and why collisions matter](#buckets-and-collisions)
3. [Calculate the probability of a collision with the birthday formula](#the-mathematics-of-collisions)
4. [Compare the terminal's hashing commands from weakest to strongest](#hashing-commands-in-the-terminal)
5. [Grasp how unimaginably large the SHA-256 space is](#the-scale-of-sha-256)
6. [Create and inspect files from Java with the File class](#handling-files-in-java)
7. [Connect it all back to Git — every commit ID is a hash](#gits-secret-identity)
8. [Check your understanding and try the stretch goals](#check-for-understanding)

---

## <font color="#388bfd">What is a Hash Function?</font>

A **hash function** takes any input — a word, a file, an entire movie — and produces a **fixed-size output** called a hash (or digest). The same input always produces the same output, but even a one-character change to the input produces a completely different, unpredictable output.

Three properties make hash functions useful:

- **Deterministic** — hashing `"hello"` today, tomorrow, or on your classmate's machine always gives the identical result.
- **Fixed size** — whether the input is 3 bytes or 3 gigabytes, a SHA-256 hash is always exactly 256 bits (written as 64 hex characters).
- **Avalanche effect** — changing a single bit of the input scrambles the entire output. There is no way to look at two hashes and tell that their inputs were "almost the same."

Think of a hash as a **fingerprint**. A fingerprint doesn't contain the person, but no two people share one — and you can't reconstruct the person from the print.

> **Note:**
> Hashing is one-way. You can go from file → hash instantly, but there is no way to go from hash → file. That asymmetry is what makes hashes useful for verification and security.

---

## <font color="#388bfd">Buckets and Collisions</font>

Hash functions were not invented for security — they were invented for **speed**. A **hash table** stores items in numbered "buckets," and the hash of an item's key tells you exactly which bucket to look in. Instead of searching through everything one by one, you jump straight to the right bucket: on average a **constant-time, O(1)** lookup. Hash tables power dictionaries, sets, caches, and database indexes.

But there's a catch. If two different items hash to the **same bucket**, that's a **collision**. Without a plan for collisions, a new entry either overwrites the old one (data loss) or gets rejected (lost capacity). Real hash tables resolve collisions with techniques like chaining, but every collision costs speed — so the deeper question is:

**How many buckets do we need so that collisions are unlikely in the first place?**

The answer is much stranger than you'd guess.

---

## <font color="#388bfd">The Mathematics of Collisions</font>

The probability that **at least two** of $k$ randomly assigned items collide inside $N$ possible slots is approximately:

$$P(\text{collision}) = 1 - e^{-\frac{k(k-1)}{2N}}$$

- $k$ — the number of items being hashed
- $N$ — the number of possible hash values (buckets, lockers, slots...)

**Worked example — 30 students, 100 lockers.** Assign each of 30 students a random locker out of 100. What's the chance two students get the same locker?

$$P = 1 - e^{-\frac{30 \cdot 29}{2 \cdot 100}} = 1 - e^{-4.35} \approx 0.987$$

**A 98.7% chance of a collision** — with more than three times as many lockers as students! This is the **birthday paradox**: collisions become likely far, far sooner than intuition suggests, because what matters is the number of *pairs* of items ($\approx k^2/2$), not the number of items.

To *design* for a collision probability, rearrange the formula to solve for $N$, where $P$ is the desired probability of **no** collision:

$$N \geq \frac{-k(k-1)}{2\ln(P)}$$

For 30 students to have **less than a 1% chance** of any shared locker ($P = 0.99$), you need $N \geq \frac{-870}{2\ln(0.99)} \approx 43{,}282$ lockers. Thirty students. Forty-three thousand lockers. That's the price of near-certainty — and it's exactly why hash outputs have to be so enormous.

👉 <details>
<summary><h3>Activity: The Locker Problem — click to expand</h3></summary>

*Concept: The birthday paradox makes collisions far more likely than intuition suggests, and the collision formula tells you exactly how much space "safe" costs.*

![Chart of collision probability versus the number of people in the room, for 365 possible birthdays. The curve races upward: at just 23 people the probability of a shared birthday already reaches 50%, and by 60 people it exceeds 99%. What matters is pairs, not people — k people form k(k−1)/2 chances to collide.](assets/the-locker-problem.svg)

## Task

1. On paper or with a calculator, use the collision formula $P = 1 - e^{-\frac{k(k-1)}{2N}}$ with your actual class. Set $k$ to the number of students in the room and $N = 365$ (days of the year). Compute the probability that two people in the room share a birthday. (For $k = 24$: $P = 1 - e^{-\frac{24 \cdot 23}{730}} \approx 0.53$ — better than a coin flip.)
2. Check the prediction against reality: go around the room and see if two people actually share a birthday.
3. Now flip the formula around. Using $N \geq \frac{-k(k-1)}{2\ln(P)}$, calculate how many lockers your class would need so there is **less than a 1% chance** any two students are randomly assigned the same locker ($P = 0.99$).
4. Write one sentence answering: why does the required $N$ grow so much faster than $k$? (The chart's caption has the key idea.)

*(Standalone file: [activities/01-the-locker-problem.md](activities/01-the-locker-problem.md))*

</details>

---

## <font color="#388bfd">Hashing Commands in the Terminal</font>

Your terminal ships with a whole family of hash functions. They differ in one crucial way: **how many bits of output they produce** — which, as you just calculated, controls how likely collisions are.

| Command | Output size | Possible values |
|---|---|---|
| `sum file` | 16-bit checksum | 2^16 = 65,536 |
| `cksum file` | 32-bit checksum | 2^32 ≈ 4.3 × 10^9 |
| `md5sum file` | 128-bit (32 hex chars) | 2^128 ≈ 3.4 × 10^38 |
| `shasum file` | 160-bit (40 hex chars) | 2^160 ≈ 1.5 × 10^48 |
| `sha256sum file` | 256-bit (64 hex chars) | 2^256 ≈ 1.2 × 10^77 |
| `sha512sum file` | 512-bit (128 hex chars) | 2^512 ≈ 1.3 × 10^154 |

> **Note:**
> On macOS, use `shasum -a 256` and `shasum -a 512` instead of `sha256sum`/`sha512sum`, and `md5` instead of `md5sum`. Same algorithms, slightly different command names.

A 16-bit `sum` collides constantly — 65,536 slots is nothing (your class of students needs 27,000+ lockers, remember?). MD5 and SHA-1 are broken for security use: researchers can manufacture collisions on purpose. **SHA-256 and SHA-512 are the modern standards** — collision-resistant enough to protect passwords, digital signatures, and Bitcoin.

👉 <details>
<summary><h3>Activity: One Bit Changes Everything — click to expand</h3></summary>

*Concept: Hashes are deterministic (same content → same hash, on any machine) yet avalanche completely when even one character changes.*

![Diagram of the avalanche effect: two input sentences differing only in the case of one letter flow into SHA-256 and come out as two 64-character hashes that share nothing — the real values f2ad2d87... and 919f031a... that this activity's commands produce on any machine.](assets/one-bit-avalanche.svg)

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

*(Standalone file: [activities/02-one-bit-changes-everything.md](activities/02-one-bit-changes-everything.md))*

</details>

---

## <font color="#388bfd">The Scale of SHA-256</font>

2^256 is not a big number. It is an **incomprehensible** number:

- Written out: 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457,584,007,913,129,639,936 possible values.
- That is comparable to the estimated number of **atoms in the observable universe** (10^78 to 10^82).
- If you could check **one trillion hashes per second**, exhausting the SHA-256 space would take roughly 10^63 years. The universe is 1.4 × 10^10 years old.
- If every person on Earth generated a million hashes per second for a century, humanity would have used about 0.0000000000000000000000001% of the space.

This is why nobody worries about two different files "accidentally" sharing a SHA-256 hash. It isn't impossible — it's just so improbable that betting on it is a worse bet than picking one specific atom out of the entire solar system.

> **Tip:**
> This is the answer to the locker problem at scale. Want a collision chance near zero for billions of files? Make $N = 2^{256}$ and the formula's exponent becomes so tiny that $P \approx 0$ for any realistic $k$.

---

## <font color="#388bfd">Handling Files in Java</font>

To hash files in a program, you first need to *touch* files from a program. Java's `File` class represents a **path** to a file or directory — a pointer to a location, not the contents:

```java
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

File file = new File("notes.txt");       // a path — nothing exists yet
file.createNewFile();                     // now the file exists (returns false if it already did)

File dir = new File("JavaFileSystem");
dir.mkdir();                              // create a directory (mkdirs() for nested paths)
```

Useful `File` methods for inspecting what a path points at:

| Method | What it tells you |
|---|---|
| `exists()` | Whether the file or directory is really there |
| `isFile()` / `isDirectory()` | Which kind of thing the path points to |
| `length()` | Size in bytes |
| `delete()` | Remove the file or (empty) directory |

Writing and reading contents uses `FileWriter` and `BufferedReader` — the same classes from the Initial Install path activity:

```java
FileWriter writer = new FileWriter("notes.txt");
writer.write("Hashing turns any content into a fixed-size fingerprint.");
writer.close();                           // always close — unwritten data may be lost otherwise
```

And Java's built-in `MessageDigest` class computes SHA-256 directly — this is the engine you will use in the assignment to build your own file hasher:

```java
import java.security.MessageDigest;

MessageDigest digest = MessageDigest.getInstance("SHA-256");
byte[] hash = digest.digest(fileContents.getBytes());   // 32 bytes = 256 bits
```

> **Warning:**
> File operations fail in the real world — the path doesn't exist, you lack permission, the disk is full. That's why Java forces you to handle `IOException` with try/catch. Treat the catch block as a first-class part of your program, not an afterthought.

---

## <font color="#388bfd">Git's Secret Identity</font>

Here is the payoff. **Git is a content-addressed database built on hashing.** Every object Git stores — every file snapshot, every commit — is named by the hash of its content. Those 40-character commit IDs you've been copying all week? Hashes.

You can run Git's own hashing yourself:

```bash
git hash-object message.txt
```

This means:

- **Identical content gets identical IDs, everywhere.** If you and a classmate each commit a file with the exact same bytes, Git gives it the exact same object ID on both machines — without your computers ever talking.
- **Tampering is self-evident.** Change one byte of a committed file's history and its hash no longer matches its ID. The avalanche effect turns any corruption or manipulation into a flashing alarm.
- **Commits chain their history together.** Each commit's hash covers its content *and* its parent commit's hash — so rewriting anything in the past changes every ID after it. That is what makes a Git history trustworthy.

The `.git/objects` folder you explored in The Hidden Detective activity on Day 1? It is one giant hash table, with SHA hashes as the bucket labels.

👉 <details>
<summary><h3>Activity: Git's Secret Identity — click to expand</h3></summary>

*Concept: Git names every object by the hash of its content — identical content produces identical IDs on any machine, and any change is instantly detectable.*

![Diagram of two different laptops each creating a file containing hello git and running git hash-object on it. Both machines produce the identical ID 8d0e41234f24b6da002d962a26c2495ea16a425f without ever communicating — because the ID is computed from the content, not assigned to it. This is exactly how commit IDs work.](assets/gits-secret-identity.svg)

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

*(Standalone file: [activities/03-gits-secret-identity.md](activities/03-gits-secret-identity.md))*

</details>

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] State the three properties of a hash function (deterministic, fixed-size, avalanche) and give a one-line example of each.
- [ ] Hash a file in the terminal with `sha256sum` (or `shasum -a 256`) and read off how many hex characters the output has.
- [ ] Explain what a collision is and why hash tables care about them.

### <font color="#79c0ff">Intermediate</font>

- [ ] Compute the collision probability for a given $k$ items and $N$ slots using $P = 1 - e^{-\frac{k(k-1)}{2N}}$.
- [ ] Use $N \geq \frac{-k(k-1)}{2\ln(P)}$ to size a hash space for a target collision probability.
- [ ] Create a directory and a file from Java using the `File` class, and write text into it with `FileWriter`.
- [ ] Rank `sum`, `md5sum`, and `sha256sum` by collision resistance and justify the ranking with bit lengths.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why 30 students need ~43,000 lockers for a 1% collision chance, in terms of pairs rather than items.
- [ ] Explain how Git uses content hashing to give identical files identical IDs across machines that have never communicated.
- [ ] Explain why hashing each commit's parent hash makes historical tampering detectable.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] **Hunt a collision you can actually find:** `sum` has only 65,536 outputs. Write a loop that generates numbered files until two of them share a `sum` checksum, and report how many files it took.
- [ ] **Peek inside the hash table:** in a real repository, open `.git/objects` and find the folder+filename that together spell out one of your commit hashes.
- [ ] **Research:** look up how Git is migrating from SHA-1 to SHA-256 and why the transition is difficult.

---

[Assignment](ASSIGNMENT.md)

← [Forks and Collaboration](../ForksAndCollaboration/) — Back to [Git Usage](../)
