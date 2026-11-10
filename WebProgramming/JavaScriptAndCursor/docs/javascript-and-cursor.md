<div align="center">

# JavaScript on the Web
*<font color="#8b949e">JavaScript is the code that runs inside a page: it waits for something to happen, then changes the tree or draws on the screen.</font>*

</div>

---

Last class you saw that a page is one HTML file, a tree, and that the tree points at a `.js` file. Today that file does something:

- **It runs inside the page.** The browser downloads the file the tree names, runs it top to bottom, then waits.
- **It waits for events.** A click, a key, a tick of a clock. You attach a function to an event, and the browser calls it every time the event happens.
- **It can draw.** A `<canvas>` tag is a blank rectangle you paint with code. Paint it again and again, a little different each time, and you have animation.

## <font color="#388bfd">Table of Contents</font>

1. [How code gets into a page: scripts, the console, and packages other people wrote](#code-in-the-page)
2. [Events: the page reacts to clicks, keys, and timers](#events-the-page-reacts)
3. [Canvas and animation: drawing frames with code](#canvas-and-animation)

## <font color="#388bfd">Code in the Page</font>

The browser fetched `scripts/main.js` on Day 1 because a tag in `head` named it:

```html
<script defer src="scripts/main.js"></script>
```

`defer` means "build the tree first, then run this." Without it the script runs before `<body>` exists, and every element it looks for comes back `null`. Once it runs, the code can reach into the tree and change it:

```javascript
const heading = document.getElementById("title");
heading.textContent = "Changed by JavaScript";
console.log("heading is now:", heading.textContent);
```

- **`document` is the tree.** `getElementById` walks it and hands back one node. `.textContent` is that node's text, and assigning to it changes the page instantly. The Elements panel shows the new tree, the file on disk is unchanged, and a refresh starts over.
- **The console is where the code talks to you.** `console.log` prints a value in the Console panel of DevTools (`Cmd+Option+J` on Mac, `Ctrl+Shift+J` on Windows). You can also type JavaScript straight into it and run it on the open page. Every error lands there too.
- **Most code on a page was written by someone else.** A **package** is a folder of code someone published for everyone to use, and a **package manager** is the app store that fetches it. You have used one already: Homebrew on Mac, or `apt` in WSL, installed `git` and `gh`. JavaScript's is **npm**, a registry of over two million packages. In a project with a build step, `npm install canvas-confetti` downloads the package into `node_modules/` and writes its name and version into `package.json`, the project's shopping list, so a teammate can run `npm install` and get exactly the same code.

Your site has no build step, so you load a package the way the browser already loads your own files: one more `<script>` tag with an address. A **CDN** (content delivery network) such as jsDelivr serves every npm package straight to browsers:

```html
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
```

Pin the version (`@1.9.3`) so your site does not change when the package does. After that tag loads, the package's function `confetti()` exists on your page, exactly like a function you wrote.

![Animated diagram of where a package comes from. On the left, the npm registry holds canvas-confetti 1.9.3 among two million packages. A CDN, jsDelivr, copies it to servers near every visitor. In the middle, your index.html tree gains one script tag whose src is the CDN address. On the right, the browser loads that file along with your own, and the function confetti() exists on your page: typing confetti() in the console fires confetti. A box glides from the registry through the CDN into the tree, and then confetti bursts on the page.](../assets/package-flow.svg)

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Borrow a Package</strong></summary>

*Concept: Add code you did not write to your page with one script tag, then call it from the console.*

![Animated diagram of where a package comes from. On the left, the npm registry holds canvas-confetti 1.9.3 among two million packages. A CDN, jsDelivr, copies it to servers near every visitor. In the middle, your index.html tree gains one script tag whose src is the CDN address. On the right, the browser loads that file along with your own, and the function confetti() exists on your page: typing confetti() in the console fires confetti. A box glides from the registry through the CDN into the tree, and then confetti bursts on the page.](../assets/package-flow.svg)

## Task

1. In VS Code, open your site's `public/index.html` and add this tag inside `<head>`, above your own `<script>` tag, because your code can only call `confetti()` after the package has loaded:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
   ```
2. Save and open the page in your browser. Open the Console (`Cmd+Option+J` on Mac, `Ctrl+Shift+J` on Windows), type `confetti()` and press Return. Confetti falls. That function came from the package, not from you.
3. Type `confetti({ particleCount: 300, spread: 120 })`. Packages take options, and the package's page on [npmjs.com](https://www.npmjs.com/package/canvas-confetti) lists every one. Find one more option there and try it.
4. Open the Network panel and refresh. Find the row for `confetti.browser.min.js`: its address is the CDN, not your site. Click it and open **Response**. That is the code you borrowed, squeezed onto a few lines so it downloads fast. People read the source on npm or GitHub, never here.

*(Standalone file: [activities/01-borrow-a-package.md](../activities/01-borrow-a-package.md))*

</details>

## <font color="#388bfd">Events: the Page Reacts</font>

Every reaction follows the same three steps: pick an element, name an event, attach a function. The browser calls the function every time the event fires.

```html
<button id="clicker">Click me</button>
<p id="output">0 clicks</p>
```

```javascript
let clickCount = 0;
const button = document.getElementById("clicker");
const output = document.getElementById("output");

button.addEventListener("click", () => {
  clickCount += 1;
  output.textContent = clickCount + " clicks";
});
```

![How a page reacts, in four steps. 1: something happens, such as a click, a key press, mouse movement, or a timer firing. 2: it happens on an element, here a button with id clicker that is listening for click. 3: the function attached to it runs, adding one to clickCount and writing the new count into the page. 4: the page changes and now shows 3 clicks. The pattern is pick an element, name an event, attach a function, written as button.addEventListener("click", () => { ... }).](../assets/event-flow.svg)

Every like button, game, and autocomplete you have used is some mix of four families:

| Family | Examples | Typical use |
|---|---|---|
| **Element** | `click`, `input`, `submit` | Buttons, forms, text boxes |
| **Keyboard** | `keydown`, `keyup` | Game controls, shortcuts |
| **Mouse** | `mousemove`, `mousedown`, `mouseover` | Drawing, hover effects, dragging |
| **Timers** | `setTimeout`, `setInterval` | Countdowns, auto-updates, slow animation |

Keyboard events listen on the whole page, and `event.key` says which key:

```javascript
document.addEventListener("keydown", (event) => {
  console.log("You pressed: " + event.key);
});
```

Timers are events you schedule yourself:

```javascript
setTimeout(() => console.log("Two seconds passed"), 2000);   // once, after 2000 ms

const tick = setInterval(() => console.log("Tick"), 1000);   // every second...
clearInterval(tick);                                          // ...until you stop it
```

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Wire Up the Page</strong></summary>

*Concept: Attach a function to a click, a key press, and a timer, and watch the page react to each one.*

![How a page reacts, in four steps. 1: something happens, such as a click, a key press, mouse movement, or a timer firing. 2: it happens on an element, here a button with id clicker that is listening for click. 3: the function attached to it runs, adding one to clickCount and writing the new count into the page. 4: the page changes and now shows 3 clicks. The pattern is pick an element, name an event, attach a function, written as button.addEventListener("click", () => { ... }).](../assets/event-flow.svg)

## Task

1. Add the button and paragraph from the lesson to `public/index.html`, and the click counter to `scripts/main.js`. Refresh and click: the number climbs.
2. Inside the click function, add `if (clickCount % 5 === 0) confetti();`. Every fifth click now fires the package from Activity 1. Your code and borrowed code call each other the same way.
3. Add a `keydown` listener on `document` that writes `event.key` into the paragraph. Press letters, arrows, Shift, and the space bar: every key has a name, and `"ArrowLeft"` is how a game knows you pressed left.
4. Add a `setInterval` that adds one to a `seconds` variable every 1000 ms and shows it on the page. Then refresh. It restarts at 0, because a refresh throws the page's memory away. A later lesson fixes that.

*(Standalone file: [activities/02-wire-up-the-page.md](../activities/02-wire-up-the-page.md))*

</details>

## <font color="#388bfd">Canvas and Animation</font>

A `<canvas>` is one node in the tree that is a blank rectangle. HTML and CSS cannot draw inside it. Only JavaScript can, through a **context**, the pen you draw with:

```html
<canvas id="stage" width="400" height="300"></canvas>
```

```javascript
const stage = document.getElementById("stage");
const pen = stage.getContext("2d");

pen.fillStyle = "#388bfd";
pen.fillRect(20, 20, 100, 60);           // a rectangle: x, y, width, height
pen.beginPath();
pen.arc(200, 150, 30, 0, Math.PI * 2);   // a circle: center x, center y, radius
pen.fill();
```

The top-left corner is `(0, 0)`. `x` grows to the right and `y` grows **downward**, the opposite of a math graph.

Animation is a flip book. Each frame you wipe the canvas, draw everything slightly moved, and ask the browser for the next frame. `requestAnimationFrame(draw)` calls `draw` once, right before the screen next repaints, about 60 times a second:

```javascript
let x = 50;
let speed = 3;

function draw() {
  pen.clearRect(0, 0, stage.width, stage.height);      // 1. wipe the frame
  pen.beginPath();
  pen.arc(x, 150, 20, 0, Math.PI * 2);                 // 2. draw the ball
  pen.fill();
  x += speed;                                          // 3. move it for next time
  if (x < 20 || x > stage.width - 20) speed = -speed;  //    bounce at the edges
  requestAnimationFrame(draw);                         // 4. ask for the next frame
}

draw();
```

![Animated diagram of the animation loop. On the left, four steps in a cycle that light up in turn: 1 clear the canvas, 2 draw everything, 3 move everything a little, 4 ask for the next frame with requestAnimationFrame. On the right, a canvas where a ball slides across and bounces off the edges while a frame counter climbs. A caption explains that the browser runs the cycle about 60 times a second and your eye turns the still frames into movement.](../assets/animation-loop.svg)

Each frame is a still picture with a tiny change. The browser shows sixty of them a second and your eye does the rest: every spinner, game, and growing chart you have seen on a web page is this loop. Events and the loop combine naturally. A `keydown` listener changes `speed`, the next frame uses it, and that is a game.

### <font color="#79c0ff">Activity 3</font>
<details>
<summary><strong>Bouncing Ball</strong></summary>

*Concept: Draw a frame, move the ball a little, and let the browser call you again until it looks like motion.*

![Animated diagram of the animation loop. On the left, four steps in a cycle that light up in turn: 1 clear the canvas, 2 draw everything, 3 move everything a little, 4 ask for the next frame with requestAnimationFrame. On the right, a canvas where a ball slides across and bounces off the edges while a frame counter climbs. A caption explains that the browser runs the cycle about 60 times a second and your eye turns the still frames into movement.](../assets/animation-loop.svg)

## Task

1. Add `<canvas id="stage" width="400" height="300"></canvas>` to `public/index.html`, create `scripts/ball.js` with the bouncing ball code from the lesson, and link it with its own `<script defer src="scripts/ball.js"></script>` tag. Refresh: the ball bounces.
2. Change `speed` to 8, then to 1. Change the ball's `fillStyle`. Each edit, save, refresh shows a different animation from the same loop.
3. Comment out the `clearRect` line and refresh. The ball leaves a trail, because every frame now draws on top of the last one. Put the line back.
4. Add a `keydown` listener: `ArrowUp` makes `speed` 1.5 times bigger and `ArrowDown` 1.5 times smaller. The next frame uses the new value. An event changing what the loop draws is the whole idea of a game.
5. In your terminal, run `firebase deploy --only hosting` and open your live address. The ball bounces for anyone, on any device.

*(Standalone file: [activities/03-bouncing-ball.md](../activities/03-bouncing-ball.md))*

</details>

---

← Back to [lesson](../README.md)
