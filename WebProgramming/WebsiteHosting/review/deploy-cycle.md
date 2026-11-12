# Review - The Firebase Deploy Cycle

*Originally covered in [Website Hosting](../README.md)*

---

| Command | What it does |
|---|---|
| `firebase login` | Connect your terminal to your Google account |
| `firebase init hosting` | Set up a folder for hosting (creates `firebase.json`, `.firebaserc`, `public/`) |
| `firebase emulators:start --only hosting` | Preview the site on your own machine. Nothing is published |
| `firebase deploy --only hosting` | Publish everything in `public/` to your live `*.web.app` URL |

| File or folder | Holds |
|---|---|
| `public/` | Everything that becomes the live website |
| `firebase.json` | Which folder to publish, and how |
| `.firebaserc` | Which Firebase project this folder belongs to |

---

## Tasks

1. Open your website project folder in a terminal.
2. Make one visible edit to a file in `public/` (change a heading or a CSS color).
3. Preview it locally and confirm the edit appears at the local address.
4. Deploy and confirm the same edit appears at your live `*.web.app` URL.
5. Commit and push the change so the repository matches the live site.
