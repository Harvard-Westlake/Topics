<div align="center">

# Deploying an ERC20 Token
*<font color="#8b949e">Read the real thing, deploy your own currency, and mint it to your classmates</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

Everything in this module converges here. You built a token in Java. You learned Vyper's syntax. You deployed a contract to Sepolia. Today you read the **real ERC20 example** — the standard token contract that thousands of real currencies follow — then deploy your own customized version and mint it to classmates. When you finish, a currency you wrote will exist on a public blockchain, visible to anyone on Earth.

---

## <font color="#388bfd">Part 1: understand the Vyper ERC20 example</font>

Open the official example and read the **entire code** carefully:

[https://github.com/vyperlang/vyper/blob/master/examples/tokens/ERC20.vy](https://github.com/vyperlang/vyper/blob/master/examples/tokens/ERC20.vy)

Take notes on:

- **What the contract does** — it is a full cryptocurrency/token on the blockchain
- **How it mirrors your Java program** — balance tracking, transfer, minting, and more

The mapping is nearly one-to-one with [Tokens in Java](../TokensInJava/):

| TicketToken.java | ERC20.vy | Same job |
|---|---|---|
| `String tokenName` | `name`, `symbol`, `decimals` | Identity of the currency |
| `HashMap<String, Long> balances` | `balanceOf: HashMap[address, uint256]` | The ledger — keyed by address, not by typed-in name |
| `giveTickets(recipientName, amount)` | `mint(_to, _value)` | Create new units, grow `totalSupply` |
| `transfer(senderName, recipientName, amount)` | `transfer(_to, _value)` | Move units; sender is `msg.sender`, proven by signature |
| `if (senderBalance < ticketAmount)` | balance check that reverts | The law against overspending |
| `System.out.println("OK: ...")` | `log Transfer(...)` events | The public record of what happened |

Be ready to discuss what you understood: name, symbol, transfer, mint, events.

> **Note:**
> Two things ERC20 has that your Java version never needed: **`approve`/`allowance`** lets a holder authorize someone else (often a contract) to spend up to a limit on their behalf, and **events** are how wallets and explorers hear about transfers without re-reading all of state. Notice also `mint` asserts `msg.sender == self.minter` — an access-control check from the vulnerability classes in [Writing Code on Ethereum](../WritingCodeOnEthereum/).

---

## <font color="#388bfd">Part 2: deploy your own ERC20 to Sepolia</font>

Follow these steps exactly on the class platform:

1. Go to [https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app)
2. Create a new file.
3. Copy the ERC20 example code into it (or use the simplified template on the site).
4. Customize it — this is what makes it *your* currency:
   - Change the token **name** and **symbol** to something fun (example: name `"ClassCoin"`, symbol `"CC"`)
   - Set an **initial supply** to yourself
5. Compile, then deploy to **Sepolia testnet** with the platform's deploy button.
6. Get free Sepolia ETH from the [faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia) if you need gas.
7. Once deployed, copy the **contract address**.

> **Warning:**
> Testnet only. Never fund a class wallet with real money, and never share a private key or seed phrase with anyone, including your teacher.

---

## <font color="#388bfd">Part 3: mint to classmates and prove it</font>

1. Ask **3–4 classmates** for their Sepolia wallet addresses.
2. Use your contract's **mint** function to send each of them some of your tokens.
3. Go to [sepolia.etherscan.io](https://sepolia.etherscan.io/), look up your contract address, and open the **#events** tab.
4. Copy the full link showing your mint transactions — example format: [https://sepolia.etherscan.io/address/0x5ceb98eea452a5ccad648af8e5d7e35bb31c6f3f#events](https://sepolia.etherscan.io/address/0x5ceb98eea452a5ccad648af8e5d7e35bb31c6f3f#events)

That link — your contract, with the mint events visible — is your submission. Details in the [assignment](ASSIGNMENT.md).

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Match each piece of TicketToken.java to its counterpart in ERC20.vy.
- [ ] Point to the line in ERC20.vy that prevents overspending.
- [ ] Customize a token's name, symbol, and initial supply before deploying.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain why the ledger is keyed by `address` instead of a typed-in name, and what that fixes.
- [ ] Explain what a Transfer event is for and who listens to it.
- [ ] Find your contract's #events tab on sepolia.etherscan.io and identify your mints.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain what `approve`/`allowance` enables that plain `transfer` cannot.
- [ ] Explain the access-control assert on `mint` and what would happen without it.
- [ ] Explain why your deployed token keeps working even if you delete your local copy of the code.

---

[Assignment](ASSIGNMENT.md)

← [Vyper with Custom Behavior](../VyperCustomBehavior/) — Next: [Crypto Research Project](../CryptoResearchProject/)
