# Activity - Wire Up the Page

*Concept: Attach a function to a click, a key press, and a timer, and watch the page react to each one.*

![How a page reacts, in four steps. 1: something happens, such as a click, a key press, mouse movement, or a timer firing. 2: it happens on an element, here a button with id clicker that is listening for click. 3: the function attached to it runs, adding one to clickCount and writing the new count into the page. 4: the page changes and now shows 3 clicks. The pattern is pick an element, name an event, attach a function, written as button.addEventListener("click", () => { ... }).](../assets/event-flow.svg)

## Task

1. Add the button and paragraph from the lesson to `public/index.html`, and the click counter to `scripts/main.js`. Refresh and click: the number climbs.
2. Inside the click function, add `if (clickCount % 5 === 0) confetti();`. Every fifth click now fires the package from Activity 1. Your code and borrowed code call each other the same way.
3. Add a `keydown` listener on `document` that writes `event.key` into the paragraph. Press letters, arrows, Shift, and the space bar: every key has a name, and `"ArrowLeft"` is how a game knows you pressed left.
4. Add a `setInterval` that adds one to a `seconds` variable every 1000 ms and shows it on the page. Then refresh. It restarts at 0, because a refresh throws the page's memory away. A later lesson fixes that.
