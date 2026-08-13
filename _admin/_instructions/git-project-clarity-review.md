# Git Project — Clarity Review

This document lists concepts, explanations, and structural decisions in the Git Project that could be made simpler, clearer, or more sensible from a student perspective. It is intended for teachers preparing or updating the content.

---

## Conceptual Clarity

**1. The name "BLOB" is misleading for text-focused students.**  
"Binary Large Object" sounds like it only applies to images or audio. Students who are working with `.java` and `.txt` files may not connect the name to what they're doing. Leading with the practical definition first — "a copy of your file stored under the name of its hash" — and introducing the acronym as a term-of-art second would reduce confusion.

**2. The SHA-1 "no longer secure" warning scares students unnecessarily.**  
Calling out SHA-1's cryptographic weakness in the middle of the hashing section causes students to wonder if their implementation is wrong or dangerous. Add a one-line clarification: "For identifying file content (not securing passwords), SHA-1 is perfectly fine. Git still uses it for exactly this reason."

**3. "Directed acyclic graph (DAG)" is introduced without enough scaffolding.**  
High school students who haven't taken a data structures course don't have this term. The commit chain section should lead with the concrete description ("a chain of commits where each one knows its parent, and you can't follow the chain in a loop") and introduce DAG as the formal name afterward, not before.

**4. Immutability vs. updating the index appears contradictory.**  
Students are told "blobs are immutable" and then immediately told "when you modify a file and add it again, the index updates." This sounds like a contradiction. The explanation needs to be explicit: "The original blob never changes. Modifying a file creates a NEW blob with a different hash. The index entry is updated to point to the new blob."

**5. "Content-addressable" is used without being explained.**  
This term appears in the blob docs but is never defined. Replace with: "The filename is computed from the content — so you can always find the content if you have the hash, and you can always verify the content is unchanged by recomputing the hash."

**6. O(1) access time is unexplained jargon if Big O hasn't been covered yet.**  
Replace with: "Because the hash is the filename, Git can retrieve any file in one step, regardless of how large the repository is."

---

## Structural Clarity

**7. The `git/` vs `.git/` distinction is buried in a warning inside GP-2.1.**  
This is the single most confusing thing for students starting the project. It should appear prominently in the ProjectSetup lesson and again at the top of the Init milestone. Students will accidentally commit the `git/` folder to GitHub if they don't understand why the `.gitignore` is critical.

**8. HEAD is created in Part 1 but its purpose isn't explained until Part 4.**  
When students create `git/HEAD` in GP-1.1, they don't know why it exists. A one-sentence explanation at the point of creation — "This file will eventually store the hash of your most recent commit" — removes the mystery and connects Part 1 to Part 4.

**9. GP-3.2 and GP-3.3 implement two separate tree methods. The reason is never stated.**  
Students will wonder: "Why am I doing this twice?" The distinction should be explicit in the lesson README: GP-3.2 creates trees from any directory path (useful for testing), GP-3.3 creates trees only from staged files (what commit actually uses). Without this, students often conflate the two.

**10. The working list algorithm in GP-3.3 explains HOW without explaining WHY.**  
Students need to understand why the bottom-up process is necessary before they can implement it correctly. Add one paragraph before the step-by-step: "Trees must be built from the inside out because a parent directory's tree file needs to include each child's hash. You can't hash a parent until all its children are already written. The working list is the data structure that tracks which directories are fully resolved."

**11. The partner handoff in Part 4 does not explain logistics.**  
GP-4.1 says "run your partner's tester" but doesn't tell students how they receive the partner's code. Add explicit instructions: fork and clone the assigned repository, read the README before touching any code, document bugs before fixing them.

---

## Naming and Consistency

**12. The wrapper class is called both `GitWrapper` and `GitInterface` in different places.**  
Standardize on `GitWrapper` everywhere. (The "next year" notes also flag this.)

**13. The GP-X.0 labels are used for learning objective headers, not milestones.**  
Students may try to use `(GP-2.0)` as a commit label. Clarify once, prominently: X.0 labels are section headers in the curriculum only. Commit labels start at X.1.

**14. Commit format has minor inconsistencies across documents.**  
Some places show `parent:` as blank for the initial commit; others say to omit the line entirely. The rubric says "empty or blank." The correct behavior (and what the rubric tests for) is to **omit the line entirely** for the initial commit. Make this consistent everywhere.

**15. "Working directory" is used in two different senses.**  
In standard Git, "working directory" means the files you're currently editing. In this project's docs, it also appears to mean "the directory structure represented by the root tree." Pick one term for each concept and use it consistently throughout all materials.

---

## Ordering and Sequencing

**16. The grading rubric appears at the end of the GP-4 section but should be accessible throughout the project.**  
Students benefit from knowing what they're being graded on from the start. Consider linking to the rubric from every ASSIGNMENT.md, or moving it to the module README.

**17. Stretch goals are sometimes referenced by later required milestones.**  
GP-2.3.2 (compression) is optional, but students who skip it may have different blob content than those who implement it, potentially breaking the later integration tests. The stretch goal should clearly state: "Do not implement this unless you are certain your partner in Part 4 will also implement it."

**18. The "next year" structural changes that were applied to this version:**  
For future reference, these changes from the original notes were incorporated:
- HEAD file initialization moved from Part 2 to Part 1 (GP-1.1)
- Initial `README.md` blob creation added to Part 1
- `GitWrapper` methods updated to static
- HEAD update explicitly documented as the final step in the commit sequence

**19. The note "In Part 3, move Milestone 2 after 4" could not be resolved from the available materials.**  
The original Part 3 appears to have had 4 milestones, but only 3 were available in the source. If a GP-3.4 exists, it should be reinserted and the ordering reviewed. The current ordering (GP-3.1 index formatting → GP-3.2 basic tree → GP-3.3 tree from index) is pedagogically sound as written.

---

## Presentation

**20. Broken image references appear throughout the original Notion content.**  
Several places referenced Notion-hosted screenshots (e.g., "!Screenshot 2025-09-08 at 4.49.55 PM.png") that do not transfer to GitHub Markdown. The content that depended on those images (diagrams of the blob as a hash map, the commit parent chain) should be replaced with ASCII diagrams or descriptive prose. The relevant ASCII representations have been included in the Docs/ pages for this version.

**21. The file modes (100644, 100755) appear prominently in index examples but students are told to ignore them.**  
Remove them from the "your implementation" examples entirely. Show them only in the "real Git's index" callout, with a clear label that students do not implement this.
