<div align="center">

# Design vs Tech Spec
*<font color="#8b949e">The same product, described in two different languages</font>*

</div>

---

A **design document** describes what a product does and why users care. A **technical specification** describes how programmers will build it. The two examples below describe the *same features* twice, so you can see exactly where the line falls.

The quick test: could a person with no programming knowledge read the sentence and picture the product? If yes, it is design. If the sentence only makes sense to a programmer, it is specification.

---

## <font color="#388bfd">Example 1 — Pac-Man (a game)</font>

### <font color="#79c0ff">Game design</font>

| Element | Design description |
|---|---|
| **Concept** | The player guides a hungry yellow character through a maze, eating every dot while being hunted by four ghosts |
| **Objective** | Clear the maze of dots without being caught; each cleared maze leads to a faster, harder one |
| **Characters** | Pac-Man (the player) and four ghosts, each with its own personality — one chases directly, one ambushes, one wanders |
| **Power pellets** | Eating one of the four large pellets turns the tables: the ghosts turn blue, flee, and can be eaten for bonus points |
| **Behaviors** | Ghosts return to their home base after being eaten and rejoin the hunt; fruit appears occasionally as a bonus |
| **Feel** | Constant tension — the maze is never safe, and the player is always one wrong turn from being cornered |
| **Relationships** | The ghosts' speed and aggression rise as fewer dots remain, so the end of every maze feels like an escape |

### <font color="#79c0ff">Technical specification</font>

| Component | Specification |
|---|---|
| **Maze representation** | A 2D grid array; each cell stores wall, dot, pellet, or empty. Movement is validated against the grid before a position updates |
| **Game loop** | A fixed-timestep loop updates entity positions, checks collisions, then redraws the frame |
| **Ghost class** | `Ghost` holds `position`, `speed`, `state` (CHASE, SCATTER, FRIGHTENED, EATEN) and a `chooseDirection()` method; each ghost subclass overrides its targeting rule |
| **Power pellet logic** | Eating a pellet calls `setState(FRIGHTENED)` on all ghosts and starts a timer; when the timer expires, states revert |
| **Collision detection** | Each update, compare Pac-Man's grid cell with each ghost's cell; identical cells trigger `loseLife()` or `eatGhost()` depending on ghost state |
| **Score storage** | An integer score incremented by constants (`DOT = 10`, `PELLET = 50`); high scores persist to local storage |

Notice: the design column never names a class, an array, or a timer. The specification column never mentions tension, personality, or feel.

---

## <font color="#388bfd">Example 2 — ATM application (an app)</font>

### <font color="#79c0ff">App design</font>

| Element | Design description |
|---|---|
| **Purpose** | Lets a bank customer withdraw cash, deposit money, and check their balance without waiting for a teller |
| **Users** | Any customer with a bank card — including first-time users, in a hurry, possibly at night |
| **Experience** | The screen greets the user, asks for their card and PIN, and offers large, unmistakable buttons for the three main actions |
| **Trust** | The user must always feel their money is safe: every action ends with a clear confirmation, and a receipt is always offered |
| **Error behavior** | If a PIN is wrong, the machine explains gently and allows another try; after three failures it keeps the card to protect the owner |
| **Accessibility** | The interface offers large text, audio prompts through a headphone jack, and reachable controls for wheelchair users |

### <font color="#79c0ff">Technical specification</font>

| Component | Specification |
|---|---|
| **Account class** | `Account` holds `accountNumber`, `balance`, `pinHash`; methods `verifyPin(entry)`, `withdraw(amount)`, `deposit(amount)`, `getBalance()` |
| **Session flow** | Card read → `verifyPin()` (max 3 attempts, counter stored in `Session`) → menu state machine → transaction → receipt → session end |
| **Transaction records** | Each operation creates a `Transaction` object (`type`, `amount`, `timestamp`, `accountNumber`) appended to a persistent ledger |
| **Withdrawal rule** | `withdraw(amount)` throws `InsufficientFundsException` if `amount > balance`; the UI layer catches it and shows the error screen |
| **Security** | PINs are never stored in plain text — `pinHash` is compared against a hash of the entry; sessions time out after 30 seconds idle |
| **Hardware interface** | A `Dispenser` class wraps the cash hardware; `dispense(amount)` returns success or failure, and failure voids the transaction |

---

## <font color="#388bfd">The dividing line</font>

| Belongs in the design | Belongs in the tech spec |
|---|---|
| What the user sees, does, and feels | Classes, variables, and methods |
| Behaviors and their consequences | Algorithms and data structures |
| Value — why anyone would use this | Architecture — how the parts connect |
| Look, theme, tone, accessibility goals | Storage, performance, error handling |

> **Tip:**
> When reviewing any document, underline every sentence a non-programmer could not picture. Those sentences are specification — they may be excellent, but they do not belong in the design.

---

← Back to [Docs](README.md)
