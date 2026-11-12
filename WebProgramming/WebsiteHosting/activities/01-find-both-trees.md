# Activity - Find Both Trees

*Concept: Download a real website and find its two trees: the folders around index.html, and the tags inside it.*

![Animated diagram of one HTML file seen three ways. On the left, index.html as text in VS Code. In the middle, the tree the browser builds from it: html splits into head and body, head holds title, body holds h1 and p. On the right, the page the browser draws, with a file:// address. A pointer hovers h1, then p, then title, and each time the same tag lights up in the text, in the tree, and as a box on the page (the title lights up in the browser tab, because head holds facts about the page rather than things you see).](../assets/document-tree.svg)

## Task

1. Open the [BasicStaticWebsite template](https://github.com/Harvard-Westlake/BasicStaticWebsite) on GitHub, click **Code → Download ZIP**, and unzip it.
2. Open the unzipped folder in VS Code (**File → Open Folder**) and expand `public/`. This is the folder tree: `index.html`, `game.html`, `style.css`, and a `scripts/` folder holding `main.js` and `game.js`.
3. Open `public/index.html` in VS Code. In `head`, find the `<link>` tag and the `<script>` tag and read the address each one holds. One points at `style.css` next to this file; the other walks into `scripts/`.
4. In Finder or File Explorer, double-click `public/index.html`. It opens in your browser, and the address bar starts with `file://`. Change the end of that address from `index.html` to `game.html` and press Return: the folder tree is the address tree.
5. Go back to `index.html`, right-click the page, and choose **Inspect**. In the **Elements** panel, expand `<body>` and hover each `<section>`. Its box lights up on the page: node equals box.
6. In VS Code, look at the last `<section>` in `index.html`. It never closes. In the Elements panel, find where the browser closed it for you. The browser does not display your text; it builds a tree from it and repairs what it must.
