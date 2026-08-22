<div align="center">

# Branches
*<font color="#8b949e">Diverging lines of history — the simplest Git-compliant implementation</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

> **Note:**
> This part of the Git Project has not yet been fully specced. Content will be added here when the lesson design is finalized.

## <font color="#388bfd">What This Part Will Cover</font>

- How Git stores branches as files — the simplest possible representation
- Pointing HEAD to a branch name instead of a commit hash directly
- Creating a new branch (`git branch`) and switching to it (`git checkout`)
- How commits advance the active branch pointer
- How this connects to the `checkout` functionality from Part 4

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain what a branch pointer is and what it stores.
- [ ] Describe how HEAD changes meaning when branches are introduced.
- [ ] Explain why creating a branch does not copy any files or commit objects.

### <font color="#79c0ff">Intermediate</font>

- [ ] Implement branch creation so that the branch file stores the current HEAD commit hash.
- [ ] Implement HEAD so it stores a branch name (e.g. `ref: refs/heads/main`) rather than a commit hash directly.
- [ ] Switch branches and verify that HEAD now points to the new branch.

### <font color="#79c0ff">Advanced</font>

- [ ] Commit on two different branches and show that each branch pointer advances independently.
- [ ] Explain what "detached HEAD" means in the context of your implementation.
- [ ] Describe what would need to change in `commit()` to support the branch pointer update pattern.

---

← [Commits](../Commits/) — Back to [Git Project](../)
