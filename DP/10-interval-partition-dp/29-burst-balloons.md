# 29. Burst Balloons

**LC 312** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Interval DP

---

## 1. Intuition

Bursting balloon `k` earns `left × k × right` coins, where `left` and `right` are its current neighbours. The trap is thinking about which balloon to burst **first**: that changes the neighbours of everything else, and the subproblems become tangled. The trick is to think **backwards**: pick the balloon `k` that is burst **last** in a range `[i, j]`. When `k` goes last, every other balloon in the range is already gone, so its neighbours are exactly the two balloons just **outside** the range, `A[i - 1]` and `A[j + 1]`. The left part `[i, k - 1]` and the right part `[k + 1, j]` are then independent subproblems.

* `A = [1] + nums + [1]` — pad with a virtual balloon worth 1 on each side, so the edges need no special cases.
* `dp(i, j)` — the most coins from bursting **every** balloon in `A[i..j]`, with `A[i - 1]` and `A[j + 1]` staying in place as the outer neighbours.
* `if i > j: return 0` — an empty range earns nothing.
* `for k in range(i, j + 1)` — try every balloon `k` as the **last** one burst in the range.
* `coins = A[i - 1] * A[k] * A[j + 1]` — the coins for that final burst, with the outer balloons as neighbours.
* `dp(i, k - 1) + dp(k + 1, j)` — the left and right parts, each solved with `k` still standing as one of its outer neighbours.
* `memo[(i, j)]` — each range is solved once.
* `return dp(1, len(nums))` — the real balloons sit at indices `1..n` of the padded array.

**Recall:** `dp(i, j) = max over k of A[i-1]·A[k]·A[j+1] + dp(i, k-1) + dp(k+1, j)`, where `k` is burst **last**.

## 2. Template

* **State:** `dp(i, j)` = max coins from bursting all balloons in `A[i..j]`, with `A[i - 1]` and `A[j + 1]` as the fixed outer neighbours
* **Choice:** which balloon `k` in `[i, j]` is burst **last**
* **Recurrence:** `dp(i, j) = max over k of A[i-1] * A[k] * A[j+1] + dp(i, k-1) + dp(k+1, j)`
* **Base:** `i > j` → `0`
* **Guard:** pad the array with `1` on both ends, and think "last", not "first"

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def maxCoins(self, nums: list[int]) -> int:
        # Pad array with 1 at both ends to easily handle out-of-bounds cases
        A = [1] + nums + [1]
        memo = {}

        def dp(i: int, j: int) -> int:
            # Base Case: Invalid range (no balloons to burst)
            if i > j:
                return 0

            # Cache lookup
            if (i, j) in memo:
                return memo[(i, j)]

            max_coins = 0

            # Choice: Iterate over every balloon 'k' in range [i, j], 
            # treating 'k' as the LAST balloon to be burst in this range.
            for k in range(i, j + 1):
                # Since 'k' is burst last in [i, j], all balloons inside [i, k-1] 
                # and [k+1, j] are gone. Its adjacent boundaries are A[i-1] and A[j+1].
                coins = A[i - 1] * A[k] * A[j + 1]

                # Total = coins from bursting k LAST + coins from left subproblem + coins from right subproblem
                total = coins + dp(i, k - 1) + dp(k + 1, j)

                max_coins = max(max_coins, total)

            memo[(i, j)] = max_coins
            return memo[(i, j)]

        # Solve for range from index 1 to len(nums)
        return dp(1, len(nums))
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo[(i, j)]` | `dp[i][j]`, sized `(n + 2) × (n + 2)` |
| `if i > j: return 0` | cells with `i > j` simply stay `0` |
| `for k in range(i, j + 1)` | the same `k` loop |
| `A[i-1] * A[k] * A[j+1] + dp(i, k-1) + dp(k+1, j)` | `A[i-1] * A[k] * A[j+1] + dp[i][k-1] + dp[k+1][j]` |
| `dp(i, j)` asks for **shorter** ranges | loop over range **length** `1..n`, then over `i`, with `j = i + length - 1` |
| `return dp(1, len(nums))` | `return dp[1][n]` |

**Loop-order rule:** the memo only asks for strictly shorter ranges (`[i, k - 1]` and `[k + 1, j]`), so fill the table by **increasing length**. This is the standard interval-DP order.

```python
class Solution:
    def maxCoins(self, nums: list[int]) -> int:
        A = [1] + nums + [1]
        n = len(nums)
        dp = [[0] * (n + 2) for _ in range(n + 2)]

        # L is the length of the subarray/window of balloons being burst
        for length in range(1, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                # Try bursting every balloon k LAST in range [i, j]
                for k in range(i, j + 1):
                    dp[i][j] = max(
                        dp[i][j],
                        A[i - 1] * A[k] * A[j + 1] + dp[i][k - 1] + dp[k + 1][j]
                    )

        return dp[1][n]
```

## 4. Dry Run (`nums = [3, 1, 5]`, so `A = [1, 3, 1, 5, 1]`)

```text
dp(1,3) = 35
├─ k=1 last: 1·3·1 + dp(1,0) + dp(2,3) = 3 + 0 + 30 = 33
│     └─ dp(2,3) = 30   (k=3 last: 3·5·1 + dp(2,2) + dp(4,3) = 15 + 15 + 0)
├─ k=2 last: 1·1·1 + dp(1,1) + dp(3,3) = 1 + 3 + 5 = 9
└─ k=3 last: 1·5·1 + dp(1,2) + dp(4,3) = 5 + 30 + 0 = 35   ← best
      └─ dp(1,2) = 30   (k=1 last: 1·3·5 + dp(1,0) + dp(2,2) = 15 + 0 + 15)
```

The single-balloon ranges are `dp(1,1) = 3`, `dp(2,2) = 15` and `dp(3,3) = 5`. The best order is to burst `1` first, then `3`, then `5` last, for `15 + 15 + 5 = 35`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, j)` with `1 <= i <= j <= n`, so about `n² / 2` entries.
* **Time:** O(n³) — there are about `n²` ranges, and each one tries up to `n` choices of `k` at O(1) each.
* **Space:** O(n²) — the memo holds about `n² / 2` entries, plus recursion depth up to `n`. The table is O(n²) too.

## 6. Recall (30 seconds)

* **Trick:** choose the balloon `k` burst **last** in `[i, j]`; its neighbours are then `A[i - 1]` and `A[j + 1]`, and the two halves are independent.
* **Transition:** `A[i-1]·A[k]·A[j+1] + dp(i, k-1) + dp(k+1, j)`, maximized over `k`; base `i > j → 0`.
* **Table:** pad `A` with `1`s, and fill ranges by increasing length.
