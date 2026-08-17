# Review — Merge Main Into Your Branch First

*Originally covered in [MVP and Merge Discipline](../README.md)*

---

| Step | Action |
|---|---|
| 1 | Checkout `main`, **Pull** — local `main` matches `origin/main` |
| 2 | Checkout your feature branch |
| 3 | Merge `main` **into** the feature branch; resolve conflicts |
| 4 | Test on the branch: happy path, one failure case, regression check |
| 5 | Push the updated feature branch |
| 6 | Open PR to `main` with a **Test Evidence** section; non-author reviews and merges |

Test Evidence fields: commands run · flows checked · expected vs actual · tester name(s) (not the author).

Terminal equivalent of steps 1–3: `git checkout main && git pull`, `git checkout <branch>`, `git merge main`.

---

## Tasks

1. In your repository, update local `main` from the remote and confirm it matches `origin/main`.
2. Checkout a feature branch that is at least one commit behind `main` (create one from an old commit if needed).
3. Merge `main` into that branch. If a conflict appears, resolve it and complete the merge commit.
4. Run the app (or tests) **on the branch** and perform all three minimum checks: happy path, one failure case, one regression check.
5. Push the branch, open a PR to `main`, and write a complete Test Evidence section in the description.
6. Have a non-author review and merge the PR, then pull `main` and re-run the happy path from `main`.
