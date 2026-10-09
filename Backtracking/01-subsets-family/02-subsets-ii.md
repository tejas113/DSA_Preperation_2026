# 90. Subsets II

**LC 90** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Backtracking with Duplicate Skipping

---

## 1. Intuition

Same as Subsets, but `nums` has repeated values and the answer must not repeat a subset. Sort first so equal numbers sit together, then never start a step with a value you already started that step with.

* `nums.sort()` — puts equal numbers side by side so a neighbor check can spot repeats.
* `if i > start and nums[i] == nums[i - 1]: continue` — inside one loop (one "step"), picking the second `2` would build the same subsets as the first `2`, so skip it.
* `i > start`, not `i > 0` — `i == start` is the first choice at this step and is always allowed. That is how `[2, 2]` still gets built: the second `2` is the *first* choice of the *next* step.
* Everything else is Subsets: save on entry, recurse at `i + 1`.

**Recall:** sort, then skip an equal value at the same step (`i > start`).

---

## 2. Template

* **Choose:** `path.append(nums[i])`
* **Explore:** `backtrack(i + 1, path)`
* **Un-choose:** `path.pop()`
* **Prune / dedup:** skip `nums[i]` if it equals `nums[i - 1]` and `i > start` (a repeat at the same step).

---

## 3. Code

```python
class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        res = []
        # Step 1: Sort to place duplicate numbers adjacent to each other
        nums.sort()
        n = len(nums)

        def backtrack(start: int, path: list[int]) -> None:
            # Append a copy of the current valid subset state
            res.append(path.copy())

            for i in range(start, n):
                # Step 2: Skip duplicates at the SAME decision level
                if i > start and nums[i] == nums[i - 1]:
                    continue

                # 1. Choose
                path.append(nums[i])
                
                # 2. Explore (move to i + 1)
                backtrack(i + 1, path)
                
                # 3. Backtrack
                path.pop()

        backtrack(0, [])
        return res

```

---

## 4. Dry Run (`nums = [1, 2, 2]`, already sorted)

```text
                     backtrack(0, []) -> res: [[]]
                   /        |        \
           i=0    /   i=1   |   i=2   \ (Skipped: nums[2] == nums[1] and 2 > 0)
                 /          |          \
     bt(1, [1])          bt(2, [2])    SKIPPED
     res: [[1]]          res: [[2]]
      /    \                 |
 i=1 /      \ i=2       i=2  |
    /        \               |
bt(2, [1,2])  bt(3, [1,2])  bt(3, [2,2])
res: [[1,2]]  SKIPPED       res: [[2,2]]
    |         (nums[2]==nums[1] and 2 > 1)
i=2 |
bt(3, [1,2,2])
res: [[1,2,2]]

```

**Final result:** `[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]`

---

## 5. Complexity

* **Time: O(n · 2^n)** — at most `2^n` subsets (fewer when values repeat), each copied at cost up to `n`. Sorting adds `O(n log n)`.
* **Space: O(n)** — recursion depth and `path` are at most `n` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Sort first, so equal values are neighbors.
* `i > start and nums[i] == nums[i - 1]` → skip a repeat at the same step.
* Going deeper is fine: `start` moves to `i + 1`, so `[2, 2]` still works.
