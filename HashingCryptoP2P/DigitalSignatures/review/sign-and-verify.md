# Review — Keys, Signing, and Verifying

*Originally covered in [Digital Signatures](../README.md)*

---

| Step | Command / rule |
|---|---|
| Generate key pair | `python3 generate_keys.py` → `public_key.txt` + `private_key.txt` |
| Sign | `python3 sign_message.py "message"` → hash the message, encrypt hash with **private** key |
| Verify | `python3 verify_signature.py "message" SIGNATURE` → recompute hash, decrypt signature with **public** key, compare |
| Share | public key, message, signature — never the private key |

| Guarantee | Meaning |
|---|---|
| Authentication | Sender is who they claim |
| Non-repudiation | Sender cannot deny sending |
| Integrity | Message unaltered (hash match) |

Hash refresher: SHA-256 digest = 256 bits = 64 hex characters; 1 hex digit = 4 bits.

---

## Tasks

1. Generate a fresh key pair and identify which printed number appears in *both* key files, and which numbers appear in neither.
2. Sign the message `practice makes permanent` and record the signature number.
3. Verify the exact message with your signature — confirm `VALID`.
4. Verify `Practice makes permanent` (capital P) with the same signature — explain the result using one of the four hash properties from [Hexadecimal and Hashing](../../HexadecimalAndHashing/README.md).
5. Without running anything, state how many hex characters the SHA-256 digest printed in step 2 had, and how many bits that represents.
