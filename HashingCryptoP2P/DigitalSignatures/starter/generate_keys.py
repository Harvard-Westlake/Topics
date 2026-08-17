# generate_keys.py — build a toy RSA key pair and watch every step of the math.
#
# WHAT THIS SCRIPT TEACHES
# A public key and a private key are not two random numbers. They are two
# numbers manufactured together from a pair of secret primes, linked so that
# whatever one key locks, only the other key can unlock. This script uses
# primes small enough to check by hand. Real RSA uses primes hundreds of
# digits long — the math is identical, only the sizes change.
#
# HOW TO RUN
#   python3 generate_keys.py
#
# It prints every intermediate value, then writes two files in this folder:
#   public_key.txt   — share this with anyone (post it, email it, shout it)
#   private_key.txt  — never share this with anyone
#
# This is a teaching toy. Never use it to protect anything real.

import math
import random

# The question: where do the keys come from?
# The answer: from two secret prime numbers. Everything else in RSA is
# computed from these two primes, so we start by picking them. Real systems
# pick random primes hundreds of digits long; we pick from a short menu of
# small primes so every number on screen stays readable.
PRIME_CHOICES = [53, 61, 71, 83, 89, 101, 103, 107, 109, 113,
                 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                 179, 181, 191, 193, 197, 199]


def choose_primes():
    # random.sample picks two DIFFERENT primes from the menu. The two primes
    # must differ — RSA's math breaks if they are equal.
    prime_one, prime_two = random.sample(PRIME_CHOICES, 2)
    return prime_one, prime_two


def choose_public_exponent(totient):
    # The question: what makes a number usable as the public exponent?
    # The answer: it must share no factors with the totient (their greatest
    # common divisor must be 1). If it shared a factor, no matching private
    # exponent would exist. We scan the odd numbers 3, 5, 7, ... and take
    # the first one that qualifies.
    candidate_exponent = 3
    while math.gcd(candidate_exponent, totient) != 1:
        candidate_exponent += 2
    return candidate_exponent


def find_private_exponent(public_exponent, totient):
    # The question: what number undoes the public exponent?
    # The answer: the private exponent is the number that makes
    #   (public_exponent * private_exponent) mod totient == 1.
    # That relationship is exactly what makes "lock with one key, unlock
    # with the other" work. Our primes are tiny, so we can afford to simply
    # try every candidate until one fits. Real systems use a faster method
    # (the extended Euclidean algorithm) because their totients are enormous.
    for candidate_exponent in range(2, totient):
        if (public_exponent * candidate_exponent) % totient == 1:
            return candidate_exponent
    raise ValueError("no private exponent exists — the public exponent "
                     "shares a factor with the totient")


def build_key_pair(prime_one, prime_two):
    # The question: how do two primes become two keys?
    # The answer: multiply them into the modulus (public), compute the
    # totient from them (secret), then derive the two exponents from the
    # totient. The modulus appears in BOTH keys; the two exponents are what
    # differ.
    modulus = prime_one * prime_two
    totient = (prime_one - 1) * (prime_two - 1)
    public_exponent = choose_public_exponent(totient)
    private_exponent = find_private_exponent(public_exponent, totient)
    return {
        "prime_one": prime_one,
        "prime_two": prime_two,
        "modulus": modulus,
        "totient": totient,
        "public_exponent": public_exponent,
        "private_exponent": private_exponent,
    }


def main():
    prime_one, prime_two = choose_primes()
    key_pair = build_key_pair(prime_one, prime_two)

    print("=== Toy RSA key generation ===")
    print()
    print("Step 1 — pick two secret primes.")
    print(f"  prime_one = {key_pair['prime_one']}")
    print(f"  prime_two = {key_pair['prime_two']}")
    print("  These two numbers are the deepest secret. Anyone who learns")
    print("  them can rebuild your private key.")
    print()
    print("Step 2 — multiply them into the modulus (this part goes public).")
    print(f"  modulus = {key_pair['prime_one']} * {key_pair['prime_two']}"
          f" = {key_pair['modulus']}")
    print("  Publishing the modulus is safe ONLY because splitting a big")
    print("  number back into its two primes is astronomically slow. With")
    print("  our tiny primes you could factor it in seconds — real RSA uses")
    print("  primes hundreds of digits long, and factoring those would take")
    print("  longer than the age of the universe.")
    print()
    print("Step 3 — compute the totient (stays secret).")
    print(f"  totient = ({key_pair['prime_one']} - 1) *"
          f" ({key_pair['prime_two']} - 1) = {key_pair['totient']}")
    print("  The totient can only be computed by someone who knows the")
    print("  primes. It is the bridge between the two exponents.")
    print()
    print("Step 4 — choose the public exponent.")
    print(f"  public_exponent = {key_pair['public_exponent']}")
    print("  The smallest odd number that shares no factors with the")
    print("  totient.")
    print()
    print("Step 5 — derive the private exponent.")
    print(f"  private_exponent = {key_pair['private_exponent']}")
    print(f"  Check: ({key_pair['public_exponent']} *"
          f" {key_pair['private_exponent']}) mod {key_pair['totient']} = "
          f"{(key_pair['public_exponent'] * key_pair['private_exponent']) % key_pair['totient']}")
    print("  That result of 1 is the whole trick: it is why raising a")
    print("  number to one exponent and then the other (mod the modulus)")
    print("  brings the original number back.")
    print()

    # The question: what actually goes in each key file?
    # The answer: both keys carry the shared modulus; they differ only in
    # which exponent they carry. The primes and totient are written to
    # NEITHER file — they did their job and must now be forgotten.
    with open("public_key.txt", "w") as public_key_file:
        public_key_file.write(f"modulus: {key_pair['modulus']}\n")
        public_key_file.write(f"public_exponent: {key_pair['public_exponent']}\n")
    with open("private_key.txt", "w") as private_key_file:
        private_key_file.write(f"modulus: {key_pair['modulus']}\n")
        private_key_file.write(f"private_exponent: {key_pair['private_exponent']}\n")

    print("Wrote public_key.txt  — share this freely.")
    print("Wrote private_key.txt — guard this with your life.")
    print()
    print("Next: python3 sign_message.py")


if __name__ == "__main__":
    main()
