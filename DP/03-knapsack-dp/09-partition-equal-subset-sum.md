# 09. Partition Equal Subset Sum

**LC 416** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 0/1 Knapsack / Subset Sum (pick / not-pick)

---

## 1. Intuition

Splitting `nums` into two subsets with equal sums means each subset sums to `total / 2`. If the total is odd, that's impossible. Otherwise ask one question: **can some subset of `nums` add up to exactly `k = total // 2`?** Go through the numbers in order with a running sum that starts at `0`. Each number is either **picked** (added to the subset) or **not picked**, and each is used at most once.

* `if total_sum % 2 != 0: return False` — an odd total can never split into two equal integer halves.
* `k = sum(nums) // 2` — the target each half must reach.
* `dp(i,current_sum)` — starting from the running sum `current_sum`, can the numbers from index `i` onward be picked to reach exactly `k`?
* `if current_sum == k: return True` — the target is hit exactly, so a valid subset exists. This check comes first.
* `if current_sum > k or i >= len(nums): return False` — overshot, or ran out of numbers.
* `pick = dp(i+1,current_sum + nums[i])` — add `nums[i]` and move to the next number (`i + 1`, so it can't be reused).
* `not_pick = dp(i+1,current_sum)` — leave it out; the sum stays the same.
* `pick or not_pick` — either choice working is enough.
* `memo[(i,current_sum)]` — different pick / not-pick histories reach the same (index, running sum) pair.

**Recall:** `dp(i, s) = dp(i + 1, s + nums[i]) or dp(i + 1, s)`.

## 2. Template

* **State:** `dp(i, current_sum)` = can numbers `i..end` bring the running sum from `current_sum` to exactly `k`
* **Choice:** pick `nums[i]` or not-pick it (each at most once, so both moves go to `i + 1`)
* **Recurrence:** `dp(i, s) = dp(i + 1, s + nums[i]) or dp(i + 1, s)`
* **Base:** `s == k` → `True`; `s > k` or `i >= len(nums)` → `False`
* **Guard:** an odd `total_sum` returns `False` before any recursion

## 3. Code

**Top-down with memoization, pick / not-pick** (primary solution).

```python
class Solution:
    def canPartition(self, nums: list[int]) -> bool:

        total_sum = sum(nums)

        if total_sum % 2 != 0:
            return False
            
        memo = {}
        k = sum(nums) // 2

        def dp(i,current_sum):
            if current_sum == k:
                return True

            if current_sum > k or i >= len(nums):
                return False

            if (i,current_sum) in memo:
                return memo[(i,current_sum)]

            pick = dp(i+1,current_sum + nums[i])
            not_pick = dp(i+1,current_sum)

            memo[(i,current_sum)] = pick or not_pick
            return memo[(i,current_sum)]

        return dp(0,0)
```

### Alternative: Tabulation

The memo has two state variables, `(i, current_sum)`, so the natural table is 2D: one row per number. But both `pick` and `not_pick` read the **next** row (`i + 1`), so a single array is enough, as long as no value is overwritten before it is read. Four moves turn the memo into it: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo[(i, current_sum)]` | `dp[s]` — one array over running sums `0..k`; the loop over numbers plays the role of `i` |
| `if current_sum == k: return True` | `dp[k] = True` |
| `current_sum > k or i >= len(nums): return False` | everything else starts as `False`, and the inner loop stops at `k - num` so the sum never overshoots |
| `not_pick = dp(i+1, current_sum)` | the value already sitting in `dp[s]` from the earlier numbers |
| `pick = dp(i+1, current_sum + nums[i])` | `dp[s + num]` — it must still be the **old** value (not updated for this number yet) |
| `pick or not_pick` | `dp[s] = dp[s] or dp[s + num]` |
| the `i` dimension | outer loop `for num in nums` |
| `pick` reads a larger sum from the **next** row | inner loop **ascending**, from `0` up to `k - num` |
| `dp(0, 0)` | `return dp[0]` |

**Loop-order rule:** the inner loop runs **ascending**. Going upward means `dp[s + num]` hasn't been touched yet in this pass, so each number is used at most once. (Coin Change is the opposite: a coin *may* repeat, so it reads a value that has already been updated in the same pass, and its loop runs the other way.)

```python
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total_sum = sum(nums)
        if total_sum % 2 != 0:
            return False

        k = total_sum // 2
        dp = [False] * (k + 1)
        dp[k] = True                                     # base: the target is reached exactly

        for num in nums:
            for s in range(0, k - num + 1):              # ascending: dp[s + num] is still the old value
                dp[s] = dp[s] or dp[s + num]

        return dp[0]
```

### Alternative: remaining-target memo

Your earlier version counts **down** instead: `i` is the amount still needed, so `i == 0` means the subset is complete. The `take` / `skip` logic is the same.

```python
from typing import List

class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total_sum = sum(nums)

        # Early exit: Odd sum cannot be split into two equal integer subsets
        if total_sum % 2 != 0:
            return False

        target = total_sum // 2
        memo = {}

        def dp(i: int, idx: int) -> bool:
            # Base Case 1: Exact target formed
            if i == 0:
                return True

            # Base Case 2: Negative target or ran out of elements
            if i < 0 or idx >= len(nums):
                return False

            if (i, idx) in memo:
                return memo[(i, idx)]

            # TAKE: Subtract current element, move to next index (idx + 1)
            take = dp(i - nums[idx], idx + 1)

            # SKIP: Don't subtract, move to next index (idx + 1)
            skip = dp(i, idx + 1)

            memo[(i, idx)] = take or skip
            return memo[(i, idx)]

        return dp(target, 0)
```

Its table indexes the sum **still needed**, so `take` reads a *smaller* sum and the loop runs **descending**. Again `dp[j - num]` must not have been updated yet for this number:

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total_sum = sum(nums)
        if total_sum % 2 != 0:
            return False

        target = total_sum // 2
        dp = [False] * (target + 1)
        dp[0] = True  # Base Case

        for num in nums:
            # Traverse backward to prevent reusing the same element multiple times
            for j in range(target, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]

        return dp[target]
```

## 4. Dry Run (`nums = [1, 2, 3]`, `k = 3`)

```text
dp(0,0) = True                             nums = [1, 2, 3], k = 3
├─ pick 1 → dp(1,1) = True
│   ├─ pick 2 → dp(2,3) = True          (base: reached k)
│   └─ not pick → dp(2,1) = False
│       ├─ pick 3 → dp(3,4) = False     (base: overshot)
│       └─ not pick → dp(3,1) = False   (base: out of numbers)
└─ not pick → dp(1,0) = True
    ├─ pick 2 → dp(2,2) = False
    │   ├─ pick 3 → dp(3,5) = False     (base: overshot)
    │   └─ not pick → dp(3,2) = False   (base: out of numbers)
    └─ not pick → dp(2,0) = True
        ├─ pick 3 → dp(3,3) = True      (base: reached k)
        └─ not pick → dp(3,0) = False   (base: out of numbers)
```

Two valid subsets: `{1, 2}` and `{3}`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, current_sum)`, where `current_sum` runs from `0` to `k`, so at most `n × (k + 1)` entries.
* **Time:** O(n × k) — each state makes one pick call and one not-pick call, and everything else is O(1).
* **Space:** O(n × k) for the memo, plus recursion depth `n`. The single-array table is O(k).

## 6. Recall (30 seconds)

* **Reduce:** odd total → `False`; otherwise find a subset summing to `k = total // 2`.
* **State / transition:** `dp(i, s) = dp(i + 1, s + nums[i]) or dp(i + 1, s)`; `s == k` → `True`, overshoot or out of numbers → `False`.
* **Table:** numbers outer, sums **ascending** (each number used once): `dp[s] = dp[s] or dp[s + num]`.
