# Assignment — MVP and Merge Discipline

**Due:** Next class

**Points:** 980

---

## Instructions

Ship a **working MVP** to `main`:

1. Finish your issue's work in its feature branch
2. Follow the six-step workflow: update `main` locally, checkout your branch, **merge `main` into your branch**, test on the branch, push, then open a PR to `main`
3. Include a **Test Evidence** section in the PR description (commands run, MVP flows checked, expected vs actual, tester names — not the author)
4. Have a **non-author** who was not working on the same feature review and merge your PR
5. After the merge, pull `main` and run the MVP end to end one more time

> **Warning:**
> This is a 980-point assignment. If any part of the product is not working and you were earlier responsible for it — by coding it or by accepting the pull request that merged it — that code falls under your responsibility.

---

## Grading Rubric (980 points total)

| Category | What "full credit" looks like | Points |
|---|---|---|
| **#1 Track work with Issues** | Issue(s) show clear scope, assignee, status updates. Assignees for each issue show who verified and who coded, with references to PR(s) if not a feature branch. | 120 |
| **#2 Individual work done in a branch + clean commits** | Feature work isolated to a branch; commits are relevant; branch matches the issue scope; no mystery code dumps. | 140 |
| **#3 PR review + merge discipline** | PR opened to `main` (or merged into feature branch); **non-author review** happens; reviewer leaves meaningful notes/checks or merges. Author does not self-merge (unless documented exception). | 160 |
| **#4 Integration hygiene: merge `main` into branch BEFORE PR + resolve conflicts** | Evidence in PR/commit history that `main` was merged into the branch prior to the final PR merge; conflicts resolved without breaking functionality. | 160 |
| **#5 Testing & verification (required evidence)** | **Test Evidence** section includes commands run, MVP flows verified, expected/actual, and tester name(s) (not the author). Tests pass / app runs on `main`. | 200 |
| **#6 Documentation & handoff** | README/docs cover how to run, how to test, MVP scope, known issues/next steps. Another team member can follow it. | 100 |
| **#7 MVP Gate (did you meet MVP?)** | `main` contains a **working MVP**: smallest end-to-end core value, demo-ready, no crashes in the core flow. | 100 |
| **Total** | | **980** |

**MVP Gate scoring (#7):**

- **100** = MVP works end-to-end on `main` (demo-ready)
- **70** = core flow completes but minor issues
- **30** = partial / major blockers
- **0** = not functional on `main`

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Issue tracked** — your final issue shows scope, assignee, status, and who coded vs who verified
- [ ] **Branch is clean** — your work is isolated to a branch whose commits match the issue's scope
- [ ] **Main merged in first** — your branch's history shows `main` was merged into it (and conflicts resolved) before the final PR
- [ ] **Tested after integration** — happy path, one failure case, and a regression check all pass after merging `main` in
- [ ] **PR has Test Evidence** — the PR description contains all four Test Evidence fields, with a tester who is not the author
- [ ] **Non-author merged it** — someone who was not working on the same thing reviewed and merged your PR into `main`
- [ ] **MVP runs on main** — the core flow runs end-to-end from `main` with no crashes

---

## Submission

Submit **one text response** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Final issue URL:               https://github.com/
Branch URL for this issue:     https://github.com/
PR into main (merged):         https://github.com/
Who reviewed and merged it:    
Tester name(s) in PR evidence: 
```

> **Note:**
> The PR must be properly merged into `main`, and the person who merged it must be someone who was **not** working on the same feature. A self-merged PR does not satisfy this assignment.
