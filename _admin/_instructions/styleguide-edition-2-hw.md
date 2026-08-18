# Markdown Styleguide — Second Edition (Harvard-Westlake)

*<font color="#8b949e">The working styleguide for this repository. It carries forward the structure of the [First Edition](styleguide-edition-1-acs.md) — the ACS "Typeset Terminal" system — re-grounded in Harvard-Westlake's red, gold, and black, and rewritten so every construction renders natively on GitHub. Where the First Edition records, this edition recommends: each rule explains what it asks for, why it earns its place, and shows the exact markup to copy.</font>*

---

## Contents

1. [What changed from the First Edition](#what-changed-from-the-first-edition)
2. [Foundations](#foundations) — the accent trio, typography, voice
3. [Shared document anatomy](#shared-document-anatomy)
4. [Image stencils](#image-stencils)
5. [Tables of contents](#tables-of-contents)
6. [**Page 1 — Lesson pages**](#page-1--lesson-pages)
7. [**Page 2 — Worksheet and assignment pages**](#page-2--worksheet-and-assignment-pages)

---

## What changed from the First Edition

| Area | First Edition (ACS) | Second Edition (HW) |
|---|---|---|
| Rendering target | Custom stylesheet + print pipeline; class-based HTML | GitHub's renderer, light and dark themes; no stylesheet assumed |
| Accent palette | Ten fixed colors | Three working accents — red, gold, ink — plus neutrals |
| Color markup | CSS classes | `<font color="…">` tags, the one color mechanism GitHub honors |
| Section badges | `>_` filled badge, `[ ]` brackets via CSS | Literal `>_` and `[ ]` characters — the terminal register survives as text |
| Callouts | `<div class="callout">` | Bold-label blockquotes with a colored label |
| Voice | Terse specification | Professional and direct; each rule states its reason |
| Punctuation | No em dashes | Em dashes welcome — this repository's house style uses them |

Everything else carries over intact: the two-register identity, the flat information-dense layout, exercise IDs and hints, the fixed section orders, image stencils, and the discipline that keeps red rare.

---

## Foundations

A Harvard-Westlake document should read the way the school's print materials look: black ink doing the work, red appearing exactly where attention must land, gold warming the margins. The restraint is the brand. A page that uses color everywhere uses it nowhere.

### The accent trio

Three accents, each with a canonical print value and a screen value tuned to stay legible on GitHub's light *and* dark themes. Use the screen value in `<font>` tags; the print value belongs in stylesheets and exported PDFs.

| Accent | Print | Screen | Role — and only this role |
|---|---|---|---|
| **Jet Ink** (black) | `#0f0f0f` | *default text color* | Titles, headings, structure, emphasis through weight. On screen, black is never a `<font>` tag — it is the absence of one, so it adapts to dark theme automatically. |
| <font color="#f85149">**Press Red**</font> | `#c8102e` | `#f85149` | The signal color: callout labels (`TASK`, `WARNING`), due dates, the pathbar leaf, one emphasized cell per table at most. Pantone 186, the school red. |
| <font color="#e3b341">**HW Gold**</font> | `#a37e00` | `#e3b341` | The annotation color: exercise hints, stretch markers, review tags, marginal notes. Gold comments; it never commands. |
| Muted | `#6b6b6b` | `#8b949e` | Subtitles, metadata, footers — text that supports without competing. |

**The Press Red Rule, kept.** Red on 10% or less of any page. One callout label, one due date, one breadcrumb leaf is a full allocation. If you have used red four times on a page, the fourth use has diluted the other three.

**The trio is closed.** No success green, no info blue, no new accents. A semantic state is carried by its label text — `WARNING`, `DONE`, `OPTIONAL` — with at most one accent color behind it. (Course-identity colors from the First Edition — Console Blue, Course Green — remain reserved for logos and course marks, never page content.)

### Typography and the two registers

GitHub chooses the fonts, so the two-register identity survives through *markup* rather than typefaces:

- **The typeset register** is ordinary prose: headings, paragraphs, tables.
- **The terminal register** is everything inline-code and fenced: commands, filenames, exact values, and the literal `>_` and `[EX 01]` markers that label sections and exercises.

The rule of thumb carries over from the First Edition: if a human says it, write it as prose; if a machine reads it or produces it, set it in backticks or a fence. `score >= 70` is machine text even mid-sentence.

### Voice

Write like a colleague, not a compiler. Every rule in a document should let a reader answer *what do I do* and *why does it matter* in one pass:

- **Lead with the action**, follow with the reason. "Test the boundary value `70` — off-by-one errors live at boundaries" beats "Boundary values should be tested."
- **Exact values are sacred.** When an autograder or answer key depends on output, quote it exactly, mark it as exact, and never paraphrase it.
- **Address the student as *you*** in worksheets and assignments; reserve *we* for lessons where the class works together.
- **Precision without coldness.** Plain language, complete sentences, no hedging — but a well-placed encouragement ("finish the required parts first; the stretch will still be there") is professionalism, not padding.

---

## Shared document anatomy

Every document opens with an identity block and closes with a footer, exactly as in the First Edition — rebuilt from constructions GitHub renders.

### The run header and pathbar

A centered identity block: school and course on one line, the path on the next with the **leaf in red** — the single red element of the header. The muted subtitle pattern matches the rest of this repository.

```markdown
<div align="center">

**Harvard-Westlake · Advanced Computer Science**
*<font color="#8b949e">Unit 0 — Java Foundations</font>*

`acs / unit-0 /` <font color="#f85149">**0.3-control-flow**</font> — `lesson.md`

</div>

---
```

### Title and numbering

One H1 per file, numbered `N.M — Title`. The number is the document's address: it appears in the folder name, the pathbar leaf, and the footer, and it is how the class refers to the day ("we're on 0.3").

```markdown
# 0.3 — Control Flow
```

### Callouts

The First Edition's callout becomes a bold-label blockquote. The label is uppercase, colored, and unique on the page section it opens; the body is bold so it stands apart from surrounding prose without further color.

```markdown
> <font color="#f85149">**TASK**</font> — **Trace each conditional and predict the exact console output.**
```

Reserve red labels for directives and warnings. Annotations take gold:

```markdown
> <font color="#e3b341">**HINT**</font> — Boundary values are where conditional bugs most often hide.
```

### The footer

A centered, muted close that repeats the document's address — the last thing on every student-facing page:

```markdown
---

<div align="center">

*<font color="#8b949e">0.3 Worksheet — Control Flow</font>*

</div>
```

### Links

Relative links throughout, angle-bracket-wrapped when the path contains spaces:

```markdown
- [Conditional Statements](<../../Documentation/Conditional Statements.md>)
```

### File naming inside a day folder

Unchanged from the First Edition — the names are the contract between lesson, worksheet, and solutions:

| File | Purpose |
|---|---|
| `lesson.md` | The teaching page for the day |
| `worksheet.md` | In-class practice |
| `worksheet-solutions.md` | Instructor key, structurally identical to the worksheet |
| `assignment-<slug>-lab.md` | The take-home lab |

---

## Image stencils

Figures earn their place the same way sentences do. The mechanics carry over from the First Edition; the embed gains explicit sizing and a caption, because GitHub renders images at full width unless told otherwise.

**Naming and placement.** Figures live in `attachments/` beside the page that owns them, named so any figure traces back to its page:

```text
attachments/<page-slug>-figure-<N>.png
```

**The embed.** Centered, width-constrained, captioned. The `width` attribute keeps a figure from dominating a page; 520px suits most diagrams.

```markdown
<div align="center">
  <img src="attachments/control-flow-figure-1.png"
       alt="Decision diamond: the true branch prints Passed, the false branch skips ahead"
       width="520">

  *<font color="#8b949e">Figure 1 — one condition, two paths</font>*
</div>
```

**Alt text is content.** Describe what the figure shows and why it matters, never the filename. If the alt text would not help someone who cannot see the image, rewrite it.

**The stencil.** Author the slot before the asset exists. A stencil comment reserves the filename, records what the figure must show, and sets the size — so producing the image later is execution, not design. A page ships with the real figure or the stencil; never a broken reference.

```markdown
<!-- IMAGE STENCIL: attachments/control-flow-figure-1.png
     Shows: decision diamond with true branch printing "Passed" and false branch skipping
     Size: 520px wide, roughly 4:3
     Status: NEEDED -->
```

When a worksheet needs a *student-facing* placeholder — a space the student draws or pastes into — make the stencil visible instead: an empty centered table cell with a gold instruction.

```markdown
<div align="center">

| <font color="#e3b341">**PASTE YOUR SCREENSHOT HERE**</font> — full window, URL bar visible |
|---|
| <br><br><br><br> |

</div>
```

---

## Tables of contents

Tables, not link lists, wherever order or pairing matters — a table forces every entry to justify itself in its second column.

**Course TOC (syllabus).** Units in a two-column table, bare integers, full titles:

```markdown
## Course Units

| Unit | Title |
|---|---|
| 0 | Java Foundations: Variables, Objects, Methods, and Output |
| 1 | Algorithmic Thinking: Decisions, Loops, and Problem-Solving Patterns |
```

**Cross-reference TOC.** Every documentation note opens with a Relevant Lessons table pairing each lesson link with one sentence on why the note matters there:

```markdown
## Relevant Lessons

| Lesson | Why this note matters |
|---|---|
| [0.3 — Control Flow](<../Unit 0/0.3 - Control Flow/lesson.md>) | The day's exercises stand on if / else if / else chains. |
```

**Unit TOC with type accents.** When a unit page lists its days, the third column may carry a gold tag naming the day's character — the one place gold appears in a TOC:

```markdown
| Day | Lesson | Focus |
|---|---|---|
| 0.3 | [Control Flow](0.3%20-%20Control%20Flow/lesson.md) | <font color="#e3b341">new concept</font> |
| 0.4 | [Arithmetic Expressions](0.4%20-%20Arithmetic%20Expressions/lesson.md) | <font color="#e3b341">practice</font> |
```

---

<br>

# Page 1 — Lesson pages

*The teaching document for one class day. A student who opens a lesson cold should know within ten seconds what they will be able to do by the end of it.*

## Structure, top to bottom

1. **Identity block** — run header, pathbar, H1 (shared anatomy above).
2. **Meta block** — unit and learning target, closed with a rule.
3. **Four fixed sections** — `>_ Lesson Notes`, `>_ Documentation`, `>_ Assignments`, `>_ Review Worksheets`.

The fixed section set is the contract: notes teach, documentation deepens, assignments direct the work, review closes the loop. A section with little to say keeps its heading and carries one line — dropping it would break the reader's map of the page.

### The meta block and the learning target

Two labeled rows. The learning target is a first-person **"I can"** sentence the student can self-assess against at the end of class — capability, not coverage. Inline code marks the exact language elements involved.

```markdown
**Unit:** Unit 0 — Java Foundations: Variables, Objects, Methods, and Output

**Learning Target:** I can use `if`, `else if`, and `else` statements to make a Java program choose between different paths.

---
```

*Why this works:* "I can use `if` statements to choose between paths" hands the student the measuring stick. "Today we cover conditionals" keeps it in the teacher's pocket.

### The four sections

Section headings keep the literal `>_` marker — the terminal register surviving as text. Collapsibility survives too, through native `<details>`, which GitHub renders:

````markdown
## >_ Lesson Notes

Control flow lets a program make decisions. A condition is a Boolean
expression, and Java runs the body of an `if` statement only when the
condition evaluates to `true`.

```java
if (score >= 70) {
    System.out.println("Passed");
}
```

**Habits that pay off:**

- Braces on every branch — even one-liners.
- Test the boundary values (`70` exactly, not just `72`) — off-by-one errors live at boundaries.
- Mutually exclusive cases take one `if` / `else if` chain; independent classifications take separate `if` statements.

## >_ Documentation

- [Conditional Statements](<../../Documentation/Conditional Statements.md>)
- [Boolean Operators](<../../Documentation/Boolean Operators.md>)
- [Ternary Operator](<../../Documentation/Ternary Operator.md>) — <font color="#e3b341">stretch reference</font>

## >_ Assignments

- Complete the [Conditional Challenge Lab](assignment-conditional-challenge-lab.md) — label every output line so your results are easy to read and grade.

## >_ Review Worksheets

- Work through [worksheet.md](worksheet.md) in class.
- [worksheet-solutions.md](worksheet-solutions.md) is the instructor key.
````

Notice the accent budget of that whole page: gold twice (stretch marker, and it would take a hint callout), red zero times. A lesson page rarely needs red at all — red belongs to deadlines and warnings, and most lessons carry neither.

### An optional collapsible variant

Long reference material inside a lesson may fold, so the page stays scannable. Keep the summary line in the section's voice:

```markdown
<details>
<summary><b>>_ Deep dive — how Java evaluates a chained condition</b></summary>

Java checks each condition top to bottom and runs only the first true branch...

</details>
```

### Documentation notes

One note per concept, shared by every unit, structured as: identity block, H1 concept name, Unit and Learning Target rows, `## Relevant Lessons` table, `## In a Nutshell`, `## Introduction`, `## Key Concepts`, examples, common mistakes. Figures follow the image stencil rules. A concept lives in exactly one note; lessons link to it rather than re-teaching it.

---

<br>

# Page 2 — Worksheet and assignment pages

*The documents a student writes on. Every exercise is addressable, every answer has a home, and a student can tell what kind of thinking is being asked before reading the problem.*

## Worksheets

Structure, top to bottom: identity block, H1, fill-in header, task callout, exercise sections, review section, footer.

### The fill-in header

One line, three write-on fields:

```markdown
**Name:** ______________________ **Date:** ______________ **Block:** ______
```

### The task callout

One per section, framing the work. The red label is usually the page's entire red allocation:

```markdown
> <font color="#f85149">**TASK**</font> — **Trace each conditional and predict the exact console output.**
```

### The exercise block

Each exercise is an H3 carrying the bracketed ID and a gold hint, then the body, then the answer area. The ID makes the exercise addressable in class ("look at EX 04"); the hint names the skill — two or three lowercase words: `if / trace`, `write`, `debug`, `boundary`, `choose structure`.

A trace exercise pairs code with an output box — a fenced block the student fills in, labeled `OUTPUT` in bold ink:

````markdown
### [EX 01] <font color="#e3b341">if / trace</font>

```java
int score = 72;
if (score >= 70) {
    System.out.println("Passed");
}
System.out.println("Done");
```

**OUTPUT**

```text


```
````

A written exercise pairs a prompt with a response area:

```markdown
### [EX 06] <font color="#e3b341">write</font>

Write an `if` / `else` statement that prints `Low battery` when
`batteryPercent` is less than `20`, and `Battery ready` otherwise.
Assume `int batteryPercent = 18;` already exists.

**YOUR CODE**

> <br><br><br>
```

*Why this works:* the ID, hint, and fixed answer area make the page addressable, predictable, and gradable — and the student learns to recognize *kinds* of problems, not just problems.

### Exercise progression and review

Exercises escalate within a worksheet: trace → boundary → write → debug → judgment. Every worksheet closes with a `## >_ Review` section of `[R 01]`-numbered exercises drawn from earlier days — spiral review is standing policy, not a pre-test event.

### Solutions

`worksheet-solutions.md` mirrors the worksheet exactly, with answers in the output and response areas — structure never diverges, so student copy and key compare side by side.

## Assignments

The take-home lab keeps the First Edition's seven sections in fixed order. Section headings carry the `>_` marker; each section opens with its bracketed semantic ID.

| Section | ID / hint | What it answers |
|---|---|---|
| `## >_ Assignment Snapshot` | `[INFO]` | What am I making, for which day, in which file? |
| `## >_ Learning Focus` | `[FOCUS]` | Why this lab, and how is it graded? |
| `## >_ Implementation Requirements` | `[REQ 01]`, `[REQ 02]`, … | Exactly what must the program do? |
| `## >_ Expected Behavior` | `[CHECK]` | What does correct output look like, verbatim? |
| `## >_ Acceptance Checks` | `[CHECKS]` | What do I verify before submitting? |
| `## >_ Submission` | `[SUBMIT]` | Where does it go? |
| `## >_ Stretch Challenge` | `[STRETCH]` | What's next if I finish early? — <font color="#e3b341">optional, ungraded</font> |

A requirement block quotes exact values, because the autograder compares exact output — and a red **due** line in the snapshot is the assignment's one red element:

````markdown
## >_ Assignment Snapshot

**Unit:** Unit 0 — Java Foundations
**Day:** 0.3
**File:** `ConditionalChallenge.java`
**Due:** <font color="#f85149">**before next class**</font>

## >_ Implementation Requirements

### [REQ 02] <font color="#e3b341">temperature</font>

Use these variables:

- `double temperature = 75.0`
- `boolean isCold = true`

If `isCold` is `true`, subtract `15` from `temperature`. Otherwise add `10`.
Print the final value with this exact label:

```text
Temperature: 60.0
```
````

Acceptance checks convert the rubric into a list the student walks in order — checkboxes, one observable fact each:

```markdown
## >_ Acceptance Checks

- [ ] The file is named `ConditionalChallenge.java` and the class matches it.
- [ ] Every part prints its required section header, spelled exactly.
- [ ] The output contains every required line from Expected Behavior.
```

The stretch section stays generous in tone and firm in order: finish the required parts first so the autograder still passes, then extend — each stretch item bolded by name and pointed at a documentation note.

---

<div align="center">

*<font color="#8b949e">Second Edition — Harvard-Westlake accents on the ACS Typeset Terminal. See the [First Edition](styleguide-edition-1-acs.md) for the source system.</font>*

</div>
