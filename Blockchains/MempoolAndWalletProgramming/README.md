<div align="center">

# Mempool and Wallet Programming
*<font color="#8b949e">Where transactions wait, where test coins come from, and a Bitcoin wallet you program yourself</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">The mempool: a waiting room for transactions</font>

When you announce a transaction, it does not go straight into a block. It goes into the **mempool** (memory pool) — every node's waiting room of valid-but-unconfirmed transactions. Miners look through the waiting room and pick which transactions to include in the block they are trying to mine. Since block space is limited, they pick the ones paying the highest fees first.

```
 your wallet          every node's mempool             miner builds a block
+-----------+       +-----------------------+       +----------------------+
| announce  | ----> |  tx  tx  tx  tx  tx   | ----> | picks highest-fee    |
| the tx    |       |  tx [your tx] tx  tx  |       | txs from the mempool | ---> confirmed
+-----------+       |  tx  tx  tx  tx       |       +----------------------+      in block
                    +-----------------------+
                     "pending" lives here
```

This is exactly the card reader's **Pending** state from Day 1, seen from the network's side. A transaction can sit in the mempool for minutes — or, if its fee is too low during a busy period, for hours — before a miner scoops it up. You can watch the real Bitcoin mempool live at [mempool.space](https://mempool.space).

---

## <font color="#388bfd">Faucets: free coins for test networks</font>

Real coins cost real money, which is no way to run a classroom. Every serious blockchain runs a **test network** (testnet) — a parallel chain with the same code but worthless coins — and **faucets** are websites that drip small amounts of testnet coins to anyone who asks. Developers use them to test wallets and programs without risking anything.

> **Warning:**
> Everything we program in this lesson runs on **testnet** with faucet coins. Never put real money into a class wallet, and never share a private key or seed phrase with anyone, including your teacher.

---

## <font color="#388bfd">Discussion: bank ETFs</font>

In 2024, US regulators approved **spot Bitcoin ETFs** — funds traded on the stock market that hold bitcoin, so people can get bitcoin exposure through an ordinary brokerage account. Discuss:

- An ETF buyer holds a *claim* on bitcoin that a custodian keeps for them. Who holds the keys?
- How does that compare to the wallet you made last lesson, where *you* hold the keys?
- Why might someone prefer each option? ("Not your keys, not your coins" — is that fair?)

Notice the irony: a technology designed to remove banks from money is now offered *by* banks, because holding your own keys is a responsibility many people do not want.

---

## <font color="#388bfd">Homework: program a Bitcoin wallet with BitcoinJ</font>

A wallet is just a program: it makes keys, derives an address, watches the chain for coins sent to that address, and signs transactions to spend them. [BitcoinJ](https://bitcoinj.org) is a Java library that does the heavy lifting, and you already speak Java — so tonight you will *program* a wallet instead of downloading one.

The full step-by-step instructions, code, and submission requirements are in the [assignment](ASSIGNMENT.md). The shape of the program:

```java
// The whole wallet in three moves:
NetworkParameters testNetwork = TestNet3Params.get();                 // 1. choose testnet
WalletAppKit walletKit = new WalletAppKit(testNetwork,
        new File("."), "class-wallet");                              // 2. create/load the wallet
walletKit.startAsync();
walletKit.awaitRunning();                                            //    sync with the network
System.out.println("Send test coins to: "
        + walletKit.wallet().freshReceiveAddress());                 // 3. print your address
```

Run it, take the address it prints to a testnet faucet, and watch your program receive coins — a bank you wrote yourself in a few dozen lines.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain what the mempool is and which transactions live in it.
- [ ] Explain what a faucet is and why testnets need them.
- [ ] State the rule about private keys and seed phrases in this class.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain how a miner decides which mempool transactions make it into the next block.
- [ ] Connect the card reader's "Pending" state to a transaction's life in the mempool.
- [ ] Describe what `WalletAppKit` does for your wallet program.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why a low-fee transaction might wait in the mempool for hours, and what a sender can do about it.
- [ ] Compare holding a Bitcoin ETF with holding your own keys — who can freeze each one.
- [ ] Trace the full journey of a faucet coin: faucet's wallet → mempool → block → your program's address.

---

[Assignment](ASSIGNMENT.md)

← [Bitcoin and Wallets](../BitcoinAndWallets/) — Next: [Keys and Layer 2](../KeysAndLayerTwo/)
