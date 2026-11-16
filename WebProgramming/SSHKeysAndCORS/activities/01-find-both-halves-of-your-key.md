# Activity - Find Both Halves of Your Key

*Concept: Look at the key pair already on your computer, and prove it works by logging in to GitHub with no password.*

![A terminal on your own computer. Listing the .ssh folder shows four files: id_ed25519, the private key that never leaves this computer, id_ed25519.pub, the public key that is safe to hand to anyone, known_hosts, the fingerprints of servers you said yes to, and config, nicknames for the servers you log in to. Printing id_ed25519.pub shows one line of text: the kind of key, the key itself, and a label.](../assets/key-files.svg)

## Task

1. In your terminal, on your own computer, list your key folder:
   ```bash
   ls -1 ~/.ssh
   ```
2. Find the two files with the same name. Say which is the private half and which is the public half.
3. In your terminal, print the public half. It is one long line:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
4. Do not print the other file. Say out loud why not.
5. In your terminal, prove the pair works. GitHub has held your public half since setup day:
   ```bash
   ssh -T git@github.com
   ```
6. GitHub greeted you by name and never asked for a password. Say what your computer sent instead.
