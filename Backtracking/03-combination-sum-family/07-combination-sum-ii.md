# 40. Combination Sum II

**LC 40** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Target-Sum Backtracking (Single Use + Duplicate Skipping)

---

## 1. Intuition

Now each candidate is a single card in your hand — every card can be used **once**. Some cards show the same number (two `1`s), but they are different cards. This is Combination Sum (#6) with **two changes**:

* `bt_dfs(i + 1, path)` instead of `bt_dfs(i, path)` — after using a card, move past it, so it can't be used again.
* `if i > start and candidates[i] == candidates[i - 1]: continue` — after sorting, identical cards sit side by side. Within one loop (one "step"), starting with the first `1` or the second `1` would build the same combinations, so we only try the first.
* Why `i > start`: `i == start` is the first card at this step and is always allowed. That's how `[1, 1, 6]` can use both `1`s — the second `1` is the *first* card of the *next* step.

**Recall:** `i + 1` = each card once. Sort + `i > start` = skip repeated values at the same step.

---

## 2. Template

* **Choose:** `path.append(candidates[i])`
* **Explore:** `bt_dfs(i + 1, path)` — next index, so the card can't be reused
* **Un-choose:** `path.pop()`
* **Prune / dedup:** `sum(path) > target` → `return`. Skip `candidates[i]` if it equals `candidates[i - 1]` and `i > start`.

---

## 3. Code

```python
class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        res = []
        # Sort to bring identical elements together for duplicate pruning
        candidates.sort()

        def bt_dfs(start, path):

            if sum(path) == target:
                res.append(path.copy())
                return

            if sum(path) > target:
                return

            for i in range(start, len(candidates)):

                # Skip duplicate elements at the SAME decision level (horizontal pruning)
                if i > start and candidates[i] == candidates[i - 1]:
                    continue

                # Choice: TAKE candidate
                path.append(candidates[i])
                
                # Recurse with i + 1 (single use per candidate element)
                bt_dfs(i + 1, path)
                
                # Backtrack
                path.pop()

        bt_dfs(0, [])
        return res

```

---

## 4. Dry Run (`candidates = [1a, 1b, 2]`, `target = 3`, already sorted)

```text
bt_dfs(0, [])
 ├─ i=0 (1a) → bt_dfs(1, [1])
 │     ├─ i=1 (1b) → bt_dfs(2, [1, 1])            sum = 2
 │     │     └─ i=2 (2) → [1, 1, 2]                sum = 4 > 3  ✗ (return)
 │     └─ i=2 (2)  → [1, 2]                        sum = 3 == target  ✔ save
 ├─ i=1 (1b) → SKIPPED   (i > start and 1b == 1a)
 └─ i=2 (2)  → bt_dfs(3, [2])                      sum = 2, nothing left to add  ✗
```

**Final result:** `[[1, 2]]`

---

## 5. Complexity

* **Time: O(N · 2^N)** — each element is either in or out, so about `2^N` calls (skipping repeats trims this). Every call runs `sum(path)`, costing up to `N`. Sorting adds `O(N log N)`.
* **Space: O(N)** — recursion depth and `path` are at most `N` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* `i + 1` → each element used once.
* Sort, then `i > start and candidates[i] == candidates[i - 1]` → skip repeats at the same step.
* Stop when `sum(path) > target`.
