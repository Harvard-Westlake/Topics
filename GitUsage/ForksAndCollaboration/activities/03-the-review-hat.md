# Activity — The Review Hat

*Concept: Real code review is a conversation — requested changes get pushed to the same branch, and the PR evolves until the maintainer is satisfied.*

![Diagram of the pull request review loop: the author opens the PR, the reviewer reads every changed line, and either approves and merges, or requests changes with comments on specific lines; the author then pushes fixes to the same branch, the PR updates automatically, and the loop repeats until the reviewer approves.](../assets/the-review-hat.svg)

## Task

1. In your browser, open the pull requests page of a major open source project — for example: `github.com/microsoft/vscode/pulls`.
2. Filter to closed PRs and open one that is **merged** and has review comments (look for PRs with a conversation count — click a few until you find one where a reviewer left line comments).
3. Read the conversation with the review checklist from yesterday in mind, and write down:
   - One thing the reviewer asked the author to change, quoted or paraphrased
   - How the author responded (a code change? a counter-argument? both?)
   - How many rounds of the loop in the diagram the conversation took before merge
4. Look at the PR's description. Does it answer *what changed, why, and how to test*? Grade it out of 3.
5. Write one sentence: what did the reviewer catch that the author missed — and what does that tell you about why maintainers require review before merging?
