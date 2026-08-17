<div align="center">

# Firebase Hosting
*<font color="#8b949e">Command reference and workflow for hosting your site on Firebase</font>*

</div>

---

## <font color="#388bfd">Command Reference</font>

| Command | What it does | Run it when |
|---|---|---|
| `firebase login` | Authenticates your terminal with your Google account | Once per machine (and after logouts) |
| `firebase init hosting` | Sets up the current folder for hosting | Once per project |
| `firebase serve` | Serves the site **locally** for preview — nothing is published | Every time you want to test changes |
| `firebase deploy` | Publishes `public/` to your live `*.web.app` URL | When the change is ready for the world |
| `firebase projects:list` | Lists the Firebase projects your account can see | When you forget a project's exact name |

Official CLI documentation: [firebase.google.com/docs/cli](https://firebase.google.com/docs/cli)

---

## <font color="#388bfd">Project Structure</font>

After `firebase init hosting`, your folder contains:

```
personalwebsite-<name>/
  firebase.json      — hosting configuration (which folder is public, rewrites)
  .firebaserc        — which Firebase project this folder deploys to
  public/            — THE WEBSITE: everything here becomes live on deploy
    index.html       — the page served at your site's root URL
```

Only what is inside the **public directory** goes live. Files next to it (like `firebase.json` itself, or your Git files) are never uploaded.

---

## <font color="#388bfd">The Workflow</font>

```
edit files in public/
        |
   firebase serve          <- check it locally at the printed address
        |
   looks right?
        |
   firebase deploy         <- live at https://<project>.web.app
        |
   open the URL and verify
```

> **Tip:**
> Deploy small and deploy often. A tiny change that breaks the live site is easy to find; twenty accumulated changes that break it are an archaeology project.

---

## <font color="#388bfd">Troubleshooting</font>

| Symptom | Likely cause | Fix |
|---|---|---|
| `firebase: command not found` | CLI not installed, or terminal not restarted | Reinstall per the [CLI docs](https://firebase.google.com/docs/cli); open a new terminal |
| `Error: Not in a Firebase app directory` | You are in the wrong folder | `cd` into the folder containing `firebase.json` |
| Deploy succeeds but the site shows the Firebase placeholder | Your files are not in the public directory | Move your `index.html` and assets into `public/` and redeploy |
| Deploy succeeds but changes don't appear | Browser cached the old page | Hard-refresh (`Cmd+Shift+R` / `Ctrl+Shift+R`) |
| `Site Not Found` at your URL | Wrong project in `.firebaserc`, or hosting never initialized | Check `.firebaserc` matches your project name; re-run `firebase init hosting` |
| Permission or login errors | Logged into the wrong Google account | `firebase logout`, then `firebase login` with the correct account |

---

← Back to [Docs](README.md)
