<div align="center">

# DOM Events and Local Storage
*<font color="#8b949e">A page is a tree your code can read and change, and local storage is the small notebook where that code saves what it should remember after a refresh.</font>*

</div>

---

Last class you put a page on the internet. Today the page starts to listen and to remember:

- **The page is a tree, and `document` is that tree as a variable.** Your code reaches into it, finds an element, and changes it while the page is open.
- **Code runs in the order the page loads it.** Put a script in the wrong place and it looks for elements that do not exist yet.
- **A refresh wipes the page's memory.** A normal variable starts over every time. Local storage is the one place a value survives a refresh, a redeploy, and closing the tab.

## <font color="#388bfd">Table of Contents</font>

1. [The page is a tree your code can read and change](#the-page-is-a-tree)
2. [Serve, deploy, and the refresh that forgets](#serve-deploy-and-the-refresh)
3. [Local storage: the page remembers](#local-storage)

## <font color="#388bfd">The Page is a Tree</font>

A web page is one HTML file, and the browser reads it as a **tree**: `html` at the root, `head` and `body` under it, and every tag nested inside another. You already met this tree in the Elements panel. JavaScript gets the same tree as a single variable named `document`, and it can walk the tree, pull out one node, and change it while you watch.

There are two trees in a web project, and they are not the same thing:

- **The file tree** is the folders on disk: `index.html`, `scripts/`, `styles/`. It is what you see in VS Code.
- **The document tree** is the live page in the browser: the tags, nested, after the browser has read the file. It is what `document` holds and what the Elements panel shows.

To change a node you first name it. The cleanest way is to give the tag an **id** in the HTML, then ask for it by that id:

```html
<h1 id="title">My Page</h1>
<button id="go">Go</button>
<p id="output">nothing yet</p>
```

```javascript
const heading = document.getElementById("title");
heading.textContent = "Changed by code";
```

An id is a name you invent. It has to be unique on the page, and it is how your code and one exact element find each other.

**Loading order decides whether any of this works.** The browser runs a `<script>` the moment it reaches it, top to bottom. If the script runs before the element it names exists, `getElementById` hands back `null` and the next line crashes. The safe habit is one attribute:

```html
<script defer src="scripts/main.js"></script>
```

`defer` tells the browser "build the whole tree first, then run this file," so a deferred script in the `head` always sees a finished page. (Older code instead puts the `<script>` as the last thing before `</body>`, which works for the same reason: by then the tree is built.)

Once the script can see the tree, you make the page react. Every reaction is the same three steps: **pick an element, name an event, attach a function.** The browser calls your function every time the event happens.

```javascript
const button = document.getElementById("go");
button.addEventListener("click", function () {
  alert("you clicked");
});
```

You will also see the older shorthand `button.onclick = function () { ... }`. Prefer `addEventListener`, because one element can hold many listeners at once. Events come in a few families, and a single page can mix them all:

| Event | Fires when |
|---|---|
| `click` | an element is clicked |
| `keydown` | a key goes down (`event.key` says which) |
| `mouseover` | the pointer enters an element |
| `input` | the text in a box changes |
| `submit` | a form is sent |
| `setInterval` | a timer you set ticks |

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Add Ids and React</strong></summary>

*Concept: Give two elements an id, then make the page change when the user does two different things.*

![The three-step event pattern. Step 1, pick an element: a button with id go. Step 2, name an event: click. Step 3, attach a function that runs on each click and writes new text into the paragraph with id output. Below, a strip of six event types a page can listen for: click, keydown, mouseover, input, submit, and a setInterval timer.](assets/events-grid.svg)

## Task

1. In your site's `public/index.html`, add a heading and a button, and give each an id you choose:
   ```html
   <h1 id="title">My Page</h1>
   <button id="go">Go</button>
   ```
2. In `scripts/main.js` (loaded with `<script defer src="scripts/main.js"></script>` in the head), get the button by its id and add a **click** listener that changes the heading's `textContent`. Save, refresh, click: the heading changes.
3. Add a **second, different** event: either a `keydown` listener on `document` that shows `event.key` in the heading, or a `mouseover` on the button that changes its text. You now have two kinds of event on one page.
4. Move the `<script>` tag up into the head and remove `defer`. Refresh and open the Console: the code now runs before the button exists, so `getElementById` returns `null` and the line crashes. Put `defer` back. That error is loading order, and you will see it again.

*(Standalone file: [activities/01-add-ids-and-react.md](activities/01-add-ids-and-react.md))*

</details>

## <font color="#388bfd">Serve, Deploy, and the Refresh</font>

You have two ways to see your site, and they answer different questions.

- **`firebase serve`** runs the site on your own computer at an address like `http://localhost:5000`. Nobody else can see it. It is for trying a change in seconds without publishing it. You stop it by pressing **`Ctrl+C`** in the terminal, which returns you to the normal prompt.
- **`firebase deploy --only hosting`** copies your files to Firebase's servers and updates your real, public address. Use it when the change is ready for the world.

```bash
firebase serve                     # preview locally; Ctrl+C to stop
firebase deploy --only hosting     # publish to your live URL
```

Now the surprise. You deploy a change, open your live site, refresh, and see the **old** page. Nothing is broken. The browser keeps a **cache**: a local copy of files it has already downloaded, so pages load fast and do not refetch everything every time. A normal refresh often serves that cached copy. A **hard refresh** forces the browser to ask the server for fresh files:

- Mac: `Cmd+Shift+R`
- Windows: `Ctrl+Shift+R`

> **Tip:** When a deploy "did not work," hard refresh before you touch any code. The deploy almost always worked; the cache was showing you yesterday.

There is a second kind of forgetting, and it is not the cache. Watch a normal variable:

```javascript
let count = 0;
document.getElementById("go").addEventListener("click", function () {
  count += 1;
  document.getElementById("output").textContent = count;
});
```

Click a few times and the number climbs. Now refresh. It is back to `0`. The variable lived in the page's memory, and a refresh throws that memory away and runs the file again from the top. The cache is about which **files** you get; this is about the **values** your code was holding. The next section fixes it.

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Serve, Deploy, and the Refresh That Forgets</strong></summary>

*Concept: Preview locally, publish, get past the cache, and watch a plain variable lose its value on every refresh.*

![Two ways to see your site. firebase serve runs it privately on your own laptop at localhost, stopped with Ctrl+C. firebase deploy copies the files to Firebase and updates your public URL, where a normal refresh may show a cached old copy until a hard refresh. Separately, a counter variable reads 5 before a refresh and resets to 0 after, because a refresh throws the page's memory away.](assets/serve-deploy-cache.svg)

## Task

1. In your terminal, run `firebase serve` and open the `localhost` address it prints. This is your site on your own machine, private to you. Press `Ctrl+C` to stop it and get your prompt back.
2. Add the click counter from the lesson to `scripts/main.js`, then run `firebase deploy --only hosting` and open your live address. Click the button: the number climbs.
3. Change the button's text in the code, deploy again, and do a normal refresh. If you still see the old text, do a **hard refresh** (`Cmd+Shift+R` on Mac, `Ctrl+Shift+R` on Windows). The new text appears: the first refresh showed you the cache.
4. Click the counter up to 5, then refresh the page. It drops to 0. The page's memory is gone. Leave it broken; you fix it next.

*(Standalone file: [activities/02-serve-deploy-and-cache.md](activities/02-serve-deploy-and-cache.md))*

</details>

## <font color="#388bfd">Local Storage</font>

**Local storage** is a tiny notebook the browser keeps for your site. What you write in it stays after a refresh, after a redeploy, and after you close the tab and come back tomorrow. It lives in the visitor's own browser, one separate notebook per site, so it is perfect for a per-person count, a saved setting, or a draft.

It has two moves:

```javascript
localStorage.setItem("count", 7);               // write: save 7 under the name "count"
const saved = localStorage.getItem("count");    // read: get it back later
```

Two things to know. **Everything is stored as text,** so `getItem` hands back a string: turn it into a number before you do math, with `Number(localStorage.getItem("count"))`. And **the first read is empty,** because a visitor who has never been to your site has nothing saved, so `getItem` returns `null`. Treat that `null` as your starting value.

Here is the counter from the last section, now with a memory. Read the saved value when the page loads, use `0` if there is nothing yet, and write the new value back on every click:

```javascript
let count = Number(localStorage.getItem("count")) || 0;   // start from what was saved
const output = document.getElementById("output");
output.textContent = count;

document.getElementById("go").addEventListener("click", function () {
  count += 1;
  output.textContent = count;
  localStorage.setItem("count", count);                   // save the new value
});
```

Now a refresh changes nothing: the page reads the number back and carries on. Close the tab, reopen it tomorrow, and the count is still there.

### <font color="#79c0ff">Activity 3</font>
<details>
<summary><strong>Make the Page Remember</strong></summary>

*Concept: Save one value to local storage so it survives the refresh that wiped it a moment ago.*

![The same counter, now saved. A plain variable loses its value on refresh and shows 0. A value written to localStorage, drawn as a labeled notebook the browser keeps for this one site, survives the refresh and still shows 5, because setItem wrote it and getItem reads it back when the page loads.](assets/local-storage.svg)

## Task

1. In `scripts/main.js`, change your click handler so it also calls `localStorage.setItem("count", count)` right after it adds one.
2. At the top of the file, start `count` from storage instead of zero: `let count = Number(localStorage.getItem("count")) || 0;`, and write that value into the page as soon as it loads.
3. Click a few times, then refresh. The number stays. Refresh again, close the tab and reopen it: still there. That is the notebook.
4. Open DevTools, find the **Application** panel (Chrome) or **Storage** panel (Firefox), and open Local Storage for your site. You can see your `count` entry, watch it change as you click, and delete it to start fresh.

*(Standalone file: [activities/03-make-the-page-remember.md](activities/03-make-the-page-remember.md))*

</details>

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Give an element an id and change it from JavaScript with `getElementById`.
- [ ] Wire up two different events, such as a click and a key press, that each change the page.
- [ ] Save a value with `localStorage.setItem` and read it back so it survives a refresh.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Store two things at once, such as a click count and a name typed into a text box, and show both the moment the page loads.

---

[Assignment](ASSIGNMENT.md)

← [Website Hosting](../WebsiteHosting/) | Next: [JavaScript on the Web](../JavaScriptAndCursor/)
