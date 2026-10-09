# 10. Target Sum

**LC 494** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 0/1 Knapsack / Subset-Sum Counting (add / subtract)

---

## 1. Intuition

Put a `+` or `-` in front of every number so the total equals `target`, and count how many ways that can be done. Go through the numbers in order with a running sum that starts at `0`. At each number you make one binary choice, **add** it or **subtract** it. When every number has been used, that path counts only if the running sum equals `target`.

* `dp(i,current_sum)` — the number of ways to sign `nums[i:]` so that, starting from `current_sum`, the final total equals `target`.
* `if i == len(nums)` with the inner `if current_sum == target` — all numbers are used: this is one valid way only if the running sum is exactly `target`, otherwise it is `0`.
* `add = dp(i+1,current_sum + nums[i])` — give `nums[i]` a `+`.
* `substract = dp(i+1,current_sum - nums[i])` — give it a `-`.
* `add + substract` — every complete sign assignment is one path; count them all.
* `memo[(i,current_sum)]` — different sign choices can reach the same (index, running sum), so each is solved once. The sum can be negative, which is fine for a dict key.

**Recall:** `dp(i, s) = dp(i + 1, s + nums[i]) + dp(i + 1, s - nums[i])`, and at the end count `1` only if `s == target`.

## 2. Template

