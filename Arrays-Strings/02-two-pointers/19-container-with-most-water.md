# 11. Container With Most Water

**LC 11** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Two pointers, greedy elimination

---

## 1. Intuition

The water held between two lines is `width × min(height)` — the shorter line always caps how much water
you can hold, no matter how tall the other one is. Start as wide as possible, then give up width only where
it can't possibly help: move the *shorter* line inward, because keeping it would waste every future width on
a bottleneck that's already known to be too short.

* `width = right - left` is the container's width; it only shrinks as the pointers close in.
* `min(height[left], height[right])` is the water's height — capped by the shorter wall.
* `max_water = max(max_water, current_water)` keeps the best area seen so far.
* `if height[left] < height[right]: left += 1 else: right -= 1` always drops the shorter wall. Moving the *taller* one instead could only lose width while the height stays capped by the same short wall — never an improvement.

**Recall:** `area = width × min(height)`; always move the pointer at the shorter line inward.

---

## 2. Approach

* **Idea:** start at maximum width and shrink from whichever side can't possibly be part of a better answer — the shorter side.
* **Data structure / pointers:** `left` starts at index `0`, `right` at the last index. `max_water` tracks the best area found.
* **Invariant:** every area that could beat `max_water` and hasn't been checked yet still lies between the current `left` and `right` — moving the shorter side only discards containers that are provably no better than the one just measured.
* **Edge cases:**
  * Fewer than 2 lines → the loop never runs (or the problem guarantees at least 2).
  * All heights equal → the widest pair (the two ends) gives the max, found on the first check.
  * Increasing or decreasing heights → still works; the shorter side is whichever wall is smaller at each step, regardless of overall trend.
  * Two adjacent lines as the answer → still reachable, since `left < right` keeps checking until they meet.

---

## 3. Code

```python
class Solution:

    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        max_water = 0

        while left < right:
            width = right - left
            current_water = width * min(height[left], height[right])
            max_water = max(max_water, current_water)

            # Move the pointer pointing to the shorter line
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water


if __name__ == "__main__":
    solution = Solution()
    assert solution.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert solution.maxArea([1, 1]) == 1
    assert solution.maxArea([4, 3, 2, 1, 4]) == 16
    print("All tests passed")
```

---

## 4. Dry Run

`height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`

| Step | `left` | `height[left]` | `right` | `height[right]` | `width` | `current_water` | `max_water` | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1** | `0` | `1` | `8` | `7` | `8` | `8 × 1 = 8` | `8` | `1 < 7` → `left = 1` |
| **2** | `1` | `8` | `8` | `7` | `7` | `7 × 7 = 49` | **`49`** | `8 ≥ 7` → `right = 7` |
| **3** | `1` | `8` | `7` | `3` | `6` | `6 × 3 = 18` | `49` | `8 ≥ 3` → `right = 6` |
| **4** | `1` | `8` | `6` | `8` | `5` | `5 × 8 = 40` | `49` | `8 ≥ 8` → `right = 5` |
| **5–8** | `1` | `8` | `5`→`2` | `4,5,2,6` | `4`→`1` | all ≤ `16` | `49` | `right` keeps shrinking toward `left` |

The loop ends when `left == right`. **Return:** `49`

---

## 5. Complexity

* **Time:** `O(n)` — `left` and `right` only move toward each other, so together they take at most `n` steps.
* **Space:** `O(1)` — only the two pointers and a running best.

---

## 6. Recall (30 seconds)

* **Area formula:** `width × min(height[left], height[right])`.
* **Greedy move:** always shrink from the shorter side — the taller side is never the bottleneck, so keeping it never helps.
* **Why it's safe:** any container you'd skip by moving the shorter side is guaranteed to be no wider *and* no taller than one you've already measured or will measure.
