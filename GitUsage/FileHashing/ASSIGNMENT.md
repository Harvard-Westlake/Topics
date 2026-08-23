# Assignment — File Hashing and Integrity

*Lesson: [File Hashing and Integrity](README.md)*

**Due:** Next class

---

## Part 1 — Build the File System

Create a new repository named `file-hasher` (initialize it locally with `git init`, then create it on GitHub and push — the Day 1 workflow). Inside it, write a Java program `FileHasher.java` whose `main` method:

1. Creates a directory named `JavaFileSystem`
2. Creates three text files inside it: `notes.txt`, `data.txt`, and `log.txt`
3. Writes a different one-sentence message into each file
4. Reads each file back and prints its contents to the console
5. Creates a subdirectory `JavaFileSystem/Backup` and writes the combined contents of all three files into `Backup/backup.txt`

Commit after each working step with a descriptive message, e.g.:

```
(FH-1): Program creates the JavaFileSystem directory
(FH-2): Program generates the three text files with messages
(FH-3): Program reads files back and builds backup.txt
```

> **Note:**
> Add a `.gitignore` that excludes compiled `.class` files before your first commit — you know how from Day 2.

---

## Part 2 — Implement hashFile()

Add a method to `FileHasher.java`:

```java
/**
 * Reads the file at filePath and returns its SHA-256 hash
 * as a lowercase hexadecimal string.
 */
public static String hashFile(String filePath) throws IOException
```

Requirements:

1. Read the entire contents of the file at `filePath`
2. Hash the contents with `MessageDigest.getInstance("SHA-256")`
3. Convert the resulting bytes to a 64-character hexadecimal string and return it
4. Handle a missing file with a clear error message rather than a raw crash (catch the exception where you call the method)

In `main`, call `hashFile` on each of your three files and print each name alongside its hash.

Commit with:

```
(FH-4): Added hashFile method with SHA-256
```

---

## Part 3 — Verify Against the Terminal

Prove your Java implementation is correct by cross-checking it against the terminal's implementation:

1. Run your program and copy the hash it prints for `notes.txt`
2. In the terminal, run `sha256sum JavaFileSystem/notes.txt` (macOS: `shasum -a 256 JavaFileSystem/notes.txt`)
3. The two 64-character strings must match exactly — two independent implementations, one fingerprint
4. Then test the edge cases from class: hash an **empty** file (create `empty.txt`) and confirm your program's output matches the terminal's, and hash a file after changing **one character** and confirm the output avalanches

Commit with:

```
(FH-5): Verified hashFile against sha256sum, including empty-file case
```

Push everything to GitHub.

---

## Success Criteria

Before submitting, confirm each of the following:

- [ ] **Repository created and pushed** — `file-hasher` exists on GitHub with a `.gitignore` excluding `.class` files
- [ ] **File system built by code** — running the program creates `JavaFileSystem/`, the three text files, and `Backup/backup.txt`
- [ ] **hashFile implemented** — returns a 64-character lowercase hex SHA-256 string
- [ ] **Exception handling present** — a missing file produces a clear message, not a raw stack trace
- [ ] **Terminal verification done** — program output matches `sha256sum` for a normal file AND an empty file
- [ ] **History tells the story** — at least five commits with the `(FH-N)` prefixes above

---

## Submission

Submit **one text response** and **one screenshot** on Canvas.

### Text response

```
Repository URL:                    https://github.com/
notes.txt SHA-256 (from Java):     
notes.txt SHA-256 (from terminal): 
Empty file SHA-256:                
One sentence — why the two implementations must agree:
```

### Screenshot

Take a screenshot showing your terminal with **both** hash outputs visible — your Java program's printed hash for `notes.txt` directly above or below the `sha256sum` output for the same file — so the match is verifiable at a glance.
