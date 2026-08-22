# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is the public student-facing curriculum repository for the **Honors Topics** computer science course at Harvard-Westlake. Student-facing content is Markdown-only, rendered on GitHub. Course-planning tooling (course hub, planner UI, verifier) lives in underscore-prefixed folders and is never student-facing. Teachers collaborate here via branches and change requests reviewed in meetings; students have read access.

No credentials are ever stored in this repo — each teacher keeps their own Canvas token in a gitignored root `.env` (copy `.env.example`). Final exam content lives only in the private sibling `../Admin` repo (along with instructor solutions); the hub reads it cross-repo and only ever pushes date/points placeholders to Canvas.

## Structure

```
Topics/
  <topic-name>/
    README.md           — overview and lesson index for the topic
    <subtopic>/
      README.md         — individual lesson
  _modules/             — curated module JSONs (reusable unit plans) imported by the course hub
  _admin/               — course administration namespace (tooling, config, docs)
    _hub/               — THE course hub: tabbed web app (Courses / Year Schedule /
                          Module Planner / Module Editor / Syllabus),
                          python3 _admin/_hub/server.py → port 5050
    _schedules/         — per-teacher year-plan JSONs edited by the hub's Year Schedule tab;
                          calendars/ holds compressed .ics imports (real class meeting
                          dates/times per block, used instead of the weekday grid when bound)
    _instructions/      — authoring guides for maintaining lessons
    _coursePlannerUI/   — standalone stdlib-only planner (superseded by _hub's Module
                          Planner tab; kept as a credential-free fallback)
    _configuration/     — module.schema.json defining the curated module format
    _lessonplans/       — GENERATED readable summaries of _modules — never edit by hand
    _verification/      — verify.py link/reference checker (also runs in CI on push)
```

Current topics: `ComputerSetup/` (InitialInstall), `Terminal/` (Basics), `GitUsage/` (RepositoriesAndCommits, BranchingAndMerging, ForksAndCollaboration), `GitProject/` (ProjectSetup, InitAndBlobs, Trees, Commits, Branches), `MiniGPT/` (Tokenizer, MarkovBaseline, FixedAttention, TrainableBigram, ObjectNetwork, ScalarAutograd, DenseEngine, SingleHeadAttention, TransformerBlock, TrainingAndGeneration, Capstone), `WebProgramming/` (InterfacingWithAI, WebsiteHosting, JavaScriptAndCursor, DebuggingJavaScript, LearningWidget, PersistenceAndIntermediateWeb, DatabasesAndCollections, UXAndBehaviorTracking, WidgetIteration, PeerReview), `AppDesign/` (LearningToDesign, CommunicatingDesign, DesignChallenge, DesignReview, IterativeDesign, TeamDesignAndPitch, GroupDesignReview, DesignRefinement, MergeDesigns, UXAndArtDirection, AmbiguityAndArchitecture, TechnicalSpecification, CombineTechSpecs, MVPPlanning, ScrumAndStandup), `GroupProgramming/` (DeliverablesAndIssueTracking, SprintWork, MVPAndMergeDiscipline, CodeReviewAndPresentation, IssuesAsWorkRequests, RefactorAndReadme, HelpAClassmate, FinalWrapUp), `HashingCryptoP2P/` (HexadecimalAndHashing, DigitalSignatures, PeerToPeerNetworks), `Blockchains/` (TransactionsAndLedgers, BitcoinAndWallets, MempoolAndWalletProgramming, KeysAndLayerTwo, SmartChainsAndWrappedBitcoin, TokensInJava, ProofOfStake, WritingCodeOnEthereum, VyperCustomBehavior, ERC20Deployment, CryptoResearchProject), `AdvancedEVM/` (WrappedTokensAndLayerTwo, DecentralizedFinance, IPFSAndNFTs, Web2Web3App), `DNDReview/` (DNDReview)

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

## Check for Understanding and Stretch Goals

**Current standard (use for every new or edited lesson).** Every README (both topic indexes and individual lesson pages) must end with a Check for Understanding section placed just above the bottom navigation link. The section header is always `☑️ Check for Understanding` — the old `Skill Building` header is retired and must never come back — and its items are grouped into the three difficulty tiers:

```markdown
## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Plain statement of an action the student can now perform.

### <font color="#79c0ff">Intermediate</font>

- [ ] ...

### <font color="#79c0ff">Advanced</font>

- [ ] ...

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] ...
```