* **State:** `dp(i, current_sum)` = ways to sign `nums[i:]` so the final total is `target`, starting from `current_sum`
* **Choice:** `+nums[i]` or `-nums[i]`
* **Recurrence:** `dp(i, s) = dp(i + 1, s + nums[i]) + dp(i + 1, s - nums[i])`
* **Base:** `i == len(nums)` → `1` if `current_sum == target`, else `0`
* **Guard:** `current_sum` can go negative, so there is no bounds check, and the target is only checked at the very end (so zeros in `nums` are counted correctly)

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:

        memo = {}
        
        def dp(i,current_sum):
            if i == len(nums):
                if current_sum == target:
                    return 1
                else:
                    return 0

            if (i,current_sum) in memo:
                return memo[(i,current_sum)]

            add = dp(i+1,current_sum + nums[i])
            substract = dp(i+1,current_sum - nums[i])

            memo[(i,current_sum)] = add + substract
            return memo[(i,current_sum)]
    
        return dp(0,0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**. One extra step: the running sum can be negative, but an array index can't. The sum always stays between `-total` and `+total` (`total = sum(nums)`), so store sum `s` at index `s + offset` with `offset = total`. Each number only asks for the **next** number's row, so two rows are enough.

| Memoization | Tabulation |
|---|---|
| `memo[(i, current_sum)]` | two rows over sums `-total..total`: `nxt` (row `i + 1`) and `cur` (row `i`) |
| `if i == len(nums): ... return 1 if current_sum == target` | the starting row (`i = n`): all zeros except `nxt[target + offset] = 1` |
| `add = dp(i+1, current_sum + nums[i])` | `nxt[s + nums[i] + offset]`, if that sum is in range |
| `substract = dp(i+1, current_sum - nums[i])` | `nxt[s - nums[i] + offset]`, if that sum is in range |
| `add + substract` | `cur[s + offset]` = the two values added |
| `dp(i, ...)` asks for row `i + 1` | `for i in range(n - 1, -1, -1)` — from the last number backward |
| `dp(0, 0)` | `return nxt[offset]` (the entry for sum `0`) |

**Loop-order rule:** the memo asks for the next number, so start from the last number and walk backward, keeping only the previous row. If `abs(target) > total`, nothing is reachable, so return `0` first (this also keeps `target + offset` inside the array).

```python
class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total:
            return 0

        offset = total                              # sum s is stored at index s + offset  (s: -total..total)
        nxt = [0] * (2 * total + 1)                 # row i + 1; starts as row n
        nxt[target + offset] = 1                    # base: all numbers used and exactly on the target = 1 way

        for i in range(len(nums) - 1, -1, -1):
            cur = [0] * (2 * total + 1)             # row i
            for s in range(-total, total + 1):
                ways = 0
                if s + nums[i] <= total:
                    ways += nxt[s + nums[i] + offset]   # '+' sign
                if s - nums[i] >= -total:
                    ways += nxt[s - nums[i] + offset]   # '-' sign
                cur[s + offset] = ways
            nxt = cur

        return nxt[offset]                          # dp(0, 0)
```

### Alternative: remaining-target memo

Your earlier version tracks the amount **still needed** instead of the sum so far: `+` subtracts from it and `-` adds to it.

```python
from typing import List

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        memo = {}

        def dp(target_rem: int, i: int) -> int:
            # Base Case: Processed all numbers
            if i == len(nums):
                return 1 if target_rem == 0 else 0

            if (target_rem, i) in memo:
                return memo[(target_rem, i)]

            # Decision 1: Assign '+' sign (subtract from remaining target)
            add = dp(target_rem - nums[i], i + 1)

            # Decision 2: Assign '-' sign (add to remaining target)
            sub = dp(target_rem + nums[i], i + 1)

            memo[(target_rem, i)] = add + sub
            return memo[(target_rem, i)]

        return dp(target, 0)
```

### Alternative: subset-sum reduction

There is a cleaner route to an O(S) table. Let `P` be the numbers that get `+` and `N` the numbers that get `-`. Then `sum(P) - sum(N) = target` and `sum(P) + sum(N) = total`. Adding the two equations gives `sum(P) = (target + total) / 2`. So the question becomes: **how many subsets of `nums` sum to `(target + total) / 2`?** That is the same table as Partition Equal Subset Sum, with `+=` (counting) instead of `or` (existence). If `abs(target) > total`, or `(target + total)` is odd, the answer is `0`.

```python
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total_sum = sum(nums)

        # Early Exits:
        # 1. target is larger than total_sum
        # 2. (target + total_sum) is odd -> cannot divide into integer subsets
        if abs(target) > total_sum or (target + total_sum) % 2 != 0:
            return 0

        p_target = (target + total_sum) // 2

        # dp[j] stores the number of ways to reach sum j
        dp = [0] * (p_target + 1)
        dp[0] = 1  # Base Case: 1 way to form sum 0 (empty set)

        for num in nums:
            # Iterate backward for 0/1 knapsack constraint (each element used once)
            for j in range(p_target, num - 1, -1):
                dp[j] += dp[j - num]

        return dp[p_target]
```

## 4. Dry Run (`nums = [1, 1, 1]`, `target = 1`)

```text
dp(0,0) = 3                               nums = [1, 1, 1], target = 1
├─ +1 → dp(1,1) = 2
│   ├─ +1 → dp(2,2) = 1
│   │   ├─ +1 → dp(3,3) = 0             (base: total 3 ≠ 1)
│   │   └─ -1 → dp(3,1) = 1             (base: total 1 = target)
│   └─ -1 → dp(2,0) = 1
│       ├─ +1 → dp(3,1) = 1             (base: total 1 = target)
│       └─ -1 → dp(3,-1) = 0            (base: total -1 ≠ 1)
└─ -1 → dp(1,-1) = 1
    ├─ +1 → dp(2,0) = 1                 (cached — not recomputed)
    └─ -1 → dp(2,-2) = 0
        ├─ +1 → dp(3,-1) = 0            (base: total -1 ≠ 1)
        └─ -1 → dp(3,-3) = 0            (base: total -3 ≠ 1)
```

The three ways: `+1 +1 -1`, `+1 -1 +1`, `-1 +1 +1`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, current_sum)`. With `S = sum(nums)`, the sum lies in `[-S, S]`, so at most `n × (2S + 1)` entries.
* **Time:** O(n × S) — each state makes exactly two calls (`add`, `substract`) and does O(1) other work.
* **Space:** O(n × S) for the memo, plus recursion depth `n`. The two-row table is O(S), and the subset-sum table is O(P) with `P = (target + S) / 2`.

## 6. Recall (30 seconds)

* **State / transition:** `dp(i, s) = dp(i + 1, s + nums[i]) + dp(i + 1, s - nums[i])`; at `i == len(nums)` count `1` only if `s == target`.
* **Table:** the sum can be negative, so store it at `s + offset` (`offset = total`) and keep two rows.
* **Reduction:** signs ↔ subsets; count subsets summing to `(target + total) / 2` (`abs(target) > total` or odd → `0`).
