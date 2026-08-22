<div align="center">

# Wrapped Tokens and Layer 2
*<font color="#8b949e">Contracts that hold other contracts' tokens — and how blockchains scale past themselves</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Objectives</font>

**Part 1**

- Addresses are people OR code
- Wrapped tokens, revisited

**Part 2**

- Rollup transactions to scale blockchains
- Rollups: Optimistic vs ZK
- Bridging assets from one chain to another
- Cross-chain transfers and token mechanics on Layer 2s

---

## <font color="#388bfd">Addresses are people OR code</font>

Every account on Ethereum is a 20-byte address, and from the outside they look identical. But there are exactly two kinds:

| Kind | Controlled by | Can it hold ETH and tokens? | Can it run code? |
|---|---|---|---|
| **Externally owned account (EOA)** | A person with a private key | Yes | No |
| **Contract account** | Its own code — nothing else | Yes | Yes |

This is the single idea today's lesson turns on: **a contract has an address just like you do, so a contract can own tokens just like you do.** When you send tokens to a contract's address, the contract holds them — and only the rules written in its code decide when they leave.

That means a contract can act as a *vault*: it accepts deposits, keeps its own ledger of who deposited what, and releases funds only when its rules are satisfied. No human holds the key. The code is the key.

---

## <font color="#388bfd">Wrapped tokens, revisited</font>

You met Wrapped Bitcoin in [Blockchains and Bitcoin](../../Blockchains/): real BTC is locked in custody, and a matching token (WBTC) is minted on Ethereum so Bitcoin's value can move through Ethereum's contracts. The same trick works between any two tokens, and now you know exactly what the "custodian" is — a contract account acting as a vault.

The mechanics have two halves that must mirror each other perfectly:

```
WRAP                                        UNWRAP

 you                    wrapper contract     you                    wrapper contract
  |                                           |
  |--- deposit 1000 TICKET ----------->|      |--- send back 1 wTICKET ------->|
  |    (vault locks them)              |      |    (contract BURNS it)         |
  |                                    |      |                                |
  |<-- contract MINTS 1 wTICKET -------|      |<-- vault releases 1000 TICKET -|
```

- **Wrap:** you deposit the original tokens into the vault; the contract mints wrapped tokens to your balance at a fixed ratio.
- **Unwrap:** you give wrapped tokens back; the contract burns them and releases the originals at the inverse ratio.

As long as *every* wrapped token in existence is backed by originals sitting in the vault, the wrapped token is a trustworthy receipt. Break that invariant — mint without locking, or release without burning — and the wrapper is a fraud.

> **Note:**
> "Burning" just means subtracting from a balance and from `totalSupply` so the tokens cease to exist. There is no fire involved, only arithmetic.

---

## <font color="#388bfd">Why Layer 2? Rollups</font>

Ethereum processes on the order of tens of transactions per second, and every node replays every one. When demand spikes, fees spike. The scaling answer is not "make blocks bigger" — it is **do the work somewhere else, and post a compressed summary to Ethereum**.

A **rollup** is a separate chain (a "Layer 2") that executes thousands of transactions off-chain, then rolls them up into one batch and posts that batch to Ethereum ("Layer 1"). Ethereum stores the summary; the rollup does the heavy lifting. One L1 transaction can settle thousands of L2 transactions, so each user's share of the fee gets tiny.

The hard question: **how does Ethereum know the rollup's batch is honest?** Two answers, two families of rollup:

| | Optimistic rollups | ZK rollups |
|---|---|---|
| **Core idea** | Assume every batch is valid | Prove every batch is valid |
| **How cheating is caught** | A challenge window (about a week) during which anyone can submit a *fraud proof* showing a batch is wrong | A cryptographic *validity proof* (zero-knowledge proof) is posted with the batch — an invalid batch cannot produce one |
| **Withdrawal back to L1** | Slow — you wait out the challenge window | Fast — as soon as the proof is verified |
| **Cost of the math** | Cheap to run, expensive to dispute | Expensive proofs to generate, cheap to verify |
| **Examples** | Arbitrum, Optimism | zkSync, Starknet |

> **Tip:**
> Remember the pair by their attitude: *optimistic* rollups trust and verify later; *ZK* rollups verify up front and trust no one.

---

## <font color="#388bfd">Bridging: wrapped tokens between chains</font>

Here is the payoff of Part 1: **a bridge is just a wrapper contract stretched across two chains.**

To move a token from Layer 1 to a Layer 2:

```
Layer 1 (Ethereum)                          Layer 2 (rollup)

 you --- deposit 1000 TICKET ---> [bridge vault contract]
                                       |
                                       |  message: "this address locked 1000"
                                       v
                                  [bridge mint contract] --- mints 1000 TICKET-L2 ---> you
```

1. You deposit tokens into a bridge contract on L1. They are **locked** in the vault.
2. The bridge relays a message to L2 proving the deposit happened.
3. A contract on L2 **mints** an equivalent token for you there.
4. Going home reverses it: the L2 token is **burned**, and the L1 vault **releases** your original.

Lock-and-mint going out, burn-and-release coming back — exactly your wrapper, split across two chains. The token you spend on an L2 is almost always a wrapped claim on something locked on L1. That is what "cross-chain transfer" means mechanically, and it is why bridge contracts hold enormous value — and why bridge bugs have caused some of the largest thefts in the history of software.

---

## <font color="#388bfd">Building a wrapper: step-by-step implementation guide</font>

Your homework is to build this vault yourself, for the ticket tokens your class deployed. Here is how to break the work down.

### <font color="#79c0ff">1. Set up the contract structure</font>

- Create a new smart contract file
- Import the ERC-20 interface so your contract can talk to other token contracts
- Define state variables for your wrapped token's supply and balances

