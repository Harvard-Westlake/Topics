# Assignment - SSH, Keys, and CORS

**Lesson:** [SSH, Keys, and CORS](README.md)  
**Due:** Before the start of next class

---

> **Warning:** CRITICAL. Never put the server's username or password in a repository, a prompt, a screenshot, or a submission.

![A small badge that reads: this page has been loaded, followed by a number, and then the word times. The number is one higher every time anyone opens this assignment, because a service on the class server draws the picture fresh each time it is asked for.](https://theiss.api.codehw.net/badge.svg?page=ssh-keys-cors-assignment)

A service on the class server counted you just now. Today you get onto that server and plan what yours will do.

## Part 1: Log In to the Box

1. In your terminal, connect with the address and class login given in class:
   ```bash
   ssh CLASS-LOGIN@SERVER-ADDRESS
   ```
2. The first time, `ssh` shows a fingerprint. Check it against the one shown in class, then answer `yes`.
3. Type the class password, then your **first name** and your **last initial** when asked. The box joins them into your name on the box, such as `alicek`.

**Verify:** `pwd` ends in your name on the box. The box made that folder for you, and it is yours alone.

> **Warning:** Typing someone else's name is an Honor Code violation.

---

## Part 2: Install Your Key and Make a Shortcut

After this part you log in with one word, no password, and no name question.

1. **Copy your public key.** In a terminal on your own computer, print it and copy the whole line:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   If the file does not exist, make a key pair first with `ssh-keygen -t ed25519` and press Enter at each question.
2. **Add it to the box with `addkey`.** In your terminal on the box, run this one command, with your own key line pasted between the quotes:
   ```bash
   addkey "PASTE-YOUR-PUBLIC-KEY-LINE-HERE"
   ```
   The box answers `Added your key`, or tells you in plain words what was wrong with the paste.
3. **Name the box.** On your own computer, add this entry to the file `~/.ssh/config`, with the three values filled in:
   ```text
   Host box
     HostName SERVER-ADDRESS
     User CLASS-LOGIN
     IdentityFile ~/.ssh/id_ed25519
     SetEnv STUDENT=yournameonthebox
   ```
4. **Make the alias.** On your own computer, add this line to `~/.zshrc` (Mac) or `~/.bashrc` (WSL), then open a new terminal:
   ```bash
   alias box="ssh box"
   ```

**What `addkey` does, and what it refuses:**

- **It adds one line.** Your public key goes at the end of the class's shared `authorized_keys` file, labeled with your name and the date.
- **It needs no special permission.** It runs as the class login you are already using.
- **It is safe to repeat.** A key that is already there is skipped, and two classmates running it at once cannot damage the file.
- **It refuses mistakes.** A private key, a key cut off in the middle, or a paste that spans several lines is rejected with a message, and nothing is written.

> **Warning:** Always use `addkey`. Editing `authorized_keys` by hand can erase every classmate's key.

| What you made | Where it lives | What it does |
|---|---|---|
| A line in `authorized_keys`, written by `addkey` | The box | Lets your key in. The class shares one file, one line per student. |
| A `Host box` entry | `~/.ssh/config` on your computer | Remembers the address, the login, your key, and your name. |
| An alias | `~/.zshrc` or `~/.bashrc` on your computer | Turns `ssh box` into `box`. |

**Verify:** type `exit`, open a new terminal, and type `box`. You land in your own folder with no password and no name question.

---

## Part 3: Read the Instructions in Your Folder

Your folder holds `README.md`: the rules that keep everyone's services apart. Nobody can edit it, and every AI you run on the box reads it first.

- **What must be true:** you have read all of `~/README.md` yourself, and run `myports`.
- **Verify:** without looking, you can say your public address, the port your service must listen on, the command that keeps a service running after you log out, and two things the proxy does so your code must not.

---

## Part 4: Make Folders by Hand

No AI for this part. You type every command.

- **What must be true:** inside `~/projects` there is one folder named for your idea, and inside that at least two more folders for the parts you expect to need.
- **Verify:** `ls -R ~/projects` shows all of them, and nothing of yours exists outside your own folder.

---

## Part 5: Plan Something People Do Together

Your site so far has one visitor at a time. Plan an experience that only works when several people are on your site at the same moment. No code for this part today: the plan is the work, and it is in your own words.

Write `PLAN.md` in your website's repository and answer each of these:

- **Who is there together:** two or more specific people, in one real moment.
- **What one person does, and what the others see:** for each action, what changes on everyone else's screen, and how fast it has to.
- **What everyone must agree on:** the one piece of information the server holds for all of them.
- **Joining and leaving:** what a late arrival sees, and what the others see when someone closes the tab.
- **Why it is better together:** what would be lost if each person used it alone.

**Verify:** read the plan to a neighbor. They can act out two people using it at once, without asking you a question.

> <font color="#a371f7">**Mini-Site Project:**</font> PLAN how your site will engage several users at once, and keep vibe coding to make it more robust, enjoyable, and interactive.

---

## Success Criteria

- [ ] **Logged in:** you reached the box over SSH and you are in the folder with your name on it.
- [ ] **Key installed:** `box` logs you in with no password and no name question.
- [ ] **Rules read:** you can state your address, your port, how a service stays up, and what the proxy does for you.
- [ ] **Folders made by hand:** your project folder and at least two folders inside it exist under `~/projects`.
- [ ] **A plan for many people:** `PLAN.md` answers all five questions for people using your site at the same moment.
- [ ] **Site link submitted:** your submission starts with a working link to your current live site.
- [ ] **No login anywhere:** the server's username and password appear nowhere in your repository, screenshot, or submission.
- [ ] <font color="#a371f7">**Mini-Site Project:**</font> you worked on your app with today's context and pushed the latest to GitHub and Firebase.

---

## Submission

Submit **text and a screenshot** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box, with your whole `PLAN.md` pasted underneath. The link to your current live site is required: a submission without it is not complete.

```
Link to my current live site (required): 
My address on the box:                  
The port my service must listen on:     
What stays up after I log out, and how: 
Two things the proxy does for me:       
Folders I made:                         
```

### Screenshot

Your terminal on the box after running `clear`, then `myports`, then `ls -R ~/projects`. Run `clear` first: the welcome message shows the class login, and it must not be in the picture.
