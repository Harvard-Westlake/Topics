<div align="center">

# Collaborative Peer Review
*<font color="#8b949e">Test, review, and fix your partner's code — with your name attached to the result</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Learning Objectives](#learning-objectives)**  
What you should be able to do by the end of this lesson.

**[Why Pull Request Reviews Exist](#why-pull-request-reviews-exist)**  
Independent eyes catch what authors cannot.

**[Becoming a Collaborator](#becoming-a-collaborator)**  
Getting Write access to your partner's fork.

**[The Testing Checklist](#the-testing-checklist)**  
Functional checks and behavioral checks.

**[The PR Write-Up](#the-pr-write-up)**  
Six required sections, posted on their pull request.

**[Accountability and Getting to Approvable](#accountability-and-getting-to-approvable)**  
Approving broken code costs you — approve only what has earned it.

---

## <font color="#388bfd">Learning Objectives</font>

By the end of this lesson, you will be able to:

- Add collaborators to code bases
- Become responsible for another person's code by attaching your name to their work as a reviewer

---

## <font color="#388bfd">Why Pull Request Reviews Exist</font>

Reviewing pull requests establishes a deliberate, auditable checkpoint for code quality. Independent eyes surface defects, security issues, performance regressions, and edge cases that original authors — subject to confirmation bias and local context — may miss. Multiple reviewers also align changes with project conventions, architectural boundaries, and style standards, preserving coherence across the codebase.

In professional teams, an approval is not a courtesy — it is a signature. When you click **Approve**, you are saying: *I tested this, and I stake my reputation on it working.* Today that stops being a metaphor: bugs you approve count against **your** grade.

---

## <font color="#388bfd">Becoming a Collaborator</font>

**1) Partner assignment (teacher-chosen).** Check the posted partner list.

**2) Collaborator access on the project:**

- Your partner adds you as a **Write** collaborator on their fork: **Settings → Collaborators → Add people → Write**
- Accept the invite (arrives by email and GitHub notifications)

Write access means you can do more than comment — you can propose and commit fixes directly, which this assignment expects.

---

## <font color="#388bfd">The Testing Checklist</font>

Work through both halves with the widget open, the console open, and the [rubric](ASSIGNMENT.md) in mind.

### <font color="#79c0ff">Functional</font>

- Does the app do what it claims (happy paths)?
- Is the behavior **correct** per docs/specs? Research the actual topic if unsure — a widget that teaches something *wrong* fails even if the code runs
- Any console/network/server errors on load, or when using the widgets?

### <font color="#79c0ff">Behavioral / user</font>

- Is the UX engaging and responsive?
- Is the UI intuitive — labels, flows, empty and error states?
- Does the UI match the `/admin` [learn.hw.com](https://learn.hw.com) page design and theme?

> **Tip:**
> Try to break it on purpose: click things twice, refresh mid-interaction, enter nonsense in inputs, resize the window. A reviewer who only follows the happy path finds only happy-path bugs.

---

## <font color="#388bfd">The PR Write-Up</font>

Post a review comment on your partner's PR with these sections:

| Section | What goes in it |
|---|---|
| **Functional** | Do the core flows work? What did you test? |
| **Correctness** | Does the behavior match reality/spec? What did you verify against? |
| **Errors** | Every console/network error you observed, with repro steps |
| **UX** | Engagement, responsiveness, clarity of feedback and states |
| **UI vs /admin** | Where the visuals match the `/admin` theme and where they drift |
| **Suggestions** | Concrete improvements, ordered by impact |

Include repro steps, screenshots, and links to any references you used. A finding that cannot be reproduced from your write-up does not count as reported.

---

## <font color="#388bfd">Accountability and Getting to Approvable</font>

**Call out all non-working functions and poor UX.** Missing bugs that get merged will reduce your grade for approving them.

Then close the loop — do not stop at criticism:

1. Propose or commit fixes (or formally request changes) until tests pass, errors are gone, and UX/UI issues are addressed
2. Re-test quickly after each round of fixes
3. When everything meets the checklist, **Approve** the PR

"Approvable" is a real bar: working flows, correct content, silent console, coherent UX, `/admin` parity. Your signature goes on it — make it mean something.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you add a collaborator with Write access to a repository and accept such an invite?
- [ ] Can you name the six required sections of the PR write-up?
- [ ] Can you explain what clicking Approve on a pull request commits you to?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you run the full testing checklist — functional and behavioral — on someone else's widget?
- [ ] Can you write a bug report with repro steps that a stranger could follow?
- [ ] Can you verify a widget's content is factually correct, not just that its code runs?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why reviewer accountability changes how carefully people review?
- [ ] Can you commit a fix to your partner's branch and re-test without breaking their work?
- [ ] Can you judge when a PR has crossed from "needs changes" to genuinely approvable, and defend the call?

---

[Assignment](ASSIGNMENT.md)

← [Widget Iteration from Feedback](../WidgetIteration/) — Back to [Web Programming](../)
