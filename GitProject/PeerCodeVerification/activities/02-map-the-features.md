# Activity — Map the Features

*Concept: Before you can judge whether code works, you have to know which piece of it is supposed to do what — a feature map turns a pile of methods into a checklist you can test.*

![Diagram of a feature map: on the left, a source file Git.java listing methods such as main, initRepo, sha1, writeBlob, and addToIndex; arrows connect each method to a row on the right in a table of the four Part 2 milestones — GP-2.1 init, GP-2.2 hash, GP-2.3 blob, GP-2.4 index — with columns for what the method takes in and what it writes. main is marked empty with a note to add a Verify.java driver.](../assets/map-the-features.svg)

## Task

1. Open `Git.java` and any other `.java` files in your fork. Find `main`. Write down what happens when it runs: nothing, prints something, or calls other methods.
2. Copy this table into your notes and fill in one row per milestone, using the **actual method names** from their code:

   | Milestone | Method name(s) | Takes in | Produces or writes |
   |---|---|---|---|
   | GP-2.1 init | | | |
   | GP-2.2 hash | | | |
   | GP-2.3 blob | | | |
   | GP-2.4 index | | | |

3. Pick the method that stages a file (blob plus index) and read it top to bottom. Note where the file content is held (a `String`? a `byte[]`?), how the path to `git/objects/<hash>` is built, and what happens if a blob with that name already exists.
4. Highlight anything that would stop the code from running on your machine — an absolute path such as `/Users/theirname/...`, a file that is assumed to exist, an empty `main`. Write it down **before** you change anything; it goes in your table.
5. If `main` does not exercise the methods, create a new file `Verify.java` in your fork with a `main` that calls them in order: init, then stage a file. Do not edit their methods — your job is to test them, not to fix them.
