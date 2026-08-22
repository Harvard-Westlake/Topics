<div align="center">

# Ambiguity and Architecture
*<font color="#8b949e">Eliminate every vague sentence, then research what the product should run on</font>*

<font color="#a371f7">Learning</font>

</div>

---

Today we walk through the design as a class and make sure **everyone has a complete understanding** of the design up until now. Aligning our understanding is critical at this step — the next lessons translate this design into technical documents, and any ambiguity we leave here becomes a bug there.

---

## <font color="#388bfd">The ambiguity standard</font>

A design section is done when it passes this bar:

> **Note:**
> A vague feature must be described well enough that **any 2 random programmers would end up creating the same feature** if they read it. Not similar features — the *same* feature.

This is the [Design Refinement](../DesignRefinement/) detail test, tightened one notch: not just "is it clear?" but "is only one interpretation possible?"

---

## <font color="#388bfd">In class</font>

Break the design into sections. Each person commits to **2 sections** to work on, and does two things:

### <font color="#79c0ff">1. Eliminate ambiguity</font>

Take your section of the design and elaborate it until it is no longer ambiguous — every behavior specified, every edge named, only one interpretation possible.

### <font color="#79c0ff">2. Engine and platform research</font>

Determine a game engine (or platform/framework, for apps) in class. For your elected portion of the infrastructure, research:

- **What the options are** for solving it
- **Pros and cons** of the main options from your research
- **What the solution looks like** — for graphical items like a HUD, produce the actual visual

> **Warning:**
> AI-generated graphics are **not acceptable** as a final submission for UI items. You must manually edit graphics to be exactly as you imagine them. AI can draft; you must direct and finish.

---

## <font color="#388bfd">Branch naming</font>

All work goes in a **new branch** named after the design lines you are elaborating, so it is immediately clear which part of the design you own:

```
Design_Lines_050-104
```

Use the actual line numbers of your section in the design document. Two sections means two branches.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] State the two-random-programmers standard from memory.
- [ ] Explain what the branch name `Design_Lines_050-104` communicates.
- [ ] Name the three things your engine/platform research must contain (options, pros/cons, what the solution looks like).

### <font color="#79c0ff">Intermediate</font>

- [ ] Find an ambiguous sentence in a design and list two different features a programmer could build from it.
- [ ] Compare two engine or platform options with at least two pros and two cons each.
- [ ] Explain why AI-generated graphics are banned as final UI submissions, in terms of design intentionality.

### <font color="#79c0ff">Advanced</font>

- [ ] Rewrite an ambiguous section so only one interpretation survives — and prove it by asking two classmates independently.
- [ ] Recommend an engine for the class project and defend the choice against the strongest alternative.
- [ ] Produce a HUD or UI mock that matches your imagination exactly, editing until it does.

---

[Assignment](ASSIGNMENT.md)

← [UX and Art Direction](../UXAndArtDirection/) — Next: [Technical Specification](../TechnicalSpecification/)
