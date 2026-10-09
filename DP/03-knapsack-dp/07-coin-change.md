# 07. Coin Change

**LC 322** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / Unbounded Knapsack (pick / not-pick)

---

## 1. Intuition

Go through the coins one at a time, in order, while keeping a running sum that starts at `0`. At coin `i` you have two choices. **Pick it:** pay one coin, add its value to the running sum, and stay on coin `i`, because a coin can be used again. **Don't pick it:** move to the next coin and never use this one again. Landing exactly on `amount` costs nothing more, and going past it is impossible.

* `dp(i, current_sum)` — the fewest **additional** coins needed to reach `amount`, using coins from index `i` onward, when you already have `current_sum`.
* `if current_sum == amount: return 0` — exactly on the target, so no more coins are needed. This check comes first, so it wins even when the coins are used up.
* `if i >= len(coins) or current_sum > amount: return float('inf')` — no coins left to choose from, or you overshot. Both are impossible, and `inf` makes `min` ignore them.
* `pick = 1 + dp(i,current_sum + coins[i])` — use coin `i` (`+ 1` coin) and **stay on `i`** so it can be picked again.
* `not_pick = dp(i+1,current_sum)` — skip coin `i` for good and move to the next coin.
* `min(pick,not_pick)` — take the cheaper choice.
* `memo[(i,current_sum)]` — different pick / not-pick histories reach the same (coin index, running sum), so each is solved once.
* the last line — if the answer is still `inf`, the amount can't be made, so return `-1`.

**Recall:** `dp(i, s) = min(1 + dp(i, s + coins[i]), dp(i + 1, s))`.

## 2. Template

* **State:** `dp(i, current_sum)` = fewest more coins to reach `amount` using coins `i..end`, starting from `current_sum`
* **Choice:** pick coin `i` (and stay on it), or not-pick it (move to `i + 1`)
* **Recurrence:** `dp(i, s) = min(1 + dp(i, s + coins[i]), dp(i + 1, s))`
* **Base:** `s == amount` → `0`; `i >= len(coins)` or `s > amount` → `inf`
* **Guard:** pick **stays on `i`** (unbounded reuse), and the `== amount` check comes before the out-of-coins check

## 3. Code

**Top-down with memoization, pick / not-pick** (primary solution).

```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:

        memo = {}

        def dp(i,current_sum):

            if current_sum == amount:
                return 0

            if i >= len(coins) or current_sum > amount:
                return float('inf')

            if (i,current_sum) in memo:
                return memo[(i,current_sum)]

            pick = 1 + dp(i,current_sum + coins[i])
            not_pick = dp(i+1,current_sum)

            memo[(i,current_sum)] = min(pick,not_pick)
            return memo[(i,current_sum)]

        ans = dp(0,0)
        return ans if ans != float('inf') else -1
```

### Alternative: Tabulation

The memo has two state variables, `(i, current_sum)`, so the natural table is 2D: one row per coin. But `pick` reads the **same** row (a larger sum) and `not_pick` reads the **next** row, so one array is enough. Four moves turn the memo into it: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo[(i, current_sum)]` | `dp[s]` — one array over running sums `0..amount`; the loop over coins plays the role of `i` |
| `if current_sum == amount: return 0` | `dp[amount] = 0` |
| `i >= len(coins) or current_sum > amount: return inf` | everything else starts as `inf` ("can't reach the target yet"), and the inner loop stops at `amount - c` so the sum never overshoots |
| `not_pick = dp(i+1, current_sum)` | the value already sitting in `dp[s]` from the previous coins |
| `pick = 1 + dp(i, current_sum + coins[i])` | `1 + dp[s + c]`, already updated for this coin, so it can be picked again |
| `min(pick, not_pick)` | `dp[s] = min(dp[s], 1 + dp[s + c])` |
| the `i` dimension | outer loop `for c in coins` |
| `current_sum` asks for **larger** sums | inner loop **descending**, from `amount - c` down to `0` |
| `dp(0, 0)` and the `-1` check | `return dp[0] if dp[0] != inf else -1` |

**Loop-order rule:** the memo asks for larger sums, so the sums run downward. That also lets a coin repeat: when you reach `s`, `dp[s + c]` has already been updated with coin `c`. (Whether "repeat" means ascending or descending depends on the table's meaning. Here the table indexes the sum so far, so it is descending.)

```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[amount] = 0                                   # base: standing exactly on the target

        for c in coins:
            for s in range(amount - c, -1, -1):          # descending: dp[s + c] already includes coin c
                dp[s] = min(dp[s], 1 + dp[s + c])

        return dp[0] if dp[0] != float('inf') else -1
