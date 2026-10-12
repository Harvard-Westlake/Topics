<div align="center">

# The Learning Widget Project
*<font color="#8b949e">A learning widget is a small interactive web page that teaches one hard idea better than it was taught to you.</font>*

</div>

---

![The Learning Widget path, four steps always in this order: 1 Topic, approved by your teacher; 2 PLAN.md, in your own words and committed first; 3 Build, on a branch, one piece at a time; 4 Ship, live on Firebase with a pull request open. Underneath, the Git history the project must show: a PLAN.md commit first, then several small widget-code commits, then the pull request. The plan comes before the first line of code, which is the proof the thinking is yours.](assets/widget-phases.svg)

This is where everything in the unit comes together:

- **You pick the idea:** one topic you struggled with, or one you can explain better than anyone taught you.
- **You plan it yourself** before any AI touches it.
- **You build it like a manager,** with the AI doing the typing, and ship it on your own website.

## <font color="#388bfd">Table of Contents</font>

1. [Choosing a topic only you can teach this way](#choosing-a-topic)
2. [Planning the widget before writing code](#plan-before-code)
3. [Building and shipping it](#building-and-shipping)
4. [What a strong widget looks like](#what-a-strong-widget-looks-like)

## <font color="#388bfd">Choosing a Topic</font>

Think back over the last year of school. Which ideas were hard to understand, explained badly, or never shown in a way you could see? Which ones can you explain more simply than whoever taught you?

Give it real time. The widget is only worth building if it adds **your** angle. A proposal often sounds like one of these:

- *"I never really understood ______ until I saw it as ______."*
- *"I get ______. People would learn it faster if they could ______."*

Before proposing, search for tools that already do it. A widget that already exists is not a dead end, but you have to say what yours does differently. Your teacher approves the topic before you plan.

## <font color="#388bfd">Plan Before Code</font>

Your plan is a `PLAN.md` file in your fork of the class project repository. Write it yourself and **commit it before any AI rewrites or formats it**. That first commit is the evidence that the thinking is yours.

A strong plan answers:

| Question | Example answer |
|---|---|
| What does the learner see first? | A one-sentence hook and a "Start" button. |
| What can the learner do? | Drag a slider that reshapes the graph, then answer a three-question check. |
| How do the parts connect? | Each section unlocks after the check before it is passed. |
| What does it remember? | Progress survives a reload; class high scores live in Firestore. |
| Why is this better than how you were taught? | It shows the idea moving instead of describing it. |

## <font color="#388bfd">Building and Shipping</font>

- **Branch first.** All widget code goes on a branch in your fork, never straight onto the default branch.
- **Use the manager's loop** from [Intro to AI Coding](../InterfacingWithAI/): Ask, Plan, then Agent one piece at a time, and test each piece in the browser with the [console open](../DebuggingJavaScript/).
- **Make it remember.** Use what you learned about [persistence](../PersistenceAndIntermediateWeb/) and [Firestore](../DatabasesAndCollections/): a learner's progress should survive a reload.
- **Match the house style.** The look must match the styles at [learnhw.web.app/admin](https://learnhw.web.app/admin) exactly.
- **Ship it.** Deploy to your Firebase site, link to it from a button on your main page, and open a pull request.

## <font color="#388bfd">What a Strong Widget Looks Like</font>

The widget is not done when it deploys. It goes through [feedback](../UXAndBehaviorTracking/), [iteration](../WidgetIteration/), a [peer review](../PeerReview/), and a presentation. Build toward that from day one:

- Every flow works as described, with nothing that blocks the learner.
- What it teaches is correct.
- The console shows zero errors on load and during use.
- It is engaging, works on a phone, and is easy to navigate.
- It looks like it belongs on learnhw.

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Say what your widget teaches and why it beats the way you were taught.
- [ ] Explain why `PLAN.md` must be committed before any AI touches it.
- [ ] Describe the path your code takes: branch, small tested pieces, deploy, pull request.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Write a plan detailed enough that a classmate could build your widget from it without asking you a question.

---

[Assignment](ASSIGNMENT.md)

← [Intro to AI Coding](../InterfacingWithAI/) | Next: [UX and Behavior Tracking](../UXAndBehaviorTracking/)
