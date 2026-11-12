# Activity - Log Your Own Clicks

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
