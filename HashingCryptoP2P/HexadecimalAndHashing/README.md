<div align="center">

# Hexadecimal and Hashing
*<font color="#8b949e">Base-16 numbers, digital fingerprints, and how hashing differs from encryption</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Hexadecimal Numbers](#hexadecimal-numbers)**  
Base-16, why computing uses it, and the digit table.

**[Converting Between Bases](#converting-between-bases)**  
Worked examples for hex ↔ decimal and hex ↔ binary.

**[Practice: Number Conversions](#practice-number-conversions)**  
A worksheet of conversions with a full answer key.

**[Hash Functions](#hash-functions)**  
The four properties, a toy hash you can compute by hand, and SHA-256.

**[Applications of Hashing](#applications-of-hashing)**  
Password storage, data integrity, Merkle trees, and proof of work.

**[Hashing vs Encryption](#hashing-vs-encryption)**  
One-way fingerprints vs two-way locked boxes.

**[Symmetric-Key Encryption](#symmetric-key-encryption)**  
The Caesar cipher and ROT13 — one shared key to lock and unlock.

---

## <font color="#388bfd">Hexadecimal Numbers</font>

**Hexadecimal** (hex) is a base-16 number system. It uses sixteen symbols: `0`–`9` for the values zero through nine, and `A`–`F` (or `a`–`f`) for the values ten through fifteen.

| Hex digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Value | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |

**Why hex?** Computers store everything in binary (base-2), but long strings of 1s and 0s are painful for humans to read or write. Hex is the fix: because 16 = 2⁴, **one hex digit represents exactly four binary digits (bits)**. A 256-bit number that would take 256 binary characters fits in just 64 hex characters — same number, far more readable.

| Hex | Binary (4 bits) | Hex | Binary (4 bits) |
|---|---|---|---|
| `0` | `0000` | `8` | `1000` |
| `1` | `0001` | `9` | `1001` |
| `2` | `0010` | `A` | `1010` |
| `3` | `0011` | `B` | `1011` |
| `4` | `0100` | `C` | `1100` |
| `5` | `0101` | `D` | `1101` |
| `6` | `0110` | `E` | `1110` |
| `7` | `0111` | `F` | `1111` |

> **Tip:**
> This table is the whole trick. Converting between hex and binary never requires arithmetic — just swap each hex digit for its 4-bit group, or each 4-bit group for its hex digit.

---

## <font color="#388bfd">Converting Between Bases</font>

### <font color="#79c0ff">Hex to binary — substitute each digit</font>

Convert `1A3` to binary, one digit at a time:

```
1    A    3
0001 1010 0011
```

Drop the leading zeros: `1A3` in hex is `110100011` in binary.

### <font color="#79c0ff">Hex to decimal — place values are powers of 16</font>

Just as decimal places are worth 1, 10, 100, …, hex places are worth 1, 16, 256, …

```
1A3 = (1 × 256) + (10 × 16) + (3 × 1)
    =  256      +  160      +  3
    =  419
```

### <font color="#79c0ff">Decimal to hex — divide by 16, keep remainders</font>

Convert 255 to hex:

```
255 ÷ 16 = 15 remainder 15     → both 15s are the hex digit F
```

Reading the digits gives `FF`. So the decimal number 255 is `FF` in hex — which is why `FF` shows up everywhere as "the biggest value that fits in one byte" (a byte is 8 bits = 2 hex digits).

### <font color="#79c0ff">Binary to hex — group into fours from the right</font>

Convert `101101` to hex. Group the bits into fours starting from the right, padding the left with zeros:

```
0010 1101
2    D
```

So `101101` in binary is `2D` in hex (which is 45 in decimal).

---

## <font color="#388bfd">Practice: Number Conversions</font>

Work these without a calculator, then check the answer key. (This replaces the paper worksheet used in previous years.)

### <font color="#79c0ff">Problems</font>

**Hex to decimal**

1. `2F`
2. `64`
3. `3E8`

**Decimal to hex**

4. 26
5. 175
6. 1000

**Hex to binary**

7. `B4`
8. `7C`
9. `A0`

**Binary to hex**

10. `11111111`
11. `10100000`
12. `0001101000110000`

### <font color="#79c0ff">Answer key</font>

| # | Problem | Answer | Check |
|---|---|---|---|
| 1 | `2F` → decimal | 47 | (2 × 16) + 15 = 47 |
| 2 | `64` → decimal | 100 | (6 × 16) + 4 = 100 |
| 3 | `3E8` → decimal | 1000 | (3 × 256) + (14 × 16) + 8 = 1000 |
| 4 | 26 → hex | `1A` | 26 = 16 + 10 |
| 5 | 175 → hex | `AF` | 175 = (10 × 16) + 15 |
| 6 | 1000 → hex | `3E8` | reverse of #3 |
| 7 | `B4` → binary | `10110100` | B = `1011`, 4 = `0100` |
| 8 | `7C` → binary | `1111100` | 7 = `0111`, C = `1100`, drop leading 0 |
| 9 | `A0` → binary | `10100000` | A = `1010`, 0 = `0000` |
| 10 | `11111111` → hex | `FF` | `1111` = F, `1111` = F |
| 11 | `10100000` → hex | `A0` | `1010` = A, `0000` = 0 |
| 12 | `0001101000110000` → hex | `1A30` | `0001` `1010` `0011` `0000` |

---

## <font color="#388bfd">Hash Functions</font>

A **hash function** is an algorithm that takes an input (a "message" — any data, any length) and returns a fixed-size output called a **digest** or simply a **hash**. The output looks random, but it is completely determined by the input. Hash functions are designed to be **one-way**: computing the hash of an input is easy, but recovering the input from its hash should be computationally infeasible.

### <font color="#79c0ff">The four key properties</font>

| Property | Meaning |
|---|---|
| **Deterministic** | The same input always produces the same output — on any computer, any day |
| **Fast computation** | Computing the hash of any input is quick |
| **Pre-image resistant** | Given a hash, it is infeasible to work backward to an input that produces it |
| **Collision resistant** | It is infeasible to find two different inputs that produce the same hash |

### <font color="#79c0ff">A toy hash you can compute by hand</font>

To see the mechanics, here is a deliberately simple hash function:

```
hash(x) = (x × 256) mod 100
```

Hashing the input `5`:

```
hash(5) = (5 × 256) mod 100 = 1280 mod 100 = 80
```

Try `hash(3)` yourself: 3 × 256 = 768, and 768 mod 100 = **68**.

This toy satisfies "deterministic" and "fast" — but it fails the other two properties badly. Every output is between 0 and 99, so collisions are everywhere: `hash(30) = 7680 mod 100 = 80`, the same as `hash(5)`. Real hash functions make collisions astronomically unlikely by using an enormous output space.

### <font color="#79c0ff">A real hash: SHA-256</font>

**SHA-256** outputs a 256-bit digest, written as 64 hex characters (there is the hex connection — one hex digit per four bits). The SHA-256 hash of the string `hello` is:

```
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

Capitalize a single letter — `Hello` — and the hash changes completely:

```
185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
```

Not one character of the two digests lines up. This total scrambling from a tiny input change is exactly what makes a hash a tamper detector.

> **Tip:**
> Open the [SHA-256 online tool](https://emn178.github.io/online-tools/sha256.html) and hash `hello` yourself — you should get exactly the digest above. Then change one character and watch the whole thing change.

---

## <font color="#388bfd">Applications of Hashing</font>

### <font color="#79c0ff">Password storage</font>

Well-built systems never store your actual password. They store its **hash**. When you log in, the system hashes what you typed and compares it to the stored hash — if they match, you knew the password. Even if the database is stolen, the attacker holds only fingerprints, not passwords. A random value called a **salt** is added to each password before hashing so that two users with the same password still get different hashes, and precomputed lookup tables become useless.

### <font color="#79c0ff">Data integrity</font>

A hash is a unique fingerprint for a file. When you download a file, the source can publish its hash; you hash your downloaded copy and compare. If even one bit changed in transit — corruption or tampering — the hashes will not match. This is why download pages often list a SHA-256 "checksum" next to the file.

### <font color="#79c0ff">Merkle trees (honors)</font>

Blockchains summarize thousands of transactions with a **Merkle tree**: each leaf is the hash of one transaction, and each parent node is the hash of its children, all the way up to a single root hash. Changing any transaction anywhere changes the root — so one 64-character hash vouches for an entire block of data, and membership of any single transaction can be proven quickly.

### <font color="#79c0ff">Proof of work (honors)</font>

Some blockchains make participants search for an input whose hash meets a target (for example, starts with many zeros). Because hashes cannot be predicted or reversed, the only strategy is guessing billions of times — so a valid answer is *proof* that real computational work was done. This is the "mining" you will meet in the [Blockchains and Bitcoin](../../Blockchains/) unit.

---

## <font color="#388bfd">Hashing vs Encryption</font>

These two are constantly confused, and the difference matters for everything that follows in this unit:

| | Hashing | Encryption |
|---|---|---|
| Direction | **One-way** — no way back | **Two-way** — designed to be reversed |
| Output size | Fixed, regardless of input size | Roughly as large as the input |
| Needs a key? | No | Yes — a key locks it, a key unlocks it |
| Purpose | Fingerprint / verify data | Hide data from everyone without the key |
| Question it answers | "Is this the same data?" | "Can I keep this secret in transit?" |

A hash is a **fingerprint**: it identifies data but cannot be turned back into it. Encryption is a **locked box**: the data is all still in there, and the right key gets it back out.

---

## <font color="#388bfd">Symmetric-Key Encryption</font>

In cryptography, **encryption** encodes information: it converts the readable original, called **plaintext**, into a scrambled form called **ciphertext**. Ideally, only authorized parties can decipher the ciphertext back to plaintext. Encryption does not stop anyone from intercepting the message — it just denies them anything intelligible to read.

**Symmetric-key** encryption uses a *single shared key* for both locking and unlocking: whoever can encrypt can also decrypt.

### <font color="#79c0ff">The Caesar cipher</font>

The oldest symmetric cipher: shift every letter forward by a fixed amount. The shift amount *is* the key. With a key of 3:

```
Plaintext:   H E L L O
Shift by 3:  K H O O R
```

To decrypt, the receiver shifts back by 3. Both sides must know the same key — that is what makes it symmetric.

### <font color="#79c0ff">ROT13</font>

**ROT13** is a Caesar cipher with a shift of exactly 13. Since the alphabet has 26 letters, applying ROT13 twice returns the original — the same operation both encrypts and decrypts:

```
A B C D E F G H I J K L M
↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕
N O P Q R S T U V W X Y Z
```

Each letter swaps with the one directly across: `A↔N`, `B↔O`, … `M↔Z`. So:

```
HELLO  → ROT13 →  URYYB
URYYB  → ROT13 →  HELLO
```

> **Warning:**
> Caesar ciphers are teaching toys, not security. There are only 25 possible shifts — an attacker just tries them all. But they demonstrate the symmetric-key idea perfectly: one shared secret, used to lock and unlock. Next lesson introduces **asymmetric** encryption, where the locking key and unlocking key are different — the idea that makes digital signatures possible.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you list the sixteen hex digits and the value of each letter `A`–`F`?
- [ ] Can you convert `FF` to decimal and 26 to hex without a calculator?
- [ ] Can you name the four key properties of a hash function?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you convert `1A3` to binary using the 4-bits-per-digit substitution, without any arithmetic?
- [ ] Can you compute `hash(x) = (x × 256) mod 100` for `x = 5` by hand and explain why this toy hash is not collision resistant?
- [ ] Can you explain the difference between hashing and encryption in one sentence each?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why SHA-256 digests are written as exactly 64 hex characters?
- [ ] Can you explain how a salt defends stored password hashes against precomputed lookup tables?
- [ ] Can you explain why applying ROT13 twice returns the original message, and why that makes it symmetric?

---

[Assignment](ASSIGNMENT.md)

← Back to [Hashing, Cryptography, and P2P Networks](../) — Next: [Digital Signatures](../DigitalSignatures/)
