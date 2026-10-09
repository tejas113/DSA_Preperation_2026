# 39. Combination Sum

**LC 39** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Target-Sum Backtracking (Unlimited Reuse)

---

## 1. Intuition

Picture a shop where every candidate is a coin you can use **as many times as you like**. Keep dropping coins into `path` until the total hits `target` (save it) or goes over (give up on that branch).

* `sum(path) == target` — a valid combination. Save `path.copy()` and `return`.
* `sum(path) > target` — all numbers are positive, so adding more only makes the total bigger. Dead end, `return`.
* `bt_dfs(i, path)` — passing **`i`, not `i + 1`**, means "the next pick may be this same number again". This is the one change that allows reuse.
* `range(start, len(candidates))` — you may repeat the current number or move forward, but never go back to an earlier index. That's why you get `[2, 3]` but never also `[3, 2]`.

**Recall:** reuse → recurse with `i`. No re-ordered duplicates → never look below `start`.

---

## 2. Template

* **Choose:** `path.append(candidates[i])`
* **Explore:** `bt_dfs(i, path)` — same index, so the number can be reused
* **Un-choose:** `path.pop()`
* **Prune / dedup:** `sum(path) > target` → `return`. `start` never goes backwards, so no re-ordered duplicates.

---

## 3. Code

```python
class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        res = []
        n = len(candidates)

        def bt_dfs(start, path):

            if sum(path) == target:
                res.append(path.copy())
                return 

            if sum(path) > target:
                return

            for i in range(start, len(candidates)):
                path.append(candidates[i])
                bt_dfs(i, path)
                path.pop()

        bt_dfs(0, [])
        return res

```

---

## 4. Dry Run (`candidates = [2, 3]`, `target = 5`)

```text
                               bt_dfs(0, [])
                              /             \
                     i=0 (use 2)             i=1 (use 3)
                            /                 \
             bt_dfs(0, [2])                    bt_dfs(1, [3])
            /              \                          |
   i=0 (use 2)            i=1 (use 3)            i=1 (use 3)
          /                  \                        |
bt_dfs(0, [2,2])        bt_dfs(1, [2,3])       bt_dfs(1, [3,3])
   /          \          sum=5 == target         sum=6 > target
i=0 (use 2)  i=1 (use 3)  res: [[2, 3]]            (RETURN)
  /            \
[2,2,2]       [2,2,3]
sum=6 > t     sum=7 > t
(RETURN)      (RETURN)

```

---

## 5. Complexity

* **Time: O(N^(T/M))** — `T` is the target and `M` the smallest candidate, so the path is at most `T/M` numbers deep, and each level tries up to `N` candidates. It's a loose upper bound (`start` cuts a lot). Each call also runs `sum(path)`, costing up to another `T/M`.
* **Space: O(T/M)** — recursion depth and `path` are at most `T/M` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Reuse allowed → `bt_dfs(i, path)`, not `i + 1`.
* Stop when `sum(path) > target` (numbers are positive).
* `start` never moves back → no `[3, 2]` after `[2, 3]`.
