<div align="center">

# The Network Stack
*<font color="#8b949e">The network stack is the set of layers every message passes through to cross the internet, each one adding its own wrapper and doing one job.</font>*

</div>

---

![Animated diagram of one web request being wrapped by four layers. Application, layer 4, says what to say: the HTTP message GET /index.html. Transport, layer 3, adds a TCP header with port 443 and piece 1 of 3: which program, and did it all arrive. Internet, layer 2, adds an IP header addressed to 199.36.158.100: which computer, anywhere on Earth. Link, layer 1, adds a frame header addressed to the next hop only. A caption says wrappers go on from top to bottom on the way out and come off in reverse on arrival, and that a router opens only the frame and the IP header and never reads your message.](../assets/packet-layers.svg)

Your website does not travel as one thing. It is cut into small pieces, and every piece finds its own way.

- **The four layers:** each layer wraps the message once and does one job.
- **One page over TCP:** the careful way, where every piece is numbered, checked, and sent again if it is lost.
- **The same page over UDP:** the fast way, where pieces are sent once and never checked.

## <font color="#388bfd">Table of Contents</font>

1. [The four layers every message is wrapped in](#the-four-layers)
2. [One page over TCP, stage by stage](#one-page-over-tcp)
3. [The same page over UDP, and why anyone would choose it](#the-same-page-over-udp)

## <font color="#388bfd">The Four Layers</font>

Mailing a whole book is hard. Mailing it one numbered postcard at a time is easy: each postcard is small, each can take a different truck, and the reader puts them back in order. A **packet** is one postcard.

Each layer writes on the outside of the postcard and never reads what the other layers wrote.

| Layer | Its one job | Its wrapper adds | You have met it as |
|---|---|---|---|
| **4. Application** | What to say | The message itself | HTTP, WebSocket, DNS |
| **3. Transport** | Which program gets it, and whether it all arrived | A **port** and a piece number | TCP, UDP |
| **2. Internet** | Which computer, anywhere on Earth | An **IP address** | IP, such as `199.36.158.100` |
| **1. Link** | Reaching the very next device | The next hop's hardware address | Wi-Fi, Ethernet, fiber |

- **TCP and UDP** are the two ways the transport layer can carry the postcards. The next two sections follow one page through each.
- **HTTP and WebSocket** are two ways the application layer can talk, and both ride on TCP: HTTP asks once and gets one answer, and a WebSocket keeps the line open.

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Read One Request by Layer</strong></summary>

*Concept: Catch your own website being delivered and point at the part of the request that each layer handled.*

![One row of the browser's Network tab for index.html. Status 200 and protocol h2 are marked as the application layer: HTTP said OK, and which version of HTTP was spoken. Port 443 is marked as the transport layer: which program on that computer gets the data. The address 199.36.158.100 is marked as the internet layer: which computer the packets were sent to. The link layer is not in the tab at all: your Wi-Fi carried every packet to the first router.](../assets/network-tab-layers.svg)

## Task

1. Open your own live website in your browser, open DevTools, and select the **Network** tab.
2. Right-click any column heading in the Network tab and turn on **Protocol** and **Remote Address**.
3. Reload the page. Every row that appears is one request.
4. Click the first row, the page itself. Write down its **Status**, its **Protocol**, and its **Remote Address**.
5. Split the Remote Address at the colon. Say which half is the internet layer and which half is the transport layer.
6. Count the rows. That is how many separate questions your browser asked to draw one page.

*(Standalone file: [activities/01-read-one-request-by-layer.md](../activities/01-read-one-request-by-layer.md))*

</details>

## <font color="#388bfd">One Page Over TCP</font>

You type an address and a page appears. Here is everything that happens in between, one stage at a time.

1. ![Animation of TCP step 1 of 8, say hello first. The browser says: hello, can we talk? The web server answers: yes, I am listening. The browser says: good, here comes my question. Nothing else is sent until all three messages have crossed.](../assets/tcp-trip-step-1.svg)

   **Say hello first.** Before anything is sent, the two computers check that the other one is really there and listening, like saying hello on the phone before you start talking.

2. ![Animation of TCP step 2 of 8, ask for the page. One small message, GET /index.html, travels from the browser to the web server, and the server finds the file index.html.](../assets/tcp-trip-step-2.svg)

   **Ask for the page.** Your browser sends one short note: please give me `index.html`. The server finds that file.

3. ![Animation of TCP step 3 of 8, cut the page into chunks, inside the server. The file index.html is too big to send as one piece, so it is cut at three places and the four pieces move apart: the opening html tag, a heading that says Hi, a paragraph, and the closing html tag. A label says 4 chunks, each small enough to travel.](../assets/tcp-trip-step-3.svg)

   **Cut the page into chunks.** The page is too big to send in one go, so the server cuts it into small pieces, like tearing a letter into postcards.

4. ![Animation of TCP step 4 of 8, number every chunk, inside the server. The four chunks get the numbers 1, 2, 3, and 4 one at a time, each labeled as 1 of 4 through 4 of 4, and then every chunk is addressed to your browser.](../assets/tcp-trip-step-4.svg)

   **Number every chunk.** Each postcard gets a number and your address, so they can be put back in order no matter how they arrive.

5. ![Animation of TCP step 5 of 8, send them over the wire. The four numbered chunks leave the web server and travel through routers along two different routes. Chunk 2 arrives first, then chunk 1, then chunk 4. Chunk 3 disappears at a router and never arrives.](../assets/tcp-trip-step-5.svg)

   **Send them over the wire.** Every chunk travels on its own. They take different roads, show up in a different order, and sometimes one gets lost.

6. ![Animation of TCP step 6 of 8, put them back in order, inside your browser. The chunks arrived as 2, 1, 4. Each one moves into the slot that matches its number, leaving the third slot empty with a red question mark. The browser notes that chunk 3 is missing.](../assets/tcp-trip-step-6.svg)

   **Put them back in order.** Your computer lines the chunks up by number. Now it can see that number 3 is not there.

7. ![Animation of TCP step 7 of 8, ask again for the missing one. The browser tells the web server: I have 1, 2, and 4, please send 3 again. The server sends chunk 3 once more, it arrives, and the browser shows a green check: 1, 2, 3, 4, all here.](../assets/tcp-trip-step-7.svg)

   **Ask again for the missing one.** Your computer tells the server exactly what it has, and the server sends the missing chunk again. TCP keeps asking until every chunk is there.

8. ![Animation of TCP step 8 of 8, join the chunks into the page, inside your browser. The four numbered chunks slide together into one file, index.html, whole again and in the right order, and a small page that says Hi appears in the browser.](../assets/tcp-trip-step-8.svg)

   **Join the chunks into the page.** With every chunk in place, they are glued back together and the page appears, exactly as it was written.

## <font color="#388bfd">The Same Page Over UDP</font>

Now send the same page the other way. UDP does less work at every stage, and that is the whole point of it.

1. ![Animation of UDP step 1 of 5, no hello, just start. The browser says: send me the page. The web server answers at once: here it comes. A label says the three hello messages are skipped, so it starts sooner.](../assets/udp-trip-step-1.svg)

   **No hello: just start.** Nobody checks that the other side is listening. The server just starts sending, which is faster.

2. ![Animation of UDP step 2 of 5, cut into chunks with no numbers, inside the server. The page is cut into the same four chunks, but the circle where each number would go stays empty. A label says no numbers, and no list of what was sent.](../assets/udp-trip-step-2.svg)

   **Cut into chunks, with no numbers.** The page is cut up the same way, but the postcards get no numbers and nobody keeps a list of them.

3. ![Animation of UDP step 3 of 5, send them over the wire. The four unnumbered chunks travel through the same routers along two routes. The heading chunk arrives first, then the opening html tag, then the closing html tag. The paragraph chunk disappears at a router and never arrives.](../assets/udp-trip-step-3.svg)

   **Send them over the wire.** Same roads, same routers, same trouble: the chunks arrive in a different order and one gets lost.

4. ![Animation of UDP step 4 of 5, use them as they land, inside your browser. The three chunks that arrived are placed side by side in the order they came: the heading, then the opening html tag, then the closing html tag. A red label says wrong order, one chunk gone, and nobody asks for it again. The browser is left with a broken page.](../assets/udp-trip-step-4.svg)

   **Use them as they land.** With no numbers, the chunks are used in the order they showed up. The lost one is never asked for, so the page comes out broken. That is why web pages travel by TCP.

5. ![Animation of UDP step 5 of 5, so why does anyone use it, shown as a live video call sending one picture at a time. On the UDP row, pictures 1 and 2 arrive, the lost one is skipped, and pictures 4 and 5 arrive on time. On the TCP row, pictures 1 and 2 arrive, then the call freezes while it waits for the lost one, and pictures 3 and 4 arrive late. A caption says UDP has one tiny glitch and is still live, and TCP has every picture and is now behind.](../assets/udp-trip-step-5.svg)

   **So why does anyone use it?** In a video call or a fast game, a late picture is useless. UDP skips what was lost and stays live, while TCP would freeze and wait.

| | TCP | UDP |
|---|---|---|
| **Says hello first** | Yes | No |
| **Numbers the chunks** | Yes | No |
| **Sends a lost chunk again** | Yes | No |
| **Good for** | Web pages, files, logins: every piece must arrive | Video calls, live games: being on time matters more |

---

← Back to [lesson](../README.md)
