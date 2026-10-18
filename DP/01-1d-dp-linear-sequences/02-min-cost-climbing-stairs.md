# 02. Min Cost Climbing Stairs

**LC 746** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** 1D DP / Fibonacci-style

---

## 1. Intuition

Every step has a price you pay when you **stand on it**, and from there you jump 1 or 2 steps. You may start on step 0 or step 1, and the "top" is one position **past** the last step. Standing on step `i`, the cheapest way to finish is to pay `cost[i]` and then jump to whichever of the next two steps is cheaper to finish from.

* `dp(i)` — the cheapest total to get from step `i` to the top, **including** `cost[i]`.
* `if i >= n: return 0` — you are at (or past) the top, so there is nothing left to pay.
* `cost[i] + min(dp(i+1), dp(i+2))` — pay for step `i`, then jump 1 or 2, whichever finishes cheaper.
* `min(dp(0), dp(1))` — you may start on either step 0 or step 1, so take the cheaper start.
* `memo[i]` — each step's cheapest finish is computed once and reused.

**Recall:** `dp(i) = cost[i] + min(dp(i + 1), dp(i + 2))`, with `dp(i >= n) = 0`; the answer is `min(dp(0), dp(1))`.

## 2. Template

* **State:** `dp(i)` = cheapest cost from step `i` to the top (with `cost[i]` paid)
* **Choice:** jump to step `i + 1` or step `i + 2`
* **Recurrence:** `dp(i) = cost[i] + min(dp(i + 1), dp(i + 2))`
* **Base:** `dp(i >= n) = 0` (at or past the top)
* **Guard:** the answer is **not** `dp(0)` alone — you can also start on step 1, so return `min(dp(0), dp(1))`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:

        n = len(cost)
        memo = {}

        def dp(i):

            if i >= n:
                return 0

            if i in memo:
                return memo[i]

            memo[i] = cost[i] + min(dp(i + 1), dp(i + 2))
            return memo[i]
        
        return min(dp(0), dp(1))
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by step `i`) | `dp = [0] * (n + 2)` (one slot per step `0..n-1`, plus slots `n` and `n + 1` for the top) |
| `if i >= n: return 0` | `dp[n]` and `dp[n + 1]` stay `0` |
| `cost[i] + min(dp(i+1), dp(i+2))` | `dp[i] = cost[i] + min(dp[i + 1], dp[i + 2])` |
| `dp(i)` asks for **larger** steps | `for i in range(n - 1, -1, -1)` — fill from the top downward |
| `return min(dp(0), dp(1))` | `return min(dp[0], dp[1])` |

**Loop-order rule:** whatever the memo asks for (`i + 1`, `i + 2`) must already be filled when you reach `i`, so loop downward from the top.

```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        n = len(cost)
        dp = [0] * (n + 2)                 # dp[n], dp[n + 1] = 0: already at the top

        for i in range(n - 1, -1, -1):
            dp[i] = cost[i] + min(dp[i + 1], dp[i + 2])

        return min(dp[0], dp[1])
```

**Shrink to O(1) space:** `dp[i]` only reads the next two slots, so keep two variables (`nxt` = `dp[i + 1]`, `nxt2` = `dp[i + 2]`) and slide them down one step at a time. When the loop ends, `nxt` is `dp[0]` and `nxt2` is `dp[1]`.

```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        nxt, nxt2 = 0, 0                   # dp[n], dp[n + 1]

        for i in range(len(cost) - 1, -1, -1):
            cur = cost[i] + min(nxt, nxt2)
            nxt2, nxt = nxt, cur

        return min(nxt, nxt2)              # min(dp[0], dp[1])
```

## 4. Dry Run (`cost = [10, 15, 20, 5]`)

```text
answer = min(dp(0), dp(1)) = min(30, 20) = 20
├─ dp(0) = 10 + min(dp(1), dp(2)) = 10 + min(20, 20) = 30
│   ├─ dp(1) = 15 + min(dp(2), dp(3)) = 15 + min(20, 5) = 20
│   │   ├─ dp(2) = 20 + min(dp(3), dp(4)) = 20 + min(5, 0) = 20
│   │   │   ├─ dp(3) = 5 + min(dp(4), dp(5)) = 5 + min(0, 0) = 5
│   │   │   │   ├─ dp(4) = 0   (base: at the top)
│   │   │   │   └─ dp(5) = 0   (base: past the top)
│   │   │   └─ dp(4) = 0       (base: at the top)
│   │   └─ dp(3) = 5           (cached — not recomputed)
│   └─ dp(2) = 20              (cached — not recomputed)
└─ dp(1) = 20                  (cached — not recomputed)
```

Best route: start on step 1 (pay 15), jump 2 to step 3 (pay 5), jump to the top. Total 20.

## 5. Complexity

* **States:** `memo` is keyed by the step `i`, so at most `n` different steps (`0..n - 1`) are ever stored; `i >= n` returns before touching it.
* **Time:** O(n) — each step is computed once, and each computation is one `min` of two values that are already known (base cases or cache hits).
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes `n` deep. Tabulation is O(n) too; the two-variable version is O(1).

## 6. Recall (30 seconds)

* **State:** `dp(i)` = cheapest cost from step `i` to the top, with `cost[i]` included.
* **Transition:** `cost[i] + min(dp(i + 1), dp(i + 2))`; `dp(i >= n) = 0`.
* **Pitfall:** you can start on step 0 **or** 1, so the answer is `min(dp(0), dp(1))`.
