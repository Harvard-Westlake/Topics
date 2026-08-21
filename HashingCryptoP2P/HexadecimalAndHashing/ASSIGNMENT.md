# Assignment — Hexadecimal and Hashing

*Lesson: [Hexadecimal and Hashing](README.md)*

**Due:** Next class  
**Points:** 5

---

## Part 1 — Number Conversions

Complete these conversions **by hand** (show the 4-bit groups or place-value arithmetic — no calculators, no converters). These are different problems from the practice set, so the answer key will not help you here.

**Hex to decimal**

1. `4B`
2. `D2`

**Decimal to hex**

3. 58
4. 141

**Hex to binary**

5. `9E`

**Binary to hex**

6. `110110`

---

## Part 2 — Hashing

7. Using the toy hash function `hash(x) = (x × 256) mod 100`, compute `hash(12)` by hand. Show the multiplication and the mod step.
8. Find a second input (different from 12) that the toy hash sends to the **same** output as `hash(12)` — that is, find a collision. Explain in one sentence how you found it.
9. Open the [SHA-256 online tool](https://emn178.github.io/online-tools/sha256.html) and hash your **first name, all lowercase**. Copy the full 64-character digest.
10. Change one letter of your name to a capital and hash again. In one sentence, describe what happened to the digest.

---

## Part 3 — Symmetric Encryption

11. Decode this ROT13 ciphertext by hand: `GUR CNFFJBEQ VF UNFU`
12. In one sentence each, state what **hashing** is for and what **encryption** is for — the two sentences must make the difference clear.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **All six conversions correct with work shown** — each answer includes the 4-bit groups or the place-value arithmetic that produced it
- [ ] **Toy hash computed by hand** — the multiplication and mod steps are both written out and the final value is correct
- [ ] **Collision found** — you name a second input with the same toy-hash output as 12 and say how you found it
- [ ] **Two SHA-256 digests captured** — both are complete 64-character hex strings copied from the tool
- [ ] **ROT13 decoded** — the plaintext is an English sentence
- [ ] **Hashing vs encryption distinguished** — a reader of your two sentences could tell which tool to use for which job

---

## Submission

Submit **one text response** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
1. 4B in decimal:            (work: )
2. D2 in decimal:            (work: )
3. 58 in hex:                (work: )
4. 141 in hex:               (work: )
5. 9E in binary:             (work: )
6. 110110 in hex:            (work: )
7. hash(12):                 (work: )
8. Collision input:          (how I found it: )
9. SHA-256 of my name:       
10. What changed and why:    
11. ROT13 plaintext:         
12. Hashing is for:          
    Encryption is for:       
```
