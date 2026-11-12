# Activity - Serve, Deploy, and the Refresh That Forgets

*Concept: Preview locally, publish, get past the cache, and watch a plain variable lose its value on every refresh.*

![Two ways to see your site. firebase serve runs it privately on your own laptop at localhost, stopped with Ctrl+C. firebase deploy copies the files to Firebase and updates your public URL, where a normal refresh may show a cached old copy until a hard refresh. Separately, a counter variable reads 5 before a refresh and resets to 0 after, because a refresh throws the page's memory away.](../assets/serve-deploy-cache.svg)

## Task

1. In your terminal, run `firebase serve` and open the `localhost` address it prints. This is your site on your own machine, private to you. Press `Ctrl+C` to stop it and get your prompt back.
2. Add the click counter from the lesson to `scripts/main.js`, then run `firebase deploy --only hosting` and open your live address. Click the button: the number climbs.
3. Change the button's text in the code, deploy again, and do a normal refresh. If you still see the old text, do a **hard refresh** (`Cmd+Shift+R` on Mac, `Ctrl+Shift+R` on Windows). The new text appears: the first refresh showed you the cache.
4. Click the counter up to 5, then refresh the page. It drops to 0. The page's memory is gone. Leave it broken; you fix it next.
