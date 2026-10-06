# 658. Find K Closest Elements

**LC 658** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Binary search the start of a window, not a value

---

## 1. Intuition

The answer is always some contiguous window of `k` elements in the sorted array — so instead of finding `x` and expanding outward, binary search directly for *where that window should start*. A window starting at index `mid` is `arr[mid .. mid + k - 1]`; the element just outside it on the right is `arr[mid + k]`.

- Compare the window's leftmost element `arr[mid]` against the element right after the window, `arr[mid + k]` — whichever is farther from `x` tells you which element doesn't belong.
- `x - arr[mid] > arr[mid + k] - x` → `arr[mid]` is strictly farther from `x` than `arr[mid + k]` is, so the window should slide right past `mid`: `left = mid + 1`.
- Otherwise → `arr[mid]` is closer (or tied, and ties favor the smaller/leftmost value by the problem's rule), so the window should start at `mid` or earlier: `right = mid`.
- Same boundary-search shape as [#1 Binary Search](01-binary-search.md)'s sibling pattern — `while left < right`, `right = mid` to keep a candidate, `left = mid + 1` to discard one — just searching for a *window start*, not a value or an index match.

**Recall:** binary search the window's starting index in `[0, n - k]` by comparing the distance of the element leaving the window (left) against the distance of the element that would enter it (right).

## 2. Approach

* **Idea:** boundary search (Form 2) over the possible window-start positions `[0, len(arr) - k]`, using a distance comparison between the window's edge and its right neighbor as the "condition."
* **Data structure / pointers:** `left`/`right` bound the window's start index; `mid` is a candidate start; `arr[mid]` and `arr[mid + k]` are the two values actually compared (never `x` directly against the full window).
* **Invariant:** the optimal window start is always within `[left, right]`; each step proves `arr[mid]` either belongs in the optimal window (keep `mid`, `right = mid`) or doesn't (discard it, `left = mid + 1`).
* **Edge cases:**
  - `x` smaller than every element → `x - arr[mid]` is always negative, `arr[mid+k] - x` positive, so the comparison is always false and `right` shrinks to `0` — returns the first `k` elements.
  - `x` larger than every element → the comparison is always true, `left` grows to `len(arr) - k` — returns the last `k` elements.
  - `k == len(arr)` → `right = len(arr) - k = 0` from the start, loop never runs, returns the whole array.
  - Duplicate values → handled the same as any other comparison; ties resolve toward the smaller/left element because `<=` (not `<`) keeps `right = mid` on a tie.

## 3. Code

```python
from typing import List


class Solution:

    def findClosestElements(
        self, arr: List[int], k: int, x: int
    ) -> List[int]:
        left = 0
        right = len(arr) - k

        while left < right:
            mid = (left + right) // 2

            # Compare distance of left element arr[mid] vs right neighbor arr[mid + k]
            if x - arr[mid] > arr[mid + k] - x:
                left = mid + 1
            else:
                right = mid

        return arr[left : left + k]
```

## 4. Dry Run

`arr = [1, 2, 3, 4, 5]`, `k = 4`, `x = 3` (`left=0, right=5-4=1`)

| Iteration | `left` | `right` | `mid` | `arr[mid]` | `arr[mid+k]` | `x-arr[mid]` | `arr[mid+k]-x` | Decision | Action |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 1 | 5 | 2 | 2 | `2 ≤ 2` → not farther | `right = 0` |
| End | 0 | 0 | — | — | — | — | — | `left == right` | return `arr[0:4] = [1,2,3,4]` |

## 5. Complexity

* **Time:** `O(log(n - k) + k)` — binary search over `n - k` possible start positions, plus `O(k)` to slice out the final window.
* **Space:** `O(1)` auxiliary, not counting the output slice.

## 6. Recall (30 seconds)

- The answer is always a contiguous window — binary search *where it starts*, not the elements themselves.
- Compare the window's current left edge `arr[mid]` against the element one past the window's right edge `arr[mid + k]` — farther one gets excluded.
- `x - arr[mid] > arr[mid + k] - x` → slide right (`left = mid + 1`); otherwise keep `mid` as a candidate (`right = mid`).
