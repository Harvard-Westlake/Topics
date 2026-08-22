<div align="center">

# Persistence and Intermediate Web
*<font color="#8b949e">Why everything your page knows vanishes on refresh — and how websites remember</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Research Topic (using AI)](#research-topic-using-ai)**  
Investigate today's central mystery before the lesson explains it.

**[The Goldfish Problem](#the-goldfish-problem)**  
JavaScript state lives in memory, and memory is wiped on every reload.

**[The Ladder of Persistence](#the-ladder-of-persistence)**  
Four places data can live, from vanishing to permanent and shared.

**[Interactive vs Persistent](#interactive-vs-persistent)**  
Two different upgrades, often confused — your widget needs both.

**[Trying It in the Console](#trying-it-in-the-console)**  
Watch persistence work with your own hands, no code files needed.

---

## <font color="#388bfd">Research Topic (using AI)</font>

Use the [research technique](../InterfacingWithAI/) to investigate:

- What happens to a JavaScript variable when the page reloads?
- How does a website remember that you are logged in, or what is in your shopping cart?
- What is the difference between data stored *in the browser* and data stored *on a server*?

Keep your answers — the lesson below is your verification source.

---

## <font color="#388bfd">The Goldfish Problem</font>

Your website is now interactive: buttons respond, timers tick, scores climb. But try this — build up a score in one of your JavaScript interactions, then press refresh.

Gone. Every variable back to its starting value.

That is not a bug. Every JavaScript variable lives in the browser's **memory for that page**, and reloading the page throws that memory away and starts the scripts from the top. Your site has the memory of a goldfish: brilliant in the moment, blank slate every time it wakes up.

Real websites remember. Carts survive a refresh. Settings survive a reboot. A **persistent** website is one whose important data outlives the page that created it.

---

## <font color="#388bfd">The Ladder of Persistence</font>

There are four rungs, each surviving more than the last:

| Rung | Where the data lives | Survives refresh? | Survives switching devices? | Shared between users? |
|---|---|---|---|---|
| **JavaScript variables** | Page memory | No | No | No |
| **Cookies** | The browser (sent to the server with requests) | Yes | No | No |
| **Local storage** | The browser | Yes | No | No |
| **A database** (Firestore) | A server in the cloud | Yes | Yes | Yes |

The pattern to remember:

```
variables      cookies / local storage        database
   |                    |                         |
this page           this browser              everyone
```

- **Browser storage** (cookies, local storage) makes a site remember *this visitor on this machine* — perfect for preferences, progress, "welcome back" experiences.
- **A database** makes data global — every visitor reads and writes the same shared records. That is what powers leaderboards, comments, and anything collaborative.

> **Note:**
> Next lesson, [Databases and Collections](../DatabasesAndCollections/), covers all three persistent rungs hands-on: local storage vs cookies in detail, then Firestore. Today is about understanding *why* each rung exists.

---

## <font color="#388bfd">Interactive vs Persistent</font>

These two words describe different upgrades, and intermediate websites need both:

| | Interactive | Persistent |
|---|---|---|
| **Question it answers** | Does the page *respond*? | Does the page *remember*? |
| **Powered by** | Events, timers, DOM updates | Cookies, local storage, databases |
| **Example** | A quiz that grades your answer instantly | A quiz that knows which levels you finished last week |

Your Learning Widget is already interactive. Ask yourself what it should *remember*: a best score? which sections a learner completed? feedback left by users? Each answer points at a rung of the ladder — and choosing the right rung is a design decision, not a technical accident.

---

## <font color="#388bfd">Trying It in the Console</font>

You can watch persistence work right now, with no code files. Open [DevTools](../DebuggingJavaScript/) on your own website and type into the console:

```javascript
// A plain variable — the bottom rung
let visits = 1;

// Local storage — one rung up
localStorage.setItem("visits", "1");
localStorage.getItem("visits");     // "1"
```

Now refresh the page and check both:

```javascript
visits;                              // ReferenceError - it never existed on this load
localStorage.getItem("visits");      // "1" - still there
```

The variable died with the old page. The local storage entry did not — it belongs to the *site*, not the page load.

> **Tip:**
> Local storage stores strings only. Numbers and objects go in through `JSON.stringify(value)` and come back out through `JSON.parse(text)` — you will use this constantly next lesson.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Explain what happens to JavaScript variables when a page reloads.
- [ ] Name the four rungs of the persistence ladder in order.
- [ ] State the difference between an interactive website and a persistent one.

### <font color="#79c0ff">Intermediate</font>

- [ ] Store a value in local storage from the console and prove it survives a refresh.
- [ ] Pick the right rung of the ladder for a "welcome back" message, and a different one for a public leaderboard.
- [ ] Explain why browser storage cannot follow a user to a different device.

### <font color="#79c0ff">Advanced</font>

- [ ] List two things your Learning Widget should remember and justify which rung each belongs on.
- [ ] Explain why `JSON.stringify` and `JSON.parse` are needed when storing objects in local storage.
- [ ] Describe what a shared database makes possible that browser storage never can.

---

← [The Learning Widget Project](../LearningWidget/) — Next: [Databases and Collections](../DatabasesAndCollections/)