```

### Alternative: single-index memo (loop over coins)

The order of coins can't change a "fewest coins" answer, so the coin index isn't actually needed. At each running total you can simply try **every** coin. That leaves only `amount` states instead of `amount × len(coins)`, which makes it leaner, though it is no longer a pick / not-pick.

```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        memo = {}

        # Forward transition: dp(curr_amount) computes min coins to reach target from curr_amount
        def dp(curr_amount):
            # Base Case 1: Target reached exactly
            if curr_amount == amount:
                return 0
            
            # Base Case 2: Over shot target
            if curr_amount > amount:
                return float('inf')

            if curr_amount in memo:
                return memo[curr_amount]

            min_coins = float('inf')

            # Forward transition: Add each coin to move forward toward amount
            for c in coins:
                res = dp(curr_amount + c)
                if res != float('inf'):
                    min_coins = min(min_coins, res + 1)

            memo[curr_amount] = min_coins
            return memo[curr_amount]

        ans = dp(0)  # Start building forward from 0
        return ans if ans != float('inf') else -1
```

## 4. Dry Run (`coins = [1, 2]`, `amount = 3`)

Each line shows a choice and its value; the choice's own two options are nested under it.

```text
dp(0,0) = 2
├─ pick 1 → 1 + dp(0,1) = 2
│   ├─ pick 1 → 1 + dp(0,2) = 2
│   │   ├─ pick 1 → 1 + dp(0,3) = 1        (dp(0,3) = 0, base: on the target)
│   │   └─ not pick → dp(1,2) = inf
│   │       ├─ pick 2 → 1 + dp(1,4) = inf    (base: overshot)
│   │       └─ not pick → dp(2,2) = inf      (base: out of coins)
│   └─ not pick → dp(1,1) = 1
│       ├─ pick 2 → 1 + dp(1,3) = 1        (dp(1,3) = 0, base: on the target)
│       └─ not pick → dp(2,1) = inf          (base: out of coins)
└─ not pick → dp(1,0) = inf
    ├─ pick 2 → 1 + dp(1,2) = inf          (dp(1,2) cached — not recomputed)
    └─ not pick → dp(2,0) = inf              (base: out of coins)
```

Best answer: 2 coins (`1 + 2`).

## 5. Complexity

* **States:** `memo` is keyed by `(i, current_sum)`, so at most `len(coins) × amount` entries (the base cases return before touching it).
* **Time:** O(amount × len(coins)) — each state makes one pick call and one not-pick call, and everything else is O(1).
* **Space:** O(amount × len(coins)) for the memo, plus recursion depth up to `amount + len(coins)` (a run of picks of a coin worth 1). The table is O(amount). For large amounts use the table, since Python's default recursion limit is 1000.

## 6. Recall (30 seconds)

* **State:** `dp(i, current_sum)` = fewest more coins to reach `amount`, using coins from `i` onward.
* **Transition:** `min(1 + dp(i, s + coins[i]), dp(i + 1, s))`; pick **stays on `i`**. Base: `s == amount` → `0`; out of coins or overshoot → `inf`.
* **Pitfall:** if the result is still `inf`, return `-1`.
