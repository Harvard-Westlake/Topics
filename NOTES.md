# NOTES — Migration Follow-Ups and Recommended Additions

Working notes from the 2026 migration of prior-year Canvas/Notion material (24-25 and 25-26 Honors Topics courses) into this repository. Six modules were migrated: [Web Programming](WebProgramming/), [App Design and Planning](AppDesign/), [Group Programming](GroupProgramming/), [Hashing, Cryptography, and P2P Networks](HashingCryptoP2P/), [Blockchains and Bitcoin](Blockchains/), and [Advanced EVM Programming](AdvancedEVM/). This repo is now the source of truth for all six.

**How the migration treated the sources:** all Notion and Canvas links were removed (content was inlined instead); Notion/Canvas-hosted images were recreated as tables and ASCII diagrams or dropped; original point values, rubrics, grade tiers, and submission requirements were preserved; prose was rewritten for clarity but stays true to the original activities. Everything below is either a gap that needs your attention before first teaching, or a recommended addition.

---

## Review before first teaching (reconstructed or corrected content)

These items had empty or heading-only sources and were reconstructed in the original's spirit. They are faithful in intent but were not written by you — review them:

- **AppDesign/MVPPlanning** — the 25-26 "4.5 - Minimum Viable Product (Planning)" Canvas item had no content anywhere. Fully authored, aligned with how MVP.md is used in Group Programming.
- **AdvancedEVM/DecentralizedFinance** — the 24-25 "Day 1 - Decentralized Finance" item was empty. Fully authored (AMM constant-product math machine-verified) so that the IPFS/NFT day's Uniswap-liquidity assignment has the lesson it presumes.
- **Blockchains/MempoolAndWalletProgramming** — the BitcoinJ homework steps were rebuilt from the standard BitcoinJ testnet tutorial shape (the Notion capture held only headings). Verify the steps against how you actually ran it.
- **Blockchains/KeysAndLayerTwo** — RSA worked example rebuilt with p=5, q=11, e=3, d=27 (machine-verified); multisig and Lightning sections written from the source's heading outline.
- **WebProgramming** — activity bodies for 2.0 (assumptions/divergence), 2.3 (persistence), 2.5 (UX "to turn in"), and the debugging lesson were heading-only in the captures and were reconstructed.
- **Corrections made to source errors:** `firebase serve` vs `firebase deploy` confusion (2.4); the inverted Vyper assert example (7.9); `hash(5) = 1280 mod 100 = 80` arithmetic (6.1); the `public` vs `firebase-web-hosting` init-directory contradiction (Web Day 0); the 4.10 rubric percentages that contradicted its own point columns.

## Assets still trapped in Canvas (retrieve and commit when possible)

- `WalletPnemonicGenerator.html` (24-25 Blockchains Day 1 file) — recommended home: `Blockchains/BitcoinAndWallets/demos/wallet-mnemonic-generator.html`.
- `Number Representation Worksheet.pdf` (Unit 6 notes page) — an equivalent practice set with answer key was authored into `HashingCryptoP2P/HexadecimalAndHashing/`, but the original may have material worth keeping.
- The 2.6 "only allowed console error" screenshot — the specific permitted error is unrecoverable; the lesson currently says "confirm the exception with your teacher."
- The Pac-Man and ATM design-vs-tech-spec Notion pages, the 9.1 example outline, and the Commission Art drawio file — `AppDesign/Docs/design-vs-tech-spec.md` was authored fresh in their spirit.
- The Learning Widget fork target — the source truncated at "Fork HarvardWestlake's ..."; the lesson says "your teacher will share the link in class." Fill in the real repo.
- The Web3VoteExample repo URL (Advanced EVM) — referenced as "shown in class"; add the actual link.

---

## Recommended additions by module

### Web Programming

1. A `demos/` interactive for Debugging JavaScript — a page with 3-4 planted bugs students must find via the console (the lesson currently has no hands-on deliverable).
2. Restore the five short quizzes (HTML, Hosting, JS/CSS, Persistence, Databases — 3-6 pts each; no content was captured) as ASSIGNMENT.md check-ins or Canvas quizzes.
3. A Firestore security-rules lab: students lock down a deliberately open database, then probe each other's.
4. A worked exemplar Learning Widget (teacher-built, with its PLAN.md, feedback.md history, and PR) so students see the full artifact chain.
5. An accessibility/mobile checklist doc — the peer-review rubric penalizes missing mobile support but nothing teaches it.
6. Migrate the 24-25 "Ollama and LLM Install" into a future local-AI lesson; it pairs well with the "AI as manager" theme.

### App Design and Planning

