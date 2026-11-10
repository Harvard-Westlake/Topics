# Activity - Read and Break JSON

*Concept: Read a small piece of JSON the way a computer does, then break it on purpose and fix it.*

![A JSON object on the left and the name of each part on the right. Curly braces wrap one object, a set of key and value pairs. Each key, such as game, rating, stillPlaying, mechanics, and session, is a label in double quotes followed by a colon. Values are text in double quotes (Wordle), a number with no quotes (9), true or false with no quotes, a list in square brackets (daily streak, share grid), or another object in curly braces (minutes 5, device phone). A comma goes between pairs and never after the last one. Break one rule and the whole text is invalid.](../assets/json-anatomy.svg)

## Task

1. Open [The JSON Explorer](https://harvard-westlake.github.io/Topics/WebProgramming/DatabasesAndCollections/demos/json-explorer.html). The left side is the text. The right side is what a computer sees.
2. Select three different values on the right and read the line under the tree: the type of each value, and how JavaScript reaches it (for example `data.session.minutes`).
3. Press each **Break it** button. Read why it broke, then repair the text by hand until the box says **Valid JSON** again.
4. Delete everything and write your own object from an empty `{ }`: one thing you enjoy on the web, with a text value, a number, a true or false, a list, and one object inside it.
5. Compare with a neighbor. Which of the four mistakes did each of you make without the buttons?
