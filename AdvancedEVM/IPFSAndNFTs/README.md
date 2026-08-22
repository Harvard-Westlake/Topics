<div align="center">

# IPFS and NFTs
*<font color="#8b949e">Files that live nowhere and everywhere — and the one-of-a-kind tokens that point at them</font>*

<font color="#a371f7">Learning</font>

</div>

---

Today's objectives are to understand IPFS and NFTs and to see their roles *together*. The motivation is cost: blockchain block space is extraordinarily expensive per byte, so storing a large object — an image, say — inside an Ethereum block is out of the question. The token lives on the chain; the file it points to has to live somewhere else. Today you learn where.

---

## <font color="#388bfd">IPFS</font>

What if we had a P2P network that was not just little players trading files, like individual users on torrent networks — and what if we linked it into the web itself?

**IPFS** stands for **InterPlanetary File System**. It is a protocol and peer-to-peer network for storing and sharing data in a distributed file system. IPFS uses **content addressing** to uniquely identify each file in a global namespace connecting all computing devices: [https://ipfs.tech/](https://ipfs.tech/)

Here is the core idea, side by side with the web you know:

```
LOCATION ADDRESSING (the normal web)          CONTENT ADDRESSING (IPFS)

"Get the file AT this place"                  "Get the file WITH this fingerprint"

 https://example.com/cat.jpg                   ipfs://QmT7XD...geWF
        |                                             |
        v                                             v
 one specific server                           ANY node holding data that
 (if it is down or the file                    hashes to QmT7XD...geWF
  changed, you get something                   (the hash proves you got
  else or nothing)                              exactly the right bytes)
```

How IPFS works, in four pieces:

1. **Content addressing.** Unlike traditional file systems that refer to data by where it is (like a URL), IPFS addresses data by *what it is*, using a hash. When you ask for a file on IPFS, you are asking for it by its contents, not its location — and the hash of what arrives proves you received exactly the file you asked for.
2. **Distributed storage.** Files are split into smaller pieces, distributed across many nodes around the world, and linked together. When you fetch a file, your computer retrieves pieces from multiple nodes rather than one central server — faster transfers, no single point straining under the load.
3. **Decentralization.** There is no central point of control or failure, which makes IPFS resilient against censorship and server outages — a sharp contrast with the centralized web servers you built against in [Web Programming](../../WebProgramming/).
4. **Caching and deduplication.** Fetched data is cached locally, saving bandwidth on repeat requests. And because addresses *are* content hashes, two identical files automatically share one address — duplicates deduplicate themselves.

Use IPFS yourself for free at [https://www.pinata.cloud/](https://www.pinata.cloud/) — you can host websites, folders, or files:

- **Website:** [http://randomplanetfacts.xyz/index.html](http://randomplanetfacts.xyz/index.html)
- **File:** [https://ipfs.io/ipfs/QmT7XDDwyRJYDo78eZ83gcg9nVvo7VV21EmjCK4etwgeWF](https://ipfs.io/ipfs/QmT7XDDwyRJYDo78eZ83gcg9nVvo7VV21EmjCK4etwgeWF)
- **Folder:** [https://ipfs.io/ipfs/QmYDvPAXtiJg7s8JdRBSLWdgSphQdac8j1YuQNNxcGE1hg/6715.png](https://ipfs.io/ipfs/QmYDvPAXtiJg7s8JdRBSLWdgSphQdac8j1YuQNNxcGE1hg/6715.png)

> **Note:**
> Look at those `Qm...` addresses and think back to the hashing unit: does IPFS use SHA, or SHA-256? Work out what property of the hash function makes content addressing safe at all.

---

## <font color="#388bfd">NFTs</font>

NFTs are tickets (tokens) which are **not** interchangeable — not *fungible*. They often have extra information written on them and are individually assigned to an owner. One NFT does not equal another NFT. And just like the fungible tickets you deployed earlier, anyone can create them.

What makes them work:

1. **Blockchain-based.** NFTs are built on Ethereum using smart contracts. The chain supports them natively, so NFTs can be bought, sold, and traded with no intermediaries.
2. **Uniqueness and scarcity.** Each NFT has distinct characteristics and is distinguishable from every other token. They can represent digital art, audio, video, game items, and other creative work; the metadata and unique identifier inside the token confirm its uniqueness and ownership.
3. **Interoperability.** Standardized protocols — **ERC-721** and **ERC-1155** — mean NFTs can be created, owned, and traded across different applications and platforms. An NFT earned in one game or marketplace can potentially be used in another that supports the same standard.
4. **Provenance and ownership.** The blockchain is a transparent, immutable ledger, so anyone can verify an NFT's full history of ownership. Proving authenticity and provenance matters enormously in the art world and anywhere else origin is value.
5. **Programmability.** Because NFTs are smart contracts, they can carry mechanics like **royalties** — automatically paying the original creator a percentage of every resale — or unlock content, or change based on conditions.
6. **Marketplaces and liquidity.** Platforms for buying, selling, and trading NFTs give creators new ways to monetize work and collectors a new asset class.

Code example — an ERC-721 written in Vyper, annotated line by line: [https://ethereum.org/en/developers/tutorials/erc-721-vyper-annotated-code/](https://ethereum.org/en/developers/tutorials/erc-721-vyper-annotated-code/)

---

## <font color="#388bfd">Reading a live NFT contract</font>

Time to investigate a real one. The contract below is Azuki, a well-known 10,000-piece NFT collection on Ethereum mainnet:

- Contract: [https://etherscan.io/token/0xed5af388653567af2f388e6224dc7c4b3241c544#readContract](https://etherscan.io/token/0xed5af388653567af2f388e6224dc7c4b3241c544#readContract)
- One of its files on IPFS: [https://ipfs.io/ipfs/QmZcH4YvBVVRJtdn4RdbaqgspFU8gH6P9vomDpBVpAL3u4/6715](https://ipfs.io/ipfs/QmZcH4YvBVVRJtdn4RdbaqgspFU8gH6P9vomDpBVpAL3u4/6715)

Etherscan lets you **run** a contract's read-only functions right in the browser. To investigate any NFT you have been given, open the contract from your transaction, then:

```
Etherscan contract page
   |
   |  1. Click the [Contract] tab
   |  2. Click [Read Contract]
   |  3. Scroll to  tokenURI  (shown as getTokenUri on some contracts)
   |  4. Enter a token ID  --  for Azuki, anything from 1 to 10000, like 7000
   |  5. Click [Query]
   v
 tokenURI(7000)  ->  "ipfs://QmZcH4YvBVVRJtdn4RdbaqgspFU8gH6P9vomDpBVpAL3u4/7000"
                                        |
                     swap ipfs:// for an ipfs.io gateway URL:
                     https://ipfs.io/ipfs/QmZcH4.../7000   ->  the token's metadata
```

The chain stores the *pointer*; IPFS stores the *content*. That is the whole partnership: a unique, ownable token on Ethereum whose data lives on a network built for files. Try a few different token IDs against the folder hash above and watch each one resolve to different metadata.

> **Tip:**
> Not every contract returns an `ipfs://` URI. Some return an HTTPS URL (centralized — the owner can change or lose the file), and some return the data itself, encoded directly into the URI. You will meet that last kind in tonight's assignment.

> **Warning:**
> Your own minting and trading happens on the **Sepolia testnet** with free test ETH — never real funds. Never share your private key or seed phrase with anyone.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain the difference between location addressing and content addressing in one sentence each.
- [ ] Explain what "non-fungible" means using the ticket metaphor from your earlier token work.
- [ ] Find the tokenURI function on an Etherscan Read Contract page and query it with a token ID.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain why NFT images are stored on IPFS instead of inside Ethereum blocks.
- [ ] Explain how IPFS gets caching and deduplication for free from content addressing.
- [ ] Name two things ERC-721 standardizes and explain why standardization lets an NFT move between platforms.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain what property of a cryptographic hash makes a content address trustworthy, and what would break if two files could share a hash.
- [ ] Compare the three kinds of tokenURI (ipfs://, https://, inline data) and rank them by how much the owner must be trusted.
- [ ] Trace the complete path from owning a token ID on Ethereum to displaying its image, naming every system involved.

---

[Assignment](ASSIGNMENT.md)

← [Decentralized Finance](../DecentralizedFinance/) — Next: [Web2 to Web3 App](../Web2Web3App/)
