<div align="center">

# Website Hosting
*<font color="#8b949e">A website starts as one HTML file, a tree of tags, and hosting puts that file on a server that is always on so anyone with the link can open it.</font>*

</div>

---

A website is just files, and the first one is always an HTML file:

- **One file:** a text file you can read in VS Code. The browser reads the same file and draws a page from it.
- **A tree:** the tags in that file nest inside each other, and the browser builds a tree out of them.
- **Hosting:** copying the files to a computer that never turns off, so anyone in the world can ask it for the page.

## <font color="#388bfd">Table of Contents</font>

1. [One file is a tree, and the tree points at other files](#one-file-one-tree)
2. [The three languages all act on that tree](#three-languages-one-tree)
3. [What happens when someone visits your site](#what-hosting-means)
4. [Setting up Firebase Hosting on your computer](#setting-up-firebase-hosting)
5. [The edit, preview, deploy loop](#the-deploy-loop)

## <font color="#388bfd">One File, One Tree</font>

In VS Code, open a new folder (**File → Open Folder**), create a file named `index.html`, and type (not paste) this:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>My First Page</title>
  </head>
  <body>
    <h1>Hello from VS Code</h1>
    <p>This page was written by hand.</p>
  </body>
</html>
```

Save it, then double-click `index.html` in Finder or File Explorer. It opens in your browser.

- **Same file, two views.** VS Code shows the text. The browser is a program that reads that same text and draws it. The address bar starts with `file://`, an address that only works on your computer.
- **Tags nest, so the file is a tree.** Every tag sits inside exactly one other tag. `html` splits into `head`, which holds facts about the page such as its title, and `body`, which holds what you see. The indentation is for you; the nesting is what the browser reads.
- **The tree is viewable two ways.** Right-click the page and choose **View Page Source** to see the file the browser received. Choose **Inspect** instead to open the **Elements** panel: the live tree the browser built. Hover a node and its box lights up on the page.

![Animated diagram of one HTML file seen three ways. On the left, index.html as text in VS Code. In the middle, the tree the browser builds from it: html splits into head and body, head holds title, body holds h1 and p. On the right, the page the browser draws, with a file:// address. A pointer hovers h1, then p, then title, and each time the same tag lights up in the text, in the tree, and as a box on the page (the title lights up in the browser tab, because head holds facts about the page rather than things you see).](../assets/document-tree.svg)

Change the heading in VS Code, **save**, and **refresh** the browser. This edit, save, refresh loop is the heartbeat of web development. If a change does not appear, you forgot to save or to refresh: check both before anything else.

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Find Both Trees</strong></summary>

*Concept: Download a real website and find its two trees: the folders around index.html, and the tags inside it.*

![Animated diagram of one HTML file seen three ways. On the left, index.html as text in VS Code. In the middle, the tree the browser builds from it: html splits into head and body, head holds title, body holds h1 and p. On the right, the page the browser draws, with a file:// address. A pointer hovers h1, then p, then title, and each time the same tag lights up in the text, in the tree, and as a box on the page (the title lights up in the browser tab, because head holds facts about the page rather than things you see).](../assets/document-tree.svg)

## Task

1. Open the [BasicStaticWebsite template](https://github.com/Harvard-Westlake/BasicStaticWebsite) on GitHub, click **Code → Download ZIP**, and unzip it.
2. Open the unzipped folder in VS Code (**File → Open Folder**) and expand `public/`. This is the folder tree: `index.html`, `game.html`, `style.css`, and a `scripts/` folder holding `main.js` and `game.js`.
3. Open `public/index.html` in VS Code. In `head`, find the `<link>` tag and the `<script>` tag and read the address each one holds. One points at `style.css` next to this file; the other walks into `scripts/`.
4. In Finder or File Explorer, double-click `public/index.html`. It opens in your browser, and the address bar starts with `file://`. Change the end of that address from `index.html` to `game.html` and press Return: the folder tree is the address tree.
5. Go back to `index.html`, right-click the page, and choose **Inspect**. In the **Elements** panel, expand `<body>` and hover each `<section>`. Its box lights up on the page: node equals box.
6. In VS Code, look at the last `<section>` in `index.html`. It never closes. In the Elements panel, find where the browser closed it for you. The browser does not display your text; it builds a tree from it and repairs what it must.

*(Standalone file: [activities/01-find-both-trees.md](../activities/01-find-both-trees.md))*

</details>

A real page is rarely one file, but it always starts with one:

- **The tree points at other files.** A `<link>` tag names a stylesheet, `<script>` names a JavaScript file, `<img>` names a picture, and `<a>` names another page to go to. Each one holds an address. The browser sends one request for the HTML, then one more for every file the tree names, and the **Network** panel in DevTools lists them in order. The HTML is the only required file.
- **Two trees.** The tags make a tree inside `index.html`. The folders make a second tree around it. An address like `scripts/main.js` is a walk down the folder tree starting from the file that named it, and `index.html` is the file a folder shows when an address names only the folder.

![Animated diagram of a small website loading. On the left, the folder tree: public/ holding index.html, style.css, a scripts/ folder with main.js and game.js, and game.html. In the middle, the document tree grows one node per tag as the browser reads index.html: html, head, title, link, script, body, h1, p, span. When the link and script nodes appear, dashed arrows fire from them to the Network panel on the right, which lists three requests in order: index.html, style.css, main.js. Below the Network panel a small page appears as plain black text, is painted blue when the CSS arrives, and its counter changes from 0 to 1 when the JavaScript runs.](../assets/files-loading.svg)

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Watch the Files Load</strong></summary>

*Concept: Watch the browser fetch one file for the tree and one more for every file the tree points at, then remove one and see what survives.*

![Animated diagram of a small website loading. On the left, the folder tree: public/ holding index.html, style.css, a scripts/ folder with main.js and game.js, and game.html. In the middle, the document tree grows one node per tag as the browser reads index.html: html, head, title, link, script, body, h1, p, span. When the link and script nodes appear, dashed arrows fire from them to the Network panel on the right, which lists three requests in order: index.html, style.css, main.js. Below the Network panel a small page appears as plain black text, is painted blue when the CSS arrives, and its counter changes from 0 to 1 when the JavaScript runs.](../assets/files-loading.svg)

## Task

1. With `public/index.html` from Activity 1 open in your browser, open DevTools (**Inspect**) and click the **Network** tab. Refresh the page.
2. Count the rows: one for `index.html`, then one for each file its tree named, `style.css` and `main.js`. Click `style.css` and read the full address the browser used to fetch it.
3. In VS Code, rename `style.css` to `style-old.css`. Refresh the page. It still loads, with no styling, and the `style.css` row is red because the file was not found. The HTML is the only required file. Rename it back.
4. In the **Elements** panel, double-click the text of the first `<h1>`, type a new heading, and press Return. The page changes. Now refresh: the change is gone, because you edited the browser's tree, not the file on disk.

*(Standalone file: [activities/02-watch-the-files-load.md](../activities/02-watch-the-files-load.md))*

</details>

## <font color="#388bfd">Three Languages, One Tree</font>

Every page you have ever visited is built from the same three ingredients, and all three work on the tree:

| Language | What it does | On the tree | In a building |
|---|---|---|---|
| **HTML** | The structure and the content: headings, paragraphs, images, links. | It is the tree. | The frame |
| **CSS** | The look: colors, fonts, spacing, layout. | A selector such as `h1` is an address into the tree, and the rule paints every node it finds. | The paint |
| **JavaScript** | The behavior: things that happen when you click, type, or wait. | Code that edits the tree while the page is open: adding, removing, and changing nodes. | The electricity |

Today is about HTML and CSS. JavaScript gets its own lesson next. Keep the references open as you work: [HTML](../../Docs/html.md), [CSS](../../Docs/css.md), [JavaScript](../../Docs/javascript.md).

## <font color="#388bfd">What Hosting Means</font>

![Animated: how a hosted website works. On the left, your laptop holds a public/ folder with index.html, styles.css, and script.js. In the middle, Firebase's servers, drawn as a cloud with a server rack inside, hold a copy and serve it at your-project-id.web.app. On the right, a phone, a classmate, and a laptop in Tokyo keep sending requests (GET /) to the servers, and each one gets back a copy of index.html, version 1. Then index.html on your laptop is saved as version 2, but the next visitor still gets version 1 because nothing was deployed. An HTML file labeled v2 then travels along the firebase deploy arrow to the servers, and from then on every visitor gets version 2.](../assets/hosting-layout.svg)

Your `index.html` works, but only on your machine. A `file://` address is a website for exactly one computer: your laptop sleeps, changes Wi-Fi, and has no address anyone else can type. A **server** is a computer that is always on, has a public address, and runs a program that answers requests with files. **Hosting** means putting your folder on one. When someone types your URL:

1. The name becomes a number. `learnhw.web.app` is looked up and turns into an IP address. In your terminal, `nslookup learnhw.web.app` shows that lookup happening.
2. Their browser asks the server at that number for the page. The padlock means the connection is encrypted with a certificate, which Firebase issues for free.
3. The server sends back the files: the HTML first, then the CSS and JavaScript the tree names.
4. The browser builds the tree and draws the page.

We use **Firebase Hosting**, a free Google service that gives every project two addresses named after its project ID: a project named `chocolateparty` gets `chocolateparty.web.app` and `chocolateparty.firebaseapp.com`. Deploying is a copy: your `public/` folder is uploaded to the server's folder, so the folder tree you see in VS Code becomes the address tree visitors walk, and `chocolateparty.web.app/` serves `public/index.html`. A site like this is **static**: the server hands every visitor the same bytes, unchanged. A site that remembers each visitor needs more than files, which is where databases come in later in this unit.

## <font color="#388bfd">Setting Up Firebase Hosting</font>

1. **Create a Firebase project.** At [console.firebase.google.com](https://console.firebase.google.com/), sign in with your **personal** Google account (not your school one) and create a project. The project name becomes your website's public address, `<unique-public-website-name>.web.app`, so pick something short and unique that anyone may see, such as `chocolateparty` for `chocolateparty.web.app`. Firebase may add a few characters to make the **project ID** unique; the project ID is what appears in your URL. You can turn off Google Analytics and Gemini for this project.
2. **Install the Firebase CLI.** The CLI (command-line interface) lets your terminal talk to Firebase. In your terminal (Mac or WSL):
   ```bash
   curl -sL https://firebase.tools | bash
   ```
3. **Log in.** In your terminal:
   ```bash
   firebase login
   ```
   A browser opens. Sign in with the same personal Google account and choose **Allow**.
4. **Initialize hosting.** Make a folder named after your project, open it in VS Code, and in its terminal run:
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
   <unique-public-website-name>/
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
   The output ends with your **Hosting URL**, for example `https://chocolateparty.web.app`.
4. **Verify** by opening that URL yourself. If you do not see the change, hard-refresh (`Cmd+Shift+R`, or `Ctrl+Shift+R` on Windows).

Then save the project's history to GitHub so the repository always matches the live site:

```bash
git init
git add -A
git commit -m "First deploy"
gh repo create <unique-public-website-name> --source=. --public --push
```

> **Note:** The preview step is for testing and deploy is for shipping. Deploying a half-finished change publishes it to everyone.

---

← Back to [lesson](../README.md)
