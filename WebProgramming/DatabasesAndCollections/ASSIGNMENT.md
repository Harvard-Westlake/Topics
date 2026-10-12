# Assignment - Databases and Collections

*Lesson: [Databases and Collections](README.md)*

**Due:** Before the start of next class

---

## What to Build

Your personal website, now with memory: browser storage for each visitor, and a Firestore database shared by everyone, working together.

The first 35 minutes of class are a **timed build**: get local storage, a cookie, and a Firestore read and write working on your live site, using any resources except direct help from classmates. Finish the rest for homework.

| Result | What it means |
|---|---|
| **Local storage** | Your site saves at least one value that is still there after a refresh. |
| **A returning-visitor cookie** | Someone coming back sees something different from a first-time visitor. |
| **A shared Firestore feature** | Your site writes to and reads from a Firestore collection, so every visitor sees the same data. |
| **Working together** | The browser storage and the database cooperate in one feature, for example a guestbook in Firestore where local storage remembers that *you* already signed it. |
| **Safe rules** | Your Firestore rules allow only what your site needs, not test mode. |
| **Live** | All of it works on your `*.web.app` URL, with no errors in the console. |

**Verify:**

1. Open your live site in a private or incognito window: you get the first-time experience.
2. Use the shared feature, then find the new document in the Firebase console.
3. Reload in your normal browser: the returning-visitor experience shows, and your local storage value is still there.
4. Open the site on a different device: the shared data is there; your local storage value is not.

---

## Success Criteria

- [ ] **Local storage in use:** a value survives a refresh.
- [ ] **Cookie in use:** a returning visitor sees something a first-time visitor does not.
- [ ] **Firestore connected:** your site writes and reads a collection you can see in the Firebase console.
- [ ] **Meaningful combination:** browser storage and the database work together in one feature.
- [ ] **Deployed and clean:** everything works on your live URL with no console errors, and your rules are no longer test mode.

---

## Submission

Submit **text** on Canvas. Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Live URL:                        https://
Where local storage is used:     
Where the cookie is used:        
Firestore collection name(s):    
The two features, under 20 words: 
```
