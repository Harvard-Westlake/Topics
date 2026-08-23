<div align="center">

# Topics

*<font color="#8b949e">Honors Topics computer science curriculum</font>*

</div>

---

This repository holds every lesson in the **Honors Topics** computer science curriculum. Lessons are student-facing, organized by topic, and written as GitHub-rendered Markdown that the course hub imports directly for scheduling.

## <font color="#388bfd">Why the Curriculum Lives in Git</font>

The curriculum changes every year, and Git is what makes those changes manageable:

- **Branching for year-over-year revision** — each year's updates are developed on branches and merged in when ready, so material can be reworked without disturbing what is currently being taught.
- **History of progression** — the commit history preserves how every lesson has evolved across years: what changed, when, and why.
- **Pick-and-choose scheduling** — every lesson, assignment, review fragment, and milestone is its own file, so the course hub can schedule any subset of items in any order and recombine them differently each year.

## <font color="#388bfd">What This Design Solves</font>

The folder layout is deliberate. Three problems drive it:

### <font color="#79c0ff">Planning flexibility</font>

Content lives in its own topic folder — never in a fixed sequence. The structure and order in which topics are combined into a course is assembled dynamically at planning time, and it is *meant* to change: as the technology landscape shifts, units can be reordered, dropped, or recombined for a new year without rewriting a single lesson.

### <font color="#79c0ff">Class-specific adjustments</font>

Review and supplemental material are composable fragments, each in its own file beside the lesson that introduced the concept. Any teacher can attach any fragment to any assignment, for whichever class needs it, on demand — so two sections of the same course can run the same lessons with different reinforcement, without forking the curriculum.

### <font color="#79c0ff">Content without built-in numbering</font>

No lesson or topic carries an inherent number — there is no "Unit 3" baked into a folder name. Unit numbers and day counts are assigned when a course is planned, not when content is written. When a unit needs more material, the new lesson is simply added to its topic's folder. That keeps collaboration focused — contributors can work deeply inside one topic — while leaving planners free to renumber, resequence, or refactor units without touching the content itself.

## <font color="#388bfd">Lesson Types</font>

| | Type | What it means |
|---|---|---|
| <font color="#3fb950">■</font> | **Environment Configuration** | Sets up your machine and tools so you are ready to code |
| <font color="#a371f7">■</font> | **Learning** / **Reinforce** | Introduces new concepts and builds on them through practice |
| <font color="#e3b341">■</font> | **Review** | Revisits and consolidates material already covered |

---

## <font color="#388bfd">Table of Contents</font>

<font color="#3fb950">■ Environment Configuration</font>

**[Computer Setup](ComputerSetup/)**  
Step-by-step guide to standardizing your terminal environment and installing developer tools on Mac or PC.

- [Initial Install](ComputerSetup/InitialInstall/) — terminal, Git, GitKraken, VS Code, and Java 25 on Mac or PC

<font color="#a371f7">■ Learning</font>

**[Terminal](Terminal/)**  
Introduction to the command line: how commands work, navigating the file system, listing files, and creating your own structure.

- [Terminal Basics](Terminal/Basics/) — navigation, listing, creating files and folders, `find`, and `man`

**[Git Usage](GitUsage/)**  
Core Git concepts and workflows: staging, committing, branching, merging, and contributing through forks and pull requests.

- [Repositories and Commits](GitUsage/RepositoriesAndCommits/) — repositories, cloning, staging, committing, pushing, and pulling
- [Branching and Merging](GitUsage/BranchingAndMerging/) — branches, `git merge`, fast-forward merges, pull requests, and `.gitignore`
- [Forks and Collaboration](GitUsage/ForksAndCollaboration/) — forking, upstream remotes, syncing forks, and cross-fork pull requests
- [File Hashing and Integrity](GitUsage/FileHashing/) — hash functions, collision probability, `sha256sum`, Java file I/O, and Git's content addressing

**[MiniGPT](MiniGPT/)**  
Project Strata: build a tiny decoder-only transformer language model in Java from first principles — tokenization, attention, backpropagation, training, and honest evaluation against a Markov baseline.

- [Patterns Become Tokens](MiniGPT/Tokenizer/) — a Byte Pair Encoding tokenizer that counts adjacent pairs and merges the most frequent
- [The Reader with One-Step Memory](MiniGPT/MarkovBaseline/) — uniform, unigram, and bigram baselines with held-out evaluation
- [The Hand-Built Spotlight](MiniGPT/FixedAttention/) — causal self-attention with hand-written rules, no learning yet
- [A Table That Learns](MiniGPT/TrainableBigram/) — softmax, cross-entropy loss, and gradient descent on a trainable bigram
- [From Exact Symbols to Features](MiniGPT/ObjectNetwork/) — token embeddings and an object-oriented neural network, forward pass only
- [Following the Error Backward](MiniGPT/ScalarAutograd/) — backpropagation and a scalar automatic-differentiation engine
- [From Glass Box to Engine](MiniGPT/DenseEngine/) — the same mathematics on dense primitive arrays
- [Learning What to Look For](MiniGPT/SingleHeadAttention/) — trainable single-head causal attention, proven on synthetic tasks
- [A Team of Readers](MiniGPT/TransformerBlock/) — multi-head attention, feed-forward layers, and a complete transformer block
- [The Machine Writes](MiniGPT/TrainingAndGeneration/) — end-to-end training, Adam, checkpointing, and text generation
- [The Trial of the Archive](MiniGPT/Capstone/) — the capstone experiment, ablation, and responsible evaluation

