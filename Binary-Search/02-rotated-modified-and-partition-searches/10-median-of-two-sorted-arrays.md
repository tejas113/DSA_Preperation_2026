# 4. Median of Two Sorted Arrays

**LC 4** · **Source:** LC150 + NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Binary search a *cut*, not a value — split both arrays so every left-side element is `<=` every right-side element

---

## 1. Intuition

Merging both arrays to find the median costs `O(m+n)`. Instead, binary search for a **partition** — a cut `i` in the smaller array (`nums1`) and a matching cut `j` in the other (`nums2`) — such that everything left of both cuts is `<=` everything right of both cuts, and the left side holds exactly half the total elements. Once that partition is found, the median is read directly off the 4 boundary values; no merging needed.

- `i` is the number of elements of `nums1` placed on the left; `j = total_left - i` is forced so the left side always has exactly `total_left` elements combined.
- `max_left1`/`min_right1` and `max_left2`/`min_right2` are the values immediately around each cut — using `±inf` when a cut is at an array's edge, so there's never a missing neighbor to compare.
- A cut is valid exactly when `max_left1 <= min_right2` **and** `max_left2 <= min_right1` — each array's left part doesn't spill past the other array's right part.
- If `max_left1 > min_right2`, `i` grabbed too much from `nums1` — shrink it (`high = i - 1`). Otherwise if `max_left2 > min_right1`, `i` grabbed too little — grow it (`low = i + 1`).
- Binary searching only `nums1` (the smaller array) is what gives `O(log(min(m, n)))` instead of `O(log(m+n))`.

**Recall:** binary search the split point `i` in the smaller array; `j` is derived, not searched; a split is valid when both arrays' left-halves stay `<=` both arrays' right-halves.

## 2. Approach

* **Idea:** boundary-style binary search (`while low <= high`), but the thing being searched for is a valid partition index `i`, not a value or a yes/no feasibility check.
* **Data structure / pointers:** `low`/`high` bound `i` within `[0, m]`; `j` is computed from `i` every iteration, never searched independently; `max_left1/2` and `min_right1/2` are the four values surrounding the two cuts.
* **Invariant:** the combined left side (`nums1[:i] + nums2[:j]`) always has exactly `total_left = (m+n+1)//2` elements; the search narrows `i` until that left side's max is `<=` the right side's min in both arrays simultaneously.
* **Edge cases:**
  - One array empty → always run the search on the smaller one, so `m` can be `0`; then `i` is forced to `0` and the whole partition falls onto `nums2`, correctly reducing to a single-array median.
  - Cuts at an array's edge (`i == 0`, `i == m`, `j == 0`, `j == n`) → `±inf` sentinels mean there's no real neighbor to violate the `<=` check.
  - Duplicate values across or within the arrays → handled the same as any other value, since the comparisons are just `<=`.

## 3. Code

```python
class Solution:

    def findMedianSortedArrays(
        self, nums1: list[int], nums2: list[int]
    ) -> float:
        # Always run binary search on the smaller array
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        low, high = 0, m
        total_left = (m + n + 1) // 2

        while low <= high:
            i = (low + high) // 2
            j = total_left - i

            # Elements surrounding the partition boundaries
            max_left1 = float("-inf") if i == 0 else nums1[i - 1]
            min_right1 = float("inf") if i == m else nums1[i]

            max_left2 = float("-inf") if j == 0 else nums2[j - 1]
            min_right2 = float("inf") if j == n else nums2[j]

            # Valid partition found
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                if (m + n) % 2 == 1:
                    return float(max(max_left1, max_left2))
                return (
                    max(max_left1, max_left2) + min(min_right1, min_right2)
                ) / 2.0

            elif max_left1 > min_right2:
                high = i - 1  # Shift left in nums1
            else:
                low = i + 1  # Shift right in nums1

        return 0.0
```

## 4. Dry Run

`nums1 = [1, 2]`, `nums2 = [3, 4]` (`m=2, n=2, total_left=2`)

| Iteration | `low` | `high` | `i` | `j` | `max_left1` | `min_right1` | `max_left2` | `min_right2` | Check | Action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 2 | 1 | 1 | 1 | 2 | 3 | 4 | `max_left2(3) > min_right1(2)` | `low = 2` |
| 2 | 2 | 2 | 2 | 0 | 2 | ∞ | -∞ | 3 | `2<=3` and `-∞<=∞` → valid | even total → `(max(2,-∞) + min(∞,3)) / 2 = (2+3)/2 = 2.5` |

## 5. Complexity

* **Time:** `O(log(min(m, n)))` — binary search runs only over `i ∈ [0, m]` where `m` is the smaller array's length; `j` is computed in `O(1)`, not searched.
* **Space:** `O(1)` — only scalar indices and the four boundary values.

## 6. Recall (30 seconds)

- Don't merge — binary search a partition index `i` in the smaller array; `j` is derived from `i` to keep the left side's size fixed.
- A partition is valid when `max_left1 <= min_right2` and `max_left2 <= min_right1`; use `±inf` for missing edge neighbors.
- Always search the smaller array — that's the whole reason this beats `O(log(m+n))`.
