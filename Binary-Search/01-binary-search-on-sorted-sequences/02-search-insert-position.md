# 35. Search Insert Position

**LC 35** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Boundary Search (lower bound / insertion point)

---

## 1. Intuition

If `target` is in `nums`, return its index like ordinary binary search. If it isn't, the search still narrows down to exactly one spot — the first position where a bigger value lives — and that's where `target` would have to be inserted to keep the array sorted.

- `nums[mid] == target` → found it, return `mid` directly.
- `nums[mid] < target` → `target` (and its insertion point) is strictly to the right, so `left = mid + 1`.
- `nums[mid] > target` → `target` could still be inserted at `mid`, so pull `right = mid - 1` but leave `left` where it can still reach `mid`.
- When the loop ends (`left > right`), `left` has been pushed past every value smaller than `target` and stopped at the first value `>= target` — that index *is* the answer.

**Recall:** same loop as exact-match search, but on a miss, `left` itself is the answer instead of `-1`.

## 2. Approach

* **Idea:** exact-match binary search (Form 1) that repurposes the final `left` as the insertion index instead of returning `-1` on a miss.
* **Data structure / pointers:** `left`/`right` are inclusive bounds; `mid` is the index tested this round.
* **Invariant:** everything strictly left of `left` is `< target`; everything strictly right of `right` is `>= target`. Once `left > right`, `left` is the first index that is `>= target`.
* **Edge cases:**
  - `target` larger than every element → `left` walks all the way to `len(nums)`.
  - `target` smaller than every element → `right` drops to `-1`, `left` stays `0`.
  - Single-element array, match or miss → loop runs once, then either returns `mid` or lands on `left ∈ {0, 1}`.
  - Empty array → `right = -1` from the start, loop body never runs, returns `left = 0`.

## 3. Code

```python
class Solution:

    def searchInsert(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        # left points to the correct insertion index when target is not found
        return left
```

## 4. Dry Run

`nums = [1, 3, 5, 6]`, `target = 2`

| Iteration | `left` | `right` | `mid` | `nums[mid]` | Comparison with `target` (`2`) | Next state |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 1 | 3 | `3 > 2` | `right = 0` |
| 2 | 0 | 0 | 0 | 1 | `1 < 2` | `left = 1` |
| End | 1 | 0 | — | — | `left > right` | return `1` |

## 5. Complexity

* **Time:** `O(log n)` — same halving as exact-match binary search; at most `log₂ n` iterations.
* **Space:** `O(1)` — only `left`, `right`, `mid` are kept.

## 6. Recall (30 seconds)

- It's exact-match binary search that also answers "where would this go?" on a miss.
- On a miss, the answer is whatever `left` ends up at — no separate insertion logic needed.
- `left` always lands on the first index whose value is `>= target` (or `len(nums)` if none is).
