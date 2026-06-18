<div align="center">

# The Index File
*<font color="#8b949e">Git's staging area — which files are queued for the next commit</font>*

</div>

---

## <font color="#388bfd">What is the Index?</font>

The **index** (also called the staging area) is a plain text file at `git/index`. It lists every file currently staged for the next commit, one file per line.

**Staging is the verb. Index is the noun.**

Files are not tracked automatically — they must be explicitly staged with `add`. Only staged files appear in commits.

## <font color="#388bfd">The Staging Workflow</font>

```bash
echo "Content" > file.txt     # create a file
git add file.txt              # stage it — creates blob, updates index
git status                    # shows what is and isn't staged
git commit -m "Add file"      # reads index to build the commit snapshot

echo "New content" > file.txt # modify the file
git add file.txt              # stage the change — new blob, updated index entry
git commit -m "Update file"   # new commit
```

Each time `add` runs, Git:
1. Computes the SHA-1 hash of the file's content
2. Creates a blob in `git/objects/<hash>`
3. Writes or updates the corresponding line in `git/index`

## <font color="#388bfd">Index File Format (Your Implementation)</font>

Each line contains the SHA-1 hash and the file's relative path, separated by a single space:

```
4377a91cdfd44db9a9bbf056849c7da0fc6cc7be myProgram/README.md
0a4d55a8d778e5022fab701977c5d840bbc486d0 myProgram/Hello.txt
0acc46ad73849ea9832f600de83a014c9db9cdf0 myProgram/scripts/Cat.java
```

Rules:
- One file per line
- No trailing space after the path
- No blank line at the end of the file
- Paths are relative to the project root

## <font color="#388bfd">Handling Edge Cases</font>

| Situation | What your code should do |
|---|---|
| New file staged | Append a new line |
| Same file, content unchanged | Do nothing (no-op) |
| Same file, content changed | Replace existing line with new hash |
| Same content, different path | Two separate entries (same hash, different paths) |
| Same filename, different directories | Two separate entries (different paths) |

## <font color="#388bfd">What the Index Does Not Contain</font>

The index lists **files only** — not directories. Directory structure is derived from file paths at commit time when trees are built. You will never write a directory name directly to the index.

> **Note:**
> Real Git's index is a binary file with extra metadata (permissions, timestamps, stage numbers). In this project, your simplified index stores only what you need: hash and path.

---

← Back to [Docs](README.md) | [Git Project](../../)
