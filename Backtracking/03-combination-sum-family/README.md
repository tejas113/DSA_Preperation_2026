# Topic 3 — Combination Sum Family (Target-Sum Backtracking)

## The pattern

It is the Subsets loop (`start` moves forward) plus a running total. Add numbers until the total **hits** the target (save it) or **passes** it (give up). The one decision that changes between problems: can a number be reused?

```python
def backtrack(start, path):
    if sum(path) == target:              # hit the target
        save path; return
    if sum(path) > target:               # passed it — numbers are positive, so it only grows
        return
    for i in range(start, n):
        if <duplicate skip>: continue    # only Combination Sum II: i > start and c[i] == c[i-1]
        path.append(candidates[i])                   # choose
        backtrack(i, path)                           # explore: i = reuse allowed
        #        backtrack(i + 1, path)              #          i + 1 = each number once
        path.pop()                                   # un-choose
```

## How to spot this topic

* You get a **list of numbers and a target**, and must return **all the combinations that add up to it**.
* The wording tells you the reuse rule: **"may be used an unlimited number of times"** → recurse at `i`. **"each number may be used once"** → recurse at `i + 1`.
* The input may contain **duplicate values** while the output must be unique → sort, then skip `i > start` repeats.
* Quick test: *am I picking numbers whose sum must equal something, and listing them all?* If yes, it's this topic.

**Not this topic if:** the question asks for a **count** or a **minimum number of items** (that is DP, e.g. Coin Change), or there is no target (→ Topic 1).

## Problems here

| # | Problem | What changes from the pattern |
|---|---|---|
| 6 | [Combination Sum](06-combination-sum.md) | Reuse allowed → recurse with `i` |
| 7 | [Combination Sum II](07-combination-sum-ii.md) | Each number once → recurse with `i + 1`, plus sort + skip `i > start` repeats |
