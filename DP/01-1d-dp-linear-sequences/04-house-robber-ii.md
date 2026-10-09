# 04. House Robber II

**LC 213** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / Circular Array

---

## 1. Intuition

The houses now form a **circle**, so house `0` and the last house are neighbours and can never both be robbed. Break the circle in two ways: either the last house is off the table (rob houses `0..n - 2`), or the first house is (rob houses `1..n - 1`). Each of those is just an ordinary straight line of houses, exactly House Robber. Solve both and take the better.

* `if n == 1` — a single house has no neighbour to clash with, and slicing `nums[:-1]` would give an empty list.
* `nums[:-1]` and `nums[1:]` — the two lines: without the last house, and without the first house.
* `rob_linear(arr)` — the House Robber recurrence, run on one line.
* `memo = {}` **inside** `rob_linear` — each slice needs its own cache, because `solve(i)` means "house `i` of *this* array".
* `max(rob_linear(...), rob_linear(...))` — whichever way of breaking the circle earns more.

**Recall:** `answer = max(rob_linear(nums[:-1]), rob_linear(nums[1:]))`.

## 2. Template

* **State:** `solve(i)` = max money from houses `0..i` of the current line `arr`
* **Choice:** on the circle, skip the first house or skip the last; on each line, rob house `i` or skip it
* **Recurrence:** `solve(i) = max(arr[i] + solve(i - 2), solve(i - 1))`
* **Base:** `solve(0) = arr[0]`, `solve(1) = max(arr[0], arr[1])`
* **Guard:** handle `n == 1` before slicing; use a fresh memo for every slice

## 3. Code

**Top-down with memoization** (primary solution). The `solve` inside `rob_linear` is the House Robber recurrence, run on one slice.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        # Edge Case: Single house can be robbed directly
        if n == 1:
            return nums[0]

        def rob_linear(arr: list[int]) -> int:
            memo = {}

            def solve(i: int) -> int:
                if i == 0:
                    return arr[0]
                if i == 1:
                    return max(arr[0], arr[1])
                if i in memo:
                    return memo[i]

                memo[i] = max(arr[i] + solve(i - 2), solve(i - 1))
                return memo[i]

            return solve(len(arr) - 1)

        # Case 1: Rob houses 0 to n-2 (Skip last house)
        # Case 2: Rob houses 1 to n-1 (Skip first house)
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### Alternative: Tabulation

The circle-level line (`max(rob_linear(nums[:-1]), rob_linear(nums[1:]))`) never changes. Only `rob_linear` is converted, with the same four moves as House Robber: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization (inside `rob_linear`) | Tabulation (inside `rob_linear`) |
|---|---|
| `memo = {}` (fresh per slice) | `dp = [0] * m` (fresh per slice) |
| `i == 0` → `arr[0]`, `i == 1` → `max(arr[0], arr[1])` | `dp[0] = arr[0]`, `dp[1] = max(arr[0], arr[1])` |
| `max(arr[i] + solve(i - 2), solve(i - 1))` | `dp[i] = max(pick, not_pick)` with `pick = arr[i] + dp[i - 2]`, `not_pick = dp[i - 1]` |
| `solve` asks for smaller houses | `for i in range(2, m)` — smaller houses get filled first |
| `return solve(len(arr) - 1)` | `return dp[m - 1]` |

**Base-case catch:** a one-house slice has no `dp[1]` slot, so the table needs `if m == 1: return arr[0]`.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        # Edge Case: Single house can be robbed directly
        if n == 1:
            return nums[0]

        def rob_linear(arr: list[int]) -> int:
            m = len(arr)
            if m == 1:
                return arr[0]

            dp = [0] * m
            dp[0] = arr[0]
            dp[1] = max(arr[0], arr[1])

            for i in range(2, m):
                pick = arr[i] + dp[i - 2]
                not_pick = dp[i - 1]
                dp[i] = max(pick, not_pick)

            return dp[m - 1]

        # Case 1: Rob houses 0 to n-2 (Skip last house)
        # Case 2: Rob houses 1 to n-1 (Skip first house)
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

**Shrink `rob_linear` to two variables:** `rob1` is `dp[i - 2]` and `rob2` is `dp[i - 1]`. Starting both at 0 acts like two empty houses before the first, so no base cases are needed.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_linear(arr: list[int]) -> int:
            rob1, rob2 = 0, 0
            for n in arr:
                new_rob = max(n + rob1, rob2)
                rob1 = rob2
                rob2 = new_rob
            return rob2

        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

## 4. Dry Run (`nums = [1, 2, 3, 1]`)

```text
rob([1, 2, 3, 1]) = max(4, 3) = 4
├─ rob_linear([1, 2, 3])  → skip the last house
│   └─ solve(2) = max(3 + solve(0), solve(1)) = max(3 + 1, 2) = 4
│       ├─ solve(0) = 1   (base)
│       └─ solve(1) = 2   (base: max(1, 2))
└─ rob_linear([2, 3, 1])  → skip the first house
    └─ solve(2) = max(1 + solve(0), solve(1)) = max(1 + 2, 3) = 3
        ├─ solve(0) = 2   (base)
        └─ solve(1) = 3   (base: max(2, 3))
```

Best robbery: houses 0 and 2 → 1 + 3 = 4.

## 5. Complexity

* **States:** each `rob_linear` call has its own memo keyed by the house index `i`, at most `n - 1` entries, and it runs twice.
* **Time:** O(n) — two passes over lines of `n - 1` houses, one `max` per state (the two slices add one more O(n) copy).
* **Space:** O(n) — the slice copies, plus each memo and a recursion depth of `n - 1`. Two rolling variables remove the memo and the stack, but the slice copies stay O(n); pass `(lo, hi)` bounds instead of slicing to reach true O(1).

## 6. Recall (30 seconds)

* **Circle → two lines:** `nums[:-1]` and `nums[1:]`; the answer is the max of the two.
* **Each line is House Robber:** `solve(i) = max(arr[i] + solve(i - 2), solve(i - 1))`.
* **Pitfalls:** guard `n == 1` before slicing, and give every slice its own memo.
