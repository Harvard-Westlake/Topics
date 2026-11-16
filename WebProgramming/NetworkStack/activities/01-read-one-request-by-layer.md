# Activity - Read One Request by Layer

*Concept: Catch your own website being delivered and point at the part of the request that each layer handled.*

![One row of the browser's Network tab for index.html. Status 200 and protocol h2 are marked as the application layer: HTTP said OK, and which version of HTTP was spoken. Port 443 is marked as the transport layer: which program on that computer gets the data. The address 199.36.158.100 is marked as the internet layer: which computer the packets were sent to. The link layer is not in the tab at all: your Wi-Fi carried every packet to the first router.](../assets/network-tab-layers.svg)

## Task

1. Open your own live website in your browser, open DevTools, and select the **Network** tab.
2. Right-click any column heading in the Network tab and turn on **Protocol** and **Remote Address**.
3. Reload the page. Every row that appears is one request.
4. Click the first row, the page itself. Write down its **Status**, its **Protocol**, and its **Remote Address**.
5. Split the Remote Address at the colon. Say which half is the internet layer and which half is the transport layer.
6. Count the rows. That is how many separate questions your browser asked to draw one page.
