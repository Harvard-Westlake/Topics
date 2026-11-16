# Activity - Get Blocked by CORS on Purpose

*Concept: Make your own page ask two other sites for data, and find the one header that explains why only one of them works.*

![A browser console on your own site. A fetch to example.com fails with a red error: blocked by CORS policy, no Access-Control-Allow-Origin header is present. A fetch to api.github.com/zen succeeds and prints a line of text. A caption explains that GitHub's server sent access-control-allow-origin with a star, meaning any origin may read the answer, and example.com sent no such header.](../assets/cors-two-fetches.svg)

## Task

1. Open your own live website, open DevTools, and select the **Console** tab.
2. Paste this into the console and press Enter:
   ```javascript
   fetch("https://example.com").then((response) => response.text()).then(console.log);
   ```
3. Read the red error. Find the name of the header it says is missing.
4. Now paste this one:
   ```javascript
   fetch("https://api.github.com/zen").then((response) => response.text()).then(console.log);
   ```
5. Switch to the **Network** tab, click the `zen` row, and find `access-control-allow-origin` under Response Headers. Write down its value.
6. Find the `example.com` row. Its status reads **CORS error**, but the server did send an answer. Say who kept that answer away from your page.
