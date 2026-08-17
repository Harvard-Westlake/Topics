<div align="center">

# App Design and Planning
*<font color="#8b949e">Design for users first, agree as a team, then plan the build</font>*

<font color="#a371f7">Learning</font>

</div>

---

Every product you have ever loved was designed before it was built. Someone decided what it should *do for people* — how it should feel, what makes it worth opening twice — long before anyone chose a programming language. This unit teaches you to walk that same path: the path a real product team walks.

The journey has three acts:

1. **Design for users.** You will learn to describe what a product does entirely in terms of user value, behavior, and experience — and to notice the exact moment a conversation slips from *design* into *implementation*. You will brainstorm, pitch, defend, review, and iterate on ideas, first alone and then in teams, until the whole class converges on a single design worth building.
2. **Translate design into a technical specification.** Once the design is settled, you will switch languages: classes, variables, methods, relationships, diagrams. A good tech spec is so unambiguous that two programmers who have never spoken would build the same feature from it.
3. **Plan the build.** You will draw the line around a Minimum Viable Product, order the work by dependency, and practice the stand-up meetings that keep a team moving.

The design your class produces here is not a throwaway exercise — it becomes the project the class actually builds in [Group Programming](../GroupProgramming/). Every hour of clarity you invest now is an hour of confusion you spare your future teammates.

> **Note:**
> This unit leans constantly on branches, commits, and pull requests. If those feel rusty, revisit [Git Usage](../GitUsage/) before you start.

---

## <font color="#388bfd">Two documents, two languages</font>

The single most important distinction in this unit:

| | Design document | Technical specification |
|---|---|---|
| **Audience** | Anyone — users, investors, teammates | Programmers |
| **Subject** | What the product does and why users care | How the product will be built |
| **Vocabulary** | Behaviors, experience, value, feel | Classes, variables, methods, architecture |
| **Example** | "Eating a power pellet makes the ghosts flee" | "`Ghost.setState(FRIGHTENED)` runs a 10-second timer" |

Mixing these two languages is the most common design mistake beginners make. By the end of this unit, you will catch it instantly — in your own writing and in everyone else's.

---

## <font color="#388bfd">Reference Documentation</font>

Consult these throughout the unit:

| Doc | Read before | What it covers |
|---|---|---|
| [Design vs Tech Spec](Docs/design-vs-tech-spec.md) | Day 1 | Side-by-side Pac-Man and ATM examples of design language vs specification language |
| [Design Communication](Docs/design-communication.md) | Day 5 | How to critique a design without critiquing the designer — with good and bad phrasing |
| [Game Dev Jobs](Docs/game-dev-jobs.md) | Day 13 | The roles on a real development team, from producer to localization specialist |

---

## <font color="#388bfd">Lessons</font>

| Day | Lesson | What you'll learn |
|---|---|---|
| 1 | [Learning to Design](LearningToDesign/) | Describe a partner's game in plain language, then separate design from technical specification |
| 2 | [Communicating Design](CommunicatingDesign/) | Brainstorm and pitch an idea in terms of user value, with zero implementation talk |
| 3–4 | [The Design Challenge](DesignChallenge/) | Design a school-scale app or game against real business requirements |
| 5 | [Design Review](DesignReview/) | Review a partner's design in a branch without sliding into implementation |
| 6 | [Iterative Design](IterativeDesign/) | Define "better," then improve a chosen design with meaningful commits |
| 7 | [Team Design and Pitch](TeamDesignAndPitch/) | Present to a team and integrate the best ideas into one cohesive design |
| 8 | [Group Design Review](GroupDesignReview/) | Open pull requests on the three designs you back the most |
| 9–11 | [Design Refinement](DesignRefinement/) | Walk every idea in small groups until the design passes the detail test |
| 12 | [Merging Designs](MergeDesigns/) | Combine the class's designs pairwise using a structured conversation protocol |
| 13 | [UX and Art Direction](UXAndArtDirection/) | Choose a track: user flows and wireframes, or mood boards and art assets |
| 14 | [Ambiguity and Architecture](AmbiguityAndArchitecture/) | Eliminate ambiguity from the design and research engines and platforms |
| 15 | [Technical Specification](TechnicalSpecification/) | Translate the design into a tech spec with class diagrams and per-feature specs |
| 16 | [Combining Tech Specs](CombineTechSpecs/) | Merge individual specs into one prioritized, color-coded document |
| 17 | [MVP Planning](MVPPlanning/) | Draw the MVP line through the tech spec and order the work by dependency |
| 18 | [Scrum and Stand-ups](ScrumAndStandup/) | Complete the detailed design and run timed stand-up updates |

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you name the three acts of this unit — design for users, translate to a tech spec, plan the build?
- [ ] Can you state who the audience of a design document is, and who the audience of a technical specification is?
- [ ] Can you give one example sentence of design language and one of specification language?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain why the design phase deliberately excludes implementation, feasibility, and technical requirements?
- [ ] Can you describe how the class's many individual designs become one shared design over the course of the unit?
- [ ] Can you explain what happens to this unit's final design in the Group Programming unit?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you take any product feature you know and describe it twice — once purely as design, once purely as specification?
- [ ] Can you explain why a tech spec must be unambiguous enough that two strangers would build the same feature from it?
- [ ] Can you argue why an hour spent on design clarity saves more than an hour of programming time later?