**[Web Programming](WebProgramming/)**  
Build and ship a live, database-backed educational widget — hosted on Firebase, styled to a production spec, and hardened through peer review — while learning to direct AI as a manager rather than lean on it.

- [Interfacing with AI](WebProgramming/InterfacingWithAI/) — assumptions in prompting, AI-guided research, and first HTML pages in Cursor
- [Website Hosting](WebProgramming/WebsiteHosting/) — HTML/CSS/JS roles and deploying a live site with the Firebase CLI
- [JavaScript and Coding with Cursor](WebProgramming/JavaScriptAndCursor/) — web event binding, classes, and Cursor's Ask/Plan/Agent modes
- [Debugging JavaScript](WebProgramming/DebuggingJavaScript/) — DevTools, console methods, and reading stack traces
- [The Learning Widget Project](WebProgramming/LearningWidget/) — research, plan, and build an educational widget published via GitHub and Firebase
- [Persistence and Intermediate Web](WebProgramming/PersistenceAndIntermediateWeb/) — why page state vanishes and the ladder of ways websites remember
- [Databases and Collections](WebProgramming/DatabasesAndCollections/) — local storage vs cookies, Firestore CRUD, and security rules
- [UX and Behavior Tracking](WebProgramming/UXAndBehaviorTracking/) — engagement speed, navigation, user flow, and heatmaps
- [Widget Iteration from Feedback](WebProgramming/WidgetIteration/) — a shrinking feedback.md and a zero-error console
- [Collaborative Peer Review](WebProgramming/PeerReview/) — reviewing a partner's PR with your grade attached to the approval

**[App Design and Planning](AppDesign/)**  
Design a product for users before any implementation talk, converge as a class on one design, translate it into a technical specification, and plan the MVP — the exact path a real product team walks.

- [Learning to Design](AppDesign/LearningToDesign/) — describe a partner's game in plain language, then separate design from technical specification
- [Communicating Design](AppDesign/CommunicatingDesign/) — brainstorm and pitch an idea in terms of user value, with zero implementation talk
- [The Design Challenge](AppDesign/DesignChallenge/) — design a school-scale app or game against real business requirements
- [Design Review](AppDesign/DesignReview/) — review a partner's design in a branch without sliding into implementation
- [Iterative Design](AppDesign/IterativeDesign/) — define "better," then improve a chosen design with meaningful commits
- [Team Design and Pitch](AppDesign/TeamDesignAndPitch/) — present to a team and integrate the best ideas into one cohesive design
- [Group Design Review](AppDesign/GroupDesignReview/) — open pull requests on the three designs you back the most
- [Design Refinement](AppDesign/DesignRefinement/) — walk every idea in small groups until the design passes the detail test
- [Merging Designs](AppDesign/MergeDesigns/) — combine the class's designs pairwise using a structured conversation protocol
- [UX and Art Direction](AppDesign/UXAndArtDirection/) — choose a track: user flows and wireframes, or mood boards and art assets
- [Ambiguity and Architecture](AppDesign/AmbiguityAndArchitecture/) — eliminate ambiguity from the design and research engines and platforms
- [Technical Specification](AppDesign/TechnicalSpecification/) — translate the design into a tech spec with class diagrams and per-feature specs
- [Combining Tech Specs](AppDesign/CombineTechSpecs/) — merge individual specs into one prioritized, color-coded document
- [MVP Planning](AppDesign/MVPPlanning/) — draw the MVP line through the tech spec and order the work by dependency
- [Scrum and Stand-ups](AppDesign/ScrumAndStandup/) — complete the detailed design and run timed stand-up updates

**[Hashing, Cryptography, and P2P Networks](HashingCryptoP2P/)**  
The foundation stones of digital trust — fingerprinting data with hashes, proving identity with public/private key signatures, and sharing files across networks with no central server.

- [Hexadecimal and Hashing](HashingCryptoP2P/HexadecimalAndHashing/) — base-16 conversions, the four hash-function properties, and hashing vs encryption
- [Digital Signatures](HashingCryptoP2P/DigitalSignatures/) — key pairs, signing a message's hash, and verifying a partner's signature with runnable Python scripts
- [Peer-to-Peer Networks](HashingCryptoP2P/PeerToPeerNetworks/) — client-server vs P2P, the torrent protocol's hash-verified pieces, and why P2P survives node loss

**[Blockchains and Bitcoin](Blockchains/)**  
Builds the idea of a blockchain from hashing, signatures, and P2P networking — from a shared class ledger of IOUs to deploying your own token on a real test blockchain.

