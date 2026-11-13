# Assignment - User Flow and Logging

**Lesson:** [User Flow and Logging](README.md)  
**Due:** Before the start of next class

---

> **Announcement:** Building with AI can be incredibly fun and fast paced. Today we are going to structure the building with the context and support needed to truly own your own app.

## Part 1: Log Your Own Clicks

Turn your own clicks on a real page into a log, then read the log like the site's owner would.

![A browser console showing four logged clicks, each an object with an event name, the kind of element clicked, and the seconds since the page opened: a button at 3 seconds, an image at 9, then the page heading at 14 and 15. A note points at the two heading clicks: the title looks like a button. Each row answers what happened, on what, and when.](assets/console-click-log.svg)

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

---

## Part 2: Build Your Own Experience, With Tracking Rails

A full working website experience that is interesting, engaging, and enjoyable. Your idea, built with your AI, live on the web. The plan comes first, and the plan is yours. The tracking is part of the plan, not something added at the end.

1. **Start the prompt list.** Make this the first message of today's session:
   ```
   From now on, save every prompt I send you in a file called prompts.md,
   in my exact words, unedited, numbered, with the newest at the bottom.
   Start with this message. Add each new prompt to the file before you do
   anything else with it.
   ```
2. **Plan with your AI before any code.** Talk each of these through in your own words until the AI can say it back correctly:
   - **One specific user:** a real person in a real moment.
   - **Arrival and the first ten seconds:** what they see, what they understand, and the first thing they do.
   - **The core loop:** the one action they repeat, and why the fifth time is as good as the first. A one-time, unique experience is OK, as long as you call it out and say how it ends.
   - **The flow for the core use:** tell the AI your user flow, step by step, for the main thing people come to do.
   - **Common edge cases:** tell it what happens when things go differently: a wrong or empty input, a first visit with nothing to show yet, a refresh or a back button halfway through.
   - **The outcome:** what the user leaves with, and the details that make it land.
   - **The tracking rails:** which moments of the flow get logged, and what you expect the log to tell you.
3. **Get the flowchart.** The AI may draw it, saved in your repository as `FLOW.md`, as long as it is totally aligned with your plan. Check it box by box and have the AI fix anything you did not say.
4. **Then build.** Have the AI build the experience from the plan, with the tracking in it, and put it live.

**The tracking rails are complete when:**

- **Every step of the flow leaves an event:** arriving, the first action, each core action, each choice the user makes, the outcome, and leaving.
- **Every event says what, on what, and when:** a name, a few details, the time, and a random session id that stands for one visit.
- **Events are saved where you can read them later:** after a friend's visit, you can open the log without their device and see what they did.
- **Time on the site can be read from the log:** the last event's time minus the first.
- **Nothing in the log says who the visitor is:** no names, no passwords, nothing typed into a text box. The page tells visitors that it logs their actions.

> **Note:** We read every prompt in `prompts.md`, today and for the rest of the unit, to see that you are on the right path. Keep the file going in every session.

**Verify:** open your live link on a phone or in a private window and walk your own flowchart. Every box and every option on the chart exists in the app, and nothing in the app is missing from the chart. Then open your log: every box you walked through is there as a row, in order, with a time.

---

## Success Criteria

- [ ] **Click log:** you logged one minute of your own clicks on a real site and can say what the owner could learn from them.
- [ ] **Working experience:** the live link opens and the whole flow works from arrival to outcome.
- [ ] **Complete tracking rails:** one visit leaves a saved row for every step of the flow, each with a time and a session id, and nothing that identifies the visitor.
- [ ] **Prompts that solve the problem:** your prompts work out who the user is, their first ten seconds, the loop or one-time experience, the flow, the outcome, and what to log, before the prompt that asks for the build.
- [ ] **Chart matches plan:** `FLOW.md` shows every step and choice you described, and nothing you did not.
- [ ] **Exact prompts:** `prompts.md` holds every prompt you sent, in your exact words, unedited.

---

## Submission

Submit your **`prompts.md`** on Canvas: paste the whole file into the text box, under these three lines:

```
Live link:                          
Part 1, the owner could learn:      
Part 1, the log must never contain: 
```

Before you submit, read your own prompts from top to bottom and answer honestly:

- **Do your prompts actually try to solve these issues?** Who the user is, what they do when they arrive, what keeps them there, where each choice leads, and what they leave with.
- **Or do they merely try to fulfill the requirements, using work you already did?** A prompt like "write a user flow for the app we made" fills in a requirement after the fact. It does not solve anything.

You need to have GOOD answers to these questions, and your prompts need to show the behavior: thinking about the user first, in your own words, and building second. That is what we read for.
