# Activity - Look Up a Name and Follow the Hops

*Concept: Ask a name server for your site's address yourself, then list every router between you and it.*

![A terminal showing two commands. nslookup web.app answers with the address 199.36.158.100. traceroute web.app then lists five hops, one per line: the Wi-Fi router, the internet provider, a router that refuses to answer and shows three stars, a big network between providers, and finally the server at 199.36.158.100, the same address the lookup returned.](../assets/lookup-and-trace.svg)

## Task

1. In your terminal, ask a name server for the address of your own site, using your site's name in place of `my-site`:
   ```bash
   nslookup my-site.web.app
   ```
2. Write down the address it returns. Compare it with the Remote Address you found in Activity 1.
3. In your terminal, list the routers between you and that address:
   ```bash
   traceroute my-site.web.app
   ```
4. Count the hops. Name hop 1, and say how you know which hop is the last one.
5. Find a line of `* * *` if you have one. That router passed your packets along but refused to answer the question.
6. Run `traceroute` again for a site in another country, such as `www.bbc.co.uk`. Compare the number of hops and the times.

> **Note:** In WSL, if `traceroute` is not found, install it with `sudo apt install traceroute`. On a school network many hops may show `* * *`: the packets still got through.