- [Transactions and Ledgers](Blockchains/TransactionsAndLedgers/) — build a shared class ledger, hash it, and discover why hash-linking files makes history unchangeable
- [Bitcoin and Wallets](Blockchains/BitcoinAndWallets/) — hash difficulty, minting, fees, block size and timing, then create a wallet and interrogate what it gives you
- [Mempool and Wallet Programming](Blockchains/MempoolAndWalletProgramming/) — where transactions wait, what faucets are, and a BitcoinJ wallet you program in Java
- [Keys and Layer 2](Blockchains/KeysAndLayerTwo/) — RSA key math worked by hand, multi-signature keys, and payment networks built on Bitcoin
- [Smart Chains and Wrapped Bitcoin](Blockchains/SmartChainsAndWrappedBitcoin/) — blockchains that run code, how Bitcoin gets wrapped onto Ethereum, and your first testnet transaction
- [Tokens in Java](Blockchains/TokensInJava/) — a complete ticketing token in plain Java: run it, personalize it, explain it
- [Proof of Stake](Blockchains/ProofOfStake/) — validators, staking, rewards, and slashing, simulated live with a classroom exercise
- [Writing Code on Ethereum](Blockchains/WritingCodeOnEthereum/) — smart contracts, Ethereum's state model, famous exploits, and a first testnet deployment
- [Vyper with Custom Behavior](Blockchains/VyperCustomBehavior/) — Vyper syntax and a deployed contract with behavior you invent
- [Deploying an ERC20 Token](Blockchains/ERC20Deployment/) — read the real ERC20 example, deploy your customized token to Sepolia, mint it to classmates
- [Crypto Research Project](Blockchains/CryptoResearchProject/) — research and present a top-100 cryptocurrency: who, what, how, where, when, why

**[Advanced EVM Programming](AdvancedEVM/)**  
Treat the Ethereum Virtual Machine as a real application platform: token vaults, markets with no market-maker, files that live nowhere and everywhere, and a web app whose backend is a blockchain.

- [Wrapped Tokens and Layer 2](AdvancedEVM/WrappedTokensAndLayerTwo/) — contract vaults, wrap/unwrap mechanics, rollups, and cross-chain bridging
- [Decentralized Finance](AdvancedEVM/DecentralizedFinance/) — automated market makers, liquidity pools, and the risks of bankless finance
- [IPFS and NFTs](AdvancedEVM/IPFSAndNFTs/) — content-addressed storage, ERC-721 tokens, and reading a live NFT contract on Etherscan
- [Web2 to Web3 App](AdvancedEVM/Web2Web3App/) — the four things a browser needs to reach a blockchain, and a website that drives your own contract

<font color="#a371f7">■ Reinforce</font>

**[Git Project](GitProject/)**  
Recreate the core of Git in Java — hashing, blobs, trees, and commits — to understand how version control actually works under the hood.

- [Project Setup](GitProject/ProjectSetup/) — GitHub repo, `Git.java`, `.gitignore`, and initial HEAD
- [Initialization and Blobs](GitProject/InitAndBlobs/) — `init()`, SHA-1 hashing, blob files, and the index
- [Trees](GitProject/Trees/) — index formatting, tree files, and building trees from staged files
- [Commits](GitProject/Commits/) — commit files, HEAD chain, and the `GitWrapper` interface
- [Branches](GitProject/Branches/) — branch pointers and HEAD *(coming soon)*

**[Group Programming](GroupProgramming/)**  
Working like an engineering team — work tracked in issues, shipped in branches, reviewed by non-authors, merged into a protected main, and handed off with documentation a stranger can continue.

- [Deliverables and Issue Tracking](GroupProgramming/DeliverablesAndIssueTracking/) — why communication beats raw code, and the issue → branch → review cycle
- [Sprint Work](GroupProgramming/SprintWork/) — planning sprints, committing to deliverables you can deliver, and proving your work runs
- [MVP and Merge Discipline](GroupProgramming/MVPAndMergeDiscipline/) — what an MVP is, and merging main into your branch and testing before every PR
- [Code Review and MVP Presentation](GroupProgramming/CodeReviewAndPresentation/) — demoing the MVP from main as a team and defending your own merged code
- [Issues as Work Requests](GroupProgramming/IssuesAsWorkRequests/) — writing GitHub Issues precise enough for a stranger to implement without questions
- [Refactoring and the README](GroupProgramming/RefactorAndReadme/) — cleaning code to match the tech spec and documenting for whoever comes next
- [Help a Classmate](GroupProgramming/HelpAClassmate/) — forking a classmate's project, running it from their README, and contributing a feature by PR
- [Final Wrap-Up and Deployment](GroupProgramming/FinalWrapUp/) — closing out pull requests, deploying live, and shipping a usable final product


<font color="#e3b341">■ Review</font>

**[DND Review + DND Review Test](DNDReview/)**  
TODO: one-sentence topic summary.

- [DND Review](DNDReview/DNDReview/) — TODO: one-line summary
