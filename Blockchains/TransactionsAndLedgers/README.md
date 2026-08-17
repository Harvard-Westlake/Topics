<div align="center">

# Transactions and Ledgers
*<font color="#8b949e">Build a shared ledger with your class, then make its history unchangeable</font>*

<font color="#a371f7">Learning</font>

</div>

---

Nothing is due today, but there is a small assignment at the end of class. Today we build the idea of a blockchain from the ground up, using three parts you already own from [Hashing, Cryptography, and P2P Networks](../../HashingCryptoP2P/):

1. **Hashing** — a unique number for the contents of a file
2. **How banks process transactions** — what actually happens when you tap a card
3. **P2P file sharing** — the whole class keeping the same file in sync, with no server

Put together, we will do something banks cannot: save a list of transactions so that it can **never be changed**, make saving it *a little difficult*, and reward the people who do the saving.

---

## <font color="#388bfd">New vocabulary</font>

### <font color="#79c0ff">Ledger</font>

A **ledger** is a book or digital file where financial transactions are recorded in detail. It provides a complete record of accounts — assets, liabilities, income, and expenses. Every bank keeps one. Today, so will we.

### <font color="#79c0ff">Transaction</font>

A **transaction** is an agreement between a buyer and a seller to exchange goods, services, or financial assets for payment. It changes the financial position of at least two parties, and it gets recorded in a ledger.

You have watched a transaction get processed hundreds of times. When you pay with a debit or credit card, what does the little card-reader screen say?

| Step | Card reader says | What it means |
|---|---|---|
| 1 | *Insert card* | Identify who is paying |
| 2 | *Confirm $15.63 charge?* | Both parties agree to the exchange |
| 3 | *Pending* | The transaction is announced, but not yet recorded |
| 4 | *Confirmed* (or *Declined*) | The bank has written it into — or rejected it from — the ledger |

Hold on to that word **pending**. A transaction that has been announced but not yet permanently recorded is the single most important idea in this whole module.

---

## <font color="#388bfd">In-class activity: a peer-to-peer ledger</font>

Let's create a ledger and share it over a P2P network — the same way a torrent shares a file. Everyone opens a plain text file, and **we all MUST keep the same copy of the ledger**.

Any person can initiate a transaction from themselves to someone else. Pretend you all have money. Who wants to send transactions to whom?

```
Mr. Theiss -> Mr. Lopez  4.30
Riley -> Anna  1500
Jake -> Mr. Lopez  301.34
```

Now two questions:

1. Is there a way to make sure the pending transactions we wrote down can **never be changed**?
2. Is there some way to represent all of this data as a single, unique number?

Yes — hashing, from last unit! Paste the ledger into an [online SHA-256 tool](https://emn178.github.io/online-tools/sha256.html) and every person in the room should get the **exact same hash**. If even one character of one transaction differs on your copy, your hash will not match the room's.

Let's format the file a little more nicely:

```
// Transactions:
Mr. Theiss -> Mr. Lopez  4.30
Riley -> Anna  1500
Jake -> Mr. Lopez  301.34

// Confirmation #:
a91b3c...   (the SHA-256 hash of the transactions above)
```

---

## <font color="#388bfd">Linking one file to the next</font>

The class ledger file is now "full" — we agreed on its contents and its hash. So we start a **new file** for the next batch of transactions. Here is the move that makes everything work: **copy the previous file's hash into the top of the new file.**

```
FILE 1                        FILE 2                        FILE 3
+---------------------+       +---------------------+       +---------------------+
| prev hash: (none)   |       | prev hash: a91b3c...|       | prev hash: 7fe210...|
|                     |  +--> |                     |  +--> |                     |
| Theiss -> Lopez 4.30|  |    | Anna -> Jake 12.00  |  |    | Riley -> Theiss 3.5 |
| Riley -> Anna 1500  |  |    | Lopez -> Riley 88.8 |  |    | Jake -> Anna 40.00  |
|                     |  |    |                     |  |    |                     |
| hash: a91b3c...  ---+--+    | hash: 7fe210...  ---+--+    | hash: c04d99...     |
+---------------------+       +---------------------+       +---------------------+
```

Each new file **links** to the previous file by containing its hash. Try to tamper with File 1 — change Riley's 1500 to 15 — and File 1's hash changes, so the "prev hash" written inside File 2 no longer matches, so File 2's hash changes, so File 3's link breaks too. To rewrite one old transaction you would have to rewrite *every file after it*, on *every classmate's computer*, before anyone noticed.

We have been deliberately saying **link** and **file**. Say it back the other way: a *chain* of *files*. Other people call the files *blocks*. You have just built a **blockchain** — and the moment you realize how simple it is, you own the idea for good.

> **Note:**
> This is also what "mining a block" means at its core: gathering the pending transactions, adding the previous hash, and producing the new file's hash. Bitcoin adds two twists you will meet next lesson — the hash must be *difficult* to produce, and whoever produces it gets *rewarded*.

---

## <font color="#388bfd">Real chains, real code: Bitcoin vs Litecoin</font>

A blockchain's personality — how fast it saves files, how big the reward is, how much currency will ever exist — is decided by a few numbers in its source code. Both Bitcoin and Litecoin are open source, and both keep those numbers in a file called `chainparams.cpp`:

- Bitcoin: [chainparams.cpp](https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp)
- Litecoin: [chainparams.cpp](https://github.com/litecoin-project/litecoin/blob/8dc9bc09aee10315679c6b6b1ef55881c57d0e34/src/chainparams.cpp)

Compare them and discuss the network itself:

| Question | Bitcoin | Litecoin |
|---|---|---|
| **Block reward** — what do you get for saving a block? | Started at 50 BTC, halves every 210,000 blocks | Started at 50 LTC, halves every 840,000 blocks |
| **Currency limit** — how much will ever exist? | 21 million BTC | 84 million LTC |
| **Block creation time** — how often is a file saved? | ~10 minutes | ~2.5 minutes |

> **Tip:**
> Notice that Litecoin is mostly Bitcoin's code with different numbers. Because the code is public, anyone can read the rules — and anyone can copy them and change the parameters. What they *cannot* do is quietly change the rules of a network other people are already running.

Today we stayed consciously on blockchain technology itself — the ledger, the links, the parameters — and off every other crypto topic. The rest of the module builds on exactly this foundation.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you define a ledger and a transaction in your own words?
- [ ] Can you list the four steps a card reader walks through, and say which step means "announced but not yet recorded"?
- [ ] Can you take the SHA-256 hash of a small text file and confirm a classmate gets the same hash from the same text?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain why every participant in the class ledger activity must hold an identical copy of the file?
- [ ] Can you describe, step by step, how linking each new file to the previous file's hash is done?
- [ ] Can you find the block reward and block creation time in a `chainparams.cpp` file on GitHub?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain exactly which hashes break, and in what order, if someone edits a transaction three files back?
- [ ] Can you explain why the words "link" and "file" describe the same thing as "chain" and "block"?
- [ ] Can you argue why an attacker would need to out-edit the entire room to rewrite history in a P2P ledger?

---

[Assignment](ASSIGNMENT.md)

← Back to [Blockchains and Bitcoin](../) — Next: [Bitcoin and Wallets](../BitcoinAndWallets/)
