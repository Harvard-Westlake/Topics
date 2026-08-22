<div align="center">

# Blockchains and Bitcoin
*<font color="#8b949e">From a shared file of IOUs to deploying your own currency</font>*

<font color="#a371f7">Learning</font>

</div>

---

This module builds the idea of a blockchain out of parts you already own. In [Hashing, Cryptography, and P2P Networks](../HashingCryptoP2P/) you learned that a hash is a unique fingerprint for a file, that a signature proves who wrote a message, and that a peer-to-peer network lets a whole room share the same data with no server in the middle. Here those three parts snap together.

We start with something almost embarrassingly simple: a shared text file of IOUs that the whole class keeps in sync. Then we ask one question — *how do we make sure nobody can quietly rewrite an old IOU?* — and the answer (put the previous file's hash at the top of the next file) turns out to be the entire trick. A chain of hash-linked files is a blockchain. Everything else in this module is what the world built on top of that trick: Bitcoin and its wallets, the mempool, cryptographic keys, smart contracts on Ethereum, and finally your own token — a real currency you write, deploy, and hand out to classmates on a real (test) blockchain.

> **Warning:**
> Every on-chain activity in this module uses **test networks** and play-money. Never put real money into a class wallet, and never share a private key or seed phrase with anyone — including your teacher.

---

## <font color="#388bfd">Lessons</font>

| # | Lesson | What you'll learn |
|---|---|---|
| 1 | [Transactions and Ledgers](TransactionsAndLedgers/) | Build a class-wide shared ledger, hash it, and discover why linking files by hash makes history unchangeable |
| 2 | [Bitcoin and Wallets](BitcoinAndWallets/) | Hash difficulty, minting, fees, block size and timing — then create your own wallet and interrogate what it really gives you |
| 3 | [Mempool and Wallet Programming](MempoolAndWalletProgramming/) | Where transactions wait before confirmation, what faucets are, and how to program a Bitcoin wallet in Java |
| 4 | [Keys and Layer 2](KeysAndLayerTwo/) | The RSA math behind public/private keys, multi-signature keys, and payment networks built on top of Bitcoin |
| 5 | [Smart Chains and Wrapped Bitcoin](SmartChainsAndWrappedBitcoin/) | Blockchains that run code, how Bitcoin gets "wrapped" onto Ethereum, and your first testnet ETH transaction |
| 6 | [Tokens in Java](TokensInJava/) | A complete ticketing token written in plain Java — run it, personalize it, and explain exactly how it works |
| 7 | [Proof of Stake](ProofOfStake/) | How validators, staking, rewards, and slashing replace mining — simulated live with a classroom exercise |
| 8 | [Writing Code on Ethereum](WritingCodeOnEthereum/) | Smart contracts, how Ethereum stores state, famous exploits, and your first contract deployed to a testnet |
| 9 | [Vyper with Custom Behavior](VyperCustomBehavior/) | Vyper syntax — external/internal methods, asserts, environment variables — and a contract with behavior you invent |
| 10 | [Deploying an ERC20 Token](ERC20Deployment/) | Read the real ERC20 example, deploy your own customized token to Sepolia, and mint it to classmates |
| 11 | [Crypto Research Project](CryptoResearchProject/) | Research a top-100 cryptocurrency and present who made it, what it does, how its code works, and why it matters |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Name the three ingredients from the previous module that a blockchain is built from.
- [ ] Explain, in one sentence, what makes a chain of hash-linked files hard to rewrite.
- [ ] State the safety rule this module applies to every on-chain activity.

### <font color="#79c0ff">Intermediate</font>

- [ ] Describe the path this module takes from a shared text file of IOUs to a deployed token.
- [ ] Explain why the module teaches Bitcoin before Ethereum.
- [ ] Say what a "test network" is and why the class uses one instead of a real blockchain.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why no lesson in this module requires trusting a central server — and which lesson first demonstrates that.
- [ ] Predict which skills from the Java lessons carry over to writing smart contracts in Vyper.
- [ ] Argue for or against the claim that "a blockchain is just a slow, shared file" using ideas from at least three lessons.
