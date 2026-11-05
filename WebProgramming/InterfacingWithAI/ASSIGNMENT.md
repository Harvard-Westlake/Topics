# Assignment - Intro to AI Coding

**Lesson:** [Intro to AI Coding](README.md)  
**Duration:** 2 class periods  
**Due:** Before the start of the next lesson's class

---

## What to Build

| Result | What it means |
|---|---|
| **A signed-in Codex** | The Codex CLI installed and signed in to a ChatGPT Plus account, on GPT-5.6-Luna (or whichever model is currently described as fast and efficient) at the lowest reasoning effort, with `/permissions` on the workspace level, never full access. |
| **A repository interview** | Two questions you asked Codex from inside your Git project repository, one of them answerable only by reading the code, plus one of its claims checked against the file it named: one thing it got right and one thing it got wrong, vague, or invented. |
| **A vague-prompt page** | `animal.html`, made by Codex CLI at the workspace level inside your website repository, from exactly this prompt: `Make me a webpage about an animal.` |
| **Five assumptions** | A list of five decisions the AI made that you never asked for (which animal, colors, tone, images, length, and so on). |
| **A pinned-down page** | `animal2.html`, made from your rewritten prompt that controls all five of those decisions. |
| **A divergence analysis** | 3 to 5 sentences comparing both of your pages with a neighbor's: where the vague prompts differed most, whether the pinned-down prompts came out alike, and which assumption surprised you most. |
| **One managed feature** | One small new feature on your hosted website, built with the manager's loop in Codex CLI: Ask (read only), then Plan (`/plan`), then Agent (workspace level) one piece at a time, testing each piece in the browser. |

**Verify:**

1. `codex --version` prints a version number, and `/status` shows your account on the Plus plan, the fast model, and the workspace permission level.
2. The file Codex named in your interview exists, and you can point at the line that proves or disproves its claim.
3. Open `animal.html` and `animal2.html` in a browser. Each of your five assumptions is visible in the first page and controlled in the second.
4. Your Git history has a commit before each Agent step and a commit after the feature worked.
5. Your live site shows the new feature, and the console has no errors while you use it.

---

## Success Criteria

- [ ] **Codex ready:** `codex --version` works and `/status` shows Plus, the fast model, and the workspace level.
- [ ] **Interview checked:** two questions asked, one claim verified against the file Codex named, one right and one wrong thing recorded.
- [ ] **Five assumptions found:** your list names five decisions the AI made without being asked.
- [ ] **Pinned-down prompt written:** your rewritten prompt controls all five decisions.
- [ ] **Divergence analysis written:** 3 to 5 sentences with at least one specific difference from your neighbor's pages.
- [ ] **Feature built by managing:** the feature is live, works, and has small commits around each Agent step.

---

## Submission

Submit **text** on Canvas. Copy the stencil below, fill in each line, and paste it into the Canvas text box:

```
Codex version (codex --version):  
Model and plan from /status:      
Permission level:                 
Question you asked your repo:     
One thing Codex got right:        
One thing it got wrong or vague:  
Five assumptions the AI made:     1.  2.  3.  4.  5.
Divergence analysis (3-5 sent.):  
Feature you built:                
Live site URL:                    https://
```
