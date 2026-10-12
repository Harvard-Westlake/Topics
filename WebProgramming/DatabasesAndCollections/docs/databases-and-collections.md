<div align="center">

# Databases and Collections
*<font color="#8b949e">A database is data kept on a server, so every visitor to your site reads and writes the same records.</font>*

</div>

---

![On the left, two visitors' browsers each run your site with their own browser storage: one has local storage theme=dark and the cookie returning=true, the other has theme=light and no cookie because it is a first visit. Arrows from both go through an orange bar labeled rules, which checks every request, to Firestore on the right, shared by everyone. Firestore holds a collection called guestbook with documents visitor-001 (name Alice, message Cool site!) and visitor-002, and a collection called scores with a document high-score (points 9800). Browser storage belongs to one visitor on one device; Firestore belongs to the whole site, but only allows what the rules allow.](../assets/firestore-layout.svg)

Last lesson's ladder had two persistent rungs. Today you build both:

- **Browser storage:** local storage and cookies remember one visitor on one device.
- **Firestore:** a database of **collections** (like folders) holding **documents** (like files), shared by every visitor.
- **Rules:** decide what anyone on the internet is allowed to read or write.

## <font color="#388bfd">Table of Contents</font>

1. [Local storage vs cookies: two kinds of browser memory](#local-storage-vs-cookies)
2. [Firestore: collections, documents, and connecting your site](#firestore-collections-and-documents)
3. [Writing and reading documents](#writing-and-reading-documents)
4. [Rules: the gatekeeper for your database](#firestore-rules)

## <font color="#388bfd">Local Storage vs Cookies</font>

Both live in the browser and both survive a refresh, but they were built for different jobs:

| | Local storage | Cookies |
|---|---|---|
| **Size limit** | About 5 MB | About 4 KB |
| **Sent to the server with every request?** | No, it stays in the browser | Yes, automatically |
| **Expires?** | Never, until cleared | Whenever you set it to |
| **Built for** | Settings, progress, saved state | "Who is this visitor?": sessions and returning visitors |

```javascript
// Local storage: simple key and value
localStorage.setItem("theme", "dark");
localStorage.getItem("theme");          // "dark"
localStorage.removeItem("theme");

// Cookies: one string of key=value pairs, joined by ";"
document.cookie = "returningVisitor=true; max-age=31536000; SameSite=Lax";  // lasts one year
console.log(document.cookie);           // "returningVisitor=true"
```

Both show up in DevTools under **Application**. Both are still **per browser**: clear the browser data or switch devices and they are gone. Data that belongs to the whole site needs a database.

## <font color="#388bfd">Firestore: Collections and Documents</font>

A **database** stores data on a server so many people can read and write it at once, safely and permanently. Every leaderboard, comment section, and shared document you have used is a database underneath.

We use **Cloud Firestore**, part of the Firebase project you already have. It stores data as **collections** of **documents**:

| Firestore term | Think of it as | Holds |
|---|---|---|
| **Collection** | A folder | Documents |
| **Document** | A file with a name (its ID) | Fields |
| **Field** | One labeled value | Text, numbers, true or false, lists, or nested objects |

**Turn it on.** In the [Firebase console](https://console.firebase.google.com/), open your project, then **Build**, then **Firestore Database**, then **Create database**. If asked, choose the **Standard** edition, pick a location near you, and start in **test mode** for now.

**Connect your site.** In **Project settings**, under **Your apps**, add a **Web** app. Firebase shows a `firebaseConfig` with your project's values. Add a module script to your page:

```html
<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";
  import { getFirestore, doc, getDoc, setDoc }
    from "https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js";

  // Copy YOUR OWN values from the Firebase console
  const firebaseConfig = {
    apiKey: "AIza...",
    authDomain: "personalwebsite-mike.firebaseapp.com",
    projectId: "personalwebsite-mike",
    appId: "1:1234567890:web:abc123"
  };

  const app = initializeApp(firebaseConfig);
  const database = getFirestore(app);
  console.log("Connected to Firestore:", app.options.projectId);
</script>
```

If the console's snippet shows a newer version number than `12.0.0`, use theirs in both import lines.

> **Note:** This config is not a password. It only says which project to talk to, and anyone can read it in your page's source. What visitors are *allowed* to do with it is decided by your [rules](#firestore-rules).

## <font color="#388bfd">Writing and Reading Documents</font>

The four things a database does are **C**reate, **R**ead, **U**pdate, and **D**elete (CRUD). Today you need two: writing a document and reading it back.

**Write a document with `setDoc`:**

```javascript
await setDoc(doc(database, "guestbook", "visitor-001"), {
  name: "Alice",
  message: "Cool site!",
  visitedAt: Date.now()
});
console.log("Saved visitor-001");
```

**Read it back with `getDoc`:**

```javascript
const snapshot = await getDoc(doc(database, "guestbook", "visitor-001"));

if (snapshot.exists()) {
  console.log("Document data:", snapshot.data());
} else {
  console.log("No such document");
}
```

Three habits that save an afternoon:

1. **Log everything** while you build. The data you think you wrote and the data you actually wrote are often different.
2. **`await` every database call.** Talking to a server takes time; without `await`, you get the unfinished request instead of the result.
3. **Check `snapshot.exists()`.** Reading a document that is not there is not an error, it is just empty.

> **Tip:** Keep the console's **Firestore Database** page open next to your site. Every `setDoc` should appear there within seconds. If it does not, the write did not happen.

## <font color="#388bfd">Firestore Rules</font>

Your config is public, so anyone can copy it and send their own reads and writes straight to your database, without ever visiting your site. **Security rules** run on Google's servers and check every request before it touches your data. Edit them in **Firestore Database**, then **Rules**.

Test mode lets anyone read and write anything, but only until a date about 30 days away:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.time < timestamp.date(2026, 11, 12);
    }
  }
}
```

When that date passes, every read and write fails. Replace it with rules that allow only what your site needs:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /guestbook/{entry} {
      allow read: if true;                       // anyone may read the guestbook
      allow create: if request.resource.data.message is string
                    && request.resource.data.message.size() <= 200;   // and sign it, briefly
    }
    match /{document=**} {
      allow read, write: if false;               // everything else is locked
    }
  }
}
```

| Rules that say | Result |
|---|---|
| `if true` everywhere | Strangers can fill, change, or empty your database. |
| `if false` everywhere | Even your own site cannot read or write. |
| One rule per collection | Each collection allows exactly what your site needs. |

> **Warning:** When your site suddenly cannot read or write, check the rules first: an expired test-mode date is the most common cause.

---

← Back to [lesson](../README.md)
