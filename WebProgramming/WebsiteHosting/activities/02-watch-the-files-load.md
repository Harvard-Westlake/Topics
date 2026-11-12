# Activity - Watch the Files Load

*Concept: Watch the browser fetch one file for the tree and one more for every file the tree points at, then remove one and see what survives.*

![Animated diagram of a small website loading. On the left, the folder tree: public/ holding index.html, style.css, a scripts/ folder with main.js and game.js, and game.html. In the middle, the document tree grows one node per tag as the browser reads index.html: html, head, title, link, script, body, h1, p, span. When the link and script nodes appear, dashed arrows fire from them to the Network panel on the right, which lists three requests in order: index.html, style.css, main.js. Below the Network panel a small page appears as plain black text, is painted blue when the CSS arrives, and its counter changes from 0 to 1 when the JavaScript runs.](../assets/files-loading.svg)

## Task

1. With `public/index.html` from Activity 1 open in your browser, open DevTools (**Inspect**) and click the **Network** tab. Refresh the page.
2. Count the rows: one for `index.html`, then one for each file its tree named, `style.css` and `main.js`. Click `style.css` and read the full address the browser used to fetch it.
3. In VS Code, rename `style.css` to `style-old.css`. Refresh the page. It still loads, with no styling, and the `style.css` row is red because the file was not found. The HTML is the only required file. Rename it back.
4. In the **Elements** panel, double-click the text of the first `<h1>`, type a new heading, and press Return. The page changes. Now refresh: the change is gone, because you edited the browser's tree, not the file on disk.
