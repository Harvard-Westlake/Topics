# Review — Stacks and Queues Built on ArrayList

*Originally covered in [DNDReview](../README.md)*

---

| Structure | Principle | Core operations | Cost |
|---|---|---|---|
| Stack | LIFO — Last In, First Out | `push`, `pop`, `peek` | O(1) each at the end of an ArrayList |
| Queue | FIFO — First In, First Out | `add`, `remove`, `peek` | `remove` from the front of an ArrayList is O(n) |

```java
import java.util.ArrayList;

public class MiniStack {
    private ArrayList<Character> items = new ArrayList<>();

    public void push(char value)  { items.add(value); }
    public char pop()             { return items.remove(items.size() - 1); }
    public char peek()            { return items.get(items.size() - 1); }
    public boolean isEmpty()      { return items.size() == 0; }
}
```

---

## Tasks

1. **Predict the printed output** of this sequence, tracking the stack's contents after every line.

   ```java
   MiniStack stack = new MiniStack();
   stack.push('A');
   stack.push('B');
   stack.push('C');
   System.out.println(stack.pop());
   stack.push('D');
   System.out.println(stack.peek());
   System.out.println(stack.pop());
   System.out.println(stack.pop());
   ```

2. **Complete MiniQueue.** Fill in the two blanks so `remove` returns the *oldest* element. Then answer: why is this queue's `remove` O(n) when the stack's `pop` was O(1)? (Think about what the ArrayList must do to the remaining elements.)

   ```java
   import java.util.ArrayList;

   public class MiniQueue {
       private ArrayList<String> items = new ArrayList<>();

       public void add(String value) { items.add(value); }

       public String remove() {
           return items.remove(________);   // FIFO: which index leaves first?
       }

       public String peek() {
           return items.get(________);
       }

       public boolean isEmpty() { return items.size() == 0; }
   }
   ```

3. **Fix the bracket checker.** This version says `"{{}"` is balanced — it isn't. Find the missing final check and explain, in LIFO terms, why the stack must be empty at the end.

   ```java
   public static boolean isBalanced(String text) {
       MiniStack stack = new MiniStack();
       for (int position = 0; position < text.length(); position++) {
           char symbol = text.charAt(position);
           if (symbol == '{') {
               stack.push(symbol);
           } else if (symbol == '}') {
               if (stack.isEmpty()) return false;
               stack.pop();
           }
       }
       return true;   // BUG: what condition is this ignoring?
   }
   ```
