<div align="center">

# Vyper with Custom Behavior
*<font color="#8b949e">Learn Vyper's moving parts, then write a contract with behavior you invent</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">Objective</font>

Today you get comfortable programming for the Ethereum blockchain. You will deploy code with an extra method that meets **all four** of these requirements:

1. Includes an **environment variable** in your code
2. Has at least one **assert**
3. Uses one **built-in method**: [Vyper built-in functions](https://docs.vyperlang.org/en/stable/built-in-functions.html)
4. Has a method which is **public (externally callable) with inputs and outputs**

A worked example lives in [starter/gamble_example.vy](starter/gamble_example.vy) — a `gamble()` method that lets a token holder bet tokens on the parity of the transaction's gas price. Study it; do **not** resubmit it. Your contract must be unique.

```python
@external
def gamble(_gambleAmount: uint256, _walletAddress: address) -> (bool):
    # Don't allow them to run this unless they have 50x the tokens to lose
    assert self.balanceOf[_walletAddress] > (_gambleAmount * 50), "You don't have enough to gamble"

    # If the transaction's gas price is odd, then you win the gamble amount!
    # 1/2 the time it's a win!
    if (tx.gasprice % 2 == 1):
        self.balanceOf[_walletAddress] += _gambleAmount
        self.totalSupply += _gambleAmount

    # If the transaction's gas price's mod 11 is 7, then you lose 50 times
    # the amount you gambled! 1/11 the time you lose 50x! Yikes!
    if (tx.gasprice % 11 == 7):
        self.balanceOf[_walletAddress] -= _gambleAmount * 50
    return (True)
```

Compiling and deploying works exactly as in [Writing Code on Ethereum](../WritingCodeOnEthereum/): the class platform ([https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app)) compiles your file and deploys it to Sepolia through your test wallet.

---

## <font color="#388bfd">Writing in Vyper</font>

### <font color="#79c0ff">1. Function definition syntax</font>

```python
# External means this is public and anyone can run it
@external
def myMethodName(__INPUTS__) -> (OUTPUTS):
    self._internalMethod(4)
    return (OUTPUTS)

# Internal can only be called from other methods inside this contract
@internal
def _internalMethod(_exampleInt: int256) -> (bool, bool, uint256):
    return (True, False, 15)
```

Every input and output is **typed** (`uint256`, `int256`, `bool`, `address`), and a method can return several values at once. The leading underscore on `_internalMethod` and `_exampleInt` is a Vyper naming convention for internal things.

### <font color="#79c0ff">2. Assert statements</font>

In Java you write the guard yourself:

```java
if (balanceOf[_address] < _amount) {
    throw new Exception("The user does not have enough money for this transaction");
}
```

Vyper compresses the same guard into one line — condition first, error message second:

```python
assert balanceOf[_address] >= _amount, "The user does not have enough money for this transaction"
```

If the condition is false, the whole transaction **reverts**: every state change is undone, as if the call never happened. That is your `REJECTED:` branch from TicketToken, enforced by the chain itself.

### <font color="#79c0ff">3. Environment variables</font>

The chain hands your code live facts about the current transaction:

```python
msg.sender    # the account that sent (and paid for) this transaction
tx.gasprice   # the gas price of this transaction (the gamble example bets on it)

# example: only let people spend their OWN balance
assert self.balanceOf[msg.sender] >= _amount, "Insufficient balance"
```

`msg.sender` is the single most important variable in smart contract programming — it is an identity **proven by a signature**, not typed into a text field. TicketToken trusted whatever name you entered; a contract cannot be lied to about who is calling.

### <font color="#79c0ff">4. Public / private access</font>

```python
# External means this is public and anyone can run it
@external
def myMethodName(_num: uint256) -> (bool):
    self._internalMethod(4)
    return (True)

# Internal can only be called from other methods inside this contract
@internal
def _internalMethod(_exampleInt: int256) -> (bool, bool, uint256):
    return (True, False, 15)
```

`@external` methods are your contract's buttons — anyone on Earth can press them, so every one needs its asserts. `@internal` methods are the machinery behind the panel.

---

## <font color="#388bfd">Homework</font>

Write code which meets all four objectives and is **unique from the example code**. Ideas: a tipping method, a raffle, a tax on transfers, an allowance that unlocks by block timestamp, a leaderboard. Full requirements and submission details are in the [assignment](ASSIGNMENT.md).

> **Warning:**
> Testnet only, as always — deploy with your Sepolia test wallet, and never share a private key or seed phrase with anyone.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you tell an `@external` method from an `@internal` one and say who can call each?
- [ ] Can you write a one-line Vyper assert with an error message?
- [ ] Can you name the four requirements your homework contract must meet?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you translate a Java if-throw guard into a Vyper assert, flipping the condition correctly?
- [ ] Can you explain what `msg.sender` is and why a caller cannot fake it?
- [ ] Can you walk through the gamble example and state the win case, the lose case, and what the assert protects?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain what happens to state changes made before an assert that fails?
- [ ] Can you explain why the gamble example's odds come from `tx.gasprice`, and why that is a questionable source of randomness?
- [ ] Can you design a method where forgetting a `msg.sender` check would let a stranger drain balances — and add the check?

---

[Assignment](ASSIGNMENT.md)

← [Writing Code on Ethereum](../WritingCodeOnEthereum/) — Next: [Deploying an ERC20 Token](../ERC20Deployment/)
