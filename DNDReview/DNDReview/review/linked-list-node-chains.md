# Review — Linked List Node Chains

*Originally covered in [DNDReview](../README.md)*

---

| Concept | Reference |
|---|---|
| Node | `data` + a `next` reference to the following node (`null` at the end) |
| Insert at beginning | Point the new node at the old head, then move `head` — O(1) |
| Traversal | Walk `current = current.next` until `null` — O(n) |
| Access by index | No direct indexing — must traverse from `head` |

```java
public class Node {
    int data;
    Node next;

    public Node(int data) {
        this.data = data;
        this.next = null;
    }
}
```

---

## Tasks

1. **Predict the output**, then check yourself by tracing each reference. Draw the chain (boxes and arrows) before answering.

   ```java
   Node head = new Node(10);
   head.next = new Node(20);
   head.next.next = new Node(30);

   Node newNode = new Node(5);
   newNode.next = head;
   head = newNode;

   Node current = head;
   while (current != null) {
       System.out.print(current.data + " -> ");
       current = current.next;
   }
   System.out.println("null");
   ```

2. **Complete the method.** `insertAtEnd` must walk to the last node and attach the new one. Fill in the two blanks, then state the time complexity and why it differs from inserting at the beginning.

   ```java
   public void insertAtEnd(int data) {
       Node newNode = new Node(data);
       if (head == null) {
           head = newNode;
           return;
       }
       Node current = head;
       while (________ != null) {   // stop ON the last node, not past it
           current = current.next;
       }
       ________ = newNode;          // attach the new node to the chain
   }
   ```

3. **Fix the bug.** This insert-at-beginning loses the entire list. Explain exactly which reference is destroyed and in what line order the two statements must run.

   ```java
   public void insertAtBeginning(int data) {
       Node newNode = new Node(data);
       head = newNode;          // BUG lives in this ordering
       newNode.next = head;
   }
   ```
