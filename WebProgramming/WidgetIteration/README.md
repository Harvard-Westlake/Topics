<div align="center">

# Widget Iteration from Feedback
*<font color="#8b949e">Turning human feedback into a shrinking feedback.md and an error-free widget</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Getting Human Feedback](#getting-human-feedback)**  
Why you cannot review your own work — and what only other humans can tell you.

**[The feedback.md Workflow](#the-feedbackmd-workflow)**  
A file that starts full and shrinks to zero as you implement.

**[Quality Assurance: A Silent Console](#quality-assurance-a-silent-console)**  
Zero errors on load, zero errors during use.

**[Updating the Pull Request](#updating-the-pull-request)**  
Your PR is a living document — keep it current.

---

## <font color="#388bfd">Getting Human Feedback</font>

How did we get useful human feedback? And why couldn't you do this on your own?

Because you built the widget, you are the one person on Earth who cannot experience it fresh. You know which parts are buttons, what order the sections go in, and what every label means — so your brain autocompletes past every confusing spot. This is the **curse of knowledge**: the better you understand your own design, the worse you are at seeing its problems.

Fresh users are walking [heatmaps](../UXAndBehaviorTracking/): watch where they hesitate, what they click that isn't clickable, where they ask "what now?" — and write down their *exact words*, not your interpretation of them.

| You see | A fresh user sees |
|---|---|
| The obvious start button | Three equally-weighted boxes, none saying "start" |
| A clever minimalist icon | A mystery symbol they are afraid to click |
| The intended order of sections | A page they read bottom-to-top on a phone |

> **Note:**
> Feedback stings precisely when it is useful. "I didn't know what to do" is not an insult — it is a reproducible bug report against your design.

---

## <font color="#388bfd">The feedback.md Workflow</font>

Feedback that lives in your memory evaporates. Feedback that lives in your repository gets implemented. Today's workflow:

1. Add a `feedback.md` file to your repository containing the **exact feedback** taken from your peers
2. **Commit** the `feedback.md`
3. As you continue to code, **continually reduce** the size of `feedback.md` — every implemented item gets deleted from the file
4. When the file is empty and no longer needed, **delete it**

```
feedback.md over time:

commit 1:  10 items   (all feedback, verbatim)
commit 4:   6 items   (four implemented, removed)
commit 7:   2 items   (six implemented)
commit 9:   file deleted - every item implemented
```

The Git history becomes the proof of the process: anyone reading your commits can watch the feedback arrive, shrink, and disappear.

> **Tip:**
> Keep each item's original wording until the moment it is fixed. Rewriting "I couldn't find the quiz" into "improve discoverability" launders the specific, checkable complaint into vague self-praise.

---

## <font color="#388bfd">Quality Assurance: A Silent Console</font>

After implementing the feedback, you must inspect your widget in [DevTools](../DebuggingJavaScript/) and verify:

- **0 behavioral errors happen on page load**
- **0 errors appear as your widget is used** — click every button, run every interaction, finish every flow with the console open

Fix any errors!

> **Note:**
> There is a single allowed exception: an error that comes from the browser or an installed extension rather than from your own code. If you believe an error qualifies, confirm with your teacher — every error produced by *your* code must be fixed, not explained away.

---

## <font color="#388bfd">Updating the Pull Request</font>

Your Learning Widget lives in a [pull request](../LearningWidget/), and a PR is a living document:

1. Commit and push all feedback-driven changes to your branch — the PR updates automatically
2. Add a comment to the PR summarizing what changed in response to feedback
3. Verify the deployed site reflects the latest push (`firebase deploy` again if needed)

Next lesson, a peer reviewer puts their own grade on the line by reviewing this PR — hand them something worth approving.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain the curse of knowledge and why it makes self-review unreliable.
- [ ] Describe the feedback.md workflow from first commit to deletion.
- [ ] State the two zero-error conditions your widget must meet.

### <font color="#79c0ff">Intermediate</font>

- [ ] Record a tester's feedback verbatim without softening or interpreting it.
- [ ] Verify a widget produces no console errors during every interaction, not just on load.
- [ ] Update a pull request with new commits and a summary comment.

### <font color="#79c0ff">Advanced</font>

- [ ] Use your Git history to prove every feedback item was implemented.
- [ ] Distinguish an error caused by your code from one caused by the browser or an extension.
- [ ] Prioritize conflicting feedback from two testers and justify which you implemented.

---

[Assignment](ASSIGNMENT.md)

← [UX and Behavior Tracking](../UXAndBehaviorTracking/) — Next: [Collaborative Peer Review](../PeerReview/)
