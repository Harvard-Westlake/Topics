<div align="center">

# Code Review and MVP Presentation
*<font color="#8b949e">Prove the MVP is real, demo it from main, and defend your own merged code</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

After coding sprints with your team, the next step is communicating what you did with other people at the company. Two types of review take place:

| Review type | Audience | What they need |
|---|---|---|
| **Code Review** | The engineering team | What engineering you did and how the product behaves under the hood |
| **Product Review** | Quality Assurance (user testing) and Sales | What they are using and how to use it |

Your presentation has two parts: a **team demo** that proves the MVP works on `main`, and an **individual deep dive** where each teammate defends their own merged contribution.

---

## <font color="#388bfd">Part 1 — Team MVP Demo (6 minutes total)</font>

**Purpose:** prove the MVP works **on `main`** and matches the team's stated MVP.

Required flow — you must hit all of these:

### <font color="#79c0ff">1. State the MVP in one sentence (10 seconds)</font>

Format: "Our MVP lets **[target user]** do **[core job]** so they get **[core value]**."

### <font color="#79c0ff">2. Show you are on main (10 seconds)</font>

Show the branch is `main` and the current commit hash (or the GitKraken view).

### <font color="#79c0ff">3. Run and demonstrate the happy path (3–3.5 minutes)</font>

- Walk through the exact end-to-end core flow that matches your MVP statement
- If your MVP is multi-step, show the minimum steps needed to prove value
- If your MVP is a game, play the game!

> **Note:**
> A happy path is the workflow — or the use of the game — in its most simple form that meets the requirements. No edge cases, no bad user input.

### <font color="#79c0ff">4. Close with scope and known issues (1–1.5 minutes)</font>

- Display the tech spec diagram and highlight the parts completed for the MVP
- Discuss priorities: which issues need to be done next
- If you did not get the MVP working, you must discuss every item left to get it working and show where each one sits on the tech spec

**Hard rules:**

- The demo must run from **`main`**, not a feature branch
- The demo must be **end-to-end** — no "imagine this part works"
- If the demo requires seed data or environment variables, that must be documented and reproducible

---

## <font color="#388bfd">Part 2 — Individual Technical Deep Dive (2 minutes per teammate)</font>

**Purpose:** show that each teammate understands and can explain their **real merged technical contribution**.

Each teammate presents **their own** work and must show code that is **in `main`**. Your two minutes must cover four things:

1. **What you owned (10–15 seconds)** — the section of the tech spec you individually solved, plus your **Issue + PR** (point to them quickly)
2. **Show a code snippet from main (30–45 seconds)** — roughly **10–25 lines** you materially contributed (not a whole-file scroll), with the **file path + function/class/component name**, and who checked this code
3. **Explain the technical challenge and the solution (45–60 seconds)** — what was hard, broken, or risky? What did you change, and why did it fix it?
4. **Verification evidence + who reviewed it (10–15 seconds)** — the test you ran, scenario you verified, log/response you validated, or game instance you ran — and who verified the code when it went into `main`

> **Warning:**
> Even if you used AI, you still need to explain *why this solution is correct* and *how you verified it*. "AI wrote it" is not an explanation.

---

## <font color="#388bfd">The 3 required questions</font>

Every student must answer all three. They are designed to reveal whether you actually understand your code and your integration work. You may prepare notes, but your answers must reference **your specific code in `main`** — names, paths, data shapes, and behavior.

### <font color="#79c0ff">Question 1 — Trace the real execution path (280 points)</font>

*"When a user triggers the feature I worked on, what is the exact execution path through our code?"*

Point to **your file(s)** and walk through:

- The **entry point** (UI event / API route / handler)
- The **next 2–4 functions or components** it calls, by name
- The **data shape** as it moves — what fields exist, what changes
- Where **validation** happens and what happens on invalid input

This cannot be answered generically — it requires knowing your exact structure and names.

### <font color="#79c0ff">Question 2 — Which part of the tech spec did this complete? (35 points)</font>

*"The highlighted section of the tech spec is the portion of the code this completed."*

Describe which part of the tech spec your code in `main` completed. Generic "we added try/catch" answers do not score — you must explain the behavior or section of the tech spec relative to the app.

### <font color="#79c0ff">Question 3 — What code did this integrate with? (35 points)</font>

*"This code has to integrate with..."*

Explain what part of your code interfaces with what other sections of code. This forces you to understand coupling, data flow, and tests in your codebase.

---

## <font color="#388bfd">What this phase is really about</font>

This phase is not about having the most features. It is about proving:

- The MVP is **real and demoable**
- The team can **ship from `main`**
- Each person can explain and defend the correctness of their work — including AI-assisted code — through **review + testing + technical clarity**

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain the difference between a code review and a product review, and who each is for.
- [ ] State your team's MVP in one sentence using the target-user / core-job / core-value format.
- [ ] Show that a demo is running from `main`, including the commit hash.

### <font color="#79c0ff">Intermediate</font>

- [ ] List the four required parts of the individual deep dive and the time budget for each.
- [ ] Pick a 10–25 line snippet from `main` that you materially contributed, with its file path and function name.
- [ ] Present your work's scope and known issues against the tech spec diagram.

### <font color="#79c0ff">Advanced</font>

- [ ] Trace the exact execution path of your feature — entry point, the next 2–4 functions by name, the data shape as it moves, and where validation happens.
- [ ] Explain the technical challenge in your contribution and why your solution is correct, even if AI helped write it.
- [ ] Identify every integration point where your code touches other sections of the codebase.

---

[Assignment](ASSIGNMENT.md)

← [MVP and Merge Discipline](../MVPAndMergeDiscipline/) — Next: [Issues as Work Requests](../IssuesAsWorkRequests/)
