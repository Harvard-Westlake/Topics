<div align="center">

# Technical Specification
*<font color="#8b949e">Translate the design into the language programmers build from</font>*

<font color="#a371f7">Learning</font>

</div>

---

Technical specifications detail how a design will be implemented from a technical standpoint. This mainly involves determining the **architecture and environment** it should use, deciding **what classes should represent different parts of the design**, and calling out which parts may not be programmable or are **"out of scope."**

You have spent this whole unit refusing to talk about implementation. Today the ban lifts — but the discipline remains: a tech spec is held to the same standard as the design, just in a different language. Two programmers reading it must build the same thing.

---

## <font color="#388bfd">Key components of a technical specification</font>

| Component | What it covers |
|---|---|
| **Technology Stack** | The programming languages, frameworks, and tools that will be used |
| **Architecture** | How the different parts of the application or game will interact with each other |
| **Data Model** | How data will be stored, retrieved, and managed — with a graphical representation of how classes relate to one another |

**Who writes them:** technical specifications require a deep understanding of technology and programming. They are typically created by software engineers or technical architects, who translate the design into a detailed plan developers can follow to build the product.

> **Tip:**
> For a worked example of the same product described as design and then as specification, revisit the Pac-Man and ATM examples in [Design vs Tech Spec](../Docs/design-vs-tech-spec.md).

---

## <font color="#388bfd">The class-wide TechSpec</font>

For each part of your group's design, plan an implementation in some way:

- Generate a **`TechSpec.md`** covering the key components listed above
- Include an **exported, comprehensive class diagram with dependencies** — built in [Figma](https://www.figma.com/) or [app.diagrams.net](https://app.diagrams.net/)
- **You must know the class structure of your own project** — the diagram is a map of your understanding, not decoration

> **Note:**
> Finished early — and only if your class diagram is complete? Verify the diagram and specifications with your teacher, then start putting priorities on items in the order they are to be programmed.

---

## <font color="#388bfd">Per-feature specs — the folder layout</font>

Each feature you own gets its own branch, and inside it a standard documentation layout:

<pre>
repository/
  documentation/
    TechSpecs/
      <strong><font color="#f0883e">MultiplayerLayout.drawio</font></strong>
      <strong><font color="#f0883e">MultiplayerSpec.md</font></strong>
      ProfileLayout.drawio
      ProfileSpec.md
</pre>

1. Create a folder named `documentation`
2. Inside it, create a folder named `TechSpecs` (short for Technical Specifications)
3. Build a diagram at [app.diagrams.net](https://app.diagrams.net/) with the design layout and relationships of your feature, then download the `.drawio` file and save it with a name suffixed `Layout.drawio` (`MultiplayerLayout.drawio`, `ProfileLayout.drawio`)
4. Create a spec file for your feature with the suffix `Spec.md` (`PlayerControlsSpec.md`, `SoundSpec.md`)

> **Tip:**
> When you start a new diagram, app.diagrams.net offers a **Software** template — it lays out classes and relationships far better than the blank canvas.

---

## <font color="#388bfd">What goes in the diagram</font>

Include all of the following:

- **User or process flows** — for example: *red shell fired → moves along center of track until within 3 ft of a player → collision with player → is it blocked? → yes: shield absorbs the hit → no: player spins out*
- **Class dependencies, variables, and relationships**
- **Color coding** for your pieces — and **include a key** for reference

## <font color="#388bfd">What goes in each Spec.md</font>

For **each** feature, call out **which lines of the design** you are laying out, then describe:

- What **variables** you expect to have for the design to be complete
- What **methods** you expect each object to have
- What **other objects** you expect to relate to that object

---

## <font color="#388bfd">Core first — always</font>

- Start with **CORE features (90% of the work)** — the ones essential for the game/app to be playable or usable
- Core features should be easily distinguishable from non-core features
- Continue with **non-essential features after (10%)** — and make sure *all* the core features are specified before worrying about the secondary ones

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Name the three key components of a technical specification.
- [ ] Recreate the `documentation/TechSpecs/` folder layout and its two file-naming suffixes from memory.
- [ ] State what three things every Spec.md describes (variables, methods, related objects).

### <font color="#79c0ff">Intermediate</font>

- [ ] Draw a process flow for one feature of the class design, decision points included.
- [ ] Explain what "comprehensive class diagram with dependencies" means, and why the dependencies matter.
- [ ] Distinguish a core feature from a non-essential one in the class design, with reasons.

### <font color="#79c0ff">Advanced</font>

- [ ] Take one refined design section and produce its full spec — variables, methods, and relationships — so two programmers would build the same class.
- [ ] Decide what belongs in the class-wide TechSpec.md versus a per-feature Spec.md.
- [ ] Mark something "out of scope" in a spec and justify why it should not be programmed now.

---

[Assignment](ASSIGNMENT.md)

← [Ambiguity and Architecture](../AmbiguityAndArchitecture/) — Next: [Combining Tech Specs](../CombineTechSpecs/)
