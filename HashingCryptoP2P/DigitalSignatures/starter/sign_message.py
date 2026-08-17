# sign_message.py — sign a message with your toy RSA private key.
#
# WHAT THIS SCRIPT TEACHES
# A digital signature is NOT the message scrambled. It is the message's
# HASH, encrypted with your private key. Anyone holding your public key can
# decrypt the signature back into that hash and compare it against a hash
# they compute themselves — if the two match, the message really came from
# you and was not altered.
#
# HOW TO RUN (after generate_keys.py has created private_key.txt)
#   python3 sign_message.py                 — prompts you for a message
#   python3 sign_message.py "your message"  — signs the given message
#
# This is a teaching toy. Never use it to protect anything real.

import hashlib
import sys


def read_private_key():
    # The private key file holds two labeled numbers: the shared modulus and
    # your secret private exponent. We read them back into integers.
    key_values = {}
    with open("private_key.txt") as private_key_file:
        for key_line in private_key_file:
            label, value = key_line.split(":")
            key_values[label.strip()] = int(value.strip())
    return key_values["modulus"], key_values["private_exponent"]


def hash_message_to_integer(message_text, modulus):
    # The question: why sign the hash instead of the message itself?
    # The answer: a hash squeezes a message of ANY length into one
    # fixed-size number, and hashing is fast. Signing that short fingerprint
    # is much cheaper than signing a whole document — and just as binding,
    # because any change to the message changes its hash completely.
    message_hash_hex = hashlib.sha256(message_text.encode("utf-8")).hexdigest()

    # SHA-256 produces a 256-bit number — far larger than our toy modulus.
    # RSA can only work on numbers smaller than the modulus, so we reduce
    # the hash with mod. Real RSA instead uses a large modulus plus a
    # careful PADDING scheme (extra structured bytes wrapped around the
    # hash) — padding keeps the security proof intact in ways plain mod
    # does not. Toy scale: mod is enough to see the idea.
    message_hash_integer = int(message_hash_hex, 16) % modulus
    return message_hash_hex, message_hash_integer


def create_signature(message_hash_integer, private_exponent, modulus):
    # The question: what does "encrypt with the private key" actually mean?
    # The answer: raise the hash to the private exponent, mod the modulus.
    # Only the matching public exponent can raise the result back to the
    # original hash — that reversal is the verification step.
    # pow(base, exponent, modulus) is Python's fast built-in for exactly
    # this "raise and take the remainder" operation.
    return pow(message_hash_integer, private_exponent, modulus)


def main():
    modulus, private_exponent = read_private_key()

    if len(sys.argv) > 1:
        message_text = sys.argv[1]
    else:
        message_text = input("Message to sign: ")

    message_hash_hex, message_hash_integer = hash_message_to_integer(
        message_text, modulus)
    signature = create_signature(message_hash_integer, private_exponent, modulus)

    print()
    print("=== Signing complete ===")
    print(f"Message:                {message_text}")
    print(f"SHA-256 of message:     {message_hash_hex}")
    print(f"Hash mod modulus:       {message_hash_integer}")
    print(f"Signature:              {signature}")
    print()
    print("Send your partner three things: the message text, the signature")
    print("number, and your public_key.txt. Keep private_key.txt to yourself.")


if __name__ == "__main__":
    main()
