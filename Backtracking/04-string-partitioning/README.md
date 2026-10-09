# Topic 4 — String Partitioning Backtracking

## The pattern

Cut the string with scissors. Standing at `start`, decide where the **first piece** ends, check the piece is valid, then solve the same problem on the rest of the string. When `start` reaches the end, the cuts so far are a complete answer.

```python
def backtrack(start, path):
    if start == n:                       # whole string used up
        save path; return
    for end in range(start + 1, n + 1):  # every possible end of the first piece
        piece = s[start:end]
        if not <piece is valid>: continue    # palindrome / dictionary word / 0–255 with no leading zero
        path.append(piece)               # choose
        backtrack(end, path)             # explore: the rest starts where this piece ended
        path.pop()                       # un-choose
```

## How to spot this topic

* The input is a **string**, and you must **split it into pieces** (in order, without rearranging characters).
* Each piece must follow a rule: **"is a palindrome"**, **"is in the dictionary"**, **"is a number from 0 to 255"**.
* The answer is **all the ways** to split it — a list of lists, or a list of sentences / addresses.
* Quick test: *am I choosing where to put the cuts?* If yes, it's this topic.

**Not this topic if:** you are picking elements from an array (→ Topic 1). If the question only asks **"can it be split?"** (yes/no) or **"how many ways?"**, use DP (e.g. Word Break) instead of listing everything.

## Problems here

| # | Problem | What changes from the pattern |
|---|---|---|
| 8 | [Palindrome Partitioning](08-palindrome-partitioning.md) | Piece is valid if it is a palindrome |
| 9 | [Restore IP Addresses](09-restore-ip-addresses.md) | Exactly 4 pieces of 1–3 digits, no leading zero, at most 255 |
| 10 | [Word Break II](10-word-break-ii.md) | Piece is valid if it is in the dictionary (memoizing on `start` is the follow-up) |
