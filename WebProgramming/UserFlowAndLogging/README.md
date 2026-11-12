<div align="center">

# User Flow and Logging
*<font color="#8b949e">A user flow is the path one visitor takes through your app, and logging is how the app writes down what visitors actually did.</font>*

</div>

---

![Flowchart of one visitor using a guess-the-song app. Arrive: the visitor sees three emoji and a text box. First ten seconds: they know the job is to guess the song without reading instructions. They type a guess, the core action. A diamond asks whether it was correct, and either way they get feedback: the answer is revealed and the streak goes up or resets. A second diamond asks play again: yes loops back to typing a guess, no leads to the outcome, sharing the streak and leaving happy. A dot travels the path and goes around the loop. A caption says to read it out loud as the user, and that a box with no arrow out means the user is stuck there.](assets/user-flow.svg)

Before anything gets built, picture one person using it.

- **One user:** a specific person, and what they see and do in their first ten seconds.
- **The flow:** every step and every choice, drawn as a chart, ending in what the user leaves with.
- **Logging:** how a site records clicks, data, and time, so you can see whether the flow you planned is the flow people take.

## <font color="#388bfd">Table of Contents</font>

1. [Start with one user and their first ten seconds](#start-with-one-user)
2. [The flow, the loop, and the outcome you want for the user](#the-flow-and-the-loop)
3. [Logging: how sites record interactions, data, and time on the site](#logging)

## <font color="#388bfd">Start With One User</font>

An app for "everyone" is designed for no one. Pick one real person in one real moment, and every decision gets easier.

| Vague | Specific |
|---|---|
| People who like music | My friend Maya, bored on the bus, phone in one hand |
| Students | A ninth grader with five minutes before class starts |

Then describe what that person does, not what the app has. "The app has a quiz" is a feature. "Maya sees three emoji and types a song name" is a user doing something.

The **first ten seconds** decide whether they stay. In that time, the screen alone must answer three questions:

- **What is this?**
- **What do I do first?**
- **Why would I stay?**

If the page needs instructions to answer them, the design is not done yet.

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>One User, Ten Seconds</strong></summary>

*Concept: Name the one person your app is for and say what they see, understand, and do in their first ten seconds.*

![A sketch of a page called Guess the song with three emoji, one text box, a Go button, and a streak counter, above a timer bar that fills in ten seconds. Three callouts point at the page. What is this? The title says it in three words. What do I do first? One box and one button, nothing else. Why would I stay? A streak that starts at zero.](assets/ten-second-test.svg)

## Task

1. Write one sentence naming a specific person in a real moment. Not "people who like puzzles" but "my cousin Dev, waiting for the bus, phone in one hand".
2. Write what that person **sees** the instant your page opens. Three things at most.
3. Write the **first thing they do**, and what on the screen told them to do it. No instructions allowed.
4. Answer the three questions in the diagram for your own app: What is this? What do I do first? Why would I stay?
5. Read your answers to a neighbor without explaining anything else. If they cannot say what your app is, rewrite step 2.

*(Standalone file: [activities/01-one-user-ten-seconds.md](activities/01-one-user-ten-seconds.md))*

</details>

## <font color="#388bfd">The Flow and the Loop</font>

A **user flow** is the whole visit, step by step. Draw it as a chart like the one at the top of this page:

| Shape | Means |
|---|---|
| **Box** | Something the user sees or does. |
| **Diamond** | A choice. Every option needs its own arrow. |
| **Arrow** | What happens next. A box with no arrow out is a dead end. |
| **Last box** | The outcome: what the user leaves with. |

The **outcome** is the reason the app exists, written from the user's side: a laugh, a score to beat, a thing they made, a fact they will remember. Name it, then add the details that make it land: what they see at the end, and what they can do with it.

Most engaging apps have a **core loop**: one action the user repeats and wants to repeat. Not every app needs one.

![Two panels. On the left, a core loop: a dot circles through do the action, see what happened, get a small reward, and want to go again, with the question: is the fifth time as good as the first? On the right, a one-time experience: a dot travels once from arrive, up to the moment, and down to a clear ending, with the question: what is the moment, and how does the user know it is done? A caption says either is a good plan, and that saying this is a one-time experience and that is intended is a complete answer.](assets/loop-or-one-time.svg)

> **Note:** A one-time, unique experience is a completely good plan. Call it out: say that it happens once, what the moment is, and how the user knows it is over.

An AI can draw the chart for you in seconds. That is fine, as long as the chart says exactly what you planned. You are the source of truth, so check it box by box.

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Walk the Flow</strong></summary>

*Concept: Say your app's whole flow out loud as the user, then check that a flowchart of it matches your words exactly.*

![Two lists side by side. Your plan, in your words, has four steps: arrive and see three emoji, type a guess, see if it was right, play again or share. The AI's flowchart matches three of them with green check marks, but its third step says sign in to see the answer, marked with a red X: a sign-in step the student never asked for, to be removed before any code.](assets/flow-check.svg)

## Task

1. Finish this sentence for your app, one step per comma: "I arrive, I see ..., I ..., then I can either ... or ..., and I leave with ...".
2. Say whether your app is a **core loop** or a **one-time experience**. If it is a loop, name the action that repeats. If it is one time, name the moment and the ending.
3. List every choice the user gets. For each choice, write where each option leads. An option that leads nowhere is a dead end.
4. Sketch the flow as boxes, diamonds, and arrows, or have your AI draw it from your sentence.
5. Walk the chart one box at a time against your sentence from step 1. Mark anything the chart has that you never said, and anything you said that the chart lost. Fix the chart, not your plan.

*(Standalone file: [activities/02-walk-the-flow.md](activities/02-walk-the-flow.md))*

</details>

## <font color="#388bfd">Logging</font>

You planned a flow. **Logging** is how you find out whether real visitors follow it. The site writes down a short row every time something happens.

![Animated diagram of logging. On the left, five things a user does: opens the page, presses Start, gets round 1 right, misses round 2, and closes the tab. Each one slides across and becomes one row in a log on the right, with a time, an event name, and details: 0:00 page_view, 0:04 click on the start button, 0:31 answer correct, 1:12 answer wrong, 2:05 page_hide. A box at the bottom reads the story from the rows: time on the site is 2 minutes 5 seconds, Start was pressed after 4 seconds, and the user left right after a miss in round 2.](assets/event-log.svg)

Each row is called an **event**, and it is a small piece of [JSON](../DatabasesAndCollections/):

```json
{ "event": "answer", "correct": true, "round": 1, "session": "a81f", "time": "2026-11-12T10:15:31Z" }
```

| What sites log | Example events | What it tells the owner |
|---|---|---|
| **Interactions** | `click`, `scroll`, `submit`, `play` | What people try, and what they ignore. |
| **Data** | `answer` with `correct: false`, `level` with `number: 3` | How the app itself is going for them. |
| **Time** | `page_view` at the start, `page_hide` at the end | Time on the site: the last event's time minus the first. |

How logging is usually handled:

1. **A listener notices** the click, scroll, or page close, the same [events](../DOMEventsAndStorage/) you already use.
2. **The page builds an event:** a name, the time, a few details, and a random session id that stands for "one visit", not for a person.
3. **Events are sent in small batches** to a server, so the page stays fast.
4. **The server stores them**, often one document per event in a collection such as `events`.
5. **Someone reads the totals:** how many visitors pressed Start, where they stopped, and how long they stayed.

`console.log` is logging too. It is the version only you can see, on your own machine.

> **Warning:** Log what people do, never who they are. No names, no passwords, nothing typed into a text box, and tell visitors that you collect it.

### <font color="#79c0ff">Activity 3</font>
<details>
<summary><strong>Log Your Own Clicks</strong></summary>

*Concept: Turn your own clicks on a real page into a log, then read the log like the site's owner would.*

![A browser console showing four logged clicks, each an object with an event name, the kind of element clicked, and the seconds since the page opened: a button at 3 seconds, an image at 9, then the page heading at 14 and 15. A note points at the two heading clicks: the title looks like a button. Each row answers what happened, on what, and when.](assets/console-click-log.svg)

## Task

1. Open any website you like in your browser, then open DevTools and select the **Console** tab.
2. Paste this into the console and press Enter:
   ```javascript
   const openedAt = Date.now();
   document.addEventListener("click", (clickEvent) => {
     console.log({
       event: "click",
       target: clickEvent.target.tagName,
       secondsIn: Math.round((Date.now() - openedAt) / 1000),
     });
   });
   ```
3. Use the page normally for one minute. Click on things, including things you are not sure are clickable.
4. Read your log from top to bottom. What did you click first, and how many seconds in? Did you click anything that did nothing?
5. Name one thing the site's owner could learn from your log, and one thing about you that this log must never contain.

*(Standalone file: [activities/03-log-your-own-clicks.md](activities/03-log-your-own-clicks.md))*

</details>

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Name one specific user for your app and say what they see, understand, and do in their first ten seconds.
- [ ] Draw your app's flow with every choice and its options, say whether it is a core loop or a one-time experience, and name the outcome the user leaves with.
- [ ] Explain what an event is, how time on a site is measured from a log, and what a log must never contain.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Have your app log one event with a time each time the user does its main action, and read the log after a friend tries it.

---

[Assignment](ASSIGNMENT.md)

← [Databases and Collections](../DatabasesAndCollections/) | Next: [The Learning Widget Project](../LearningWidget/)
