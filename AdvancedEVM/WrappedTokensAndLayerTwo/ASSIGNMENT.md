# Assignment — Wrapped Tokens and Layer 2

**Due:** Next class

---

Write the code to correctly wrap and unwrap **anyone's** ticket token using yours. Your wrapper must work at a ratio of at least **1000 to 1** in the worst case — 1000 of another person's tokens buy one of yours.

Study the class example first: [`starter/wrapped_ticket_example.vy`](starter/wrapped_ticket_example.vy). It is the *studied example*, not your submission — write your own variant, and fix at least one of the design questions the example's comments raise.

## Steps

1. Pick a classmate's ticket token from [Blockchains and Bitcoin](../../Blockchains/) and record its contract address.
2. Write your wrapper contract in Vyper on the class platform: [https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app)
   - A `wrapToken` function that pulls in the original tickets and mints your wrapped tokens at 1000:1
   - An `unwrapToken` function that burns your wrapped tokens and releases the originals at 1:1000
   - Validation checks and at least one helper view function
3. Deploy to the **Sepolia testnet**.
4. On the classmate's ticket token contract, `approve` your wrapper, then wrap at least 1000 of their tickets.
5. Unwrap at least one wrapped token and confirm the originals come back.
6. Verify both transactions on [https://sepolia.etherscan.io](https://sepolia.etherscan.io).

> **Warning:**
> Sepolia testnet only — never real funds. Never share your private key or seed phrase with anyone or anything.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Wrapper deployed** — your contract has a Sepolia address and its deployment transaction is visible on sepolia.etherscan.io
- [ ] **Wraps anyone's ticket** — the wrap function takes the token's address as a parameter and worked on a classmate's token, not just your own
- [ ] **1000:1 ratio holds** — wrapping 1000 tickets mints exactly 1 wrapped token, and the contract rejects amounts below 1000 with a clear error
- [ ] **Unwrap reverses wrap** — burning 1 wrapped token returned exactly 1000 original tickets to your address
- [ ] **Validation checks present** — your code asserts on insufficient amount, failed transfers, and insufficient wrapped balance rather than failing silently

---

## Submission

Submit **one text response** and **one screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Wrapper contract address:        0x
Ticket token wrapped (owner):    
Ticket token address:            0x
Wrap transaction hash:           0x
Unwrap transaction hash:         0x
One check my code makes:         
```

### Screenshot

A screenshot of your wrapper contract's page on sepolia.etherscan.io showing both the wrap and unwrap transactions in its transaction list. The address shown must match the one in your text response. Do not include your wallet's seed phrase, private key, or browser extension unlock screen anywhere in the screenshot.
