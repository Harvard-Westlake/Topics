<div align="center">

# Initialization and Blobs
*<font color="#8b949e">Build the repository structure, hash files, and store them as blobs</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">What You'll Build</font>

| Milestone | What it does |
|---|---|
| GP-2.1 | `init()` — creates the `git/`, `git/objects/`, `git/index`, and `git/HEAD` structure |
| GP-2.2 | `hashFile()` — computes SHA-1 hash of any file's contents |
| GP-2.3 | `addBlob()` — stores a file in `objects/` under its hash |
| GP-2.4 | `updateIndex()` — records the hash and path in the index file |

By the end of this part, running your program should:
1. Create the `git/` directory structure
2. Accept a file path as input
3. Hash the file, copy it to `objects/`, and record it in `index`

## <font color="#388bfd">Read Before Starting</font>

- [BLOBs](../Docs/blobs.md) — how content-addressed storage works
- [Index File](../Docs/index-file.md) — what the index tracks and its format

## <font color="#388bfd">Design Note: git/ Stays Out of .git/</font>

Your program creates a `git/` directory in the project root. This is separate from the `.git/` folder that real Git uses for your project's version control. The `.gitignore` from Part 1 prevents your `git/` folder from being accidentally committed to GitHub.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you explain what `init()` creates and why each file or folder is needed?
- [ ] Can you verify your SHA-1 hash against an online tool to confirm it is correct?
- [ ] Can you describe what is stored in a blob file — what the filename is and what the content is?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement `init()` so that calling it twice does not overwrite the existing structure?
- [ ] Can you stage two files with identical content and show that only one blob is created but two index entries exist?
- [ ] Can you stage a modified file and show that the index entry updates to the new hash?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you write a tester that creates files, stages them, and verifies the blob files and index entries programmatically?
- [ ] Can you explain why identical file content produces a single blob, and why that is useful for storage efficiency?
- [ ] Can you explain what would go wrong if two different files happened to produce the same SHA-1 hash (a collision)?

---

[Assignment](ASSIGNMENT.md)

← [Project Setup](../ProjectSetup/) — Next: [Trees](../Trees/)
