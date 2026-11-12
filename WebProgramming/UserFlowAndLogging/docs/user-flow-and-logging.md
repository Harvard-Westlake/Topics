<div align="center">

# User Flow and Logging
*<font color="#8b949e">A user flow is the path one visitor takes through your app, and logging is how the app writes down what visitors actually did.</font>*

</div>

---

![Flowchart of one visitor using a guess-the-song app. Arrive: the visitor sees three emoji and a text box. First ten seconds: they know the job is to guess the song without reading instructions. They type a guess, the core action. A diamond asks whether it was correct, and either way they get feedback: the answer is revealed and the streak goes up or resets. A second diamond asks play again: yes loops back to typing a guess, no leads to the outcome, sharing the streak and leaving happy. A dot travels the path and goes around the loop. A caption says to read it out loud as the user, and that a box with no arrow out means the user is stuck there.](../assets/user-flow.svg)

Before anything gets built, picture one person using it.

- **One user:** a specific person, what they see and do in their first ten seconds, and how fast the page has to appear.
- **The flow:** every step and every choice, drawn as a chart, ending in what the user leaves with.
- **Logging:** how a site records clicks, data, and time, and how a heatmap turns that record into a picture, so you can see whether the flow you planned is the flow people take.

## <font color="#388bfd">Table of Contents</font>

