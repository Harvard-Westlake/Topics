<div align="center">

# Decentralized Finance
*<font color="#8b949e">Lending, trading, and earning without a bank — markets run entirely by contracts</font>*

<font color="#a371f7">Learning</font>

</div>

---

Yesterday you built a vault: a contract that holds other people's tokens under rules no human can override. Decentralized finance — **DeFi** — is what happens when an entire financial system is built out of vaults like yours.

---

## <font color="#388bfd">What is DeFi?</font>

Traditional finance runs on intermediaries. A bank holds your deposit, decides your loan, and sets your interest. An exchange matches your trade and takes a cut. In every case you trust an institution to hold the money and follow its own rules.

DeFi replaces the institution with a smart contract:

| You want to... | Traditional finance | DeFi |
|---|---|---|
| Trade one asset for another | An exchange matches buyers and sellers | A **liquidity pool** contract quotes a price from a formula |
| Borrow | A bank checks your credit and holds collateral | A **lending pool** contract holds your collateral and enforces repayment in code |
| Earn interest | The bank lends your deposit and pays you a sliver | You deposit into a pool and earn the fees or interest it collects directly |

The contract cannot decide it dislikes you, cannot close on weekends, and cannot quietly change the rules — the rules are the deployed code, readable by anyone. That is the promise. The price of the promise is that the code's bugs are also the rules.

---

## <font color="#388bfd">The automated market maker</font>

The hardest thing to decentralize is a market itself. A stock exchange needs an **order book** — a live list of buyers and sellers — and someone standing in the middle matching them. On a blockchain, where every update costs gas, maintaining an order book is painfully expensive.

DeFi's answer is the **automated market maker (AMM)**: a pool contract that holds a reserve of two tokens and prices every trade with one formula. No order book. No market-maker. Just math and a vault.

The most famous formula is **constant product**:

```
reserve_of_A  ×  reserve_of_B  =  k        (k never decreases from trading)
```

Every trade must leave the product of the two reserves unchanged. That single rule sets the price.

### <font color="#79c0ff">A worked example</font>

A pool holds **100 ALPHA** and **10,000 BETA**:

```
k = 100 × 10,000 = 1,000,000
```

A trader sends in 25 ALPHA and asks for BETA. The pool's ALPHA reserve becomes 125, and the product must stay 1,000,000:

```
new BETA reserve = 1,000,000 ÷ 125 = 8,000
BETA paid out    = 10,000 − 8,000  = 2,000
```

The trader paid 25 ALPHA for 2,000 BETA — an effective price of 80 BETA per ALPHA, even though the pool's starting ratio implied 100 BETA per ALPHA. Bigger trades push the price further against you: this is **price impact**. Try it — a trade of 100 ALPHA into the same pool only returns 5,000 BETA (50 BETA per ALPHA).

> **Note:**
> The formula is self-balancing. The scarcer a token gets in the pool, the more expensive the formula makes it. No one adjusts the price; the price *is* the reserves.

---

## <font color="#388bfd">Providing liquidity — and the NFT you get for it</font>

Where do the pool's reserves come from? From users called **liquidity providers** who deposit *both* tokens into the pool. In exchange, they earn a small fee (typically a fraction of a percent) from every trade that passes through. That is DeFi's version of earning interest: your tokens work in a market instead of sitting in a wallet.

When you provide liquidity on **Uniswap** — the largest AMM — the contract mints you a token representing your position. And here is the connection to tomorrow's lesson: that position token is an **NFT**, not a regular token. Your position specifies its own pair of tokens, its own fee tier, and its own price range, so no two positions are interchangeable. A one-of-a-kind claim needs a one-of-a-kind token — which is exactly what ERC-721 provides, and exactly what you will inspect on-chain tomorrow.

### <font color="#79c0ff">Impermanent loss</font>

Providing liquidity has a subtle cost. Traders constantly rebalance the pool toward market prices, which means the pool *sells the token that is going up* and *accumulates the token that is going down* — the opposite of what you would want. Suppose you provided our whole example pool and ALPHA's market price then doubled:

| Strategy | You end up holding | Value (in BETA) |
|---|---|---|
| Just held your tokens | 100 ALPHA + 10,000 BETA | about 30,000 |
| Provided liquidity | about 71 ALPHA + 14,142 BETA | about 28,284 |

The gap — roughly 5.7% here — is called **impermanent loss**: "impermanent" because it shrinks if prices return to where they started, but very permanent if you withdraw while prices are moved. Trading fees exist to compensate providers for exactly this risk.

---

## <font color="#388bfd">DeFi risk</font>

DeFi removes the banker but not the danger — it relocates it:

- **Smart-contract bugs.** The pool is a program holding real value. One flawed line — a bad assert, a lying `balanceOf` like yesterday's lesson — and everything in the vault can be drained. Some of the largest thefts in software history are DeFi contract exploits.
- **Rug pulls.** Anyone can create a token and a pool for it. A creator who keeps most of the supply can wait for others to provide real value, then dump their tokens into the pool and walk away with the reserves. "Anyone can create a market" cuts both ways.

> **Warning:**
> Every exercise in this module uses the **Sepolia testnet** with free test ETH — never real funds. Never connect a wallet holding real assets to an unfamiliar site, and never share a private key or seed phrase with anyone.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you name the intermediary DeFi removes for trading, and say what replaces it?
- [ ] Can you state the constant-product rule and explain what "k stays the same" means for a trade?
- [ ] Can you explain what a liquidity provider deposits and what they earn in return?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you compute the payout for a trade of 50 ALPHA into a pool of 100 ALPHA and 10,000 BETA using the constant-product formula?
- [ ] Can you explain why a bigger trade gets a worse effective price in an AMM?
- [ ] Can you explain why a Uniswap liquidity position is represented as an NFT instead of a regular token?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain impermanent loss — why the pool ends up holding less of whichever token went up in price?
- [ ] Can you describe how a rug pull works, step by step, from pool creation to the reserves disappearing?
- [ ] Can you connect yesterday's "contracts can lie" security lesson to a way a malicious token could exploit a liquidity pool?

---

[Assignment](ASSIGNMENT.md)

← [Wrapped Tokens and Layer 2](../WrappedTokensAndLayerTwo/) — Next: [IPFS and NFTs](../IPFSAndNFTs/)