### <font color="#79c0ff">2. Implement token wrapping</font>

- Write a wrapping function that accepts the address of the token to be wrapped and the amount to wrap
- Add validation checks: the amount is large enough, the sender has sufficient balance, and the sender has approved your contract to pull the tokens
- Apply the 1000:1 ratio — wrapped tokens minted = original tokens deposited / 1000

### <font color="#79c0ff">3. Implement token unwrapping</font>

- Burn the caller's wrapped tokens
- Return the original tokens at the inverse 1:1000 ratio
- Add safety checks: the caller has enough wrapped tokens, and the vault holds enough originals to pay out

### <font color="#79c0ff">4. Add helper functions</font>

- View functions to check balances, preview conversion amounts, and read total supply

### <font color="#79c0ff">5. Test</font>

- Test with small amounts first
- Verify the 1000:1 ratio is exact in both directions
- Test edge cases — the minimum amount, very large amounts, and amounts that do not divide evenly by 1000
- Confirm every failure case actually reverts with a clear error message

> **Note:**
> Also include events for important state changes, and consider an admin function for emergencies. Real wrapper contracts have both.

---

## <font color="#388bfd">The studied example</font>

The class example lives in [`starter/wrapped_ticket_example.vy`](starter/wrapped_ticket_example.vy) — read it top to bottom before writing your own. Its core is these two functions:

```python
@external
def wrapToken(ticket_token_address: address, ticket_amount: uint256):
    assert ticket_amount >= 1000, "Minimum 1000 tickets required"
    wrapped_amount: uint256 = ticket_amount // 1000

    # Pull the original tickets into the vault
    transfer_succeeded: bool = extcall IERC20(ticket_token_address).transferFrom(
        msg.sender, self, ticket_amount
    )
    assert transfer_succeeded, "Transfer failed"

    # Mint wrapped tickets to the depositor
    self.totalSupply += wrapped_amount
    self.balanceOf[msg.sender] += wrapped_amount


@external
def unwrapToken(ticket_token_address: address, wrapped_amount: uint256):
    original_amount: uint256 = wrapped_amount * 1000

    # Burn the wrapped tickets first
    assert self.balanceOf[msg.sender] >= wrapped_amount, "Insufficient wrapped tokens"
    self.balanceOf[msg.sender] -= wrapped_amount
    self.totalSupply -= wrapped_amount

    # Release the originals from the vault
    transfer_succeeded: bool = extcall IERC20(ticket_token_address).transfer(
        msg.sender, original_amount
    )
    assert transfer_succeeded, "Transfer failed"
```

### <font color="#79c0ff">Calling the functions</font>

Wrapping is a two-step dance, because your contract pulls tokens it does not own yet:

1. On the **original token's** contract, approve the wrapper to spend your tokens:

```python
# Called on the ticket token contract
original_token.approve(wrapper_contract_address, amount_to_wrap)
```

2. Then call the wrap function on **your wrapper**:

```python
wrapper_contract.wrapToken(original_token_address, amount_to_wrap)
```

Unwrapping is one step — your contract already holds both sides:

```python
wrapper_contract.unwrapToken(original_token_address, amount_of_wrapped_tokens)
```

> **Tip:**
> The amount you wrap must be at least 1000 tokens because of the ratio, and the conversion is always 1000:1 wrapping and 1:1000 unwrapping. Make sure you hold enough balance before calling either function.

---

## <font color="#388bfd">Security: contracts can lie</font>

Suppose you try to double-check a deposit by asking the token contract itself:

```python
assert staticcall someone_elses_token.balanceOf(self) == expected_amount, "Transferred Tokens"
```

Here is the trap: `staticcall` only prevents the called contract from *modifying state* — it does not prevent the contract from **reporting incorrect values**. A malicious token contract can implement `balanceOf` to return whatever number it wants. You asked a stranger to grade their own homework.

Defenses, in increasing order of paranoia:

- **Verify the token contract's code** and confirm it is the genuine token you expect, not a lookalike
- **Check the actual balance delta** — read the vault's balance before and after the transfer, and assert the increase matches the amount claimed
- **Use a trusted token list or registry** so your wrapper simply refuses to wrap unknown or malicious tokens

The studied example includes the balance-delta check. Depending on what your wrapper is for, you may need more.

> **Warning:**
> Everything here runs on the Sepolia testnet with free test ETH. Never deploy experiments with real funds, and never share your private key or seed phrase — a leaked key on a testnet wallet becomes a leaked key on mainnet the moment you reuse it.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain the difference between an externally owned account and a contract account, given that both are just addresses.
- [ ] Describe what happens to the original tokens and the wrapped tokens during a wrap, and during an unwrap.
- [ ] State why 1000 tickets in must always equal exactly 1 wrapped ticket out in this lesson's design.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain why wrapping requires calling `approve` on the original token before calling `wrapToken` on the wrapper.
- [ ] Compare optimistic and ZK rollups — how each one convinces Ethereum a batch is honest, and what that costs in withdrawal time.
- [ ] Trace a token bridging from L1 to L2 and back, naming the lock, mint, burn, and release steps in order.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why `staticcall` does not make `balanceOf` trustworthy, and what the balance-delta check catches that the assert alone does not.
- [ ] Identify what goes wrong in `wrapToken` when someone deposits 1,500 tickets, and how your own contract should handle it.
- [ ] Explain why every wrapped token in existence must be backed by locked originals, and describe one attack that becomes possible the moment that invariant breaks.

---

[Assignment](ASSIGNMENT.md)

← Back to [Advanced EVM Programming](../) — Next: [Decentralized Finance](../DecentralizedFinance/)
