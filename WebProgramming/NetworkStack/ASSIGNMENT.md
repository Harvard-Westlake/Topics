# Assignment - The Network Stack

**Lesson:** [The Network Stack](README.md)  
**Due:** Before the start of next class

---

> **Warning:** CRITICAL. Never write the server's username or password anywhere except the login prompt in your own terminal. This page and your repository are public, and a login that appears in either one is a security vulnerability for every project on the server. That means never in your code, a commit, `prompts.md`, a prompt to your AI, a screenshot, or your Canvas submission. The login is given out in class only. If you think it has leaked, tell your teacher right away.

![A small badge that reads: this page has been loaded, followed by a number, and then the word times. The number is one higher every time anyone opens this page, because the picture is drawn by the class example service each time it is asked for.](https://theiss.api.codehw.net/badge.svg)

That number went up because you opened this page. A small service on the class server counted you, and by the end of today you will have built one like it.

## Part 1: SSH Onto the Box and Get a Folder With Your Name on It

Your website so far has lived on someone else's computers. Today you get a terminal on a real web server that the whole class shares.

1. In your terminal, connect with the address and class login given in class. You type the login yourself. Your AI never sees it.
   ```bash
   ssh CLASS-LOGIN@SERVER-ADDRESS
   ```
2. The first time, `ssh` shows the server's fingerprint and asks whether you trust it. Check it against the one shown in class, then answer `yes`.
3. The server asks for **your first name**. Type it in lowercase. Use the same name every time you log in.

- **What must be true:** a folder with your name on it exists on the box, and your terminal is inside it.
- **Verify:** `pwd` ends in your name, and `myports` prints your name's address and the ports that belong to you.

> **Warning:** Logging in under someone else's name puts you inside their folder and their services. That is an Honor Code violation.

---

## Part 2: Read the Rules of the Box

Everyone shares one login and one computer, so your name is your namespace: your folder, your ten ports, and your own address on the internet. The rules that keep everyone's services apart are in `~/README.md`, a file everyone can read and nobody can edit.

- **What must be true:** you have read `~/README.md`, and your AI has read it before it writes or runs anything on the box.
- **Verify:** without looking, you can say which port your service must listen on, what your public address is, which command keeps a service running after you log out, and two things the proxy does so your code must not.

---

## Part 3: A Simple App Your Website Talks To

Build one small service in your own folder on the box, and make your live website talk to it.

- **The service:** it runs on the box, on your port, and answers a `GET` request at your address with a JSON object that holds the number of times it has been accessed. Ask twice and the number is higher the second time.
- **It stays up:** the service keeps answering after you log out.
- **The website:** your live website, the one you already host, asks your service for that JSON and shows the number on the page.
- **The headers:** your website and your service are different origins, so CORS applies. On this box the proxy in front of your service adds the CORS headers and the HTTPS for you. Adding your own breaks it.
- **The code is yours:** the project lives in your own GitHub repository as well as on the box, with nothing secret in it.

A working example, built by the same rules:

| What | Where |
|---|---|
| The JSON, counting every access | <https://theiss.api.codehw.net/> |
| A page that gets the JSON and shows the numbers | <https://theiss.api.codehw.net/example> |
| The whole service, to read | <https://theiss.api.codehw.net/server.js> |

**Verify:** open your live website with DevTools on the **Network** tab and reload. The request to your service shows status 200, its response headers include `access-control-allow-origin`, the number on your page is one higher than before the reload, and the Console has no errors. Then log out of the box and reload once more: it still works.

---

## Success Criteria

- [ ] **Logged in:** you reached the box over SSH and you are in the folder with your name on it.
- [ ] **No login anywhere:** the server's username and password appear nowhere in your repository, `prompts.md`, screenshot, or submission.
- [ ] **By the rules:** your service listens on your own port, was started the way `~/README.md` says, and touches nothing outside your folder.
- [ ] **Counts accesses:** your address answers with a JSON object whose number goes up with every request.
- [ ] **Connected:** your live website gets that JSON from your service and shows the number, with no errors in the Console.
- [ ] **Still up:** the service answers after you have logged out of the box.

---

## Submission

Submit **text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Live website link:                        
My service's address:                     
The JSON it returned:                     
Value of access-control-allow-origin:     
Who added that header, and why not me:    
GitHub repository for the service:        
```

### Screenshot

Your live website with DevTools open on the **Network** tab, the request to your service selected, and its response headers visible. It must show status 200 and the `access-control-allow-origin` line. It must not show the server's username or password, or a terminal where either one is visible.
