<div align="center">

# Website Hosting
*<font color="#8b949e">Hosting puts your website's files on a server that is always on, so anyone with the link can open it.</font>*

</div>

---

![How a hosted website works. On the left, your laptop holds a public/ folder with index.html, styles.css, and script.js; only you can open these. An arrow labeled firebase deploy copies the folder to Firebase's servers, which are always on and serve it at your-project-id.web.app. Arrows from the servers go to a phone and a classmate: anyone who visits the URL gets the files. Visitors only see what you last deployed, and a saved change that was never deployed stays invisible.](../assets/hosting-layout.svg)

A website is just files. Hosting is what lets other people see them:

- **On your laptop:** only you can open the page.
- **Deploying:** copies those files to a server that never turns off.
- **The URL:** where anyone in the world can ask that server for your page.

## <font color="#388bfd">Table of Contents</font>

1. [Make your first web page and learn its three languages](#your-first-web-page)
2. [What happens when someone visits your site](#what-hosting-means)
3. [Setting up Firebase Hosting on your computer](#setting-up-firebase-hosting)
4. [The edit, preview, deploy loop](#the-deploy-loop)

## <font color="#388bfd">Your First Web Page</font>

Every page you have ever visited is built from the same three ingredients. Think of a building:

| Language | What it does | In a building |
|---|---|---|
| **HTML** | The structure and the content: headings, paragraphs, images, links. | The frame |
| **CSS** | The look: colors, fonts, spacing, layout. | The paint and decoration |
| **JavaScript** | The behavior: things that happen when you click, type, or wait. | The electricity |

Today is about HTML and CSS. JavaScript gets its own lesson next. Keep the references open as you work: [HTML](../../Docs/html.md), [CSS](../../Docs/css.md), [JavaScript](../../Docs/javascript.md).

To make a page, in Cursor open a new folder (**File → Open Folder**), create a file named `index.html`, and type (not paste) this:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>My First Page</title>
  </head>
  <body>
    <h1>Hello from Cursor</h1>
    <p>This page was written by hand.</p>
  </body>
</html>
```

Save it, then double-click `index.html` in Finder or File Explorer. It opens in your browser.

Now change the heading, **save**, and **refresh** the browser. This edit, save, refresh loop is the heartbeat of web development. If a change does not appear, you forgot to save or to refresh: check both before anything else.

## <font color="#388bfd">What Hosting Means</font>

Your `index.html` works, but only on your machine. When someone types your site's URL:

1. Their browser asks the server at that address for the page.
2. The server sends back the files: the HTML, then the CSS and JavaScript it links to.
3. The browser draws the page from those files.

A **server** is just a computer that is always on, always online, and answers those requests. **Hosting** means putting your files on one. We use **Firebase Hosting**, a free Google service that gives every project two addresses, `your-project-id.web.app` and `your-project-id.firebaseapp.com`, both secured with HTTPS.

## <font color="#388bfd">Setting Up Firebase Hosting</font>

1. **Create a Firebase project.** At [console.firebase.google.com](https://console.firebase.google.com/), sign in with your **personal** Google account (not your school one) and create a project named `personalwebsite-<your first name>`. Firebase may add a few characters to make the **project ID** unique; the project ID is what appears in your URL. You can turn off Google Analytics and Gemini for this project.
2. **Install the Firebase CLI.** The CLI (command-line interface) lets your terminal talk to Firebase. In your terminal (Mac or WSL):
   ```bash
   curl -sL https://firebase.tools | bash
   ```
3. **Log in.** In your terminal:
   ```bash
   firebase login
   ```
   A browser opens. Sign in with the same personal Google account and choose **Allow**.
4. **Initialize hosting.** Make a folder named after your project, open it in Cursor, and in its terminal run:
   ```bash
   firebase init hosting
   ```
   | Prompt | Answer |
   |---|---|
   | Please select an option | **Use an existing project**, then pick yours |
   | What do you want to use as your public directory? | `public` (press Return) |
   | Configure as a single-page app (rewrite all urls to /index.html)? | `N`: this site has real pages |
   | Set up automatic builds and deploys with GitHub? | `N` |

   Firebase creates three things:

   ```
   personalwebsite-<name>/
     firebase.json   which folder to publish, and how
     .firebaserc     which Firebase project this folder belongs to
     public/         everything in here becomes your website
   ```

## <font color="#388bfd">The Deploy Loop</font>

Web developers repeat the same loop all day:

1. **Edit** a file in `public/` and save it.
2. **Preview** it on your own machine. Nothing is published:
   ```bash
   firebase emulators:start --only hosting
   ```
   Open the local address it prints (usually `http://localhost:5000`). Press `Ctrl+C` to stop it.
3. **Deploy** it to the world:
   ```bash
   firebase deploy --only hosting
   ```
   The output ends with your **Hosting URL**, for example `https://personalwebsite-mike.web.app`.
4. **Verify** by opening that URL yourself. If you do not see the change, hard-refresh (`Cmd+Shift+R`, or `Ctrl+Shift+R` on Windows).

Then save the project's history to GitHub so the repository always matches the live site:

```bash
git init
git add -A
git commit -m "First deploy"
gh repo create personalwebsite-<name> --source=. --public --push
```

> **Note:** The preview step is for testing and deploy is for shipping. Deploying a half-finished change publishes it to everyone.

---

← Back to [lesson](../README.md)
