<div align="center">

# Tokens in Java
*<font color="#8b949e">Concept review, then a complete currency written in a language you already speak</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">Questions for topical understanding</font>

Before touching code, check the concepts. Answer these out loud with a partner — every one of them was covered in the last five lessons:

1. What is a ledger, and where does a blockchain keep it?
2. What is the difference between a *pending* and a *confirmed* transaction?
3. Where does new bitcoin come from, and what limits how much will ever exist?
4. What does a **mint** operation do to the total supply? What does a **transfer** do to it?
5. What stops someone from transferring more than they have — a rule, a person, or code?
6. Bitcoin's ledger tracks coins; Ethereum's contracts can track anything. What does a **token** contract track?
7. If everyone can read all balances on a blockchain, what stays secret?
8. Why does a smart chain make a token trustworthy even when its author is not?

If any answer feels shaky, revisit [Transactions and Ledgers](../TransactionsAndLedgers/), [Bitcoin and Wallets](../BitcoinAndWallets/), or [Smart Chains and Wrapped Bitcoin](../SmartChainsAndWrappedBitcoin/) before continuing — today's program *is* those answers, written in Java.

---

## <font color="#388bfd">A token in Java</font>

A cryptocurrency token sounds exotic until you list what it actually needs:

| A token needs | In Java, that's |
|---|---|
| A ledger of who owns how much | `HashMap<String, Long> balances` |
| A way to create (mint) new units | a `giveTickets` method that grows a balance and the total supply |
| A way to move units between owners | a `transfer` method that subtracts from one balance and adds to another |
| A rule against overspending | one `if (senderBalance < ticketAmount)` check |
| A running count of all units | a `totalSupply` field |

That is the whole thing. The starter file [starter/TicketToken.java](starter/TicketToken.java) is a complete, working ticketing token with a menu so you can bank with yourself in the terminal.

### <font color="#79c0ff">Your task, from the source assignment</font>

Create a ticketing program in Java which creates virtual tickets you give out to different people. You can name your tickets whatever you like. You need to be able to give any amount to people, and allow people to use your program to give their tickets to someone else.

1. Open VS Code.
2. Create a Java file named `TicketToken.java` and copy in the [starter code](starter/TicketToken.java).
3. Run the program and test it using the menu that appears.
4. **Change the ticket name and the initial amounts so it is your own creation** — the `=== CHANGE THESE ===` comments mark every spot.
5. Read every comment in the code so you fully understand how it works.
6. When finished, show the working program to a classmate and **explain how the `transfer` and `giveTickets` methods work**, line by line.

### <font color="#79c0ff">Reading the two methods that matter</font>

**`giveTickets` (minting).** New tickets appear from nowhere: the recipient's balance grows *and* `totalSupply` grows. Compare: the block reward from [Bitcoin and Wallets](../BitcoinAndWallets/) is exactly a mint.

**`transfer` (moving).** No tickets are created or destroyed: one balance shrinks, another grows, `totalSupply` is untouched — and it happens *only if* the sender's balance covers the amount. That single `if` check is the entire law against counterfeiting.

> **Note:**
> Here is what your Java program *cannot* do that a blockchain token can: your HashMap lives in one process on one laptop, you can edit any balance by editing the code, and the program forgets everything when it exits. Put the same five ingredients into a smart contract and the ledger becomes public, permanent, and impossible for even its author to quietly edit. That translation is exactly what you will do in [Deploying an ERC20 Token](../ERC20Deployment/).

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Run TicketToken, mint tickets to a new person, and read the resulting balances.
- [ ] Point to the line that stores the ledger, the line that mints, and the line that blocks overspending.
- [ ] Rename the token and change the initial supply so the program is your own.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain why `transfer` leaves `totalSupply` unchanged while `giveTickets` grows it.
- [ ] Trigger the insufficient-balance rejection on purpose and explain what it prevents.
- [ ] Explain `transfer` and `giveTickets` to a classmate without looking at your notes.

### <font color="#79c0ff">Advanced</font>

- [ ] List what this program lacks compared with a real on-chain token, and which lesson supplies each missing piece.
- [ ] Predict what would break if `transfer` did its subtraction *after* its addition and the program crashed in between.
- [ ] Sketch how you would add a "burn" method, and state what it should do to `totalSupply`.

---

[Assignment](ASSIGNMENT.md)

← [Smart Chains and Wrapped Bitcoin](../SmartChainsAndWrappedBitcoin/) — Next: [Proof of Stake](../ProofOfStake/)
