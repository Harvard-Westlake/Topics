# Review — Blockchain Vocabulary

*Originally covered in [Transactions and Ledgers](../README.md)*

---

| Term | Meaning |
|---|---|
| Ledger | File where transactions are recorded |
| Transaction | Agreement to exchange value between at least two parties |
| Pending | Announced, not yet permanently recorded |
| Confirmed | Written into the ledger |
| Hash | Unique fingerprint of a file's exact contents |
| Link | Previous file's hash copied into the top of the next file |
| Block / chain | Other names for the file / the linked files |
| Block reward | Payment for saving a block |

---

## Tasks

1. Write a plain-text ledger containing three transactions in `Sender -> Recipient  Amount` format.
2. Take the SHA-256 hash of your ledger and record it under a `// Confirmation #:` line.
3. Start a second file. Put the first file's hash at the top as `prev hash:`, then add two new transactions.
4. Change one digit of one amount in the first file. Re-hash it and compare against the `prev hash:` in your second file.
5. In two sentences, state which file(s) an attacker must rewrite to hide that change, and why the class would notice.
