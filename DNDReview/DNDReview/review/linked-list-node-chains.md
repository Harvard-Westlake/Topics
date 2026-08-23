# Review — Linked List Node Chains

*Originally covered in [DNDReview](../README.md)*

---

| Concept | Reference |
|---|---|
| Node | `data` + a `next` reference to the following node (`null` at the end) |
| Insert at beginning | Point the new node at the old head, then move `head` — O(1) |
| Traversal | Walk `current = current.getNext()` until `null` — O(n) |
| Access by index | No direct indexing — must traverse from `head` |

```java
public class Node {
    private int data;
    private Node next;

    public Node(int data) {
        this.data = data;
        this.next = null;
    }

    // Assume proper getters and setters exist for every field:
    // getData(), setData(int), getNext(), setNext(Node)
}
```

---

## Tasks

1. **Predict the output**, then check yourself by tracing each reference. Draw the chain (boxes and arrows) before answering.

   ```java
   Node head = new Node(10);
   head.setNext(new Node(20));
   head.getNext().setNext(new Node(30));

   Node newNode = new Node(5);
   newNode.setNext(head);
   head = newNode;

   Node current = head;
   while (current != null) {
       System.out.print(current.getData() + " -> ");
       current = current.getNext();
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
       while (current.________() != null) {   // stop ON the last node, not past it
           current = current.getNext();
       }
       current.________(newNode);             // attach the new node to the chain
   }
   ```

3. **Fix the bug.** This insert-at-beginning loses the entire list. Explain exactly which reference is destroyed and in what line order the two statements must run.

   ```java
   public void insertAtBeginning(int data) {
       Node newNode = new Node(data);
       head = newNode;              // BUG lives in this ordering
       newNode.setNext(head);
   }
   ```
