# 13. Unique Paths

**LC 62** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 2D DP / Grid Paths

---

## 1. Intuition

A robot starts at the top-left and can only move **right or down**. Look at the last move into cell `(r, c)`: it came either from the cell above or from the cell to the left. So the paths to `(r, c)` are the paths to those two cells, added together. Any cell on the top row or left column has just one path (a straight line).

* `dp(r, c)` — the number of paths from the start `(0, 0)` to cell `(r, c)`.
* `dp(r - 1, c) + dp(r, c - 1)` — you entered `(r, c)` from above or from the left; add both counts.
* `if r == 0 or c == 0: return 1` — along the top row or the left column there is only one way in.
* `return dp(m - 1, n - 1)` — we ask about the bottom-right corner and recurse back toward the start.
* `memo[(r, c)]` — many routes pass through the same cell; without the cache the paths are recounted exponentially.

**Recall:** `dp(r, c) = dp(r - 1, c) + dp(r, c - 1)`, and the top row and left column are 1.

## 2. Template

* **State:** `dp(r, c)` = number of paths from `(0, 0)` to `(r, c)`
* **Choice:** the last move came from above or from the left
* **Recurrence:** `dp(r, c) = dp(r - 1, c) + dp(r, c - 1)`
* **Base:** `dp(0, c) = dp(r, 0) = 1`
* **Guard:** none needed — the base case catches the edges before an index can go negative

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        memo = {}

        def dp(r: int, c: int) -> int:
            # Base Case: top row or left column has exactly 1 path
            if r == 0 or c == 0:
                return 1

            if (r, c) in memo:
                return memo[(r, c)]

            memo[(r, c)] = dp(r - 1, c) + dp(r, c - 1)
            return memo[(r, c)]

        return dp(m - 1, n - 1)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `(r, c)`) | `dp = [[0] * n for _ in range(m)]` |
| `if r == 0 or c == 0: return 1` | first row and first column set to `1` |
| `dp(r - 1, c) + dp(r, c - 1)` | `dp[r][c] = dp[r - 1][c] + dp[r][c - 1]` |
| `dp(r, c)` asks for the cell above and the cell to the left | loop `r` and `c` **ascending** from 1, so above and left are already filled |
| `return dp(m - 1, n - 1)` | `return dp[m - 1][n - 1]` |

**Loop-order rule:** the memo asks for cells above and to the left, so fill the table from the top-left toward the bottom-right.

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0] * n for _ in range(m)]

        for r in range(m):
            dp[r][0] = 1
        for c in range(n):
            dp[0][c] = 1

        for r in range(1, m):
            for c in range(1, n):
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

        return dp[m - 1][n - 1]
```

**Shrink to one row:** `dp[r][c]` only reads the row above and the cell to its left, so keep just one row and rebuild it row by row.

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row = [1] * n

        for r in range(1, m):
            new_row = [1] * n
            for c in range(1, n):
                # new_row[c - 1] is paths from left
                # row[c] is paths from above
                new_row[c] = new_row[c - 1] + row[c]
            row = new_row

        return row[-1]
```

*Also worth knowing:* the robot makes `m - 1` down-moves and `n - 1` right-moves in some order, so the answer is `math.comb(m + n - 2, m - 1)` in O(min(m, n)) time.

## 4. Dry Run (`m = 3`, `n = 3`)

Path counts for every cell, which is exactly what the memo computes:

```text
1  1  1
1  2  3
1  3  6
```

`dp(2, 2) = dp(1, 2) + dp(2, 1) = 3 + 3 = 6`.

## 5. Complexity

* **States:** `memo` is keyed by `(r, c)`, so at most `m × n` cells.
* **Time:** O(m × n) — each cell is solved once, and each solve is one addition.
* **Space:** O(m × n) — the memo holds about `m × n` entries, and the recursion goes up to `m + n` deep. The full table is O(m × n) too; the one-row version is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(r, c)` = paths from the start to `(r, c)`.
* **Transition:** `dp(r - 1, c) + dp(r, c - 1)`; top row and left column are `1`.
* **Shortcuts:** keep one row for O(n) space, or use `math.comb(m + n - 2, m - 1)`.
