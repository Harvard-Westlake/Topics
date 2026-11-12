# Activity - Add Ids and React

*Concept: Give two elements an id, then make the page change when the user does two different things.*

![The three-step event pattern. Step 1, pick an element: a button with id go. Step 2, name an event: click. Step 3, attach a function that runs on each click and writes new text into the paragraph with id output. Below, a strip of six event types a page can listen for: click, keydown, mouseover, input, submit, and a setInterval timer.](../assets/events-grid.svg)

## Task

1. In your site's `public/index.html`, add a heading and a button, and give each an id you choose:
   ```html
   <h1 id="title">My Page</h1>
   <button id="go">Go</button>
   ```
2. In `scripts/main.js` (loaded with `<script defer src="scripts/main.js"></script>` in the head), get the button by its id and add a **click** listener that changes the heading's `textContent`. Save, refresh, click: the heading changes.
3. Add a **second, different** event: either a `keydown` listener on `document` that shows `event.key` in the heading, or a `mouseover` on the button that changes its text. You now have two kinds of event on one page.
4. Move the `<script>` tag up into the head and remove `defer`. Refresh and open the Console: the code now runs before the button exists, so `getElementById` returns `null` and the line crashes. Put `defer` back. That error is loading order, and you will see it again.
