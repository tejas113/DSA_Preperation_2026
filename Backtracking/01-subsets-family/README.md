# Topic 1 — Subsets Family (Include/Exclude Backtracking)

## The pattern

Go through the elements in order. At each step, pick any element from `start` onwards, then move `start` **past** it. Because you never look back, `[1, 2]` gets built but `[2, 1]` never does.

```python
def backtrack(start, path):
    save path                        # Subsets: every call.  Combinations: only when len(path) == k
    for i in range(start, n):
        if <duplicate skip>: continue    # only Subsets II: i > start and nums[i] == nums[i-1]
        path.append(nums[i])             # choose
        backtrack(i + 1, path)           # explore (i + 1: each element used at most once)
        path.pop()                       # un-choose
```

## How to spot this topic

* The question says **"all subsets"**, **"power set"**, or **"all combinations"** / **"choose k from n"**.
* **Order doesn't matter** — `[1, 2]` and `[2, 1]` count as the same answer.
* Each element is used **at most once**.
* Quick test: *would `[2, 1]` be a duplicate of `[1, 2]`?* If yes, it's this topic.
* The input has repeated values but the output must not repeat a subset → **sort, then skip `i > start` repeats**.

**Not this topic if:** order matters (→ Topic 2), or there is a target sum (→ Topic 3).

## Problems here

| # | Problem | What changes from the pattern |
|---|---|---|
| 1 | [Subsets](01-subsets.md) | Base pattern — save on every call |
| 2 | [Subsets II](02-subsets-ii.md) | Input has repeats → sort + skip `i > start` repeats |
| 3 | [Combinations](03-combinations.md) | Save only when `len(path) == k` |
