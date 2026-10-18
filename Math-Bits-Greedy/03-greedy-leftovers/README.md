# Topic 3 — Greedy Leftovers

## The pattern

Make the best local choice at each step and **never undo it**. In this topic the scan is over characters, ranges or groups, and the "running summary" is a tiny piece of state.

```python
# Partition Labels: cut as soon as you reach the farthest last-occurrence of everything in the group
last = {ch: i for i, ch in enumerate(s)}
start = end = 0
for i, ch in enumerate(s):
    end = max(end, last[ch])
    if i == end:
        sizes.append(end - start + 1)
        start = i + 1

# Valid Parenthesis String: track the RANGE of possible open counts
low = high = 0
for ch in s:
    low  += 1 if ch == "(" else -1       # "*" as ")" gives the lowest count
    high += 1 if ch != ")" else -1       # "*" as "(" gives the highest count
    if high < 0: return False            # too many ")" even in the best case
    low = max(low, 0)                    # an open count can't be negative
return low == 0
```

## How to spot this topic

* The question asks for a **yes/no or a count** from a **single pass**, and a local choice never needs to be undone.
* Words to look for: **"partition into as many parts as possible"**, **"`*` can be `(`, `)` or empty"**, **"can the cards be grouped"**, **"circular subarray"**.
* Quick test: *does keeping only a small summary (a farthest index, a range of counts) let me decide as I scan?* If yes, it's this topic.

**Not this topic if:** a local choice can turn out wrong later (→ DP), or you need every valid answer (→ Backtracking). For greedy scans over number arrays (Jump Game, Gas Station), see Arrays-Strings, Topic 8.

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 18 | Partition Labels | Store each letter's last index; cut when `i` reaches the farthest last index seen |
| 19 | Valid Parenthesis String | Track `low` and `high` counts of possible open brackets; `*` widens the range |
| 20 | Maximum Sum Circular Subarray | Answer = max(max subarray, total − min subarray); handle the all-negative case |
| 21 | Hand of Straights | Sort (or use a min-heap), then repeatedly start a group at the smallest card |
| 22 | Merge Triplets to Form Target Triplet | Keep only triplets with no value above the target; check that each target value is matched |
