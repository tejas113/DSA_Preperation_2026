# 122. Best Time to Buy and Sell Stock II

**LC 122** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Greedy, sum every upward day-to-day slope

---

## 1. Intuition

With unlimited transactions allowed, holding a stock across a multi-day rise gives exactly the same profit
as buying and selling on every single day of that rise: `day3 - day1 = (day3 - day2) + (day2 - day1)`. So
there's no need to find actual buy/sell points at all — just add up every positive day-to-day price change,
and that sum equals the maximum possible profit.

* `for i in range(1, len(prices))` compares each day to the one before it.
* `if prices[i] > prices[i - 1]: max_profit += prices[i] - prices[i - 1]` — captures the gain from an upward move; a downward or flat move contributes nothing.
* Because consecutive upward differences sum to the same total as one big buy-low-sell-high move across the whole rise, this greedy sum is provably optimal — no need to track actual entry/exit days.

**Recall:** sum `prices[i] - prices[i-1]` for every day the price went up; ignore every day it didn't.

---

## 2. Approach

* **Idea:** rather than identifying which days to buy and sell on, decompose the whole price sequence into its up-moves and down-moves — only the up-moves contribute profit, and unlimited transactions means every one of them can be captured.
* **Data structure / pointers:** just `max_profit`, accumulated in a single pass; `i` walks the array comparing consecutive days.
* **Invariant:** at every step, `max_profit` equals the sum of every positive `prices[j] - prices[j-1]` for `j` from `1` to `i` — which is exactly the maximum achievable profit using only price information up to day `i`.
* **Edge cases:**
  * Strictly decreasing prices → the condition never triggers, correctly returning `0` (no profitable trade exists).
  * Strictly increasing prices → every single day contributes, and the sum equals buying on day 1 and selling on the last day (the telescoping sum collapses to that single difference).
  * Single price → the loop range is empty, returning `0` immediately.
  * Empty array → same as above, `0`.

---

## 3. Code

```python
class Solution:

    def maxProfit(self, prices: list[int]) -> int:
        max_profit = 0

        for i in range(1, len(prices)):
            # Capture every positive price slope
            if prices[i] > prices[i - 1]:
                max_profit += prices[i] - prices[i - 1]

        return max_profit


if __name__ == "__main__":
    solution = Solution()
    assert solution.maxProfit([7, 1, 5, 3, 6, 4]) == 7
    assert solution.maxProfit([7, 6, 4, 3, 1]) == 0
    assert solution.maxProfit([1, 2, 3, 4, 5]) == 4
    assert solution.maxProfit([5]) == 0
    print("All tests passed")
```

---

## 4. Dry Run

`prices = [7, 1, 5, 3, 6, 4]`

| `i` | `prices[i-1]` | `prices[i]` | `prices[i] > prices[i-1]`? | Added | `max_profit` after |
| --- | --- | --- | --- | --- | --- |
| `1` | `7` | `1` | False | `0` | `0` |
| `2` | `1` | `5` | **True** | `+4` | `4` |
| `3` | `5` | `3` | False | `0` | `4` |
| `4` | `3` | `6` | **True** | `+3` | `7` |
| `5` | `6` | `4` | False | `0` | **`7`** |

**Return:** `7`

---

## 5. Complexity

* **Time:** `O(n)` — a single pass over `prices`.
* **Space:** `O(1)` — one scalar variable.

---

## 6. Recall (30 seconds)

* **Sum every up-move, ignore every down-move:** `max_profit += prices[i] - prices[i-1]` when positive.
* **Why it's optimal:** consecutive up-moves telescope into the same total profit as one long hold across the whole rise — no need to find actual buy/sell days.
* **Unlimited transactions is what makes this work:** capturing every single up-move is only valid because there's no cap on how many trades can happen.
