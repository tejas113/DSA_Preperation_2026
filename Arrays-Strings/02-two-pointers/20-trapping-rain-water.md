# 42. Trapping Rain Water

**LC 42** · **Source:** LC150 + NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Two pointers, bottleneck by the shorter side

---

## 1. Intuition

The water sitting above any single bar is trapped by whichever wall — left or right — is *shorter*, because
water can't rise past the lower of its two boundaries. If you know the tallest wall to the left and the
tallest wall to the right of a bar, the water there is `min(those two) - height[bar]`. The two-pointer trick
avoids ever building those two full arrays: whichever side currently has the *smaller* running max is the
one whose water level is already fully decided, so you can process it and move on.

* `left_max` and `right_max` are the tallest bar seen so far from each side — updated as the pointers move inward.
* `if left_max < right_max` — the left side's running max is smaller, so the water above `height[left]` is capped by `left_max`, no matter how tall anything further right turns out to be.
* `water += left_max - height[left]` (after updating `left_max`) is exactly `min(left_max, right_max) - height[left]`, because `left_max < right_max` guarantees `left_max` is the true minimum.
* The `else` branch mirrors this from the right side.

**Recall:** water at a bar is `min(left_max, right_max) - height[bar]`; move whichever pointer has the smaller max, since that side's water level is already known.

---

## 2. Approach

* **Idea:** at any moment, if `left_max < right_max`, then no matter what heights appear later on the right, the water above `height[left]` is bounded by `left_max` — so it's safe to finalize that bar right now and move `left` inward. Symmetric on the other side.
* **Data structure / pointers:** `left`, `right` close in from both ends; `left_max`, `right_max` track the tallest wall seen so far on each side; `water` accumulates the total.
* **Invariant:** at every step, `left_max` is the true maximum of `height[0..left]` and `right_max` is the true maximum of `height[right..n-1]`; whichever of the two is smaller is guaranteed correct for the bar about to be processed, even though the full max on the *other* side isn't known yet.
* **Edge cases:**
  * Empty array → `0` (guarded by `if not height: return 0`).
  * Fewer than 3 bars → `0`, since there's nothing to trap between two edges or a single bar.
  * Strictly increasing or strictly decreasing heights → `0`, correctly, since one side never has a taller wall to trap against.
  * A single tall peak in the middle → both approaches still find it correctly, since the peak becomes the new `left_max` or `right_max` as the pointers pass it.

---

## 3. Code

```python
class Solution:

    def trap(self, height: list[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        water = 0

        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                water += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                water += right_max - height[right]

        return water


if __name__ == "__main__":
    solution = Solution()
    assert solution.trap([4, 2, 0, 3, 2, 5]) == 9
    assert solution.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert solution.trap([]) == 0
    assert solution.trap([5]) == 0
    print("All tests passed")
```

### Alternative: Prefix & suffix max arrays (O(n) space)

Precompute `left_max[i]` and `right_max[i]` for every index directly, instead of tracking them as running
values. Easier to derive from the water formula, but uses `O(n)` extra space instead of `O(1)`.

```python
class Solution:

    def trap(self, height: list[int]) -> int:
        if not height:
            return 0

        n = len(height)
        left_max = [0] * n
        right_max = [0] * n

        # Build prefix max array (highest wall to the left of each index)
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        # Build suffix max array (highest wall to the right of each index)
        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        # Calculate trapped water at each bar
        water = 0
        for i in range(n):
            water += min(left_max[i], right_max[i]) - height[i]

        return water


if __name__ == "__main__":
    solution = Solution()
    assert solution.trap([4, 2, 0, 3, 2, 5]) == 9
    assert solution.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    print("All tests passed")
```

---

## 4. Dry Run

`height = [4, 2, 0, 3, 2, 5]` (using the prefix/suffix version, since it's easiest to see all at once)

`left_max = [4, 4, 4, 4, 4, 5]`, `right_max = [5, 5, 5, 5, 5, 5]`

| Index `i` | `height[i]` | `left_max[i]` | `right_max[i]` | `min(...)` | Water at `i` |
| --- | --- | --- | --- | --- | --- |
| `0` | `4` | `4` | `5` | `4` | `4 - 4 = 0` |
| `1` | `2` | `4` | `5` | `4` | `4 - 2 = 2` |
| `2` | `0` | `4` | `5` | `4` | `4 - 0 = 4` |
| `3` | `3` | `4` | `5` | `4` | `4 - 3 = 1` |
| `4` | `2` | `4` | `5` | `4` | `4 - 2 = 2` |
| `5` | `5` | `5` | `5` | `5` | `5 - 5 = 0` |

**Total water:** `0 + 2 + 4 + 1 + 2 + 0 = 9`

The two-pointer version reaches the same total (`9`) without ever building `left_max[]`/`right_max[]` as full arrays — it only ever needs the running maxes.

---

## 5. Complexity

* **Time:** `O(n)` — the two-pointer version makes one pass, `left` and `right` together moving at most `n` steps; the prefix/suffix version makes three linear passes, still `O(n)`.
* **Space:** `O(1)` for the two-pointer version — only scalar trackers. `O(n)` for the prefix/suffix version — two full arrays.

---

## 6. Recall (30 seconds)

* **Formula:** water at a bar is `min(left_max, right_max) - height[bar]`.
* **Two-pointer rule:** move whichever side has the *smaller* running max — that side's water level is already fully decided, regardless of what's unseen on the other side.
* **Space trade-off:** prefix/suffix arrays make the formula explicit but cost `O(n)` space; two pointers get the same answer in `O(1)`.
