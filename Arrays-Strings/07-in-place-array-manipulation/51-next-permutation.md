# 31. Next Permutation

**LC 31** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Find the pivot, swap with its successor, reverse the tail

---

## 1. Intuition

The next permutation is the smallest arrangement that's still strictly bigger than the current one. To make
the *smallest* possible increase, you want to change the array as little as possible, and change it as far
to the *right* as possible — a change near the end moves you up by less than a change near the start.

A strictly *decreasing* suffix (like `..., 7, 6, 5, 3, 1`) is already the largest possible arrangement of
those values — there's no way to rearrange a decreasing run into anything bigger. So the first place you
*can* increase anything, scanning from the right, is the last position where a number is smaller than the
one right after it: that number, `nums[i]`, can be swapped for something bigger from the decreasing suffix
to its right.

* `i = n - 2`; `while nums[i] >= nums[i + 1]: i -= 1` finds the pivot — the last index where increasing is still possible. Everything from `i+1` onward is a decreasing run (by construction of the scan).
* Once you have the pivot, you want the *smallest* increase to `nums[i]` — so among everything in the decreasing suffix that's bigger than `nums[i]`, pick the one closest to `nums[i]` in value. Scanning the suffix from the right (`while nums[j] <= nums[i]: j -= 1`) finds exactly that, because the suffix is decreasing: the first value from the right that beats `nums[i]` is the smallest one that does.
* Swapping `nums[i]` and `nums[j]` makes the prefix up to `i` strictly larger, using the smallest possible bump.
* The suffix after the swap is *still* decreasing (swapping in a value from a decreasing sequence into another decreasing sequence preserves that order at the ends touching the swap point — provably, since `nums[j]` was the smallest value in the suffix greater than the old `nums[i]`). Reversing a decreasing suffix turns it into an *increasing* one — the smallest possible arrangement of those exact values, which is exactly what's needed to make the overall result the *very next* permutation, not some larger one.
* If no pivot exists (`i` reaches `-1`), the whole array is decreasing — it's already the *largest* permutation, so the "next" one wraps around to the smallest: reversing the whole array (which the Step 3 code does unconditionally, using `i + 1 = 0`) produces exactly that.

**Recall:** find the pivot (last index where `nums[i] < nums[i+1]`), swap it with the smallest larger value to its right, then reverse everything after the pivot.

---

## 2. Approach

* **Idea:** change the array as little as possible and as far right as possible — find the last spot where any increase is possible, make the smallest valid increase there, then arrange everything after it into its smallest possible order.
* **Data structure / pointers:** `i` (the pivot), `j` (the pivot's swap partner), then `left`/`right` for the final reversal.
* **Invariant:** after the pivot scan, `nums[i+1:]` is a non-increasing (weakly decreasing) run; after the swap, that same range is still non-increasing, so reversing it correctly produces the smallest possible ordering of those values.
* **Edge cases:**
  * Entirely decreasing (`[3, 2, 1]`) → no pivot found (`i = -1`); the reversal step runs on the whole array (`left = 0`), producing the fully sorted ascending array — wrapping from the largest permutation to the smallest.
  * Duplicates (`[1, 1, 5]`) → `nums[i] >= nums[i+1]` (using `>=`, not `>`) correctly treats equal adjacent values as part of the decreasing run, and `nums[j] <= nums[i]` (using `<=`) correctly skips values equal to `nums[i]` when looking for the swap partner.
  * Single element → `i` starts at `-1` (since `n - 2 = -1`), so the pivot scan never runs, and reversing a zero/one-length range leaves it unchanged.
  * Two elements → either swaps them (if increasing) or reverses them (if decreasing) — both are just the two-element special case of the general algorithm.

---

## 3. Code

```python
class Solution:

    def nextPermutation(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        i = n - 2

        # Step 1: Find the first decreasing element from the right (Pivot)
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        # Step 2: If pivot exists, find the next larger element to swap
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]

        # Step 3: Reverse the suffix starting at index i + 1
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1


if __name__ == "__main__":
    solution = Solution()

    nums = [1, 5, 8, 4, 7, 6, 5, 3, 1]
    solution.nextPermutation(nums)
    assert nums == [1, 5, 8, 5, 1, 3, 4, 6, 7]

    fully_decreasing = [3, 2, 1]
    solution.nextPermutation(fully_decreasing)
    assert fully_decreasing == [1, 2, 3]

    with_duplicates = [1, 1, 5]
    solution.nextPermutation(with_duplicates)
    assert with_duplicates == [1, 5, 1]

    single = [1]
    solution.nextPermutation(single)
    assert single == [1]

    pair = [1, 2]
    solution.nextPermutation(pair)
    assert pair == [2, 1]

    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 5, 8, 4, 7, 6, 5, 3, 1]`

| Step | Index | Value | Result | `nums` after |
| --- | --- | --- | --- | --- |
| **Pivot scan** | `i = 3` | `nums[3] = 4` | `4 < nums[4] = 7` → pivot found, stop | `[1, 5, 8, 4, 7, 6, 5, 3, 1]` |
| **Successor scan** | `j = 6` | `nums[6] = 5` | `5 > 4` → swap `nums[3]` and `nums[6]` | `[1, 5, 8, 5, 7, 6, 4, 3, 1]` |
| **Suffix reverse** | `left=4, right=8` | suffix `[7, 6, 4, 3, 1]` | reverse → `[1, 3, 4, 6, 7]` | `[1, 5, 8, 5, 1, 3, 4, 6, 7]` |

**Return (in-place):** `[1, 5, 8, 5, 1, 3, 4, 6, 7]`

---

## 5. Complexity

* **Time:** `O(n)` — the pivot scan, successor scan, and reversal each touch at most `n` elements, and none overlap in a way that compounds.
* **Space:** `O(1)` — everything happens in place with a constant number of index variables.

---

## 6. Recall (30 seconds)

* **Three steps:** find the pivot (last `nums[i] < nums[i+1]`), swap it with the smallest larger value to its right, reverse everything after it.
* **Why the suffix reverse gives the smallest result:** the suffix is decreasing both before and after the swap, and reversing a decreasing run gives the smallest possible ordering of those exact values.
* **No pivot means wrap-around:** a fully decreasing array is already the largest permutation, so the algorithm naturally produces the fully sorted (smallest) one instead.
