# Activity - Make the Page Remember

*Concept: Save one value to local storage so it survives the refresh that wiped it a moment ago.*

![The same counter, now saved. A plain variable loses its value on refresh and shows 0. A value written to localStorage, drawn as a labeled notebook the browser keeps for this one site, survives the refresh and still shows 5, because setItem wrote it and getItem reads it back when the page loads.](../assets/local-storage.svg)

## Task

1. In `scripts/main.js`, change your click handler so it also calls `localStorage.setItem("count", count)` right after it adds one.
2. At the top of the file, start `count` from storage instead of zero: `let count = Number(localStorage.getItem("count")) || 0;`, and write that value into the page as soon as it loads.
3. Click a few times, then refresh. The number stays. Refresh again, close the tab and reopen it: still there. That is the notebook.
4. Open DevTools, find the **Application** panel (Chrome) or **Storage** panel (Firefox), and open Local Storage for your site. You can see your `count` entry, watch it change as you click, and delete it to start fresh.
