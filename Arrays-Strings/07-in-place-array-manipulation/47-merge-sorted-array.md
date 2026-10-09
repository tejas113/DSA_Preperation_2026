# 88. Merge Sorted Array

**LC 88** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Fill from the back

---

## 1. Intuition

Merging from the front would mean constantly shifting `nums1`'s real elements rightward to make room —
expensive, and easy to get wrong. But `nums1` already has empty space at the *back* (the trailing zeros), so
merge from the back instead: compare the largest remaining candidates from each array, and drop the bigger
one into the last open slot. Working backward means you only ever write into space that's already been
"used up" by a value you've already read — no shifting, no overwriting anything you still need.

* `p1 = m - 1`, `p2 = n - 1` start at the last *real* elements of each array (not `len(nums1) - 1`, since the tail of `nums1` is just placeholder zeros).
* `p = m + n - 1` is the last index of the combined array — the write position.
* `if nums1[p1] > nums2[p2]` picks the larger candidate and places it at `nums1[p]`, then only that side's pointer moves back.
* Once `p2 < 0`, the loop stops — any remaining `nums1[p1..]` values are already exactly where they need to be, since they were never touched.
* The final `while p2 >= 0` only matters if `nums2` still has smaller leftover elements once `nums1` runs out — those get copied into the front of `nums1`.

**Recall:** three pointers from the back (`p1`, `p2`, `p`); place the larger of `nums1[p1]`/`nums2[p2]` at `nums1[p]`; if `nums2` outlives `nums1`, copy its leftovers.

---

## 2. Approach

* **Idea:** since `nums1` has exactly enough trailing space to fit `nums2`, filling from the back guarantees every write lands in a slot whose original value has already been read (or was never meaningful in the first place).
* **Data structure / pointers:** `p1` (last unmerged real element of `nums1`), `p2` (last unmerged element of `nums2`), `p` (next write position, from the back).
* **Invariant:** at every step, `nums1[p+1:]` already holds the correct, fully sorted tail of the final merged array — everything from the largest values down to whatever's been placed so far.
* **Edge cases:**
  * `m = 0` → the first loop never finds a `nums1[p1]` to compare (`p1` starts at `-1`), so the second loop alone copies all of `nums2` into `nums1`.
  * `n = 0` → both loops are skipped entirely (`p2` starts at `-1`), and `nums1` is already correct as-is.
  * Every element of `nums2` smaller than every element of `nums1` → `p1` never runs out first in the main loop until the end; the final state still ends up correct because the main loop keeps picking whichever is larger.
  * If `nums1` runs out first (`p1 < 0`) while `nums2` still has elements, the loop `while p1 >= 0 and p2 >= 0` stops, and the remaining `nums2` values are copied by the trailing `while p2 >= 0` loop — this is why only `p2`'s leftover case needs a separate copy step, not `p1`'s.

---

## 3. Code

```python
class Solution:

    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """Do not return anything, modify nums1 in-place instead."""
        p1 = m - 1
        p2 = n - 1
        p = m + n - 1

        # Compare from the back and place larger elements at the end
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1

        # Copy any remaining elements from nums2
        # (If p1 >= 0, those elements are already in place in nums1)
        while p2 >= 0:
            nums1[p] = nums2[p2]
            p2 -= 1
            p -= 1


if __name__ == "__main__":
    solution = Solution()

    nums1 = [1, 2, 3, 0, 0, 0]
    solution.merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]

    empty_nums1 = [0]
    solution.merge(empty_nums1, 0, [1], 1)
    assert empty_nums1 == [1]

    empty_nums2 = [1]
    solution.merge(empty_nums2, 1, [], 0)
    assert empty_nums2 == [1]

    print("All tests passed")
```

---

## 4. Dry Run

`nums1 = [1, 2, 3, 0, 0, 0]`, `m = 3`; `nums2 = [2, 5, 6]`, `n = 3`

| Step | `p1` (val) | `p2` (val) | `p` before | Action | `nums1` after |
| --- | --- | --- | --- | --- | --- |
| **init** | `2` (`3`) | `2` (`6`) | `5` | — | `[1, 2, 3, 0, 0, 0]` |
| **1** | `2` (`3`) | `2` (`6`) | `5` | `6 > 3` → `nums1[5] = 6` | `[1, 2, 3, 0, 0, 6]` |
| **2** | `2` (`3`) | `1` (`5`) | `4` | `5 > 3` → `nums1[4] = 5` | `[1, 2, 3, 0, 5, 6]` |
| **3** | `2` (`3`) | `0` (`2`) | `3` | `3 > 2` → `nums1[3] = 3` | `[1, 2, 3, 3, 5, 6]` |
| **4** | `1` (`2`) | `0` (`2`) | `2` | `2 !> 2` → `nums1[2] = 2` (from `nums2`) | `[1, 2, 2, 3, 5, 6]` |

`p2 = -1` now, so the main loop ends; the trailing `while p2 >= 0` copy loop has nothing to do.

**Final:** `[1, 2, 2, 3, 5, 6]`

---

## 5. Complexity

* **Time:** `O(m + n)` — each pointer only moves backward, so together they take at most `m + n` total steps.
* **Space:** `O(1)` — everything happens in place on `nums1`.

---

## 6. Recall (30 seconds)

* **Fill from the back:** avoids shifting elements, since `nums1`'s trailing space is exactly where the largest values end up anyway.
* **Pick the bigger candidate:** `nums1[p1] > nums2[p2]` decides which pointer moves.
* **Only `nums2`'s leftovers need copying:** if `nums1` still has elements when `nums2` runs out, they're already correctly placed — only a leftover `nums2` needs an explicit final copy.
