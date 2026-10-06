# 704. Binary Search

**LC 704** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Exact-Match Binary Search

---

## 1. Intuition

`nums` is sorted, so looking at one middle value tells you which half the target can possibly be in — you never have to look at the other half. Keep shrinking the range `[left, right]` around that fact until you either land on `target` or run out of range.

- `mid` is just a guess — the value there decides which half survives.
- `nums[mid] == target` → done, return `mid` immediately.
- `nums[mid] < target` → everything at or before `mid` is too small, so `left = mid + 1`.
- `nums[mid] > target` → everything at or after `mid` is too big, so `right = mid - 1`.
- The loop condition `left <= right` is what lets a single-element range still get checked; once `left > right` there's nothing left to check.

**Recall:** sorted array + exact target → shrink `[left, right]` by comparing `nums[mid]` to `target`, return `-1` when the pointers cross.

## 2. Approach

* **Idea:** classic exact-match binary search (Form 1 from the README) — the answer, if it exists, is `mid` itself.
* **Data structure / pointers:** `left` and `right` are inclusive bounds of the current search range; `mid` is the index being tested this iteration.
* **Invariant:** if `target` is in `nums`, its index always lies within `[left, right]`. Each iteration either finds it or provably removes `mid` from that range.
* **Edge cases:**
  - Empty array (`nums = []`) → `right = -1` before the loop starts, loop body never runs, returns `-1`.
  - Single element, match or miss → loop runs exactly once, then either returns immediately or `left > right`.
  - `target` smaller than every element → `right` shrinks to `-1`.
  - `target` larger than every element → `left` shrinks to `len(nums)`.

## 3. Code

```python
class Solution:

    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            # Prevents potential integer overflow in languages like C++/Java: left + (right - left) // 2
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1
```

## 4. Dry Run

`nums = [-1, 0, 3, 5, 9, 12]`, `target = 9`

| Iteration | `left` | `right` | `mid` | `nums[mid]` | Comparison with `target` (`9`) | Next state |
|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 | 3 | `3 < 9` | `left = 3` |
| 2 | 3 | 5 | 4 | 9 | `9 == 9` | return `4` |

## 5. Complexity

* **Time:** `O(log n)` — every iteration halves the size of `[left, right]` (either `left` jumps past the midpoint or `right` drops before it), so the loop runs at most `log₂ n` times.
* **Space:** `O(1)` — only the three index variables `left`, `right`, `mid` are used; no extra data structures.

## 6. Recall (30 seconds)

- Sorted array, exact target → binary search, not linear scan.
- Loop while `left <= right`; compare `nums[mid]` to `target` to decide `left = mid + 1` or `right = mid - 1`.
- Pointers crossing (`left > right`) means the target isn't in the array — return `-1`.
