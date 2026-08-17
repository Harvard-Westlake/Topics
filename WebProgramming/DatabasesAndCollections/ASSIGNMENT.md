# Assignment — Databases and Collections

**Due:** End of class (Part 1 is timed); Part 2 before next class  
**Points:** 10

---

## Part 1 — Timed Assignment (35 minutes)

On your personal website, using ANY resources you can (but no direct help from classmates):

1. Add support for **local storage** and **cookies** on your personal website
2. Research and implement a **Firestore database** on your website
3. Implement a combination of Firestore and local storage/cookies on your website **in a meaningful way** — the pieces should work together, not sit side by side
4. Test locally with `firebase serve`, then deploy the latest version of your website with `firebase deploy`
5. Submit the URL for your website as soon as it is uploaded

> **Note:**
> "Meaningful" means the storage serves the visitor. Examples: a guestbook whose entries live in Firestore while local storage remembers that *you* already signed it; a poll where cookies prevent double-voting and Firestore holds the tallies.

---

## Part 2 — Returning Visitors and Shared Data

Extend what you built with two specific features:

1. **Returning-visitor experience.** Create a setting using cookies which allows users to come back to your webpage and have a different experience than someone arriving there for the first time
2. **Shared database feature.** Write to (and read from) the database so that users of your site can all access and relate to the same data

Describe the two features you used to implement this in **fewer than 20 words**. Don't overthink it (seriously, don't).

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Local storage in use** — your site writes at least one value that survives a page refresh
- [ ] **Cookies in use** — a cookie changes the experience for a returning visitor
- [ ] **Firestore connected** — your site writes to and reads from a Firestore collection, visible in the Firebase console
- [ ] **Meaningful combination** — the browser storage and the database cooperate in one coherent feature
- [ ] **Deployed** — everything above works on your live `*.web.app` URL, not just locally
- [ ] **Console clean** — no errors on load or while using the storage features

---

## Submission

Submit **one text response** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Live URL:                          https://
Where local storage is used:       
Where cookies are used:            
Firestore collection name(s):      
Two features, under 20 words:      
```

> **Note:**
> Test the returning-visitor experience honestly: open your site in a private/incognito window to see the first-time view, then revisit in your normal browser to confirm the return view differs.
