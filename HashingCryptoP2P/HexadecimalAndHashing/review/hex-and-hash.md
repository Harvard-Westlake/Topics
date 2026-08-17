# Review — Hex Conversions and Hash Properties

*Originally covered in [Hexadecimal and Hashing](../README.md)*

---

| Conversion | Method |
|---|---|
| Hex → binary | Each hex digit → its 4-bit group (`A` = `1010`) |
| Binary → hex | Group bits in fours from the right, pad left with zeros |
| Hex → decimal | Place values 1, 16, 256, … (`1A3` = 256 + 160 + 3 = 419) |
| Decimal → hex | Divide by 16, keep remainders (255 = `FF`) |

| Hash property | One-liner |
|---|---|
| Deterministic | Same input → same output, always |
| Fast | Quick to compute for any input |
| Pre-image resistant | Cannot work backward from hash to input |
| Collision resistant | Cannot find two inputs with the same hash |

Toy hash: `hash(x) = (x × 256) mod 100` — e.g. `hash(5) = 1280 mod 100 = 80`

---

## Tasks

1. Convert `C8` to decimal by hand, then to binary using 4-bit groups.
2. Convert the binary number `10011110` to hex, then to decimal.
3. Compute `hash(17)` with the toy hash. Show both steps.
4. Name the hash property the toy hash breaks, and prove it by producing two inputs with the same output.
5. Hash the string `hw` with the [SHA-256 tool](https://emn178.github.io/online-tools/sha256.html), then state which hash property guarantees a classmate hashing `hw` gets the identical digest.
