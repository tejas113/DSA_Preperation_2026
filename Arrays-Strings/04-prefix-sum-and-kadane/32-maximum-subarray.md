# 53. Maximum Subarray

**LC 53** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Kadane's algorithm

---

## 1. Intuition

Carry a running sum as you scan the array. The moment that running sum goes negative, it can only drag down
any subarray built on top of it — so throw it away and start fresh from the next number, rather than
carrying dead weight forward.

* `current_sum` is the best sum of a subarray *ending exactly at the current position*.
* `if current_sum < 0: current_sum = 0` — a negative running sum would only shrink whatever gets added next, so it's reset before including `num`.
* `current_sum += num` — this always includes the current number, whether the sum was just reset or not.
* `max_sum = max(max_sum, current_sum)` — updated every step, since the best subarray might end anywhere, not just at the last position.

**Recall:** reset `current_sum` to `0` whenever it goes negative, then add `num`; track the running max of `current_sum` as you go.

---

## 2. Approach

* **Idea:** the best subarray ending at each position is either "just this number" (if everything before it was a net negative) or "everything before it, plus this number" — Kadane's algorithm computes both possibilities implicitly via the reset rule.
* **Data structure / pointers:** `current_sum` (best sum ending at the current index), `max_sum` (best sum seen anywhere so far).
* **Invariant:** at the end of each iteration, `current_sum` equals the maximum sum of any subarray that ends exactly at the current index, and `max_sum` is the best such value across all indices processed so far.
* **Edge cases:**
  * All negative numbers → the reset rule never helps (every prefix is already negative), so the answer is just the largest single element — verified against `[-3, -2, -1]` giving `-1`.
  * Single element → returns that element directly.
  * All positive numbers → `current_sum` never resets, and the answer is the sum of the whole array.
  * Starting `max_sum` at `float("-inf")` (not `0`) matters — it guarantees the answer is correct even when every number is negative, since `0` would incorrectly suggest an empty subarray is allowed.

---

## 3. Code

```python
class Solution:

    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = float("-inf")
        current_sum = 0

        for num in nums:
            if current_sum < 0:
                current_sum = 0
            current_sum += num

            max_sum = max(max_sum, current_sum)
        return max_sum


if __name__ == "__main__":
    solution = Solution()
    assert solution.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert solution.maxSubArray([1]) == 1
    assert solution.maxSubArray([-3, -2, -1]) == -1
    assert solution.maxSubArray([5, 4, -1, 7, 8]) == 23
    print("All tests passed")
```

### Alternative: divide and conquer — O(n log n)

Split the array in half; the best subarray either lies entirely in the left half, entirely in the right
half, or crosses the midpoint. Correct, and a good follow-up to know, but slower and more code than Kadane.

```python
class SolutionDivideConquer:

    def maxSubArray(self, nums: list[int]) -> int:

        def maxCrossingSum(nums, low, mid, high):
            # Include elements on left of mid
            left_sum = float("-inf")
            curr = 0
            for i in range(mid, low - 1, -1):
                curr += nums[i]
                left_sum = max(left_sum, curr)

            # Include elements on right of mid
            right_sum = float("-inf")
            curr = 0
            for i in range(mid + 1, high + 1):
                curr += nums[i]
                right_sum = max(right_sum, curr)

            return left_sum + right_sum

        def helper(nums, low, high):
            if low == high:
                return nums[low]

            mid = (low + high) // 2

            left_max = helper(nums, low, mid)
            right_max = helper(nums, mid + 1, high)
            cross_max = maxCrossingSum(nums, low, mid, high)

            return max(left_max, right_max, cross_max)

        return helper(nums, 0, len(nums) - 1)


if __name__ == "__main__":
    solution = SolutionDivideConquer()
    assert solution.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert solution.maxSubArray([-3, -2, -1]) == -1
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| Step | `num` | `current_sum` before reset | `current_sum` after add | `max_sum` |
| --- | --- | --- | --- | --- |
| `1` | `-2` | `0` | `-2` | `-2` |
| `2` | `1` | `-2` → reset `0` | `1` | `1` |
| `3` | `-3` | `1` | `-2` | `1` |
| `4` | `4` | `-2` → reset `0` | `4` | `4` |
| `5` | `-1` | `4` | `3` | `4` |
| `6` | `2` | `3` | `5` | `5` |
| `7` | `1` | `5` | `6` | **`6`** |
| `8` | `-5` | `6` | `1` | `6` |
| `9` | `4` | `1` | `5` | `6` |

**Return:** `6` — the subarray `[4, -1, 2, 1]`.

---

## 5. Complexity

* **Time:** `O(n)` — one pass, constant work per element.
* **Space:** `O(1)` — two scalar variables.

**Divide and conquer:** `O(n log n)` time (the recurrence `T(n) = 2T(n/2) + O(n)`), `O(log n)` space for the recursion stack.

---

## 6. Recall (30 seconds)

* **Reset rule:** `if current_sum < 0: current_sum = 0`, then add the current number.
* **Why it works:** a negative running sum can only make the next subarray worse, never better, so dropping it loses nothing.
* **Track the max continuously:** the best subarray can end at any position, so `max_sum` updates every step, not just at the end.
