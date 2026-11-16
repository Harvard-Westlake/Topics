# Assignment - The Network Stack

**Lesson:** [The Network Stack](README.md)  
**Due:** Before the start of next class

---

> **Warning:** CRITICAL. Never write the server's username or password anywhere except the login prompt in your own terminal. This page and your repository are public, and a login that appears in either one is a security vulnerability for every project on the server. That means never in your code, a commit, `prompts.md`, a prompt to your AI, a screenshot, or your Canvas submission. The login is given out in class only. If you think it has leaked, tell your teacher right away.

> **Note:** This assignment is a stencil. The server's address and login are handed out in class.

<!-- TODO(teacher): fill in the three parts below before this day is taught. Keep each part as WHAT must be true plus a way to verify it. NEVER put the shared username or password in this file or anywhere in this repo: it is public. -->

## Part 1: Log In to the Class Web Server

Your website so far has lived on someone else's computers. Today you get a terminal on a real web server that the whole class shares.

- **What must be true:** you are logged in to the class web server from your own terminal, over SSH, with the shared class login. You type the login yourself. Your AI never sees it.
- **Verify:** the server prints its own name and the class account's name when you ask it who and where you are.

<!-- TODO(teacher): server address only. The login is given in class, never written here. -->

---

## Part 2: Claim Your Namespace

Everyone logs in as the same user and everyone's services run on the same box, so each service needs a name, a folder, and a port that belong to one person only. The box holds a standards file for this: a Markdown file that everyone can read and nobody can edit. Read it yourself, then have your AI read it before it builds anything, and follow it exactly.

- **What must be true:** your service has its own name, its own folder, and its own port, each chosen the way the standards file says, and none of them collides with a classmate's. Nothing of yours touches a classmate's files or services.
- **Verify:** your entry appears where the standards file says every service is listed, and nobody else's entry uses your name or your port.

<!-- TODO(teacher): where the standards file lives on the box, the naming and port rules, where services are registered. -->

---

## Part 3: A Service Your Website Talks To

Build something small that runs on the box and answers your own website.

- **What must be true:** a service of yours runs on the class server and answers a request with JSON. Your live website asks it for that JSON and shows the answer on the page.
- **The headers are part of the work:** your website and your service are different origins, so the service's answer carries an `Access-Control-Allow-Origin` header that names your website's origin, and the right `Content-Type`.
- **Verify:** open your live website with DevTools on the **Network** tab. The request to your service shows status 200, the response headers show your origin, and the Console has no CORS error.

<!-- TODO(teacher): what the service should do, how it is started and kept running on the box, and whether the box serves HTTPS (an https:// page cannot call an http:// service). -->

---

## Success Criteria

- [ ] **Logged in:** you reached the class web server over SSH with the shared class login.
- [ ] **No login anywhere:** the username and password appear nowhere in your repository, `prompts.md`, screenshot, or submission.
- [ ] **Namespaced:** your service's name, folder, and port follow the standards file and collide with nobody's.
- [ ] **Connected:** your live website requests data from your service and shows the answer on the page.
- [ ] **Headers correct:** the service's answer names your website's origin in `Access-Control-Allow-Origin`, and the Console shows no CORS error.

---

## Submission

Submit **text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Live website link:                    
Service address (host, port, path):   
My namespace on the box:              
Access-Control-Allow-Origin value:    
TCP or UDP, and how I know:           
```

### Screenshot

Your live website with DevTools open on the **Network** tab, the request to your service selected, and its response headers visible. It must show status 200 and the `Access-Control-Allow-Origin` line. It must not show the server's username or password, or a terminal where either one is visible.