- **Check for Understanding** — one `- [ ]` item per concept taught on the page, phrased as a plain imperative statement ("Create a branch and switch to it."). Never "Can you...?" questions and never an "I can ..." prefix.
- **Tiers** — the three `### <font color="#79c0ff">...</font>` subheaders (Introductory / Intermediate / Advanced) group items by difficulty, in that order.
- **Stretch Goals** — optional section after Check for Understanding: exploration just beyond the curriculum (a related command, tool, or idea a curious student can chase on their own). Not required, not tested, no fixed count.
- Both use plain `- [ ]` checkboxes like every other checklist in this repo (see the `- [ ]` / `- [x]` note under Content Conventions).
- A few recently authored lessons (e.g. `ComputerSetup/InitialInstall`, `GitUsage/RepositoriesAndCommits`) intentionally use a flat, untiered "I can ..." list instead — leave those as they are unless asked.

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

## _ prefix convention

Folders whose names begin with `_` (e.g. `_admin/`, `_modules/`) are **ignored by the module importer** and excluded from all student-facing behaviors: do not add them to the root `README.md` TOC, do not add them to any `LESSONS.md`, do not apply lesson type labels or standard title formatting inside them. They exist for admin, documentation, or tooling only. Non-lesson admin content belongs under `_admin/` (e.g. authoring guides live at `_admin/_instructions/`); the only other top-level underscore folder is `_modules/`, kept at the top level so curated modules are easy to find and update.

## Curated modules and course planning

`_modules/<slug>.json` files are saved unit plans: an ordered selection of lessons (possibly spanning topics) with optional review fragments attached, plus unit number, base points, and scale factor. Format: `_admin/_configuration/module.schema.json`. Review fragments are stored as **references** (`{module, path, file}`), never inline content — the repo's markdown stays the single source of truth and the hub resolves content at import time.

