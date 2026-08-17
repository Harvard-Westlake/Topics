<div align="center">

# Interfacing with AI
*<font color="#8b949e">Assumptions, prompting, and using AI to research topics you have never seen</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Learning Objectives](#learning-objectives)**  
What you should be able to do by the end of this lesson.

**[Assumptions: The Silent Ingredient in Every Prompt](#assumptions-the-silent-ingredient-in-every-prompt)**  
Why the same prompt produces wildly different results, and where the differences come from.

**[Researching a New Topic with AI](#researching-a-new-topic-with-ai)**  
A repeatable technique for learning something you have never seen — starting with HTML.

**[Creating and Viewing HTML Pages in Cursor](#creating-and-viewing-html-pages-in-cursor)**  
Your first hands-on step: make a real page and open it in a browser.

---

## <font color="#388bfd">Learning Objectives</font>

By the end of this lesson, you should be able to:

1. Explain what an **assumption** is in the context of prompting AI, and identify the assumptions hidden in a prompt
2. Use AI to research a topic that is new to you — and verify what it tells you
3. Create an HTML file in Cursor and view it in a web browser

---

## <font color="#388bfd">Assumptions: The Silent Ingredient in Every Prompt</font>

When you ask an AI for something, everything you *do not* say gets filled in for you. Ask for "a website about dogs" and the AI silently decides the colors, the layout, the tone, the breed in the photos, and whether there is a navigation bar. Those decisions are **assumptions** — gaps in your prompt that the AI papers over with its own defaults.

This matters for two reasons:

| If you don't manage assumptions... | If you do... |
|---|---|
| Two people with the "same" idea get completely different results | You can predict and reproduce what you'll get |
| The AI's choices quietly replace your choices | Your intent survives the trip through the AI |
| You can't tell whether an odd result is a bug or a guess | You know exactly what you specified and what you left open |

> **Note:**
> Assumptions are not bad — you could never specify *everything*. The skill is knowing which decisions you care about and stating those explicitly, while consciously leaving the rest open.

You will test this directly in today's activities: everyone runs a nearly identical prompt, then we analyze how — and why — the results diverge.

---

## <font color="#388bfd">Researching a New Topic with AI</font>

AI is one of the fastest research tutors ever built — *if* you drive it correctly. Today's research topic is **HTML**, the language web pages are written in. Use this technique, and reuse it every time this course throws a new topic at you:

1. **Ask for the shape first.** "What is HTML? Explain it to a high school student in five sentences." Get the outline before the details.
2. **Ask follow-ups relentlessly.** Every term you don't recognize becomes your next question: "You said 'tag' — what is a tag?"
3. **Ask for a tiny example.** "Show me the smallest complete HTML page that displays one heading."
4. **Flip the direction: make it quiz you.** "Ask me three questions to check whether I understood." Being tested exposes what reading alone hides.
5. **Verify one claim independently.** Pick a statement the AI made and confirm it against a primary source — for HTML, that is [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML). AI answers are drafts, not verdicts.

> **Tip:**
> If the AI's answer contains a sentence you could not explain to a classmate, you are not done researching — you have just moved the mystery one layer down.

Skim the [HTML reference doc](../Docs/html.md) after your research and check the AI's story against it.

---

## <font color="#388bfd">Creating and Viewing HTML Pages in Cursor</font>

Time to make a real page. In Cursor:

1. Create a folder for today's work and open it (**File → Open Folder**)
2. Create a new file named `index.html`
3. Type (do not paste — typing builds recognition) a minimal page:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My First Page</title>
  </head>
  <body>
    <h1>Hello from Cursor</h1>
    <p>This page was written by hand.</p>
  </body>
</html>
```

4. Save the file
5. Find `index.html` in your file manager (Finder or File Explorer) and double-click it — it opens in your web browser

The browser renders your text file as a page. Change the heading in Cursor, save, and refresh the browser to watch the edit appear. This edit-save-refresh loop is the basic heartbeat of all web development.

> **Warning:**
> The browser shows the file *as it was when you loaded it*. If an edit doesn't seem to appear, you almost certainly forgot to save the file or refresh the browser — check both before suspecting anything deeper.

Today's activities — the assumption experiment and the divergence analysis — are in the [assignment](ASSIGNMENT.md).

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you define an assumption in the context of prompting AI and give one example?
- [ ] Can you create an HTML file in Cursor and open it in a browser?
- [ ] Can you name the five steps of the AI research technique?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you take a vague prompt and list three decisions the AI would have to make on its own?
- [ ] Can you explain why the same prompt gives different students different results?
- [ ] Can you use the edit-save-refresh loop to change a page and see the change appear?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you rewrite a vague prompt so that two different people would get nearly identical results?
- [ ] Can you verify an AI claim against a primary source and explain why that step is never optional?
- [ ] Can you apply the research technique to a topic outside computer science and show it still works?

---

[Assignment](ASSIGNMENT.md)

← Back to [Web Programming](../) — Next: [Website Hosting](../WebsiteHosting/)
