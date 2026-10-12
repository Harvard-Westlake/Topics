<div align="center">

# Intro to AI Coding
*<font color="#8b949e">AI coding means you decide what gets built and check every result, while the AI does the typing.</font>*

</div>

---

![Two ideas side by side. On the left, every prompt is what you said, for example "a quiz page about the heart", plus what you left out, such as colors, layout, how many questions, and what happens on a wrong answer; the AI decides those for you. On the right, the manager's loop: 1 Ask, 2 Plan, 3 Agent, 4 Test, then back to Ask for the next small piece. Test means the browser and the console, not the AI saying it works. The AI writes drafts; your name is on the commit.](assets/ai-coding-loop.svg)

You already know HTML, CSS, JavaScript, hosting, and Firestore. Now you get a very fast assistant:

- **The AI fills every gap** you leave in a prompt with its own guess.
- **You are the manager:** you plan, you choose, and you check.
- **Work in small pieces** and test each one in the browser before asking for the next.

## <font color="#388bfd">Table of Contents</font>

1. [Assumptions: what the AI decides when you do not](#assumptions)
2. [Ask, Plan, and Agent: picking the right mode in Cursor](#ask-plan-and-agent)
3. [The manager's loop for building any feature](#the-managers-loop)

## <font color="#388bfd">Assumptions</font>

When you ask an AI for something, everything you **do not** say gets filled in for you. Ask for "a website about dogs" and the AI silently picks the colors, the layout, the tone, the breed in the photos, and whether there is a navigation bar. Those choices are **assumptions**: gaps in your prompt that the AI covers with its own defaults.

| If you don't manage assumptions | If you do |
|---|---|
| Two people with the "same" idea get completely different results. | You can predict and repeat what you get. |
| The AI's choices quietly replace yours. | Your intent survives the trip through the AI. |
| You can't tell a bug from a guess. | You know what you specified and what you left open. |

You could never specify everything. The skill is knowing which decisions you care about, stating those, and leaving the rest open on purpose.

## <font color="#388bfd">Ask, Plan, and Agent</font>

Cursor's chat panel has a mode picker. Choosing the mode is a management decision:

| Mode | What it does | Use it when |
|---|---|---|
| **Ask** | Answers questions about your code. Changes nothing. | You want to **understand** what to do. |
| **Plan** | Researches your files and writes a step-by-step plan for you to edit and approve. | You want to **decide how** it gets built. |
| **Agent** | Edits files and runs commands to carry out the work. | You know what you want and are ready to **hand off the typing**. |

Two more tools keep you in charge:

- **Context:** type `@` to point the AI at the exact files it should read, instead of letting it guess.
- **Rules:** a project rules file (in `.cursor/rules/`) states your standing decisions once, like "use the learnhw styles" or "no frameworks", so you do not repeat them in every prompt.

> **Warning:** AI makes mistakes and then confidently insists it is right. It will say code works that was never run, and "fix" one bug by breaking something else. Check results in the browser and the console, never in the chat window.

## <font color="#388bfd">The Manager's Loop</font>

Build every feature the same way:

1. **Ask** until you can describe the feature precisely in plain English.
2. **Plan** the pieces: which files, which functions, which events, what data goes to Firestore.
3. **Agent** one piece at a time, small enough to test right away. Commit before each Agent step so you can always go back.
4. **Test** in the browser with the console open. Have the AI fix what is actually broken, not what it claims is broken.

Managers who skip straight to Agent get code they do not understand, solving a problem they never defined.

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Take a vague prompt and list three decisions the AI would have to make on its own.
- [ ] Say which Cursor mode you would use to understand, to plan, and to build, and why.
- [ ] Run one loop: ask, plan, build one small piece with Agent, and test it in the browser.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Write a project rules file that pins down three decisions you keep repeating, and show that the AI follows it.

---

[Assignment](ASSIGNMENT.md)

← [Databases and Collections](../DatabasesAndCollections/) | Next: [The Learning Widget Project](../LearningWidget/)
