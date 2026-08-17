<div align="center">

# Debugging JavaScript
*<font color="#8b949e">DevTools, the console, and reading what the browser is telling you</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Why Debugging Is the Real Skill](#why-debugging-is-the-real-skill)**  
In an AI-assisted workflow, finding what's broken matters more than typing what works.

**[1. Opening the Developer Tools Window](#1-opening-the-developer-tools-window)**  
Every browser ships with a full debugging suite.

**[2. Using the Console for Debugging](#2-using-the-console-for-debugging)**  
`console.log()` — printing what your program is actually doing.

**[3. Catching Errors with console.error()](#3-catching-errors-with-consoleerror)**  
Making failures loud instead of silent.

**[4. Inspecting Objects with console.dir()](#4-inspecting-objects-with-consoledir)**  
Seeing everything an object contains.

**[Reading Stack Traces](#reading-stack-traces)**  
The error message is a map — here is how to read it.

---

## <font color="#388bfd">Why Debugging Is the Real Skill</font>

Last lesson you were promoted to manager: AI writes drafts, you verify them. Verification happens in exactly one place — the browser's **developer tools**. A manager who cannot read the console has no way to know whether the AI's confident "it works now" is true. Every lesson from here forward assumes you work with the console open.

---

## <font color="#388bfd">1. Opening the Developer Tools Window</font>

| Method | How |
|---|---|
| Keyboard (Mac) | `Cmd` + `Option` + `I` |
| Keyboard (Windows) | `F12` or `Ctrl` + `Shift` + `I` |
| Mouse | Right-click anywhere on the page → **Inspect** |

DevTools opens as a panel with several tabs. The two you need now:

| Tab | Shows |
|---|---|
| **Elements** | The live HTML of the page — as it exists *right now*, after JavaScript has modified it |
| **Console** | Messages your code prints, plus every error and warning the browser encounters |

> **Tip:**
> Keep DevTools docked to the side or bottom of the window while you develop, and reload the page after every change. Errors you never see are errors you never fix.

---

## <font color="#388bfd">2. Using the Console for Debugging</font>

`console.log()` prints values to the Console tab. It is the flashlight you point at your running program:

```javascript
const score = 42;
console.log("score is:", score);           // score is: 42

const player = { name: "Alice", level: 3 };
console.log("player:", player);            // player: {name: "Alice", level: 3}
```

Use it to answer the two questions behind almost every bug:

1. **Did this line even run?** Put a log at the top of the function. No message means the function was never called — the bug is upstream.
2. **What value does this variable actually hold?** Log it. `undefined`, `null`, or `NaN` where you expected a number is the bug's fingerprint.

You can also type JavaScript directly into the console and press Return — it runs immediately against the current page. Try `document.title` or `2 + 2`.

---

## <font color="#388bfd">3. Catching Errors with console.error()</font>

`console.error()` prints a message styled as an error — red, loud, and with a stack trace attached:

```javascript
function setVolume(level) {
  if (level < 0 || level > 10) {
    console.error("Volume must be 0-10, got:", level);
    return;
  }
  // ... proceed normally
}
```

Use it when your code detects a situation that should never happen. Unlike a silent `return`, an error message tells future-you (and your reviewer) exactly where the impossible thing occurred.

| Method | Appearance | Use for |
|---|---|---|
| `console.log()` | Plain text | Normal tracing while developing |
| `console.warn()` | Yellow warning | Suspicious but survivable situations |
| `console.error()` | Red error + stack trace | Things that should never happen |

---

## <font color="#388bfd">4. Inspecting Objects with console.dir()</font>

`console.log()` on an HTML element shows it as markup. `console.dir()` shows it as a **JavaScript object** — an expandable tree of every property it carries:

```javascript
const button = document.getElementById("clicker");

console.log(button);   // <button id="clicker">Click me</button>
console.dir(button);   // button#clicker (expandable tree) - open it to see .id,
                       // .textContent, .onclick, .style, and hundreds more properties
```

Reach for `console.dir()` when you know *which* object matters but not *what is inside it* — a perfect tool for exploring objects that AI-generated code handed you.

---

## <font color="#388bfd">Reading Stack Traces</font>

When JavaScript fails, the console prints an error like this:

```
Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')
    at setupButtons (game.js:12)
    at startGame (game.js:3)
    at main.js:8
```

Read it in three parts:

| Part | This example | What it tells you |
|---|---|---|
| **Error type + message** | `TypeError: Cannot read properties of null` | *What* went wrong — here, something was `null` when code expected an object |
| **Top line of the trace** | `at setupButtons (game.js:12)` | *Where* it broke — file `game.js`, line 12 |
| **Lines below** | `startGame` → `main.js:8` | *How the program got there* — the chain of calls, newest first |

For this error, line 12 of `game.js` called `.addEventListener` on the result of a `getElementById` that returned `null` — usually a typo in the id, or a script that ran before the element existed.

> **Note:**
> The most common beginner mistake is reading only the message and never the location. The trace hands you the exact file and line — click it in the console and the browser shows you the offending source.

> **Warning:**
> When you paste a stack trace to an AI and ask for a fix, it will propose one instantly and with total confidence — sometimes for a different bug than the one you have. Read the trace yourself first, form a hypothesis, and use the AI to check your reasoning rather than replace it.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you open DevTools with the keyboard shortcut and find the Console tab?
- [ ] Can you use `console.log()` to print a variable's value while a page runs?
- [ ] Can you state the difference between `console.log()`, `console.warn()`, and `console.error()`?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you use `console.dir()` to explore the properties of an HTML element?
- [ ] Can you read a stack trace and identify the error type, the file, and the line where it broke?
- [ ] Can you use a top-of-function `console.log()` to prove whether a function was ever called?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain why `getElementById` returning `null` leads to the exact TypeError shown in this lesson?
- [ ] Can you follow a stack trace downward to explain the full chain of calls that led to a crash?
- [ ] Can you diagnose a bug yourself from the trace, then use AI only to verify your hypothesis?

---

← [JavaScript and Coding with Cursor](../JavaScriptAndCursor/) — Next: [The Learning Widget Project](../LearningWidget/)
