<div align="center">

# Bitcoin and Wallets
*<font color="#8b949e">How the network confirms blocks, and what owning a wallet actually means</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Review: what we built last time</font>

Users sit in a P2P network. They initiate transactions by **announcing** them to the network. The network verifies the transactions, and once verified, the *block* of transactions is complete and added as another node in a linked list:

```
announce            verify              append
[ users ]  ---->  [ network ]  ---->  block N-2 <-- block N-1 <-- block N
                                       (each block holds the previous block's hash)
```

The network does the verifying with **hashes** — but with a twist we skipped last lesson.

---

## <font color="#388bfd">Hash difficulty: making saving hard on purpose</font>

Anyone can hash a file in a millisecond, so what stops a bad actor from instantly producing thousands of alternative histories? Bitcoin sets a **hash difficulty**: a block's hash only counts if it starts with a required number of zeros. Since hash output is unpredictable, the only way to get such a hash is to keep tweaking a throwaway number in the block and re-hashing — billions of times. Finding one is like winning a lottery you can only enter by doing work.

```
try:  hash(block + 1)  = 8f31ac...   no
try:  hash(block + 2)  = 44b0e9...   no
try:  hash(block + 3)  = 000000c4... YES - difficulty met, block confirmed!
```

Once a hash with the required difficulty is found, the block's transactions are **confirmed** — and here is the reward from last lesson's outline: **new bitcoin is created (minted) and given to the producer of the block.** That is the entire supply schedule of Bitcoin: money is only ever created as payment for saving history.

---

## <font color="#388bfd">Going deeper</font>

### <font color="#79c0ff">Minting</font>

Minting is the creation of new currency. In Bitcoin, minting happens only in the block reward, the reward halves on a fixed schedule, and the total is capped at 21 million — all enforced by the code everyone runs.

### <font color="#79c0ff">Transaction fees</font>

- A fee buys **space in a block** — block space is limited, so it is a market.
- Users can **offer** a higher fee to incentivize miners to include their transaction sooner.
- On February 16, 2024, the average transaction fee was **$5.664**.
- You can estimate a good fee from current network usage and state — busy network, higher fees.

### <font color="#79c0ff">Block size</font>

Blocks were originally capped at **1 MB**; upgrades have raised the effective limit to about **4 MB**. Bigger blocks fit more transactions but make the chain heavier to store and share.

### <font color="#79c0ff">Processing time</font>

Bitcoin saves a block roughly every **10 minutes**, so a transaction can take that long (or longer, if you underpaid on fees) to confirm. Other coins choose different speeds — recall Litecoin's ~2.5 minutes from last lesson.

### <font color="#79c0ff">Bitcoin philosophy</font>

- **Permissionless** — nobody can stop you from participating, and you need nobody's approval.
- **~10 minutes per block** — a deliberately calm pace that keeps the network verifiable by ordinary computers worldwide.

---

## <font color="#388bfd">Quick exercise (offline)</font>

Work these with pencil and paper — no explorer allowed:

1. Roughly how many blocks have been mined right now? (~830,000 as of early 2024)
2. If we are at block 830,000 right now, about when did the chain start?
3. If the block size is 4 MB, what is the largest the Bitcoin blockchain could possibly be when it reaches block 1,000,000?

Work them before peeking:

> **Note:**
> **2.** 830,000 blocks × 10 minutes = 8.3 million minutes ≈ 5,760 days ≈ **15.8 years** — counting back from early 2024 estimates a 2008 start. The real genesis block was January 3, 2009; blocks have averaged slightly under 10 minutes, so the estimate overshoots a little. **3.** 1,000,000 × 4 MB = 4,000,000 MB = **4 TB** at absolute most — small enough that ordinary people can still store the whole history, which is the point.

---

## <font color="#388bfd">Code comparison: open source, "code is law"</font>

Bitcoin's rules are not enforced by a government or company — they are enforced by open-source code that every participant runs. If the code allows it, it happens; if not, it does not. That is what people mean by **code is law**. Compare the two rulebooks (pinned versions, so the line numbers stay put):

- Bitcoin: [chainparams.cpp](https://github.com/bitcoin/bitcoin/blob/f47dda2c58b5d8d623e0e7ff4e74bc352dfa83d7/src/chainparams.cpp)
- Litecoin: [chainparams.cpp](https://github.com/litecoin-project/litecoin/blob/8dc9bc09aee10315679c6b6b1ef55881c57d0e34/src/chainparams.cpp)

### <font color="#79c0ff">Where keys come from: the BIP-39 wordlist</font>

Wallet keys start life as randomness, but humans are terrible at writing down randomness. So wallets encode it as a **mnemonic**: 12 (or 24) words drawn from a fixed, public list of 2048 English words — the [BIP-39 wordlist](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt). Those words *are* your key: anyone holding them holds your money. In class we demonstrated a small wallet-mnemonic generator that picks words from this exact list and derives the keys from them.

---

## <font color="#388bfd">Activity: create a wallet</font>

1. [Install a bitcoin wallet](https://www.okx.com/web3) (or another wallet your teacher approves).
2. Follow the wallet's setup flow to create a new wallet and **write down the seed phrase on paper**.
3. Understand the importance of the private key: the seed phrase and private key are the wallet. There is no "forgot password" link, and no support line can restore them.

> **Warning:**
> Never put real money into a class wallet, and never share your private key or seed phrase with **anyone** — not a classmate, not a website, not your teacher. Anyone who has the phrase has the money, permanently.

**Takeaway questions** — answer honestly from your own setup experience:

- Did I need to confirm I was 18+?
- Did I need to verify my phone number, or my identity?
- Am I in control of the money?
- Can I access this anywhere in the world?
- Does anyone else have access?

Compare your answers with what a bank account would require. That contrast *is* the permissionless philosophy from earlier in this lesson.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain what hash difficulty is and how a confirmed block's hash shows it?
- [ ] Can you state where new bitcoin comes from and what the total supply cap is?
- [ ] Can you name two things the wallet setup never asked you for that a bank would require?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain why offering a higher transaction fee gets you confirmed faster?
- [ ] Can you estimate Bitcoin's start date from a current block height and the 10-minute block time?
- [ ] Can you explain what the BIP-39 wordlist is and why a seed phrase must stay secret?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you compute the maximum possible chain size at block 1,000,000 and explain why keeping it small matters?
- [ ] Can you explain "code is law" using the two `chainparams.cpp` files as evidence?
- [ ] Can you argue both a benefit and a danger of a financial system with no identity checks and no support line?

---

← [Transactions and Ledgers](../TransactionsAndLedgers/) — Next: [Mempool and Wallet Programming](../MempoolAndWalletProgramming/)
