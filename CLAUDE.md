# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is the public student-facing curriculum repository for the **Honors Topics** computer science course at Harvard-Westlake. It contains no runnable code — only Markdown content rendered on GitHub.

## Structure

```
Topics/
  <topic-name>/
    README.md           — overview and lesson index for the topic
    <subtopic>/
      README.md         — individual lesson
```

Current topics: `ComputerSetup/` (Mac, PC), `Terminal/` (Navigation, Search, Experiment, Files)

## Root README

`README.md` at the repo root must always reflect the current structure. Whenever a topic or subtopic is added, renamed, or removed:

1. Update the top-level `README.md` — one bold linked entry per topic (with a one-sentence summary), and a bulleted list of its subtopics beneath it.
2. Keep the order in `README.md` consistent with the folder order.

Format:

```markdown
**[Topic Name](TopicFolder/)**  
One-sentence description of the topic.

- [Subtopic](TopicFolder/Subtopic/) — one-line summary
```

## Skill Building section

Every README (both topic indexes and individual lesson pages) must end with a Skill Building section placed just above the bottom navigation link. It has three `###` sub-sections — Introductory, Intermediate, Advanced — each with 3 checkbox items (`- [ ]`) phrased as "Can you…" questions that directly test the content on that page.

```markdown
## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you ...
- [ ] Can you ...
- [ ] Can you ...

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you ...

### <font color="#79c0ff">Advanced</font>

- [ ] Can you ...
```

## Topic README (parent folder)

Each topic's `README.md` must end with a numbered lessons table so students know the intended order:

```markdown
## Lessons

| # | Lesson | What you'll learn |
|---|---|---|
| 1 | [First](First/) | One-line description |
| 2 | [Second](Second/) | One-line description |
```

Numbers reflect the recommended consumption order. Update the table whenever subtopics are added or reordered.

## Lesson classifications

Every README title block includes a lesson type label directly below the italic subtitle, inside the `<div align="center">` block. There are four labels that map to three colors:

| Label | Color | Hex | Meaning |
|---|---|---|---|
| Environment Configuration | Green | `#3fb950` | Setup guides — gets machines and tools ready |
| Learning | Purple | `#a371f7` | Introduces new concepts |
| Reinforce | Purple | `#a371f7` | Builds on concepts through practice (same color as Learning) |
| Review | Yellow | `#e3b341` | Revisits and consolidates prior material |

The root README `## Table of Contents` section groups topics by type using a colored `■ Type Name` label on its own line before each group. A `## Lesson Types` legend table appears above the TOC explaining the three colors.

## Color scheme

Apply these colors to non-body, non-H1 text using `<font color="">` tags:

| Element | Color | Usage |
|---|---|---|
| `##` section headers | `#388bfd` | `## <font color="#388bfd">Title</font>` |
| `###` sub-headers | `#79c0ff` | `### <font color="#79c0ff">Title</font>` |
| Italic subtitles | `#8b949e` | `*<font color="#8b949e">subtitle</font>*` |
| Highlighted path in tree diagrams | `#f0883e` | `<strong><font color="#f0883e">item</font></strong>` inside `<pre>` |

When adding new pages, apply the same pattern. To regenerate across all files run the Python script used to create this scheme (regex-based, idempotent — safe to re-run).

## Title format

Every README must open with a centered title block, followed by a rule, then body content:

```markdown
<div align="center">

# Page Title
*Short italic subtitle*

</div>

---

Body content starts here...
```

## ASSIGNMENT.md files

Any lesson subfolder may contain an optional `ASSIGNMENT.md` with the class instructions for that session. These will eventually be linked from Canvas assignments on the course hub, which will point directly to these files.

When an `ASSIGNMENT.md` exists in the same folder as a `README.md`, the README must link to it at the very bottom, placed **above** the bottom navigation line:

```markdown
[Assignment](ASSIGNMENT.md)

← [Prev](../Prev/) — Next: [Next](../Next/)
```

Never add a placeholder link if no `ASSIGNMENT.md` exists — only include it when the file is actually present in that folder.

## Content conventions

- All lessons are GitHub-rendered Markdown — write for GitHub's renderer, not a local previewer.
- Use `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]` callouts for key asides (GitHub renders these as colored blocks).
- Use fenced code blocks with `bash` syntax highlighting for all terminal commands.
- Each subtopic README ends with `← prev — Next: next` navigation links using relative paths.
- No emojis. No frontmatter. No HTML unless Markdown genuinely can't express it.
- Audience: high school students new to CS. Be precise, not condescending.
