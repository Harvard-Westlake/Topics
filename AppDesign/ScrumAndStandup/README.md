<div align="center">

# Scrum and Stand-ups
*<font color="#8b949e">Finish the detailed design — and learn the meeting that keeps teams moving</font>*

<font color="#a371f7">Learning</font>

</div>

---

This lesson focuses on refining and detailing the design aspects of the product the class is developing. The design still lacks clarity and specificity in places — item behavior, functionality, and their interrelation. You will work collaboratively to prioritize the design elements that need detail, then individually detail specific parts. And starting next class, every session opens with a **stand-up**.

**Objectives:**

- Understand the importance of clarity and detail in design
- Learn to identify and prioritize high-impact design elements
- Develop detailed design specifications for specific components

---

## <font color="#388bfd">Class structure</font>

### <font color="#79c0ff">1. Review of current design (10 minutes)</font>

Brief overview of the current design and UX work; highlight areas lacking detail and clarity.

### <font color="#79c0ff">2. Critique designs (10 minutes)</font>

Group discussion to identify and prioritize design elements needing further detail; vote or reach consensus on high-priority items.

### <font color="#79c0ff">3. Prioritization session (20 minutes)</font>

Decide the high-priority items and assign each item to an individual.

### <font color="#79c0ff">4. Migration of work back to GitHub</font>

Starting next class, **all work lives in GitHub** — and every class begins with stand-up.

---

## <font color="#388bfd">Worked examples — vague design to detailed design</font>

### <font color="#79c0ff">Example 1: "Clothes will have rarity based on same border colors as faculty"</font>

**Current issue:** the statement is vague — it doesn't specify how clothing rarity works or how it relates to the game's departments.

**Proposed design solution:**

- Introduce 5 types of clothing: shirts, jackets, pants, shoes, sunglasses, hats
- Clothing can be department-specific or neutral, with departmental clothing offering character bonuses
- Introduce rarity levels: **Common** (70% drop rate, no bonus), **Uncommon** (25% drop rate, belongs to a department), **Rare** (5% drop rate, can belong to multiple departments), **Legendary** (0.5% drop rate, 2x department bonus)
- Assign colors to departments for visual representation (e.g., red for Math, orange for Science)
- Clothing is non-tradable, to maintain game balance
- Clothing of a given department has an outline of that department's color; Common has no outline

### <font color="#79c0ff">Example 2: "Players can collect resources from different school areas"</font>

**Current issue:** lacks specifics on the types of resources, their use, and how they are collected.

**How to solve:**

- Define specific resources (e.g., textbooks, lab equipment, art supplies) available in different school areas (e.g., library, science lab, art room)
- Explain what each resource type offers — unique benefits or abilities for the player
- Implement a collection mechanism (e.g., mini-quests, time-based collection)
- Detail which resources can be used to upgrade skills, trade with other players, or complete specific challenges

Notice the pattern: the vague sentence became drop rates, named categories, and explicit rules. That is what "detailed" means.

---

## <font color="#388bfd">Stand-up meetings</font>

Starting next class, we run **stand-up** at the beginning of every class. Each student takes a turn presenting their update — **limited to 1–2 minutes**, enforced with a timer.

A good stand-up update answers three things:

| Question | What it sounds like |
|---|---|
| **What did you work on?** | "I detailed the clothing-rarity section and pushed it to my branch" |
| **Was it communicated clearly?** | Specific nouns and outcomes — not "I did some stuff on the design" |
| **Any blockers?** | "I can't finish resource collection until the map areas are named — I need help from whoever owns that section" |

You are evaluated on sticking to the time limit and the clarity of your communication — and on whether you called out items where you need help from other people.

> **Tip:**
> The blocker call-out is the entire point of stand-up. A team that surfaces blockers daily never loses a week to silent waiting.

---

## <font color="#388bfd">Grading going forward</font>

| Component | Points |
|---|---|
| SCRUM update | 8 |
| Work done during class | 12 |

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Name the three things a good stand-up update contains.
- [ ] State the stand-up time limit and how it is enforced.
- [ ] Recite the going-forward grading split between the SCRUM update and in-class work.

### <font color="#79c0ff">Intermediate</font>

- [ ] Give a 90-second stand-up update about your current design work without rambling.
- [ ] Take the clothing-rarity example and explain what specifically turned it from vague to detailed.
- [ ] Phrase a blocker so the person who can unblock you knows exactly what you need.

### <font color="#79c0ff">Advanced</font>

- [ ] Find the vaguest sentence in the class design and produce a detailed-design solution in the style of the worked examples.
- [ ] Prioritize three underspecified design elements by their impact on the product, and defend the order.
- [ ] Explain why stand-ups are timed, in terms of what long updates cost a team.

---

[Assignment](ASSIGNMENT.md)

← [MVP Planning](../MVPPlanning/) — Back to [App Design and Planning](../)
