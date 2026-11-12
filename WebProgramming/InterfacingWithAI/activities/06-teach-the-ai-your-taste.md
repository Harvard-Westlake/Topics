# Activity - Teach the AI Your Taste

*Concept: Let the AI interview you about what you enjoy on the web, so it knows your tastes before you ever ask it to build something.*

![Two panels showing the same request, Build me a game. Before, the AI knows nothing about you: it returns its own favorite, a blue page with a number-guessing game, a Play again button, and confetti, every gap filled with its own guess, and you spend the next hour correcting it. After, the AI interviewed you first and holds a file named TASTES.md that says short rounds, one more try, dark and quiet, hates timers, loves a puzzle that clicks: the same request now returns a dark, quiet puzzle with short rounds, no timer, and a reason to try once more. A footer gives today's rule: no building, the AI only gets to know your tastes, likes, and dislikes.](../assets/taste-before-tasks.svg)

## Task

1. In your terminal, start Codex inside your website folder, so the record of your tastes is saved next to your site:
   ```bash
   cd ~/HTCS_Projects/YOUR-WEBSITE
   codex
   ```
2. Paste this prompt, or write your own version of it:
   ```
   Ask me about what I find enjoyable about web experiences, and the
   mechanisms and features on the web that I enjoy. Pry and discover the
   nuance of what makes my tastes unique. Discover why my tastes are the
   way they are and what I find genuinely interesting. Ask one question at
   a time, do not build anything, and keep a permanent record of my tastes
   in a file named TASTES.md.
   ```
3. Answer every question honestly and in detail. When your answer is "it's just fun", keep going until you can say why. Describe tastes, not identity: no names, schools, or addresses.
4. After at least ten questions, ask:
   ```
   What do you know about my tastes?
   ```
5. Read the answer like a stranger would. Tell the AI one thing it got wrong and one thing it missed, then ask the question again. Could a classmate tell it is you, with no name on it?
6. Open `TASTES.md` in VS Code and check that it matches. Type `/quit`.
