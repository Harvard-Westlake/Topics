<div align="center">

# SSH, Keys, and CORS
*<font color="#8b949e">SSH is a terminal on a computer somewhere else, a key pair proves who you are without sending a secret, and CORS is the browser's check on who may read a server's answer.</font>*

</div>

---

Your website has lived on someone else's computers. Today you get onto a server yourself.

- **SSH:** your terminal, running on a far-away computer, through an encrypted tunnel.
- **Keys:** two matching files that log you in without a password ever being sent.
- **CORS:** the one header that decides whether your page may read what a server answers.

## <font color="#388bfd">Table of Contents</font>

1. [SSH: a terminal on another computer, and what the tunnel hides](#ssh)
2. [Keys: logging in without sending a secret, and where each file lives](#keys)
3. [CORS: why the browser blocks an answer, with a working example to load](#cors)

## <font color="#388bfd">SSH</font>

![Animated diagram of one SSH session between your terminal and a server on port 22, in six steps. Step 1: your terminal connects to port 22. Step 2: the server sends its fingerprint, so you know it is really the server. Step 3: both sides agree on a secret code for this one session. From there an encrypted tunnel covers the rest: step 4, logging in with a password or a key, step 5, a command you type, ls, and step 6, what the server prints back. A router in between sees only scrambled bytes for steps 4 to 6. A caption says that the first time you connect, ssh shows the fingerprint and asks whether you trust it, and warns you if it ever changes.](assets/ssh-session.svg)

**SSH** is a terminal that runs on another computer. You type here, and the commands run there.

```bash
ssh username@server-address
```

- **Everything is encrypted, the login included.** The computers in between pass your data along and cannot read it.
- **The fingerprint question** appears the first time you connect. Answering yes saves it. A later warning that it changed means stop and ask.
- **`exit`** closes the session and puts you back on your own computer.

## <font color="#388bfd">Keys</font>

![Animated diagram of logging in with a key pair. Your laptop holds a public key, in the file id_ed25519.pub, that is safe to hand to anyone, and a private key, in the file id_ed25519, that never leaves the computer. Once, at setup, a copy of the public key travels to the server's authorized_keys file. To log in, the server asks the laptop to prove itself by signing the number 48151. The laptop signs it with the private key, and only the signature travels to the server. The server sees that the signature fits the public key and lets you in, and no secret was sent. A caption says a password is different because it has to be sent, so it can be shared, guessed, or leaked, and that GitHub already holds the public half of the SSH key made on setup day.](assets/key-pair.svg)

A **key pair** is a lock and the one key that opens it. Hand out copies of the lock to anyone. Keep the key.

| | Password | Key pair |
|---|---|---|
| **What you send to log in** | The secret itself | A signature that works once |
| **If someone copies what was sent** | They can log in as you | They get nothing they can reuse |
| **What to protect** | The password, everywhere it was ever typed | One file, on your own computer |

> **Warning:** A private key never leaves your computer. A public key can go anywhere.

### <font color="#79c0ff">Where each file lives</font>

Every piece is a plain text file in a folder named `.ssh`.

| File | On | What it is |
|---|---|---|
| `~/.ssh/id_ed25519` | Your computer | The private key. |
| `~/.ssh/id_ed25519.pub` | Your computer | The public key: one line of text. |
| `~/.ssh/authorized_keys` | The server | The public keys allowed to log in, one per line. |
| `~/.ssh/known_hosts` | Your computer | Fingerprints of servers you said yes to. |
| `~/.ssh/config` | Your computer | A nickname for each server: its address, your username, and which key to use. |

Installing a key means adding your public line to the server's `authorized_keys`. A `config` entry then turns a long command into a short one:

```text
Host box
  HostName server-address
  User username
  IdentityFile ~/.ssh/id_ed25519
```

With that entry, `ssh box` is the whole command. An **alias** in `~/.zshrc` (Mac) or `~/.bashrc` (WSL) makes it one word:

```bash
alias box="ssh box"
```

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Find Both Halves of Your Key</strong></summary>

*Concept: Look at the key pair already on your computer, and prove it works by logging in to GitHub with no password.*

![A terminal on your own computer. Listing the .ssh folder shows four files: id_ed25519, the private key that never leaves this computer, id_ed25519.pub, the public key that is safe to hand to anyone, known_hosts, the fingerprints of servers you said yes to, and config, nicknames for the servers you log in to. Printing id_ed25519.pub shows one line of text: the kind of key, the key itself, and a label.](assets/key-files.svg)

## Task

1. In your terminal, on your own computer, list your key folder:
   ```bash
   ls -1 ~/.ssh
   ```
2. Find the two files with the same name. Say which is the private half and which is the public half.
3. In your terminal, print the public half. It is one long line:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
4. Do not print the other file. Say out loud why not.
5. In your terminal, prove the pair works. GitHub has held your public half since setup day:
   ```bash
   ssh -T git@github.com
   ```
6. GitHub greeted you by name and never asked for a password. Say what your computer sent instead.

*(Standalone file: [activities/01-find-both-halves-of-your-key.md](activities/01-find-both-halves-of-your-key.md))*

</details>

## <font color="#388bfd">CORS</font>

![Animated diagram of CORS. A page from my-site.web.app, inside your browser, asks a service at a different origin for scores, and the browser adds the header Origin: https://my-site.web.app. Before the fix, the service answers 200 OK with no Access-Control-Allow-Origin header, and the browser's check stops the answer: the page gets an error and no data. After the fix, the service answers 200 OK with Access-Control-Allow-Origin: https://my-site.web.app, and the browser hands the scores to the page. A caption says the service answered both times, that CORS is the browser deciding whether your page may read the answer, and that an origin is scheme plus host plus port.](assets/cors-check.svg)

Every request and every answer on the web starts with short labeled lines called **headers**. A page may always talk to the place it came from. To read an answer from anywhere else, that other server has to send a header saying your page is allowed. That permission slip is **CORS**.

- **An origin** is scheme + host + port: `https://my-site.web.app`. Change any one and it is a different origin.
- **The browser is the guard.** The server answers either way. The browser decides whether your page may read it.
- **The preflight:** before a request that changes data or sends JSON, the browser first sends an `OPTIONS` request to ask permission.

| Header or flag | Sent by | What it decides |
|---|---|---|
| `Access-Control-Allow-Origin` | The server | Which origins' pages may read this answer. `*` means any. |
| `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers` | The server, answering the preflight | Which actions (`GET`, `POST`) and which request headers are allowed. |
| `Content-Type` | Both sides | What the body is: `text/html`, `application/json`. |
| `Cache-Control` | The server | How long the browser may reuse its saved copy. |
| `Strict-Transport-Security` | The server | From now on, reach this site by HTTPS only. |
| `Set-Cookie` with `Secure`, `HttpOnly`, `SameSite` | The server | HTTPS only, hidden from JavaScript, and not sent along by other sites. |

> **Warning:** An `https://` page may only call `https://` and `wss://` services.

### <font color="#79c0ff">A working example</font>

![A small badge that reads: this page has been loaded, followed by a number, and then the word times. The number is one higher every time anyone opens this lesson, because a service on the class server draws the picture fresh each time it is asked for.](https://theiss.api.codehw.net/badge.svg?page=ssh-keys-cors-lesson)

That number went up because you opened this page. This lesson lives at one origin, and the service that counted you lives at another.

| What | Where |
|---|---|
| The JSON the service answers with | <https://theiss.api.codehw.net/> |
| A page that gets the JSON, then updates live while other people load pages | <https://theiss.api.codehw.net/example> |
| The whole service, to read | <https://theiss.api.codehw.net/server.js> |

### <font color="#79c0ff">Activity 2</font>
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

*(Standalone file: [activities/02-get-blocked-by-cors-on-purpose.md](activities/02-get-blocked-by-cors-on-purpose.md))*

</details>

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Log in to another computer with SSH, and say what the computers in between can and cannot see.
- [ ] Say which half of a key pair goes on the server, which never leaves your computer, and why.
- [ ] Explain why a browser blocks an answer that has no CORS header, and who is doing the blocking.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Make a second key pair used only for the class server, and point your `config` entry at it.

---

[Assignment](ASSIGNMENT.md)

← [User Flow and Logging](../UserFlowAndLogging/) | Next: [The Network Stack](../NetworkStack/)