1. [Start with one user, their first ten seconds, and how fast the page must load](#start-with-one-user)
2. [The flow, the loop, and the outcome you want for the user](#the-flow-and-the-loop)
3. [Logging and heatmaps: how sites record interactions, data, and time on the site](#logging)

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

### <font color="#79c0ff">Load time</font>

The ten seconds start when the user taps the link, not when the page finishes loading. Every second spent waiting is a second they are not using your app, and many leave before it appears.

- **The target:** the main content is on screen within about **2.5 seconds**.
- **Social apps are the hardest case.** A link tapped inside a feed opens while the user is mid-scroll, with the next video one swipe away. A slow page loses to the feed.
- **Speed decides purchases.** The companies that measured it report the same thing: faster pages get more people all the way to buying.

| What was measured | Result | Who measured it |
|---|---|---|
| Mobile visitors who leave a page that takes more than 3 seconds to load | 53% | [Google](https://www.thinkwithgoogle.com/marketing-strategies/app-and-mobile/mobile-page-speed-new-industry-benchmarks/) |
| Chance a visitor leaves at once when load time goes from 1 second to 3 seconds | 32% higher | [Google](https://www.thinkwithgoogle.com/data/page-load-time-statistics/) |
| Visitors who abandon a link tapped in the Facebook feed after 3 seconds of delay | As many as 40% | [Facebook](https://about.fb.com/news/2017/08/news-feed-fyi-showing-you-stories-that-link-to-faster-loading-webpages/) |
| Purchases on retail sites when the mobile site got 0.1 seconds faster | 8.4% more purchases, and 9.2% more spent per order | [Deloitte, for Google](https://www.deloitte.com/ie/en/services/consulting/research/milliseconds-make-millions.html) |
| Pinterest sign-ups when the wait for the mobile page was cut by 60% | 40% more | [Pinterest](https://medium.com/pinterest-engineering/driving-user-growth-with-performance-improvements-cfc50dafadd7) |

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>One User, Ten Seconds</strong></summary>

*Concept: Name the one person your app is for and say what they see, understand, and do in their first ten seconds.*

![A sketch of a page called Guess the song with three emoji, one text box, a Go button, and a streak counter, above a timer bar that fills in ten seconds. Three callouts point at the page. What is this? The title says it in three words. What do I do first? One box and one button, nothing else. Why would I stay? A streak that starts at zero.](../assets/ten-second-test.svg)

## Task

1. Write one sentence naming a specific person in a real moment. Not "people who like puzzles" but "my cousin Dev, waiting for the bus, phone in one hand".
2. Write what that person **sees** the instant your page opens. Three things at most.
3. Write the **first thing they do**, and what on the screen told them to do it. No instructions allowed.
4. Answer the three questions in the diagram for your own app: What is this? What do I do first? Why would I stay?
5. Read your answers to a neighbor without explaining anything else. If they cannot say what your app is, rewrite step 2.

*(Standalone file: [activities/01-one-user-ten-seconds.md](../activities/01-one-user-ten-seconds.md))*

</details>

## <font color="#388bfd">The Flow and the Loop</font>

A **user flow** is the whole visit, step by step, ending in what the user leaves with. Most apps repeat one **core loop**. A one-time, unique experience is just as good, as long as you call it out.

![Two panels. On the left, a core loop: a dot circles through do the action, see what happened, get a small reward, and want to go again, with the question: is the fifth time as good as the first? On the right, a one-time experience: a dot travels once from arrive, up to the moment, and down to a clear ending, with the question: what is the moment, and how does the user know it is done? A caption says either is a good plan, and that saying this is a one-time experience and that is intended is a complete answer.](../assets/loop-or-one-time.svg)

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Walk the Flow</strong></summary>

*Concept: Say your app's whole flow out loud as the user, then check that a flowchart of it matches your words exactly.*

![Two lists side by side. Your plan, in your words, has four steps: arrive and see three emoji, type a guess, see if it was right, play again or share. The AI's flowchart matches three of them with green check marks, but its third step says sign in to see the answer, marked with a red X: a sign-in step the student never asked for, to be removed before any code.](../assets/flow-check.svg)

## Task

1. Finish this sentence for your app, one step per comma: "I arrive, I see ..., I ..., then I can either ... or ..., and I leave with ...".
2. Say whether your app is a **core loop** or a **one-time experience**. If it is a loop, name the action that repeats. If it is one time, name the moment and the ending.
3. List every choice the user gets. For each choice, write where each option leads. An option that leads nowhere is a dead end.
4. Sketch the flow as boxes, diamonds, and arrows, or have your AI draw it from your sentence.
5. Walk the chart one box at a time against your sentence from step 1. Mark anything the chart has that you never said, and anything you said that the chart lost. Fix the chart, not your plan.

*(Standalone file: [activities/02-walk-the-flow.md](../activities/02-walk-the-flow.md))*

</details>

## <font color="#388bfd">Logging</font>

You planned a flow. **Logging** is how you find out whether real visitors follow it. The site writes down a short row every time something happens.

![Animated diagram of logging. On the left, five things a user does: opens the page, presses Start, gets round 1 right, misses round 2, and closes the tab. Each one slides across and becomes one row in a log on the right, with a time, an event name, and details: 0:00 page_view, 0:04 click on the start button, 0:31 answer correct, 1:12 answer wrong, 2:05 page_hide. A box at the bottom reads the story from the rows: time on the site is 2 minutes 5 seconds, Start was pressed after 4 seconds, and the user left right after a miss in round 2.](../assets/event-log.svg)

Each row is called an **event**, and it is a small piece of [JSON](../../DatabasesAndCollections/):

```json
{ "event": "answer", "correct": true, "round": 1, "session": "a81f", "time": "2026-11-12T10:15:31Z" }
```

| What sites log | Example events | What it tells the owner |
|---|---|---|
| **Interactions** | `click`, `scroll`, `submit`, `play` | What people try, and what they ignore. |
| **Data** | `answer` with `correct: false`, `level` with `number: 3` | How the app itself is going for them. |
| **Time** | `page_view` at the start, `page_hide` at the end | Time on the site: the last event's time minus the first. |

How logging is usually handled:

1. **A listener notices** the click, scroll, or page close, the same [events](../../DOMEventsAndStorage/) you already use.
2. **The page builds an event:** a name, the time, a few details, and a random session id that stands for "one visit", not for a person.
3. **Events are sent in small batches** to a server, so the page stays fast.
4. **The server stores them**, often one document per event in a collection such as `events`.
5. **Someone reads the totals:** how many visitors pressed Start, where they stopped, and how long they stayed.

`console.log` is logging too. It is the version only you can see, on your own machine.

> **Warning:** Log what people do, never who they are. No names, no passwords, nothing typed into a text box, and tell visitors that you collect it.

### <font color="#79c0ff">Heatmaps</font>

A **heatmap** is the log drawn as a picture. The events of many visitors are laid over the page: hot colors where activity piles up, cold where nothing happens.

![A screenshot of the German Wikipedia main page with an eye-tracking heat map laid over it. The article of the day in the upper left glows red and orange, where people looked longest. The news column on the right and the lower boxes are yellow and green. The sidebar of links on the far left, the search box, and the footer stay blue or untouched, because almost nobody looked there.](../assets/eyetracking-heatmap-wikipedia.jpg)

<sub>Example: where people looked on the Wikipedia main page. Image by Tschneidr, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0), from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Eyetracking_heat_map_Wikipedia.jpg). More pictures: the [F-shaped reading heatmaps](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/) and [scroll attention charts](https://www.nngroup.com/articles/scrolling-and-attention/) from Nielsen Norman Group.</sub>

There are three types: the **click map**, the **scroll map**, and the **move map**.

### <font color="#79c0ff">Activity 3</font>
<details>
<summary><strong>Log Your Own Clicks</strong></summary>

*Concept: Turn your own clicks on a real page into a log, then read the log like the site's owner would.*

![A browser console showing four logged clicks, each an object with an event name, the kind of element clicked, and the seconds since the page opened: a button at 3 seconds, an image at 9, then the page heading at 14 and 15. A note points at the two heading clicks: the title looks like a button. Each row answers what happened, on what, and when.](../assets/console-click-log.svg)

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

*(Standalone file: [activities/03-log-your-own-clicks.md](../activities/03-log-your-own-clicks.md))*

</details>

---

← Back to [lesson](../README.md)
