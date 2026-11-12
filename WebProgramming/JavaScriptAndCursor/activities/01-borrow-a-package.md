# Activity - Borrow a Package

*Concept: Add code you did not write to your page with one script tag, then call it from the console.*

![Animated diagram of where a package comes from. On the left, the npm registry holds canvas-confetti 1.9.3 among two million packages. A CDN, jsDelivr, copies it to servers near every visitor. In the middle, your index.html tree gains one script tag whose src is the CDN address. On the right, the browser loads that file along with your own, and the function confetti() exists on your page: typing confetti() in the console fires confetti. A box glides from the registry through the CDN into the tree, and then confetti bursts on the page.](../assets/package-flow.svg)

## Task

1. In VS Code, open your site's `public/index.html` and add this tag inside `<head>`, above your own `<script>` tag, because your code can only call `confetti()` after the package has loaded:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
   ```
2. Save and open the page in your browser. Open the Console (`Cmd+Option+J` on Mac, `Ctrl+Shift+J` on Windows), type `confetti()` and press Return. Confetti falls. That function came from the package, not from you.
3. Type `confetti({ particleCount: 300, spread: 120 })`. Packages take options, and the package's page on [npmjs.com](https://www.npmjs.com/package/canvas-confetti) lists every one. Find one more option there and try it.
4. Open the Network panel and refresh. Find the row for `confetti.browser.min.js`: its address is the CDN, not your site. Click it and open **Response**. That is the code you borrowed, squeezed onto a few lines so it downloads fast. People read the source on npm or GitHub, never here.
