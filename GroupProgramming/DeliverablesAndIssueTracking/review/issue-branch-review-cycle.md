# Review — The Issue → Branch → Review Cycle

*Originally covered in [Deliverables and Issue Tracking](../README.md)*

---

| Step | Action | Rule |
|---|---|---|
| 1 | Create an Issue | One person assigned per issue; child issues link to a parent feature issue |
| 2 | Work in a branch | Never commit directly to `main`; link the branch/PR to the issue |
| 3 | Review and merge | A non-author reviews and merges; author never self-merges to `main` |

| Issue status | When |
|---|---|
| In Progress | Actively working |
| In Review | Committed, awaiting non-author verification |
| Done | Merged into feature branch, or PR into `main` closed |

Deliverable = something committed, documented, and visible every class. Too-big issue → split it, deliver the part you finished, document what is left.

---

## Tasks

1. In your team repository, create an issue for one small piece of work, assigned to only yourself.
2. Create a branch for it, make at least one commit, and push the branch.
3. Link the branch (or a pull request from it) to the issue.
4. Move the issue to In Review and ask a teammate who did not write the code to review it.
5. Have the reviewer merge the work; confirm the issue can be marked Done and closed.
6. Pretend the issue was twice as big as expected: split it into "done" and "remaining" issues, and write one sentence in each explaining the split.
