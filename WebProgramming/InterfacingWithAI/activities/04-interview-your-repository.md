# Activity - Interview Your Repository

*Concept: Codex only knows the folder it was started in, so starting it in the right place is the first prompt, and checking its answers against the files is the last.*

![Left, a folder box for ~/HTCS_Projects/YOUR-PROJECT listing README.md, src/Blob.java, src/Tree.java, src/Commit.java, and .git/, captioned "you typed: cd here, then codex". An arrow labeled reads points to a Codex box showing its receipts: Explored, List ls -la, Read Blob.java. An arrow labeled answers points to the exchange: you ask which file hashes a blob, Codex answers Blob.java, sha1 over "blob size null byte" plus the bytes, and you open Blob.java to check it. A red footer warns that started on your Desktop it will confidently describe your Desktop, and a grey one that no receipts means an answer written from the file names alone.](../assets/codex-reads-your-repo.svg)

## Task

1. In your terminal, start Codex inside your Git project repository:
   ```bash
   cd ~/HTCS_Projects/YOUR-PROJECT
   codex
   ```
2. Ask the opening question the Codex docs suggest:
   ```
   Tell me about this project. What does it do, and which file does most of the work?
   ```
   Watch the lines it prints while it works (`Explored`, `List`, `Read`, file names). Those are the files it opened before answering.
3. Ask something only a reader of the code could answer, for example:
   ```
   Which method computes the SHA-1 hash of a blob, and exactly what bytes go into the hash?
   ```
4. Open the file it named in VS Code and check the claim line by line. Write down one thing it got right and one thing it got wrong, vague, or invented. If everything checks out, ask a harder question until something does not.
5. Ask for an opinion:
   ```
   What is one thing you would change in this code, and why?
   ```
   Decide whether you agree. Do not let it make the change today: if it asks for approval to edit, answer no.
6. Type `/quit`.
