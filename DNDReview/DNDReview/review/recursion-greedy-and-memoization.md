# Review — Recursion, Greedy Choices, and Memoization

*Originally covered in [DNDReview](../README.md)*

---

| Concept | Reference |
|---|---|
| Recursion | A method calling itself: **base case** stops it, **recursive case** shrinks the problem |
| Greedy | Take the locally best choice each step — fast, but not always optimal |
| Dynamic programming | Overlapping subproblems, each computed once |
| Memoization | Cache each result; return the cached value on repeat calls |

---

## Tasks

1. **Trace the recursion.** For `fib(4)`, draw the full call tree of this naive version. Count the total calls, circle the base-case calls, and mark every *repeated* subproblem — the repetition is exactly what memoization will remove.

   ```java
   public static int fib(int n) {
       if (n <= 1) return n;              // base cases: fib(0) = 0, fib(1) = 1
       return fib(n - 1) + fib(n - 2);    // recursive case
   }
   ```

2. **Test the greedy strategy.** This coin counter always grabs the largest coin that still fits. Trace it for 41 cents with `{25, 10, 5, 1}` and list the coins chosen. Then rerun it by hand for 30 cents with coins `{25, 10, 1}` — compare the greedy answer against the best possible answer and state what this proves about greedy algorithms.

   ```java
   public static ArrayList<Integer> makeChange(int amount, int[] coins) {
       ArrayList<Integer> chosen = new ArrayList<>();
       for (int coin : coins) {                 // coins ordered largest to smallest
           while (amount >= coin) {
               chosen.add(coin);
               amount = amount - coin;
           }
       }
       return chosen;
   }
   ```

3. **Complete the memoized version.** The cache is a plain array where `memo[n]` holds `fib(n)`, with `-1` meaning "not computed yet." Fill in the two blanks, then answer: how many *new* computations does `fib(6)` make with the cache, versus the call count you found in Task 1's style?

   ```java
   public static int fibFast(int n, int[] memo) {
       if (n <= 1) return n;
       if (memo[n] != ________) {     // cache hit: this subproblem is already solved
           return memo[n];
       }
       int result = fibFast(n - 1, memo) + fibFast(n - 2, memo);
       ________ = result;             // store it so no future call recomputes it
       return result;
   }

   // Call with a cache filled with -1:
   int[] memo = new int[7];
   for (int position = 0; position < memo.length; position++) {
       memo[position] = -1;
   }
   System.out.println(fibFast(6, memo));   // 8
   ```
