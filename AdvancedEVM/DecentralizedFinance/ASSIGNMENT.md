# Assignment — Decentralized Finance

**Due:** Next class

---

Today's work is preparation: tomorrow's assignment requires you to **mint an NFT by providing pooled liquidity on the Uniswap testnet**, and that only works if your wallet, your test ETH, and your understanding of the math are all ready.

## Steps

1. **Do the math by hand.** A pool holds 100 ALPHA and 10,000 BETA. Work out, on paper or in a note:
   - The constant `k`
   - The BETA paid out for a trade of 50 ALPHA into the pool
   - The effective price (BETA per ALPHA) of that trade, compared to the pool's starting ratio of 100
2. **Stock up on test ETH.** Collect Sepolia ETH from the faucet: [https://cloud.google.com/application/web3/faucet/ethereum/sepolia](https://cloud.google.com/application/web3/faucet/ethereum/sepolia). Collect every day this week — the rest of this module will spend it.
3. **Connect to Uniswap on the testnet.** Open [https://app.uniswap.org](https://app.uniswap.org), connect your **testnet wallet**, and switch the network to **Sepolia**. Find the screen for creating or adding to a liquidity pool position — you do not have to complete a deposit today, but you must know exactly where you will do it tomorrow.

> **Warning:**
> Testnet only. Double-check the network says **Sepolia** before you confirm anything in your wallet, use a wallet that holds no real assets, and never share your private key or seed phrase.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Trade computed correctly** — your k, payout, and effective price for the 50-ALPHA trade all follow from the constant-product formula
- [ ] **Sepolia ETH in hand** — your wallet shows a non-zero Sepolia ETH balance on sepolia.etherscan.io
- [ ] **Wallet connected on Sepolia** — Uniswap shows your wallet connected with the network set to Sepolia, not Ethereum mainnet
- [ ] **Pool screen located** — you can navigate to the new-liquidity-position screen without help

---

## Submission

Submit **one text response** and **one screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
k for the example pool:                  
BETA paid out for 50 ALPHA in:           
Effective price (BETA per ALPHA):        
My wallet address:                       0x
My Sepolia ETH balance:                  
```

### Screenshot

A screenshot of the Uniswap app with your wallet connected and the network selector showing **Sepolia**. The screenshot must not show a seed phrase, private key, or any wallet backup screen.
