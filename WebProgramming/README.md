<div align="center">

# Web Programming
*<font color="#8b949e">From a blank HTML file to a live, database-backed learning widget — built by directing AI, not leaning on it</font>*

<font color="#a371f7">Learning</font>

</div>

---

This unit is a journey from "what is a web page, actually?" to shipping a real product: a live, database-backed educational widget that other people use, critique, and formally review.

Along the way you will pick up a second skill that matters just as much as the web technology itself: **working with AI as a manager, not a passenger**. Modern AI tools can research, plan, and write code — but they make confident mistakes, fill silent gaps with assumptions, and will happily insist broken code works. Your job in this unit is to learn to direct them: give precise instructions, verify every claim, and debug what comes back. The students who thrive here are not the ones who type the least — they are the ones who *check the most*.

The arc of the unit:

1. **Learn to interrogate AI** — discover how assumptions creep into prompts and how to research a brand-new topic with an AI tutor.
2. **Put a real website on the internet** — HTML, CSS, and JavaScript, hosted live on Firebase with a URL you can text to your family.
3. **Make it interactive** — events, timers, classes, and the Cursor workflow of Ask, Plan, and Agent.
4. **Make it remember** — local storage, cookies, and a shared Firestore database.
5. **Ship the Learning Widget** — a polished educational tool on a topic *you* can teach better than it was taught to you, styled to match a real production site, delivered through a fork-branch-pull-request workflow.
6. **Survive review** — gather human feedback, iterate until your console is silent, and pass a formal peer review where your reviewer's grade depends on catching your bugs.

> **Note:**
> This unit uses the Git skills you built earlier in the course — clone, commit, push, fork, branch, and pull request. If any of those feel rusty, revisit [Git Usage](../GitUsage/) before the Learning Widget project begins.

---

## <font color="#388bfd">Reference Documentation</font>

These are standalone reference pages — consult them throughout the unit whenever you need a reminder.

| Doc | Read before | What it covers |
|---|---|---|
| [HTML](Docs/html.md) | Lesson 1 | Page structure, common tags, attributes, semantic elements |
| [CSS](Docs/css.md) | Lesson 2 | Selectors, the box model, colors, fonts, layout basics |
| [JavaScript](Docs/javascript.md) | Lesson 3 | Variables, functions, DOM access, events, classes, console tools |
| [Firebase Hosting](Docs/firebase-hosting.md) | Lesson 2 | CLI commands, project structure, deploy workflow, troubleshooting |
| [Website Inspiration](Docs/website-inspiration.md) | Lesson 9 | Curated examples of innovative UX and interactive design |

---

## <font color="#388bfd">Lessons</font>

| Day | Lesson | What you'll learn |
|---|---|---|
| 1 | [Interfacing with AI](InterfacingWithAI/) | Assumptions in prompting, researching new topics with AI, creating and viewing HTML pages in Cursor |
| 2 | [Website Hosting](WebsiteHosting/) | HTML/CSS/JS roles, creating a Firebase project, deploying a live static website |
| 3 | [JavaScript and Coding with Cursor](JavaScriptAndCursor/) | Web event binding, JavaScript classes, and directing Cursor's Ask, Plan, and Agent modes |
| 4 | [Debugging JavaScript](DebuggingJavaScript/) | DevTools, the console, `console.error()`, `console.dir()`, and reading stack traces |
| 5–6 | [The Learning Widget Project](LearningWidget/) | Research, plan, and build an educational widget published via GitHub and Firebase |
| 7 | [Persistence and Intermediate Web](PersistenceAndIntermediateWeb/) | Why page state vanishes on refresh and the ways websites remember |
| 8 | [Databases and Collections](DatabasesAndCollections/) | Local storage vs cookies, Firestore documents and collections, CRUD, and security rules |
| 9 | [UX and Behavior Tracking](UXAndBehaviorTracking/) | Engagement speed, navigation, user flow, and heatmaps of user behavior |
| 10 | [Widget Iteration from Feedback](WidgetIteration/) | Turning human feedback into a shrinking `feedback.md` and an error-free widget |
| 11 | [Collaborative Peer Review](PeerReview/) | Reviewing a partner's pull request with your name — and grade — attached to the result |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Describe the roles of HTML, CSS, and JavaScript in one sentence each.
- [ ] Explain what it means for a website to be "hosted" and name the service this unit uses for it.
- [ ] State the three phases every Learning Widget must go through before it is coded.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain why a prompt with unstated assumptions produces different results for different people.
- [ ] Name the three ways this unit stores data that survives a page refresh, and where each one lives.
- [ ] Describe the fork-branch-pull-request path a Learning Widget takes from idea to review.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why a peer reviewer's grade depends on the quality of the code they approve.
- [ ] Argue why "the AI said it works" is never sufficient evidence that code works.
- [ ] Trace the full lifecycle of this unit's final product, from topic approval to an approved pull request.
