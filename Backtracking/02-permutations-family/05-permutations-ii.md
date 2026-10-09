# 47. Permutations II

**LC 47** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Permutation Backtracking with Duplicate Skipping

---

## 1. Intuition

Permutations, but the input has repeated numbers and the answer must not repeat. Sort so identical numbers (twins) sit side by side, then force twins to be used **left to right**. Swapping two identical balls gives the same permutation, so only one order is allowed.

* `visited = [False] * n` — track *positions*, not values. `num in path` would wrongly block a second `1`.
* `nums.sort()` — puts twins next to each other so `nums[i] == nums[i - 1]` can detect them.
* `if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]: continue` — the twin rule:
  * left twin **not** in `path` → it was already tried at this slot and undone, so the right twin would repeat it. **Skip.**
  * left twin **in** `path` → this is the legitimate second copy. **Allow** (that's how `[1, 1, 2]` is built).
* Without the `not visited[i - 1]` part, the check would also block `[1, 1, 2]` and lose real answers.

**Recall:** sort, use `visited[]`, and let the right twin go only after the left twin.

---

## 2. Template

* **Choose:** `visited[i] = True` and `path.append(nums[i])`
* **Explore:** `bt_dfs(path)`
* **Un-choose:** `path.pop()` and `visited[i] = False`
* **Prune / dedup:** skip if `visited[i]`, or if it's a right twin whose left twin isn't in use.

---

## 3. Code

```python
class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        res = []
        n = len(nums)
        # Step 1: Sort to bring duplicate elements together
        nums.sort()

        visited = [False] * n
        
        def bt_dfs(path: list[int]):
            # Base Case: Valid unique permutation completed
            if len(path) == n:
                res.append(path.copy())
                return

            for i in range(n):
                # 1. Skip elements already selected in the current branch
                if visited[i]:
                    continue

                # 2. Skip duplicate choices at the SAME decision level
                if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                    continue
                
                # Make choice
                visited[i] = True
                path.append(nums[i])

                # Recurse
                bt_dfs(path)

                # Backtrack
                path.pop()
                visited[i] = False

        bt_dfs([])
        return res

```

---

## 4. Dry Run (`nums = [1a, 1b, 2]`, already sorted)

```text
                                   bt_dfs([]) -> res: []
                      /                    |                     \
          i=0 (1a)   /         i=1 (1b)    |                      \ i=2 (2)
                    /       (SKIPPED: not visited[0])              \
             bt_dfs([1a])                                      bt_dfs([2])
             /          \                                      /         \
   i=1 (1b) /            \ i=2 (2)                   i=0 (1a) /           \ i=1 (1b)
           /              \                                  /             (SKIPPED)
    bt_dfs([1a, 1b])   bt_dfs([1a, 2])               bt_dfs([2, 1a])
          |                  |                              |
    i=2   |            i=1   |                        i=1   |
  bt_dfs([1a, 1b, 2])  bt_dfs([1a, 2, 1b])           bt_dfs([2, 1a, 1b])
   res: [[1, 1, 2]]     res: [[1, 1, 2],              res: [[1, 1, 2], [1, 2, 1],
                               [1, 2, 1]]                    [2, 1, 1]]

```

---

## 5. Complexity

* **Time: O(n · n!)** — at most `n!` permutations (fewer with repeats). Each call loops over `n` positions with `O(1)` checks, and each result is copied at cost `n`. Sorting adds `O(n log n)`.
* **Space: O(n)** — `visited`, `path` and the recursion depth are each at most `n` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Sort first; track positions with `visited[]`.
* `nums[i] == nums[i - 1] and not visited[i - 1]` → skip (twins go left to right).
* `visited[i - 1]` True means the left twin is already placed, so the right twin is allowed.
