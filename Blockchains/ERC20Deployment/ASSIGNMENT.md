# Assignment — Deploying an ERC20 Token

**Due:** Next class
**Points:** 500

---

Deploy your own customized ERC20 token to the Sepolia testnet and mint it to classmates. This is the capstone of the token project that began with [Tokens in Java](../TokensInJava/ASSIGNMENT.md).

## Steps

1. **Read and annotate** the official example — [ERC20.vy](https://github.com/vyperlang/vyper/blob/master/examples/tokens/ERC20.vy) — noting how it mirrors your Java ticketing program (balance tracking, transfer, minting, events).
2. On the class platform ([https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app)), create a new file and copy in the ERC20 example (or the simplified template on the site).
3. **Customize it**: your own token name and symbol, and an initial supply minted to yourself.
4. Compile and **deploy to Sepolia** with the platform's deploy button. Get gas from the [faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia) if needed.
5. Collect Sepolia wallet addresses from **3–4 classmates** and **mint** some of your tokens to each of them.
6. On [sepolia.etherscan.io](https://sepolia.etherscan.io/), open your contract address's **#events** tab and copy the full link — example format, which your submission must match:
   [https://sepolia.etherscan.io/address/0x5ceb98eea452a5ccad648af8e5d7e35bb31c6f3f#events](https://sepolia.etherscan.io/address/0x5ceb98eea452a5ccad648af8e5d7e35bb31c6f3f#events)

> **Warning:**
> Testnet only. Never fund a class wallet with real money, and never share a private key or seed phrase with anyone, including your teacher.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Example understood** — you can name what ERC20.vy's `balanceOf`, `transfer`, `mint`, and events correspond to in your Java program
- [ ] **Token customized** — your name, symbol, and initial supply, not the example's defaults
- [ ] **Deployed to Sepolia** — the contract exists at an address you control the minter role for
- [ ] **Minted to 3–4 classmates** — separate mint transactions to at least three different classmate addresses
- [ ] **Events link works** — your `...#events` link opens on sepolia.etherscan.io and shows those mint transactions

---

## Submission

Submit **one text response** on Canvas.

### Text response

Copy the stencil, fill in each line, and paste it into the Canvas text box. The events link is the graded artifact — it must follow the example format exactly:

```
Token name and symbol:        
Contract address:             0x
Events link (the submission): https://sepolia.etherscan.io/address/0x...#events
Classmates I minted to:       
```
