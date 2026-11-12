<div align="center">

# Widget Iteration from Feedback
*<font color="#8b949e">Iterating means turning what testers told you into fixes, one at a time, until nothing on their list and nothing in the console is left.</font>*

</div>

---

![feedback.md over your commits. At commit 1 the file holds 10 items, at commit 4 six, at commit 7 two, and at commit 9 the file is deleted and the console shows 0 errors. Every item you fix is deleted, so the Git history proves the feedback was handled. Keep each item in the tester's exact words until it is fixed, then push: the pull request updates on its own.](../assets/feedback-loop.svg)

You built the widget, so you are the one person who cannot see it fresh. Iteration fixes that:

- **Testers:** show you where a first-time visitor gets stuck.
- **feedback.md:** holds every comment in their exact words, and shrinks as you fix them.
- **A silent console:** proves nothing is quietly broken.

## <font color="#388bfd">Table of Contents</font>

1. [Why you need other people to test your work](#getting-human-feedback)
2. [The feedback.md file that shrinks to nothing](#the-feedbackmd-workflow)
3. [A silent console and an updated pull request](#a-silent-console)

## <font color="#388bfd">Getting Human Feedback</font>

Because you built it, you already know which parts are buttons, what order to read things in, and what every label means. Your brain fills in every confusing spot without noticing. This is the **curse of knowledge**: the better you know your own design, the worse you are at seeing its problems.

Fresh testers are walking [heatmaps](../../UXAndBehaviorTracking/). Watch where they hesitate, what they click that is not clickable, and where they ask "what now?" Write down their **exact words**, not your summary of them.

| You see | A fresh tester sees |
|---|---|
| The obvious start button | Three equally sized boxes, none saying "start" |
| A clever minimal icon | A mystery symbol they are afraid to click |
| The intended order | A page they read bottom to top on a phone |

> **Note:** "I didn't know what to do" is not an insult. It is a bug report against your design.

## <font color="#388bfd">The feedback.md Workflow</font>

Feedback that lives in your memory disappears. Feedback that lives in your repository gets fixed:

1. Add `feedback.md` to your repository with every tester's comment, word for word, and commit it.
2. Each time you fix an item, delete it from the file and commit.
3. When the file is empty, delete it.

Anyone reading your history can watch the feedback arrive, shrink, and disappear.

> **Tip:** Keep each item's original words until the moment it is fixed. Rewriting "I couldn't find the quiz" as "improve discoverability" turns a specific, checkable complaint into something vague.

## <font color="#388bfd">A Silent Console</font>

Open your widget with [DevTools](../../DebuggingJavaScript/) and its Console showing:

- **0 errors when the page loads.**
- **0 errors while it is used:** click every button, try every interaction, finish every path.

The one exception is an error that comes from the browser or an extension rather than your code. Check with your teacher before counting one.

Then push. Your Learning Widget's [pull request](../../LearningWidget/) updates on its own with every push. Add a comment to it summarizing what changed because of feedback, and deploy again so the live site matches.

---

← Back to [lesson](../README.md)
