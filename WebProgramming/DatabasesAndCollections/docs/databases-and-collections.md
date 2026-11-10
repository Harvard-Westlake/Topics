<div align="center">

# Databases and Collections
*<font color="#8b949e">A database is data kept on a server, so every visitor to your site reads and writes the same records.</font>*

</div>

---

![On the left, two visitors' browsers each run your site with their own browser storage: one has local storage theme=dark and the cookie returning=true, the other has theme=light and no cookie because it is a first visit. Arrows from both go through an orange bar labeled rules, which checks every request, to Firestore on the right, shared by everyone. Firestore holds a collection called guestbook with documents visitor-001 (name Alice, message Cool site!) and visitor-002, and a collection called scores with a document high-score (points 9800). Browser storage belongs to one visitor on one device; Firestore belongs to the whole site, but only allows what the rules allow.](../assets/firestore-layout.svg)

Today's new tool is where a site keeps data that everyone shares.

- **JSON:** the way data is written down, as keys and values.
- **Firestore:** a database of **collections** (like folders) holding **documents** (like files), and each document is a set of key and value fields.
- **By name:** every write and every read names its collection, then its document.

The last section is review from [Intro to AI Coding](../../InterfacingWithAI/): how a brain learns, why a brain and an AI both squeeze everything into words, and the question that leads into today's assignment.

## <font color="#388bfd">Table of Contents</font>

1. [JSON: keys and values, the format data is written in](#json)
2. [Firestore: collections, documents, and fields, and how to lay them out](#firestore-collections-and-documents)
3. [Writing and reading a document by name: put and get](#writing-and-reading-by-name)
4. [Rules: the gatekeeper for your database](#firestore-rules)
5. [Local storage vs cookies: two kinds of browser memory](#local-storage-vs-cookies)
6. [Supplemental review: how a brain learns, why everything becomes language, and the question](#supplemental-learning-language-and-ai)

## <font color="#388bfd">JSON</font>

**JSON** is a way to write data down as plain text so that any program can read it. Think of a form: a label, then what you wrote next to it. JSON calls the label a **key** and what you wrote a **value**.

![A JSON object on the left and the name of each part on the right. Curly braces wrap one object, a set of key and value pairs. Each key, such as game, rating, stillPlaying, mechanics, and session, is a label in double quotes followed by a colon. Values are text in double quotes (Wordle), a number with no quotes (9), true or false with no quotes, a list in square brackets (daily streak, share grid), or another object in curly braces (minutes 5, device phone). A comma goes between pairs and never after the last one. Break one rule and the whole text is invalid.](../assets/json-anatomy.svg)

| Piece | Looks like | Rule |
|---|---|---|
| **Object** | `{ ... }` | A set of key and value pairs. |
| **Key** | `"game"` | Always text in double quotes, followed by a colon. |
| **Text** | `"Wordle"` | Double quotes only, never single. |
| **Number, true or false, null** | `9`, `true`, `null` | No quotes. |
| **List** (array) | `["daily streak", "share grid"]` | Values in order, inside square brackets. |
| **Object inside an object** | `"session": { "minutes": 5 }` | A value can be a whole object. |

A comma goes between pairs, never after the last one. JSON is strict: one missing quote and the whole text is rejected.

JSON is text. A JavaScript object is a live thing in memory. Two built-in functions convert between them:

```javascript
const taste = { game: "Wordle", rating: 9 };
const text = JSON.stringify(taste);    // '{"game":"Wordle","rating":9}'  object to text
const again = JSON.parse(text);        // text back to an object
console.log(again.rating);             // 9
```

Try it live: [The JSON Explorer](https://harvard-westlake.github.io/Topics/WebProgramming/DatabasesAndCollections/demos/json-explorer.html) ([source](../demos/json-explorer.html)) shows what a computer sees as you type, and lets you break JSON on purpose.

### <font color="#79c0ff">Activity 1</font>
<details>
<summary><strong>Read and Break JSON</strong></summary>

*Concept: Read a small piece of JSON the way a computer does, then break it on purpose and fix it.*

![A JSON object on the left and the name of each part on the right. Curly braces wrap one object, a set of key and value pairs. Each key, such as game, rating, stillPlaying, mechanics, and session, is a label in double quotes followed by a colon. Values are text in double quotes (Wordle), a number with no quotes (9), true or false with no quotes, a list in square brackets (daily streak, share grid), or another object in curly braces (minutes 5, device phone). A comma goes between pairs and never after the last one. Break one rule and the whole text is invalid.](../assets/json-anatomy.svg)

## Task

1. Open [The JSON Explorer](https://harvard-westlake.github.io/Topics/WebProgramming/DatabasesAndCollections/demos/json-explorer.html). The left side is the text. The right side is what a computer sees.
2. Select three different values on the right and read the line under the tree: the type of each value, and how JavaScript reaches it (for example `data.session.minutes`).
3. Press each **Break it** button. Read why it broke, then repair the text by hand until the box says **Valid JSON** again.
4. Delete everything and write your own object from an empty `{ }`: one thing you enjoy on the web, with a text value, a number, a true or false, a list, and one object inside it.
5. Compare with a neighbor. Which of the four mistakes did each of you make without the buttons?

*(Standalone file: [activities/01-read-and-break-json.md](../activities/01-read-and-break-json.md))*

</details>

## <font color="#388bfd">Firestore: Collections and Documents</font>

A **database** stores data on a server so many people can read and write it at once, safely and permanently. Every leaderboard, comment section, and shared document you have used is a database underneath.

We use **Cloud Firestore**, part of the Firebase project you already have. It is a filing cabinet for JSON:

| Firestore term | Think of it as | Holds |
|---|---|---|
| **Collection** | A folder with a name | Documents |
| **Document** | A file with a name (its ID) | Fields |
| **Field** | One key and its value | Text, numbers, true or false, lists, or nested objects |

![Animated diagram of data being stored. On the left, your page calls setDoc for the collection tastes and the document games with three key and value pairs. One at a time, the pairs favorite: Wordle, why: one puzzle a day, and rating: 9 slide across to Firestore on the right and land as three fields inside the document named games, which sits inside the collection named tastes. Each one is marked saved as it lands. A caption says a document is a JSON object with a name, and the collection is the folder it is filed in.](../assets/fields-into-document.svg)

A document is a JSON object with a name. Laying out a database means deciding three things:

- **One collection per kind of thing:** `tastes`, `scores`, `guestbook`. Not one giant collection for everything.
- **One document per thing,** with a name you can ask for later (`games`, `high-score`), or an ID Firestore invents when you do not care about the name.
- **The same keys in every document of a collection,** so code that reads one can read them all. Firestore does not force this. Your future self will wish you had.

<pre>
<strong><font color="#f0883e">tastes</font></strong>                      collection
├── <strong><font color="#f0883e">games</font></strong>                   document
│     favorite: "Wordle"
│     why: "one puzzle a day"
│     rating: 9
├── websites                document
│     favorite: "..."
│     why: "..."
└── wishes                  document
      list: ["...", "..."]
scores                      collection
└── high-score              document
      points: 9800
</pre>

Every document has a **path**, read as collection, then document: `tastes/games`. That path is its address, and it is the only thing you need to find it again.

**Turn it on.** In the [Firebase console](https://console.firebase.google.com/), open your project, then **Build**, then **Firestore Database**, then **Create database**. If asked, choose the **Standard** edition, pick a location near you, and start in **test mode** for now.

**Connect your site.** In **Project settings**, under **Your apps**, add a **Web** app. Firebase shows a `firebaseConfig` with your project's values. Add a module script to your page:

```html
<script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";
  import { getFirestore, doc, getDoc, setDoc }
    from "https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js";

  // Copy YOUR OWN values from the Firebase console
  const firebaseConfig = {
    apiKey: "AIza...",
    authDomain: "personalwebsite-mike.firebaseapp.com",
    projectId: "personalwebsite-mike",
    appId: "1:1234567890:web:abc123"
  };

  const app = initializeApp(firebaseConfig);
  const database = getFirestore(app);
  console.log("Connected to Firestore:", app.options.projectId);
</script>
```

If the console's snippet shows a newer version number than `12.0.0`, use theirs in both import lines.

> **Note:** This config is not a password. It only says which project to talk to, and anyone can read it in your page's source. What visitors are *allowed* to do with it is decided by your [rules](#firestore-rules).

### <font color="#79c0ff">Activity 2</font>
<details>
<summary><strong>Lay Out a Collection</strong></summary>

*Concept: Decide what your collections, documents, and fields are, then build that layout by hand in the Firebase console.*

![Animated diagram of data being stored. On the left, your page calls setDoc for the collection tastes and the document games with three key and value pairs. One at a time, the pairs favorite: Wordle, why: one puzzle a day, and rating: 9 slide across to Firestore on the right and land as three fields inside the document named games, which sits inside the collection named tastes. Each one is marked saved as it lands. A caption says a document is a JSON object with a name, and the collection is the folder it is filed in.](../assets/fields-into-document.svg)

## Task

1. On paper, lay out a `tastes` collection for yourself: three documents (for example `games`, `websites`, `wishes`) with two or three fields each. Write every field as a key and a value.
2. Open the [Firebase console](https://console.firebase.google.com/), choose your project, and open **Build**, then **Firestore Database**. Create the database if you have not yet (Standard edition, test mode).
3. Click **Start collection**. The collection ID is `tastes`.
4. The console asks for the first document. Give it the **Document ID** `games`, add each field from your paper with its type (string, number, boolean, or array), and save.
5. Use **Add document** for your other two documents. Give each a name you chose, not an Auto-ID.
6. Read the path at the top of the console for one document, such as `tastes/games`. Say it out loud as "collection, then document".

*(Standalone file: [activities/02-lay-out-a-collection.md](../activities/02-lay-out-a-collection.md))*

</details>

## <font color="#388bfd">Writing and Reading by Name</font>

The four things a database does are **C**reate, **R**ead, **U**pdate, and **D**elete (CRUD). Today you need two: a **put** (write a document) and a **get** (read it back). Both start the same way, with `doc(database, "collection", "document")`: the address.

![Animated diagram of a put and a get. Firestore on the right holds a collection named tastes with documents games, websites, and wishes, and a collection named scores with a document high-score. First the put: setDoc names tastes and games, the tastes collection lights up, then the games document lights up, a dot carries the data into it, and the page shows saved: tastes/games. Then the get: getDoc names tastes and games, the same collection and document light up, a dot travels back to the page, and the page shows the fields favorite: Wordle and rating: 9. The websites and wishes documents and the whole scores collection are labeled not named, not touched.](../assets/put-get-by-name.svg)

**Put a document with `setDoc`:**

```javascript
await setDoc(doc(database, "tastes", "games"), {
  favorite: "Wordle",
  why: "one puzzle a day",
  rating: 9
});
console.log("Saved tastes/games");
```

**Get it back with `getDoc`:**

```javascript
const snapshot = await getDoc(doc(database, "tastes", "games"));

if (snapshot.exists()) {
  console.log("Document data:", snapshot.data());
} else {
  console.log("No such document");
}
```

Firestore goes to the collection you named, then to the document you named, and touches nothing else. Names are exact: `"taste"` and `"tastes"` are two different collections, and writing to a name that does not exist creates it without a warning.

Three habits that save an afternoon:

1. **Log everything** while you build. The data you think you wrote and the data you actually wrote are often different.
2. **`await` every database call.** Talking to a server takes time; without `await`, you get the unfinished request instead of the result.
3. **Check `snapshot.exists()`.** Reading a document that is not there is not an error, it is just empty.

> **Tip:** Keep the console's **Firestore Database** page open next to your site. Every `setDoc` should appear there within seconds. If it does not, the write did not happen.

### <font color="#79c0ff">Activity 3</font>
<details>
<summary><strong>Put and Get by Name</strong></summary>

*Concept: Write one document from your own page and read it back, naming the collection and the document each time.*

![Animated diagram of a put and a get. Firestore on the right holds a collection named tastes with documents games, websites, and wishes, and a collection named scores with a document high-score. First the put: setDoc names tastes and games, the tastes collection lights up, then the games document lights up, a dot carries the data into it, and the page shows saved: tastes/games. Then the get: getDoc names tastes and games, the same collection and document light up, a dot travels back to the page, and the page shows the fields favorite: Wordle and rating: 9. The websites and wishes documents and the whole scores collection are labeled not named, not touched.](../assets/put-get-by-name.svg)

## Task

1. In VS Code, add the Firestore module script from the lesson to your page, with your own `firebaseConfig`, and reload with the Console open. You should see `Connected to Firestore`.
2. Put a document. Inside the module script, add:
   ```javascript
   await setDoc(doc(database, "tastes", "today"), {
     enjoyed: "something you enjoyed on the web today",
     rating: 8
   });
   console.log("Saved tastes/today");
   ```
3. Reload, then find `tastes/today` in the Firebase console. If it is not there, the write did not happen: read the Console error.
4. Get it back. Add:
   ```javascript
   const snapshot = await getDoc(doc(database, "tastes", "today"));
   console.log(snapshot.exists(), snapshot.data());
   ```
5. Change `"today"` in the `getDoc` line to a name that does not exist and reload. Nothing crashes: `exists()` is `false`.
6. Change `"tastes"` in the `setDoc` line to `"taste"` and reload. Look in the Firebase console: a misspelled name quietly created a second collection. Delete it, and fix the name.

*(Standalone file: [activities/03-put-and-get-by-name.md](../activities/03-put-and-get-by-name.md))*

</details>

## <font color="#388bfd">Firestore Rules</font>

Your config is public, so anyone can copy it and send their own reads and writes straight to your database, without ever visiting your site. **Security rules** run on Google's servers and check every request before it touches your data. Edit them in **Firestore Database**, then **Rules**.

Test mode lets anyone read and write anything, but only until a date about 30 days away:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.time < timestamp.date(2026, 11, 12);
    }
  }
}
```

When that date passes, every read and write fails. Replace it with rules that allow only what your site needs:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /guestbook/{entry} {
      allow read: if true;                       // anyone may read the
      guestbook
      allow create: if request.resource.data.message is string
                    && request.resource.data.message.size() <= 200;   // and sign it,
                    briefly
    }
    match /{document=**} {
      allow read, write: if false;               // everything else is locked
    }
  }
}
```

| Rules that say | Result |
|---|---|
| `if true` everywhere | Strangers can fill, change, or empty your database. |
| `if false` everywhere | Even your own site cannot read or write. |
| One rule per collection | Each collection allows exactly what your site needs. |

> **Warning:** When your site suddenly cannot read or write, check the rules first: an expired test-mode date is the most common cause.

## <font color="#388bfd">Local Storage vs Cookies</font>

Both live in the browser and both survive a refresh, but they were built for different jobs:

| | Local storage | Cookies |
|---|---|---|
| **Size limit** | About 5 MB | About 4 KB |
| **Sent to the server with every request?** | No, it stays in the browser | Yes, automatically |
| **Expires?** | Never, until cleared | Whenever you set it to |
| **Built for** | Settings, progress, saved state | "Who is this visitor?": sessions and returning visitors |

```javascript
// Local storage: simple key and value
localStorage.setItem("theme", "dark");
localStorage.getItem("theme");          // "dark"
localStorage.removeItem("theme");

// Cookies: one string of key=value pairs, joined by ";"
document.cookie = "returningVisitor=true; max-age=31536000; SameSite=Lax";  // lasts one year
console.log(document.cookie);           // "returningVisitor=true"
```

Both show up in DevTools under **Application**. Both are still **per browser**: clear the browser data or switch devices and they are gone. Data that belongs to the whole site needs a database.

## <font color="#388bfd">Supplemental: Learning, Language, and AI</font>

This part is review. It comes from [Intro to AI Coding](../../InterfacingWithAI/), where it is taught in full, and it is here because today's assignment builds on it. Open any piece you want to see again.

<details>
<summary><strong>How a Brain Learns</strong></summary>

![A computer reconstruction of about one cubic millimeter of human brain, a piece the size of a grain of sand taken from the temporal lobe of the cerebral cortex. Thousands of neurons are drawn as glowing, branching threads in pink, orange, green, blue, and yellow, tangled so densely that the block looks like a ball of colored lightning. Each large cell body sends one long trunk upward and a spray of fine branches in every direction, and every branch touches many others.](../../InterfacingWithAI/assets/neurons-cubic-millimeter.jpg)

*<font color="#8b949e">One cubic millimeter of human cerebral cortex: about 57,000 cells and 150 million connections. Image: Google Research and the Lichtman Lab, Harvard University.</font>*

That grain of brain is about one millionth of yours. A whole human brain has about 86 billion **neurons**, and each one connects to thousands of others. The connection points are **synapses**, and you have roughly 100 trillion of them.

![A single neuron in white at the center, with a rounded cell body and thick branches reaching up and out. Thousands of thin blue fibers, the axons of other neurons, weave past and touch it. Small green dots mark each synapse, the point where one of those fibers connects to this neuron. There are thousands of green dots on this one cell.](../../InterfacingWithAI/assets/one-neuron-synapses.jpg)

*<font color="#8b949e">One neuron (white), about 5,600 incoming fibers from other neurons (blue), and the synapses where they connect (green). Image: Google Research and the Lichtman Lab, Harvard University.</font>*

**What a pathway is.** A neuron fires an electrical pulse down its fiber (the **axon**). At the synapse the pulse cannot jump the gap, so the neuron releases a chemical, a **neurotransmitter**, most often **glutamate**. Glutamate crosses the gap and fits into **receptors** on the next neuron, which open and let charged sodium atoms in. Enough of that and the next neuron fires too. A pathway is a chain of neurons that fire one after another.

**How a pathway is reinforced.** A synapse is not fixed. It gets stronger when it is used at the right moment:

1. **The coincidence detector.** The receiving neuron has a second receptor, the **NMDA receptor**, plugged by a magnesium ion. The plug only pops out when the receiving neuron is already firing. So this receptor opens only when the sender and the receiver are active at the same time.
2. **Calcium is the signal.** When it opens, calcium flows in. Calcium switches on enzymes (one is called CaMKII) that push more of the ordinary receptors (AMPA receptors) into the synapse. Within minutes the same pulse now produces a bigger response. This is **long-term potentiation**, LTP.
3. **Repetition makes it physical.** Repeat it and the signal reaches the cell's nucleus, genes switch on, new proteins are built, and the synapse grows larger or a new one sprouts. That change can last for years.
4. **Unused connections weaken.** A synapse that fires out of step with its neighbor lets in only a trickle of calcium, which removes receptors. This is **long-term depression**, LTD.
5. **Reward marks what to keep.** When something turns out better than expected, a burst of **dopamine** tells recently active synapses to strengthen. That is why what you enjoy is what you get good at.
6. **Used pathways get faster.** Support cells wrap busy axons in a fatty insulation, **myelin**, which can speed the signal up many times over. Sleep then replays the day's pathways and stabilizes them.

The short version, from the scientist Donald Hebb: **neurons that fire together wire together.** So to **learn** is not to save a file somewhere. Learning is a physical change in which connections exist, how strong they are, and how fast they carry a signal. The memory is the wiring.

**Neuroplasticity** is the brain's ability to rewire itself this way, and it lasts your whole life. It is strongest during **critical periods**, windows when one region is especially easy to shape: vision in the first years, the sounds of a language in the first year, language itself through childhood. After a window closes you can still learn, but it costs more practice.

**Pruning** is the other half. A young brain builds far more synapses than it will keep: a toddler has about half again as many as an adult in some regions. Then the brain removes the ones that are not being used. Weak synapses get tagged with marker proteins, and cleanup cells called **microglia** digest them. This is not damage. It makes the pathways that remain faster and cheaper to run. The rule is **use it or lose it**, and what you spend your time doing decides which connections stay.

![Animated side view of a human brain, front on the left, with its regions lighting up in the order they are pruned. First, seeing and hearing: the occipital lobe at the back and the auditory cortex on the temporal lobe, busiest from about ages 1 to 6 and done near 11 or 12. Second, touch and movement: the sensory and motor strips across the top, through childhood, about ages 2 to 10. Third, language: Broca's area in the frontal lobe and Wernicke's area at the back of the temporal lobe, from about age 3 to the early teens. Fourth, space, memory, and meaning: the parietal and temporal lobes, about ages 10 to 18. Fifth and last, planning and self-control: the prefrontal cortex at the very front, from about age 12 into the mid to late twenties. The cerebellum and brain stem are shown in grey. A caption says the last region to finish is the one you use to plan, judge, and decide, and you are in those years right now.](../../InterfacingWithAI/assets/pruning-order.svg)

| When (approximate) | What is being pruned | What it runs |
|---|---|---|
| Ages 1 to 6, finished near 11 or 12 | Visual and auditory cortex | Seeing and hearing |
| Ages 2 to 10 | Sensory and motor strips | Touch and movement |
| Age 3 to the early teens | Language areas | Speech and understanding |
| Ages 10 to 18 | Parietal and temporal lobes | Space, memory, meaning |
| Age 12 to the mid or late 20s | Prefrontal cortex | Planning, judgment, self-control |

> **Note:** These ages come from counting synapses in donated brains and from brain scans. They differ from person to person and the stages overlap. The order, back of the brain to front, is the dependable part.

An AI model learns by a cousin of the same idea. Its "synapses" are billions of numbers called **weights**. During training, every weight that helped produce a good answer is nudged up and every weight that hurt is nudged down, over and over. Nobody types the knowledge in. As in your brain, the knowledge is the strengths of the connections.

</details>

<details>
<summary><strong>Everything Becomes Language</strong></summary>

Here is the strange part. Whatever is happening inside a brain or an AI, the only way out is words.

- **In you:** a thought is a pattern of activity across millions of synapses at once. To share it you must pick words, one after another, from the words you know.
- **In an AI:** each step holds thousands of numbers spread over dozens of layers. To answer, it must pick one **token** (a word or a piece of a word) at a time, from a fixed list of about 100,000 to 200,000 tokens.

Either way, something enormous is squeezed through something narrow. Whatever does not fit the vocabulary does not come out. Three examples:

1. **A two-year-old sees the ocean for the first time.** Wind, noise, salt, a horizon with no end, and maybe 200 words to work with. What comes out: "Big water!" The experience was not small. The vocabulary was.
2. **Koko, a gorilla taught about 1,000 hand signs,** lost her pet kitten in 1984. Her caretakers reported that she signed "cry," "sad," and "frown." Scientists still argue about how much apes mean by their signs, but something large was clearly going on behind three small words.
3. **An AI looks at the brain picture above.** More than a million pixels become millions of numbers inside it. Asked to describe it in five words, it says "glowing, tangled, colorful neuron branches." Whether an AI experiences anything is an open question. What is certain is that almost everything inside it never reaches the page.

The same experience, at three sizes of vocabulary:

![Animated diagram of one experience squeezed through three vocabularies. On the left, a sunset over the ocean is drawn as a dense web of colored connections: millions of synapses firing in a brain, or thousands of numbers per token in an AI. It passes through three openings of different widths. About 50 words or tokens, a toddler or a tiny model, gives: Big. Pretty. More! About 5,000, a ten-year-old or a small model, gives: The sky went orange and pink. I felt calm, and kind of sad when it was over. About 50,000 or more, a well-read adult or a large model, gives: Amber light draining into violet, and the ache of watching something beautiful that does not need you. A caption says the experience never changed, only the words available to carry it out did.](../../InterfacingWithAI/assets/language-bottleneck.svg)

| Vocabulary | Who has it | What comes out |
|---|---|---|
| About 50 words or tokens | A toddler, or a tiny AI model | "Big. Pretty. More!" |
| About 5,000 | A ten-year-old, or a small model | "The sky went orange and pink. I felt calm, and kind of sad when it was over." |
| About 50,000 or more | A well-read adult, or a large model | "Amber light draining into violet, and the ache of watching something beautiful that does not need you." |

This works in both directions. The AI knows only the part of you that you put into words. And you see only the part of the AI that fits into tokens. A richer vocabulary, on either side, lets more of the real thing through.

</details>

<details>
<summary><strong>The Question</strong></summary>

Put the two halves together:

- Your brain keeps the pathways you use and prunes the ones you do not.
- The region being pruned in you right now is the one that plans, judges, and decides.
- An AI will happily do your planning, judging, and deciding for you, in words, as often as you ask.

> **So:** every time you hand a kind of thinking to an AI, which of your own pathways are you choosing to strengthen, and which are you letting go quiet? If an AI can only know the you that fits into words, what does it need to hear from you, and what should you keep doing yourself, so that it becomes more of who you are and not a replacement for it?

There is no single right answer, and it is yours to work out. Start by making sure the AI actually knows you: today's assignment goes deeper into your tastes than last class did.

</details>

---

← Back to [lesson](../../README.md)
