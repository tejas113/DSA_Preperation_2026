# 04. House Robber II

**LC 213** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / Circular Array

---

## 1. Intuition

The houses now form a **circle**, so house `0` and the last house are neighbours and can never both be robbed. Break the circle in two ways: either the last house is off the table (rob houses `0..n - 2`), or the first house is (rob houses `1..n - 1`). Each of those is just an ordinary straight line of houses, exactly House Robber. Solve both and take the better.

* `if n == 1` — a single house has no neighbour to clash with, and slicing `nums[:-1]` would give an empty list.
* `nums1 = nums[:-1]` and `nums2 = nums[1:]` — the two lines: without the last house, and without the first house.
* `solve(lis)` — the House Robber recurrence, run forward on one line.
* `dp(i)` — the most money from houses `i..length-1` of `lis`.
* `if i >= length: return 0` — past the last house, nothing left to take.
* `skip_current = dp(i + 1)` and `rob_current = lis[i] + dp(i + 2)` — skip house `i`, or rob it and jump over its neighbour.
* `memo = {}` **inside** `solve` — each slice needs its own cache, because `dp(i)` means "house `i` of *this* list".
* `max(solve(nums1), solve(nums2))` — whichever way of breaking the circle earns more.

**Recall:** `answer = max(solve(nums[:-1]), solve(nums[1:]))`, where each `solve` is House Robber's `dp(i) = max(dp(i + 1), lis[i] + dp(i + 2))`.

## 2. Template

* **State:** `dp(i)` = max money from houses `i..length-1` of the current line `lis`
* **Choice:** on the circle, skip the first house or skip the last; on each line, rob house `i` or skip it
* **Recurrence:** `dp(i) = max(dp(i + 1), lis[i] + dp(i + 2))`
* **Base:** `dp(i >= length) = 0`
* **Guard:** handle `n == 1` before slicing; use a fresh memo for every slice

## 3. Code

**Top-down with memoization** (primary solution). The `dp` inside `solve` is the House Robber recurrence, run on one slice.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
            
        nums1 = nums[:-1]  # Exclude last house
        nums2 = nums[1:]   # Exclude first house
        
        def solve(lis):
            length = len(lis)
            memo = {}
            
            def dp(i):
                # Base case: if we go past the last house, 0 loot
                if i >= length:
                    return 0
                if i in memo:
                    return memo[i]
                
                # Forward choices:
                # 1. Skip house i and move forward to i + 1
                # 2. Rob house i and move forward to i + 2
                skip_current = dp(i + 1)
                rob_current = lis[i] + dp(i + 2)
                
                memo[i] = max(skip_current, rob_current)
                return memo[i]
            
            return dp(0)
            
        return max(solve(nums1), solve(nums2))
```

### Alternative: Tabulation

The circle-level line (`max(solve(nums1), solve(nums2))`) never changes. Only `solve` is converted, with the same four moves as House Robber: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization (inside `solve`) | Tabulation (inside `solve`) |
|---|---|
| `memo = {}` (fresh per slice) | `dp = [0] * (length + 2)` (fresh per slice, plus two "past the end" slots) |
| `if i >= length: return 0` | `dp[length]` and `dp[length + 1]` stay `0` |
| `max(dp(i + 1), lis[i] + dp(i + 2))` | `dp[i] = max(dp[i + 1], lis[i] + dp[i + 2])` |
| `dp(i)` asks for **larger** houses | `for i in range(length - 1, -1, -1)` — fill from the last house backward |
| `return dp(0)` | `return dp[0]` |

The two zero slots stand in for the base case, so a one-house slice needs no special guard.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        def solve(lis):
            length = len(lis)
            dp = [0] * (length + 2)        # dp[length], dp[length + 1] = 0: past the end

            for i in range(length - 1, -1, -1):
                skip_current = dp[i + 1]
                rob_current = lis[i] + dp[i + 2]
                dp[i] = max(skip_current, rob_current)

            return dp[0]

        return max(solve(nums[:-1]), solve(nums[1:]))
```

**Shrink `solve` to two variables:** `nxt` is `dp[i + 1]` and `nxt2` is `dp[i + 2]`. Starting both at 0 acts like two empty houses past the end.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def solve(lis):
            nxt, nxt2 = 0, 0               # dp[length], dp[length + 1]
            for i in range(len(lis) - 1, -1, -1):
                cur = max(nxt, lis[i] + nxt2)
                nxt2, nxt = nxt, cur
            return nxt                     # dp[0]

        return max(solve(nums[:-1]), solve(nums[1:]))
```

## 4. Dry Run (`nums = [1, 2, 3, 1]`)

Calls are shown in your order: skip first, then rob.

```text
rob([1, 2, 3, 1]) = max(4, 3) = 4
├─ solve([1, 2, 3])  → skip the last house
│   └─ dp(0) = max(dp(1), 1 + dp(2)) = max(3, 1 + 3) = 4
│       ├─ skip: dp(1) = max(dp(2), 2 + dp(3)) = max(3, 2 + 0) = 3
│       │   ├─ skip: dp(2) = max(dp(3), 3 + dp(4)) = max(0, 3 + 0) = 3
│       │   └─ rob: 2 + dp(3) = 2 + 0           (base: past the end)
│       └─ rob: 1 + dp(2) = 1 + 3               (dp(2) cached — not recomputed)
└─ solve([2, 3, 1])  → skip the first house
    └─ dp(0) = max(dp(1), 2 + dp(2)) = max(3, 2 + 1) = 3
        ├─ skip: dp(1) = max(dp(2), 3 + dp(3)) = max(1, 3 + 0) = 3
        │   ├─ skip: dp(2) = max(dp(3), 1 + dp(4)) = max(0, 1 + 0) = 1
        │   └─ rob: 3 + dp(3) = 3 + 0           (base: past the end)
        └─ rob: 2 + dp(2) = 2 + 1               (dp(2) cached — not recomputed)
```

Best robbery: houses 0 and 2 → 1 + 3 = 4.

## 5. Complexity

* **States:** each `solve` call has its own memo keyed by the house index `i`, at most `n - 1` entries, and it runs twice.
* **Time:** O(n) — two passes over lines of `n - 1` houses, one `max` per state (the two slices add one more O(n) copy).
* **Space:** O(n) — the slice copies, plus each memo and a recursion depth of `n - 1`. Two rolling variables remove the memo and the stack, but the slice copies stay O(n); pass `(lo, hi)` bounds instead of slicing to reach true O(1).

## 6. Recall (30 seconds)

* **Circle → two lines:** `nums[:-1]` and `nums[1:]`; the answer is the max of the two.
* **Each line is House Robber:** `dp(i) = max(dp(i + 1), lis[i] + dp(i + 2))`, `dp(i >= length) = 0`.
* **Pitfalls:** guard `n == 1` before slicing, and give every slice its own memo.
