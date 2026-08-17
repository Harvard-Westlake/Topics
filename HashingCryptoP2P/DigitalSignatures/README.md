<div align="center">

# Digital Signatures
*<font color="#8b949e">Proving who sent a message — public/private keys, signing hashes, and verification</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Review: Hashing vs Encryption](#review-hashing-vs-encryption)**  
The one-way fingerprint vs the two-way locked box.

**[Symmetric vs Asymmetric Encryption](#symmetric-vs-asymmetric-encryption)**  
One shared key vs a manufactured pair of keys.

**[How Public/Private Key Pairs Work](#how-publicprivate-key-pairs-work)**  
Two primes, one modulus, two exponents — and why you can share one key freely.

**[The Three Guarantees of a Signature](#the-three-guarantees-of-a-signature)**  
Authentication, non-repudiation, and integrity.

**[Creating and Verifying a Signature](#creating-and-verifying-a-signature)**  
The full walkthrough — and why you sign the hash, not the message.

**[Why Digital Signatures Matter](#why-digital-signatures-matter)**  
Timestamping, traceability, legal standing, and more.

**[The Starter Scripts](#the-starter-scripts)**  
Three Python scripts that generate keys, sign, and verify.

**[Class Activity: Catch the Fake](#class-activity-catch-the-fake)**  
Sign two messages — one real, one fake — and let a partner catch the forgery.

**[Public/Private Keys for SSH](#publicprivate-keys-for-ssh)**  
The same key-pair idea logs you into servers and GitHub.

---

## <font color="#388bfd">Review: Hashing vs Encryption</font>

From [last lesson](../HexadecimalAndHashing/): a **hash** is a one-way fingerprint — fixed size, no key, no way back. **Encryption** is a two-way locked box — a key locks the plaintext into ciphertext, and a key unlocks it again. Today the two team up: a digital signature is a **hash** that has been **encrypted** with a special kind of key.

---

## <font color="#388bfd">Symmetric vs Asymmetric Encryption</font>

The Caesar cipher from last lesson is **symmetric**: one shared key both locks and unlocks. That works between two people who already trust each other — but it has a fatal flaw for proving identity. If both of us hold the same key, a message "signed" with it could have been written by either of us.

**Asymmetric** encryption fixes this with a pair of different keys, manufactured together:

| | Symmetric | Asymmetric |
|---|---|---|
| Keys | One, shared by both parties | Two — a public key and a private key |
| Who can lock | Anyone with the key | Either key locks; only the *other* unlocks |
| Key sharing problem | Must secretly deliver the key first | Public key can be shared with the whole world |
| Example | Caesar cipher, ROT13, AES | RSA |
| Can prove identity? | No — both holders look identical | Yes — only one person holds the private key |

The pair is built so that **whatever one key locks, only the other key can unlock**. You publish one (the **public key**) and guard the other (the **private key**). Anything that unlocks correctly with your public key *must* have been locked with your private key — and only you have that.

---

## <font color="#388bfd">How Public/Private Key Pairs Work</font>

The keys are not two random numbers — they are computed together from a pair of secret prime numbers. In RSA (the scheme our starter scripts use), the recipe is:

1. Pick two secret primes and multiply them into a **modulus**. The modulus goes public.
2. From the primes, compute a secret helper number (the *totient*).
3. Derive two exponents from the totient — a **public exponent** and a **private exponent** — matched so that raising a number to one exponent and then the other (mod the modulus) returns the original number.

Publishing the modulus is safe for one reason only: splitting a large number back into its two primes is astronomically slow. Our classroom scripts use primes you could factor in seconds — which is exactly the point, so you can watch every step. Real RSA uses primes **hundreds of digits long**, and factoring those would take longer than the age of the universe. Same math, much bigger numbers.

> **Note:**
> The private key is never sent, never shown, never shared — not even during verification. That is the magic of the whole scheme: you prove you hold the secret without ever revealing it.

---

## <font color="#388bfd">The Three Guarantees of a Signature</font>

A valid digital signature proves three separate things at once:

| Guarantee | What it promises |
|---|---|
| **Authentication** | The receiver can be sure the message was sent by the claimed person |
| **Non-repudiation** | The creator cannot later deny having sent it — only their private key could have produced the signature |
| **Integrity** | The message has not been altered since signing — because the signature contains its hash |

Notice how the third guarantee is powered entirely by last lesson's hashing: change one character of the message and its hash changes completely, so the signature no longer matches.

---

## <font color="#388bfd">Creating and Verifying a Signature</font>

### <font color="#79c0ff">To create a signature</font>

1. Generate a key pair (public + private).
2. Compute the **hash** of the message.
3. **Encrypt that hash with your private key.** The encrypted hash — along with information such as which hashing algorithm was used — *is* the digital signature.
4. Send the message, the signature, and your public key to the receiver.

### <font color="#79c0ff">To verify a signature</font>

The verifier computes two numbers independently:

1. The **hash of the received message**, recomputed from scratch.
2. The **signature decrypted with the sender's public key** — which, if everything is genuine, is the hash the sender computed.

If the two match, the message is authentic and untouched. If they differ, either the message was tampered with after signing, or the signature was made with a private key that does not match the presented public key — an authentication failure. Either way: reject.

### <font color="#79c0ff">Why sign the hash, not the message?</font>

A hash function converts an input of *any* length into a short fixed-size value. Signing that short fingerprint is much faster than encrypting an entire document — and it is just as binding, because any change to the document changes its hash completely. Hash first, then sign the hash: fast *and* tamper-proof.

---

## <font color="#388bfd">Why Digital Signatures Matter</font>

Security is the main benefit: a signed document cannot be altered undetected, and the signature cannot be forged. Beyond that core, signatures bring:

- **Timestamping.** Recording the date and time of a signature matters when timing is critical — stock trades, lottery ticket issuance, legal proceedings.
- **Traceability.** Signatures create an audit trail, making record-keeping easier and leaving fewer chances for a document to be misplaced or a record mishandled.
- **Legal standing.** The public key infrastructure (PKI) standard governs how keys are generated and stored, and a growing number of countries accept digital signatures as legally binding.
- **Time savings.** Signing digitally removes the printing, mailing, and filing that paper signatures require.
- **Environmental impact.** Less paper produced, shipped, and thrown away.

---

## <font color="#388bfd">The Starter Scripts</font>

The `starter/` folder contains three Python scripts that walk the entire journey with numbers small enough to check by hand:

| Script | What it does |
|---|---|
| [generate_keys.py](starter/generate_keys.py) | Picks two small primes, prints every step of building the key pair, writes `public_key.txt` and `private_key.txt` |
| [sign_message.py](starter/sign_message.py) | Hashes your message with SHA-256, encrypts the hash with your private key, prints the signature |
| [verify_signature.py](starter/verify_signature.py) | Recomputes the message hash and decrypts the signature with a public key — declares `VALID` or `TAMPERED` |

Run them in order from inside the `starter/` folder:

```bash
python3 generate_keys.py
python3 sign_message.py "your message here"
python3 verify_signature.py "your message here" 12345
```

(Replace `12345` with the signature number that `sign_message.py` printed.)

> **Warning:**
> These scripts are teaching toys — their primes are tiny on purpose so you can see the math. Never use them to protect anything real.

---

## <font color="#388bfd">Class Activity: Catch the Fake</font>

1. Generate your key pair and **sign one real message**.
2. Write a **second, fake message** — one you did *not* sign.
3. Send a partner three things: both messages, your one signature, and your `public_key.txt`.
4. Your partner runs `verify_signature.py` against each message and identifies which one you actually signed.

If the verifier says `VALID` for exactly one message, the system worked: your partner authenticated the real message and caught the fake — without ever seeing your private key.

---

## <font color="#388bfd">Public/Private Keys for SSH</font>

This same key-pair idea is how developers log into remote servers — and GitHub — without passwords. **SSH authentication** works like a standing signature challenge:

1. You generate an SSH key pair on your machine and upload the **public key** to the server (or your GitHub account settings).
2. When you connect, the server sends a random challenge; your machine signs it with your **private key**.
3. The server verifies the signature with your stored public key. Match → you are in. No password ever crosses the network, and the server never learns your secret.

This is why GitHub can authenticate millions of developers without storing a single one of their private keys — it only ever holds public keys, which are safe to expose.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you state the difference between symmetric and asymmetric encryption in one sentence?
- [ ] Can you name the three guarantees of a digital signature and give a one-line description of each?
- [ ] Can you run the three starter scripts in order and get a `VALID` verification of your own message?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain why the signature encrypts the message's hash rather than the message itself?
- [ ] Can you describe the two numbers a verifier computes and what a mismatch between them means?
- [ ] Can you explain why publishing the modulus is safe when the primes are huge but unsafe when they are small?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why a symmetric key cannot provide non-repudiation but a private key can?
- [ ] Can you trace how SSH login proves your identity to a server without a password ever being transmitted?
- [ ] Can you predict what a verifier reports when a message is altered after signing — and which of the two computed numbers changed?

---

[Assignment](ASSIGNMENT.md)

← [Hexadecimal and Hashing](../HexadecimalAndHashing/) — Next: [Peer-to-Peer Networks](../PeerToPeerNetworks/)
