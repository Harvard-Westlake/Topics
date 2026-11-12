<div align="center">

# UX and Behavior Tracking
*<font color="#8b949e">UX (user experience) is how using a site feels, and behavior tracking measures it from what real visitors actually do.</font>*

</div>

---

![A heatmap laid over a widget page. The moon slider in the middle glows red: it is what people came for. The page title also glows, marked as dead clicks, because users click it but it does nothing. A dashed scroll line sits above the More examples section: most visitors never scroll below it. Hot means many users, cold means nobody, and the map shows what users do, not what they say.](assets/heatmap-layout.svg)

Good UX is not a matter of taste. You can see it in what visitors do:

- **Engagement speed:** how fast the page earns their attention.
- **Navigation and flow:** whether they always know where they are and what to do next.
- **Heatmaps:** a picture of where many visitors clicked and how far they scrolled.

## <font color="#388bfd">Table of Contents</font>

1. [Three principles every widget is judged by](#three-principles-of-user-experience)
2. [Heatmaps: what visitors really do](#heatmaps)
3. [What makes content people finish](#engaging-content)

## <font color="#388bfd">Three Principles of User Experience</font>

### <font color="#79c0ff">Engagement speed</font>

Visitors decide within a few seconds whether to stay. Your widget has about one breath to answer: *what is this, and what do I do first?*

- The main content appears right away: no long loading, no wall of setup text.
- The first thing to interact with is visible without scrolling.
- Google measures this too: a page's main content should finish appearing within about 2.5 seconds.

### <font color="#79c0ff">Clear navigation</font>

At every moment, a visitor can answer three questions without thinking:

| Question | Answered by |
|---|---|
| Where am I? | Headings, titles, progress indicators |
| What can I do here? | Obvious, honestly labeled buttons and links |
| How do I get back? | Back and home controls that never trap them |

### <font color="#79c0ff">User flow</font>

**User flow** is the path a visitor takes from arriving to the payoff. Decide it on purpose:

```
arrive -> understand what this is -> first interaction -> learning loop (repeat) -> payoff
```

Every place a real visitor hesitates, backtracks, or asks "what now?" is a break in the flow.

## <font color="#388bfd">Heatmaps</font>

You cannot stand behind every visitor, but every click, scroll, and mouse move is a [web event](../JavaScriptAndCursor/) that can be recorded. A **heatmap** combines many visitors' events into a color overlay: hot where activity piles up, cold where nothing happens.

| Heatmap | Built from | Shows |
|---|---|---|
| **Click map** | Every click and tap | What people think is clickable, including things that are not |
| **Scroll map** | How far down each visitor scrolls | Where attention runs out. Content below that line is barely seen |
| **Move map** | Mouse position over time | Roughly where eyes travel |

Free tools such as [Microsoft Clarity](https://clarity.microsoft.com/) record these for a real site, plus session replays (a video of one visitor's mouse and scrolling) and warning signs like **dead clicks** (clicking something that does nothing) and **rage clicks** (clicking the same spot over and over).

Heatmaps are powerful because they show what people **do**, which often contradicts what they say and what the designer assumed.

> **Note:** Tracking comes with responsibility. Collect only what improves the experience, tell visitors you collect it, and never record what they type into forms.

## <font color="#388bfd">Engaging Content</font>

Content people finish tends to share five things:

- **Immediate payoff:** something interesting happens in the first seconds, before any instructions.
- **Interaction over explanation:** visitors *do* the idea instead of reading about it.
- **One clear focus per screen:** no competing buttons asking for attention.
- **Feedback for every action:** every click, drag, and keypress visibly changes something.
- **Curiosity:** the design hints there is more ("one more level") without demanding it.

Pretty but passive content gets skimmed. Content that responds gets explored.

## <font color="#388bfd">☑️ Check for Understanding</font>

- [ ] Name the three UX principles and the three questions clear navigation answers.
- [ ] Name the three kinds of heatmap and what each one shows.
- [ ] Sketch your widget's user flow from arriving to the payoff.

## <font color="#388bfd">🚀 Stretch Goals</font>

- [ ] Predict what a click map of your widget would show, including one thing visitors would click that is not a button.

---

[Assignment](ASSIGNMENT.md)

← [The Learning Widget Project](../LearningWidget/) | Next: [Widget Iteration from Feedback](../WidgetIteration/)
