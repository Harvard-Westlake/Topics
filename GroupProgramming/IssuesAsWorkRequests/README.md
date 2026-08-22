<div align="center">

# Issues as Work Requests
*<font color="#8b949e">Write GitHub Issues so precise that a stranger can implement them without asking you anything</font>*

<font color="#a371f7">Learning</font>

</div>

---

You have designed a product, written a technical spec, built parts of it, and integrated an MVP. The next skill is **virtual engineering communication**: describing work so clearly that **someone else can implement it correctly without asking you for clarification**. In modern teams, **GitHub Issues are the unit of work** — they define what to build, how it connects to the product, and how we prove it is done.

A well-written issue answers four questions for the receiving programmer:

1. **Exactly what to build** — precise behavior, not vague goals
2. **Where it fits** in the project — code area, plus design link if relevant
3. **How to verify it works** — clear acceptance tests
4. **What it depends on** — other PRs, APIs, environment variables, data migrations, libraries, feature flags, and so on

---

## <font color="#388bfd">The five-part issue structure</font>

Copy this structure into each issue you write.

**Title:** actionable + specific — "Add password reset email flow," not "Auth improvements."

**Top line in the body (required):**

```
Author: [Your Name](link-to-your-github-profile-or-class-profile)
```

### <font color="#79c0ff">1. Summary (1–2 sentences)</font>

What is being added or changed, stated concretely.

### <font color="#79c0ff">2. Context + where it fits</font>

- Link to the relevant **Figma frame/page** (or screenshot link) if UI-related
- Link to the relevant **repo locations** — file paths, folders, routes, components
- Explain the integration point(s): "This affects X screen," "This adds Y API route," "This modifies Z table"

### <font color="#79c0ff">3. Detailed requirements (behavior-first, technical)</font>

Write in precise, testable terms:

- **User-facing behavior** — states, edge cases, errors, loading, empty states
- **Data requirements** — fields, shapes, validation rules
- **API behavior** — routes, request/response shape, status codes, error payloads
- **Constraints** — rate limits, auth rules, permissions, performance expectations

### <font color="#79c0ff">4. Acceptance criteria (verification steps)</font>

Provide a checklist someone can run to confirm it is correct:

- A step-by-step manual test — happy path plus at least one failure/edge case
- Expected results for each step
- Any setup required — seed data, env vars, test accounts

### <font color="#79c0ff">5. Dependencies</font>

List anything that must exist first:

- Other issues/PRs, database migrations, services, endpoints, design approvals, credentials, libraries
- If the issue is blocked, say **what blocks it** and what unblocks it

> **Warning:**
> If your issue can be "implemented" in multiple incompatible ways, it is not specific enough. Force one correct interpretation by stating concrete behaviors, states, and verification steps.

---

## <font color="#388bfd">Hard rules</font>

- **Each student creates 3 issues.**
- **No AI-generated content in the issues** — including "ideas," "requirements," "acceptance criteria," or "steps." You may use AI **only** for formatting (turning your own content into clean Markdown).
- Each issue must include **your name as a clickable link** on the top line of the body.
- Write issues as if the implementer **cannot ask you questions** and must rely on the issue + the repo alone.

---

## <font color="#388bfd">Main branch protection and reviews</font>

From this point on, `main` will be **locked** to prevent direct pushes. All changes must go through pull requests:

- Every PR must have **2 reviewers** who were **not** the original coder(s) for that feature
- Reviewers verify behavior and code quality; they can **request changes**, which sends the work back to the author
- If a PR **cannot merge cleanly into `main`**, the responsibility falls on the original programmer (or whoever had AI generate the code) to fix the branch so it merges and still works

### <font color="#79c0ff">Fixing a merge conflict (minimal process)</font>

```bash
git checkout <pr-branch>
git merge main            # resolve conflicts
# re-run the verification steps from the Issue to confirm behavior still works
git push                  # update the PR branch
```

> **Note:**
> At companies, automated test suites run these checks for you on every PR. This workflow is the manual version of what **CI/CD** (continuous integration / continuous deployment) should eventually automate.

---

## <font color="#388bfd">Priority setting</font>

Once every teammate's issues exist, set priorities **as a team**: rank the full set of issues so it is obvious which ones should be picked up first. This ranked list is what the next round of work — including classmates who will contribute to your project — pulls from.

---

## <font color="#388bfd">☑️ Check for Understanding</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Name the five parts of a well-structured issue in order.
- [ ] Write an issue title that is actionable and specific rather than vague.
- [ ] State the hard rules for this assignment, including what AI may and may not be used for.

### <font color="#79c0ff">Intermediate</font>

- [ ] Write acceptance criteria with a happy path, one failure case, and expected results for each step.
- [ ] Explain what branch protection on `main` changes about how work gets merged.
- [ ] List a realistic set of dependencies for a feature in your own project.

### <font color="#79c0ff">Advanced</font>

- [ ] Fix a PR that cannot merge cleanly into `main` using checkout, merge, re-verify, and push.
- [ ] Explain how the manual review-and-verify workflow maps onto what CI/CD automates at companies.
- [ ] Take a vague request like "make login better" and rewrite it as an issue with only one correct interpretation.

---

[Assignment](ASSIGNMENT.md)

← [Code Review and MVP Presentation](../CodeReviewAndPresentation/) — Next: [Refactoring and the README](../RefactorAndReadme/)
