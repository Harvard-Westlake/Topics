<div align="center">

# Collaborative Peer Review
*<font color="#8b949e">A peer review is when you test someone else's code, report what is wrong, help fix it, and approve it only once it truly works.</font>*

</div>

---

![The review loop on one pull request with two names on it. The author opens the PR. The reviewer tests everything, then writes up findings with steps to reproduce them. Fixes are made and re-tested, looping back to testing, until the reviewer can approve. Approving is a signature: a bug you approve counts against you too. Tomorrow you present this widget: a 1-minute walkthrough, then what you tested, what you found, and what got fixed.](../assets/review-loop.svg)

A review is a second pair of eyes with its name on the line:

- **Test:** use the widget the way a stranger would, and try to break it.
- **Report:** write up every problem so anyone could make it happen again.
- **Approve:** only when it works. Your approval is your signature.

## <font color="#388bfd">Table of Contents</font>

1. [Why pull request reviews exist](#why-reviews-exist)
2. [How to test like a reviewer](#testing-like-a-reviewer)
3. [Writing it up and getting to approvable](#getting-to-approvable)

## <font color="#388bfd">Why Reviews Exist</font>

The author of a widget cannot see it fresh: they know what every button does and which path to take. A reviewer does not, so they find the problems the author's brain skips over: bugs, wrong facts, confusing screens, and edge cases nobody tried.

On real teams, clicking **Approve** is not a courtesy. It means *I tested this, and I stake my name on it working.* In this class that is literal: a bug you approve counts against **your** grade too.

## <font color="#388bfd">Testing Like a Reviewer</font>

**Get access first.** The author adds you as a collaborator with **Write** access on their repository (**Settings → Collaborators → Add people**), and you accept the invite from your email or GitHub notifications. Write access lets you commit fixes, not just comment.

Then test with the widget open and the Console showing:

| Kind of check | Questions to answer |
|---|---|
| **Functional** | Does every feature it claims actually work? |
| **Correctness** | Is what it teaches true? Check it against a real source: a widget that teaches something wrong fails even if the code runs. |
| **Errors** | Do any errors show in the Console on load, or while using it? |
| **UX** | Is it engaging and quick to respond? Are the labels, paths, and empty states clear? |
| **UI** | Does it match the look of the `/admin` page on [learn.hw.com](https://learn.hw.com)? |

> **Tip:** Try to break it on purpose: click things twice, refresh halfway through, type nonsense, shrink the window to phone size. A reviewer who only follows the happy path only finds happy-path bugs.

## <font color="#388bfd">Getting to Approvable</font>

Post your findings as a review on the author's pull request, with one section for each kind of check above plus **Suggestions**, ordered by how much they matter. Every problem gets **steps to reproduce** and a screenshot. A problem nobody can make happen again from your write-up does not count as reported.

Then close the loop instead of stopping at criticism:

1. Commit fixes yourself, or formally **Request changes**.
2. Re-test after every round of fixes.
3. When everything passes, **Approve**.

"Approvable" means every feature works, the content is correct, the Console is silent, and the look matches `/admin`.

---

← Back to [lesson](../README.md)
