# Assignment — Vyper with Custom Behavior

**Due:** Next class
**Points:** 100

---

Write and deploy a Vyper contract with a custom method that meets **all four objectives** and is **unique from the example code** in [starter/gamble_example.vy](starter/gamble_example.vy).

## Requirements

Your code must:

1. Include an **environment variable** (e.g. `msg.sender`, `tx.gasprice`, `block.timestamp`)
2. Have at least one **assert** with an error message
3. Use one **built-in method** from the [Vyper built-in functions](https://docs.vyperlang.org/en/stable/built-in-functions.html)
4. Have an **@external method with inputs and outputs**

## Steps

1. Design a behavior of your own — not a gamble. Tipping, raffles, transfer taxes, time-locked allowances, and leaderboards are all fair game.
2. Write it on the class platform: [https://learn.hw.com/code/vyper-framework#/app](https://learn.hw.com/code/vyper-framework#/app)
3. Compile until clean, then deploy to **Sepolia** with your test wallet.
4. **Verify your code uses each of the objectives** — mark the line numbers where each of the four appears.
5. Push your `.vy` file to a GitHub repository so you can link to the code.

> **Warning:**
> Testnet only. Never deploy with a wallet holding real funds, and never share a private key or seed phrase with anyone.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Unique behavior** — your method does something the gamble example does not
- [ ] **All four objectives present** — environment variable, assert with message, built-in function, and an external method with inputs and outputs, each at a line you can point to
- [ ] **Compiles and deploys** — the contract deployed successfully to Sepolia
- [ ] **Code on GitHub** — the exact deployed `.vy` source is visible at a GitHub link
- [ ] **You can defend it** — you can explain what your assert rejects and what your method returns

---

## Submission

Submit **one text response** on Canvas.

### Text response

Copy the stencil, fill in each line, and paste it into the Canvas text box:

```
GitHub link to my code:            https://github.com/
Deployed contract address:         0x
Line with environment variable:    
Line with assert:                  
Line with built-in function:       
External method name (in/out):     
One sentence on what it does:      
```
