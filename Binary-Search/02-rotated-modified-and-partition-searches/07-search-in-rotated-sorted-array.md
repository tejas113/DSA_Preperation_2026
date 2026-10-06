# 33. Search in Rotated Sorted Array

**LC 33** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** One half is always sorted — check whether the target lies inside it

---

## 1. Intuition

Rotating a sorted array breaks the "everything to the left is smaller" property globally, but cutting it at `mid` always leaves at least one of the two halves still plainly sorted. So the question each iteration isn't "is `target` bigger or smaller than `nums[mid]`?" — it's "which half is sorted, and does `target` fall inside that sorted half's range?"

- `nums[left] <= nums[mid]` → the left half `[left, mid]` is sorted (no rotation point crossed it).
- In that case, `nums[left] <= target < nums[mid]` tells you `target` is inside that sorted left range, so hunt there (`right = mid - 1`); otherwise it must be in the other half (`left = mid + 1`).
- Otherwise the right half `[mid, right]` is the sorted one, and the same idea applies mirrored: `nums[mid] < target <= nums[right]` means hunt right (`left = mid + 1`), else go left (`right = mid - 1`).
- `nums[mid] == target` is still checked first and returns immediately, same as plain binary search.

**Recall:** figure out which side of `mid` is sorted, then treat that side like an ordinary bounded binary search; if `target` doesn't fit in that sorted range, it must be on the other side.

## 2. Approach

* **Idea:** a single modified binary search (still `O(log n)`, one pass) that adds a "which half is sorted?" check before deciding which way to move.
* **Data structure / pointers:** `left`/`right` are the usual inclusive bounds; `mid` is tested first for an exact match, then used to compare `nums[left]` vs `nums[mid]` to detect the sorted half.
* **Invariant:** if `target` is in `nums`, its index is always within `[left, right]`; each iteration proves one half can't contain it (either because it's sorted and out of range, or because it contains the rotation point and isn't fully checkable, but the comparison still safely rules it out).
* **Edge cases:**
  - Unrotated array → `nums[left] <= nums[mid]` is always true, so it behaves exactly like plain binary search.
  - Single element → loop runs once, either matches or falls through to `-1`.
  - Two elements → still handled correctly since `nums[left] <= nums[mid]` degenerates cleanly to a 1-element "sorted half."
  - Empty array → `right = -1` from the start, loop never runs, returns `-1`.

## 3. Code

```python
class Solution:

    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Determine which half is sorted
            if nums[left] <= nums[mid]:
                # Left half is sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                # Right half is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

## 4. Dry Run

`nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`

| Iteration | `left` | `right` | `mid` | `nums[mid]` | Sorted half | In sorted bound? | Next state |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | Left (`4 <= 7`) | No (`0 ∉ [4, 7)`) | `left = 4` |
| 2 | 4 | 6 | 5 | 1 | Left (`0 <= 1`) | Yes (`0 ∈ [0, 1)`) | `right = 4` |
| 3 | 4 | 4 | 4 | 0 | — | match | return `4` |

## 5. Complexity

* **Time:** `O(log n)` — every iteration still eliminates half the remaining range, same as plain binary search; the sorted-half check is `O(1)` extra work per step.
* **Space:** `O(1)` — only `left`, `right`, `mid`.

## 6. Recall (30 seconds)

- Rotation breaks global order but never breaks the fact that one of the two halves around `mid` is still sorted.
- Decide which half is sorted first (`nums[left] <= nums[mid]`), then check if `target` fits in that sorted half's range — if it does, search there; if not, search the other half.
- It degrades to plain binary search whenever the array isn't actually rotated.
