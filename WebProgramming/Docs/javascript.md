<div align="center">

# JavaScript
*<font color="#8b949e">The language that makes web pages dynamic and interactive</font>*

</div>

---

## <font color="#388bfd">What JavaScript Is</font>

JavaScript is the **electricity and plumbing** — a full programming language that runs inside the browser, reacting to the user and rewriting the page while it is open. Load it from your HTML at the end of `<body>`:

```html
<script src="main.js"></script>
```

---

## <font color="#388bfd">Variables and Functions</font>

```javascript
let score = 0;                     // variable that can change
const maxScore = 100;              // constant - cannot be reassigned

function addPoints(points) {       // named function
  score = score + points;
  return score;
}

const double = (value) => value * 2;   // arrow function (compact form)
```

| Keyword | Use for |
|---|---|
| `const` | Everything by default — reassignment is an error |
| `let` | Values that genuinely change (counters, state) |

---

## <font color="#388bfd">Reaching Into the Page (the DOM)</font>

The browser exposes the page as the **DOM** — a tree of objects JavaScript can read and rewrite:

```javascript
const button = document.getElementById("start-button");   // find by id
const cards = document.querySelectorAll(".card");         // find all by CSS selector

button.textContent = "Go!";                 // change text
button.style.background = "gold";          // change style
button.classList.add("active");            // add a CSS class
```

---

## <font color="#388bfd">Events</font>

```javascript
// Element events
button.addEventListener("click", () => {
  console.log("clicked");
});

// Keyboard (attach to the whole document)
document.addEventListener("keydown", (event) => {
  console.log("key:", event.key);
});

// Mouse position
document.addEventListener("mousemove", (event) => {
  console.log(event.clientX, event.clientY);
});

// Timers - events you schedule yourself
setTimeout(() => console.log("once, after 2s"), 2000);
const ticker = setInterval(() => console.log("every second"), 1000);
clearInterval(ticker);             // stop a repeating timer
```

| Event family | Common events |
|---|---|
| Element | `click`, `input`, `submit` |
| Keyboard | `keydown`, `keyup` |
| Mouse | `mousemove`, `mousedown`, `mouseover` |
| Timers | `setTimeout`, `setInterval` |

---

## <font color="#388bfd">Classes</font>

```javascript
class Quiz {
  constructor(questions) {
    this.questions = questions;
    this.currentIndex = 0;
    this.correctCount = 0;
  }

  currentQuestion() {
    return this.questions[this.currentIndex];
  }

  answer(isCorrect) {
    if (isCorrect) this.correctCount = this.correctCount + 1;
    this.currentIndex = this.currentIndex + 1;
  }
}

const quiz = new Quiz(["Q1", "Q2", "Q3"]);
```

| Piece | Meaning |
|---|---|
| `constructor` | Runs once per `new`; sets up the instance's data |
| `this` | The specific instance being worked on |
| Method | A function every instance carries |

---

## <font color="#388bfd">Console Tools</font>

| Call | Shows |
|---|---|
| `console.log(value)` | Plain output — your everyday flashlight |
| `console.warn(value)` | Yellow warning |
| `console.error(value)` | Red error with a stack trace |
| `console.dir(object)` | Expandable tree of every property an object has |

Full walkthrough: the [Debugging JavaScript](../DebuggingJavaScript/) lesson.

---

## <font color="#388bfd">Storage Quick Reference</font>

```javascript
localStorage.setItem("theme", "dark");        // survives refresh, this browser only
localStorage.getItem("theme");                // "dark"
document.cookie = "visited=true; max-age=31536000";   // cookie, one year
```

Objects must be converted to strings on the way in and back on the way out:

```javascript
localStorage.setItem("player", JSON.stringify({ name: "Alice", level: 3 }));
const player = JSON.parse(localStorage.getItem("player"));
```

---

← Back to [Docs](README.md)
