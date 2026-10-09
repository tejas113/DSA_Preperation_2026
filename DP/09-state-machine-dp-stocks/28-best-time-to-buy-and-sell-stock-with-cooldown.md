# 28. Best Time to Buy and Sell Stock with Cooldown

**LC 309** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** State-Machine DP (cooldown)

---

## 1. Intuition

You can trade as many times as you like, but after **selling** you must rest one day before buying again. Each day you are either holding a share or not. If you are **not holding**, you can skip the day or buy. If you **are holding**, you can skip the day or sell, and selling forces the next day to be a rest, so after a sell you jump straight to day `i + 2`.

* `dp(i, holding)` — the best profit from day `i` onward, given whether you hold a share (`1` or `0`).
* `if i >= n: return 0` — no days left. It's `>=` (not `==`) because a sell jumps to `i + 2`, which can go past the end.
* `skip = dp(i + 1, holding)` — do nothing today.
* `holding` → `sell = prices[i] + dp(i + 2, 0)` — collect the price, then the next day is a forced cooldown, so continue from `i + 2`.
* not holding → `buy = -prices[i] + dp(i + 1, 1)` — pay the price and hold from tomorrow.
* `max(skip, sell)` / `max(skip, buy)` — make the move only if it beats doing nothing.
* `memo[(i, holding)]` — only `2n` states exist.

**Recall:** `dp(i, h) = max(skip, sell if holding else buy)`, where a sell continues from `i + 2`.

## 2. Template

* **State:** `dp(i, holding)` = best profit from day `i` onward
* **Choice:** do nothing, or buy (if not holding), or sell (if holding)
* **Recurrence:** holding → `max(dp(i+1, 1), prices[i] + dp(i+2, 0))`; not holding → `max(dp(i+1, 0), -prices[i] + dp(i+1, 1))`
* **Base:** `i >= n` → `0`
* **Guard:** the cooldown is encoded as the jump `i + 2` after a sell

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        memo = {}

        def dp(i: int, holding: int) -> int:
            if i >= n:
                return 0

            if (i, holding) in memo:
                return memo[(i, holding)]

            skip = dp(i + 1, holding)

            if holding:
                # Must jump to i + 2 to skip cooldown day
                sell = prices[i] + dp(i + 2, 0)
                memo[(i, holding)] = max(skip, sell)
            else:
                buy = -prices[i] + dp(i + 1, 1)
                memo[(i, holding)] = max(skip, buy)

            return memo[(i, holding)]

        return dp(0, 0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo[(i, holding)]` | `dp[i][holding]`, with `n + 2` rows |
| `if i >= n: return 0` | rows `n` and `n + 1` stay `0` (the two spare rows cover `i + 1` and `i + 2` past the end) |
| `skip = dp(i + 1, holding)` | `dp[i + 1][holding]` |
| `buy = -prices[i] + dp(i + 1, 1)` | `-prices[i] + dp[i + 1][1]` |
| `sell = prices[i] + dp(i + 2, 0)` | `prices[i] + dp[i + 2][0]` — the `i + 2` **is** the cooldown |
| `dp(i, ...)` asks for **larger** `i` | `for i in range(n - 1, -1, -1)` — from the last day backward |
| `return dp(0, 0)` | `return dp[0][0]` |

**Loop-order rule:** the memo asks for later days (`i + 1`, `i + 2`), so fill from the last day backward.

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        # dp[i][holding] = best profit from day i onward; days >= n are worth 0
        dp = [[0, 0] for _ in range(n + 2)]

        for i in range(n - 1, -1, -1):
            dp[i][0] = max(dp[i + 1][0], -prices[i] + dp[i + 1][1])   # not holding: skip or buy
            dp[i][1] = max(dp[i + 1][1], prices[i] + dp[i + 2][0])    # holding: skip, or sell and rest a day

        return dp[0][0]
```

Each row only reads the next two rows, so the table can be cut to three rolling rows for O(1) space. The state machine below is the popular form.

### Alternative: State machine (three variables)

Read the states **forward** in time. `held` is the best balance while holding a share, `sold` is the balance right after selling (this is the cooldown day), and `reset` is the balance when free to buy. A sell's cooldown becomes "from `sold` you can only move into `reset` next".

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if not prices:
            return 0

        held = float('-inf')  # Balance if holding stock
        sold = float('-inf')  # Balance right after selling stock
        reset = 0             # Balance when free to buy

        for price in prices:
            prev_sold = sold
            
            # 1. Hold stock OR buy stock today using balance from reset state
            held = max(held, reset - price)
            
            # 2. Sell stock held previously
            sold = held + price
            
            # 3. Stay in reset OR move out of cooldown (prev_sold)
            reset = max(reset, prev_sold)

        return max(sold, reset)
```

## 4. Dry Run (`prices = [1, 2, 3, 0, 2]`)

The memo's values: the best future profit from each day on, when not holding (`free`) or holding.

```text
day   price   dp(i, free)   dp(i, holding)
 0      1          3              4
 1      2          2              4
 2      3          2              3
 3      0          2              2
 4      2          0              2
```

The answer is `dp(0, free) = 3`: buy at 1, sell at 2, rest a day, buy at 0, sell at 2, for `1 + 2 = 3`. Selling at 3 instead would force a rest on the day the price is 0, so you'd miss that buy.

## 5. Complexity

* **States:** `memo` is keyed by `(i, holding)`, so at most `2n` entries.
* **Time:** O(n) — each state does a constant amount of work: one `skip` call, and one `buy` or `sell` call.
* **Space:** O(n) — the memo holds about `2n` entries and the recursion goes `n` deep (for `n` in the thousands, raise Python's recursion limit or use the table). The state machine is O(1).

## 6. Recall (30 seconds)

* **State:** `dp(i, holding)` = best profit from day `i` onward.
* **Transition:** not holding → `max(skip, -prices[i] + dp(i+1, 1))`; holding → `max(skip, prices[i] + dp(i+2, 0))`.
* **Cooldown:** a sell continues from `i + 2`, and the base case is `i >= n`.
