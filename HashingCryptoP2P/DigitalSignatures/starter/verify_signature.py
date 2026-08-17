# verify_signature.py — check a (message, signature) pair against a public key.
#
# WHAT THIS SCRIPT TEACHES
# Verification never touches the private key. Given a message, a signature,
# and the signer's PUBLIC key, the verifier computes two numbers
# independently:
#   1. the hash of the message, recomputed from scratch, and
#   2. the signature decrypted with the public key.
# If the signer was genuine and the message untouched, the two numbers are
# identical. If even one character of the message changed — or the signature
# was made with a different private key — they will not match.
#
# HOW TO RUN (with the signer's public_key.txt in this folder)
#   python3 verify_signature.py                          — prompts you
#   python3 verify_signature.py "message" signature      — checks directly
#
# This is a teaching toy. Never use it to protect anything real.

import hashlib
import sys


def read_public_key():
    # The public key file holds the shared modulus and the public exponent.
    # If you are verifying a PARTNER's message, this must be THEIR
    # public_key.txt — copy it into this folder first.
    key_values = {}
    with open("public_key.txt") as public_key_file:
        for key_line in public_key_file:
            label, value = key_line.split(":")
            key_values[label.strip()] = int(value.strip())
    return key_values["modulus"], key_values["public_exponent"]


def hash_message_to_integer(message_text, modulus):
    # The question: how does the verifier know what hash to expect?
    # The answer: by hashing the message again, from scratch, using the
    # EXACT same rule the signer used (SHA-256, then mod the modulus).
    # Hashes are deterministic — same input, same output, on any computer.
    message_hash_hex = hashlib.sha256(message_text.encode("utf-8")).hexdigest()
    message_hash_integer = int(message_hash_hex, 16) % modulus
    return message_hash_hex, message_hash_integer


def decrypt_signature(signature, public_exponent, modulus):
    # The question: how can a PUBLIC number undo a PRIVATE one?
    # The answer: the two exponents were manufactured as a matched pair —
    # raising to one and then the other (mod the modulus) returns the
    # starting number. The signer raised the hash to the private exponent;
    # raising the signature to the public exponent brings the hash back.
    return pow(signature, public_exponent, modulus)


def main():
    modulus, public_exponent = read_public_key()

    if len(sys.argv) > 2:
        message_text = sys.argv[1]
        signature = int(sys.argv[2])
    else:
        message_text = input("Message to verify: ")
        signature = int(input("Signature number:  "))

    message_hash_hex, recomputed_hash = hash_message_to_integer(
        message_text, modulus)
    recovered_hash = decrypt_signature(signature, public_exponent, modulus)

    print()
    print("=== Verification ===")
    print(f"Message:                        {message_text}")
    print(f"SHA-256 of message:             {message_hash_hex}")
    print(f"Recomputed hash (mod modulus):  {recomputed_hash}")
    print(f"Signature decrypted with key:   {recovered_hash}")
    print()
    if recomputed_hash == recovered_hash:
        print("VALID — the two numbers match. This message was signed by the")
        print("holder of the matching private key and has not been altered.")
    else:
        print("TAMPERED — the two numbers differ. Either the message was")
        print("changed after signing, or the signature was not made with the")
        print("private key that matches this public key.")


if __name__ == "__main__":
    main()
