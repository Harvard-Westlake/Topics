# Assignment — Keys and Layer 2

**Due:** Next class
**Points:** 10

---

Generate your own RSA keypair, exchange encrypted messages with a classmate, and prove both directions work.

## Steps

1. Pick two small primes `p` and `q` (different from the lesson's 5 and 11 — try pairs like 3 & 23, 7 & 13, or 11 & 17).
2. Work the key generation on paper: `n`, `phi`, your choice of `e`, and the matching `d`. Show the check that `e × d mod phi = 1`.
3. Give your **public key** `(e, n)` to a classmate. Keep `d` to yourself.
4. Turn a short message into numbers (`A=1, B=2, …`, one letter at a time, each letter must be smaller than `n`).
5. **Encrypt** a message to your classmate using *their* public key: `c = m^e mod n` for each letter. Python's `pow(m, e, n)` is allowed once your paper example works.
6. **Decrypt** the message your classmate sends you using *your* private key: `m = c^d mod n`.
7. Photograph your work: the key generation, the encryption of your outgoing message, and the decryption of the incoming one.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Own primes chosen** — your `p` and `q` are not the lesson's 5 and 11
- [ ] **Key generation shown** — `n`, `phi`, `e`, and `d` all appear with the check that `e × d mod phi = 1`
- [ ] **Encryption shown** — a message encrypted with your classmate's public key, with the arithmetic visible
- [ ] **Decryption shown** — a classmate's ciphertext decrypted with your private key back to readable text
- [ ] **Keys handled correctly** — you only ever shared `(e, n)`; `d` appears nowhere except your own private work

---

## Submission

Submit **both text and a picture** on Canvas.

### Text response

Copy the stencil, fill in each line, and paste it into the Canvas text box:

```
My primes p, q:                  
My public key (e, n):            
Classmate I exchanged with:      
Message I decrypted (plaintext): 
```

### Picture

A photo (or scan) of your worked math showing key generation, one encryption, and one decryption. Handwritten is expected — this is a pencil-and-paper assignment with Python allowed only for the modular exponentiation.
