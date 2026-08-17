<div align="center">

# Combining Tech Specs
*<font color="#8b949e">Merge every individual spec into one prioritized, color-coded document</font>*

<font color="#a371f7">Reinforce</font>

</div>

---

Today we combine your individual technical specifications into a **single, comprehensive document**. This ensures the project is well-structured and prioritized, making it easier to develop.

**The plan:**

- Form groups, discuss specifications, and prepare to combine files
- Create and populate a single draw.io diagram, organized and **color coded by priority**
- Handle version control, resolve conflicts, and commit the combined file
- Review, finalize, and submit the comprehensive specification **as a class**

---

## <font color="#388bfd">Step 1 — Form groups by highest priority</font>

Group yourselves by the importance of features: **core features first** (essential for the app to be working/playable), non-essential ones much later today. Each group needs at least two people; additional students are assigned as needed.

> **Note:**
> If you are in 2 high-priority groups, choose the one with the **higher** priority. And if your group has more than 3 people, do a **merge sort** of branches — merge in pairs, then merge the merged pairs — instead of a single big branch merge.

---

## <font color="#388bfd">Step 2 — Discuss and agree on structure</font>

- Review each person's technical specification
- Discuss how to implement the design structurally, focusing on **user flows, class dependencies, and relationships**
- Resolve any conflicts between specs to ensure consistency

---

## <font color="#388bfd">Step 3 — Combine the draw.io files</font>

Combine diagrams by dragging and dropping them together in [app.diagrams.net](https://app.diagrams.net/).

> **Tip:**
> If you are merging two **unrelated** systems — say, the UI layout and the API/multiplayer modeling — put them on separate **page tabs** (the tab bar at the bottom-left of the draw.io editor) instead of cramming them into one canvas.

### <font color="#79c0ff">Colorize by priority</font>

| Priority | Color |
|---|---|
| **Core features** | Green |
| **Secondary features** | Yellow |
| **Non-essential features** | Orange / red / purple |

Organize items by priority so the diagram visually shows the build order.

---

## <font color="#388bfd">Step 4 — Manage version control</font>

- Create a Git branch named **`Merge_<FeatureName>`** for each group
- **Cherry-pick** significant commits from individual branches, or merge them — being cautious with draw.io file conflicts, since `.drawio` files are XML and merge badly
- Use communication to avoid concurrent edits — **"soft locking"**: announce who is editing the diagram file, and nobody else touches it until they push

> **Note:**
> Missing a group member because they are in a more important meeting? Start by discussing **their** work, layout, and design; touch base with them to make sure you have their correct branch; then call over a teacher and ask them to explain the design once you have it figured out.

---

## <font color="#388bfd">Once all core features have been reviewed</font>

> **Warning:**
> **STOP once all core features have been merged within their groups.**

Then merge those core groups together **before** moving on to less important items. It is critical to have the core behavior laid out before the smaller, less meaningful parts — those have less impact on the overall structure and should be added into the main design later.

### <font color="#79c0ff">Repeat, with extra steps</font>

The goal: every subsequent less-important feature is combined **into** the more important features. Unless it is a core meeting, each later merge session must start **from the branch with the features you already merged** — if you just came from merging multi-user communication, you bring those items with you into your next topic.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you recite the priority color scheme (green, yellow, orange/red/purple)?
- [ ] Can you state the branch naming convention for merge groups?
- [ ] Can you explain what "soft locking" is and why the group needs it?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain why `.drawio` files are dangerous to merge concurrently, in terms of their file format?
- [ ] Can you decide when two diagrams belong on separate page tabs versus one canvas?
- [ ] Can you explain why core groups must finish merging before any secondary feature is touched?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you run a merge-sort-style combination for a group of four, naming each intermediate branch?
- [ ] Can you cherry-pick a significant commit from a teammate's branch into the group's merge branch?
- [ ] Can you explain why later merge sessions must start from the branch you already merged, and what breaks if you don't?

---

[Assignment](ASSIGNMENT.md)

← [Technical Specification](../TechnicalSpecification/) — Next: [MVP Planning](../MVPPlanning/)
