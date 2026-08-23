# Review — Java File I/O and Integrity Checking

*Originally covered in [File Hashing and Integrity](../README.md)*

---

Everything from the hashing-commands review, plus:

| Java | What it does |
|---|---|
| `new File("path")` | A pointer to a path — creates nothing on disk |
| `file.createNewFile()` | Create the file (false if it already exists) |
| `dir.mkdir()` / `dir.mkdirs()` | Create a directory / nested directories |
| `file.exists()` / `isFile()` / `isDirectory()` | Inspect what a path points at |
| `new FileWriter("path")` + `write()` + `close()` | Write text into a file |
| `MessageDigest.getInstance("SHA-256")` | Java's built-in SHA-256 engine |

---

## Tasks

1. Write a Java program that creates a directory `IntegrityCheck` containing a file `data.txt` with one sentence of your choice, using `File`, `mkdir()`, and `FileWriter` inside a try/catch for `IOException`.
2. From the terminal, hash the file the program produced with `sha256sum` (or `shasum -a 256`) and record the hash.
3. Run your Java program again without changing anything, rehash, and confirm the hash is identical — determinism end to end.
4. Edit one character of the sentence in your Java code, rerun, rehash, and confirm the hash avalanches.
5. Explain in two sentences how you could use this hash to prove to someone that a file they downloaded from you was not corrupted or tampered with in transit.
