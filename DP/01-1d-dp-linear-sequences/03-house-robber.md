# 03. House Robber

**LC 198** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / Include-Exclude

---

## 1. Intuition

You walk down a street of houses, and robbing two **adjacent** houses trips the alarm. At house `i` you have exactly two options. **Rob it:** then house `i - 1` is off-limits, so you add its money to the best you could do up to `i - 2`. **Skip it:** then the best you could do up to `i - 1` simply carries over. Take the better of the two.

* `dp(i)` — the most money you can take from houses `0..i`.
* `if i == 0: return nums[i]` — with a single house, take it.
* `if i < 0: return 0` — no houses left, so nothing to take. This also removes the need for a separate base case at house 1, because `dp(1) = max(nums[1] + dp(-1), dp(0)) = max(nums[1], nums[0])`.
* `not_rob = dp(i-1)` — skip house `i`; the best of houses `0..i - 1` carries over.
* `rob = nums[i] + dp(i-2)` — rob house `i`, skip `i - 1`, and add the best of houses `0..i - 2`.
* `max(rob , not_rob)` — pick whichever choice earns more.
* `memo[i]` — both branches reach `dp(i - 2)`, so without the cache the calls blow up exponentially; with it each house is solved once.

**Recall:** `dp(i) = max(nums[i] + dp(i - 2), dp(i - 1))`.

## 2. Template

* **State:** `dp(i)` = max money from houses `0..i`
* **Choice:** rob house `i`, or skip it
* **Recurrence:** `dp(i) = max(nums[i] + dp(i - 2), dp(i - 1))`
* **Base:** `dp(0) = nums[0]`, `dp(i < 0) = 0`
* **Guard:** `dp(-1) = 0` also covers house 1, since `dp(1)` calls `dp(-1)`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        memo = {}
        max_sum = float('-inf')
        n = len(nums)

        def dp(i):

            if i == 0:
                return nums[i]

            if i < 0:
                return 0

            if i in memo:
                return memo[i]

            not_rob = dp(i-1)
            rob = nums[i] + dp(i-2)

            memo[i] = max(rob , not_rob)

            return memo[i]

        return dp(n-1)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by house `i`) | `dp = [0] * n` (one slot per house) |
| `if i == 0: return nums[i]` | `dp[0] = nums[0]` |
| `if i < 0: return 0` | a table has no negative slot, so write `dp[1] = max(nums[0], nums[1])` directly (that is `dp(1)` with `dp(-1) = 0` plugged in) and start the loop at 2 |
| `rob = nums[i] + dp(i-2)` and `not_rob = dp(i-1)`, then `max` | `pick = nums[i] + dp[i - 2]` and `not_pick = dp[i - 1]`, then `dp[i] = max(pick, not_pick)` |
| `dp` asks for smaller houses | `for i in range(2, n)` — smaller houses get filled first |
| `return dp(n-1)` | `return dp[n - 1]` |

**Loop-order rule:** whatever the memo asks for (`i - 1`, `i - 2`) must already be filled when you reach `i`, so loop upward from the base cases.

**Base-case catch:** in the memo the base cases fire on their own. In a table you write them yourself, so a single house needs the `n == 1` guard (there is no `dp[1]` slot).

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)

        if n == 1:
            return nums[0]

        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, n):
            pick = nums[i] + dp[i - 2]
            not_pick = dp[i - 1]
            dp[i] = max(pick, not_pick)

        return dp[n - 1]
```

**Shrink to O(1) space:** `dp[i]` only reads the previous two slots. `rob1` is `dp[i - 2]` and `rob2` is `dp[i - 1]`. Starting both at 0 acts like two empty houses before house 0, so no special base cases are needed.

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        rob1, rob2 = 0, 0

        # [rob1, rob2, n, n+1, ...]
        for n in nums:
            temp = max(n + rob1, rob2)
            rob1 = rob2
            rob2 = temp

        return rob2
```

## 4. Dry Run (`nums = [2, 7, 9, 3, 1]`)

```text
dp(4) = 12
├─ not rob: dp(3) = 11
│   ├─ not rob: dp(2) = 11
│   │   ├─ not rob: dp(1) = 7
│   │   │   ├─ not rob: dp(0) = 2            (base)
│   │   │   └─ rob: 7 + dp(-1) = 7 + 0       (base: no houses left)
│   │   └─ rob: 9 + dp(0) = 9 + 2 = 11       (base)
│   └─ rob: 3 + dp(1) = 3 + 7 = 10           (dp(1) cached — not recomputed)
└─ rob: 1 + dp(2) = 1 + 11 = 12              (dp(2) cached — not recomputed)
```

Best robbery: houses 0, 2 and 4 → 2 + 9 + 1 = 12.

## 5. Complexity

* **States:** `memo` is keyed by the house index `i`, so at most `n` entries (`dp(0)` and `dp(-1)` return before touching it).
* **Time:** O(n) — each house is solved once, and each solve is one `max` of two values that are already known (base cases or cache hits).
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes `n` deep. Tabulation is O(n) too; the two-variable version is O(1).

## 6. Recall (30 seconds)

* **State:** `dp(i)` = max money from houses `0..i`.
* **Transition:** `max(nums[i] + dp(i - 2), dp(i - 1))`; `dp(0) = nums[0]`, `dp(i < 0) = 0`.
* **Speed:** cache → O(n); table's `n == 1` guard; two variables → O(1) space.
