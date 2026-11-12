<div align="center">

# Debugging JavaScript
*<font color="#8b949e">Debugging is finding out what your code actually does, using the tools built into every browser.</font>*

</div>

---

![Reading an error in the DevTools Console tab. The console shows "Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')" followed by three lines: at setupButtons (game.js:12:10), at startGame (game.js:3:3), at main.js:8:1. Labels explain the parts: the message says WHAT broke, the top line says WHERE it broke (file game.js, line 12), and the lines below say HOW the program got there, newest first. Clicking the file and line jumps to that spot in your code.](../assets/stack-trace.svg)

Your code does exactly what it says, not what you meant. Debugging closes that gap:

- **DevTools:** a panel in every browser that shows what your page is really doing.
- **The console:** where your code can print values, and where every error shows up.
- **A stack trace:** the error's map, pointing at the exact file and line that broke.

## <font color="#388bfd">Table of Contents</font>

1. [Open the developer tools and find the right panel](#opening-devtools)
2. [Print what your program is doing with the console](#printing-with-the-console)
3. [Read a stack trace to find where it broke](#reading-a-stack-trace)

## <font color="#388bfd">Opening DevTools</font>

| Browser | How |
|---|---|
| Chrome or Edge (Mac) | `Cmd` + `Option` + `I` |
| Chrome or Edge (Windows) | `F12` or `Ctrl` + `Shift` + `I` |
| Any browser | Right-click the page, then **Inspect** |

DevTools opens as a panel with several tabs. The ones you need:

| Panel | Shows |
|---|---|
| **Elements** | The live HTML of the page, as it is right now after JavaScript changed it. |
| **Console** | Messages your code prints, plus every error and warning. |
| **Sources** | Your files, where you can pause the code on any line. |
| **Application** | What the site has saved in this browser: local storage and cookies. |

> **Tip:** Keep DevTools open while you work, and reload after every change. An error you never see is an error you never fix.

## <font color="#388bfd">Printing with the Console</font>

`console.log()` prints values to the Console. It is a flashlight pointed at your running program:

```javascript
const score = 42;
console.log("score is:", score);           // score is: 42

const player = { name: "Alice", level: 3 };
console.log("player:", player);            // player: {name: 'Alice', level: 3}
```

It answers the two questions behind almost every bug:

1. **Did this line run at all?** Put a log at the top of the function. No message means the function was never called, so the bug is earlier.
2. **What does this variable really hold?** Log it. `undefined`, `null`, or `NaN` where you expected a number is the bug's fingerprint.

The console has a few more tools:

| Call | Looks like | Use it for |
|---|---|---|
| `console.log()` | Plain text | Tracing while you work. |
| `console.warn()` | Yellow warning | Something odd that the page survives. |
| `console.error()` | Red error, with a stack trace | Something that should never happen. |
| `console.dir()` | An expandable tree | Seeing every property inside an object, like an HTML element. |
| `console.table()` | A table | Lists of objects, one row each. |

You can also type JavaScript straight into the console and press Return to run it against the page. Try `document.title` or `2 + 2`.

## <font color="#388bfd">Reading a Stack Trace</font>

When JavaScript fails, the console prints an error like the one in the diagram above:

```
Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')
    at setupButtons (game.js:12:10)
    at startGame (game.js:3:3)
    at main.js:8:1
```

| Part | In this example | Tells you |
|---|---|---|
| **The message** | `TypeError: Cannot read properties of null` | What went wrong: something was `null` where code expected an element. |
| **The top line** | `at setupButtons (game.js:12:10)` | Where: file `game.js`, line 12, column 10. |
| **The lines below** | `startGame`, then `main.js:8` | How the program got there: the calls before it, newest first. |

Here, line 12 called `.addEventListener` on the result of a `getElementById` that found nothing. That is usually a typo in the id, or a script that ran before the element existed.

> **Note:** The most common mistake is reading only the message and never the location. Click `game.js:12:10` in the console and DevTools shows you the exact line.

---

← Back to [lesson](../README.md)