1. A `demos/` drag-and-drop categorizer for the design-vs-tech-spec exercise.
2. Starter `TechSpec.md` / `Spec.md` template files students copy, matching the exact required sections.
3. A full worked Pac-Man tech spec as one Docs artifact (recover the original Notion page if possible).
4. Review fragments for MVP Planning, injectable into Group Programming's first week.
5. A documented rubric/mechanism for the class vote that selects the Design Challenge winner (currently undocumented; the "financial influence" bidding in Group Design Review is also unexplained in any source).
6. An accessibility checklist expanding the non-discrimination requirement into concrete design checks.
7. Reconcile the UX and Art Direction point value (Canvas said 5 pts; the activity's own criteria say 30).

### Group Programming

1. A Docs page: PR-description template with the Test Evidence stencil.
2. Recreate the lost issue-board/deliverable visuals from 5.0 as screenshots or a demo page.
3. Review fragments for Issues as Work Requests (the 5-part issue structure is highly drillable) and the merge-conflict fix flow.
4. A reviewer's checklist doc — what a reviewer actually verifies before merging (currently implied, never enumerated).
5. An explicit CI/CD extension lesson — 5.4's manual-vs-automated framing sets it up naturally.
6. A slide template for the 5.3 individual deep-dive (four parts, timed).

### Hashing, Cryptography, and P2P Networks

1. A `demos/` interactive base-conversion trainer.
2. A second, harder review fragment chaining conversions into SHA-256 digest reading.
3. An SSH-key hands-on assignment bridging Digital Signatures to [Git Usage](GitUsage/) (generate a key, add it to GitHub).
4. A Merkle-tree pencil-and-paper activity as a bridge into Blockchains.
5. A short section on password-cracking economics (why salts and slow hashes matter).
6. An in-class "swarm simulation" card game for Peer-to-Peer Networks.

### Blockchains and Bitcoin

1. Recover and commit the wallet-mnemonic-generator demo (see Canvas assets above).
2. A `demos/` hash-difficulty visualizer (the leading-zeros lottery) for Bitcoin and Wallets.
3. A review fragment mapping Java-to-Vyper token vocabulary, injectable before the ERC20 lesson.
4. A small Python RSA script in `KeysAndLayerTwo/starter/` so the classmate key exchange scales beyond hand arithmetic.
5. An ASSIGNMENT.md for Proof of Stake capturing the simulation reflection in writing.
6. A topic-claim table for the Crypto Research Project to enforce first-come-first-served topics.

### Advanced EVM Programming

1. Add the real Web3VoteExample repo link (see Canvas assets above).
2. A minimal committed web3 page in `Web2Web3App/starter/` (wallet connect + one contract read + one write) so the four browser-to-chain requirements are demonstrated in code, not just prose.
3. A testnet-survival Docs page: faucet list, typical wait times, and what to do when a faucet runs dry.
4. A bridge-security case study (the largest bridge hacks) extending the "contracts can lie" lesson.
5. An NFT metadata lab where students pin their own JSON + image to IPFS via Pinata and mint against it.

---

## Prior-year material not yet migrated (candidates for new modules)

- **Web Applications & Data Science** (25-26 Unit 3, 5 items): React + Vite + Firebase apps, npm packages, data.gov analysis, native app from web content. A natural follow-on module to Web Programming.
- **Parallel Processing** (24-25 Unit 5, 2 items).
- **Security & Hacking** (24-25, 2 items: 0-days/password leaks, prompt injection vs classical hacking). Thin sources; would need authoring.
- **Setup/Terminal/Git and Programming Git** consolidated files (01, 02) were not migrated because current-repo modules (ComputerSetup, Terminal, GitUsage, GitProject) already cover them — worth a diff pass someday to confirm nothing valuable was left behind.
- Assorted 24-25 one-offs with no captured content: Lip Sync Video, AI Usage/SAM demo, "Random Prompt for ClodHost", the per-period Bitcoin screenshot posts, and the five web quizzes.

## Cross-cutting recommendations

1. **Curated module JSONs**: assemble `_modules/*.json` unit plans for the six new modules in the planner UI (`python3 _admin/_coursePlannerUI/server.py`) once you decide each year's day selection and point scaling.
2. **Point-value audit**: originals carried wildly different scales (5 pts to 980 pts). The values were preserved faithfully, but the planner's base-points/scale-factor mechanism is the right place to normalize them.
3. **Per-lesson review fragments**: 10 review fragments were created across the six modules; the highest-leverage additions are listed per module above.
4. **AI-policy alignment**: several assignments now carry explicit AI-use boundaries from the originals (no AI-generated issues in 5.4, no ChatGPT in Learning to Design, AI-as-formatter-only rules). Consider stating each assignment's allowed AI level using the school's approved framework, per faculty guidelines.
