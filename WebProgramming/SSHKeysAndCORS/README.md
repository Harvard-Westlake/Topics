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
2. [Keys: making a pair, logging in without sending a secret, and where each file lives](#keys)
3. [CORS: why the browser blocks an answer, with a working example to load](#cors)

## <font color="#388bfd">SSH</font>

### <font color="#79c0ff">A secret tunnel</font> <sub>[technical](assets/ssh-protocol-technical.svg)</sub>

![Animated diagram of SSH in plain words. Your computer and a far-away computer are joined by a secret tunnel that passes three computers on the way. You type ls, and it travels through the tunnel as a locked box showing only question marks. The far-away computer runs ls and sends the answer back the same way, and README.md appears on your computer. A note on a computer on the way says it can see the address on the box and cannot see what you typed. Below, one locked box is drawn in three parts: the address, which computer it is for; the door number, which program gets it; and, locked inside, what you typed. Anyone passing the box along can read the first two, and only your computer and the far-away one can open the third. A caption says SSH lets you use a far-away computer as if you were sitting at it, and nobody in between can listen in.](assets/ssh-protocol-eli5.svg)

**SSH** is a terminal that runs on another computer. You type here, and the commands run there.

```bash
ssh username@server-address
```

- **Everything is encrypted, the login included.** The computers in between pass your data along and cannot read it.
- **The fingerprint question** appears the first time you connect. Answering yes saves it. A later warning that it changed means stop and ask.
- **`exit`** closes the session and puts you back on your own computer.

### <font color="#79c0ff">One session, step by step</font>

![Animated diagram of one SSH session between your terminal and a server on port 22, in six steps. Step 1: your terminal connects to port 22. Step 2: the server sends its fingerprint, so you know it is really the server. Step 3: both sides agree on a secret code for this one session. From there an encrypted tunnel covers the rest: step 4, logging in with a password or a key, step 5, a command you type, ls, and step 6, what the server prints back. A router in between sees only scrambled bytes for steps 4 to 6. A caption says that the first time you connect, ssh shows the fingerprint and asks whether you trust it, and warns you if it ever changes.](assets/ssh-session.svg)

## <font color="#388bfd">Keys</font>

### <font color="#79c0ff">Making a key pair</font> <sub>[technical](assets/key-generation-technical.svg)</sub>

![Animated diagram of making a key pair, all on one laptop that belongs to one person, Maya. In a terminal on her laptop she types the command ssh-keygen and presses Enter. Underneath, the terminal says it is rolling a giant random number and shows the number, so big that nobody could ever guess it, then says it made 2 key files from it. The number travels into a folder on the same laptop and becomes two outlined key files: the private key, the secret half that never leaves this laptop, and the public key, the half she hands out and that is safe for anyone to see. They are a matching pair, and each one only works with the other. Nothing is sent anywhere.](assets/key-generation-eli5.svg)

A **key pair** is a lock and the one key that opens it. Hand out copies of the lock to anyone. Keep the key. One command makes both halves:

```bash
ssh-keygen -t ed25519
```

### <font color="#79c0ff">Logging in with a key</font> <sub>[technical](assets/key-login-technical.svg)</sub>

![Animated diagram of three people trying to log in to a server that keeps a folder of allowed keys holding key files for maya, noor, and kai. First, Dev knocks and shows his key. He has a key pair, but his key was never put in the folder, so the server says no entry. Second, Maya knocks and shows her key. It is in the folder, so the server asks her to prove the key is hers. She sends proof stamped with her secret key, the proof fits her key in the folder, and the server lets her in. Third, Sam knocks with no key files at all, and the server says no key, no entry. A caption says Maya never showed her secret key, only proof that she has it, and the proof works one time.](assets/key-login-eli5.svg)

| | Password | Key pair |
|---|---|---|
| **What you send to log in** | The secret itself | A signature that works once |
| **If someone copies what was sent** | They can log in as you | They get nothing they can reuse |
| **What to protect** | The password, everywhere it was ever typed | One file, on your own computer |

> **Warning:** A private key never leaves your computer. A public key can go anywhere.

### <font color="#79c0ff">Where each file lives</font> <sub>[technical](assets/key-files-access-technical.svg)</sub>

![Animated diagram of the files behind a key login, in plain words. On your computer, the .ssh folder holds four files: an address book with the server's nickname, its address, and your login; the secret key, which stamps your proof and never leaves this folder; the public key, the copy you hand out; and servers you trust, which remembers what the real server looks like. On the server, a file of allowed keys has one line for each person allowed in, with yours among them. Five steps light up in order: once, a copy of your public key is added to the server's list; you type ssh box and your address book fills in where to go and who you are; your secret key stamps a proof and only the proof travels; the server finds your line, checks the proof against it, and lets you in with no password; and your computer remembers this server, so a fake one would be noticed next time.](assets/key-files-access-eli5.svg)

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

### <font color="#79c0ff">The browser's check</font> <sub>[technical](assets/cors-check-technical.svg)</sub>

![Animated diagram of CORS in plain words. Your page, from my-site, sits inside your browser, and your browser acts as a guard. The page asks another website: can I have the scores? The first time, the other website answers with the scores but forgot the permission note, so the guard keeps the answer and the page gets nothing. The second time, the other website answers with the scores and a note saying pages from my-site may read this, so the guard hands the scores to the page. A caption says the other website answered both times, the guard is your own browser, and only the other website can add the note.](assets/cors-check-eli5.svg)

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
