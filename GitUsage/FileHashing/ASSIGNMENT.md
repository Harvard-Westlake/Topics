# Assignment — File Hashing

*Lesson: [File Hashing](README.md)*

**Due:** Next class

---

## Instructions

For the two problems below, **state your assumptions before your calculations**. Also indicate which of the terminal hash functions (from Part 3 of the lesson) is most suitable for each problem.

Use the general form from the lesson, where $P$ is the desired probability of **no** collisions:

$$N \geq \frac{-k(k-1)}{2\ln(P)}$$

---

## Worked Example

<details>
<summary><strong>Unique Transaction IDs in a Global Payment System</strong></summary>

In a global digital payment system processing billions of transactions daily, each transaction requires a unique identifier for record-keeping and fraud prevention. How should the transaction ID space be sized to guarantee that no two transactions ever receive the same ID?

**Assumptions:**

- An average of 10 billion daily transactions globally; the transaction ID space needs to be large enough to handle at least $10^{10}$ daily transactions over approximately 100 years (or 100 × 365.25 days) without collisions.
- Assuming no increase in the number of transactions per day.
- We want less than a 0.1% chance of a duplicate transaction ID occurring within 100 years.

**Calculation:**

1. Determine the desired probability of no collisions.

$$P(\text{Collisions}) = 1 - P(\text{No Collisions})$$

$$P(\text{Collisions}) = 0.001$$

$$P(\text{No Collisions}) = 1 - 0.001$$

Therefore, the desired probability of no collisions is $P(\text{No Collisions}) = 0.999$.

2. Let $k$ be the number of daily transactions for 100 years.

$$k = 10^{10} \text{ transactions} \times 36525 \text{ days}$$

$$k = 3.65 \times 10^{14}$$

3. Solve for $N$, the number of unique identifiers required for no collisions. Substitute $k$ and $P$.

$$N \geq \frac{-k(k-1)}{2\ln(P)}$$

$$N \geq \frac{-(3.65 \times 10^{14})(3.65 \times 10^{14} - 1)}{2\ln(0.999)}$$

$$N \geq \frac{-1.33 \times 10^{29}}{-0.002001}$$

$$N \geq 6.67 \times 10^{31}$$

$$N \geq 2^{105}$$

Since we'd need a minimum of $2^{105}$ buckets to solve this problem, we can safely use the terminal command `md5sum` as it has $2^{128}$ possible outputs.

</details>

---

## Problem 1 — Unique File Data

In a global cloud storage service where users can upload any number of files, each file needs a unique identifier to prevent overwrites and ensure data integrity. Considering that files can be uploaded by billions of users, each potentially uploading thousands of files, how would you size the hash table to guarantee that no two files ever receive the same identifier by chance?

## Problem 2 — Unique Bank Accounts

Let's say any time someone wants to make a new bank account, they pick a new random account number. Any human can have as many bank accounts as they want. What's a reasonably large size hash table so that no person ever (within a time frame of your choice) accidentally picks the same account number as anyone else?

> **Note:**
> There is no single right answer to either problem. Your grade rests on whether your assumptions are stated explicitly and are reasonable, whether your calculation follows from those assumptions, and whether the hash function you pick actually has more than $N$ possible outputs.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Partner work attached** — a scan of your work from the in-class activity "Calculating Hash Table Sizes" (all four exercises) is uploaded
- [ ] **Assumptions stated first** — each problem opens with an explicit list of assumptions (how many items, over what time frame, what target collision probability) before any math
- [ ] **Calculation shown** — each problem computes $k$, then solves $N \geq \frac{-k(k-1)}{2\ln(P)}$ with the numbers substituted, ending in a value for $N$
- [ ] **Hash function chosen** — each problem names the most suitable terminal hash function from Part 3 and shows that its $2^{\text{bits}}$ outputs exceed your $N$
- [ ] **Two screenshots** — one per problem, each showing that problem's assumptions, calculation, and chosen hash function

---

## Submission

Submit **one text response** and **screenshots** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Problem 1 — k (number of files):            
Problem 1 — P (no-collision probability):   
Problem 1 — N (buckets needed):             
Problem 1 — hash function chosen:           
Problem 2 — k (number of accounts):         
Problem 2 — P (no-collision probability):   
Problem 2 — N (buckets needed):             
Problem 2 — hash function chosen:           
```

### Screenshots

Upload:

1. A scan or photo of your partner work from the in-class activity (all four exercises, both names visible).
2. One screenshot per homework problem showing the assumptions, the full calculation, and the chosen hash function together. A screenshot that shows only the final $N$ with no assumptions or work does not count.
