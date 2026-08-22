<div align="center">

# Proof of Stake
*<font color="#8b949e">Securing a blockchain with collateral instead of computation</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Understanding Proof of Stake</font>

Imagine you are part of a club where the more tokens you hold and "lock up" (like putting money in a savings account), the more voting power you have in decisions. That is basically how **Proof of Stake (PoS)** works in blockchain technology.

### <font color="#79c0ff">How does it work?</font>

In a Proof of Stake system, instead of using powerful computers to solve hash puzzles (like Bitcoin's **Proof of Work** from [Bitcoin and Wallets](../BitcoinAndWallets/)), people become **validators** by staking their cryptocurrency. Think of it as putting down a security deposit — the more you stake, the more likely you are to be chosen to validate new transactions and create new blocks.

### <font color="#79c0ff">Key components</font>

- **Validators** — people who lock up (stake) their tokens to participate in block creation
- **Stake** — the amount of cryptocurrency someone commits to the network
- **Rewards** — validators earn new tokens and transaction fees for maintaining the network
- **Slashing** — bad behavior (like trying to cheat) costs some or all of the staked tokens

### <font color="#79c0ff">Benefits over Proof of Work</font>

- **Energy efficient** — no massive computing power needed, far more environmentally friendly
- **Lower entry barrier** — no expensive mining equipment required to participate
- **Better security** — attacking the network requires staking huge amounts of money, making attacks very expensive

### <font color="#79c0ff">Real-world picture</font>

Becoming a validator is like becoming a bank security guard who posts collateral: the more money you put down as collateral (stake), the more likely you are to be trusted with protecting the vault (validating transactions). Do the job well and you earn rewards; try to steal and you lose the collateral.

### <font color="#79c0ff">Popular PoS blockchains</font>

- Ethereum (since its merge in 2022)
- Cardano
- Solana
- Polkadot

### <font color="#79c0ff">Potential drawbacks</font>

- **Initial distribution** — those with more tokens have more power in the network
- **Minimum stake requirements** — some networks require large amounts to become a validator
- **Technical knowledge** — running a validator node still takes expertise

Proof of Stake is a more sustainable and accessible approach to consensus. It is not perfect, but it solves many of Proof of Work's problems, which is why modern networks increasingly choose it.

---

## <font color="#388bfd">Classroom P2P network simulation</font>

We will *be* a Proof of Stake network for twenty minutes:

1. **Forming the network** — divide into groups of three; each group is a node in a P2P network.
2. **Initial investment** — every student contributes $5 to a collective pot.
3. **Transaction announcement** — each student writes down a unique transaction or code execution (e.g., sending a message) and shares it with the other two in their group.
4. **Hash generation** — each student individually creates a hash of all transactions shared within the group, using a simple hashing technique (e.g., the first letter of each transaction, concatenated).
5. **Hash comparison** — students reveal their hashes to the group.
6. **Reward or slash** — if all three hashes match, each student adds $3 to their initial amount. If one hash differs, that student **loses $3**, split between the other two.
7. **Reflection** — discuss the importance of consensus and the consequences of discrepancies.

What just happened: you formed a mini network and contributed capital ($5) to participate — that is **staking**. You validated transactions (hash generation) and reached **consensus**; correct validators were **rewarded**, and a diverging validator was **slashed**. Economic incentives made everyone careful — that is PoS security in one sentence. Unlike Bitcoin's Proof of Work, which spends electricity on competition, PoS relies on committed capital, making it more energy-efficient and capital-efficient.

> **Note:**
> Play with pretend dollars or points if the class prefers — the incentive structure, not the cash, is the lesson.

---

## <font color="#388bfd">Proof of Stake vocabulary</font>

| # | Term | Meaning |
|---|---|---|
| 1 | **PoS (Proof of Stake)** | Validators secure the network by staking their own tokens |
| 2 | **Capital efficiency** | Better use of financial resources without wasting energy |
| 3 | **Validator** | A participant who stakes tokens to validate transactions and create new blocks |
| 4 | **Staking** | Locking up tokens as collateral to participate in network operations |
| 5 | **Consensus** | Agreement reached among nodes in a blockchain network |
| 6 | **Slashing** | Penalty for malicious behavior or failure to validate accurately |
| 7 | **Delegation** | Token holders appoint others to validate on their behalf |
| 8 | **Epoch** | A fixed period for validating transactions and distributing rewards |
| 9 | **Finality** | The point at which completed transactions cannot be altered or reversed |
| 10 | **Bonding period** | Time during which staked tokens cannot be transferred or withdrawn |
| 11 | **Nonce** | A value demonstrating computational effort in PoW; less relevant in PoS |
| 12 | **Governance** | Token holders' ability to vote on network changes and decisions |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Define validator, stake, reward, and slashing in your own words.
- [ ] State the main resource PoW consumes and the main resource PoS commits instead.
- [ ] Name three blockchains that use Proof of Stake.

### <font color="#79c0ff">Intermediate</font>

- [ ] Map each step of the classroom simulation to its PoS vocabulary term.
- [ ] Explain why slashing makes validators careful even when nobody is watching them.
- [ ] Explain why an attacker finds a PoS network expensive to attack.

### <font color="#79c0ff">Advanced</font>

- [ ] Argue the strongest criticism of PoS (who ends up with the power?) and a response to it.
- [ ] Explain the difference between consensus and finality using the simulation as your example.
- [ ] Compare the energy story of the block confirmations in Bitcoin and post-merge Ethereum.

---

← [Tokens in Java](../TokensInJava/) — Next: [Writing Code on Ethereum](../WritingCodeOnEthereum/)
