# Review — Graphs, Trees, and Traversal

*Originally covered in [DNDReview](../README.md)*

---

| Concept | Reference |
|---|---|
| Adjacency list | One ArrayList of neighbors per node |
| DFS | Go deep before backtracking — recursion (or a stack) |
| BFS | Visit level by level — a queue; shortest paths in unweighted graphs |
| Tree | Connected, acyclic, exactly n − 1 edges for n nodes |
| BST property | Left subtree keys smaller, right subtree keys larger — balanced gives O(log n), degenerate gives O(n) |

```java
import java.util.ArrayList;

// Undirected graph: nodes 0..4, neighbors stored per node
ArrayList<ArrayList<Integer>> neighbors = new ArrayList<>();
for (int node = 0; node < 5; node++) {
    neighbors.add(new ArrayList<Integer>());
}
// edge helper: add each endpoint to the other's list
```

---

## Tasks

1. **Trace a DFS.** Build the undirected graph with edges (0–1), (0–2), (1–3), (2–4) — add both directions to the adjacency lists, smaller node first in each list. Then trace this recursive DFS from node 0 and write the exact visit order printed.

   ```java
   public static void dfs(int node, ArrayList<ArrayList<Integer>> neighbors, boolean[] visited) {
       visited[node] = true;
       System.out.print(node + " ");
       for (int neighbor : neighbors.get(node)) {
           if (!visited[neighbor]) {
               dfs(neighbor, neighbors, visited);
           }
       }
   }
   ```

2. **Complete a BFS.** An ArrayList used queue-style (`add` at the back, `remove(0)` from the front) visits nodes level by level. Fill in the two blanks, trace the visit order from node 0 on the same graph, and answer: why does BFS — not DFS — find shortest paths in an unweighted graph?

   ```java
   public static void bfs(int start, ArrayList<ArrayList<Integer>> neighbors, boolean[] visited) {
       ArrayList<Integer> queue = new ArrayList<>();
       queue.add(start);
       visited[start] = true;
       while (queue.size() > 0) {
           int node = queue.remove(________);        // FIFO: take from which end?
           System.out.print(node + " ");
           for (int neighbor : neighbors.get(node)) {
               if (!visited[neighbor]) {
                   visited[neighbor] = true;
                   queue.________(neighbor);          // and join at which end?
               }
           }
       }
   }
   ```

3. **Shape a BST.** Using this insert, draw the tree produced by inserting `8, 3, 10, 1, 6` in that order. Then give an insertion order of those same five keys that degenerates the tree into a chain, and state what happens to search cost when it does.

   ```java
   public static TreeNode insert(TreeNode root, int key) {
       if (root == null) return new TreeNode(key);
       if (key < root.getKey()) root.setLeft(insert(root.getLeft(), key));
       else                     root.setRight(insert(root.getRight(), key));
       return root;
   }

   class TreeNode {
       private int key;
       private TreeNode left;
       private TreeNode right;

       public TreeNode(int key) { this.key = key; }

       // Assume proper getters and setters exist for every field:
       // getKey(), getLeft(), setLeft(TreeNode), getRight(), setRight(TreeNode)
   }
   ```
