<div align="center">

# HTML
*<font color="#8b949e">Hypertext Markup Language — the structure and content of every web page</font>*

</div>

---

## <font color="#388bfd">What HTML Is</font>

HTML defines a page's **structure and content** — the skeleton of the building. It is not a programming language: there are no variables or logic, only nested **elements** that say "this is a heading", "this is a paragraph", "this is a link".

An element is written with **tags**:

```html
<p>This is a paragraph.</p>
```

| Piece | Name |
|---|---|
| `<p>` | Opening tag |
| `This is a paragraph.` | Content |
| `</p>` | Closing tag |

A few elements are self-contained and have no closing tag: `<img>`, `<br>`, `<input>`.

---

## <font color="#388bfd">The Minimal Document</font>

Every HTML file has the same skeleton:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Shown in the browser tab</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <h1>Everything visible goes inside body</h1>
    <script src="main.js"></script>
  </body>
</html>
```

| Part | Role |
|---|---|
| `<!DOCTYPE html>` | Declares modern HTML — always the first line |
| `<head>` | Invisible setup: title, linked CSS, metadata |
| `<body>` | Everything the user actually sees |
| `<script>` at the end of body | Loads JavaScript after the page content exists |

---

## <font color="#388bfd">Common Tags</font>

| Tag | Meaning | Example |
|---|---|---|
| `<h1>`–`<h6>` | Headings, largest to smallest | `<h1>Title</h1>` |
| `<p>` | Paragraph | `<p>Text.</p>` |
| `<a>` | Link | `<a href="https://example.com">Visit</a>` |
| `<img>` | Image | `<img src="cat.png" alt="A cat">` |
| `<button>` | Clickable button | `<button>Start</button>` |
| `<input>` | Text box, checkbox, etc. | `<input type="text">` |
| `<ul>` / `<ol>` / `<li>` | Bulleted / numbered lists and their items | `<ul><li>One</li></ul>` |
| `<div>` | Generic container (block) | `<div class="card">...</div>` |
| `<span>` | Generic container (inline) | `<span class="highlight">word</span>` |

---

## <font color="#388bfd">Attributes</font>

Attributes are extra settings written inside the opening tag as `name="value"`:

```html
<a href="https://example.com" target="_blank">Opens in a new tab</a>
<img src="cat.png" alt="A sleeping cat" width="300">
<button id="start-button" class="big primary">Start</button>
```

| Attribute | Purpose |
|---|---|
| `href` | Where a link goes |
| `src` | Where an image/script file lives |
| `alt` | Text description of an image (accessibility) |
| `id` | Unique name for **one** element — used by JavaScript's `getElementById` |
| `class` | Reusable label for **many** elements — used by CSS |

---

## <font color="#388bfd">Semantic Elements</font>

These behave like `<div>` but *say what they are*, which helps browsers, screen readers, and future-you:

| Tag | Marks |
|---|---|
| `<header>` | Top-of-page banner or section intro |
| `<nav>` | Navigation links |
| `<main>` | The page's primary content |
| `<section>` | A thematic grouping of content |
| `<footer>` | Bottom matter — credits, links |

---

← Back to [Docs](README.md)
