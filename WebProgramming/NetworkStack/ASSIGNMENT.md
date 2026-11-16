# Assignment - The Network Stack

**Lesson:** [The Network Stack](README.md)  
**Due:** Before the start of next class

---

> **Warning:** CRITICAL. Never put the server's username or password in a repository, a prompt, a screenshot, or a submission.

![A small badge that reads: this page has been loaded, followed by a number, and then the word times. The number is one higher every time anyone opens this assignment, because a service on the class server draws the picture fresh each time it is asked for.](https://theiss.api.codehw.net/badge.svg?page=network-stack-assignment)

That badge is a service at work. Today you install your own: the one that makes your plan for several people at once real.

## Part 1: Bring Codex Onto the Box

1. Log in with `box` and go to the project folder you made by hand.
2. Start Codex there and sign in with your own account. It reads the box's rules on its own.
3. Make this your first message, so every prompt is saved in your exact words:
   ```
   From now on, save every prompt I send you in a file called prompts.md,
   in my exact words, unedited, numbered, with the newest at the bottom.
   Start with this message. Add each new prompt to the file before you do
   anything else with it.
   ```
4. Before any code, have Codex tell you the rules of the box. Correct it until it is right.

**Verify:** Codex can state your port, your public address, how a service is kept running, and what the proxy already does, and all four match `~/README.md`.

---

## Part 2: Install the Service Behind Your Plan

Give Codex your `PLAN.md` in your own words, one piece at a time, and have it build the service that makes the plan work.

**The service is done when:**

- **People share a moment:** two people on two devices each see what the other does within about a second, with no reload.
- **Late arrivals catch up:** someone who opens the site in the middle sees how things stand right now.
- **Leaving is handled:** when one person closes the tab, the others see it and nothing breaks.
- **It lives on the box:** the service runs in your folder, on your port, started the way `~/README.md` says, and it keeps running after you log out.
- **Your website uses it:** your live website connects to your address on the box.
- **The proxy does its part:** your code adds no CORS headers and no HTTPS of its own.
- **The code is yours to keep:** the project is in your own GitHub repository, with nothing secret in it.

**Verify:** open your live website on your laptop and on a phone at the same time. Act on one and watch the other. Then log out of the box, reload both, and do it again.

---

## Part 3: Say What Travels

Look at your own service through today's lesson, with DevTools open on the **Network** tab.

- **The connection:** whether your site keeps asking by HTTP or holds a WebSocket open, and what you would lose with the other one.
- **The transport:** whether it rides on TCP or UDP, and how you know.
- **The trip:** the address and port your browser reached, and which machine on the way added the CORS header.

> <font color="#a371f7">**Mini-Site Project:**</font> Add a server-based interaction that works through the class box, and get your app playable and customer-ready for next class.

---

## Success Criteria

- [ ] **Rules first:** Codex stated the box's rules correctly before it wrote any code.
- [ ] **Together:** two devices on your live website see each other's actions within about a second, with no reload.
- [ ] **Joining and leaving:** a late arrival sees the current state, and a closed tab breaks nothing.
- [ ] **Installed by the rules:** the service runs on your own port, was started the way `~/README.md` says, and still answers after you log out.
- [ ] **Explained:** you can say which connection and which transport your service uses, and why.
- [ ] **Exact prompts:** `prompts.md` holds every prompt you sent, in your exact words.
- [ ] **No login anywhere:** the server's username and password appear nowhere in your repository, `prompts.md`, screenshot, or submission.
- [ ] <font color="#a371f7">**Mini-Site Project:**</font> you worked on your app with today's context and pushed the latest to GitHub and Firebase.

---

## Submission

Submit **text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box, with your whole `prompts.md` pasted underneath:

```
Live website link:                         
My service's address:                      
HTTP or WebSocket, and what I'd lose:      
TCP or UDP, and how I know:                
Who added the CORS header:                 
GitHub repository for the service:         
```

### Screenshot

Your live website open in two windows side by side, each showing the other's most recent action. It must not show the server's username or password, or a terminal where either one is visible.
