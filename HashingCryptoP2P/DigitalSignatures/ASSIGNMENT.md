# Assignment — Digital Signatures

**Due:** Next class  
**Points:** 50

---

## Part 1 — Set Up

1. Confirm Python 3 is installed:

```bash
python3 --version
```

If the command is not found, install Python 3 from [python.org](https://www.python.org/downloads/) (or see [Computer Setup](../../ComputerSetup/) for your machine's setup guide).

2. Get the three scripts from this lesson's [starter/](starter/) folder onto your machine (clone or download this repository), and open a terminal in that folder.

---

## Part 2 — Generate Keys and Sign Your Own Message

3. Generate your key pair and read every printed step:

```bash
python3 generate_keys.py
```

This writes `public_key.txt` (shareable) and `private_key.txt` (never share it).

4. Sign a message of your own — write your own sentence, at least five words:

```bash
python3 sign_message.py "your own message here"
```

Record the message text and the signature number it prints.

5. Verify your own signature to confirm the round trip:

```bash
python3 verify_signature.py "your own message here" YOUR_SIGNATURE_NUMBER
```

You must see `VALID`.

---

## Part 3 — Verify a Partner's Message

6. Exchange with a partner: send them your message text, your signature number, and your `public_key.txt`. Receive the same three things from them.
7. Replace the `public_key.txt` in your folder with **your partner's** (save yours elsewhere first), then verify their message:

```bash
python3 verify_signature.py "partner's message" PARTNER_SIGNATURE_NUMBER
```

8. Now change one character of their message and verify again — confirm the verifier reports `TAMPERED`.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Python 3 runs** — `python3 --version` prints a version number
- [ ] **Key pair generated** — `public_key.txt` and `private_key.txt` both exist in your folder
- [ ] **Own message signed and verified** — your original sentence verifies as `VALID` with your own public key
- [ ] **Partner's message verified** — their message and signature verify as `VALID` using *their* public key
- [ ] **Tampering detected** — the one-character-changed version of their message reports `TAMPERED`
- [ ] **Private key never shared** — at no point did `private_key.txt` leave your machine

---

## Submission

Submit **one file** and **one text response** on Canvas.

### File

Upload your `public_key.txt` (the file `generate_keys.py` created — the one that is safe to share).

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
My message text:               
My signature number:           
My verification result:        
Partner's name:                
Partner's message text:        
Partner's signature number:    
Partner verification result:   
Tampered verification result:  
```

> **Note:**
> If any verification printed `TAMPERED` when you expected `VALID`, check that the message text matches character-for-character (including spaces and punctuation) and that the right person's `public_key.txt` is in the folder.
