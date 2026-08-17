<div align="center">

# Keys and Layer 2
*<font color="#8b949e">The math inside a keypair, keys that need multiple signers, and payment networks built on Bitcoin</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Overview for today</font>

- Understand a little more of the **math** behind key generation
- Learn about other types of keys — **multi-signature** keys
- Understand **payment networks built on top of Bitcoin** (Layer 2)

You have been *using* public/private keys since [Hashing, Cryptography, and P2P Networks](../../HashingCryptoP2P/) — signing messages and verifying signatures. Today you finally see the machinery: numbers small enough to compute by hand.

---

## <font color="#388bfd">RSA public / private key math</font>

RSA keys are built from prime numbers. The whole system rests on one asymmetry: multiplying two primes is trivial, but starting from the product and recovering the primes is brutally hard when the primes are enormous.

### <font color="#79c0ff">Generating a keypair (worked example)</font>

| Step | Rule | Our tiny example |
|---|---|---|
| 1 | Pick two primes `p` and `q` | `p = 5`, `q = 11` |
| 2 | Compute `n = p × q` | `n = 55` |
| 3 | Compute `phi = (p − 1) × (q − 1)` | `phi = 4 × 10 = 40` |
| 4 | Pick `e` sharing no factors with `phi` | `e = 3` |
| 5 | Find `d` so that `e × d` leaves remainder 1 when divided by `phi` | `d = 27`, since `3 × 27 = 81 = 2 × 40 + 1` |

- **Public key** = `(e, n)` = `(3, 55)` — hand this to anyone.
- **Private key** = `(d, n)` = `(27, 55)` — tell no one.

### <font color="#79c0ff">Encrypting and decrypting</font>

Turn your message into a number `m` smaller than `n` (say `A=1, B=2, …`), then:

| Direction | Rule | Our tiny example |
|---|---|---|
| Encrypt with the **public** key | `c = m^e mod n` | `m = 7`: `7³ = 343`, and `343 mod 55 = 13` → ciphertext `13` |
| Decrypt with the **private** key | `m = c^d mod n` | `13²⁷ mod 55 = 7` → message `7` recovered |

That last exponent is unpleasant by hand — let Python do the modular arithmetic:

```bash
python3 -c "print(pow(13, 27, 55))"   # prints 7
```

Why can't an eavesdropper undo the encryption? They see `(3, 55)` and the ciphertext `13`. To find `d` they must factor `55` back into `5 × 11`. Trivial here — but real RSA uses primes hundreds of digits long, and factoring *that* `n` would take longer than the age of the universe. The public key can shout; the private key stays safe.

> **Note:**
> This is the same key mathematics behind the signatures you made last unit — run in reverse. Encrypting with the *private* key (which anyone can undo with the public key) proves *who wrote it*: that is a signature. Encrypting with the *public* key (which only the private key can undo) hides *what it says*: that is encryption.

---

## <font color="#388bfd">Multi-signature keys</font>

A normal wallet needs one signature to spend. A **multi-signature** (multisig) wallet requires **m of n** keys to sign before a transaction is valid:

| Setup | Requires | Good for |
|---|---|---|
| 2-of-2 | Both keys | Two business partners who must both approve every payment |
| 2-of-3 | Any two of three keys | You + your parent + a backup key in a drawer — lose any one key and funds survive |
| 3-of-5 | Any three of five keys | An exchange's cold storage, spread across executives and locations |

Multisig turns "whoever steals the key gets everything" into "an attacker must compromise several people in different places at once" — security by arithmetic rather than by trust.

---

## <font color="#388bfd">Bitcoin Layer 2: payment networks</font>

Bitcoin confirms a block roughly every 10 minutes and charges a market-rate fee for block space. That is fine for moving your savings — and hopeless for buying a $3 coffee. **Layer 2 payment networks** (the Lightning Network is the famous one) fix this by taking small payments *off* the chain:

```
ON-CHAIN                      OFF-CHAIN (fast, free-ish)                ON-CHAIN
open a channel:               update the balance as often as you like:  close the channel:
Alice + Bob lock              Alice 0.010 | Bob 0.000                   one final tx settles
0.010 BTC into a       --->   Alice 0.007 | Bob 0.003   (coffee!)  ---> Alice 0.005 | Bob 0.005
shared 2-of-2 address         Alice 0.005 | Bob 0.005   (again!)        back on the chain
      1 transaction                  0 transactions                        1 transaction
```

- **Opening a channel** is one on-chain transaction that locks funds into a shared multisig address — there is the multisig idea, immediately put to work.
- While the channel is open, Alice and Bob exchange **signed balance updates** directly, instantly, thousands of times if they like. Nothing touches the blockchain.
- **Closing the channel** is one final on-chain transaction that records the ending balances.

The blockchain remains the court of final settlement (either party can always close the channel and take what the latest signed update says is theirs), but the everyday traffic happens above it — a second *layer*. Channels connected to channels form a network: Alice can pay Carol through Bob without ever opening a channel to Carol directly.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you generate an RSA keypair by hand from `p = 5` and `q = 11`, ending with the public and private keys?
- [ ] Can you say which key encrypts and which key decrypts when sending a secret message?
- [ ] Can you explain what "2-of-3" means for a multisig wallet?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you encrypt the message `m = 7` with the public key `(3, 55)` and show the ciphertext is 13?
- [ ] Can you explain why publishing `(e, n)` does not reveal `d` for real-sized keys?
- [ ] Can you describe the three phases of a payment channel and which ones touch the blockchain?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain how the same RSA math produces signatures when run with the keys swapped?
- [ ] Can you design a multisig setup for a family emergency fund and justify your choice of m and n?
- [ ] Can you explain why Layer 2 payments stay honest even though the blockchain never sees them?

---

[Assignment](ASSIGNMENT.md)

← [Mempool and Wallet Programming](../MempoolAndWalletProgramming/) — Next: [Smart Chains and Wrapped Bitcoin](../SmartChainsAndWrappedBitcoin/)
