<div align="center">

# The Network Stack
*<font color="#8b949e">The network stack is the set of layers every message passes through to cross the internet, each one adding its own wrapper and doing one job.</font>*

</div>

---

![Animated diagram of one web request being wrapped by four layers. Application, layer 4, says what to say: the HTTP message GET /index.html. Transport, layer 3, adds a TCP header with port 443 and piece 1 of 3: which program, and did it all arrive. Internet, layer 2, adds an IP header addressed to 199.36.158.100: which computer, anywhere on Earth. Link, layer 1, adds a frame header addressed to the next hop only. A caption says wrappers go on from top to bottom on the way out and come off in reverse on arrival, and that a router opens only the frame and the IP header and never reads your message.](assets/packet-layers.svg)

Your website does not travel as one thing. It is cut into small pieces, and every piece finds its own way.

- **Packets and layers:** a message is cut into packets, and four layers each wrap it once. Two layers give you a choice: TCP or UDP, HTTP or WebSocket.
- **The machines in between:** name servers turn a name into an address, routers pass packets hop by hop, and data centers hold the computers that answer.
- **SSH and keys:** a terminal on a far-away computer through an encrypted tunnel, and a way to prove who you are without sending a secret.
- **CORS and headers:** short lines at the top of every message that decide whether a browser will accept the answer at all.

## <font color="#388bfd">Table of Contents</font>

