# Markdown Styleguide — First Edition (ACS Conventions)

*Documented from the Harvard-Westlake [ACSCurriculum](https://github.com/Harvard-Westlake/ACSCurriculum) repository: its markdown files, worksheets, assignments, and the "Typeset Terminal" design system in its `DESIGN.md`. This edition records the source system as it exists. The [Second Edition](styleguide-edition-2-hw.md) adapts it for this repository with Harvard-Westlake accent colors and GitHub-native rendering.*

---

## Contents

1. [Foundations](#foundations) — palette, typography, named rules
2. [Shared document anatomy](#shared-document-anatomy) — identity blocks every file carries
3. [Image stencils](#image-stencils) — figure naming, placement, and placeholders
4. [Tables of contents](#tables-of-contents) — syllabus, unit, and cross-reference tables
5. [**Page 1 — Lesson pages**](#page-1--lesson-pages)
6. [**Page 2 — Worksheet and assignment pages**](#page-2--worksheet-and-assignment-pages)

---

## Foundations

The ACS system is called **"The Typeset Terminal."** Two registers coexist in every document. The typeset register: editorial hierarchy, print rhythm, ink-on-white clarity. The terminal register: monospace labels, the `>_` section marker, the `[EX 01]` exercise tag. Neither overwhelms the other. A document should feel like a well-written technical specification designed to be handed to a student and written on.

The system is flat and information-dense. Space is rationed. A callout earns its weight through structure and label, not a colored stripe. An exercise card earns its framing through a hairline border and a bracketed identifier, not shadow or radius.

### The fixed palette

Ten colors. They cannot change, and no new accents may be introduced.

| Color | Hex | Role |
|---|---|---|
| Jet Ink | `#0f0f0f` | Primary text; the filled `>_` section badge. Not pure black: the faint warmth keeps it from reading as digital. |
| Press Red | `#c8102e` | The sole chromatic accent. Links, callout labels, the pathbar leaf, active states. Harvard-Westlake Pantone 186 equivalent. |
| Annotation Gold | `#a37e00` | Secondary accent for annotation context: exercise hints, selection highlight, link hover. Darkened from school gold to meet AA contrast on white. |
| Console Blue | `#3a6b96` | Exclusively the `OUTPUT` label on output boxes. Signals machine output without competing with red. |
| Course Green | `#2c5d3f` | Course-identity marks only (logos, thumbnails). Never appears inside a document or UI surface. |
| Muted | `#6b6b6b` | Secondary text: breadcrumbs, header labels, bracket decorations, metadata. |
| Hairline | `#e6e6e6` | Every border and divider in the system, at 1px. |
| Draft Cream | `#f3f1e8` | Warm tint for output boxes and table headers. Signals "occupied space." |
| Code Surface | `#f5f5f4` | Code block backgrounds. A step between the output box and the page. |
| Page | `#ffffff` | Document background. |

**The Press Red Rule.** Press Red appears on 10% or less of any view. One active link, one callout label, one breadcrumb leaf: that is a full allocation. If red appears in four places on one view, one of them is wrong. Rarity is what creates emphasis.

**The Fixed Palette Rule.** Semantic states (success, error, warning) are communicated through label text and structure, never through additional colors. There is no success green or warning amber.

### Typography: two fonts, two roles

- **Geist** (fallback Inter, system-ui) carries all human prose: instructions, explanations, problem descriptions.
- **JetBrains Mono** (fallback Cascadia Code, Consolas) carries the machine voice: labels, badges, metadata, breadcrumbs, and decorative syntax.

These roles never swap. A button label is machine voice (mono, uppercase). A task description is prose (Geist, sentence case). Breaking this rule collapses the dual-register identity.

The hierarchy, from the design tokens:

| Level | Font | Treatment | Used for |
|---|---|---|---|
| Display | Geist 600, 1.75rem | Once per document | The H1 title |
| Headline | Geist 600, 1rem | Rendered with the filled `>_` ink badge | H2 section headings |
| Title | Mono 600, 0.78rem, uppercase | Flanked by `[` `]` in Muted | H3 subsections |
| Body | Geist 400, 0.88rem | 65–75ch line cap in handouts | All prose |
| Label | Mono 700, ~0.6rem, uppercase | Wide tracking | `TASK`, `OUTPUT`, hints, field names |

**The Bracket Decoration Rule.** The `>_` headline prefix and `[ ]` title brackets are part of the type system, not removable decoration. Any rendering that drops them has left the system.

### Flatness

There are no box shadows anywhere. There is no border radius anywhere. Depth comes from exactly three mechanisms: hairline borders, tonal background shifts (page → code surface → draft cream → `#fafafa`), and weight or scale. If a surface seems to need a shadow, the correct move is a 1px hairline border and a background tint.

### Prose rules

From the ACS collaboration guidelines, applied to all curriculum prose:

- **No em dashes.** Use commas, colons, parentheses, or restructure the sentence.
- **Plain, precise language.** No jargon, hedging, or filler. Sentences earn their place.
- **Pedagogy first.** Consider pacing, scaffolding, cognitive load, and likely misconceptions.
- **Exact values.** When an autograder or answer key depends on output, the required text is quoted exactly and marked as exact.

---

## Shared document anatomy

Every ACS markdown file (lesson, worksheet, assignment, documentation note) opens with the same two identity blocks and closes with a footer. These require the handout stylesheet to render; on raw GitHub they degrade to plain text, which is accepted because the delivery surfaces are the curriculum GUI and print.

### The run header

A two-segment strip naming the school and course on the left and the unit on the right. Machine voice, muted, hairline rule below.

```html
<div class="worksheet-runheader">
  <span>Harvard-Westlake | Advanced Computer Science</span>
  <span>Unit 0 - Java Foundations</span>
</div>
```

### The pathbar

A monospace breadcrumb bar above the title: path on the left with the **leaf segment in Press Red**, filename on the right. It is a document identity marker, not optional. The `/` separators render in Hairline so they recede into structure.

```html
<div class="worksheet-pathbar">
  <span class="worksheet-pathbar__crumbs">
    acs<span class="worksheet-pathbar__sep">/</span>unit-0<span class="worksheet-pathbar__sep">/</span><span class="worksheet-pathbar__leaf">0.3-control-flow</span>
  </span>
  <span>lesson.md</span>
</div>
```

### Title and numbering

One H1 per file, numbered `N.M - Title` where `N` is the unit and `M` the day. The same number appears in the folder name, the pathbar leaf, and the footer.

```markdown
# 0.3 - Control Flow
```

### The footer

Every student-facing file closes with a footer strip repeating the day number and document type:

```html
<footer class="worksheet-footer">
  0.3 Worksheet - Control Flow
</footer>
```

### Links

Relative links throughout. Paths containing spaces are wrapped in angle brackets so the link survives markdown parsing:

```markdown
- [Conditional Statements](<../../Documentation/Conditional Statements.md>)
- Complete [worksheet.md](worksheet.md).
```

### File naming inside a day folder

| File | Purpose |
|---|---|
| `lesson.md` | The teaching page for the day |
| `worksheet.md` | In-class practice, printed or on screen |
| `worksheet-solutions.md` | Instructor answer key, same structure as the worksheet |
| `assignment-<slug>-lab.md` | The take-home lab, one file per assignment |

---

## Image stencils

Figures live in an `attachments/` folder beside the markdown that uses them, and follow a strict naming pattern so a figure can always be traced to its page:

```text
attachments/<page-slug>-figure-<N>.png
```

For example, the page `If Statements.md` owns `attachments/if-statements-figure-1.png`. Numbering restarts per page and follows reading order.

A figure is embedded with standard markdown image syntax inside a body-text wrapper:

```html
<div class="documentation-body-text">

![Flow of an if statement from condition to branch](attachments/if-statements-figure-1.png)

</div>
```

Rules:

- **Alt text describes what the figure shows**, not the filename. A screen reader user and a teacher scanning source should both learn something from it.
- **One figure per embed.** Do not stack images in a single paragraph.
- **The stencil placeholder.** When a page is authored before its figure exists, reserve the slot with a stencil comment so the reference, the intended content, and the size are already decided. The comment is invisible in every renderer and is replaced by the real embed when the asset lands:

```markdown
<!-- IMAGE STENCIL: attachments/control-flow-figure-1.png
     Shows: decision diamond with true branch printing "Passed" and false branch skipping
     Size: 520px wide, roughly 4:3
     Status: NEEDED -->
```

- A page ships with either the real figure or the stencil comment. It never ships with a broken image reference.

---

## Tables of contents

The system uses tables, not link lists, wherever order or pairing matters.

### Course TOC (syllabus)

The syllabus lists units in a two-column table. Numbers are bare integers; titles carry the unit's full name:

```markdown
## Course Units

| Unit | Title |
|---|---|
| 0 | Java Foundations: Variables, Objects, Methods, and Output |
| 1 | Algorithmic Thinking: Decisions, Loops, and Problem-Solving Patterns |
```

### Cross-reference TOC (documentation notes)

Every documentation note opens with a "Relevant Lessons" table pairing each linked lesson with one sentence on why the note matters there. The second column always justifies the first:

```markdown
## Relevant Lessons

| Lesson | Why This Note Matters |
|---|---|
| [0.3 - Control Flow](<../Unit 0 - .../0.3 - Control Flow/lesson.md>) | Students use If Statements to support the concepts and practice in this lesson. |
```

### In-lesson TOC

A lesson does not carry a TOC of its own. Its four collapsible sections (see Page 1) are the navigation.

---

<br>

# Page 1 — Lesson pages

*The teaching document for one class day. Reference renderings: the Unit 0 lessons.*

Every `lesson.md` follows one wrapper structure with six structural classes plus two for the collapsible layer, so a teacher writing a new lesson never invents a layout. Every block of text sits inside one of these wrappers.

## Structure, top to bottom

1. **Run header** and **pathbar** (see shared anatomy).
2. **Title block**: the H1 inside a `.lesson-title` div.
3. **Meta block**: `.lesson-meta` holding exactly two labeled rows, closed by a hairline rule.
4. **Four collapsible sections**, each a native `<details open>` element: Lesson Notes, Documentation, Assignments, Review Worksheets.

### The meta block and the learning target

The meta block names the unit and states the day's learning target. The learning target is always a first-person "I can" sentence a student could read aloud and self-assess against. Inline code marks the exact language elements involved.

```html
<div class="lesson-meta">

**Unit:** Unit 0 - Java Foundations: Variables, Objects, Methods, and Output

**Learning Target:** I can use `if`, `else if`, and `else` statements to make a Java program choose between different paths.

</div>
```

How the rule works: one target per day, phrased as capability rather than coverage. "I can use `if` statements to choose between paths" tells the student what they should be able to do when the day ends. "Today we cover conditionals" does not.

### The four sections

Each section is a `<details class="lesson-section" open>` element. The `<summary>` renders with the `>_` ink badge and a rotating chevron; the section is collapsible on screen and prints expanded. Bodies nest `.lesson-section-body` then `.lesson-body-text`; code samples sit in their own `.exercise-body-code` wrapper so they render on Code Surface.

````html
<details class="lesson-section" open>
<summary>Lesson Notes</summary>

<div class="lesson-section-body">

<div class="lesson-body-text">

Control flow lets a program make decisions. A condition is a Boolean expression, and Java runs the body of an `if` statement only when the condition evaluates to `true`.

</div>

<div class="exercise-body-code">

```java
if (score >= 70) {
    System.out.println("Passed");
}
```

</div>

</div>

</details>
````

The four sections and what belongs in each:

| Section | Contents |
|---|---|
| **Lesson Notes** | The concept in prose, minimal and precise, with each code pattern in its own code wrapper, closing with an "Important habits" bullet list. |
| **Documentation** | A flat link list into the shared `Documentation/` reference notes. Stretch references are marked `(stretch reference)` after the link. |
| **Assignments** | Links to the day's `assignment-*.md` labs, each as an actionable bullet: `Complete [Conditional Challenge Lab](assignment-conditional-challenge-lab.md).` |
| **Review Worksheets** | Links to `worksheet.md` and `worksheet-solutions.md`, with the solutions line marked "for instructor review." |

How the rule works: the fixed section set means a student always knows where to look. Notes teach, Documentation deepens, Assignments direct the work, Review Worksheets close the loop. A lesson missing a section keeps the heading with a one-line body rather than dropping it.

### Documentation notes (the reference layer)

The `Documentation/` folder holds one note per concept, shared across all units. Each note follows: identity blocks, H1 concept name, Unit and Learning Target rows, `## Relevant Lessons` cross-reference table, `## In a Nutshell`, `## Introduction`, `## Key Concepts` (with bracketed H3 subsections), examples, and common mistakes. Figures follow the image stencil rules above. Lessons link into notes; notes link back to lessons through the Relevant Lessons table. Content lives in exactly one place.

---

<br>

# Page 2 — Worksheet and assignment pages

*The documents a student writes on. Reference implementation: the 0.1 Introduction to OOP and Printing worksheet.*

## Worksheets

A worksheet is a grid of exercise cards under a task callout. Structure, top to bottom: identity blocks, H1, the fill-in header, one or more sections of exercise cards, the footer.

### The fill-in header

Three labeled write-on lines. Machine-voice labels, hairline lines:

```html
<header class="worksheet-header">
  <div class="worksheet-header__field"><span class="worksheet-header__label">Name</span><span class="worksheet-header__line"></span></div>
  <div class="worksheet-header__field"><span class="worksheet-header__label">Date</span><span class="worksheet-header__line"></span></div>
  <div class="worksheet-header__field"><span class="worksheet-header__label">Block</span><span class="worksheet-header__line"></span></div>
</header>
```

### The task callout

One callout opens each worksheet section and frames the work. The label is the only red element; the body is bold Geist. No side stripe: the full hairline border and the label carry all the emphasis.

```html
<div class="callout">
  <span class="callout__label">Task</span>
  <p class="callout__text">Trace each conditional and predict the exact console output.</p>
</div>
```

### The exercise card

The signature component. Cards sit in a 2-column `.worksheet-grid`; a card that needs the full width adds `exercise--wide`. Every card has a header strip, a body, and an answer area pinned to the bottom.

The header strip carries two labels:

- **The ID**: `EX 01`, `EX 02` for the day's exercises; `R 01`, `R 02` for spiral-review items. Brackets render in Muted around the ink label.
- **The hint** (Annotation Gold, uppercase): the skill being exercised, in two or three lowercase words: `if / trace`, `write`, `debug`, `boundary`, `choose structure`.

Trace exercises take a code body and an empty output box; written exercises take a prose body and a response box:

````html
<section class="exercise exercise--code">
<div class="exercise__head"><span class="exercise__id">EX 01</span><span class="exercise__hint">if / trace</span></div>

<div class="exercise-body-code">

```java
int score = 72;
if (score >= 70) {
    System.out.println("Passed");
}
System.out.println("Done");
```

</div>

<pre class="output-box"><code></code></pre>
</section>
````

```html
<section class="exercise exercise--response">
<div class="exercise__head"><span class="exercise__id">EX 06</span><span class="exercise__hint">write</span></div>

<div class="exercise-body-text">

Write an `if` / `else` statement that prints `Low battery` when `batteryPercent` is less than `20`.

</div>

<div class="response-box"></div>
</section>
```

How the rule works: the ID makes every exercise addressable in class ("look at EX 04"), the hint tells the student what kind of thinking is being asked before they read the problem, and the fixed answer area makes the page writable and gradable. The output box is Draft Cream with the Console Blue `OUTPUT` badge; it is sized for the expected answer, not left to grow.

### Exercise progression

Within a worksheet, exercises escalate: trace first, boundary cases next, then write, then debug, then judgment ("choose structure"). A closing `## Review` section carries `R`-numbered cards drawn from earlier days. Review is present on every worksheet, not only before assessments.

### Solutions

`worksheet-solutions.md` mirrors the worksheet exactly, with the output and response boxes filled. Structure never diverges from the student copy, so the two can be compared side by side.

## Assignments

An assignment (`assignment-<slug>-lab.md`) uses the same card grammar inside `.assignment-grid` wrappers, one section per H2, in a fixed order. Card IDs are semantic rather than numbered where the section has one card:

| Section | Card ID / hint | Contents |
|---|---|---|
| `## Assignment Snapshot` | `INFO` / `snapshot` | Unit, day number, and the exact file to create. |
| `## Learning Focus` | `FOCUS` / `overview` | What the lab practices and how it is graded. Names the autograder when one is used. |
| `## Implementation Requirements` | `REQ 01`, `REQ 02`, ... | One card per requirement, each with exact variable values and required output labels. The first REQ card is usually `exercise--wide` and carries the starter skeleton. |
| `## Expected Behavior` | `CHECK` / `expected` | The full required output in an output box, quoted exactly. |
| `## Acceptance Checks` | `CHECKS` / `verify` | A pre-submission bullet checklist a student can walk in order. |
| `## Submission` | `SUBMIT` / `turn in` | Where and what to submit, one sentence. |
| `## Stretch Challenge` | `STRETCH` / `optional` | Ungraded extensions, each bolded by name, each pointing at a documentation note. |

A requirement card states exact values because the autograder compares exact output:

````html
<section class="exercise">
<div class="exercise__head"><span class="exercise__id">REQ 02</span><span class="exercise__hint">temperature</span></div>

<div class="exercise-body-text">

### Part 1: Temperature Converter

Use these variables:

- `double temperature = 75.0`
- `boolean isCold = true`

If `isCold` is `true`, subtract `15` from `temperature`. Otherwise, add `10`.

Print the final value with this exact label:

</div>

<div class="exercise-body-code">

```text
Temperature: 60.0
```

</div>
</section>
````

How the rule works: Snapshot answers "what am I making," Focus answers "why," Requirements answer "exactly what," Expected Behavior lets a student self-grade before submitting, Acceptance Checks convert grading criteria into a walkable list, and Stretch keeps fast finishers inside the same lab. The stretch section always opens by telling the student to finish the required parts first so the autograder still passes.

---

*First Edition. Recorded from ACSCurriculum as-is; adjustments for this repository's colors and GitHub rendering are the [Second Edition](styleguide-edition-2-hw.md).*
