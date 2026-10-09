# Topic 6 — Build-a-String Backtracking

## The pattern

Build the answer one character at a time. At each position there is a small, fixed set of options; try each one, and only add an option that keeps the string valid. The recursion depth is the length of the result.

```python
def backtrack(<position or counters>, current):
    if len(current) == target_length:    # string is complete
        save current; return
    for ch in <options at this position>:                # e.g. letters of a digit, or '(' / ')'
        if <counter rule fails>: continue                # e.g. open_count < n, closing_count < open_count
        backtrack(<next position or counters>, current + ch)   # choose + explore
        # no pop: current + ch is a NEW string, so the parent's string is unchanged
```

## How to spot this topic

* The answer is a set of **strings built character by character**.
* There is **no array to pick elements from** — the input is just a number `n` or a short digit string.
* Each position has a **small fixed set of options**: the letters on a phone key, or `(` and `)`.
* Some problems add a **rule that must hold at every step**, tracked with counters (for example, never close more brackets than you opened).
* Quick test: *am I filling `n` slots with characters from a fixed menu?* If yes, it's this topic.

**Not this topic if:** you are picking elements from an input array (→ Topic 1 or 2), or cutting an existing string into pieces (→ Topic 4).

## Problems here

| # | Problem | What changes from the pattern |
|---|---|---|
| 14 | [Letter Combinations of a Phone Number](14-letter-combinations-of-a-phone-number.md) | Options come from a digit → letters map; no validity rule |
| 15 | [Generate Parentheses](15-generate-parentheses.md) | Options are `(` / `)`; counters decide which are allowed |
