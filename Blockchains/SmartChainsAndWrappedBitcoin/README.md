<div align="center">

# Smart Chains and Wrapped Bitcoin
*<font color="#8b949e">Blockchains that run code, Bitcoin in an Ethereum costume, and your first testnet transaction</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Smart chains</font>

### <font color="#79c0ff">What are smart chains?</font>

Think of smart chains (also called smart contract platforms) as digital vending machines that can do much more than hand you snacks. They are blockchain networks that can run small computer programs — called **smart contracts** — automatically.

### <font color="#79c0ff">How do smart chains work?</font>

Imagine the shared notebook from Day 1 (that's the blockchain), but instead of only recording who owes money to whom, the notebook can automatically *handle tasks when conditions are met*: pay out an allowance every week, or unlock a game console when the homework is marked done.

Key features:

- **Automation** — once a smart contract is set up, it runs by itself; no human needed
- **Trust** — nobody can cheat, because everyone can see what is happening
- **Security** — everything is protected by the cryptography you now know the math behind
- **Decentralization** — no single person or company controls the machine

### <font color="#79c0ff">Real-world examples</font>

- **Digital art sales** — artists sell digital artwork automatically and get paid instantly
- **Gaming** — players truly own in-game items and can trade them
- **School records** — grades and certificates that cannot be faked
- **Allowance systems** — automatic scheduled payments

### <font color="#79c0ff">Popular smart chains</font>

- **Ethereum** — the first and most popular smart contract platform
- **Solana** — known for being fast and cheap to use
- **Binance Smart Chain** — built by the crypto company Binance

### <font color="#79c0ff">Challenges</font>

- **Learning curve** — they can be complicated at first
- **Energy use** — some chains use a lot of electricity (more on this in the Proof of Stake lesson)
- **Cost** — when many people use a chain at once, running code on it gets expensive

---

## <font color="#388bfd">In-class review: Bitcoin vs Ethereum</font>

A review of Bitcoin, and an introduction to Ethereum:

| Property | Bitcoin | Ethereum |
|---|---|---|
| Censorship resistant — no government can control it | Yes | Yes |
| Decentralized | Yes | Yes |
| Permissionless — no one can stop you from accessing it | Yes | Yes |
| Secure | Yes | Yes |
| Valuable | Yes | Yes |
| Fixed supply | Yes (21 million) | No fixed cap |
| Code is law — all behaviors are known rules | Yes | Yes |
| **Can save and execute computer code in each block** | No | **Yes** |

That last row is the entire difference in kind: Ethereum blocks carry *programs*, not just transactions.

---

## <font color="#388bfd">Wrapped Bitcoin</font>

Wrapped Bitcoin (WBTC) is like giving your Bitcoin a special costume that lets it play in the Ethereum playground.

### <font color="#79c0ff">What is it, and why?</font>

Bitcoin and Ethereum are like two different video game consoles — they do not naturally work together. **Wrapped Bitcoin** is an Ethereum version of Bitcoin: like converting dollars into arcade tokens, the value stays the same, but now you can use it in a different place — Ethereum's world of decentralized apps (dApps) and DeFi (decentralized finance).

### <font color="#79c0ff">How does it work?</font>

```
you            custodian (a trusted vault)              Ethereum
+-----+        +---------------------------+        +----------------+
| BTC | -----> | holds your real BTC safe  | -----> | mints an equal |
+-----+        | 1 BTC locked              |        | amount of WBTC |
               +---------------------------+        | to your wallet |
                                                    +----------------+
        (unwrapping runs the same diagram right-to-left)
```

1. You start with regular Bitcoin.
2. A special **custodian** (like a trusted bank) holds your Bitcoin safely.
3. The custodian creates (mints) an equal amount of **WBTC** on the Ethereum network.
4. You can now use that WBTC in Ethereum applications — and always convert back.

Think of wrapping a gift: the Bitcoin is the gift, the Ethereum-compatible wrapper goes around it, and the original sits safely stored while you use its Ethereum stand-in.

### <font color="#79c0ff">Is it safe? And is it really the same price?</font>

WBTC is generally considered safe because the original Bitcoin is securely stored, the process is managed by known organizations, and smart contracts run the mint/unwrap automatically — but notice you are trusting a **custodian**, which is exactly the kind of trust Bitcoin itself was built to remove. Compare the two prices yourself:

- [Bitcoin price](https://coinmarketcap.com/currencies/bitcoin/) vs [Wrapped Bitcoin price](https://coinmarketcap.com/currencies/wrapped-bitcoin/)

One is the Bitcoin blockchain; the other is Bitcoin held in a wallet and mirrored on the Ethereum blockchain. Last lesson we programmed a Bitcoin wallet in Java. Someone effectively programmed a Bitcoin wallet *on Ethereum* — you can deposit and transact Bitcoin through Ethereum code just as you did through Java code. That is all "wrapping" an asset means.

An example of what a real Ethereum account looks like from the outside — a teacher demo address you can inspect on a block explorer: [0xae111CBB37f948F244C565dB3b695348C986C982](https://sepolia.etherscan.io/address/0xae111CBB37f948F244C565dB3b695348C986C982)

---

## <font color="#388bfd">Activity: your first Ethereum testnet transaction</font>

> **Warning:**
> Test networks only. Never put real money into a class wallet, and never share a private key or seed phrase with anyone, including your teacher.

1. **Create a Sepolia test wallet.** Sepolia is Ethereum's test network. In Phantom Wallet: Settings → Developer Settings → **Enable Test Networks**. Your existing wallet address now works on Sepolia.
2. **Record your public key / wallet address** (it looks like `0x3aFB0B4cA9aB60165E207CB14067B07A04114413`).
3. **Get test ETH from the faucet:** [https://cloud.google.com/application/web3/faucet/ethereum/sepolia](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
4. **Send some testnet ETH to someone else in class** — sending from your wallet is what proves you own that address.
5. Find your transaction on [sepolia.etherscan.io](https://sepolia.etherscan.io/) and note **which block** it landed in.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain what a smart contract is using the vending machine analogy.
- [ ] Name the one capability Ethereum blocks have that Bitcoin blocks do not.
- [ ] Get Sepolia test ETH from the faucet into your own wallet.

### <font color="#79c0ff">Intermediate</font>

- [ ] Walk through the four steps that turn 1 BTC into 1 WBTC, naming who holds what at each step.
- [ ] Explain why sending ETH from a wallet proves you own that wallet's address.
- [ ] Find your own transaction on sepolia.etherscan.io and read off its block number.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain what trust WBTC reintroduces that plain Bitcoin was designed to remove.
- [ ] Compare the Bitcoin and Wrapped Bitcoin market prices and explain why they track each other.
- [ ] Connect "wrapping" to the Java wallet you wrote — what does it mean that code on one chain can represent value from another.

---

[Assignment](ASSIGNMENT.md)

← [Keys and Layer 2](../KeysAndLayerTwo/) — Next: [Tokens in Java](../TokensInJava/)
