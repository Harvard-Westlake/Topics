<div align="center">

# Commits
*<font color="#8b949e">Chain snapshots into a history — and read a classmate's code to build it</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">What You'll Build</font>

| Milestone | Whose code | What it does |
|---|---|---|
| GP-4.1 | Your classmate's | Run their tester, trace the root tree, verify the snapshot |
| GP-4.2 | Your classmate's | Add `commit()` — build trees from index, write commit file, update HEAD |
| GP-4.3 | Your classmate's | Wrap everything in `GitWrapper` with a standardized interface |

All work in this part happens in a classmate's codebase. You will clone their repository, read their code, understand their design decisions, and add the commit functionality on top.

## <font color="#388bfd">Read Before Starting</font>

- [Commits](../Docs/commits.md) — commit file format, the HEAD chain, step ordering

## <font color="#388bfd">Working in Someone Else's Code</font>

Before writing a single line, read:
1. Their `README.md` — how to run their program, what their methods do
2. Their `Git.java` (or equivalent) — how they structured their classes and methods
3. Their tester — what inputs they use and what the expected output is

Do not refactor their code unnecessarily. Your job is to extend it. If something is missing or broken, document it in a README update before you start fixing.

> **Note:**
> If the program does not compile or run as expected, document the issue and the fix in the README. You will receive credit for identified and corrected bugs.

## <font color="#388bfd">The GitWrapper</font>

The final milestone wraps everything in a single class with a fixed interface. The `GitWrapper` exists so the entire project can be tested through one consistent API — the same methods, same signatures, regardless of how different students designed the internals.

`GitWrapper` methods must be **static**. Do not change the method signatures.

## <font color="#388bfd">HEAD Update Must Come Last</font>

In the commit sequence, `git/HEAD` must be updated as the very last step. Writing HEAD before the commit file is saved would leave HEAD pointing to a file that does not yet exist if anything fails in between.

See [Docs/commits.md](../Docs/commits.md) for the full ordered sequence.

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you clone a classmate's repository, read their README, and run their tester successfully?
- [ ] Can you identify the root tree in their `objects/` folder and trace its contents manually?
- [ ] Can you explain the structure of a commit file and what each field stores?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you implement `commit()` so that the first commit has no parent field and all subsequent commits reference the previous HEAD?
- [ ] Can you verify that calling `commit()` twice produces two commit files where the second's parent field matches the first's hash?
- [ ] Can you implement `GitWrapper` without changing the method signatures?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you implement `checkout(commitHash)` — restoring all files to the state of a specific prior commit?
- [ ] Can you explain why HEAD is updated last in the commit sequence?
- [ ] Can you describe what would happen to the commit chain if two commits had the same content, author, and timestamp?

---

[Assignment](ASSIGNMENT.md)

← [Trees](../Trees/) — Back to [Git Project](../)
