# Assignment — Writing Code on Ethereum

**Due:** Next class
**Points:** 50

---

Deploy your first smart contract to the Sepolia testnet using the class platform, and prove it lives on-chain.

## Steps

1. Open the class platform: [https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app)
2. Start a new file from the platform's starting template and read every line — you should be able to say what each part does.
3. Compile the contract on the platform until it compiles cleanly.
4. Deploy it to the **Sepolia testnet** using your test wallet. If the deployment fails for lack of gas, top up from the faucet: [https://cloud.google.com/application/web3/faucet/ethereum/sepolia](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
5. Copy the deployed **contract address**, look it up on [sepolia.etherscan.io](https://sepolia.etherscan.io/), and confirm you can see the contract creation transaction.

> **Warning:**
> Testnet only. Deploy with your Sepolia test wallet, never one holding real funds, and never share a private key or seed phrase with anyone.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Contract compiles** — the platform compiles your code with no errors
- [ ] **Contract deployed** — the deployment transaction succeeded on Sepolia
- [ ] **Address recorded** — you have the deployed contract's address (it starts with `0x`)
- [ ] **Visible on Etherscan** — sepolia.etherscan.io shows the contract creation transaction at that address
- [ ] **You can explain it** — you can state in one or two sentences what your deployed contract does

---

## Submission

Submit **one text response** on Canvas.

### Text response

Copy the stencil, fill in each line, and paste it into the Canvas text box:

```
Deployed contract address:       0x
Etherscan link:                  https://sepolia.etherscan.io/address/
What my contract does:           
Wallet address that deployed it: 0x
```
