# 77. Combinations

**LC 77** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Fixed-Length Include/Exclude Backtracking

---

## 1. Intuition

Pick a team of `k` numbers from `1..n`. Order doesn't matter (`[1, 2]` is the same team as `[2, 1]`), so always pick in **increasing order**. The team is finished the moment it has `k` members.

* `range(start, n + 1)` — only numbers at or after `start`.
* `bt_dfs(i + 1, path)` — the next pick must be bigger than `i`, so `[2, 1]` never appears.
* `len(path) == k` — team is full: save `path.copy()` and `return`. Without the `return`, the loop would keep adding and build lists longer than `k`.
* `path.pop()` — un-pick, so the loop can try the next number.

**Recall:** increasing picks, stop at length `k`.

---

## 2. Template

* **Choose:** `path.append(i)`
* **Explore:** `bt_dfs(i + 1, path)`
* **Un-choose:** `path.pop()`
* **Prune / dedup:** `start` moving to `i + 1` prevents re-ordered duplicates. (Optional speed-up, not in this code: stop the loop early when too few numbers remain to reach `k`.)

---

## 3. Code

```python
class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        res = []

        def bt_dfs(start, path):
            # Base Case: valid combination of length k found
            if len(path) == k:
                res.append(path.copy())
                return

            # Explore choices from 'start' to 'n'
            for i in range(start, n + 1):
                path.append(i)
                bt_dfs(i + 1, path)
                path.pop()

        bt_dfs(1, [])
        return res

```

---

## 4. Dry Run (`n = 4`, `k = 2`)

```text
                        bt_dfs(1, [])
                    /         |         \
           i=1     /     i=2  |          \  i=3
                  /           |           \
        bt_dfs(2, [1])    bt_dfs(3, [2])   bt_dfs(4, [3])
       /    |    \          /    \             |
  i=2 /  i=3| i=4 \    i=3 /  i=4 \        i=4 |
     /      |      \      /        \           |
[1,2]    [1,3]   [1,4]  [2,3]    [2,4]       [3,4]

```

Each leaf has `len(path) == 2`, so it is saved. Result: 6 combinations = C(4, 2).

---

## 5. Complexity

* **Time: O(k · C(n, k))** — there are `C(n, k)` combinations, and each `path.copy()` costs `k`.
* **Space: O(k)** — recursion depth and `path` never go past `k` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Pick in increasing order: loop from `start`, recurse at `i + 1`.
* Base case is `len(path) == k` — save a copy, then `return`.
* `C(n, k)` answers, each copied → `O(k · C(n, k))`.
