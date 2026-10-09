# 26. Best Time to Buy and Sell Stock III

**LC 123** · **Source:** LC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** State-Machine DP

---

## 1. Intuition

You can hold at most one share, and you may complete at most **2 transactions** (a transaction is a buy followed by a sell). Each day you are in one of two situations, holding a share or not, with some transactions still left. On any day you can do nothing, or make the one move that is allowed: **buy** if you don't hold, **sell** if you do.

* `dp(i, holding, transactions)` — the best profit from day `i` onward, given whether you hold a share (`1` or `0`) and how many transactions you have left.
* `if i == n or transactions == 0: return 0` — no days left, or no transactions left, so nothing more can be earned.
* `skip = dp(i + 1, holding, transactions)` — do nothing today.
* `holding` → `sell = prices[i] + dp(i + 1, 0, transactions - 1)` — collect today's price, stop holding, and use up one transaction. A transaction is counted when it **completes** (the sell).
* not holding → `buy = -prices[i] + dp(i + 1, 1, transactions)` — pay today's price and start holding. No transaction is used up yet.
* `max(skip, sell)` / `max(skip, buy)` — make the move only if it beats doing nothing.
* `memo[(i, holding, transactions)]` — three numbers identify a state, and only `n × 2 × 3` of them exist.

**Recall:** `dp(i, h, t) = max(skip, sell if holding else buy)`, and a sell uses one transaction.

## 2. Template

* **State:** `dp(i, holding, transactions)` = best profit from day `i` onward
* **Choice:** do nothing, or the one move allowed: buy if not holding, sell if holding
* **Recurrence:** holding → `max(dp(i+1, 1, t), prices[i] + dp(i+1, 0, t-1))`; not holding → `max(dp(i+1, 0, t), -prices[i] + dp(i+1, 1, t))`
* **Base:** `i == n` or `transactions == 0` → `0`
* **Guard:** count the transaction on the **sell**, so buying with one transaction left is still allowed

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        memo = {}

        def dp(i: int, holding: int, transactions: int) -> int:
            if i == n or transactions == 0:
                return 0

            if (i, holding, transactions) in memo:
                return memo[(i, holding, transactions)]

            skip = dp(i + 1, holding, transactions)

            if holding:
                sell = prices[i] + dp(i + 1, 0, transactions - 1)
                memo[(i, holding, transactions)] = max(skip, sell)
            else:
                buy = -prices[i] + dp(i + 1, 1, transactions)
                memo[(i, holding, transactions)] = max(skip, buy)

            return memo[(i, holding, transactions)]

        return dp(0, 0, 2)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**. The memo only ever looks one day ahead (`i + 1`), and each day has just `2 × 3` states, so we keep **one day's grid at a time** instead of a table over all days.

| Memoization | Tabulation |
|---|---|
| `memo[(i, holding, transactions)]` | `cur[holding][tx]` for day `i`, and `nxt[holding][tx]` for day `i + 1` |
| `if i == n or transactions == 0: return 0` | day `n` is all zeros (`nxt` starts as zeros), and `tx = 0` stays `0` |
| `skip = dp(i + 1, holding, transactions)` | `nxt[holding][tx]` |
| `buy = -prices[i] + dp(i + 1, 1, transactions)` | `-prices[i] + nxt[1][tx]`, stored in `cur[0][tx]` |
| `sell = prices[i] + dp(i + 1, 0, transactions - 1)` | `prices[i] + nxt[0][tx - 1]`, stored in `cur[1][tx]` |
| `dp(i, ...)` asks for day `i + 1` | `for i in range(n - 1, -1, -1)` — from the last day backward |
| `return dp(0, 0, 2)` | `return nxt[0][2]` |

**Loop-order rule:** the memo asks for the next day, so start at the last day and walk backward, keeping only the previous result.

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        # nxt[holding][tx] = best profit from day i + 1 onward; day n is all zeros
        nxt = [[0] * 3 for _ in range(2)]

        for i in range(n - 1, -1, -1):
            cur = [[0] * 3 for _ in range(2)]
            for tx in range(1, 3):
                cur[0][tx] = max(nxt[0][tx], -prices[i] + nxt[1][tx])       # not holding: skip or buy
                cur[1][tx] = max(nxt[1][tx], prices[i] + nxt[0][tx - 1])    # holding: skip or sell
            nxt = cur

        return nxt[0][2]
```

This is already O(1) space (a `2 × 3` grid).

### Alternative: State machine (four variables)

The famous four-variable version reads the same states **forward** in time. `first_buy` is the best balance after the 1st buy, `first_sell` the best profit after the 1st sell, `second_buy` after the 2nd buy (starting from `first_sell`'s profit), and `second_sell` after the 2nd sell.

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        first_buy = float('-inf')
        first_sell = 0
        second_buy = float('-inf')
        second_sell = 0

        for price in prices:
            # Max balance after 1st buy
            first_buy = max(first_buy, -price)
            # Max profit after 1st sell
            first_sell = max(first_sell, first_buy + price)
            # Max balance after 2nd buy (uses first_sell profit)
            second_buy = max(second_buy, first_sell - price)
            # Max profit after 2nd sell
            second_sell = max(second_sell, second_buy + price)

        return second_sell
```

## 4. Dry Run (`prices = [1, 3, 2]`)

```text
dp(0,0,2) = 2                             prices = [1, 3, 2]
├─ skip → dp(1,0,2) = 0
│   ├─ skip → dp(2,0,2) = 0
│   └─ buy 3 → -3 + dp(2,1,2) = -3 + 2 = -1
│       (dp(2,1,2) = 2, from selling 2 → 2 + dp(3,0,1) = 2)
└─ buy 1 → -1 + dp(1,1,2) = -1 + 3 = 2
    ├─ skip → dp(2,1,2) = 2               (cached — not recomputed)
    └─ sell 3 → 3 + dp(2,0,1) = 3 + 0 = 3
```

The best plan: buy at 1, sell at 3, for a profit of `2`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, holding, transactions)`, so at most `n × 2 × 3 = 6n` entries.
* **Time:** O(n) — each state does a constant amount of work: one `skip` call, and one `buy` or `sell` call.
* **Space:** O(n) — the memo holds about `6n` entries and the recursion goes `n` deep. For large `n` (up to 10^5) Python's recursion limit makes the memo unusable, so submit the table or the state machine, both O(1) space.

## 6. Recall (30 seconds)

* **State:** `dp(i, holding, transactions)` = best profit from day `i` onward.
* **Transition:** skip, or `sell` (`prices[i] + dp(i+1, 0, t-1)`) if holding, or `buy` (`-prices[i] + dp(i+1, 1, t)`) if not.
* **Speed:** roll the `2 × 3` grid backward, or use the four forward variables, for O(1) space.
