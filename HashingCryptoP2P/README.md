<div align="center">

# Hashing, Cryptography, and P2P Networks
*<font color="#8b949e">Fingerprints, secret-free proofs, and networks with no one in charge</font>*

<font color="#a371f7">Learning</font>

</div>

---

Every time you log in, download a file, or send a message, three quiet ideas are working underneath — the foundation stones of digital trust.

The first is **hashing**: a single number can fingerprint anything. Feed a hash function a password, a photo, or a thousand-page book, and it returns a short fixed-size code that changes completely if even one character of the input changes. That fingerprint is how computers detect tampering without ever comparing the originals.

The second is **digital signatures**: math lets you prove who you are without revealing your secret. A public/private key pair is manufactured so that whatever one key locks, only the other can unlock — so you can sign a message with a key nobody ever sees, and anyone in the world can verify it was really you.

The third is **peer-to-peer networks**: strangers' computers can cooperate without any central server. When there is no company in the middle to trust, hashing verifies every piece of data and no single machine's failure can take the network down.

These three ideas are worth learning on their own — and they are also the exact parts that the [Blockchains and Bitcoin](../Blockchains/) unit will later assemble into a working cryptocurrency.

---

## <font color="#388bfd">Lessons</font>

| # | Lesson | What you'll learn |
|---|---|---|
| 1 | [Hexadecimal and Hashing](HexadecimalAndHashing/) | Base-16 numbers, converting between binary/decimal/hex, the four properties of hash functions, and how hashing differs from encryption |
| 2 | [Digital Signatures](DigitalSignatures/) | Public/private key pairs, signing a message's hash with a private key, and verifying a partner's signature with their public key |
| 3 | [Peer-to-Peer Networks](PeerToPeerNetworks/) | Client-server vs peer-to-peer, how the torrent protocol splits and hash-verifies files, and why P2P networks survive losing nodes |

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you name the three ideas this unit covers and give a one-sentence description of each?
- [ ] Can you explain what it means for a hash to "fingerprint" a file?
- [ ] Can you state which of the two keys in a key pair must stay secret?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain why a signature made with a private key can be checked by anyone, but forged by no one?
- [ ] Can you describe one thing a peer-to-peer network can do that a single central server cannot?
- [ ] Can you explain how hashing lets a downloader detect a tampered file without seeing the original?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you predict which of the three ideas a cryptocurrency needs, and what job each one would do?
- [ ] Can you explain why "trust the math" can replace "trust the company in the middle"?
- [ ] Can you argue which of the three ideas would be hardest to remove from a blockchain and still have it work?
