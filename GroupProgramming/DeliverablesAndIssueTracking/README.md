<div align="center">

# Deliverables and Issue Tracking
*<font color="#8b949e">Communication beats raw code — track work in issues, ship it in branches, merge it through review</font>*

<font color="#a371f7">Learning</font>

</div>

---

By the end of this lesson, you will be able to:

- Explain what a **deliverable** is
- Track a piece of work with a GitHub **Issue**
- Submit that work in its own **branch** through a **pull request**, reviewed and merged by someone else

> **Warning:**
> Before you begin, your WHOLE TEAM needs a clear, shared understanding of your project layout, its priorities, and the order in which you are going to program. That plan is the design and tech spec you built in [App Design and Planning](../../AppDesign/). If your team does not have this, go back and prepare it properly first.

---

## <font color="#388bfd">Group programming is a team sport</font>

Group programming is equal parts work and communication. A programmer who quietly completes a pile of "working code" without communicating is far **less** useful to a team than one who ships something smaller in a way everyone can understand and build on. Communication is the job.

Two checks tell you whether you are communicating effectively with your work:

- **If you disappeared tomorrow, could a teammate pick up exactly where you left off?**
- **Is your code documented clearly enough that a reader can understand it without you?**

If either answer is no, the code you wrote is trapped inside your head — and code trapped in one person's head is a liability, not an asset.

There are **three steps** to doing work the right way on a team:

1. **Track your work by creating an Issue**
2. **Do the work in its own branch**, submitted with a pull request
3. **Review someone else's work** to verify their code and merge their branch — and get someone to do the same for you

---

## <font color="#388bfd">Step 1 — Issues for tracking</font>

The fundamental unit of communication is an **Issue**: a tracked description of the item you are working on. When you give your daily status, you reference the issue you are working on. Issues are native to GitHub — they can be assigned to specific people, linked to branches and pull requests, and organized on project boards (the same job Jira or a Kanban board does at a company).

Rules for your team:

- Make sure **you** have an issue with **only you** assigned to it
- If two or more people share a feature, make a separate issue for each individual's work, then link those issues to a parent **feature issue**
- When you open a pull request, **link it to the issue** it completes

> **Tip:**
> Open your repository's **Issues** tab on GitHub and keep it open all class. If the board does not reflect what you are actually working on, fix the board — that is part of the work.

---

## <font color="#388bfd">Step 2 — Do the work in a branch</font>

Before you write any code, you should be on a branch. If you (or a small group) are building a specific feature: finish it, test it, and merge work within its own **feature branch** before ever creating a pull request to `main`.

As a general rule, you should only submit to `main` if:

- **A.** You are done with your entire feature and have tested it, **or**
- **B.** Someone else depends on a portion of your feature, so you need to get that part in early

Make sure GitHub shows clean commit messages or a succinct description of what you did.

```
main            ●───────────────────────────────●─────────▶
                 \                             ↑
                  \                   pull request merged
                   \                  by a NON-author who
                    \                 reviewed and tested it
                     \                         |
feature-branch        ●──────●──────●──────────●
                      ^      commits as you work,
                      |      tested on the branch
                      branch created from main
```

---

## <font color="#388bfd">Step 3 — Review and merge</font>

One person is responsible for completing an issue's code, committing it, and merging it into their feature branch (or opening a pull request to `main`). But you are **also** responsible for checking other people's code during your work cycle.

Under **no circumstance** should you believe your code is finished until it has been reviewed and tested by at least one other person.

Keep your issue's status accurate as it moves:

| Status | Meaning |
|---|---|
| **In Progress** | You are actively working on it |
| **In Review** | Code is committed and waiting for a non-author to verify it |
| **Done** | Merged into its parent feature branch, or the pull request into `main` is closed |

> **Warning:**
> People who worked on a feature should **not** merge that feature's pull request into `main` themselves. The merge should be done by a member of another group — that merge is their signature saying "I checked this and it works."

---

## <font color="#388bfd">What counts as a deliverable</font>

Every class you need to *deliver* something. That something is called a **deliverable**.

Suppose you created an issue and, partway through, discovered it is far more work than expected. You still must deliver something — in a branch, with documentation of what you did and what is left. Here is how to deliver partial work honestly:

1. **Split the issue** — one issue for the portion of the work you *did* do, another for the portion still left
2. **Do the work you can in a branch** — commit the portion you completed
3. **Review and merge** — merge code if it will not conflict with the feature branch you are working toward (since the work is split, it is clearly not ready for `main`)

> **Note:**
> Delivering an honest half with a clear record of what remains is real engineering. Delivering nothing — or claiming "it's basically done" with nothing committed — is not.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] List the three steps of doing team work the right way, in order.
- [ ] Create a GitHub Issue, assign yourself to it, and link it to a pull request.
- [ ] Name the three issue statuses and say what each one means.

### <font color="#79c0ff">Intermediate</font>

- [ ] Explain the two checks that tell you whether your work communicates effectively.
- [ ] State the two situations in which it is acceptable to submit work to `main`.
- [ ] Explain why a non-author — ideally from another group — must merge a feature into `main`.

### <font color="#79c0ff">Advanced</font>

- [ ] Walk through delivering an issue that turned out to be too big — splitting it, committing what you finished, and documenting what remains.
- [ ] Set up a parent feature issue with individual child issues for a two-person feature.
- [ ] Argue why a programmer who communicates a small deliverable beats one who silently writes twice as much code.

---

[Assignment](ASSIGNMENT.md)

← Back to [Group Programming](../) — Next: [Sprint Work](../SprintWork/)
