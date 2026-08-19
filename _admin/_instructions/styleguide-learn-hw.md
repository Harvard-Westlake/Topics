# HW Digital Brand Reference — learn.hw.com

*<font color="#4D4D4D">The design system of the Harvard-Westlake class resources app, extracted verbatim from the learn.hw.com production bundle (its `--hw-*` CSS tokens and the `/styleguide` route) on 2026-08-19. This document records the source system as it exists — it does not adapt it. The [Second Edition styleguide](styleguide-edition-2-hw.md) is the proposal that translates this system into GitHub-renderable markdown for this repository.</font>*

---

## Contents

1. [Provenance](#provenance)
2. [Color tokens](#color-tokens)
3. [Typography](#typography)
4. [Surfaces and structure](#surfaces-and-structure)
5. [Component inventory](#component-inventory)
6. [Page templates](#page-templates)
7. [What markdown can and cannot adopt](#what-markdown-can-and-cannot-adopt)

---

## Provenance

learn.hw.com is a single-page app; its style guide lives at the `/styleguide` route and describes itself as:

> "HW brand tokens, UI components, and page templates used across the class resources app."

Everything below was read from the shipped assets (`assets/index-CrxlknMd.css` for tokens and rules, `assets/index-BW_kMC2g.js` for the style-guide page's own copy). Quoted sentences are the app's own usage guidance, verbatim.

---

## Color tokens

> "Approved brand palette only. Primary colors stay solid; every secondary color ships in 100%, 50%, and 20% opacity tokens."

### Primary

| Token | Hex | RGB |
|---|---|---|
| `--hw-brand-black` | `#000000` | 0 0 0 |
| `--hw-brand-red` | `#DA0016` | 218 0 22 |
| `--hw-brand-gold` | `#EDA300` | 237 163 0 |

Red and gold also ship `-50` and `-20` opacity tints (used for tinted backgrounds, focus rings, and highlight fills — the primaries themselves "stay solid" when used as ink).

### Secondary

Each secondary ships in 100%, 50%, and 20% opacity tokens (`--hw-secondary-<name>`, `-50`, `-20`).

| Token | Hex | RGB |
|---|---|---|
| `--hw-secondary-black` | `#4D4D4D` | 77 77 77 |
| `--hw-secondary-blue` | `#539ADC` | 83 154 220 |
| `--hw-secondary-green` | `#9CCA00` | 156 202 0 |
| `--hw-secondary-khaki` | `#BFC299` | 191 194 153 |
| `--hw-secondary-orange` | `#FA7300` | 250 115 0 |

### Semantic aliases

The app locks each secondary to a meaning — colors are never decorative:

| Alias | Resolves to | Meaning |
|---|---|---|
| `--hw-info` | Secondary Blue | Informational alerts and accents |
| `--hw-success` | Secondary Green | Success alerts and confirmations |
| `--hw-warning` | Secondary Orange | Warning alerts and cautions |
| `--hw-code-bg` / `--hw-code-text` | Brand Black / Secondary Khaki | Code blocks are khaki-on-black |
| `--hw-border` | Secondary Black at 20% | Every hairline border |
| `--hw-focus-ring` | 3px ring of Brand Red at 20% | Keyboard focus everywhere |
| Callout error variant | Brand Red (border + 20% tint fill) | Errors and critical caveats |
| Eyebrow / muted text | Secondary Black | Labels, metadata, supporting text |

---

## Typography

> "Headlines use Source Sans Black; subheads Semibold; body Light/Regular. (Arial as fallback when needed.)"

- **Family:** `"Source Sans 3", "Source Sans Pro", Arial`, then system sans fallbacks.
- **Weights:** Light 300 · Regular 400 · Semibold 600 · Bold 700 · Black 900.
- **All headings are black** (`h1–h6 { color: --hw-black }`), never colored — with one sanctioned exception below.

### The fluid scale

| Step | Size (clamp) | Used by |
|---|---|---|
| `--step-5` | 2.75 → 3.25 rem | H1 — Black 900, line-height 1.15 |
| `--step-4` | 2.25 → 2.75 rem | H2 — Black 900, lh 1.2 |
| `--step-3` | 1.875 → 2.25 rem | H3 — Black 900, lh 1.25 |
| `--step-2` | 1.5 → 1.875 rem | H4 — Semibold 600, lh 1.3 |
| `--step-1` | 1.25 → 1.5 rem | H5 — Semibold 600, lh 1.35; also `.lead` at Light 300 |
| `--step-0` | 1 → 1.1 rem | H6 — Bold 700, lh 1.4; body paragraphs |
| `--step--1` | 0.85 → 0.95 rem | Eyebrows, alerts, callouts, captions |

The demo headline copy is the school's brand voice: *"Discover your voice / Discover your power / Discover your community."*

### Named text utilities

| Utility | Spec | Role |
|---|---|---|
| **Lead** | `--step-1`, Light 300 | "Larger body for intro paragraphs." |
| **Eyebrow** | `--step--1`, uppercase, letter-spacing .08em, Bold, Secondary Black | Small label above a title |
| **`.red`** | Brand Red + uppercase | "Red uppercase heading utility" — demonstrated on H1–H4; the one sanctioned colored heading |

---

## Surfaces and structure

| Token | Value |
|---|---|
| Surface | white |
| Page background | radial Secondary-Blue-20 glow at top-left over a white → Khaki-20 vertical wash |
| Shadow | `0 1px 3px rgba(0,0,0,.08)` — one subtle level only |
| Radius | 8px (panels) / 6px (small) / 4px (xs); several page scopes — including the style guide itself — zero all radii for a squared, print-brand look |
| Borders | 1px, Secondary Black at 20% |

---

## Component inventory

What the style guide page demonstrates, with its own captions where it gives usage rules:

- **Buttons** — solid Brand Red primary, white text, Semibold, min-height 44px; Outline and Ghost variants turn **gold** on hover; All-Caps, Small, Large variants; disabled = solid Khaki. Squared corners in brand-strict scopes.
- **Badges & Alerts** — Neutral and Accent badges; Info / Success / Warning alerts: 20%-tint background + 3px colored left border in the semantic color.
- **Forms** — "Controls are 44px high minimum for touch, have 1px borders, clear focus rings, and never overflow their container." Focus ring is the red-20 ring; validation messages in success green / error red.
- **Tables** — plain, documented as Component / Example / Notes three-column pattern.
- **Code blocks** — Secondary Khaki text on Brand Black, `SF Mono / Fira Code / Consolas`, 0.82rem, line-height 1.7, tab-size 2, language label (Java, Python).
- **Icons** — an SVG icon set (`IconCpu`, `IconHash`, `IconKey`, …) taking `size` / `color` props. "Emoji-replacements (🕹️ 💾 📱 🖥️) are the canonical icons for Binary Interpretation Explorer system cards; use the SVG variants in all new widget UI." — i.e. **emoji are replaced by SVG icons everywhere new.**
- **Feedback & status** — dismissable toasts; tooltips; a centered popup/modal (dimmed, blurred overlay; Escape closes); progress bars ("Lesson Progress", "Score", "Gold milestone"); skeleton loaders; empty states with a primary action ("No widgets yet … Browse all widgets").
- **Navigation & controls** — breadcrumb trail for deep pages; horizontal tabs; accordion ("Expandable panels for hints, FAQs, or collapsible content"); segmented control; removable chips; a **labeled divider** — a rule carrying an inline uppercase label ("SECTION BREAK").
- **Data display** —
  - **Selectable cards**: "Radio-button-style card grid for selecting a mode, system, or category."
  - **Callouts**: "Gold-bordered notes for educational hints and important caveats." Note (gold) and Warning variants; the error variant swaps to Brand Red border + red-20 fill.
  - **Step cards**: "Numbered sequence cards for showing algorithm phases or process steps." (Demoed with the SHA-1 pipeline.)
  - **Stat cards & metrics**: "At-a-glance numbers for dashboards, summaries, or algorithm stats."
  - **Canvas card & legend**: "Container for canvas-based visualizations with a color-key legend below."

---

## Page templates

- **Widget layout** — sidebar of controls + metrics + legend beside a chart/canvas area; shared `WidgetShell` / `OperationField` / `MetricsDisplay` components with a documented prop API.
- **Overview page** (`/<subject>/overview`) — shell of "title, eyebrow, intro paragraph, optional back button"; **OverviewGroup** "visually bands related sections together with a labeled accent bar" (accents: gray, gold, black); **OverviewSection** is "one two-column section: copy left, hero right, faded watermark behind"; a connector element goes "between sections where the narrative genuinely chains (not between siblings)."
- **Homepage** — header, section headings, module grid of subject cards.
- **Subject page** — "centered h1 title, subtitle, and one or more sectioned panels with eyebrow headers and widget grids."

---

## What markdown can and cannot adopt

GitHub-rendered markdown has no stylesheet, so the tokens survive as *values and roles*, not CSS: hex colors in `<font>` tags, weight hierarchy through heading levels and bold, tints and radii not at all. The [Second Edition styleguide](styleguide-edition-2-hw.md) is the working translation — every construction there names the token it implements. Interactive `demos/*.html` pages, which ship their own CSS, should use the tokens above **directly and completely** (including tints, focus rings, and khaki-on-black code).

---

<div align="center">

*<font color="#4D4D4D">HW Digital Brand Reference — recorded from learn.hw.com, 2026-08-19</font>*

</div>
