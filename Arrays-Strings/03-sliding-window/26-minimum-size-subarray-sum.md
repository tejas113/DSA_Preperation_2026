# 209. Minimum Size Subarray Sum

**LC 209** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Variable sliding window, shrinking on positive numbers

---

## 1. Intuition

Grow the window until its sum is big enough, then shrink it from the left for as long as it's *still* big
enough — every shrink attempt that succeeds is a candidate for the shortest window. Because every number is
positive, adding a number to the window only ever grows the sum, and removing one only ever shrinks it — so
there's never a reason to backtrack.

* `current_sum += nums[r]` grows the window by including the newest number.
* `while current_sum >= target` shrinks the window one step at a time for as long as it's still valid — a `while`, not an `if`, because the window might stay valid through several shrinks in a row.
* `min_len = min(min_len, r - l + 1)` records the window's length *before* removing `nums[l]` — that's the last point this exact window was known to be valid.
* `current_sum -= nums[l]; l += 1` removes the leftmost number and tries an even smaller window on the next loop check.
* `float("inf")` as the starting `min_len` lets `min(...)` work cleanly; converting back to `0` at the end handles "no valid window exists."

**Recall:** grow `r`, and while `current_sum >= target`, record the window length and shrink `l` — this only works because every number is positive.

---

## 2. Approach

* **Idea:** because all numbers are positive, both the sum and the window's validity move monotonically as pointers move — there's no case where shrinking further and then growing again could ever help, so a straightforward two-pointer sweep finds the true minimum.
* **Data structure / pointers:** `l`, `r` are the window bounds; `current_sum` is the sum of `nums[l:r+1]`; `min_len` tracks the best answer.
* **Invariant:** at the start of each outer loop iteration, `current_sum` equals the sum of `nums[l:r+1]` exactly, and every window shorter than the current one that was ever valid has already been recorded in `min_len`.
* **Edge cases:**
  * No subarray reaches `target` → `min_len` stays `float("inf")`, converted to `0` at the end.
  * The whole array is needed → still found, since the window only starts shrinking once the sum is already `>= target`.
  * A single element `>= target` → caught immediately when `r` reaches it, giving `min_len = 1`.
  * Empty array → the loop never runs, returns `0`.

---

## 3. Code

```python
class Solution:

    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        l = 0
        current_sum = 0
        min_len = float("inf")

        for r in range(len(nums)):
            current_sum += nums[r]

            while current_sum >= target:
                min_len = min(min_len, r - l + 1)
                current_sum -= nums[l]
                l += 1
        return min_len if min_len != float("inf") else 0


if __name__ == "__main__":
    solution = Solution()
    assert solution.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2
    assert solution.minSubArrayLen(4, [1, 4, 4]) == 1
    assert solution.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    print("All tests passed")
```

### Alternative: prefix sums + binary search — O(n log n)

This only works because every number is positive, which is exactly what makes the prefix sum array
**strictly increasing**. That's what makes binary search on it valid — with negative numbers present, the
prefix sums would no longer be monotonic and `bisect_left` could return the wrong index.

```python
import bisect


class SolutionBinarySearch:

    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        min_len = float("inf")

        for i in range(n):
            needed = target + prefix[i]
            # Binary search for index j where prefix[j] >= needed
            j = bisect.bisect_left(prefix, needed)
            if j <= n:
                min_len = min(min_len, j - i)

        return min_len if min_len != float("inf") else 0


if __name__ == "__main__":
    solution = SolutionBinarySearch()
    assert solution.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2
    assert solution.minSubArrayLen(4, [1, 4, 4]) == 1
    print("All tests passed")
```

---

## 4. Dry Run

`target = 7`, `nums = [2, 3, 1, 2, 4, 3]`

| Step | `r` | `nums[r]` | `current_sum` before shrink | shrink steps (`l`, `current_sum` after) | `min_len` |
| --- | --- | --- | --- | --- | --- |
| 1–3 | `0,1,2` | `2,3,1` | `2 → 5 → 6` | none (`< 7` each time) | `inf` |
| 4 | `3` | `2` | `8` | `l=0→1`, sum `8→6` | `4` |
| 5 | `4` | `4` | `10` | `l=1→2`, sum `10→7`; `l=2→3`, sum `7→6` | `3` |
| 6 | `5` | `3` | `9` | `l=3→4`, sum `9→7`; `l=4→5`, sum `7→3` | **`2`** |

**Return:** `2` (the window `[4, 5]` = `[4, 3]`, sum `7`)

---

## 5. Complexity

* **Time:** `O(n)` — `r` moves `n` times, and `l` only ever moves forward, so its total movement across the whole run is at most `n`.
* **Space:** `O(1)` — only scalar trackers.

**Binary search alternative:** `O(n log n)` — building `prefix` is `O(n)`, and each of the `n` starting points does one `O(log n)` binary search.

---

## 6. Recall (30 seconds)

* **Grow, then shrink while still valid:** `while current_sum >= target`, record the length, then shrink.
* **Why it's O(n), not O(n²):** every number is positive, so `l` never needs to move backward — its total movement is bounded by `n`.
* **Binary search needs positive numbers too:** it works *because* positive numbers make the prefix sum array strictly increasing — with negatives, the prefix sums aren't monotonic and binary search on them breaks.
