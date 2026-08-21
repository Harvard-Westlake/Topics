# Assignment — IPFS and NFTs

*Lesson: [IPFS and NFTs](README.md)*

**Due:** Next class
**Points:** 100

---

Get yourself two NFTs, then dig into what they actually are:

1. **Mint an NFT by providing pooled liquidity on Uniswap** (Sepolia testnet — this is the position NFT from yesterday's lesson)
2. **Buy an NFT on the OpenSea testnet:** [https://testnets.opensea.io](https://testnets.opensea.io)

Then work up through the grade tiers. Each tier includes everything below it.

> **Warning:**
> Sepolia testnet only — never real funds. Never share your private key or seed phrase with anyone or any website.

## For a C grade

- Look up either NFT on the testnet scanner ([https://sepolia.etherscan.io](https://sepolia.etherscan.io)) and read the instance variable `tokenURI` for your NFT
- Figure out what the NFT data is from reading the contract's tokenURI for your NFT's ID

## For a B grade

- Decode the NFT data. The Uniswap position NFT's tokenURI does not point at IPFS or the web — it carries its data *inline*, encoded in base64:

```
data:application/json;base64,eyJuYW1lIjoiVW5pc3dhcCAtIC4uLiJ9...
                             \__________________________________/
                               base64 -> JSON metadata, which itself
                               contains a base64-encoded SVG image
```

- These decoders will likely be helpful once you have the data:
  - [https://codebeautify.org/base64-to-json-converter](https://codebeautify.org/base64-to-json-converter)
  - [https://base64.guru/converter/decode/image/svg](https://base64.guru/converter/decode/image/svg)
- Answer: **does this data use IPFS?** If so, provide the IPFS URL.

> **Note:**
> You may use an AI assistant for help decoding — if you do, disclose in your submission how you used it, per the course AI policy.

## For an A grade

- Figure out how to transfer the NFT. Then transfer it to — or trade NFTs with — someone else in class.

---

## Success Criteria

Confirm the criteria for your tier (and every tier below it) before submitting:

- [ ] **Two NFTs acquired** — one minted via a Uniswap liquidity position and one bought on the OpenSea testnet, both visible in your wallet or on the scanner
- [ ] **C: tokenURI read** — you queried tokenURI on sepolia.etherscan.io for your token's ID and can say what kind of data it returned
- [ ] **B: data decoded** — you turned the base64 payload into readable JSON (and its image), and answered the IPFS question with evidence
- [ ] **A: NFT transferred** — a transfer or trade transaction to a classmate's address exists on the scanner

---

## Submission

Submit **one text response** and your **screenshot stack** on Canvas.

### Text response

Copy the stencil below, fill in each line (leave tiers you did not attempt blank), and paste it into the Canvas text box:

```
Tier attempted (C / B / A):           
NFT contract address:                 0x
My token ID:                          
tokenURI returned (first ~60 chars):  
B: Does the data use IPFS (yes/no):   
B: IPFS URL (if yes):                 
A: Classmate traded with:             
A: Transfer transaction hash:         0x
AI assistance used (what and how):    
```

### Screenshot stack

Upload a screenshot of whatever progress you made, **including all prerequisite tiers** — for an A, submit screenshots of the C, B, and A evidence:

- **C:** the Etherscan Read Contract page showing your tokenURI query and its result
- **B:** the decoded JSON (and the decoded image, if you got it)
- **A:** the transfer transaction on sepolia.etherscan.io showing the recipient's address

No screenshot may show a seed phrase, private key, or wallet backup screen.
