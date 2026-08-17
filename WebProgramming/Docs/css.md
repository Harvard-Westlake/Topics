<div align="center">

# CSS
*<font color="#8b949e">Cascading Style Sheets — the design and layout of the page</font>*

</div>

---

## <font color="#388bfd">What CSS Is</font>

CSS controls **design and layout** — the paint and decorations. A stylesheet is a list of rules; each rule says *which elements* it targets (the **selector**) and *what to change* (the **declarations**):

```css
h1 {
  color: darkblue;        /* one declaration: property + value */
  font-size: 48px;
}
```

Link the stylesheet from your HTML's `<head>`:

```html
<link rel="stylesheet" href="styles.css">
```

---

## <font color="#388bfd">Selectors</font>

| Selector | Targets | Example |
|---|---|---|
| `p` | Every `<p>` element | `p { line-height: 1.5; }` |
| `.card` | Everything with `class="card"` | `.card { border: 1px solid gray; }` |
| `#start-button` | The one element with `id="start-button"` | `#start-button { font-size: 20px; }` |
| `.card p` | Paragraphs *inside* a `.card` | `.card p { color: gray; }` |
| `button:hover` | Buttons while the mouse is over them | `button:hover { background: gold; }` |

When rules conflict, the more specific selector wins (`#id` beats `.class` beats `tag`) — that is the "cascading" in the name.

---

## <font color="#388bfd">Everyday Properties</font>

| Property | Controls | Example values |
|---|---|---|
| `color` | Text color | `black`, `#388bfd`, `rgb(60, 60, 60)` |
| `background-color` | Fill behind the element | `white`, `#1a1a2e` |
| `font-size` | Text size | `16px`, `1.2rem` |
| `font-family` | Typeface | `Arial, sans-serif` |
| `margin` | Space **outside** the border | `16px`, `0 auto` (center a block) |
| `padding` | Space **inside** the border | `12px 20px` |
| `border` | The edge itself | `1px solid #ccc` |
| `border-radius` | Rounded corners | `8px`, `50%` (circle) |
| `width` / `max-width` | Element width | `300px`, `100%` |
| `display` | Layout behavior | `block`, `inline`, `flex`, `none` (hidden) |

---

## <font color="#388bfd">The Box Model</font>

Every element is a rectangle wrapped in three layers of spacing. Margin pushes *other elements away*; padding pushes *the content inward*:

```
+-------------------------------------+
|              margin                 |   (transparent, outside)
|   +-----------------------------+   |
|   |          border             |   |
|   |   +---------------------+   |   |
|   |   |      padding        |   |   |
|   |   |   +-------------+   |   |   |
|   |   |   |   content   |   |   |   |
|   |   |   +-------------+   |   |   |
|   |   +---------------------+   |   |
|   +-----------------------------+   |
+-------------------------------------+
```

---

## <font color="#388bfd">Simple Layout with Flexbox</font>

To place children side by side and control their spacing, make the parent a flex container:

```css
.toolbar {
  display: flex;
  gap: 12px;                   /* space between children */
  justify-content: center;     /* horizontal placement */
  align-items: center;         /* vertical alignment */
}
```

Flexbox handles most layouts this unit needs: navigation bars, button rows, centering a widget on the page.

> **Tip:**
> The fastest way to learn CSS is to open DevTools, click any element, and edit its styles live in the Elements tab — changes appear instantly and vanish on refresh.

---

← Back to [Docs](README.md)
