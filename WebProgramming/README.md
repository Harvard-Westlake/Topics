<div align="center">

# Web Programming
*<font color="#8b949e">Web programming is building pages that run in a browser: their structure, their look, their behavior, and the data they remember.</font>*

</div>

---

This unit goes from "what is a web page, actually?" to shipping a real product: a live, database-backed learning widget that other people use, critique, and review.

1. **Put a real website on the internet:** HTML, CSS, and JavaScript, hosted live on Firebase.
2. **Make it interactive:** JavaScript inside the page, packages other people wrote, events, and canvas animation.
3. **Make it remember:** local storage, cookies, and a shared Firestore database.
4. **Code with AI as the manager, not the passenger:** teach the AI your tastes before it builds anything, state the decisions you care about, build one piece at a time, and check everything it hands back.
5. **Ship the Learning Widget:** an educational tool on a topic you can teach better than it was taught to you.
6. **Improve it and present it:** gather feedback, iterate, review a partner's widget, and present what you found.

> **Note:** This unit uses the Git skills from earlier in the course: clone, commit, push, fork, branch, and pull request. If any of those feel rusty, revisit [Git Usage](../GitUsage/) before the Learning Widget begins.

---

## <font color="#388bfd">Reference Documentation</font>

| Doc | Read before | What it covers |
|---|---|---|
| [HTML](Docs/html.md) | Lesson 1 | Page structure, common tags, attributes, semantic elements |
| [CSS](Docs/css.md) | Lesson 1 | Selectors, the box model, colors, fonts, layout basics |
| [JavaScript](Docs/javascript.md) | Lesson 2 | Variables, functions, DOM access, packages, events, canvas and animation, classes |
| [Firebase Hosting](Docs/firebase-hosting.md) | Lesson 1 | CLI commands, project structure, deploy workflow, troubleshooting |
| [Codex Commands](InterfacingWithAI/docs/codex-commands.md) | Lesson 5 | Every Codex slash command in one plain sentence, with the real risk behind the dangerous ones |
| [Website Inspiration](Docs/website-inspiration.md) | Lesson 10 | Examples of innovative UX and interactive design |

---

## <font color="#388bfd">Lessons</font>

| Day | Lesson | What you'll learn |
|---|---|---|
| 1 | [Website Hosting](WebsiteHosting/) | One HTML file as a tree, the three languages, and deploying a live site with Firebase |
| 2 | [DOM Events and Local Storage](DOMEventsAndStorage/) | The page as a tree your code changes, events, serve vs deploy and the cache, and localStorage |
| 3 | [JavaScript on the Web](JavaScriptAndCursor/) | Scripts inside the page, packages from npm, events, and canvas animation |
| 4 | [Persistence and Intermediate Web](PersistenceAndIntermediateWeb/) | Why page state vanishes on refresh and the ways websites remember |
| 5 | [Intro to AI Coding](InterfacingWithAI/) | Codex CLI in your terminal, what an AI agent may touch, and teaching the AI your tastes before it builds anything |
| 6 | [Databases and Collections](DatabasesAndCollections/) | JSON, Firestore collections and documents, reading and writing a document by name, and security rules |
| 7 | [User Flow and Logging](UserFlowAndLogging/) | One specific user, their first ten seconds, the flow as a chart, and how sites log what visitors do |
| 8–9 | [The Learning Widget Project](LearningWidget/) | Plan and build an educational widget published via GitHub and Firebase |
| 10 | [UX and Behavior Tracking](UXAndBehaviorTracking/) | Engagement, navigation, user flow, and heatmaps of real behavior |
| 11 | [Widget Iteration from Feedback](WidgetIteration/) | Turning feedback into a shrinking `feedback.md` and an error-free widget |
| 12 | [Collaborative Peer Review](PeerReview/) | Reviewing a partner's widget and preparing to present what you found |
| 13 | [Widget Presentations](WidgetPresentations/) | In class: a one-minute walkthrough of the widget you reviewed, and your findings |
| Extra | [Debugging JavaScript](DebuggingJavaScript/) | DevTools, the console, and reading stack traces: open it whenever something breaks |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Say what HTML, CSS, and JavaScript each do, and what hosting adds.
- [ ] Name the ways a site can remember data after a refresh, and where each one lives.
- [ ] Explain why "the AI said it works" is never enough proof that code works.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Trace your Learning Widget's whole life, from topic approval to the presentation, and name the Git step behind each stage.
