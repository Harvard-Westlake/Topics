# Assignment — Technical Specification

**Due:** Next class

---

Two graded parts: the class-wide technical specification (**Part 1 — 30 pts**) and your two per-feature specifications (**Part 2 — 300 pts: 2 feature branches, 150 pts each**).

## Part 1 — TechSpec.md and class diagram (30 pts)

For each part of your group's design, plan an implementation in some way:

1. Generate a **`TechSpec.md`** including the key components: **Technology Stack**, **Architecture**, and **Data Model**
2. Include an **exported, comprehensive class diagram with dependencies** (built in [Figma](https://www.figma.com/) or [app.diagrams.net](https://app.diagrams.net/))
3. You must know — and be able to explain — the class structure of your own project

## Part 2 — Two feature branches (150 pts each)

Each person commits to **2 different parts of the design** (every part needs at least 2 people; your teacher assigns extras). Beyond design sections, the class must also cover: technical architecture (code structure, engine setup, networking), art and assets, user interface/experience, and audio.

For **each** of your two features, create a **branch**, and in it:

1. Create `documentation/TechSpecs/`
2. Build a diagram at [app.diagrams.net](https://app.diagrams.net/) with the feature's layout and relationships; download the file as `<Feature>Layout.drawio` (e.g. `MultiplayerLayout.drawio`)
3. Create `<Feature>Spec.md` (e.g. `PlayerControlsSpec.md`, `SoundSpec.md`) that calls out **which lines of the design** you are laying out and describes:
   - What **variables** you expect for the design to be complete
   - What **methods** you expect each object to have
   - What **other objects** you expect to relate to each object
4. Include **user or process flows**, **class dependencies**, **color-coded pieces**, and a **key** in the diagram
5. Commit and push the branch

**Start with CORE features (90%)** — the ones essential for the game/app to be playable. Continue with non-essential features (10%) only after all core features are specified.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **TechSpec.md complete** — stack, architecture, and data model all have real content
- [ ] **Class diagram exported and comprehensive** — every class in the project appears, with its dependencies drawn
- [ ] **Two feature branches pushed** — each with `documentation/TechSpecs/` containing a `Layout.drawio` and a `Spec.md`
- [ ] **Specs cite design lines** — each Spec.md names the exact lines of the design it implements
- [ ] **Variables, methods, relationships listed** — for every object in each feature
- [ ] **Diagram is color coded with a key** — a stranger can decode it without asking you
- [ ] **Core before secondary** — all core features are specified before any non-essential work

---

## Submission

Submit **one text response** on Canvas: a commit for each of your feature branches (2 in total).

### Text response

Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Feature 1 branch commit URL:   https://github.com/
Feature 2 branch commit URL:   https://github.com/
Design lines covered (1):      
Design lines covered (2):      
Core or non-essential (each):  
```
