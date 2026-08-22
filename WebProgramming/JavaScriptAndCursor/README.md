<div align="center">

# JavaScript and Coding with Cursor
*<font color="#8b949e">Web events, classes, and your promotion from coder to manager</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Learning Objectives](#learning-objectives)**  
What you should be able to do by the end of this lesson.

**[Research Topic (with AI)](#research-topic-with-ai)**  
Warm up on today's vocabulary before writing any code.

**[Part 1: Web Event Binding](#part-1-web-event-binding)**  
Elements, keyboard, mouse, and timers — how a page reacts to the user.

**[Part 2: JavaScript Classes](#part-2-javascript-classes)**  
Organizing code with class-based structure.

**[Congratulations on Your Promotion](#congratulations-on-your-promotion)**  
You are not just a coder anymore — you are a manager. Ask, Plan, and Agent in Cursor.

---

## <font color="#388bfd">Learning Objectives</font>

By the end of this lesson, you should be able to:

1. Introduce yourself to JavaScript and CSS
2. Bind JavaScript to web events: element clicks, keyboard input, mouse movement, and timers
3. Structure code with JavaScript classes
4. Understand the ways you can interact with AI in Cursor — **Ask**, **Plan**, and **Agent**
5. Expect AI to make mistakes — and to confidently insist it is correct anyway

---

## <font color="#388bfd">Research Topic (with AI)</font>

Use the [research technique](../InterfacingWithAI/) to answer:

- What is JavaScript, and how is it different from HTML and CSS?
- What is an **event** in a browser? Name five events a user can trigger.
- What does it mean to "listen" for an event?

Cross-check against the [JavaScript reference doc](../Docs/javascript.md) when you are done.

---

## <font color="#388bfd">Part 1: Web Event Binding</font>

A web page without JavaScript is a poster. With JavaScript, it becomes a machine that *responds*. The mechanism is always the same: pick an element, name an event, attach a function. The function runs every time the event fires.

```html
<button id="clicker">Click me</button>
<p id="output">0 clicks</p>

<script>
  let clickCount = 0;
  const button = document.getElementById("clicker");
  const output = document.getElementById("output");

  button.addEventListener("click", () => {
    clickCount = clickCount + 1;
    output.textContent = clickCount + " clicks";
  });
</script>
```

The four families of events you will use constantly:

| Family | Event examples | Typical use |
|---|---|---|
| **Element** | `click`, `input`, `submit` | Buttons, forms, text boxes |
| **Keyboard** | `keydown`, `keyup` | Game controls, shortcuts |
| **Mouse** | `mousemove`, `mousedown`, `mouseover` | Drawing, hover effects, drag |
| **Timers** | `setTimeout`, `setInterval` | Animation, countdowns, auto-updates |

Keyboard events attach to the whole document:

```javascript
document.addEventListener("keydown", (event) => {
  console.log("You pressed: " + event.key);
});
```

Timers are not user events — they are events you schedule yourself:

```javascript
// Run once, after 2 seconds (2000 milliseconds)
setTimeout(() => { console.log("Two seconds passed"); }, 2000);

// Run every second, forever (until cleared)
setInterval(() => { console.log("Tick"); }, 1000);
```

> **Tip:**
> Every interactive thing you have ever done on a website — every like button, every game, every autocomplete — is some combination of these four families. Master them and nothing on the web looks like magic anymore.

---

## <font color="#388bfd">Part 2: JavaScript Classes</font>

As soon as a page does more than one thing, loose functions and global variables turn into spaghetti. **Classes** bundle related data and behavior into one named structure:

```javascript
class ScoreKeeper {
  constructor(playerName) {
    this.playerName = playerName;
    this.score = 0;
  }

  addPoints(points) {
    this.score = this.score + points;
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
| `constructor` | Runs once when `new` creates an instance; sets up starting data |
| `this` | The specific instance being worked on |
| Methods (`addPoints`, `display`) | Behavior every instance can perform |
| `new ScoreKeeper("Alice")` | An **instance** — one concrete object built from the blueprint |

Class-based structure matters for this unit because your Learning Widget will have real moving parts — a quiz engine, a score tracker, an animation loop — and each deserves its own class rather than a pile of shared globals.

---

## <font color="#388bfd">Congratulations on Your Promotion</font>

You are no longer just a coder. Instead, you are a **manager**. Your new tasks are to:

- **Plan** out how you want to architect an application
- **Choose** the way in which you want things coded
- **Debug** the imperfect AI responses

Cursor gives you three ways to interact with AI, and choosing the right one is a management decision:

| Mode | What it does | Use it when |
|---|---|---|
| **Ask** | Answers questions about code — explains, suggests, teaches | You want to *understand* what to do |
| **Plan** | Helps design and architect before any code is written | You want to *decide how* to build it |
| **Agent** | Writes and edits code across your files | You know what you want and are ready to *delegate the typing* |

The order matters. Managers who skip straight to Agent get code they do not understand, solving a problem they never defined.

> **Warning:**
> Expect AI to make mistakes — and then confidently insist it is correct. It will tell you code works that has never been run. It will "fix" a bug by breaking something else. The AI writes drafts; **you** are the one whose name is on the commit. Verify everything in the browser and the console, never in the chat window.

A good management loop for any feature:

1. **Ask** until you can describe the feature precisely in plain English
2. **Plan** the pieces — what files, what classes, what events
3. **Agent** one piece at a time, small enough to test immediately
4. Test in the browser with the console open; make the AI fix what is actually broken, not what it claims is broken

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Attach a click handler to a button and change text on the page when it fires.
- [ ] Name the four families of events and one example of each.
- [ ] State what Cursor's Ask, Plan, and Agent modes each do.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain the difference between `setTimeout` and `setInterval` and pick the right one for a countdown clock.
- [ ] Write a class with a constructor and two methods, and create two independent instances of it.
- [ ] Explain why a manager uses Ask and Plan before Agent.

### <font color="#79c0ff">Advanced</font>

- [ ] Combine a keyboard event, a timer, and a class into one small interactive program.
- [ ] Catch an AI-generated bug by testing in the browser rather than trusting the chat.
- [ ] Explain what `this` refers to inside a method and why each instance keeps its own data.

---

[Assignment](ASSIGNMENT.md)

← [Website Hosting](../WebsiteHosting/) — Next: [Debugging JavaScript](../DebuggingJavaScript/)
