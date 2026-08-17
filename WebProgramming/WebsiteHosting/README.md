<div align="center">

# Website Hosting
*<font color="#8b949e">HTML, CSS, and JavaScript — and putting a real website on the internet with Firebase</font>*

<font color="#a371f7">Learning</font>

</div>

---

## <font color="#388bfd">Table of Contents</font>

**[Learning Objectives](#learning-objectives)**  
What you should be able to do by the end of this lesson.

**[Research Topic: "The Web"](#research-topic-the-web)**  
Use the AI research technique on today's subject before touching any tools.

**[The Three Languages of a Web Page](#the-three-languages-of-a-web-page)**  
HTML is the skeleton, CSS is the paint, JavaScript is the electricity.

**[What Hosting Means](#what-hosting-means)**  
Why a file on your laptop is not a website yet.

**[Step 1: Create a Firebase Project](#step-1-create-a-firebase-project)**  
Set up the project that will hold your site.

**[Step 2: Install the Firebase CLI and Log In](#step-2-install-the-firebase-cli-and-log-in)**  
Command-line tools that connect your computer to Firebase.

**[Step 3: Initialize Hosting](#step-3-initialize-hosting)**  
`firebase init hosting` and how to answer its prompts.

**[Step 4: Deploy](#step-4-deploy)**  
`firebase deploy` and your first live URL.

**[Step 5: Download the Website Template](#step-5-download-the-website-template)**  
Start from Harvard-Westlake's BasicStaticWebsite and make it yours.

**[Step 6: Put It Under Version Control](#step-6-put-it-under-version-control)**  
Initialize the repository in GitKraken and push it public.

---

## <font color="#388bfd">Learning Objectives</font>

By the end of this lesson, you should be able to:

1. Install the Firebase CLI tools ([firebase.google.com/docs/cli](https://firebase.google.com/docs/cli))
2. Host a basic static website using Firebase
3. Understand the fundamental differences between HTML, CSS, and JavaScript
4. Modify a website's appearance using only HTML and CSS
5. Generate additional CSS to style the website

---

## <font color="#388bfd">Research Topic: "The Web"</font>

Before the tools, the territory. Use the [research technique from last lesson](../InterfacingWithAI/) to answer, with AI:

- What actually happens between typing a URL and seeing a page?
- What is a **server**, and what does it mean for one to "serve" your files?
- What is the difference between a website that lives on your laptop and one that is **hosted**?

Verify at least one answer against [MDN's "How the Web works"](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works).

---

## <font color="#388bfd">The Three Languages of a Web Page</font>

Every page you have ever visited is built from the same three ingredients. Think of a building:

| Language | Role | Building metaphor |
|---|---|---|
| **HTML** (Hypertext Markup Language) | Defines the structure and content | The frame and skeleton |
| **CSS** (Cascading Style Sheets) | Controls the design and layout | The paint and decorations |
| **JavaScript** | Makes the page dynamic and interactive | The electricity and plumbing — things *happen* in response to actions |

Today's emphasis is on **HTML and CSS** — JavaScript gets its own lesson next.

> **Tip:**
> Keep the reference docs open as you work: [HTML](../Docs/html.md), [CSS](../Docs/css.md), [JavaScript](../Docs/javascript.md).

---

## <font color="#388bfd">What Hosting Means</font>

The `index.html` you made last lesson works — but only on your machine. Nobody else on Earth can visit it. **Hosting** means placing your files on a server that is always on, always connected, and reachable at a public URL.

We use **Firebase Hosting**, a Google service with a generous free tier. The workflow you learn today — edit locally, deploy, verify live — is the same loop professional web developers run every day.

```
your laptop                         Firebase's servers
+------------------+   deploy    +---------------------+
| public/          | ----------> | https://your-site   |
|   index.html     |             |        .web.app     |
|   styles.css     |             |                     |
+------------------+             |  anyone can visit   |
                                  +---------------------+
```

---

## <font color="#388bfd">Step 1: Create a Firebase Project</font>

1. Go to [console.firebase.google.com](https://console.firebase.google.com/)
2. Sign in with your **personal Google account** (not your HW account)
3. Create a project named `personalwebsite-<name>`, replacing `<name>` with your first name — for example `personalwebsite-mike`, but using your own first name
4. Follow the prompts to finish creating the project

---

## <font color="#388bfd">Step 2: Install the Firebase CLI and Log In</font>

The **CLI** (command-line interface) lets your terminal talk to Firebase. Visit the [Firebase CLI documentation](https://firebase.google.com/docs/cli) and follow the installation instructions for your operating system.

On macOS, this is one command in the terminal:

```bash
curl -sL https://firebase.tools | bash
```

Then authenticate with Google:

```bash
firebase login
```

Follow the prompts in the web browser that opens, sign in to the same Google account you used for the console, and make sure to select **Allow**.

---

## <font color="#388bfd">Step 3: Initialize Hosting</font>

1. Create a new project folder on your computer, named the same as your Firebase project: `personalwebsite-<name>`
2. Open that folder in Cursor, and open a terminal inside it
3. Run:

```bash
firebase init hosting
```

4. Answer the prompts as follows:

| Prompt | Answer |
|---|---|
| Which Firebase project? | Select the `personalwebsite-<name>` project you created |
| What do you want to use as your public directory? | `public` (press Return to accept the default) |
| Configure as a single-page app? | `y` |
| Set up automatic builds and deploys with GitHub? | `n` — we set up GitHub ourselves later |
| Any remaining questions | `No` |

When you see **"Firebase initialization complete"**, your folder now contains:

```
personalwebsite-<name>/
  firebase.json      — hosting configuration
  .firebaserc        — which Firebase project this folder belongs to
  public/            — everything in here becomes your website
    index.html
```

---

## <font color="#388bfd">Step 4: Deploy</font>

```bash
firebase deploy
```

The command uploads everything in `public/` and prints a **Hosting URL** that looks like:

```
Hosting URL: https://personalwebsite-mike.web.app
```

Open that URL in your browser. That page is live — on a real server, reachable from any device in the world.

> **Note:**
> `firebase deploy` publishes to the internet. To preview changes locally *before* publishing, run `firebase serve` and open the local address it prints. Serve is for testing; deploy is for shipping.

---

## <font color="#388bfd">Step 5: Download the Website Template</font>

Rather than building from nothing, start from Harvard-Westlake's template:

1. Navigate to the [BasicStaticWebsite repository](https://github.com/HarvardWestlake/BasicStaticWebsite)
2. Click **Code → Download ZIP**
3. Unzip the file and copy the contents into the `public/` directory Firebase created
4. Examine the file structure — identify the HTML and CSS files, and open the HTML file in a browser to view the current design

Then make it yours:

- Change colors, fonts, or margins in the CSS
- Modify headings or text in the HTML
- Refresh the browser after each save to observe the change
- Ask AI to generate additional CSS to style the site — then read what it produced and confirm you understand each rule before keeping it

When you like what you see, run `firebase deploy` again and confirm the live site updated.

---

## <font color="#388bfd">Step 6: Put It Under Version Control</font>

Your website is now a real project — it deserves a repository. In GitKraken:

1. Click **File → Init Repo**
2. Select the folder to place it in — the *parent* folder of your website folder, not the website folder itself (for example `C:\Users\andre\Documents\`, **not** `C:\Users\andre\Documents\MyWebsite`)
3. Type the name of your website folder (i.e. `personalwebsite-<name>`)
4. Create the repository by clicking the green button
5. Push your repository to GitHub and make it **public**

> **Tip:**
> Forgot how init, commit, and push work? The [Git Usage](../../GitUsage/) module covers all of it.

---

## <font color="#388bfd">Skill Building</font>

### <font color="#79c0ff">Introductory</font>

- [ ] Can you state what HTML, CSS, and JavaScript each do, using the building metaphor?
- [ ] Can you explain the difference between a file on your laptop and a hosted website?
- [ ] Can you run `firebase deploy` and find the Hosting URL in its output?

### <font color="#79c0ff">Intermediate</font>

- [ ] Can you explain what each prompt in `firebase init hosting` is asking and how you answered it?
- [ ] Can you describe what `firebase.json`, `.firebaserc`, and `public/` each contain?
- [ ] Can you modify the template's CSS, verify the change locally, and push the update live?

### <font color="#79c0ff">Advanced</font>

- [ ] Can you explain when to use `firebase serve` versus `firebase deploy`, and what could go wrong if you confused them?
- [ ] Can you trace the full path of a file from your `public/` folder to a stranger's browser?
- [ ] Can you take AI-generated CSS and explain what every rule in it does before deploying it?

---

[Assignment](ASSIGNMENT.md)

← [Interfacing with AI](../InterfacingWithAI/) — Next: [JavaScript and Coding with Cursor](../JavaScriptAndCursor/)
