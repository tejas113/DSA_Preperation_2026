# Topic 2 — Permutations Family

## The pattern

Fill the slots one by one. Any element that isn't used yet can go in the next slot, so there is **no `start`** — the loop begins at the front every time and skips what's already placed.

```python
def backtrack(path):
    if len(path) == n:                   # every slot filled
        save path; return
    for i in range(n):
        if used[i]: continue                                   # already placed
        if <twin skip>: continue    # only Permutations II: nums[i] == nums[i-1] and not used[i-1]
        used[i] = True; path.append(nums[i])                   # choose
        backtrack(path)                                        # explore
        path.pop(); used[i] = False                            # un-choose
```

## How to spot this topic

* The question says **"all permutations"**, **"all arrangements"**, **"all orderings"**, or **"rearrange all elements"**.
* **Order matters** — `[1, 2, 3]` and `[2, 1, 3]` are different answers.
* Every element is used **exactly once**, so every answer has length `n` and there are `n!` of them.
* Quick test: *would `[2, 1]` be a different answer from `[1, 2]`?* If yes, it's this topic.
* The input has repeated values but the output must not repeat → **sort, then the twin rule** (use identical values left to right).

**Not this topic if:** order doesn't matter (→ Topic 1), or answers can have different lengths (→ Topic 1).

## Problems here

| # | Problem | What changes from the pattern |
|---|---|---|
| 4 | [Permutations](04-permutations.md) | Base pattern — uses `num in path` instead of `used[]` (safe because values are distinct) |
| 5 | [Permutations II](05-permutations-ii.md) | Input has repeats → `used[]` on positions + twin rule |
