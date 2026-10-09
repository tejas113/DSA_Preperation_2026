# 15. Minimum Path Sum

**LC 64** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 2D DP / Grid Min Cost

---

## 1. Intuition

Moving only right or down from the top-left to the bottom-right, you want the smallest total of cell values. Look at the last move into `(r, c)`: it came from above or from the left. Whichever of those two has the cheaper path to it is the one you'd rather have come from, and then you pay for the current cell.

* `dp(r, c)` — the minimum path sum from the start to `(r, c)`, including `grid[r][c]`.
* `if r == 0 and c == 0: return grid[0][0]` — the start costs just its own value.
* `if r < 0 or c < 0: return float('inf')` — stepping off the grid isn't a real path; `inf` makes `min` never choose it. This also handles the first row and column automatically, since one of the two neighbours is off-grid there.
* `grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))` — pay for this cell plus the cheaper way in.
* `memo[(r, c)]` — each cell's cheapest cost is computed once.

**Recall:** `dp(r, c) = grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))`.

## 2. Template

* **State:** `dp(r, c)` = minimum path sum from `(0, 0)` to `(r, c)`
* **Choice:** arrive from above or from the left
* **Recurrence:** `dp(r, c) = grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))`
* **Base:** `dp(0, 0) = grid[0][0]`
* **Guard:** off-grid → `inf`, so `min` ignores it

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        memo = {}

        def dp(r: int, c: int) -> int:
            # Base Case 1: Reached start cell
            if r == 0 and c == 0:
                return grid[0][0]

            # Base Case 2: Out of bounds (infinity so min() ignores it)
            if r < 0 or c < 0:
                return float('inf')

            if (r, c) in memo:
                return memo[(r, c)]

            # Transition: current cell value + minimum path to reach from above or left
            memo[(r, c)] = grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))
            return memo[(r, c)]

        return dp(m - 1, n - 1)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `(r, c)`) | `dp = [[0] * n for _ in range(m)]` |
| `r == 0 and c == 0` → `grid[0][0]` | `dp[0][0] = grid[0][0]` |
| off-grid → `inf` (so the first row/column only have one way in) | first row and column are running sums: `dp[0][c] = dp[0][c - 1] + grid[0][c]`, `dp[r][0] = dp[r - 1][0] + grid[r][0]` |
| `grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))` | `dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])` |
| asks for above/left | loop `r` and `c` **ascending** |
| `return dp(m - 1, n - 1)` | `return dp[m - 1][n - 1]` |

**Loop-order rule:** the memo asks for cells above and to the left, so fill the table from the top-left toward the bottom-right.

```python
class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [[0] * n for _ in range(m)]

        dp[0][0] = grid[0][0]

        # Fill first row
        for c in range(1, n):
            dp[0][c] = dp[0][c - 1] + grid[0][c]

        # Fill first column
        for r in range(1, m):
            dp[r][0] = dp[r - 1][0] + grid[r][0]

        # Fill remaining grid
        for r in range(1, m):
            for c in range(1, n):
                dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])

        return dp[m - 1][n - 1]
```

**Shrink to one row:** only the row above and the left neighbour are read, so one array is enough. Seeding `dp[0] = 0` and everything else `inf` lets the first row and first column fall out of the same formula.

```python
class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [float('inf')] * n
        dp[0] = 0  # Base seed

        for r in range(m):
            for c in range(n):
                if c == 0:
                    dp[c] += grid[r][c]  # Only comes from above
                else:
                    dp[c] = grid[r][c] + min(dp[c], dp[c - 1])

        return dp[-1]
```

*Also worth knowing:* if you may modify the input, write the running sums back into `grid` itself for O(1) extra space.

## 4. Dry Run (`grid = [[1,3,1],[1,5,1],[4,2,1]]`)

Minimum cost to reach each cell, which is what the memo computes:

```text
1  4  5
2  7  6
6  8  7
```

The answer is `7` (path `1 → 3 → 1 → 1 → 1`).

## 5. Complexity

* **States:** `memo` is keyed by `(r, c)`, so at most `m × n` cells.
* **Time:** O(m × n) — each cell is solved once, and each solve is one `min` of two known values.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep. The full table is O(m × n); the one-row version is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(r, c)` = cheapest path sum to `(r, c)`, including its own value.
* **Transition:** `grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))`; the start is `grid[0][0]`.
* **Trick:** return `inf` off-grid so `min` never picks an impossible move.
