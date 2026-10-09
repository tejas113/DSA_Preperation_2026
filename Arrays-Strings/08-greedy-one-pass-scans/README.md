# Topic 8 — Greedy & One-Pass Array Scans

## The pattern

Scan the array **once**, keeping a **running summary** of everything that matters so far. At each element, make the locally best choice and never come back to undo it.

```python
farthest = 0                                   # the summary: how far can I get so far?
for i, jump in enumerate(nums):
    if i > farthest:                           # I can't even reach this index
        return False
    farthest = max(farthest, i + jump)         # update the summary with what this index offers
return True
```

The summary changes by problem: **farthest reach** (jump games), **running tank and a reset point** (gas station), **a candidate and a vote count** (majority element), **the sum of every rise** (stock II).

## How to spot this topic

* You need **one answer** (yes/no, a count, an index) from a **single pass**, and the choice at each step doesn't need to be revisited.
* Words to look for: **"can you reach the end"**, **"minimum number of jumps"**, **"circular route"**, **"maximum profit with unlimited transactions"**, **"appears more than n/2 times"**.
* Quick test: *does taking the best local choice ever need to be undone later?* If **no**, it's this topic.

**Not this topic if:** a locally good choice can turn out wrong later (→ DP), or you need every possible answer (→ Backtracking).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 62 | Majority Element | Boyer-Moore: keep a candidate and a count; a different value cancels one vote |
| 63 | Jump Game | Track the farthest reachable index; fail if you fall behind it |
| 64 | Jump Game II | Track the end of the current jump's reach; when you pass it, count a jump |
| 65 | Gas Station | If the total gas ≥ total cost, a start exists; reset the start whenever the tank goes negative |
| 66 | Best Time to Buy and Sell Stock II | Add up every positive day-to-day rise |
| 67 | H-Index | Sort (or count by citation) and find the largest `h` with `h` papers of at least `h` citations |
| 68 | Candy | Two passes: left-to-right for the left neighbor, right-to-left for the right neighbor, take the max |
