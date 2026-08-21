# Assignment — Tokens in Java

*Lesson: [Tokens in Java](README.md)*

**Due:** Next class

---

Build and personalize your ticketing token, and prove you understand every line. This is Part 1 of the token project — the same program becomes a real on-chain currency in [Deploying an ERC20 Token](../ERC20Deployment/ASSIGNMENT.md), where the combined project is graded.

## Steps

1. Open VS Code and create a new Java file named `TicketToken.java`.
2. Copy in the [starter code](starter/TicketToken.java) exactly, then run it and test every menu option.
3. Personalize it — the `=== CHANGE THESE ===` comments mark the spots:
   - Change the **ticket name** to your own invention.
   - Change the **creator name** to your name.
   - Change the **initial giveaways** to real classmates and your own amounts.
4. Read every comment in the code so you fully understand how it works.
5. Show the running program to a classmate and **explain how `transfer` and `giveTickets` work**, including what each does to `totalSupply` and which line stops overspending. Have them sign off (you will name them in the submission).

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Program runs** — it compiles and the menu loop works for all five options
- [ ] **Personalized** — ticket name, creator name, and initial giveaways are yours, not the starter's
- [ ] **Mint demonstrated** — you minted tickets to someone and the total supply grew accordingly
- [ ] **Rejection demonstrated** — you attempted a transfer larger than a balance and the program refused it
- [ ] **Explained to a classmate** — a classmate heard your line-by-line walkthrough of `transfer` and `giveTickets`

---

## Submission

Submit **both text and a screenshot** on Canvas.

### Text response

Copy the stencil, fill in each line, and paste it into the Canvas text box:

```
My token name:                       
Classmate I explained the code to:   
What transfer does to totalSupply:   
What giveTickets does to totalSupply:
Line/check that stops overspending:  
```

### Screenshot

Your terminal showing the program running with **your** token name visible, including one successful transfer and one REJECTED insufficient-balance attempt in the output.
