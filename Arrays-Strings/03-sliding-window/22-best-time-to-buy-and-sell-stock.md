# 121. Best Time to Buy and Sell Stock

**LC 121** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Sliding window, running minimum

---

## 1. Intuition

You want to buy low and sell high, with the buy day strictly before the sell day. Instead of checking every
pair (`O(n²)`), walk through the prices once and remember the *lowest price seen so far* — that's always the
best possible buy day for anything sold today. Then just check if selling today beats your best profit yet.

* `min_price` is the cheapest price seen up to and including the current day — the best buy so far.
* `if price < min_price: min_price = price` — today is a new record low, so update the buy price. Selling on the same day as the lowest price would give `0` profit, so there's nothing to check yet.
* `elif price - min_price > max_profit` — today isn't a new low, so check whether selling now beats the best profit found so far.
* Because this is `elif`, the two checks never both run on the same day — a new minimum can't also be a new maximum profit day (selling at your own buy price is always `0`).

**Recall:** track the running minimum price; on any day that isn't a new minimum, check if `price - min_price` beats `max_profit`.

---

## 2. Approach

* **Idea:** a single left-to-right scan where the "window" is implicitly `[best buy day so far, today]` — you never need to remember *which* day was the minimum, only its value.
* **Data structure / pointers:** `min_price` (best buy price so far) and `max_profit` (best profit so far); no indices needed since the buy day is always "whichever day gave the current `min_price`".
* **Invariant:** at the start of each iteration, `min_price` is the minimum of all prices seen so far, and `max_profit` is the best `price - min_price` achievable using only days already visited.
* **Edge cases:**
  * Empty list → `max_profit` stays `0` (loop never runs).
  * One price → `0` (nothing to sell against).
  * Strictly decreasing prices → `0`, since every day sets a new `min_price` and none ever beats `0` profit.
  * Strictly increasing prices → the first day becomes `min_price` forever, and profit grows every day, ending at `prices[-1] - prices[0]`.
  * All equal prices → `0`.

---

## 3. Code

```python
class Solution:

    def maxProfit(self, prices: list[int]) -> int:
        min_price = float("inf")
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price

        return max_profit


if __name__ == "__main__":
    solution = Solution()
    assert solution.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert solution.maxProfit([7, 6, 4, 3, 1]) == 0
    assert solution.maxProfit([]) == 0
    assert solution.maxProfit([5]) == 0
    print("All tests passed")
```

---

## 4. Dry Run

`prices = [7, 1, 5, 3, 6, 4]`

| Day | `price` | `min_price` after | `price - min_price` | `max_profit` after | Action |
| --- | --- | --- | --- | --- | --- |
| **1** | `7` | `7` | — | `0` | new minimum |
| **2** | `1` | `1` | — | `0` | new minimum |
| **3** | `5` | `1` | `5 - 1 = 4` | `4` | `4 > 0` → update |
| **4** | `3` | `1` | `3 - 1 = 2` | `4` | `2 < 4` → no change |
| **5** | `6` | `1` | `6 - 1 = 5` | **`5`** | `5 > 4` → update |
| **6** | `4` | `1` | `4 - 1 = 3` | `5` | `3 < 5` → no change |

**Return:** `5`

---

## 5. Complexity

* **Time:** `O(n)` — one pass over `prices`, `O(1)` work per day.
* **Space:** `O(1)` — only `min_price` and `max_profit`.

---

## 6. Recall (30 seconds)

* **Track the floor, not the pair:** keep the running minimum price; that's always the best buy day for today's sell.
* **One check per day:** `elif price - min_price > max_profit` only runs on days that aren't a new low.
* **Kadane's connection:** this is equivalent to finding the maximum subarray sum of day-to-day price differences (`prices[i] - prices[i-1]`).
