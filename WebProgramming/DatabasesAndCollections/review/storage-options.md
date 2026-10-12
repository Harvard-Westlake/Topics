# Review - Web Storage Options

*Originally covered in [Databases and Collections](../README.md)*

---

| Option | Where it lives | Survives refresh | Shared between visitors | Typical job |
|---|---|---|---|---|
| JavaScript variable | Page memory | No | No | State while the page is open |
| Cookie | Browser (sent to the server) | Yes | No | Identity, returning visitors |
| Local storage | Browser | Yes | No | Settings, progress, saved state |
| Firestore | Google's servers | Yes | Yes | Shared data: leaderboards, guestbooks |

| Call | Does |
|---|---|
| `localStorage.setItem("key", "value")` / `getItem("key")` | Write / read browser storage |
| `document.cookie = "key=value; max-age=31536000; SameSite=Lax"` | Set a cookie for one year |
| `setDoc(doc(database, "collection", "id"), {...})` | Write a Firestore document |
| `getDoc(doc(database, "collection", "id"))` | Read a Firestore document |

---

## Tasks

1. In the console on your own site, store a value in local storage, refresh, and read it back.
2. Set a cookie in the console and confirm it appears in `document.cookie` after a refresh.
3. Write one Firestore document from your site, then find it in the Firebase console.
4. For each of these, say where the data belongs: a dark-mode preference, a "welcome back" flag, a public high-score table.
5. Open your site in a private window and explain which stored values are missing there, and why.
