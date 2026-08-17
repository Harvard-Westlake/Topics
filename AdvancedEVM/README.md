<div align="center">

# Advanced EVM Programming
*<font color="#8b949e">The Ethereum Virtual Machine as a real application platform</font>*

<font color="#a371f7">Learning</font>

</div>

---

In [Blockchains and Bitcoin](../Blockchains/) you deployed your first token — a contract that hands out tickets with your name on them. That was a single program running alone. This module treats the Ethereum Virtual Machine as what it actually is: an application platform. You will write contracts that hold *other contracts'* tokens in a vault, study markets that run with no market-maker behind the counter, store files that live nowhere and everywhere at once, and finish by shipping a working web app whose backend is a blockchain.

Everything in this module runs on the **Sepolia testnet**.

> **Warning:**
> Never use real funds anywhere in this module, and never share a private key or seed phrase with anyone — not a classmate, not a website, not an AI assistant. Test ETH is free; your real keys are not.

---

## <font color="#388bfd">Lessons</font>

| Day | Lesson | What you'll learn |
|---|---|---|
| 1 | [Wrapped Tokens and Layer 2](WrappedTokensAndLayerTwo/) | Addresses are people or code; wrapping one token inside another; rollups and cross-chain bridging |
| 2 | [Decentralized Finance](DecentralizedFinance/) | Lending, trading, and earning without a bank; how an automated market maker prices a trade |
| 3 | [IPFS and NFTs](IPFSAndNFTs/) | Content-addressed storage, ERC-721 tokens, and reading a live NFT contract on Etherscan |
| 4–6 | [Web2 to Web3 App](Web2Web3App/) | The four things a browser needs to reach a blockchain, and building a website that drives your own contract |

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you name the four lessons in this module and say in one sentence what each one builds?
- [ ] Can you explain why every exercise in this module uses the Sepolia testnet instead of Ethereum mainnet?
- [ ] Can you state the one rule about private keys and seed phrases that applies to every lesson here?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain how this module differs from the token you deployed in Blockchains and Bitcoin — what does "the EVM as an application platform" add?
- [ ] Can you describe one way two of these lessons connect (for example, how liquidity pools in Day 2 produce the NFT you study in Day 3)?
- [ ] Can you explain why a contract holding another contract's tokens is a bigger idea than a contract holding only its own?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you sketch the full arc of the module — from wrapping a classmate's token to a public web app — and say what new capability each day unlocks?
- [ ] Can you explain what it means for a web app's "backend" to be a blockchain instead of a server you administer?
- [ ] Can you argue for or against the claim that everything in this module could be built with a normal database and web server — what, exactly, does the EVM buy you?
