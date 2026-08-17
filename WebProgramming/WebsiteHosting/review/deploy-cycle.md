# Review — The Firebase Deploy Cycle

*Originally covered in [Website Hosting](../README.md)*

---

| Command | What it does |
|---|---|
| `firebase login` | Authenticate your terminal with your Google account |
| `firebase init hosting` | Set up a folder for hosting (creates `firebase.json`, `.firebaserc`, `public/`) |
| `firebase serve` | Preview the site locally — nothing published |
| `firebase deploy` | Publish everything in `public/` to your live `*.web.app` URL |

| File/folder | Holds |
|---|---|
| `public/` | Everything that becomes the live website |
| `firebase.json` | Hosting configuration |
| `.firebaserc` | Which Firebase project this folder belongs to |

---

## Tasks

1. Open your website project folder in a terminal
2. Make one visible edit to a file in `public/` (change a heading or a CSS color)
3. Run `firebase serve` and confirm the edit appears at the local address it prints
4. Run `firebase deploy` and confirm the same edit appears at your live `*.web.app` URL
5. Commit and push the change so the repository matches the live site
