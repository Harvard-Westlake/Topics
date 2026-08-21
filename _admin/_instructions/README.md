# Curriculum Repository — Structure Guide

This repository is the **single source of truth** for the Honors Topics computer science curriculum at Harvard-Westlake. All lesson content, assignments, and course structure live here. Canvas assignments link directly to files in this repo, and the module importer reads this repo to build the course schedule automatically.

---

## Repo structure

The repo uses a two-level hierarchy:

- **Module** — a top-level folder (e.g. `Terminal/`, `ComputerSetup/`) representing a unit of the course
- **Day lesson** — a subfolder inside a module (e.g. `Terminal/Navigation/`) representing one or more class periods

```
Topics/
  ModuleName/
    README.md       — module overview, lesson table, skill building
    LESSONS.md      — machine-readable lesson list for the module importer
    LessonName/
      README.md     — lesson content
      ASSIGNMENT.md — class assignment (optional)
```

Every module folder contains a `README.md` overview page, a `LESSONS.md` for the importer, and one or more day lesson subfolders.

---

## The _ prefix convention

Any folder whose name begins with `_` (such as this one) is **ignored by the module importer** and excluded from all student-facing navigation, table of contents entries, and lesson type labels. Use `_` folders for documentation, templates, or admin files that should never appear in the curriculum.

---

## Adding a new day lesson

To add a lesson to an existing module — for example, adding "Pipe and GREP" to Terminal after the Search lesson:

1. Create the subfolder: `Terminal/PipeAndGREP/`
2. Create `Terminal/PipeAndGREP/README.md` with the lesson content
3. Add a row to `Terminal/LESSONS.md`:

   ```
   | 5 | Pipe and GREP | [PipeAndGREP/](PipeAndGREP/) |
   ```

4. Add a row to the `## Lessons` table in `Terminal/README.md`
5. Add a bullet under the Terminal entry in the root `README.md`:

   ```
   - [Pipe and GREP](Terminal/PipeAndGREP/) — combining commands with pipes and filtering with grep
   ```

If the lesson has a class assignment, also create `Terminal/PipeAndGREP/ASSIGNMENT.md` and add a link to it at the bottom of the lesson `README.md` above the navigation line.

---

## Adding a new module

1. Create a top-level folder: `NewModule/`
2. Create `NewModule/README.md` — the module overview page
3. Create `NewModule/LESSONS.md` — start with the first lesson row
4. Create at least one day lesson subfolder with its own `README.md`
5. Add the module to the root `README.md` under the appropriate lesson type color label

---

## LESSONS.md

Each module folder contains a `LESSONS.md`. This is the file the module importer reads to determine delivery order and build the Canvas course schedule. Keep it in sync whenever lessons are added, removed, or reordered.

Format:

```markdown
# ModuleName — Lesson Plan

| Day | Lesson | Path |
|---|---|---|
| 1 | Navigation | [Navigation/](Navigation/) |
| 2 | Search     | [Search/](Search/)         |
```

- **Day** — delivery order number; use `1-2` for multi-day lessons
- **Lesson** — human-readable name matching the lesson `README.md` title
- **Path** — relative link to the lesson subfolder

---

## ASSIGNMENT.md

Each day lesson folder may contain an `ASSIGNMENT.md` with the class instructions for that session. These files are version-controlled alongside lesson content and will be linked directly from Canvas assignment pages.

When an `ASSIGNMENT.md` exists, add a link at the very bottom of that lesson's `README.md`, placed above the navigation line:

```markdown
[Assignment](ASSIGNMENT.md)

← [Prev Lesson](../PrevLesson/) — Next: [Next Lesson](../NextLesson/)
```

Only add the link when the file actually exists in that folder. Never add a placeholder link.

### review/ folder

Every lesson folder may optionally contain a `review/` subfolder with one `.md` file per reviewable concept:

```
LessonFolder/
  README.md
  ASSIGNMENT.md
  review/
    absolute-vs-relative-paths.md
    what-is-a-shell.md
```

