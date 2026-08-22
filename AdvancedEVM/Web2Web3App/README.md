<div align="center">

# Web2 to Web3 App
*<font color="#8b949e">A working web app whose backend is a blockchain</font>*

<font color="#a371f7">Learning</font>

</div>

---

Blockchains can be accessed from the web. Everything you have deployed so far, you have driven through Etherscan or the class platform — but a normal web page can create transactions and talk to applications on the blockchain directly from the browser. This project connects the two halves of your training: the websites you built in [Web Programming](../../WebProgramming/) become the front end, and a contract you write becomes the backend.

---

## <font color="#388bfd">The four requirements</font>

To reach a blockchain from a browser, a page needs exactly four things:

| # | Requirement | What it is | Where it comes from |
|---|---|---|---|
| 1 | **A link between the blockchain and the browser** | A wallet extension — [MetaMask](https://metamask.io/) or similar — that holds keys, signs transactions, and exposes the chain to page JavaScript | The user installs it |
| 2 | **A pointer to the app you want** | The contract's **address** on the chain | You get it when you deploy |
| 3 | **A stencil of the application** | The **ABI** (Application Binary Interface) — a description of the contract's methods, variables, and structure, so the website knows which part of the app contains which part of the code | The compiler produces it alongside your bytecode |
| 4 | **A contract that is actually deployed** | Your code, live on the blockchain | You deploy it to Sepolia |

Assembled, the pipeline looks like this:

```
your web page (JavaScript)
      |
      |   "call vote(3)"           needs the ABI (#3) to encode the call,
      v                            and the address (#2) to aim it
wallet extension (#1)
      |
      |   user clicks Confirm -> the wallet signs the transaction
      v
Sepolia blockchain
      |
      v
your deployed contract (#4) runs, and its new state is
readable by EVERY visitor's browser -- no server of yours involved
```

> **Note:**
> The ABI deserves the word "stencil." The blockchain stores your contract as raw bytecode — no function names, no types. The ABI is the overlay that tells the browser "the `vote` function lives here and takes one number," letting JavaScript trace calls onto the right spots. Wrong ABI, and your page is dialing methods that do not exist.

---

## <font color="#388bfd">The project</font>

You are to create a web3 contract **which serves a purpose**, and add a page to your website which can run your web3 code.

"Serves a purpose" is the load-bearing phrase. A counter that increments is a demo; a poll the whole class votes in, a guestbook, a wager tracker, a class leaderboard — those are applications. The strongest projects (see the rubric in the [assignment](ASSIGNMENT.md)) are contracts the entire class can meaningfully interact with.

You are encouraged to reference the **Web3VoteExample** shown in class — it has working code that talks to the blockchain and can be interacted with. Use it to see how the four requirements fit together, not as a template to re-skin.

> **Tip:**
> Collect as much Sepolia ETH as you can **every day** of this project — [https://cloud.google.com/application/web3/faucet/ethereum/sepolia](https://cloud.google.com/application/web3/faucet/ethereum/sepolia). You WILL need it. Deploying costs gas, every write costs gas, and every redeploy after a bug costs gas. Running dry the night before the deadline is a preventable disaster.

Your workflow over the three days:

1. **Design and write the contract** in Vyper ([https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app)) and deploy to Sepolia
2. **Save the address and the ABI** from your deployment — requirements 2 and 3
3. **Build the page**: connect to the wallet extension, wire buttons and displays to your contract's functions
4. **Test end to end** with a classmate's wallet, not just your own
5. **Commit as you go** — the rubric grades your GitHub history and README, and one giant final commit is self-reporting that you did not

> **Warning:**
> Sepolia testnet only — never real funds. Your page's JavaScript must never ask for, store, or transmit a private key or seed phrase; the wallet extension exists precisely so keys never touch your code.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Name the four things a browser needs to reach a contract on a blockchain.
- [ ] Explain what a wallet extension like MetaMask actually does when a page requests a transaction.
- [ ] Say where the contract address and the ABI each come from in your own deployment.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain why the ABI is called a stencil — what information the raw bytecode is missing that the ABI supplies.
- [ ] Explain why a wrong or outdated ABI breaks a page even when the contract address is correct.
- [ ] Describe the difference between reading contract state and writing it, and which one costs gas.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain how two visitors' browsers see the same application state with no server owned by you in the middle.
- [ ] Design a contract the whole class can meaningfully interact with, and defend why it is more than a counter.
- [ ] Walk the full path of one button click — encode, sign, broadcast, mine, re-read — naming which of the four requirements each step depends on.

---

[Assignment](ASSIGNMENT.md)

← [IPFS and NFTs](../IPFSAndNFTs/) — Back to [Advanced EVM Programming](../)
