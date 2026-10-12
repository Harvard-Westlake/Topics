<div align="center">

# JavaScript Events and Classes
*<font color="#8b949e">JavaScript makes a page react: when something happens, a function you wrote runs and changes the page.</font>*

</div>

---

![How a page reacts, in four steps. 1: something happens, such as a click, a key press, mouse movement, or a timer firing. 2: it happens on an element, here a button with id clicker that is listening for click. 3: the function attached to it runs, adding one to clickCount and writing the new count into the page. 4: the page changes and now shows 3 clicks. The pattern is pick an element, name an event, attach a function, written as button.addEventListener("click", () => { ... }).](../assets/event-flow.svg)

HTML is the page and CSS is its look. JavaScript is what happens next:

- **An event:** something happens, like a click, a key press, or a timer going off.
- **A listener:** a function you attach to an element for one kind of event.
- **A class:** a blueprint that keeps related data and functions together once the page does more than one thing.

## <font color="#388bfd">Table of Contents</font>

1. [Making the page react to an event](#making-the-page-react)
2. [The four families of events](#the-four-families-of-events)
3. [Organizing the code with classes](#organizing-code-with-classes)

## <font color="#388bfd">Making the Page React</font>

Every reaction follows the same three steps: pick an element, name an event, attach a function. The function runs every time the event fires.

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

Keep JavaScript in its own file and link it from the HTML, just before `</head>`:

```html
<script src="clicker.js" defer></script>
```

`defer` waits until the whole page has loaded before running the file, so `getElementById` finds the button instead of `null`.

## <font color="#388bfd">The Four Families of Events</font>

Every like button, game, and autocomplete you have used is some mix of these:

| Family | Examples | Typical use |
|---|---|---|
| **Element** | `click`, `input`, `submit` | Buttons, forms, text boxes |
| **Keyboard** | `keydown`, `keyup` | Game controls, shortcuts |
| **Mouse** | `mousemove`, `mousedown`, `mouseover` | Drawing, hover effects, dragging |
| **Timers** | `setTimeout`, `setInterval` | Animation, countdowns, auto-updates |

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

## <font color="#388bfd">Organizing Code with Classes</font>

Once a page does more than one thing, loose variables and functions turn into spaghetti. A **class** bundles related data and behavior into one named blueprint:

```javascript
class ScoreKeeper {
  constructor(playerName) {
    this.playerName = playerName;
    this.score = 0;
  }

  addPoints(points) {
    this.score += points;
  }

  display() {
    return this.playerName + ": " + this.score;
  }
}

const alice = new ScoreKeeper("Alice");
alice.addPoints(10);
console.log(alice.display());   // Alice: 10
```

| Piece | What it is |
|---|---|
| `class ScoreKeeper` | The blueprint |
| `constructor` | Runs once when `new` builds an instance, and sets up its starting data |
| `this` | The one instance being worked on right now |
| `addPoints`, `display` | Methods: behavior every instance can do |
| `new ScoreKeeper("Alice")` | An **instance**: one real object built from the blueprint |

Two instances never share data: `new ScoreKeeper("Bo")` starts at 0 no matter what Alice scored. That is why a game's score, timer, and board each deserve their own class.

---

← Back to [lesson](../README.md)
