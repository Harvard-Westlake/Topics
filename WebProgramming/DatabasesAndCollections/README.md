<div align="center">

# Databases and Collections
*<font color="#8b949e">Local storage, cookies, and a shared Firestore database your whole site can read and write</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Learning Objectives](#learning-objectives)**  
What you should be able to do by the end of this lesson.

**[Research Topic](#research-topic)**  
Use AI to investigate storage, Firestore, and rules before the lesson.

**[Local Storage vs Cookies](#local-storage-vs-cookies)**  
Two kinds of browser memory, built for different jobs.

**[What a Database Is and Why It Matters](#what-a-database-is-and-why-it-matters)**  
Shared, permanent, server-side data — and Firestore's document model.

**[Connecting to Firestore with the JavaScript SDK](#connecting-to-firestore-with-the-javascript-sdk)**  
Credentials, initialization, and your first connection.

**[CRUD: Writing and Reading Data](#crud-writing-and-reading-data)**  
PUT and GET — `setDoc` and `getDoc` in practice.

**[Firestore Rules](#firestore-rules)**  
Why the database needs a gatekeeper, and how to set one up.

---

## <font color="#388bfd">Learning Objectives</font>

By the end of this lesson, you will be able to:

1. Understand the fundamental concept of databases and their importance
2. Connect an app to Firebase Firestore using JavaScript SDK credentials
3. Implement basic CRUD operations (specifically, GET and PUT requests) with Firestore
4. Use `console.log()` to verify what your data code is actually doing

---

## <font color="#388bfd">Research Topic</font>

**Use AI to learn the following:**

- What is the difference between local storage and cookies?
- How is data stored with Google's Firestore Database?
- Why are rules necessary for a Firestore Database, and how are they set up?

Then read on and check the AI's answers against the lesson.

---

## <font color="#388bfd">Local Storage vs Cookies</font>

Both live in the browser and both survive a refresh — but they were built for different jobs:

| | Local storage | Cookies |
|---|---|---|
| **Size limit** | ~5 MB | ~4 KB |
| **Sent to the server with every request?** | No — stays in the browser | Yes — automatically attached |
| **Expiration** | Never (until cleared) | Optional expiry date |
| **Built for** | App data: settings, progress, saved state | Identity: sessions, "who is this visitor?" |
| **API feel** | Clean key-value methods | One awkward string |

```javascript
// Local storage - clean key-value pairs
localStorage.setItem("theme", "dark");
localStorage.getItem("theme");          // "dark"
localStorage.removeItem("theme");

// Cookies - one string, key=value pairs joined with ";"
document.cookie = "returningVisitor=true; max-age=31536000";  // lasts one year
console.log(document.cookie);           // "returningVisitor=true"
```

> **Tip:**
> Rule of thumb: cookies answer *"who is visiting?"*, local storage answers *"what has this visitor done here?"* A returning-visitor experience is classic cookie territory; a saved quiz score is classic local storage.

Both are still **per-browser** — clear the browser data, or switch devices, and it is gone. For data that belongs to your *site* rather than one visitor's browser, you need a database.

---

## <font color="#388bfd">What a Database Is and Why It Matters</font>

A **database** is an organized store of data on a server, built to be read and written by many users at once, safely and permanently. Every leaderboard, comment section, and shared document you have ever used is a database wearing a costume.

We use **Cloud Firestore**, the database in your existing Firebase project. Firestore organizes data into **collections** of **documents**:

```
firestore/
  guestbook/                  <- a COLLECTION (like a folder)
    visitor-001               <- a DOCUMENT (like a file)
      { name: "Alice", message: "Cool widget!" }
    visitor-002
      { name: "Ben", message: "The slider is great" }
  scores/
    high-score
      { player: "Cam", points: 9800 }
```

| Firestore term | Think of it as | Holds |
|---|---|---|
| **Collection** | A folder | Documents |
| **Document** | A file with a name (ID) | Fields — key-value data |
| **Field** | One labeled value | Strings, numbers, booleans, lists, nested objects |

To turn Firestore on: in the [Firebase console](https://console.firebase.google.com/), open your project → **Firestore Database** → **Create database** → start in **test mode** for now (we fix that in [Firestore Rules](#firestore-rules)).

---

## <font color="#388bfd">Connecting to Firestore with the JavaScript SDK</font>

Your web page talks to Firestore through the **JavaScript SDK**, using credentials that identify *your* Firebase project. Get them from the console: **Project settings → Your apps → Web app → SDK setup and configuration**.

```html
<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
  import { getFirestore, doc, getDoc, setDoc }
    from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

  // Your project's credentials - copy YOUR OWN values from the Firebase console
  const firebaseConfig = {
    apiKey: "AIza...",
    authDomain: "personalwebsite-mike.firebaseapp.com",
    projectId: "personalwebsite-mike",
    appId: "1:1234567890:web:abc123"
  };

  const app = initializeApp(firebaseConfig);
  const database = getFirestore(app);
  console.log("Connected to Firestore:", database.app.options.projectId);
</script>
```

> **Note:**
> These credentials are not a password — they only *identify* your project, and every visitor's browser can see them in your source code. What visitors are *allowed to do* with them is decided entirely by your [Firestore rules](#firestore-rules). That is why rules matter.

---

## <font color="#388bfd">CRUD: Writing and Reading Data</font>

Database operations come in four flavors — **C**reate, **R**ead, **U**pdate, **D**elete. Today's focus is the two you need first: writing (PUT) and reading (GET).

**PUT — write a document with `setDoc`:**

```javascript
await setDoc(doc(database, "guestbook", "visitor-001"), {
  name: "Alice",
  message: "Cool widget!",
  visitedAt: Date.now()
});
console.log("Saved visitor-001");
```

**GET — read a document with `getDoc`:**

```javascript
const snapshot = await getDoc(doc(database, "guestbook", "visitor-001"));

if (snapshot.exists()) {
  console.log("Document data:", snapshot.data());
} else {
  console.log("No such document");
}
```

Three habits that prevent an afternoon of confusion:

1. **`console.log()` everything** while developing — the data you *think* you wrote and the data you *actually* wrote are often different
2. **`await` matters** — database calls take time; without `await`, you log the request instead of the result
3. **Check `snapshot.exists()`** — reading a document that is not there is not an error, it is just empty

> **Tip:**
> Open the Firebase console's **Firestore Database** tab side-by-side with your site. Every `setDoc` should appear there within seconds — if it does not, your write did not happen, no matter what the AI says.

---

## <font color="#388bfd">Firestore Rules</font>

Here is the uncomfortable truth from earlier: your config is public, so **anyone** can open DevTools on your site, copy your credentials, and send their own reads and writes to your database. Nothing stops them — except rules.

**Firestore security rules** are the gatekeeper that runs on Google's servers, checking every single request before it touches your data. Edit them in the console: **Firestore Database → Rules**.

Test mode's rule — fine for today's experiments, dangerous long-term:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;      // ANYONE can read and write ANYTHING
    }
  }
}
```

A more sensible shape — public reads, but writes only where you intend them:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /guestbook/{entry} {
      allow read: if true;             // anyone may read the guestbook
      allow write: if true;            // and sign it
    }
    match /{document=**} {
      allow read, write: if false;     // everything else is locked
    }
  }
}
```

| Rules say... | Result |
|---|---|
| `if true` everywhere | Strangers can fill, corrupt, or empty your database |
| `if false` everywhere | Even your own site cannot read or write |
| Per-collection rules | Each collection allows exactly what your site needs |

> **Warning:**
> Rules are necessary because the database is reachable by anyone on the internet, with or without your website in between. Test mode also expires after 30 days — when your widget suddenly cannot read or write, expired rules are the first suspect.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] State two differences between local storage and cookies and one job each is best at.
- [ ] Explain what a collection and a document are in Firestore.
- [ ] Name the four CRUD operations and identify which two this lesson implements.

### <font color="#79c0ff">Intermediate</font>

- [ ] Connect a page to Firestore with the SDK and prove the connection with `console.log()`.
- [ ] Write a document with `setDoc`, read it back with `getDoc`, and see it in the Firebase console.
- [ ] Explain why your Firebase config being public is safe only if your rules are right.

### <font color="#79c0ff">Advanced</font>

- [ ] Combine browser storage and Firestore in one feature and justify which data went where.
- [ ] Write a rule set that allows public reads of one collection and blocks everything else.
- [ ] Explain what `await` does in a database call and what you would see without it.

---

[Assignment](ASSIGNMENT.md)

← [Persistence and Intermediate Web](../PersistenceAndIntermediateWeb/) — Next: [UX and Behavior Tracking](../UXAndBehaviorTracking/)
