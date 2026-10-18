# 03. House Robber

**LC 198** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / Include-Exclude

---

## 1. Intuition

You walk down a street of houses, and robbing two **adjacent** houses trips the alarm. At house `i` you have exactly two options. **Rob it:** then house `i + 1` is off-limits, so you add its money to the best you could do from `i + 2` onward. **Skip it:** then the best you could do from `i + 1` onward simply carries over. Take the better of the two.

* `dp(i)` — the most money you can take from houses `i..n-1`.
* `if i >= n: return 0` — no houses left, so nothing to take. This one check covers both `dp(n)` and `dp(n + 1)` (the jump past the last house).
* `rob = nums[i] + dp(i+2)` — rob house `i`, skip `i + 1`, and add the best from `i + 2` onward.
* `not_rob = dp(i+1)` — skip house `i`; the best from `i + 1` onward carries over.
* `max(rob,not_rob)` — pick whichever choice earns more.
* `memo[i]` — both branches reach `dp(i + 2)`, so without the cache the calls blow up exponentially; with it each house is solved once.

**Recall:** `dp(i) = max(nums[i] + dp(i + 2), dp(i + 1))`, with `dp(i >= n) = 0`.

## 2. Template

* **State:** `dp(i)` = max money from houses `i..n-1`
* **Choice:** rob house `i`, or skip it
* **Recurrence:** `dp(i) = max(nums[i] + dp(i + 2), dp(i + 1))`
* **Base:** `dp(i >= n) = 0`
* **Guard:** use `>=`, not `==`, because robbing the last house calls `dp(n + 1)`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def rob(self, nums: list[int]) -> int:

        n = len(nums)

        memo = {}

        def dp(i):

            if i >= n:
                return 0
            
            if i in memo:
                return memo[i]

            rob = nums[i] + dp(i + 2)
            not_rob = dp(i + 1)

            memo[i] = max(rob, not_rob)
            return memo[i]
        
        return dp(0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by house `i`) | `dp = [0] * (n + 2)` (one slot per house, plus slots `n` and `n + 1` for "no houses left") |
| `if i >= n: return 0` | `dp[n]` and `dp[n + 1]` stay `0` |
| `rob = nums[i] + dp(i+2)` and `not_rob = dp(i+1)`, then `max` | `rob = nums[i] + dp[i + 2]` and `not_rob = dp[i + 1]`, then `dp[i] = max(rob, not_rob)` |
| `dp(i)` asks for **larger** houses | `for i in range(n - 1, -1, -1)` — fill from the last house backward |
| `return dp(0)` | `return dp[0]` |

**Loop-order rule:** whatever the memo asks for (`i + 1`, `i + 2`) must already be filled when you reach `i`, so loop downward from the end.

The two extra zero slots stand in for the base case, so a single house needs no special guard.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [0] * (n + 2)                 # dp[n], dp[n + 1] = 0: no houses left

        for i in range(n - 1, -1, -1):
            rob = nums[i] + dp[i + 2]
            not_rob = dp[i + 1]
            dp[i] = max(rob, not_rob)

        return dp[0]
```

**Shrink to O(1) space:** `dp[i]` only reads the next two slots. `nxt` is `dp[i + 1]` and `nxt2` is `dp[i + 2]`. Starting both at 0 acts like two empty houses past the end.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        nxt, nxt2 = 0, 0                   # dp[n], dp[n + 1]

        for i in range(len(nums) - 1, -1, -1):
            cur = max(nums[i] + nxt2, nxt)
            nxt2, nxt = nxt, cur

        return nxt                         # dp[0]
```

## 4. Dry Run (`nums = [2, 7, 9, 3, 1]`)

```text
dp(0) = 12
├─ rob: 2 + dp(2) = 2 + 10 = 12
│   ├─ rob: 9 + dp(4) = 9 + 1 = 10
│   │   ├─ rob: 1 + dp(6) = 1 + 0 = 1        (base: no houses left)
│   │   └─ not rob: dp(5) = 0                (base: no houses left)
│   └─ not rob: dp(3) = 3
│       ├─ rob: 3 + dp(5) = 3 + 0 = 3        (base: no houses left)
│       └─ not rob: dp(4) = 1                (cached — not recomputed)
└─ not rob: dp(1) = 10
    ├─ rob: 7 + dp(3) = 7 + 3 = 10           (dp(3) cached — not recomputed)
    └─ not rob: dp(2) = 10                   (cached — not recomputed)
```

Best robbery: houses 0, 2 and 4 → 2 + 9 + 1 = 12.

## 5. Complexity

* **States:** `memo` is keyed by the house index `i`, so at most `n` entries (`i >= n` returns before touching it).
* **Time:** O(n) — each house is solved once, and each solve is one `max` of two values that are already known (base cases or cache hits).
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes `n` deep. Tabulation is O(n) too; the two-variable version is O(1).

## 6. Recall (30 seconds)

* **State:** `dp(i)` = max money from houses `i..n-1`.
* **Transition:** `max(nums[i] + dp(i + 2), dp(i + 1))`; `dp(i >= n) = 0`; start at `dp(0)`.
* **Speed:** cache → O(n); two extra zero slots → no special cases; two variables → O(1) space.
