<div align="center">

# Peer-to-Peer Networks
*<font color="#8b949e">How strangers' computers share files with no server in the middle</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Review: Public and Private Keys](#review-public-and-private-keys)**  
The key-pair idea from last lesson, in three sentences.

**[Where Do Downloads Come From?](#where-do-downloads-come-from)**  
The client-server model that runs most of the internet.

**[Client-Server vs Peer-to-Peer](#client-server-vs-peer-to-peer)**  
Two shapes of network, and what each is good at.

**[The Torrent Protocol](#the-torrent-protocol)**  
Trackers, seeders, leechers, pieces — and hashing as the trust layer.

**[Why P2P Survives Losing Nodes](#why-p2p-survives-losing-nodes)**  
No single point of failure.

**[Legality and Ethics](#legality-and-ethics)**  
The technology is neutral; what you share with it is not.

**[Optional Activity: Watch a Swarm](#optional-activity-watch-a-swarm)**  
Download a Linux distribution over BitTorrent and watch the protocol work.

---

## <font color="#388bfd">Review: Public and Private Keys</font>

From [last lesson](../DigitalSignatures/): a key pair is manufactured so that whatever one key locks, only the other unlocks. You publish the public key and guard the private key, so anyone can *verify* your signature but no one can *forge* it. Keep that idea nearby — in a network with no one in charge, signatures and hashes are the only reasons to trust anything you receive.

---

## <font color="#388bfd">Where Do Downloads Come From?</font>

When you download an app, stream a video, or load this page, your computer is a **client** asking a **server** — a computer owned by some company — to send the data. This is the **client-server model**, and it runs most of the internet:

```
                 ┌────────┐
   request  →    │        │    ← request
  ┌────────┐     │ SERVER │     ┌────────┐
  │ client │ ←── │        │ ──→ │ client │
  └────────┘     └────────┘     └────────┘
                    ↑ ↓
                 ┌────────┐
                 │ client │
                 └────────┘
```

Every byte flows through the center. That gives the company control (they can update, secure, and bill for the service) — and it also makes the server a **single point of failure**. If it goes down, is overloaded, or gets shut off, every client loses access at once. And the more clients arrive, the more bandwidth the server must buy.

---

## <font color="#388bfd">Client-Server vs Peer-to-Peer</font>

A **peer-to-peer (P2P)** network removes the center. Every participant — every **peer** — is both a client *and* a server, downloading from some peers while uploading to others:

```
  ┌──────┐ ←──→ ┌──────┐
  │ peer │      │ peer │
  └──────┘ ←┐ ┌→└──────┘
     ↕       ╳      ↕
  ┌──────┐ ←┘ └→┌──────┐
  │ peer │      │ peer │
  └──────┘ ←──→ └──────┘
```

| | Client-server | Peer-to-peer |
|---|---|---|
| Who holds the data | The central server | Spread across many peers |
| What happens as users join | Server load grows — service slows or costs rise | More uploaders join — the network gets *faster* |
| Single point of failure | Yes — the server | No — any peer can vanish |
| Who is in charge | The server's owner | No one |
| Trust comes from | Trusting the company | Verifying the data itself (hashes, signatures) |

That last row is why this unit taught hashing first. With no company in the middle vouching for the data, the data must vouch for itself.

---

## <font color="#388bfd">The Torrent Protocol</font>

**BitTorrent** is the most famous P2P protocol. Here is how downloading one large file from a crowd of strangers actually works:

### <font color="#79c0ff">The cast</font>

| Term | Role |
|---|---|
| **Torrent file / magnet link** | A tiny description of the real file: its name, size, how it is split into pieces, and the **hash of every piece** |
| **Tracker** | A coordinator that introduces peers to each other — "here are the addresses of others sharing this file." It never stores the file itself |
| **Seeder** | A peer with the **complete** file, uploading to others |
| **Leecher** | A peer still downloading — it has some pieces and is fetching the rest (while uploading the pieces it already has) |
| **Swarm** | Everyone — seeders and leechers — sharing one particular file |

### <font color="#79c0ff">The process</font>

1. The file is split into hundreds or thousands of small **pieces**.
2. You open the torrent file and contact the tracker, which hands you a list of peers in the swarm.
3. You download different pieces from different peers simultaneously — piece 12 from one stranger, piece 847 from another — in whatever order peers can supply them.
4. **Every arriving piece is hashed, and the hash is compared against the expected hash from the torrent file.** Match → keep the piece. Mismatch → throw it away and fetch it from someone else.
5. As soon as you hold *any* complete piece, you start uploading it to other leechers. When you have every piece, you become a seeder.

> **Note:**
> Step 4 is last lesson's ideas doing real work. You just accepted data from complete strangers who could have sent you anything — corrupted data, malware, garbage — and it did not matter, because every piece had to match a known hash to be accepted. The trust is in the math, not in the peers.

---

## <font color="#388bfd">Why P2P Survives Losing Nodes</font>

Shut down a central server and its service dies instantly. Shut down a peer in a swarm and… nothing happens. Every piece of the file exists on many machines, so the remaining peers keep exchanging pieces and any newcomer can still assemble the whole file. Even the tracker is dispensable in modern BitTorrent — peers can find each other through a distributed hash table (DHT), a phone book that is *itself* spread across the peers.

This resilience is not an accident; it is the design goal. A network with no center has nothing to overload, nothing to seize, and no single owner whose failure — or decision — can switch it off. Bitcoin and other blockchain networks (next unit: [Blockchains and Bitcoin](../../Blockchains/)) are P2P for exactly this reason: thousands of peers each hold a copy of the ledger, so no government, company, or outage can take the ledger down.

---

## <font color="#388bfd">Legality and Ethics</font>

P2P technology is legal and widely used for legitimate work — Linux distributions ship over BitTorrent, game companies push updates with it, and scientific datasets are mirrored through it.

But the same properties that make P2P resilient also made it the engine of media piracy. Sites exist that stream or torrent current movies and TV for free — copies shared peer-to-peer with no permission from the people who made them. Their names change constantly because they are repeatedly shut down and resurrected under new domains — a cat-and-mouse game the resilience of P2P makes possible.

Be clear about the line:

- **The protocol is neutral.** Downloading a Linux distribution over BitTorrent is legal everywhere.
- **Sharing copyrighted work without permission is not.** It is copyright infringement regardless of how effortless the technology makes it, and using such sites also routinely exposes you to malware and scams.
- **Uploading is part of the deal.** Remember step 5: a torrenting peer *redistributes* pieces while downloading. With copyrighted material, you would not just be taking a copy — you would be distributing it to strangers.

> **Warning:**
> On school networks and school machines, only ever torrent content you have a clear legal right to share, such as open-source software. This lesson teaches you how the machinery works precisely so you can reason about what it is being used for.

---

## <font color="#388bfd">Optional Activity: Watch a Swarm</font>

If you want to see the protocol live (on your own machine, not required):

1. Install a reputable torrent client such as [Transmission](https://transmissionbt.com/) or [qBittorrent](https://www.qbittorrent.org/).
2. Get the official torrent for a Linux distribution — Ubuntu publishes theirs at [ubuntu.com/download/alternative-downloads](https://ubuntu.com/download/alternative-downloads).
3. While it downloads, open the client's peers/details view and find: the number of **seeders** and **leechers**, the **pieces** display filling in out of order, and your own **upload** counter rising.
4. When it finishes, notice your client keeps uploading — you are now a seeder. Verify the finished file: the download page lists its SHA-256 checksum, so hash your copy and compare.
5. Delete the file (or install Linux in a virtual machine, if you are curious).

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you describe the client-server model and name what happens to it when the server goes down?
- [ ] Can you define seeder, leecher, and tracker in one sentence each?
- [ ] Can you state what a torrent file contains, and what it does *not* contain?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain how a downloader verifies a piece received from an untrusted stranger?
- [ ] Can you explain why a P2P network gets faster as more users join, while a client-server service gets slower?
- [ ] Can you trace what happens in a swarm when a seeder suddenly disconnects?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why piece-level hash verification means peers never need to be trusted?
- [ ] Can you argue where the legal and ethical line sits in P2P file sharing, using the uploading-while-downloading fact?
- [ ] Can you predict which properties of P2P networks a cryptocurrency needs and why a central server would defeat its purpose?

---

← [Digital Signatures](../DigitalSignatures/) — Back to [Hashing, Cryptography, and P2P Networks](../)
