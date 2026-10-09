# 08. Coin Change II

**LC 518** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Unbounded Knapsack (pick / not-pick, counting combinations)

---

## 1. Intuition

Now you count the **number of ways** to reach `amount`, and `[1, 2]` and `[2, 1]` must count as **one** way (a combination, not a permutation). The trick is to go through the coins in a fixed order while keeping a running sum that starts at `0`. At coin `i` you either **pick** it (add its value, and stay on `i` because it can be used again) or **not pick** it (move on to the next coin for good). Each combination can then only be built in one order.

* `dp(i,current_sum)` — the number of ways to reach `amount` from `current_sum`, using coins from index `i` onward.
* `if current_sum == amount: return 1` — exactly on the target, so this is one complete combination.
* `if i >= len(coins) or current_sum > amount: return 0` — out of coins, or overshot, so there is no way.
* `pick = dp(i,current_sum + coins[i])` — use one more copy of coin `i`, and **stay on `i`** so it can repeat.
* `not_pick = dp(i+1,current_sum)` — never use coin `i` again; move to the next coin.
* why `i` is in the state — the fixed coin order means each combination is built in exactly one way, so `[1, 2]` and `[2, 1]` are not double-counted.
* `pick + not_pick` — every combination either uses this coin (at least once more) or doesn't.
* `memo[(i,current_sum)]` — different histories reach the same (coin index, running sum), so each is solved once.

**Recall:** `dp(i, s) = dp(i, s + coins[i]) + dp(i + 1, s)`.

## 2. Template

* **State:** `dp(i, current_sum)` = ways to reach `amount` from `current_sum` using coins `i..end`
* **Choice:** pick coin `i` (and stay on it), or not-pick it (move to `i + 1`)
* **Recurrence:** `dp(i, s) = dp(i, s + coins[i]) + dp(i + 1, s)`
* **Base:** `s == amount` → `1`; `i >= len(coins)` or `s > amount` → `0`
* **Guard:** the coin index is what stops `[1, 2]` and `[2, 1]` from both being counted, and the `== amount` check comes first

## 3. Code

**Top-down with memoization, pick / not-pick** (primary solution).

```python
class Solution:
    def change(self, amount: int, coins: list[int]) -> int:

        memo = {}

        def dp(i,current_sum):

            if current_sum == amount:
                return 1
            
            if i >= len(coins) or current_sum > amount:
                return 0

            if (i,current_sum) in memo:
                return memo[(i,current_sum)]

            pick = dp(i,current_sum + coins[i])
            not_pick =  dp(i+1,current_sum)

            memo[(i,current_sum)] = pick + not_pick

            return memo[(i,current_sum)]

        return dp(0,0)
```

### Alternative: Tabulation

The memo has two state variables, `(i, current_sum)`, so the natural table is 2D: one row per coin. But `pick` reads the **same** row (a larger sum) and `not_pick` reads the **next** row, so one array is enough. Four moves turn the memo into it: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo[(i, current_sum)]` | `dp[s]` — one array over running sums `0..amount`; the loop over coins plays the role of `i` |
| `if current_sum == amount: return 1` | `dp[amount] = 1` |
| `i >= len(coins) or current_sum > amount: return 0` | everything else starts at `0`, and the inner loop stops at `amount - c` so the sum never overshoots |
| `not_pick = dp(i+1, current_sum)` | the value already sitting in `dp[s]` from the previous coins |
| `pick = dp(i, current_sum + coins[i])` | `dp[s + c]`, already updated for this coin, so it can be reused |
| `pick + not_pick` | `dp[s] += dp[s + c]` |
| the `i` dimension | outer loop `for c in coins` |
| `current_sum` asks for **larger** sums | inner loop **descending**, from `amount - c` down to `0` |
| `dp(0, 0)` | `return dp[0]` |

**Loop-order rule:** the memo asks for larger sums, so the sums run downward, which also lets a coin repeat, because `dp[s + c]` has already been updated with coin `c`. Coins are the **outer** loop so each combination is counted once; swapping the two loops would count permutations.

```python
class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        dp = [0] * (amount + 1)
        dp[amount] = 1                                   # base: standing exactly on the target = one combination

        for c in coins:                                  # coins outer: each combination is counted once
            for s in range(amount - c, -1, -1):          # descending: dp[s + c] already includes coin c
                dp[s] += dp[s + c]

        return dp[0]
```

### Alternative: remaining-amount memo

Your earlier version counts **down** instead: `i` is the amount still to make, so `i == 0` means done. The `take` / `skip` logic is the same.

```python
from typing import List

class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        memo = {}

        def dp(i: int, idx: int) -> int:
            # Base Case 1: Exact amount formed -> 1 valid combination
            if i == 0:
                return 1
            
            # Base Case 2: Out of bounds or ran out of coins -> 0 valid combinations
            if i < 0 or idx == len(coins):
                return 0

            if (i, idx) in memo:
                return memo[(i, idx)]

            # TAKE: Subtract current coin, stay at 'idx' (can reuse this coin)
            take = dp(i - coins[idx], idx)

            # SKIP: Don't subtract, move to 'idx + 1' (never see this coin again)
            skip = dp(i, idx + 1)

            memo[(i, idx)] = take + skip
            return memo[(i, idx)]

        return dp(amount, 0)
```

Its table counts the remaining amount **upward**, so the sums run **ascending**, and `dp[i - coin]` has already been updated for this coin, which allows reuse:

```python
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1  # Base Case: 1 way to make amount 0

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]

        return dp[amount]
```

## 4. Dry Run (`coins = [1, 2]`, `amount = 3`)

Each line shows a choice and its value; the choice's own two options are nested under it.

```text
dp(0,0) = 2                                coins = [1, 2], amount = 3
├─ pick 1 → dp(0,1) = 2
│   ├─ pick 1 → dp(0,2) = 1
│   │   ├─ pick 1 → dp(0,3) = 1          (base: on the target)
│   │   └─ not pick → dp(1,2) = 0
│   │       ├─ pick 2 → dp(1,4) = 0      (base: overshot)
│   │       └─ not pick → dp(2,2) = 0    (base: out of coins)
│   └─ not pick → dp(1,1) = 1
│       ├─ pick 2 → dp(1,3) = 1          (base: on the target)
│       └─ not pick → dp(2,1) = 0        (base: out of coins)
└─ not pick → dp(1,0) = 0
    ├─ pick 2 → dp(1,2) = 0              (cached — not recomputed)
    └─ not pick → dp(2,0) = 0            (base: out of coins)
```

The two combinations: `1+1+1` (three picks of coin 1) and `1+2` (pick 1, not-pick it, then pick 2).

## 5. Complexity

* **States:** `memo` is keyed by `(i, current_sum)`, so at most `len(coins) × amount` entries (the base cases return before touching it).
* **Time:** O(amount × len(coins)) — each state makes one pick call and one not-pick call, and everything else is O(1).
* **Space:** O(amount × len(coins)) for the memo, plus recursion depth up to `amount + len(coins)`. The collapsed table is O(amount).

## 6. Recall (30 seconds)

* **State:** `dp(i, current_sum)` = ways to reach `amount` from `current_sum` using coins from `i` onward.
* **Transition:** `dp(i, s + coins[i])` (pick, **stay**) plus `dp(i + 1, s)` (not pick); `s == amount` → `1`, out of coins or overshoot → `0`.
* **Table:** coins outer, sums **descending** (this orientation) → `dp[s] += dp[s + c]` counts combinations with reuse.
