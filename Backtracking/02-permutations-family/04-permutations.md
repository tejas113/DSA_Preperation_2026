# 46. Permutations

**LC 46** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Permutation Backtracking

---

## 1. Intuition

Order matters here, so `[1, 2, 3]` and `[2, 1, 3]` are different answers. Any number not yet used can go in the next slot, so there is **no `start`** — the loop begins at the front every time and just skips numbers already in `path`.

* `for num in nums` — try every number at every level (not from a `start` index).
* `if num in path: continue` — skip a number that's already placed. This works because the values are all distinct.
* `len(path) == n` — every slot is filled: save `path.copy()` and `return`.
* `path.pop()` — remove the last number so the loop can try the next one in that slot.

**Recall:** full loop at every level, skip what's already in `path`.

---

## 2. Template

* **Choose:** `path.append(num)`
* **Explore:** `bt_dfs(path)`
* **Un-choose:** `path.pop()`
* **Prune / dedup:** `if num in path: continue` — never use a number twice in one permutation.

---

## 3. Code

```python
class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        result = []
        n = len(nums)

        def bt_dfs(path: list[int]):
            # Base Case: A permutation is complete when it contains all 'n' elements
            if len(path) == n:
                result.append(path.copy())
                return

            # Try every number in 'nums'
            for num in nums:
                # Constraint Check: Skip numbers already used in the current path
                if num in path:
                    continue

                # Choice: TAKE num
                path.append(num)

                # Recurse: Continue building the permutation
                bt_dfs(path)

                # Undo choice (Backtrack)
                path.pop()

        bt_dfs([])
        return result

```

---

## 4. Dry Run (`nums = [1, 2, 3]`)

```text
                               bt_dfs([])
                   /               |               \
            num=1 /          num=2 |          num=3 \
                 /                 |                 \
         bt_dfs([1])           bt_dfs([2])           bt_dfs([3])
         /         \           /         \           /         \
    num=2 /   num=3 \     num=1 /   num=3 \     num=1 /   num=2 \
         /           \         /           \         /           \
  bt_dfs([1,2]) bt_dfs([1,3]) bt_dfs([2,1]) bt_dfs([2,3]) bt_dfs([3,1]) bt_dfs([3,2])
       |             |             |             |             |             |
  num=3|        num=2|        num=3|        num=1|        num=2|        num=1|
   [1,2,3]       [1,3,2]       [2,1,3]       [2,3,1]       [3,1,2]       [3,2,1]

```

---

## 5. Complexity

* **Time: O(n² · n!)** — there are `n!` permutations. Each call loops over `n` numbers, and `num in path` scans up to `n` items. Using a `used[]` boolean array (as in #5) makes the check `O(1)` and brings it to `O(n · n!)`.
* **Space: O(n)** — recursion depth and `path` are at most `n` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* No `start`: loop over all of `nums` at every level.
* `num in path` → skip used numbers (only safe when values are distinct).
* `n!` permutations, each copied → at least `O(n · n!)`.
