# Activity — Map the Tree Methods

*Concept: Part 3 is three cooperating pieces — the index format, one directory's tree, and the loop that builds every tree — and you cannot judge any of them until you know which method is which.*

![Diagram of a Part 3 feature map: on the left, a source file Git.java listing methods such as add, createTree, createTreeFromIndex, and main; arrows connect each method to a row in a table of the three Part 3 milestones — GP-3.1 index stores relative paths, GP-3.2 createTree writes one directory's tree, GP-3.3 createTreeFromIndex builds the root — with columns for what the method takes in and what it writes. A red flag marks any call to File.listFiles, because trees must come from the index, never from the folder on disk.](../assets/map-the-tree-methods.svg)

## Task

1. Open `Git.java` and any other `.java` files in your fork. Find `main`, and write down whether it does nothing, prints something, or calls the tree methods.
2. Copy this table into your notes and fill in one row per milestone, using the **actual method names** from their code:

   | Milestone | Method name(s) | Takes in | Produces or writes |
   |---|---|---|---|
   | GP-3.1 index stores relative paths | | | |
   | GP-3.2 one directory's tree | | | |
   | GP-3.3 root tree from the index | | | |

3. Find where the working list is built. Note its data type (a `List<String>`? an `ArrayList` of objects? a `TreeMap`?) and the line that **sorts** it. No sort is a finding: the tree files may come out in a different order on a different run.
4. Find how `createTree` decides which entries belong to a directory. Write down the expression, for example `path.substring(0, path.lastIndexOf('/'))`. Then find the line that writes each tree line and check whether it writes the final name or the whole path.
5. Search the whole project for `listFiles`, `Files.walk`, and `isDirectory`. Any of these inside the tree code means it is reading the folder on disk instead of the index. Write down the method name; this is the behavior 5 trap.
6. If `main` does not exercise these methods, create a new file `Verify.java` in your fork with a `main` that calls init, stages the test files, and calls their root-tree method. Do not edit their methods.
