<div align="center">

# MVP Planning
*<font color="#8b949e">Draw the line around the smallest product worth shipping</font>*

<font color="#a371f7">Learning</font>

</div>

---

Your class now owns a comprehensive, prioritized technical specification. It describes far more product than you can build first. Today you decide what gets built **first** — by defining the Minimum Viable Product and ordering its work by dependency.

## <font color="#388bfd">What an MVP is</font>

> **Note:**
> **MVP (Minimum Viable Product):** the **smallest working version** of your product that delivers the **core user value**, runs without breaking, and can be **demonstrated end-to-end**.

All three requirements matter:

| Requirement | Test |
|---|---|
| **Core user value** | A user who tries only the MVP still gets the point of the product |
| **Runs without breaking** | The happy path never crashes |
| **Demonstrable end-to-end** | You can show a complete user journey, start to finish, live |

An MVP is not a demo of one feature, and it is not the full product with bugs. It is a complete — tiny — product.

---

## <font color="#388bfd">Cutting the tech spec down to the MVP line</font>

Your combined spec is already color coded by priority. The MVP line falls almost entirely inside the green:

| Spec color | MVP verdict |
|---|---|
| **Green (core)** | In — this is the MVP's backbone |
| **Yellow (secondary)** | Almost always out — deferred until after the MVP ships |
| **Orange/red/purple (non-essential)** | Out — do not even estimate it yet |

For each green item, ask the brutal question: *if this were missing, could the end-to-end demo still deliver the core value?* If yes, it is not actually MVP — move it below the line. Expect the MVP to feel uncomfortably small. That is correct.

---

## <font color="#388bfd">Ordering by dependency</font>

MVP items cannot be built in arbitrary order — some work is load-bearing for other work. For each item, ask: **what must already exist for this to be buildable and testable?**

A game example:

```
1. Game world renders            (nothing depends on nothing)
2. Player character moves        (needs: world)
3. Resources appear in world     (needs: world)
4. Player collects resources     (needs: player movement + resources)
5. Score displays                (needs: collecting)
```

Item 4 cannot start before items 2 and 3 exist. Writing the order down prevents three people from all starting at item 5.

---

## <font color="#388bfd">The MVP.md file</font>

The deliverable is an **`MVP.md`** file at the root of the class repository:

- An ordered checklist of every MVP item, **sorted by dependency** — each item listing what it needs before it can start
- Each item small enough for one person to make real progress on in one class period
- A clearly marked line: everything below it is **post-MVP**

This file is the bridge into [Group Programming](../../GroupProgramming/), where `MVP.md` drives every sprint: teammates pick the highest-priority unblocked item, build it, and check it off — and the MVP must be demo-ready on `main`.

> **Tip:**
> Write each MVP item as something you could *demonstrate*: "player can collect a resource and see the score change" beats "resource system."

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Define an MVP in one sentence, hitting all three requirements.
- [ ] State which spec colors fall inside the MVP line and which fall outside.
- [ ] Say what file the MVP plan lives in and where in the repository it goes.

### <font color="#79c0ff">Intermediate</font>

- [ ] Apply the "if this were missing, does the demo still deliver core value?" test to a green item and defend the verdict.
- [ ] Order five MVP items by dependency and name what each one needs first.
- [ ] Rewrite a vague item like "resource system" as a demonstrable checklist entry.

### <font color="#79c0ff">Advanced</font>

- [ ] Explain why an MVP that feels uncomfortably small is usually the right size.
- [ ] Spot a dependency cycle in an ordering (A needs B, B needs A) and break it by splitting an item.
- [ ] Explain how MVP.md will drive sprint work in the Group Programming unit.

---

[Assignment](ASSIGNMENT.md)

← [Combining Tech Specs](../CombineTechSpecs/) — Next: [Scrum and Stand-ups](../ScrumAndStandup/)