- **The course hub** (`python3 _admin/_hub/server.py` → http://127.0.0.1:5050) is the one UI for everything: the **Module Planner** tab creates/edits `_modules/*.json` (with the same lesson file editor and Canvas-fidelity preview as the standalone planner), the **Year Schedule** tab drags modules/tests/finals onto real class dates (`_admin/_schedules/<teacher>.json`, one file per teacher), and the **Courses** tab talks to Canvas using the teacher's own token from the gitignored root `.env`.
- **Planner lesson rows are drag-reorderable and may interleave topics.** Each row has a `⋮⋮` drag handle; the table order IS the module order, so lessons from different selected topics can be intermixed day by day (with placeholders anywhere). The saved `assignments` array order is authoritative: loading a module rebuilds rows in saved order, appends repo lessons missing from the save unchecked, and reports saved-but-deleted lessons as stale. Adding/removing a topic chip preserves the existing row order and only appends/removes that topic's lessons. Tabs also refresh their repo-derived lists every time they're re-shown (`onShow` in `shell.js`), so topics/lessons created in the Module Editor appear in the Planner and Year Schedule palettes without a page reload.
- **The Module Editor tab** edits the topic folders themselves — the content layer upstream of the Planner. Strict one-way flow: content → curated modules (references) → schedules (references); no tab writes upstream. Clicking a lesson opens everything in it (README, ASSIGNMENT, milestones, activities, reviews, demos, `assets/` uploads) in one workspace, with an impact banner showing which curated modules and schedules reference the lesson (`_scan_usage` in `server.py`). Structural ops (create/rename/delete/reorder lessons, new topics) regenerate every index file server-side (LESSONS.md, topic README table, root README bullets, the CLAUDE.md "Current topics" line, prev/next navs) and rewrite `_modules/*.json` references on rename; deleting a lesson or review file that a curated module still references is refused — detach it in the Planner first. Saving an activity file auto-regenerates its embedded `<details>` toggle in the README (matched by the standalone-file link), so the two intentional duplicates can't drift; creating one inserts the toggle above Check for Understanding, deleting one removes it. The workspace's file tabs are grouped into labeled rows (Lesson / Milestones / Activities / Reviews / Demos / Materials), and the new-review / new-activity dialogs include a one-click "Copy for AI" prompt: the lesson's full text (README + assignment + reviews + activities, from `/api/editor/bundle`) with an intention prompt appended, ready to paste into a chat. Uploads land in the lesson's `assets/` (filenames kebab-cased, extension whitelist) and return a ready-to-paste link snippet; asset deletion is refused while any markdown in the topic still links to the file.
- Saving a module also regenerates `_admin/_lessonplans/<slug>.md`.
- The standalone planner (`python3 _admin/_coursePlannerUI/server.py` → http://127.0.0.1:8901) still works as a stdlib-only, credential-free fallback; its `mdrender.py` must stay in lockstep with the hub's `md_to_html`.
- Year schedules store module **references** (a `_modules` slug or topic folder name) — day counts and lessons re-resolve from the repo on every request, so content edits automatically re-date every teacher's schedule.
- A schedule's `show_day0_syllabus` flag (toggled in the Year Schedule tab) reserves the first class date for a syllabus placeholder — it isn't a `sequence` block, adds no unit number, and has no Canvas sync button; `resolve_schedule` returns its date as `day0_date` and every real block's first day starts on the class meeting after it.
- `_admin/_lessonplans/*.md` are generated — regenerate with `verify.py --fix`, never hand-edit.

### Placeholder ("Additional Day") entries

The Module Planner's lesson table has a hover-revealed insert control above/below every row (`Planner.insertPlaceholder` in `planner.js`) for dropping in an "Additional Day" stub — a day slot with no real lesson yet, to be filled in later. On disk it's an ordinary `assignments` entry with `"placeholder": true` and empty `path`/`_module`:

```json
{ "day": 4, "duration": 1, "title": "Additional Day", "path": "", "_module": "", "placeholder": true }
```

A placeholder may also carry an optional `"kind"` flag (a select on the placeholder row in the Module Planner) controlling what Canvas sync does with it:

- **no `kind`** — plain Additional Day: to be filled with a real lesson later; sync creates nothing.
- **`"kind": "page"`** — in-class day with no homework: sync creates an unpublished Canvas **Page** (titled `unit.day: Title`, linked into the module, containing any attached review plus an "In-class day — no assignment due" note) instead of an assignment. Both sync paths handle it via `create_canvas_page` in `_admin/_hub/server.py`.
- **`"kind": "test"`** — reserved test day: the day still consumes its `unit.day` number (so numbering stays consistent for a manually placed test) but sync creates nothing.

- Lesson-existence checks (`verify.py`'s `check_modules`, the hub's and standalone planner's `validate_module`) skip a placeholder's `path`/`_module`, but still validate its `review` reference if it has one.
- `generate_lessonplan` renders its Source cell as *placeholder — not yet filled in* instead of a broken link.
- Year Schedule resolution (`expand_module_block`) needs no special case — it already builds a slot from whatever `title`/`day`/`duration` an assignment carries.
- Canvas assignment creation must skip placeholders rather than create an empty assignment for them — both `api_create_module` (guards on `a.get("placeholder")`) and the Year Schedule's `api_schedule_sync_block` (guards on the slot's lesson having an empty `path`/`_module`, since that loop's slots don't carry the flag itself).
- The standalone planner's UI doesn't render placeholders at all; its save handler merges any forward from the prior save so they aren't silently dropped, but editing them (renaming, reordering, deleting) currently only works from the hub's Module Planner.
- Inserting or removing a placeholder renumbers every `day` in that module sequentially from array order — an explicit, opt-in action, not something that happens on a plain load/save.

## Verification

After ANY content, structure, or module change, run:

```bash
python3 _admin/_verification/verify.py        # exit 1 on errors
python3 _admin/_verification/verify.py --fix  # also regenerate _admin/_lessonplans/
```

It checks every relative link in every `.md`, topic/lesson structure (LESSONS.md ↔ folders, Check for Understanding sections, ASSIGNMENT.md links), root README coverage, and `_modules/*.json` referential integrity (lessons, review files, title drift, lesson-plan sync). CI runs it on every push via `.github/workflows/verify.yml` — do not leave the repo in a state where it fails.

## Module and day-lesson structure

Each top-level subfolder (e.g. `Terminal/`, `ComputerSetup/`) is a **module**. Each interior subfolder is a **day lesson** — one or more class periods of content. A lesson folder always contains a `README.md` and optionally an `ASSIGNMENT.md`.

Lesson folders may also contain sibling `.md` files instead of further nested subfolders when content naturally splits by variant (e.g. `InitialInstall/Mac.md` and `InitialInstall/PC.md`). In this pattern, the lesson's `README.md` links to those files rather than to sub-subfolders.

**When adding a new day lesson to a module** (e.g. "add a PipeAndGREP day to Terminal"):
1. Create `Terminal/PipeAndGREP/` with a `README.md`
2. Add a row to `Terminal/LESSONS.md`
3. Add a row to the `## Lessons` table in `Terminal/README.md`
4. Add a subtopic bullet to the `Terminal` entry in the root `README.md`

## LESSONS.md

Every module folder contains a `LESSONS.md` listing day lessons in delivery order. It is used by the module importer to build the course schedule.

Format:

```markdown
# [Module Name] — Lesson Plan

| Day | Lesson | Path |
|---|---|---|
| 1 | Lesson Name | [FolderName/](FolderName/) |
```

Column definitions:
- **Day** — lesson number in delivery order; use `1-2` for multi-day lessons
- **Lesson** — human-readable name matching the lesson folder's `README.md` title
- **Path** — relative link to the lesson subfolder

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

## Table of Contents (in-page navigation)

When a README, a variant file (e.g. `Mac.md`/`PC.md`), or an `ASSIGNMENT.md` is long enough to need in-page navigation, add a numbered Table of Contents right after the intro paragraph (or right after the title block for `ASSIGNMENT.md`):

```markdown
## <font color="#388bfd">Table of Contents</font>

1. [Descriptive link text that stands alone](#anchor-slug)
2. [Another descriptive link](#anchor-slug)
```

Rules:
- **Numbered, not bulleted or bold-linked** — the numbering matches the order sections appear in the page.
- **The link text alone must say what the section covers.** Do not add a second line of prose under the link — fold that sentence into the link text itself, e.g. `1. [Install Homebrew, the macOS package manager](#4-homebrew)`, not `**[Homebrew](#4-homebrew)**` followed by a description line on the next line.
- Anchors are GitHub's auto-generated heading slugs: lowercase, spaces become hyphens, punctuation is stripped.

## ASSIGNMENT.md files

Any lesson subfolder may contain an optional `ASSIGNMENT.md` with the class instructions for that session. These will eventually be linked from Canvas assignments on the course hub, which will point directly to these files.

When an `ASSIGNMENT.md` exists in the same folder as a `README.md`, the README must link to it at the very bottom, placed **above** the bottom navigation line:

```markdown
[Assignment](ASSIGNMENT.md)

← [Prev](../Prev/) — Next: [Next](../Next/)
```

Never add a placeholder link if no `ASSIGNMENT.md` exists — only include it when the file is actually present in that folder.

### review/ folder

Every lesson folder may contain a `review/` subfolder. Inside it, any number of `.md` files can exist — one per concept being reviewed. These files are **composable review components**: the module importer can inject one or more of them at the beginning or end of any assignment, in any module, not just the one they live in.

```
LessonFolder/
  README.md
  ASSIGNMENT.md        (optional)
  review/
    concept-name.md    (one file per reviewable concept)
    another-concept.md
```

**review file format:**

```markdown
# Review — [Concept Name]

*Originally covered in [Lesson](../README.md)*

---

[Terse reference — a table or bullet list of commands/syntax only. No explanations. Jog memory, do not re-teach.]

---

## Tasks

1. [Concrete action the student performs]
2. [Next action — builds on the prior one]
```

Rules for review files:
- **Task-based, not checkbox-based.** Reviews are exercises the student performs, not self-assessments. Use a numbered `## Tasks` list, not "I can…" checkboxes (those belong in Check for Understanding sections).
- **Terse reference only.** The top section must fit in a table or a few bullet points. If you find yourself writing a sentence of explanation, stop — that belongs in the lesson README.
- **Self-contained.** Must make sense when inserted into any other assignment with no surrounding context.
- **Cumulative scope.** Each review file covers content up to and including the current lesson, plus any earlier lessons in the same module.
- **Progressive complexity within a set.** When creating multiple review files for one lesson, each should be harder than the last — Day 1 tests isolated commands, Day 2 chains them, Day 3 requires multi-step reasoning.
- **Name files descriptively in kebab-case, after what the review covers** — not after its position in a sequence. e.g. `absolute-vs-relative-paths.md`, `branch-and-merge-basics.md`. Only append a number (`-1`, `-2`, ...) when two or more files in the same set cover the identical topic and must be distinguished.
- **Source link is required.** Points back to the lesson where the content was originally taught.
- **No navigation links at the bottom.** These are fragments, not standalone pages.

### ASSIGNMENT.md format

Every assignment file follows this structure:

```markdown
# Assignment — [Lesson Name]

*Lesson: [Lesson Name](README.md)*

**Due:** [due date or relative deadline]

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Item** — one-sentence description of what "done" looks like
- [ ] **Item** — ...

---

## Submission

Submit **[text / screenshot / both]** on Canvas.

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

\`\`\`
Field label:   value
Field label:   value
\`\`\`

### Screenshot

[Description of what the screenshot must show and what it must NOT show]
```

When converting old-format assignments (pasted from Notion or elsewhere), always:
1. Rewrite success criteria as explicit checkboxes with a one-sentence pass/fail description
2. Add a Submission section with a copy-paste stencil for any text fields
3. Specify exactly what the screenshot must show (and what disqualifies it)
4. Clarify any ambiguous criteria with a `> [!NOTE]` callout

The `*Lesson: [Lesson Name](README.md)*` line is required on every ASSIGNMENT.md — it's how a student looks up the day's context from inside Canvas. When the hub pushes this assignment to Canvas, it also automatically prepends a collapsible "View the lesson for this assignment" block with the full rendered README (see `_lesson_readme_html` in `_admin/_hub/server.py`) — that's pipeline behavior, not something to hand-author. Milestone files (`milestones/gp-X-N.md`) don't need their own lesson link — they already link to their parent ASSIGNMENT.md, which links to the lesson.

## Content conventions

- All lessons are GitHub-rendered Markdown — write for GitHub's renderer, not a local previewer.
- Use bold-label blockquotes for key asides: `> **Note:** text`, `> **Tip:** text`, `> **Warning:** text`. Do not use the `> [!NOTE]` GitHub alert syntax — it does not render correctly in this repo's context.
- Use fenced code blocks with `bash` syntax highlighting for all terminal commands.
- Each subtopic README ends with `← prev — Next: next` navigation links using relative paths.
- No emojis in body text, with three fixed exceptions that are structural markers, not decoration: the `👉 **Activity Break:**` callout (see "activities/ folders"), and the `☑️`/`🚀` prefixes on the Check for Understanding / Stretch Goals headers (see above). No frontmatter. No HTML unless Markdown genuinely can't express it.
- Audience: high school students new to CS. Be precise, not condescending.
- Keep writing `- [ ]` / `- [x]` for every checkbox (Check for Understanding, Stretch Goals, Success Criteria) — GitHub renders these as real checkboxes natively, and the hub/planner renderer rewrites the same markers into actual `<input type="checkbox" disabled>` elements before conversion, so they also render as checkboxes in the Canvas-fidelity preview and on Canvas itself (see `_TASKLIST_RE` in `_admin/_hub/server.py` and `_admin/_coursePlannerUI/mdrender.py`). Never hand-write `<input>` checkboxes in content — the renderer already does it.

## Starter-code conventions

Applies to every file under a lesson's `starter/` folder, in any language — students read this code as teaching material, so every name carries meaning:

- **No single-letter identifiers.** Never `i`/`j`/`k`/`d`/`t`/`p` — name every loop index and local for the thing it enumerates or holds: `queryPosition`, `keyPosition`, `slot`, `slotsPerCard`, `currentToken`, `nextToken`, `position`, `mergeNumber`, `flashcardStart`, `entry`. Meaning-free math locals in provided helpers still get full words (`sum`, `max`, `total`).
- **Parameters say what they hold, not just their shape.** `double[][] statCards`, never `double[][] sequence`; `queryCard, keyCard`, never `left, right`; `attentionWeights`, never `weights`. If a student would ask "a sequence of *what*?", the name is wrong.
- **Use the lesson's own vocabulary in names** (query/key/value, stat card, slot, flashcard, logit) so the code and the prose teach the same words. Validator error messages speak the same language.
- **Every TODO comment opens with a motivator**: a plain-language "The question: …" / "The answer: …" pair (no jargon), then a `Dimensions:` block naming each input and output, the per-element rule, and a worked example using the lesson's exact machine-verified numbers.
- **When one artifact is built several ways across a lesson** (e.g. the attention matrix's three fillings), tag each TODO with its place in that progression and mark shared machinery as shared — the segmentation in code must mirror the lesson page.

## Multi-day assignments

When an assignment spans more than one class period, add a `**Duration:**` field on the line immediately after the title, before `**Due:**`:

```markdown
# Assignment — [Lesson Name]

**Duration:** 3 class periods  
**Due:** [due date or relative deadline]
```

In `LESSONS.md`, show the day range in the Day column using an en dash:

```markdown
| Day | Lesson | Path |
|---|---|---|
| 2–4 | Lesson Name | [FolderName/](FolderName/) |
```

Single-day lessons omit the `**Duration:**` field entirely and use a single number in the Day column.

---

## milestones/ subfolder

When an assignment contains multiple distinct milestones (typically multi-day work), split it into a menu-plus-subfiles structure rather than one long file.

**Folder layout:**
```
LessonName/
  ASSIGNMENT.md            — menu only (links to docs + each milestone)
  milestones/
    gp-X-1.md              — one file per milestone
    gp-X-2.md
    gp-X-3.md
```

**`ASSIGNMENT.md` menu format:**
```markdown
# Assignment — [Lesson Name]

*Lesson: [Lesson Name](README.md)*

**Duration:** N class periods
**Due:** [due date]

---

## Reference Documentation

| Doc | Read before |
|---|---|
| [Doc Name](../Docs/doc-name.md) | Starting this assignment |

---

## Milestones

| Milestone | Description |
|---|---|
| [GP-X.1](milestones/gp-X-1.md) | One-line description |
| [GP-X.2](milestones/gp-X-2.md) | One-line description |

---

## Success Criteria

- [ ] **Item** — what "done" looks like overall
```

**Individual milestone file format:**
```markdown
# GP-X.N — Milestone Title

*Part of the [LessonName](../ASSIGNMENT.md) assignment*

---

## Recall   (optional — brief refresher linking to relevant Docs)

## Instructions

[Numbered steps]

---

**Commit summary:** `(GP-X.N): Short Description`

---

← [GP-X.prev](gp-X-prev.md) — [Back to assignment](../ASSIGNMENT.md) — Next: [GP-X.next](gp-X-next.md) →
```

Rules:
- **ASSIGNMENT.md becomes a menu**, not the full assignment. Move all milestone content into subfiles.
- Each milestone file is **self-contained** — it must make sense without the surrounding assignment.
- Include a **Recall** section only when the student needs a quick pointer to prior content or reference docs.
- The milestone file nav links follow the same first/middle/last pattern as lesson bottom navs, replacing prev/next with the adjacent milestone files.
- **No Check for Understanding / Stretch Goals section** in milestone files — those belong in the lesson README only.

**When adding milestone files to an existing lesson (Common Operations checklist):**
1. Create `LessonName/milestones/` folder
2. Create `milestones/gp-X-N.md` for each milestone
3. Rewrite `LessonName/ASSIGNMENT.md` as a menu (links to docs + milestones table + overall success criteria)

---

## Docs/ folders

A module may contain a `Docs/` folder for standalone reference documentation — conceptual explanations, data format specs, or key concept summaries that students consult throughout the module. These are not day lessons.

Rules for `Docs/` folders:
- **Not added to `LESSONS.md`** — it is not a day lesson
- **Not listed as a subtopic bullet in the root `README.md`** — it is not a course topic
- **Linked from the module `README.md`** under a "Reference Documentation" section or table
- **Linked from individual lesson READMEs** as relevant
- The index file inside `Docs/` is named **`README.md`** (GitHub renders it automatically when browsing the folder)
- Individual doc files use lowercase kebab-case: `blobs.md`, `index-file.md`
- Doc files follow the standard title format (centered `<div>` block with `#` title and italic subtitle) but have **no lesson type label**, **no Check for Understanding section**, and **no bottom nav** — only a simple `← Back to [Docs](README.md)` link
- Doc files use the same `##` / `###` color scheme as lesson pages

**When adding a new module with reference documentation:**
1. Create `ModuleName/Docs/README.md` — index of all docs in the folder
2. Create individual doc files: `ModuleName/Docs/concept-name.md`
3. Add a "Reference Documentation" table to `ModuleName/README.md` linking each doc file
4. Do NOT add `Docs/` to `LESSONS.md` or the root `README.md`

---

## demos/ folders (standalone HTML pages)

A lesson folder may contain a `demos/` subfolder holding standalone interactive HTML pages used for in-class demonstration — visualizers, calculators, activity tools. **The committed file in this repo is the source of truth**; never maintain a copy elsewhere that can drift.

Rules for `demos/` folders:

- **One self-contained file per demo.** A complete HTML document (`<!doctype html>` through `</html>`) with all CSS and JavaScript inline. No external requests of any kind: no CDNs, no webfonts, no analytics, and no data leaving the page (classroom inputs stay in the browser).
- **Naming:** lowercase kebab-case, e.g. `demos/spotlight-bench.html`.
- **Viewing:** GitHub shows `.html` files as source only. The rendered page is served by **GitHub Pages** at `https://harvard-westlake.github.io/Topics/<Module>/<Lesson>/demos/<name>.html`. One-time setup (repo admin): Settings → Pages → Deploy from a branch → `main`, `/ (root)`. Pages serves whatever is on `main`, so a demo goes live on push.
- **Pages serves files verbatim — never rendered markdown.** The root `.nojekyll` file disables Jekyll on purpose: Jekyll's kramdown cannot process markdown inside the `<div align="center">` title blocks (headers rendered as literal `# Topics *…*`), and Liquid can break builds on brace-heavy code. Do not delete `.nojekyll`, and never link students to a `.md` file on the Pages domain — lessons are read on github.com, which is the only renderer the markdown targets. The root `index.html` redirects Pages visitors to the GitHub repo.
- **Linking from the lesson README** — always link both the live page and the source, in this format:

  ```markdown
  [The Spotlight Bench](https://harvard-westlake.github.io/Topics/MiniGPT/FixedAttention/demos/spotlight-bench.html) ([source](demos/spotlight-bench.html))
  ```

- `demos/` is never added to `LESSONS.md`, the root `README.md`, or module JSONs — demos are lesson support material, like `review/`.
- Demos must be usable by keyboard and render correctly in both light and dark system themes.
- The planner UI lists `demos/*.html` as tabs in the lesson file editor and renders them live (demo tabs open directly into Live Preview, an embedded frame showing the current buffer), so demos are viewable and editable inside the UI alongside the lesson's markdown.

---

## assets/ folders (images and other embedded media)

Any lesson folder, or `Docs/` folder, that embeds images (diagrams, screenshots, figures) holds them in an `assets/` subfolder rather than loose beside the `.md` file.

Rules for `assets/` folders:

- **Naming:** lowercase kebab-case, matching the concept it depicts, e.g. `assets/blob-example.png`, `assets/attention-matrix.png`.
- **Referencing:** link with a relative path and a full descriptive alt text — the alt text is the only version of the image many students effectively read, so describe what it shows, not just its filename: `![Alt text describing the figure](assets/blob-example.png)`.
- **One `assets/` folder per lesson (or per `Docs/` folder)** — do not create nested subfolders inside it or share an `assets/` folder across lessons.
- **Prefer PNG/SVG** for diagrams and screenshots; keep files reasonably sized (compress before committing) since GitHub renders them inline in the lesson page.
- `assets/` is never added to `LESSONS.md`, the root `README.md`, or module JSONs — it is lesson support material, like `review/` and `demos/`.
- This is distinct from `demos/`: `demos/` holds standalone interactive HTML pages served by GitHub Pages; `assets/` holds static media embedded directly in markdown via `![]()`. A diagram that is a static export of a demo (e.g. a frozen screenshot) still lives in `assets/`, not `demos/`.

---

## activities/ folders (in-lesson engagement exercises)

**Current standard for every new or edited lesson.** Every lesson's `README.md` must weave short, hands-on activities directly into its lecture — right after the section that introduces a concept, not saved up for homework — so students prove each idea to themselves before moving on. The activities themselves live as separate files in an `activities/` subfolder.

```
LessonFolder/
  README.md
  ASSIGNMENT.md        (optional — this is separate from activities; see below)
  activities/
    01-descriptive-name.md    (one file per activity, numbered in README order)
    02-descriptive-name.md
```

**Activity file format:**

```markdown
# Activity — [Title]

*Concept: [one sentence naming the idea this activity proves]*

## Task

1. [Concrete, numbered step]
2. [Next step — builds on the prior one]
```

**Weaving into the README:** immediately after the section whose concept the activity reinforces, embed the activity as a collapsed, togglable `<details>` block — not just a link — so a student can do it inline without leaving the page:

```markdown
👉 <details>
<summary><h3>Activity: [Title] — click to expand</h3></summary>

*Concept: [one sentence naming the idea this activity proves]*

## Task

1. [Concrete, numbered step]
2. [Next step — builds on the prior one]

*(Standalone file: [activities/01-descriptive-name.md](activities/01-descriptive-name.md))*

</details>
```

The `<details>` body is a **full, byte-for-byte duplicate** of the activity file's content (everything below its own `# Activity — [Title]` line) — GitHub markdown has no way to transclude another file, so this is the only way to get an inline toggle. This means every activity's content is intentionally maintained in two places; when you edit one, edit the other to match.

Rules:
- **Naming:** the activity file is numbered (`01-`, `02-`, ...) matching the order activities appear in the README, then a short kebab-case description, e.g. `activities/02-clone-vs-zip-challenge.md`. The embedded toggle's summary is always `Activity: [Title]`, where `[Title]` is that same activity's title **before** it was turned into the kebab-case filename (e.g. file `02-clone-vs-zip-challenge.md` ↔ summary `Activity: Clone vs. ZIP Challenge`) — this is the fixed, mechanical link between a toggle you see in the README and the file it lives in, so anyone can find one from the other.
- **Activity headers are always large.** The toggle's summary text is wrapped in `<h3>` (as in the template above), never plain bold — activity headers must render larger than body text so they stand out while scrolling a lesson. The hub's Module Editor writes and re-syncs toggles in this format automatically (`_activity_toggle` in `_admin/_hub/server.py`).
- **One concept per activity.** Keep each one short enough to do in a few minutes without breaking lecture flow.
- **Self-contained task steps.** A student should be able to follow the numbered steps without leaving the toggle (or the standalone file) for more instructions.
- **A blank line must follow `<summary>...</summary>`** — GitHub only renders the markdown inside an HTML block (headers, lists, code fences) when a blank line separates it from the opening tag; skip it and the whole body renders as literal text.
- **Not added to `LESSONS.md`, the root `README.md`, or module JSONs** — like `review/`, `demos/`, and `assets/`, this is lesson support material.
- **Distinct from `ASSIGNMENT.md`:** activities are in-lecture engagement/comprehension checks completed as you read; `ASSIGNMENT.md` is the graded homework due after class. A lesson can have both, neither, or just one.
- **Always include the "Standalone file" link** shown in the template above, inside the toggle. It's not just a courtesy — it's the one real markdown link connecting the embed back to `activities/*.md`, so `verify.py`'s link checker still confirms the file exists.

---

## Common Operations

These checklists are the authoritative source for keeping the repo consistent. Every item is required unless marked optional. **Finish every operation by running `python3 _admin/_verification/verify.py`** — it catches broken links, missing index rows, and stale module references.

### Add a new module

A module is a new top-level folder (e.g. `Python/`, `DataStructures/`).

**Create:**
1. `ModuleName/README.md` — centered title block + type label + one-paragraph intro + TOC linking to each lesson + Lessons table at bottom
2. `ModuleName/LESSONS.md` — machine-readable lesson index
3. For each day lesson inside it: see **Add a lesson to an existing module** below

**Update:**
4. Root `README.md` — add a bold linked entry under the correct `■ Type Label` group (create the group if the type is new); include one-sentence summary and a subtopic bullet per lesson
5. `CLAUDE.md` — add the new module to the "Current topics:" line with its lessons in parentheses

---

### Add a lesson to an existing module

A lesson is a new subfolder inside a module (e.g. `Terminal/PipeAndGREP/`).

**Create:**
1. `ModuleName/LessonName/README.md` — centered title block + type label + all lesson content woven with `👉 Activity Break` callouts + Check for Understanding / Stretch Goals sections + bottom nav
2. `ModuleName/LessonName/activities/` — one numbered file per activity break referenced from the README; see **activities/ folders**
3. `ModuleName/LessonName/ASSIGNMENT.md` — optional; if present, add `[Assignment](ASSIGNMENT.md)` link above the nav line in the README
4. `ModuleName/LessonName/review/` — optional; see **Add review files** below

**Update:**
5. `ModuleName/LESSONS.md` — add a row for the new lesson
6. `ModuleName/README.md` — add a row to the Lessons table; if the module README has a TOC, add an entry there too
7. Root `README.md` — add a subtopic bullet under the module's entry
8. `CLAUDE.md` — add the new lesson name to the module's parenthetical in "Current topics:"
9. Previous lesson's README — update its bottom nav to add `Next: [NewLesson](../NewLesson/)`
10. New lesson's README bottom nav — add `← [PrevLesson](../PrevLesson/)` on the left side

---

### Add review files to a lesson

Review files are composable fragments in `LessonFolder/review/`. The module importer picks them up automatically — no index changes are needed.

**Create:**
1. `LessonFolder/review/descriptive-name.md` — named for what it covers, e.g. `branch-and-merge-basics.md` (add a `-N` suffix only when two files in the set cover the identical topic)
   - Title: `# Review — [Concept Name]`
   - Source link: `*Originally covered in [Lesson Title](../README.md)*`
   - Terse reference table (commands/syntax only — no explanations)
   - `## Tasks` numbered list (concrete actions, not "Can you…" checkboxes)
   - Cumulative scope: cover content up to and including this lesson plus all prior lessons in the module
   - Progressive complexity: each file in a set must be harder than the last

**No other files need updating.**

---

### Add a media asset to a lesson

1. Place the image in `LessonFolder/assets/` (create the folder if it doesn't exist yet), named descriptively in kebab-case
2. Embed it in the relevant `.md` file with `![Descriptive alt text](assets/file-name.png)`

**No other files need updating.**

---

### Rename a lesson folder

1. `mv ModuleName/OldName/ ModuleName/NewName/` (bash)
2. `ModuleName/LESSONS.md` — update the Path cell for that row; update the Lesson name if it changed
3. `ModuleName/README.md` — update the Lessons table link and label; update any TOC entry
4. Root `README.md` — update the subtopic bullet link and label
5. `CLAUDE.md` — update the lesson name in "Current topics:"
6. Previous lesson's README bottom nav — update its `Next:` link to `NewName/`
7. Next lesson's README bottom nav — update its `←` link to `NewName/`
8. Any review files in sibling lessons that link back to this lesson (source links) — update the path and label

---

### Rename a module

1. `mv OldModule/ NewModule/` (bash)
2. Root `README.md` — update the bold linked entry path and all subtopic bullet paths
3. `CLAUDE.md` — update the module name in "Current topics:"
4. Any review files in other modules that link back to a lesson in this module — scan with `grep -r "OldModule"` and update paths

---

### Edit lesson content (no rename)

When updating content inside an existing lesson:

- **New commands or concepts added:** add or update Check for Understanding items to test them, and consider whether a new `activities/` exercise would reinforce it in-lecture; add the commands to any existing review files that cover this lesson
- **Commands or concepts removed:** remove them from Check for Understanding (and delete any activity that exercised them); update or remove the corresponding review file tasks; update the source link label in any review files that referenced the removed content
- **ASSIGNMENT.md criteria change:** update the Success Criteria checkboxes; update the submission stencil if new fields are needed
- **Section renamed within a README:** search for anchor links (`#section-name`) in the same file's TOC and in any review files — update them

---

### Navigation link format reference

Bottom nav lines use this pattern. Adapt based on position in the module:

```markdown
← [Prev Lesson](../PrevLesson/) — Next: [Next Lesson](../NextLesson/)
```

First lesson in a module (no prev):
```markdown
← Back to [Module Name](../) — Next: [NextLesson](../NextLesson/)
```

Last lesson in a module (no next):
```markdown
← [PrevLesson](../PrevLesson/) — Back to [Module Name](../)
```

When an `ASSIGNMENT.md` is present, the assignment link goes on the line immediately above the nav line with a blank line between them:
```markdown
[Assignment](ASSIGNMENT.md)

← [Prev](../Prev/) — Next: [Next](../Next/)
```
