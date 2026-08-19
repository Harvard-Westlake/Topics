# Markdown Styleguide — Second Edition (Harvard-Westlake)

*<font color="#4D4D4D">The working styleguide for this repository. It carries forward the structure of the [First Edition](styleguide-edition-1-acs.md) — the ACS "Typeset Terminal" system — re-grounded in Harvard-Westlake's brand, and rewritten so every construction renders natively on GitHub. **Revision 2 (proposal):** every color and semantic role now comes from the school's official digital brand tokens, recorded verbatim in the [HW Digital Brand Reference](styleguide-learn-hw.md) extracted from learn.hw.com. Where the First Edition records, this edition recommends: each rule explains what it asks for, why it earns its place, and shows the exact markup to copy.</font>*

---

## Contents

1. [What changed from the First Edition](#what-changed-from-the-first-edition)
2. [Revision 2 — alignment with learn.hw.com](#revision-2--alignment-with-learnhwcom)
3. [Foundations](#foundations) — the approved palette, typography, voice
4. [Shared document anatomy](#shared-document-anatomy)
5. [Constructions borrowed from the app](#constructions-borrowed-from-the-app)
6. [Image stencils](#image-stencils)
7. [Tables of contents](#tables-of-contents)
8. [**Page 1 — Lesson pages**](#page-1--lesson-pages)
9. [**Page 2 — Worksheet and assignment pages**](#page-2--worksheet-and-assignment-pages)

---

## What changed from the First Edition

| Area | First Edition (ACS) | Second Edition (HW) |
|---|---|---|
| Rendering target | Custom stylesheet + print pipeline; class-based HTML | GitHub's renderer; no stylesheet assumed |
| Accent palette | Ten fixed colors | The approved HW brand palette — three primaries + five semantic secondaries |
| Color markup | CSS classes | `<font color="…">` tags carrying the official token values |
| Section badges | `>_` filled badge, `[ ]` brackets via CSS | Literal `>_` and `[ ]` characters — the terminal register survives as text |
| Callouts | `<div class="callout">` | Bold-label blockquotes with a colored label |
| Voice | Terse specification | Professional and direct; each rule states its reason |
| Punctuation | No em dashes | Em dashes welcome — this repository's house style uses them |

Everything else carries over intact: the two-register identity, the flat information-dense layout, exercise IDs and hints, the fixed section orders, image stencils, and the discipline that keeps red rare.

---

## Revision 2 — alignment with learn.hw.com

Revision 1 approximated the school's colors from print references and GitHub's own palette. The school's class resources app at learn.hw.com publishes the actual brand tokens; this revision adopts them wholesale. What changes, old → new:

| What | Revision 1 | Revision 2 (this proposal) |
|---|---|---|
| Red | `#c8102e` print / `#f85149` screen | **Brand Red `#DA0016`** — the official token, one value |
| Gold | `#a37e00` print / `#e3b341` screen | **Brand Gold `#EDA300`** |
| Muted | `#6b6b6b` print / `#8b949e` screen | **Secondary Black `#4D4D4D`** |
| Palette scope | Closed trio — "no success green, no info blue" | The approved eight: 3 primaries + 5 secondaries, each locked to its semantic role |
| `WARNING` callouts | Red | **Secondary Orange `#FA7300`** — the app's warning color; red is reserved for errors, deadlines, and directives |
| `OUTPUT` label | Bold ink | **Secondary Blue `#539ADC`** — restores the First Edition's Console Blue distinction with an approved token |
| New label families | — | `INFO` (blue) and `DONE` (green) callouts |
| New constructions | — | Eyebrow, step table, metrics table, labeled divider |
| Emoji | Banned by repo convention | Confirmed by the brand: the app replaces emoji with SVG icons; markdown simply omits them |

Dropping the print/screen dual values simplifies every construction: one token, one hex. Two tokens read poorly on dark surfaces — if a construction targets a surface known to be dark, substitute Brand Red → `#f85149` and Secondary Black → `#8b949e`; everywhere else the official values stand. Interactive `demos/*.html` pages carry their own CSS and should use the [full token set](styleguide-learn-hw.md) directly, tints and all.

---

## Foundations

A Harvard-Westlake document should read the way the school's print materials look: black ink doing the work, red appearing exactly where attention must land, gold warming the margins. The restraint is the brand. A page that uses color everywhere uses it nowhere.

### The approved palette

Eight colors, verbatim from the school's brand tokens. The three primaries do the everyday editorial work; the five secondaries appear **only in their semantic roles**, never decoratively.

| Accent | Token | Role — and only this role |
|---|---|---|
| **Brand Black** | `#000000` | Titles, headings, structure, emphasis through weight. On GitHub, black is never a `<font>` tag — it is the absence of one, so it adapts to dark theme automatically. |
| <font color="#DA0016">**Brand Red**</font> | `#DA0016` | The signal color: directive labels (`TASK`), due dates, error callouts, the pathbar leaf, at most one emphasized cell per table. |
| <font color="#EDA300">**Brand Gold**</font> | `#EDA300` | The annotation color: hints, stretch markers, review tags, marginal notes. The app's default callout is gold-bordered — "educational hints and important caveats." Gold comments; it never commands. |
| <font color="#4D4D4D">**Secondary Black**</font> | `#4D4D4D` | Muted text: subtitles, eyebrows, metadata, footers — text that supports without competing. |
| <font color="#539ADC">**Secondary Blue**</font> | `#539ADC` | Information: `INFO` callout labels and the `OUTPUT` label on output boxes. |
| <font color="#9CCA00">**Secondary Green**</font> | `#9CCA00` | Success: `DONE` / `SUCCESS` callout labels and expected end states. |
| <font color="#FA7300">**Secondary Orange**</font> | `#FA7300` | Warning: `WARNING` / `CAUTION` callout labels, destructive-command notes. |
| <font color="#BFC299">**Secondary Khaki**</font> | `#BFC299` | The code identity (khaki-on-black in the app) and disabled states. In markdown it almost never appears as text color — GitHub styles code blocks itself — but demos and generated HTML use it for code surfaces. |

**The Red Rule, kept.** Red on 10% or less of any page. One callout label, one due date, one breadcrumb leaf is a full allocation. If you have used red four times on a page, the fourth use has diluted the other three.

**The palette is closed at the approved eight.** No new accents, and no secondary outside its role: blue never decorates a heading, green never highlights a table row, orange never marks a hint. A semantic state is carried by its label text — `WARNING`, `DONE`, `OPTIONAL` — with exactly its one assigned color behind it. (The tokens' 50% and 20% tints do not survive markdown; tables and blockquotes provide "occupied space" instead. Demos use the tints directly.)

### Typography and the two registers

The brand sets Source Sans 3 — Black 900 headlines, Semibold subheads, Light/Regular body. GitHub chooses the fonts, so the hierarchy survives through *markup weight* instead: heading levels carry the Black-headline role, bold lead-ins carry Semibold, body text carries Regular. The two-register identity survives the same way:

- **The typeset register** is ordinary prose: headings, paragraphs, tables.
- **The terminal register** is everything inline-code and fenced: commands, filenames, exact values, and the literal `>_` and `[EX 01]` markers that label sections and exercises. (In the app this register is literally khaki-on-black code panels; on GitHub, fenced blocks carry it.)

The rule of thumb carries over from the First Edition: if a human says it, write it as prose; if a machine reads it or produces it, set it in backticks or a fence. `score >= 70` is machine text even mid-sentence.

**Headings are black — with one sanctioned exception.** The app ships a `.red` utility: a Brand Red, all-uppercase heading for moments that must command the page. The markdown equivalent is allowed at most once per page, and it spends the entire red budget:

```markdown
## <font color="#DA0016">DUE DATES MOVED — READ BEFORE CLASS</font>
```

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

A centered identity block: an eyebrow above, school and course on one line, the path on the next with the **leaf in red** — the single red element of the header. The eyebrow is the app's small-uppercase-label pattern: bold, uppercase, Secondary Black.

```markdown
<div align="center">

**<font color="#4D4D4D">UNIT 0 · JAVA FOUNDATIONS</font>**

**Harvard-Westlake · Advanced Computer Science**

`acs / unit-0 /` <font color="#DA0016">**0.3-control-flow**</font> — `lesson.md`

</div>

---
```

### Title and numbering

One H1 per file, numbered `N.M — Title`. The number is the document's address: it appears in the folder name, the pathbar leaf, and the footer, and it is how the class refers to the day ("we're on 0.3").

```markdown
# 0.3 — Control Flow
```

### Callouts

The app's callouts and alerts translate to bold-label blockquotes. The label is uppercase, colored by its semantic family, and unique in the section it opens; the body of a directive is bold so it stands apart without further color.

| Label family | Color | Use |
|---|---|---|
| `TASK` `DUE` `ERROR` | <font color="#DA0016">Brand Red `#DA0016`</font> | Directives, deadlines, errors — the page's red allocation |
| `WARNING` `CAUTION` | <font color="#FA7300">Orange `#FA7300`</font> | Risky steps, destructive commands, common pitfalls |
| `HINT` `NOTE` `STRETCH` | <font color="#EDA300">Gold `#EDA300`</font> | Educational hints and caveats — the app's default callout |
| `INFO` | <font color="#539ADC">Blue `#539ADC`</font> | Background and context that isn't an instruction |
| `DONE` `SUCCESS` | <font color="#9CCA00">Green `#9CCA00`</font> | Confirmations and expected end states |

```markdown
> <font color="#DA0016">**TASK**</font> — **Trace each conditional and predict the exact console output.**

> <font color="#FA7300">**WARNING**</font> — `git reset --hard` erases uncommitted work. Run `git status` first.

> <font color="#EDA300">**HINT**</font> — Boundary values are where conditional bugs most often hide.

> <font color="#539ADC">**INFO**</font> — Canvas lists this assignment under Unit 0; the repo is the source of truth.

> <font color="#9CCA00">**DONE**</font> — Your prompt now shows the branch name. That's the end state for this section.
```

Budget: gold and blue are the everyday labels. Orange appears when a mistake would genuinely cost the student something. Green closes a section at most once. Red follows the Red Rule — one directive or one due date is a full allocation.

### The footer

A centered, muted close that repeats the document's address — the last thing on every student-facing page:

```markdown
---

<div align="center">

*<font color="#4D4D4D">0.3 Worksheet — Control Flow</font>*

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

## Constructions borrowed from the app

Four patterns from the app's component library translate cleanly to markdown. Use them when the content genuinely has their shape — never as decoration.

### Step table

The app's step cards — "numbered sequence cards for showing algorithm phases or process steps" — become a two-column table with bold, numbered step names:

```markdown
| Step | What happens |
|---|---|
| **1 — Pre-processing** | Pad the message to a multiple of 512 bits; append the original length. |
| **2 — Chunk processing** | Break the padded message into 512-bit chunks; expand each into 80 words. |
| **3 — Final hash** | Concatenate the five state variables into the 160-bit digest. |
```

### Metrics table

The app's stat cards — "at-a-glance numbers for dashboards, summaries, or algorithm stats" — become a compact table with the numbers bold and the units plain:

```markdown
| Digest size | Rounds | Block size | Word size |
|---|---|---|---|
| **160** bits | **80** | **512** bits | **32** bits |
```

### Eyebrow

The small uppercase label the app places above titles. In markdown it opens the identity block (see above) and may introduce a major page region:

```markdown
**<font color="#4D4D4D">INTERACTIVE TOOLS</font>**
```

### Labeled divider

The app's divider-with-inline-label, for a hard break between unrelated page regions. Optional — most pages only need `---`:

```markdown
---

<div align="center">

**<font color="#4D4D4D">SECTION BREAK</font>**

</div>
```

### Accordion

Long reference material may fold, so the page stays scannable — the app's accordion is "expandable panels for hints, FAQs, or collapsible content," and GitHub renders `<details>` natively. Keep the summary line in the section's voice:

```markdown
<details>
<summary><b>>_ Deep dive — how Java evaluates a chained condition</b></summary>

Java checks each condition top to bottom and runs only the first true branch...

</details>
```

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

  *<font color="#4D4D4D">Figure 1 — one condition, two paths</font>*
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

| <font color="#EDA300">**PASTE YOUR SCREENSHOT HERE**</font> — full window, URL bar visible |
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
| 0.3 | [Control Flow](0.3%20-%20Control%20Flow/lesson.md) | <font color="#EDA300">new concept</font> |
| 0.4 | [Arithmetic Expressions](0.4%20-%20Arithmetic%20Expressions/lesson.md) | <font color="#EDA300">practice</font> |
```

---

<br>

# Page 1 — Lesson pages

*The teaching document for one class day. A student who opens a lesson cold should know within ten seconds what they will be able to do by the end of it.*

## Structure, top to bottom

1. **Identity block** — eyebrow, run header, pathbar, H1 (shared anatomy above).
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

Section headings keep the literal `>_` marker — the terminal register surviving as text:

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
- [Ternary Operator](<../../Documentation/Ternary Operator.md>) — <font color="#EDA300">stretch reference</font>

## >_ Assignments

- Complete the [Conditional Challenge Lab](assignment-conditional-challenge-lab.md) — label every output line so your results are easy to read and grade.

## >_ Review Worksheets

- Work through [worksheet.md](worksheet.md) in class.
- [worksheet-solutions.md](worksheet-solutions.md) is the instructor key.
````

Notice the accent budget of that whole page: gold twice (stretch marker, and it would take a hint callout), red zero times. A lesson page rarely needs red at all — red belongs to deadlines, directives, and errors, and most lessons carry none of them.

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
> <font color="#DA0016">**TASK**</font> — **Trace each conditional and predict the exact console output.**
```

### The exercise block

Each exercise is an H3 carrying the bracketed ID and a gold hint, then the body, then the answer area. The ID makes the exercise addressable in class ("look at EX 04"); the hint names the skill — two or three lowercase words: `if / trace`, `write`, `debug`, `boundary`, `choose structure`.

A trace exercise pairs code with an output box — a fenced block the student fills in, labeled `OUTPUT` in Secondary Blue, the machine-voice color the First Edition reserved for exactly this:

````markdown
### [EX 01] <font color="#EDA300">if / trace</font>

```java
int score = 72;
if (score >= 70) {
    System.out.println("Passed");
}
System.out.println("Done");
```

**<font color="#539ADC">OUTPUT</font>**

```text


```
````

A written exercise pairs a prompt with a response area:

```markdown
### [EX 06] <font color="#EDA300">write</font>

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
| `## >_ Stretch Challenge` | `[STRETCH]` | What's next if I finish early? — <font color="#EDA300">optional, ungraded</font> |

A requirement block quotes exact values, because the autograder compares exact output — and a red **due** line in the snapshot is the assignment's one red element:

````markdown
## >_ Assignment Snapshot

**Unit:** Unit 0 — Java Foundations
**Day:** 0.3
**File:** `ConditionalChallenge.java`
**Due:** <font color="#DA0016">**before next class**</font>

## >_ Implementation Requirements

### [REQ 02] <font color="#EDA300">temperature</font>

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

*<font color="#4D4D4D">Second Edition, Revision 2 — the official HW brand tokens on the ACS Typeset Terminal. Sources: the [First Edition](styleguide-edition-1-acs.md) for the system, the [HW Digital Brand Reference](styleguide-learn-hw.md) for the tokens.</font>*

</div>
