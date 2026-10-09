# 78. Subsets

**LC 78** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Include/Exclude Backtracking (Power Set)

---

## 1. Intuition

Every element is either **in** or **out**, so `n` elements give `2^n` subsets. Every partial `path` you build on the way is already a valid subset, so save it at every step.

* `res.append(path.copy())` — runs at the start of every call, so every `path` is saved (including `[]`). No separate base case needed.
* `for i in range(start, n)` — only look at elements at or after `start`, so `[1, 2]` is built but `[2, 1]` never is.
* `backtrack(i + 1, path)` — the next pick must come after `i`, so each element is used at most once.
* `path.copy()` — save a copy, because `path` keeps changing.

**Recall:** save `path` on entry, loop from `start`, recurse at `i + 1`.

---

## 2. Template

* **Choose:** `path.append(nums[i])`
* **Explore:** `backtrack(i + 1, path)`
* **Un-choose:** `path.pop()`
* **Prune / dedup:** none needed — moving `start` forward is what prevents repeats.

---

## 3. Code

```python
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        n = len(nums)

        def backtrack(start: int, path: list[int]) -> None:
            # Append a copy of the current valid state at every step
            res.append(path.copy())

            # Explore choices from 'start' onwards
            for i in range(start, n):
                # 1. Choose
                path.append(nums[i])
                
                # 2. Explore (only move forward to avoid duplicates)
                backtrack(i + 1, path)
                
                # 3. Unchoose / Backtrack
                path.pop()

        backtrack(0, [])
        return res

```

### Alternative: Binary Include/Exclude

Same answer, seen as a yes/no decision per element. Subsets are saved only at the leaves (`i == n`).

```python
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        n = len(nums)

        def dfs(i: int, path: list[int]) -> None:
            if i == n:
                res.append(path.copy())
                return

            # Decision 1: Include nums[i]
            path.append(nums[i])
            dfs(i + 1, path)

            # Decision 2: Exclude nums[i]
            path.pop()
            dfs(i + 1, path)

        dfs(0, [])
        return res

```

---

## 4. Dry Run (`nums = [1, 2, 3]`)

```text
                     backtrack(0, []) -> res: [[]]
                    /       |        \
            i=0    /   i=1  |   i=2   \
                  /         |          \
      bt(1, [1])         bt(2, [2])     bt(3, [3])
      res: [[1]]         res: [[2]]     res: [[3]]
       /    \                 |
  i=1 /      \ i=2       i=2  |
     /        \               |
bt(2, [1,2])  bt(3, [1,3])  bt(3, [2,3])
res: [[1,2]]  res: [[1,3]]  res: [[2,3]]
     |
 i=2 |
bt(3, [1,2,3])
res: [[1,2,3]]

```

---

## 5. Complexity

* **Time: O(n · 2^n)** — `2^n` subsets are saved, and each `path.copy()` costs up to `n`.
* **Space: O(n)** — recursion depth and `path` are at most `n` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Every `path` is a subset — save it on entry.
* `start` + `i + 1` = no repeats, no re-ordering.
* `2^n` subsets, each copied → `O(n · 2^n)`.
