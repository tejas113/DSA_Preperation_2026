# 02. Min Cost Climbing Stairs

**LC 746** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** 1D DP / Fibonacci-style

---

## 1. Intuition

Every step has a price you pay when you **stand on it**, and from there you jump 1 or 2 steps. You may start on step 0 or step 1, and the "top" is one position **past** the last step. The cheapest way to be standing on step `i` is to pay `cost[i]` plus the cheaper of the two places you could have come from.

* `solve(i)` — the cheapest total to land on step `i`, **including** `cost[i]`.
* `if i == 0 or i == 1: return cost[i]` — you can start on either, so landing there costs only its own price.
* `cost[i] + min(solve(i - 1), solve(i - 2))` — pay for step `i`, arriving from whichever earlier step was cheaper.
* `min(solve(n - 1), solve(n - 2))` — the top is past the array, so you reach it from either of the last two steps and pay nothing extra to step off.
* `memo[i]` — each step's cheapest cost is computed once and reused.

**Recall:** `solve(i) = cost[i] + min(solve(i - 1), solve(i - 2))`; the answer is the min of the last two.

## 2. Template

* **State:** `solve(i)` = cheapest cost to stand on step `i` (with `cost[i]` paid)
* **Choice:** you arrived from step `i - 1` or step `i - 2`
* **Recurrence:** `solve(i) = cost[i] + min(solve(i - 1), solve(i - 2))`
* **Base:** `solve(0) = cost[0]`, `solve(1) = cost[1]` (free choice of starting step)
* **Guard:** the answer is **not** `solve(n)` — the top is past the last step, so return `min(solve(n - 1), solve(n - 2))`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        memo = {}
        n = len(cost)

        def solve(i: int) -> int:
            # Base Cases: Reaching index 0 or 1 incurs just its own cost
            if i == 0 or i == 1:
                return cost[i]

            # Return cached result if already computed
            if i in memo:
                return memo[i]

            # Recurse: Minimum cost to reach step i
            memo[i] = cost[i] + min(solve(i - 1), solve(i - 2))
            return memo[i]

        # Top of the stairs can be reached from step n-1 or n-2
        return min(solve(n - 1), solve(n - 2))
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by step `i`) | `dp = [0] * n` (one slot per step `0..n-1`) |
| `if i == 0 or i == 1: return cost[i]` | `dp[0] = cost[0]`, `dp[1] = cost[1]` |
| `cost[i] + min(solve(i - 1), solve(i - 2))` | `dp[i] = cost[i] + min(dp[i - 1], dp[i - 2])` |
| `solve` asks for smaller steps | `for i in range(2, n)` — smaller steps get filled first |
| `return min(solve(n - 1), solve(n - 2))` | `return min(dp[n - 1], dp[n - 2])` |

**Loop-order rule:** whatever the memo asks for (`i - 1`, `i - 2`) must already be filled when you reach `i`, so loop upward from the base cases.

```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        n = len(cost)
        dp = [0] * n

        # Base Cases
        dp[0] = cost[0]
        dp[1] = cost[1]

        # Build DP array iteratively
        for i in range(2, n):
            dp[i] = cost[i] + min(dp[i - 1], dp[i - 2])

        # Top of the stairs can be reached from n-1 or n-2
        return min(dp[n - 1], dp[n - 2])
```

**Shrink to O(1) space:** `dp[i]` only reads the previous two slots, so keep two variables (`first` = step `i - 2`, `second` = step `i - 1`) and slide them forward.

```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        first = cost[0]
        second = cost[1]

        for i in range(2, len(cost)):
            curr = cost[i] + min(first, second)
            first = second
            second = curr

        return min(first, second)
```

## 4. Dry Run (`cost = [10, 15, 20, 5]`)

```text
answer = min(solve(3), solve(2)) = min(20, 30) = 20
├─ solve(3) = 5 + min(solve(2), solve(1)) = 5 + min(30, 15) = 20
│   ├─ solve(2) = 20 + min(solve(1), solve(0)) = 20 + min(15, 10) = 30
│   │   ├─ solve(1) = 15   (base)
│   │   └─ solve(0) = 10   (base)
│   └─ solve(1) = 15       (base)
└─ solve(2) = 30           (cached — not recomputed)
```

Best route: start on step 1 (pay 15), jump 2 to step 3 (pay 5), jump to the top. Total 20.

## 5. Complexity

* **States:** `memo` is keyed by the step `i`, so at most `n` different steps are ever stored.
* **Time:** O(n) — each step is computed once, and each computation is one `min` of two values that are already known (base cases or cache hits).
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes `n` deep. Tabulation is O(n) too; the two-variable version is O(1).

## 6. Recall (30 seconds)

* **State:** `solve(i)` = cheapest cost to stand on step `i`, with `cost[i]` included.
* **Transition:** `cost[i] + min(solve(i - 1), solve(i - 2))`; bases are steps 0 and 1.
* **Pitfall:** the answer is `min(solve(n - 1), solve(n - 2))`, not `solve(n)`.
