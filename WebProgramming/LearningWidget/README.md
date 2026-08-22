<div align="center">

# The Learning Widget Project
*<font color="#8b949e">Research, plan, and build an educational widget for a topic you can teach better</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Background](#background)**  
Finding the topic only you can teach this way.

**[Overview](#overview)**  
What you are building and the rules it must follow.

**[Phase 1: Research](#phase-1-research)**  
Confirm your idea doesn't already exist, then get approval.

**[Phase 2: Plan](#phase-2-plan)**  
Design the experience and commit a `PLAN.md` — before AI touches it.

**[Phase 3: Code](#phase-3-code)**  
Build with Cursor on a branch, publish via GitHub and Firebase.

**[What Your Widget Will Be Judged On](#what-your-widget-will-be-judged-on)**  
The quality bar the later review lessons will hold you to.

---

## <font color="#388bfd">Background</font>

During your recent school career — the last year or so — recall a few topics or lessons that were difficult to understand, not communicated clearly, or that you wish had been taught or visualized a different way. Or a few that you can explain more simply than anyone who taught you.

Take some time and think about this now.

Done already? Doubtful. Give it a good few minutes and dig a little deeper. For this project to be useful, you need to ***add*** your unique perspective and insight to it.

If you need help shaping the idea, your proposal may follow one of these outlines:

- *"I never could really understand ________, but then I learned it this new way which made it more understandable..."*
- *"I have a good grasp of ________. I think I can help people learn it more easily by displaying the information like ________."*

---

## <font color="#388bfd">Overview</font>

You are going to research, design, plan out, and — with AI's help — build an **educational widget** for a topic which is not easily understood or visualized. It can be ANY topic, but it must be approved by your teacher.

Two hard rules:

1. **Style parity.** The look must perfectly match the styles defined at [learnhw.web.app/admin](https://learnhw.web.app/admin) — find and use the exact same styles.
2. **Three phases, in order.** Research and approval, then a committed plan, then code. No skipping ahead: the plan must exist in Git history *before* the code does.

> **Note:**
> Your website can hold multiple things at once — add a button on your main website that links to your educational widget.

---

## <font color="#388bfd">Phase 1: Research</font>

1. After you have some ideas, go see if they already exist online
2. Ask an AI chat to look around the web and find similar tools
3. Once you are satisfied the idea is not already done well online, **propose it to your teacher** and get explicit approval

An idea that already exists as a polished widget is not a dead end — but you must articulate what yours will do differently, and your teacher decides whether the difference is enough.

---

## <font color="#388bfd">Phase 2: Plan</font>

1. Design and lay out how you want the site to look and behave
2. **Fork** the Harvard-Westlake project repository for this assignment (your teacher will share the link in class) — forking and pull requests were covered in [Git Usage](../../GitUsage/)
3. Write your design as a `PLAN.md` file in your fork, and **commit the plan BEFORE using AI to rewrite or format it** — the raw, human version must appear in your Git history first

Think hard about how you want the user to *learn* the material and *interact* with the site, and in what general order. A strong `PLAN.md` answers:

| Question | Example answer |
|---|---|
| What does the user see first? | A one-sentence hook and a "start" button |
| What are the interactive parts? | A slider that morphs the graph; a three-question check |
| How do the parts connect? | Each section unlocks after the previous check is passed |
| Why does this beat the way you were taught? | It shows the idea moving instead of describing it |

> **Warning:**
> Committing the plan before AI touches it is not busywork — it is the evidence that the thinking is yours. A `PLAN.md` whose first committed version reads like AI wrote it defeats the point of the phase.

---

## <font color="#388bfd">Phase 3: Code</font>

1. Create a **branch** in your fork and do all coding there
2. Use Cursor — Ask, Plan, and Agent modes — to code the site, testing continuously with the [console open](../DebuggingJavaScript/)
3. Publish it to GitHub and to your live website via Firebase
4. Open a **pull request** containing your final submission

Work like a manager: delegate typing to the Agent in small, testable pieces; verify each piece in the browser before requesting the next.

---

## <font color="#388bfd">What Your Widget Will Be Judged On</font>

This widget is not finished when it deploys — it will go through [feedback iteration](../WidgetIteration/) and a formal [peer review](../PeerReview/) with a published rubric. Build from day one toward that bar:

- Core flows work as stated, with no blocking issues
- Behavior is factually correct for the topic being taught
- Zero console errors on load and during use
- Engaging, responsive UX with clear navigation
- Visual match with the [learnhw.web.app/admin](https://learnhw.web.app/admin) styles

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] State the three phases of the project and what each one produces.
- [ ] Explain why the topic must be approved before any planning starts.
- [ ] Name the two hard rules every widget must follow.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain why `PLAN.md` must be committed before AI rewrites it.
- [ ] Describe the fork-branch-pull-request path your code takes from idea to submission.
- [ ] Check whether your idea already exists online and articulate what yours does differently.

### <font color="#79c0ff">Advanced</font>

- [ ] Write a plan detailed enough that a classmate could build the widget from it.
- [ ] Match an existing site's styles exactly by inspecting its pages.
- [ ] Break the build into Agent-sized pieces and verify each one before moving on.

---

[Assignment](ASSIGNMENT.md)

← [Debugging JavaScript](../DebuggingJavaScript/) — Next: [Persistence and Intermediate Web](../PersistenceAndIntermediateWeb/)
