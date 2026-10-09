# 27. Best Time to Buy and Sell Stock IV

**LC 188** · **Source:** LC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** State-Machine DP (k transactions)

---

## 1. Intuition

This is Stock III with the transaction budget turned into a parameter: at most **`k`** transactions instead of a fixed 2. Nothing else changes. Each day you are holding or not, with `transactions` left, and you may do nothing or make the one allowed move (buy if not holding, sell if holding). The transaction is counted when the **sell** completes.

* `dp(i, holding, transactions)` — the best profit from day `i` onward, given whether you hold a share and how many transactions are left.
* `if i == n or transactions == 0: return 0` — no days left, or no transactions left.
* `skip = dp(i + 1, holding, transactions)` — do nothing today.
* `holding` → `sell = prices[i] + dp(i + 1, 0, transactions - 1)` — collect the price and use up one transaction.
* not holding → `buy = -prices[i] + dp(i + 1, 1, transactions)` — pay the price; no transaction is used yet.
* `return dp(0, 0, k)` — the only change from Stock III: start with `k` transactions instead of 2.
* `memo[(i, holding, transactions)]` — `n × 2 × (k + 1)` states in total.

**Recall:** the same recurrence as Stock III, started with `transactions = k`.

## 2. Template

* **State:** `dp(i, holding, transactions)` = best profit from day `i` onward
* **Choice:** do nothing, or the one move allowed: buy if not holding, sell if holding
* **Recurrence:** holding → `max(dp(i+1, 1, t), prices[i] + dp(i+1, 0, t-1))`; not holding → `max(dp(i+1, 0, t), -prices[i] + dp(i+1, 1, t))`
* **Base:** `i == n` or `transactions == 0` → `0`
* **Guard:** count the transaction on the **sell**; when `k >= n // 2` the limit no longer matters (see the shortcut below)

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
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

        return dp(0, 0, k)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**. The memo only looks one day ahead, so keep one day's `2 × (k + 1)` grid at a time.

| Memoization | Tabulation |
|---|---|
| `memo[(i, holding, transactions)]` | `cur[holding][tx]` for day `i`, `nxt[holding][tx]` for day `i + 1` |
| `if i == n or transactions == 0: return 0` | day `n` is all zeros, and `tx = 0` stays `0` |
| `skip = dp(i + 1, holding, transactions)` | `nxt[holding][tx]` |
| `buy = -prices[i] + dp(i + 1, 1, transactions)` | `-prices[i] + nxt[1][tx]`, stored in `cur[0][tx]` |
| `sell = prices[i] + dp(i + 1, 0, transactions - 1)` | `prices[i] + nxt[0][tx - 1]`, stored in `cur[1][tx]` |
| `dp(i, ...)` asks for day `i + 1` | `for i in range(n - 1, -1, -1)` |
| `return dp(0, 0, k)` | `return nxt[0][k]` |

**Loop-order rule:** the memo asks for the next day, so walk the days backward and keep only the previous grid.

```python
class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        n = len(prices)
        nxt = [[0] * (k + 1) for _ in range(2)]            # day n: all zeros

        for i in range(n - 1, -1, -1):
            cur = [[0] * (k + 1) for _ in range(2)]
            for tx in range(1, k + 1):
                cur[0][tx] = max(nxt[0][tx], -prices[i] + nxt[1][tx])       # not holding: skip or buy
                cur[1][tx] = max(nxt[1][tx], prices[i] + nxt[0][tx - 1])    # holding: skip or sell
            nxt = cur

        return nxt[0][k]
```

That is O(k) space.

### Alternative: buy/sell arrays with a greedy shortcut

Read the same states **forward** in time. `buy[t]` is the best balance after the `t`-th buy, and `sell[t]` is the best profit after the `t`-th sell. It generalizes Stock III's four variables into two arrays. If `k >= n // 2`, you can never run out of transactions, so just add up every price rise.

```python
class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        if not prices or k == 0:
            return 0

        n = len(prices)

        # Shortcut: Unlimited transactions if k >= n // 2
        if k >= n // 2:
            return sum(max(prices[i] - prices[i - 1], 0) for i in range(1, n))

        buy = [float('-inf')] * (k + 1)
        sell = [0] * (k + 1)

        for price in prices:
            for t in range(1, k + 1):
                # Balance after t-th buy: uses profit from (t-1)-th sell
                buy[t] = max(buy[t], sell[t - 1] - price)
                # Profit after t-th sell: uses balance from t-th buy
                sell[t] = max(sell[t], buy[t] + price)

        return sell[k]
```

## 4. Dry Run (`prices = [2, 4, 1]`, `k = 1`)

```text
dp(0,0,1) = 2                             prices = [2, 4, 1],  k = 1
├─ skip → dp(1,0,1) = 0
│   ├─ skip → dp(2,0,1) = 0
│   └─ buy 4 → -4 + dp(2,1,1) = -4 + 1 = -3
│       (dp(2,1,1) = 1, from selling 1 → 1 + dp(3,0,0) = 1)
└─ buy 2 → -2 + dp(1,1,1) = -2 + 4 = 2
    ├─ skip → dp(2,1,1) = 1               (cached — not recomputed)
    └─ sell 4 → 4 + dp(2,0,0) = 4 + 0 = 4  (base: no transactions left)
```

The best plan: buy at 2, sell at 4, for a profit of `2`. With a larger `k` the tree is the same shape, just with more `transactions` levels.

## 5. Complexity

* **States:** `memo` is keyed by `(i, holding, transactions)`, so at most `n × 2 × (k + 1)` entries.
* **Time:** O(n × k) — each state does a constant amount of work: one `skip` call, and one `buy` or `sell` call.
* **Space:** O(n × k) — the memo plus recursion `n` deep. The rolling grid and the buy/sell arrays are O(k).

## 6. Recall (30 seconds)

* **State:** `dp(i, holding, transactions)`, exactly as in Stock III but started with `k`.
* **Transition:** skip, or `sell` (`prices[i] + dp(i+1, 0, t-1)`) if holding, or `buy` (`-prices[i] + dp(i+1, 1, t)`) if not.
* **Shortcut:** if `k >= n // 2`, sum every positive price rise; otherwise roll a `2 × (k + 1)` grid for O(k) space.
