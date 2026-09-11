# Activity — Calculating Hash Table Sizes

*Concept: The formula $N \geq \frac{-k(k-1)}{2\ln(P)}$ tells you exactly how many buckets a hash table needs to keep collisions below a chosen probability, and the answer grows with $k^2$.*

![Flow diagram for sizing a hash table. Two inputs, k (the number of items to store) and P (the desired probability of no collision, such as 0.99), feed the formula N is at least negative k times k minus 1 over 2 ln P, which outputs N, the buckets needed, which grows like k squared. Two already-worked rows: 30 students at P = 0.99 gives about 43,282 lockers, and 1,000 students at P = 0.995 gives about 99,650,041 lockers. A "your turn" row lists the activity's inputs: 100,000 employees, 8 billion humans, 2 to the 62.72 grains of sand, and 2 to the 73.08 stars.](../assets/calculating-hash-table-sizes.svg)

## Task

Partner up to tackle the following exercises on determining optimal hash table sizes. Show your work for each one.

1. **Exercise #1 — A large Hash Table (Government Employees).** Suppose the US government employs 100,000 people and assigns each a random ID. How large should the range of IDs be to ensure less than a 0.1% chance that any two employees receive the same ID?
   - A. ~5,000,000,000 IDs
   - B. ~50,000,000,000 IDs
   - C. ~500,000,000,000 IDs
   - D. ~5,000,000,000,000 IDs
2. **Exercise #2 — Just a little bigger! (Humanity-Sized).** Imagine you want to store and retrieve any person within the world's population in O(1) time using, of course, a hash table! How many buckets do you need in the table so that there's less than a 1% chance that any two people end up in the same bucket? (Assume a population of 8 billion humans.)
3. **Exercise #3 — This has got to be the biggest... (Grains of Sand).** Imagine you want to analyze every grain of sand on Earth because, well... you're into that sort of thing. Of course, you want to look up any grain of sand instantly (O(1) time, naturally). How many containers do you need in your hash table so that there's less than a 1% chance that any two grains of sand collide in your storage?

   > **Hint:** Assume there are $2^{62.72}$ (or $7.5 \times 10^{18}$) grains of sand on Earth as of last Thursday.

4. **Exercise #4 — So big it hurts... my brain (Stars in the "known" Universe).** On a blue-green planet named after dirt, a bunch of barely civilized, fur-deprived primates wildly guess the number of stars in the universe to be $2^{73.08}$. If we want to store that many planet names and look them up on Google's new Solar Search Engine in O(1) time with less than a 1% chance of a stellar collision, how many buckets does our Hash Table need?
5. **Deliverable:** Scan and upload your work using a document scanning app for online submission. You will attach it to tonight's assignment.
