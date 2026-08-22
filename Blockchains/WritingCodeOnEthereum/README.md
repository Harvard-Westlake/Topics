<div align="center">

# Writing Code on Ethereum
*<font color="#8b949e">Smart contracts, how Ethereum stores the world, what has gone wrong, and your first deployment</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">What are smart contracts?</font>

Think of smart contracts as digital vending machines that live on the Ethereum blockchain. Just as a vending machine automatically gives you a snack when you put in money, a smart contract automatically executes actions when conditions are met — no middle person needed.

Smart contracts are computer programs following **"if this, then that"** logic. For example: *if Person A sends 1 ETH to this contract, then automatically send Person B a digital ticket.*

### <font color="#79c0ff">Key features</font>

- **Automatic** — once deployed, contracts run by themselves based on their programming
- **Transparent** — anyone can read the contract's code on the blockchain
- **Immutable** — once deployed, the code cannot be changed (like writing in permanent marker)
- **Trustless** — you do not need to trust the other person; the code enforces the rules

### <font color="#79c0ff">Real-world examples</font>

- **Digital tokens** — creating and managing cryptocurrencies on Ethereum (your TicketToken, but real)
- **NFTs** — ownership of digital art and collectibles
- **DeFi** — automated lending and trading platforms
- **Gaming** — in-game items and rewards

### <font color="#79c0ff">A first contract</font>

```solidity
// Basic smart contract example (Solidity)
contract SimpleStorage {
    uint storedData; // Declares a variable

    function set(uint x) public {
        storedData = x; // Stores a number
    }

    function get() public view returns (uint) {
        return storedData; // Returns the stored number
    }
}
```

A very basic digital storage box: it stores one number and lets anyone read it. The benefits (no intermediaries, fast automated execution, tamper-proof) and the costs (bugs cannot be fixed after deployment, gas fees, blockchain speed limits) all flow from the same fact — the code, once deployed, is on its own.

> **Note:**
> Smart contracts are "smart" only in that they execute automatically. They can only do what they are programmed to do — think "automated contracts," not artificially intelligent ones.

---

## <font color="#388bfd">How Ethereum stores transactions</font>

Ethereum's blockchain shares Bitcoin's skeleton but stores more.

**Similarities with Bitcoin:**

- **Chain of blocks** — a sequence of blocks containing transaction data
- **Cryptographic linking** — each block references the previous block's hash (Day 1's linked files)
- **Distributed ledger** — stored across many nodes in the network

**Key differences:**

| | Bitcoin | Ethereum |
|---|---|---|
| Accounting model | **UTXO** — unspent transaction outputs, like tracking individual bills | **Account-based** — like a bank account with a balance |
| What's stored | Transactions | Transactions **plus state**: account balances and smart contract data |
| Structure | Merkle trees of transactions | **Patricia Merkle Trees** that efficiently store and verify the whole state |

Beyond transactions, Ethereum blocks also carry smart contract code, contract state data, event logs, and gas usage information. That heavier storage is exactly what lets Ethereum be a platform for applications rather than only a currency.

---

## <font color="#388bfd">Does every contract call create a new block?</font>

No. Here is how it actually works:

- **Transactions are bundled** — many contract interactions and transfers are grouped into a single block
- **Block timing** — Ethereum creates a new block roughly every **12–15 seconds**, regardless of contract activity
- **Transaction queuing** — your contract call joins a pool of pending transactions waiting for the next block (Ethereum's mempool)

Think of blocks like buses: they leave on schedule and carry multiple passengers. Your contract call is one passenger waiting for the next bus. One nuance: anything that **changes state** (sending tokens, updating stored values) must ride a bus to count — but **read-only** calls that change nothing need no block at all.

---

## <font color="#388bfd">Smart contract security: famous exploits</font>

Immutability cuts both ways — bugs cannot be patched, only exploited or abandoned:

| Exploit | Year | What happened |
|---|---|---|
| **The DAO Hack** | 2016 | A contract vulnerability let an attacker drain ~3.6 million ETH (~$50 million then) — so significant it caused Ethereum to hard fork |
| **Parity Wallet Bug** | 2017 | A bug in a multi-signature wallet contract permanently froze ~$300 million of ETH |
| **Poly Network Exploit** | 2021 | A cross-chain vulnerability let hackers take over $600 million (later returned) |

**Common vulnerability classes:**

- **Reentrancy attacks** — a contract is interrupted mid-execution and re-entered to drain funds
- **Integer overflow/underflow** — math that exceeds a variable's size limits
- **Access control issues** — improper permissions allowing unauthorized actions
- **Logic errors** — mistakes in the business rules themselves

This is why auditing and thorough testing come *before* deployment — afterward is too late. Deployed bugs usually mean deploying a whole new contract and migrating users, if that is even possible.

---

## <font color="#388bfd">Token behavior, and the language we'll write</font>

Recall the five ingredients of [Tokens in Java](../TokensInJava/): a balances ledger, mint, transfer, an overspend check, and a total supply. A token *contract* is those five ingredients deployed as a vending machine — which is why you wrote the Java version first.

We will write contracts in **Vyper**: a Python-like language for Ethereum designed for **readability and security** — it deliberately removes features that make contracts hard to audit. (Solidity, used above, is the other common choice.) You will learn its syntax properly next lesson.

---

## <font color="#388bfd">Activity: write code on a real (test) blockchain</font>

Using the class platform — [https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app) — write and deploy a small Vyper contract to the **Sepolia testnet**:

1. Open the platform and start a new file (a starting template is provided there).
2. Compile, then deploy to Sepolia using your test wallet from [Smart Chains and Wrapped Bitcoin](../SmartChainsAndWrappedBitcoin/) — deployment is itself a transaction, so it costs faucet ETH.
3. Find your deployed contract's address on [sepolia.etherscan.io](https://sepolia.etherscan.io/) — your code is now stored on thousands of computers.

> **Warning:**
> Testnets only. Never deploy with a wallet holding real money, and never share a private key or seed phrase with anyone, including your teacher.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain a smart contract using "if this, then that" and the vending machine analogy.
- [ ] Name the four key features of deployed contracts and say which one makes bugs permanent.
- [ ] Name the three famous exploits and roughly what each one cost.

### <font color="#79c0ff">Intermediate</font>

- [ ] Contrast the UTXO and account-based models in one sentence each.
- [ ] Use the bus analogy to explain why a contract call does not create its own block.
- [ ] Explain which contract calls must be included in a block and which need none at all.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain what a reentrancy attack interrupts, and why the DAO hack forced a hard fork.
- [ ] Explain what Patricia Merkle Trees store for Ethereum that Bitcoin never needs to store.
- [ ] Argue why Vyper deliberately removes language features that Solidity keeps.

---

[Assignment](ASSIGNMENT.md)

← [Proof of Stake](../ProofOfStake/) — Next: [Vyper with Custom Behavior](../VyperCustomBehavior/)