Review files are **composable components**. The module importer can inject one or more into any assignment — at the beginning as a warm-up or at the end as a follow-up — regardless of which lesson or module the review file lives in. A review of "absolute vs relative paths" from Navigation could be prepended to the Files assignment weeks later.

**Review file format:**

```markdown
# Review — [Concept Name or Day Label]

*Originally covered in [Lesson](../README.md)*

---

Terse reference — a table or bullet list of commands/syntax only.
No explanations. Enough to jog memory, not re-teach.

---

## Tasks

1. Concrete action the student performs
2. Builds on the prior step
3. ...
```

Rules:
- **Task-based.** Reviews are exercises the student performs — numbered tasks under `## Tasks`, not "Can you…" checkboxes (those live in Skill Building sections in lesson READMEs).
- **Terse reference only.** The top section is a quick-reference table or bullet list, nothing more. No explanatory prose.
- **Self-contained.** Must make sense when injected into any assignment without surrounding context.
- **Cumulative scope.** Each review covers content up to and including the current lesson, plus all prior lessons in the same module.
- **Progressive complexity in ordered sets.** Day 1 = isolated commands. Day 2 = chained operations. Day 3 = multi-step reasoning.
- **Filename in kebab-case, named for the content.** e.g. `absolute-vs-relative-paths.md`, `branch-and-merge-basics.md`. Only append a number (`-1`, `-2`, ...) when two or more files in the same set genuinely cover the identical topic and must be told apart.
- **Source link required.** Points to the lesson where the content was originally taught.
- **No bottom navigation links.** Fragments, not standalone pages.

### Assignment file format

Every `ASSIGNMENT.md` follows this structure:

```
# Assignment — [Lesson Name]

**Due:** [deadline]

---

## Success Criteria
Checkboxes — each item states explicitly what "done" looks like.

---

## Submission
Specifies what to submit on Canvas (text, screenshot, or both).

### Text response
A copy-paste stencil with labeled fields the student fills in.

### Screenshot
Exact description of what the screenshot must show (and what disqualifies it).
```

When converting old-format assignments from Notion or other sources:
- Rewrite criteria as explicit checkboxes with a one-sentence pass/fail description
- Add a stencil for any text submission fields
- Specify screenshot requirements precisely (what it must show and must NOT show)
- Use `> [!NOTE]` to clarify any ambiguous criteria

---

## Lesson type labels

Every lesson README includes a colored type label in the title block that tells students what kind of lesson they are about to read. There are four labels that use three colors:

| Label | Color | Meaning |
|---|---|---|
| Environment Configuration | Green (`#3fb950`) | Setup guides — gets machines and tools ready |
| Learning | Purple (`#a371f7`) | Introduces new concepts |
| Reinforce | Purple (`#a371f7`) | Builds on concepts through practice |
| Review | Yellow (`#e3b341`) | Revisits and consolidates prior material |

The root `README.md` groups modules by type using a colored `■ Type Name` marker before each group, with a legend table at the top of the Table of Contents.

---

## Lesson README format

Every lesson and module `README.md` follows the same structure:

```markdown
<div align="center">

# Lesson Title
*subtitle in gray*

Type Label in color

</div>

---

[body content]

## Skill Building

### Introductory
- [ ] Can you ...

### Intermediate
- [ ] Can you ...

### Advanced
- [ ] Can you ...

---

[Assignment](ASSIGNMENT.md)    ← only if ASSIGNMENT.md exists

← [Prev Lesson](../Prev/) — Next: [Next Lesson](../Next/)
```

Module overview `README.md` pages also include a numbered `## Lessons` table and a `## Table of Contents` section linking to each lesson.

---

## Canvas and module importer integration

Canvas assignment pages link directly to files in this repo. The URL pattern is:

```
https://github.com/[org]/Topics/tree/main/ModuleName/LessonName/
```

For OS-variant files inside a lesson (e.g. Mac vs PC setup):

```
https://github.com/[org]/Topics/blob/main/ComputerSetup/InitialInstall/Mac.md
```

The module importer reads each `LESSONS.md` to determine lesson order and syncs it with the Canvas course schedule. Keeping `LESSONS.md` accurate is what keeps the Canvas schedule correct.
