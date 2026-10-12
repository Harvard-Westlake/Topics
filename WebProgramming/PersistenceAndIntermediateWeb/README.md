<div align="center">

# Persistence and Intermediate Web
*<font color="#8b949e">Persistence means your site remembers data after the page reloads, instead of starting over every time.</font>*

</div>

---

![The ladder of persistence, three rungs. Bottom: JavaScript variables, in this page's memory, gone the moment the page reloads. Middle: cookies and local storage, inside this one browser, survive a refresh but belong only to this visitor on this device. Top: a database (Firestore), on a server in the cloud, survives refresh, works from any device, and is shared with everyone. Each rung up lasts longer and reaches more people.](assets/persistence-ladder.svg)

Your page forgets everything when it reloads. Persistence is how websites remember:

- **Variables:** live only while the page is open.
- **Browser storage:** remembers this visitor, on this device.
- **A database:** remembers for everyone, everywhere.

## <font color="#388bfd">Table of Contents</font>

1. [Why everything vanishes when the page reloads](#the-goldfish-problem)
2. [The ladder: where data can live and how long it lasts](#the-ladder-of-persistence)
3. [Watch persistence work in the console](#trying-it-in-the-console)

## <font color="#388bfd">The Goldfish Problem</font>

Your site is interactive now: buttons respond and values change. Build up a score or a counter on your site, then press refresh.

Gone. Every variable is back to its starting value.

That is not a bug. Every JavaScript variable lives in the browser's memory **for that page**, and a reload throws that memory away and runs the scripts from the top again. Your site has the memory of a goldfish: sharp in the moment, blank every time it wakes up.

Real websites remember. A cart survives a refresh, and settings survive a restart. Those sites are **persistent**: their important data outlives the page that made it.

## <font color="#388bfd">The Ladder of Persistence</font>

| Rung | Where the data lives | Survives a refresh? | Follows you to another device? | Shared with other visitors? |
|---|---|---|---|---|
| **JavaScript variables** | This page's memory | No | No | No |
| **Cookies** | This browser (also sent to the server with each request) | Yes | No | No |
| **Local storage** | This browser | Yes | No | No |
| **A database** (Firestore) | A server in the cloud | Yes | Yes | Yes |

- **Browser storage** (cookies and local storage) remembers *this visitor on this machine*: preferences, progress, a "welcome back" message.
- **A database** remembers for the whole site: every visitor reads and writes the same records. That is what makes leaderboards, comments, and anything shared possible.

Picking a rung is a design choice. Ask what your site should remember, and who should see it. Next lesson, [Databases and Collections](../DatabasesAndCollections/), builds both kinds of storage for real.

## <font color="#388bfd">Trying It in the Console</font>

Open DevTools on your own site, go to the **Console**, and type:

```javascript
// A plain variable: the bottom rung
let visits = 1;

// Local storage: one rung up
localStorage.setItem("visits", "1");
localStorage.getItem("visits");     // "1"
```

Now refresh the page and check both:

```javascript
visits;                              // ReferenceError: it does not exist on this load
localStorage.getItem("visits");      // "1": still there
```

The variable died with the old page. The local storage entry did not, because it belongs to the **site**, not to one page load. You can see it in DevTools under **Application**, then **Local storage**.

> **Tip:** Local storage only holds text. Numbers and objects go in through `JSON.stringify(value)` and come back out through `JSON.parse(text)`.

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Explain what happens to a JavaScript variable when the page reloads, and why.
- [ ] Name the rungs of the persistence ladder in order, and pick the right one for a "welcome back" message and for a public leaderboard.
- [ ] Store a value in local storage from the console and prove it survives a refresh.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Save an object (like `{ name: "Ada", level: 3 }`) in local storage, refresh, and get it back as an object, not a string.

---

← [Debugging JavaScript](../DebuggingJavaScript/) | Next: [Databases and Collections](../DatabasesAndCollections/)
