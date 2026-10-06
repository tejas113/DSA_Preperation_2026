# 153. Find Minimum in Rotated Sorted Array

**LC 153** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Compare `mid` with the right end; the minimum is on the side with the drop

---

## 1. Intuition

The minimum element is exactly the rotation point — the one spot where a bigger value sits right before a smaller one. Comparing `nums[mid]` to `nums[right]` tells you which side of `mid` that drop is on, without ever needing to know `target`.

- `nums[mid] > nums[right]` → the drop (and the minimum) is strictly after `mid`, since `mid` is still "too high" to be in the same sorted run as `right`. Move `left = mid + 1`.
- `nums[mid] <= nums[right]` → `mid` through `right` is already a clean ascending run, so the minimum is either `nums[mid]` itself or somewhere to its left. Keep `mid` in play: `right = mid`.
- This is the same boundary-search shape as [#3 Find First and Last Position](../01-binary-search-on-sorted-sequences/03-find-first-and-last-position-of-element-in-sorted-array.md) — `while left < right`, `right = mid` to keep a candidate, `left = mid + 1` to discard one.
- When `left == right`, that index holds the minimum.

**Recall:** compare `nums[mid]` to `nums[right]`, not to `target` — bigger means the drop is to the right, smaller-or-equal means `mid` could still be (part of) the answer.

## 2. Approach

* **Idea:** boundary search (Form 2) where the "condition" being searched for is "am I inside the clean run that ends at `right`?" instead of a value comparison.
* **Data structure / pointers:** `left`/`right` bound the search range; `mid` is only ever compared against `nums[right]`, never against a target value.
* **Invariant:** the minimum is always within `[left, right]`; `nums[mid] > nums[right]` proves the minimum can't be at or before `mid`, so it's safe to discard that entire prefix.
* **Edge cases:**
  - Unrotated array → `nums[mid] > nums[right]` is never true, so `right` just walks down to `left`, landing on index `0`.
  - Single element → `left == right` from the start, loop body never runs, returns `nums[0]`.
  - Two elements → still correct: either they're in order (unrotated case) or `nums[0] > nums[1]` pushes `left` to the second element.

## 3. Code

```python
class Solution:

    def findMin(self, nums: list[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            # If mid element is greater than rightmost element, minimum is in right half
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                # Otherwise, minimum is at mid or in left half
                right = mid

        return nums[left]
```

## 4. Dry Run

`nums = [4, 5, 6, 7, 0, 1, 2]`

| Iteration | `left` | `right` | `mid` | `nums[mid]` | `nums[right]` | Comparison | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | 2 | `7 > 2` | `left = 4` |
| 2 | 4 | 6 | 5 | 1 | 2 | `1 <= 2` | `right = 5` |
| 3 | 4 | 5 | 4 | 0 | 1 | `0 <= 1` | `right = 4` |
| End | 4 | 4 | — | — | — | `left == right` | return `nums[4] = 0` |

## 5. Complexity

* **Time:** `O(log n)` — the `[left, right]` range halves every iteration, same as any boundary search.
* **Space:** `O(1)` — only `left`, `right`, `mid`.

## 6. Recall (30 seconds)

- The minimum is the rotation point — find it by comparing `nums[mid]` to `nums[right]`, not to a target.
- `nums[mid] > nums[right]` means the drop is to the right of `mid` — discard `mid` too (`left = mid + 1`).
- `nums[mid] <= nums[right]` means `mid` is inside (or is) the clean tail run — keep it as a candidate (`right = mid`).
