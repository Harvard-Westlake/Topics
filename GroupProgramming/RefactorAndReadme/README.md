<div align="center">

# Refactoring and the README
*<font color="#8b949e">Clean the code to match the spec, understand every line, and document it for whoever comes next</font>*

<font color="#a371f7">Learning</font>

</div>

---

Today you clean up your code, make sure you understand it, and then write the two documents that let someone else continue your project: a **README.md** that explains how to set up and run the code, and an **MVP.md** that records what is done and what comes next.

Next class, a classmate will pick up your project cold — the only help they get is what you write today.

---

## <font color="#388bfd">Step 1 — Refactor your code to match your tech spec</font>

The whole point of documentation is to clearly communicate what is going on. Your code should match your documentation.

- **Refactor your code** — organize it into classes and methods
- **Match your tech spec** — if items are now implemented in a way that does not match the tech spec, you are responsible for updating the tech spec to match reality
- **Standardize formatting** — make your indentation, variable names, and function structures consistent
- **Do NOT have all your code in one file**

> **Warning:**
> All of your code **must not be** in a single file — unless it is already represented that way in your Figma design.

---

## <font color="#388bfd">Step 2 — Understand your code</font>

Now it is time to answer the big question: **do you know what your code does?**

- **Go through each function** — write a brief explanation of what it does in plain English
- **Find areas of confusion** — if there is a part you do not fully understand, write it down; we will troubleshoot those together or with AI
- **Reflect on AI-assisted solutions** — identify any code you copied from AI and figure out how it works. It is okay that you relied on AI, but now is your chance to learn how those solutions were built

> **Note:**
> If you cannot explain a function in plain English, you do not own it yet — and you certainly cannot debug it when it breaks in someone else's hands.

---

## <font color="#388bfd">Step 3 — Update your documentation</font>

Once you have cleaned and understood your code, write **two key documents** for your project.

### <font color="#79c0ff">README.md</font>

This file explains:

- How to **set up** your project
- The **key parts of the code** — what are the main files or functions?
- Any **special instructions or tools** you used, and how you set them up
- How someone else can **run** your project — for example `firebase serve`, or whether they need to `npm install` a set of packages first

### <font color="#79c0ff">MVP.md</font>

- Document everything you have **completed so far**
- Clearly define the **next steps** and timeline for whoever works on your code next
- Make it obvious **where the project is headed**

---

## <font color="#388bfd">Why this matters</font>

Understanding your code is not just about passing this class — it is about building real-world skills. Whether you work on a team or come back to this project in six months, your future self (or teammates) will thank you for writing clean, understandable code and clear documentation.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you name the four refactoring requirements (classes/methods, match the spec, consistent formatting, never one file)?
- [ ] Can you list what a project README.md must explain?
- [ ] Can you list what MVP.md must contain?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain each function in your project in plain English, and identify the ones you cannot?
- [ ] Can you find one place where your code no longer matches your tech spec, and fix the mismatch?
- [ ] Can you identify a piece of AI-generated code in your project and explain how it actually works?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you write setup instructions precise enough that a classmate gets your project running without asking you anything?
- [ ] Can you split a too-large file into sensible classes and methods without changing behavior?
- [ ] Can you prioritize the next steps in MVP.md so a stranger would pick the right feature to build first?

---

[Assignment](ASSIGNMENT.md)

← [Issues as Work Requests](../IssuesAsWorkRequests/) — Next: [Help a Classmate](../HelpAClassmate/)
