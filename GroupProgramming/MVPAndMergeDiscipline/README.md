<div align="center">

# MVP and Merge Discipline
*<font color="#8b949e">Ship a working Minimum Viable Product to main — merge main into your branch and test first</font>*

<font color="#a371f7">Learning</font>

</div>

---

> **Note:**
> **MVP:** the **smallest working version** of your product that delivers the **core user value**, runs without breaking, and can be **demonstrated end-to-end**.

The goal of this phase is to ship a **working Minimum Viable Product (MVP)** to `main`.

That means: not "almost working," not "features half-finished," and not "it works on my machine." It runs, it is merged, and it is tested.

> **Warning:**
> Responsibility follows the merge. If any part of the product is broken and you were earlier responsible for it — either by **coding** it or by **accepting the pull request that merged it** — that broken code is your responsibility.

---

## <font color="#388bfd">Why you merge main INTO your branch and test first</font>

Your branch is only correct if it works with the **newest** code in `main`. Teams change `main` constantly — teammates may have changed files, dependencies, routes, schemas, or configs since you branched. If you only test your feature branch against an old snapshot, your code can break the moment it meets everyone else's changes.

Merging `main` **into your branch** before opening a PR:

- Forces you to resolve conflicts **early**, on your own branch, where a mistake hurts only you
- Proves your feature still works in the **current integrated codebase**, not a stale one
- Makes the final merge into `main` predictable, so it does not "blow up" the build right before a deadline

```
                    others keep merging into main
main      ●───────●───────●───────────────●──────────●───▶
           \               \             ↑
            \               \  step 3:  / step 6: PR to main
             \               \ merge   /  (only after testing)
              \               \ main  /
               \               ▼ in  /
your branch     ●───●───●──────●────●
                    your        step 4: TEST here —
                    commits     conflicts and breakage
                                surface on YOUR branch
```

---

## <font color="#388bfd">The GitKraken workflow</font>

Follow these six steps every time you prepare work for `main`. (Branch basics are covered in [Git Usage](../../GitUsage/).)

### <font color="#79c0ff">1 — Update main locally</font>

1. In GitKraken, click the **branch list** on the left and select `main`
2. Click **Pull** (top toolbar) — this brings `origin/main` changes into your local `main`
3. Confirm `main` is up to date (your local `main` aligned with `origin/main`)

### <font color="#79c0ff">2 — Checkout your feature branch</font>

1. In the left branch list, click your feature branch name (or find it on the graph and right-click it)
2. Choose **Checkout**

### <font color="#79c0ff">3 — Merge main into your feature branch</font>

This is the key integration step.

1. Make sure you are currently **on your feature branch** (GitKraken shows the current branch at the top)
2. Find `main` in the branch list or graph
3. Right-click `main` and choose **Merge main into (your-feature-branch)**
4. If GitKraken shows conflicts, it opens a conflict resolution flow:
   - Use the conflict editor (choose the correct hunks, or manually edit)
   - Mark files as resolved
   - Complete the merge commit when prompted

### <font color="#79c0ff">4 — Test on your feature branch after the merge</font>

Do this after step 3 **every time**, because you just integrated new code:

- Run your normal project checks (run the app, run tests, build)
- Do the human test — walk through the MVP flow end to end

### <font color="#79c0ff">5 — Push your updated feature branch</font>

1. In GitKraken, click **Push** (top toolbar)
2. Confirm your feature branch is pushed to `origin` (no pending outgoing commits)

### <font color="#79c0ff">6 — Create a PR to main only after steps 1–5 are clean</font>

1. Click **Pull Requests** (left panel), then **New Pull Request**
2. Set the source to your feature branch and the target to `main`
3. In the PR description, include a section titled **Test Evidence** (see below)
4. Assign a reviewer — **not the author**
5. After approval, merge the PR — then pull `main` and do a quick MVP run again

---

## <font color="#388bfd">Test Evidence — required in every PR</font>

Every pull request description must include a **Test Evidence** section containing:

| Field | What to write |
|---|---|
| **Commands run** | Commands you ran (or what buttons you clicked) to run tests |
| **MVP flows checked** | The happy path plus at least one failure case |
| **Expected vs actual** | The expected result and the actual result |
| **Tester name(s)** | Who tested it — **not the author** |

---

## <font color="#388bfd">Minimum required testing checks</font>

Before your PR, your testing must cover at least:

- **Happy path** — the core MVP flow completes with no crash
- **One failure case** — invalid input or missing data does not crash the app
- **Regression check** — something that used to work still works

> **Tip:**
> A "happy path" is the simplest complete use of your product that meets the requirements — no edge cases, no bad user input. It is the first thing a reviewer will try and the first thing you should protect.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you define an MVP in one sentence, hitting all three requirements (core value, runs, demonstrable end-to-end)?
- [ ] Can you list the six steps of the GitKraken workflow in order?
- [ ] Can you name the four required fields of a Test Evidence section?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain why merging `main` into your branch surfaces conflicts earlier and more safely than merging your branch straight into `main`?
- [ ] Can you name the three minimum testing checks and give a concrete example of each for your project?
- [ ] Can you explain why accepting someone's pull request makes their broken code your responsibility too?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you perform the full six-step workflow on your real project, including resolving a merge conflict in GitKraken?
- [ ] Can you write a complete Test Evidence section that another student could reproduce exactly?
- [ ] Can you explain what could go wrong if a team skips step 4 (testing after the merge) and only tests before merging `main` in?

---

[Assignment](ASSIGNMENT.md)

← [Sprint Work](../SprintWork/) — Next: [Code Review and MVP Presentation](../CodeReviewAndPresentation/)
