<div align="center">

# The Network Stack
*<font color="#8b949e">The network stack is the set of layers every message passes through to cross the internet, each one adding its own wrapper and doing one job.</font>*

</div>

---

![Animated diagram of one web request being wrapped by four layers. Application, layer 4, says what to say: the HTTP message GET /index.html. Transport, layer 3, adds a TCP header with port 443 and piece 1 of 3: which program, and did it all arrive. Internet, layer 2, adds an IP header addressed to 199.36.158.100: which computer, anywhere on Earth. Link, layer 1, adds a frame header addressed to the next hop only. A caption says wrappers go on from top to bottom on the way out and come off in reverse on arrival, and that a router opens only the frame and the IP header and never reads your message.](assets/packet-layers.svg)

Your website does not travel as one thing. It is cut into small pieces, and every piece finds its own way.

- **Packets and layers:** a message is cut into packets, and four layers each wrap it once. Two layers give you a choice: TCP or UDP, HTTP or WebSocket.
- **The machines in between:** name servers turn a name into an address, routers pass packets hop by hop, and data centers hold the computers that answer.

## <font color="#388bfd">Table of Contents</font>

1. [Packets and the four layers, with TCP against UDP and HTTP against WebSocket](#packets-and-the-four-layers)
2. [The machines in between: name servers, routers, and data centers](#the-machines-in-between)

## <font color="#388bfd">Packets and the Four Layers</font>

Mailing a whole book is hard. Mailing it one numbered postcard at a time is easy: each postcard is small, each can take a different truck, and the reader puts them back in order. A **packet** is one postcard.

Each layer writes on the outside of the postcard and never reads what the other layers wrote.

| Layer | Its one job | Its wrapper adds | You have met it as |
|---|---|---|---|
| **4. Application** | What to say | The message itself | HTTP, WebSocket, DNS |
| **3. Transport** | Which program gets it, and whether it all arrived | A **port** and a piece number | TCP, UDP |
| **2. Internet** | Which computer, anywhere on Earth | An **IP address** | IP, such as `199.36.158.100` |
| **1. Link** | Reaching the very next device | The next hop's hardware address | Wi-Fi, Ethernet, fiber |

### <font color="#79c0ff">Transport: TCP and UDP</font>

![Animated comparison of TCP and UDP, each sending three pieces of data and each losing piece 2. TCP, a phone call: a three-step hello of SYN, SYN-ACK, and ACK, then pieces 1, 2, and 3, then the server reports it has 1 and still needs 2, piece 2 is sent again, and the server confirms it has all 3. Everything arrives complete and in order, at the cost of extra trips and waiting, which suits web pages, files, and logins. UDP, postcards: pieces 1, 2, and 3 are sent with no hello, piece 2 is lost, and the sender is done already without ever learning it. Pieces 1 and 3 arrive with a gap but nothing ever waits, which suits video calls, games, and live audio.](assets/tcp-vs-udp.svg)

A **port** is a numbered door on one computer, so many programs can share one address.

| Port | Who answers there |
|---|---|
| `80` | HTTP, a website with no encryption |
| `443` | HTTPS, a website with encryption |
| `22` | [SSH](../SSHKeysAndCORS/), a terminal on a far-away computer |
| `53` | DNS, the name servers |

### <font color="#79c0ff">Application: HTTP and WebSocket</font>

![Animated comparison of HTTP and WebSocket, both carried inside TCP. HTTP, one question and one answer: the browser sends GET /scores and receives 200 OK with the scores, then nothing happens until the browser asks again, and it must keep asking to learn whether anything is new. WebSocket, an open line: the browser sends one GET with Upgrade: websocket, the server answers 101 Switching Protocols, the connection stays open, and from then on the server sends new score and player joined while the browser sends my move, each at any time. HTTP suits pages, images, forms, and saving data. WebSocket suits chat, multiplayer games, and live scores.](assets/http-vs-websocket.svg)

An HTTP message is plain text: one first line, then **headers**, then a blank line, then the body.

```text
GET /scores HTTP/1.1                 the request: a method and a path
Host: my-site.web.app                a header
Accept: application/json             a header

HTTP/1.1 200 OK                      the response: a status code
Content-Type: application/json       a header
Cache-Control: max-age=600           a header

{ "maya": 12, "dev": 9 }             the body
```

**HTTPS** is the same HTTP inside one more wrapper that encrypts it, so nobody between you and the server can read or change it.

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Read One Request by Layer</strong></summary>

*Concept: Catch your own website being delivered and point at the part of the request that each layer handled.*

![One row of the browser's Network tab for index.html. Status 200 and protocol h2 are marked as the application layer: HTTP said OK, and which version of HTTP was spoken. Port 443 is marked as the transport layer: which program on that computer gets the data. The address 199.36.158.100 is marked as the internet layer: which computer the packets were sent to. The link layer is not in the tab at all: your Wi-Fi carried every packet to the first router.](assets/network-tab-layers.svg)

## Task

1. Open your own live website in your browser, open DevTools, and select the **Network** tab.
2. Right-click any column heading in the Network tab and turn on **Protocol** and **Remote Address**.
3. Reload the page. Every row that appears is one request.
4. Click the first row, the page itself. Write down its **Status**, its **Protocol**, and its **Remote Address**.
5. Split the Remote Address at the colon. Say which half is the internet layer and which half is the transport layer.
6. Count the rows. That is how many separate questions your browser asked to draw one page.

*(Standalone file: [activities/01-read-one-request-by-layer.md](activities/01-read-one-request-by-layer.md))*

</details>

## <font color="#388bfd">The Machines In Between</font>

Three kinds of machine sit between your browser and the answer. None of them is in charge of the whole trip.

### <font color="#79c0ff">Name servers</font>

![Animated diagram of a DNS lookup for my-site.web.app. Step 1: the browser asks a resolver, run by your internet provider or a public one such as 8.8.8.8, which does the asking for you. Step 2: the resolver asks a root name server, which knows who runs every ending and says to ask the .app servers. Step 3: the .app name server says to ask web.app's name server. Step 4: web.app's name server, which holds the real records, answers 199.36.158.100. Step 5: the resolver hands that address back to the browser. A caption says the resolver remembers the answer for a while, so the next lookup skips steps 2 to 4, and that a DNS question usually travels by UDP.](assets/dns-lookup.svg)

Packets need a number, and people type names. **DNS** is the phone book, split across many **name servers** so that no single one has to know everything.

### <font color="#79c0ff">Routers</font>

![Animated diagram of routers. A laptop at 192.168.1.20 sends packet 1 through its Wi-Fi router, its internet provider's router, and two more routers to a server at 199.36.158.100. Then the link between two of the routers goes down. Packet 2 leaves afterward, and the router next to the break sends it another way, through a different router, and it still arrives. A caption says no router knows the whole route and no one has to plan it, which is why the internet survives broken links.](assets/router-hops.svg)

A **router** is a mail sorter. It reads the destination address, picks the best next hop, and forgets the packet.

### <font color="#79c0ff">Data centers</font>

![Animated diagram of three sizes of data center. An edge location is a few racks in or near your city that keeps copies of files, and Firebase Hosting serves your HTML from one. A data center is one building with thousands of servers. A region is several data centers linked together: it runs services and holds the databases, your Firestore data lives in one region, and if one building fails the others carry on. A green dot shows loading the page: a short trip to the edge and back, a few milliseconds. An orange dot shows saving a score: a long trip through the edge to the database in the region and back, often 50 to 150 milliseconds.](assets/data-center-tiers.svg)

The computers that answer live in **data centers**, and the size decides the distance: small ones are close and hold copies, big ones are far and hold the real data.

One building is also rated by how much can break before it goes dark:

| Rating | What is built in | Time offline in a year |
|---|---|---|
| **Tier I** | One path for power and cooling, no spares | About 29 hours |
| **Tier II** | Spare parts for power and cooling | About 22 hours |
| **Tier III** | Any part can be repaired while everything stays on | About 1.6 hours |
| **Tier IV** | Two of everything, so any single failure changes nothing | About 26 minutes |

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Look Up a Name and Follow the Hops</strong></summary>

*Concept: Ask a name server for your site's address yourself, then list every router between you and it.*

![A terminal showing two commands. nslookup web.app answers with the address 199.36.158.100. traceroute web.app then lists five hops, one per line: the Wi-Fi router, the internet provider, a router that refuses to answer and shows three stars, a big network between providers, and finally the server at 199.36.158.100, the same address the lookup returned.](assets/lookup-and-trace.svg)

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
5. Find a line of `* * *` if you have one. That router passed your packets along but refused to answer the question. A school network may show many.
6. Run `traceroute` again for a site in another country, such as `www.bbc.co.uk`. Compare the number of hops and the times.

> **Note:** In WSL, `sudo apt install traceroute` adds the command if it is missing.

*(Standalone file: [activities/02-look-up-a-name-and-follow-the-hops.md](activities/02-look-up-a-name-and-follow-the-hops.md))*

</details>

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Name the four layers in order and say what each one's wrapper adds to a packet.
- [ ] Pick TCP or UDP, and HTTP or WebSocket, for an app, and say what each choice costs.
- [ ] Trace a request from a typed name, through name servers and routers, to a data center and back.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Find a site whose Protocol column in the Network tab reads `h3`, and work out which transport it rides on and why that is a surprise.

---

[Assignment](ASSIGNMENT.md)

← [SSH, Keys, and CORS](../SSHKeysAndCORS/) | Next: [The Learning Widget Project](../LearningWidget/)