1. [Packets and the four layers, with TCP against UDP and HTTP against WebSocket](#packets-and-the-four-layers)
2. [The machines in between: name servers, routers, and data centers](#the-machines-in-between)
3. [SSH and keys: a terminal on another computer, and logging in without sending a secret](#ssh-and-keys)
4. [CORS and the headers every website needs to work](#cors-and-headers)

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
| `22` | SSH, a terminal on a far-away computer |
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
5. Find a line of `* * *` if you have one. That router passed your packets along but refused to answer the question.
6. Run `traceroute` again for a site in another country, such as `www.bbc.co.uk`. Compare the number of hops and the times.

> **Note:** In WSL, if `traceroute` is not found, install it with `sudo apt install traceroute`. On a school network many hops may show `* * *`: the packets still got through.

*(Standalone file: [activities/02-look-up-a-name-and-follow-the-hops.md](activities/02-look-up-a-name-and-follow-the-hops.md))*

</details>

## <font color="#388bfd">SSH and Keys</font>

So far the browser did the talking. To work on a server yourself, you need your own terminal on it.

### <font color="#79c0ff">SSH</font>

![Animated diagram of one SSH session between your terminal and a server on port 22, in six steps. Step 1: your terminal connects to port 22. Step 2: the server sends its fingerprint, so you know it is really the server. Step 3: both sides agree on a secret code for this one session. From there an encrypted tunnel covers the rest: step 4, logging in with a password or a key, step 5, a command you type, ls, and step 6, what the server prints back. A router in between sees only scrambled bytes for steps 4 to 6. A caption says that the first time you connect, ssh shows the fingerprint and asks whether you trust it, and warns you if it ever changes.](assets/ssh-session.svg)

**SSH** is a terminal that runs on another computer. You type here, and the commands run there.

```bash
ssh username@server-address
```

- **Everything is encrypted, the login included.** The routers in between carry your packets and cannot read them.
- **The fingerprint question** appears the first time you connect. Answering yes saves it. A warning that it changed means you may be talking to a different computer: stop and ask.
- **`exit`** closes the session and puts you back on your own computer.

### <font color="#79c0ff">Keys</font>

![Animated diagram of logging in with a key pair. Your laptop holds a public key, in the file id_ed25519.pub, that is safe to hand to anyone, and a private key, in the file id_ed25519, that never leaves the computer. Once, at setup, a copy of the public key travels to the server's authorized_keys file. To log in, the server asks the laptop to prove itself by signing the number 48151. The laptop signs it with the private key, and only the signature travels to the server. The server sees that the signature fits the public key and lets you in, and no secret was sent. A caption says a password is different because it has to be sent, so it can be shared, guessed, or leaked, and that GitHub already holds the public half of the SSH key made on setup day.](assets/key-pair.svg)

A **key pair** is a lock and the one key that opens it. Hand out copies of the lock to anyone. Keep the key.

| | Password | Key pair |
|---|---|---|
| **What you send to log in** | The secret itself | A signature that works once |
| **If someone copies what was sent** | They can log in as you | They get nothing they can reuse |
| **What to protect** | The password, everywhere it was ever typed | One file, the private key, on your own computer |

> **Warning:** A private key or a password never goes in a repository, a prompt, a screenshot, or a message. A public key can go anywhere.

## <font color="#388bfd">CORS and Headers</font>

![Animated diagram of CORS. A page from my-site.web.app, inside your browser, asks a service at a different origin for scores, and the browser adds the header Origin: https://my-site.web.app. Before the fix, the service answers 200 OK with no Access-Control-Allow-Origin header, and the browser's check stops the answer: the page gets an error and no data. After the fix, the service answers 200 OK with Access-Control-Allow-Origin: https://my-site.web.app, and the browser hands the scores to the page. A caption says the service answered both times, that CORS is the browser deciding whether your page may read the answer, and that an origin is scheme plus host plus port.](assets/cors-check.svg)

A page may always talk to the place it came from. To read an answer from anywhere else, that other server has to say your page is allowed. That permission slip is **CORS**, and it is one header.

- **An origin** is scheme + host + port: `https://my-site.web.app`. Change any one and it is a different origin.
- **The browser is the guard.** The service answers either way. The browser decides whether your page may read it.
- **The preflight:** before a request that changes data or sends JSON, the browser first sends an `OPTIONS` request to ask permission. The service has to answer that one too.

The headers and flags that decide whether a site works:

| Header or flag | Sent by | What it decides |
|---|---|---|
| `Access-Control-Allow-Origin` | The service | Which origins' pages may read this answer. `*` means any. |
| `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers` | The service, answering the preflight | Which actions (`GET`, `POST`) and which request headers are allowed. |
| `Content-Type` | Both sides | What the body is: `text/html`, `application/json`. The wrong type and the browser refuses to use it. |
| `Cache-Control` | The server | How long the browser may reuse its saved copy instead of asking again. |
| `Strict-Transport-Security` | The server | From now on, reach this site by HTTPS only. |
| `Set-Cookie` with `Secure`, `HttpOnly`, `SameSite` | The server | The cookie travels only over HTTPS, JavaScript cannot read it, and other sites' requests do not carry it. |

> **Warning:** A page loaded over `https://` may only call services that are also `https://` (or `wss://` for a WebSocket). The browser blocks a call to plain `http://` before it is ever sent.

### <font color="#79c0ff">Activity 3</font>
<details>
<summary><strong>Get Blocked by CORS on Purpose</strong></summary>

*Concept: Make your own page ask two other sites for data, and find the one header that explains why only one of them works.*

![A browser console on your own site. A fetch to example.com fails with a red error: blocked by CORS policy, no Access-Control-Allow-Origin header is present. A fetch to api.github.com/zen succeeds and prints a line of text. A caption explains that GitHub's server sent access-control-allow-origin with a star, meaning any origin may read the answer, and example.com sent no such header.](assets/cors-two-fetches.svg)

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

*(Standalone file: [activities/03-get-blocked-by-cors-on-purpose.md](activities/03-get-blocked-by-cors-on-purpose.md))*

</details>

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Name the four layers and what each wrapper adds, and pick TCP or UDP and HTTP or WebSocket for an app.
- [ ] Trace a request from a typed name to a data center and back, and explain why a browser blocks an answer that has no CORS header.
- [ ] Say what SSH hides from the routers in between, and why a private key never leaves your computer.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Find a site whose Protocol column in the Network tab reads `h3`, and work out which transport it rides on and why that is a surprise.

---

[Assignment](ASSIGNMENT.md)

← [User Flow and Logging](../UserFlowAndLogging/) | Next: [The Learning Widget Project](../LearningWidget/)
