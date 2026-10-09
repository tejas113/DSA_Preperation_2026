# 14. Unique Paths II

**LC 63** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** 2D DP / Grid Paths with Obstacles

---

## 1. Intuition

Same robot, same right/down moves as Unique Paths, but some cells are blocked (`1`). A blocked cell has **zero** paths through it, and that zero simply flows into everything that depends on it. The paths to `(r, c)` are the paths to the cell above plus the paths to the cell on the left, unless `(r, c)` itself is blocked.

* `if r < 0 or c < 0 or obstacleGrid[r][c] == 1: return 0` — stepping off the grid, or onto an obstacle, contributes no paths.
* `if r == 0 and c == 0: return 1` — reached the start: one path. This check comes **after** the obstacle check, so a blocked start correctly returns `0`.
* `dp(r - 1, c) + dp(r, c - 1)` — enter from above or from the left.
* no "edge is 1" shortcut — unlike Unique Paths, an obstacle in the first row or column makes every cell after it unreachable, so those edges are computed, not assumed.
* `memo[(r, c)]` — each cell is solved once.

**Recall:** `dp(r, c) = 0` if blocked, else `dp(r - 1, c) + dp(r, c - 1)`.

## 2. Template

* **State:** `dp(r, c)` = number of paths from `(0, 0)` to `(r, c)`
* **Choice:** the last move came from above or from the left
* **Recurrence:** `dp(r, c) = dp(r - 1, c) + dp(r, c - 1)`
* **Base:** `dp(0, 0) = 1`
* **Guard:** off-grid or obstacle → `0` (checked first, so a blocked start gives `0`)

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        memo = {}

        def dp(r: int, c: int) -> int:
            # Base Case 1: Out of bounds or hit an obstacle
            if r < 0 or c < 0 or obstacleGrid[r][c] == 1:
                return 0

            # Base Case 2: Reached starting cell (0, 0)
            if r == 0 and c == 0:
                return 1

            if (r, c) in memo:
                return memo[(r, c)]

            # State transition: sum of paths from above and left
            memo[(r, c)] = dp(r - 1, c) + dp(r, c - 1)
            return memo[(r, c)]

        return dp(m - 1, n - 1)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `(r, c)`) | `dp = [[0] * n for _ in range(m)]` |
| `r == 0 and c == 0` → `1` | `dp[0][0] = 1` |
| obstacle → `0` | obstacle cells simply stay `0` |
| off-grid → `0` (the first row/column have no cell above/left) | first column: `dp[r][0] = dp[r - 1][0]` if free; first row: `dp[0][c] = dp[0][c - 1]` if free |
| `dp(r - 1, c) + dp(r, c - 1)` | `dp[r][c] = dp[r - 1][c] + dp[r][c - 1]` for free cells |
| asks for above/left | loop `r` and `c` **ascending** |

**Loop-order rule:** the memo asks for cells above and to the left, so fill the table from the top-left. The first row and column are filled separately because they have no cell above (or to the left).

```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        if obstacleGrid[0][0] == 1 or obstacleGrid[-1][-1] == 1:
            return 0

        m, n = len(obstacleGrid), len(obstacleGrid[0])
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = 1

        # Fill first column
        for r in range(1, m):
            if obstacleGrid[r][0] == 0:
                dp[r][0] = dp[r - 1][0]

        # Fill first row
        for c in range(1, n):
            if obstacleGrid[0][c] == 0:
                dp[0][c] = dp[0][c - 1]

        # Fill remainder of table
        for r in range(1, m):
            for c in range(1, n):
                if obstacleGrid[r][c] == 1:
                    dp[r][c] = 0
                else:
                    dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

        return dp[m - 1][n - 1]
```

**Shrink to one row:** the table only reads the row above and the cell to the left, so one array is enough. `dp[c]` holds "paths from above" until it is updated, and `dp[c - 1]` is "paths from the left".

```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        dp = [0] * n
        
        # Base case for start cell
        dp[0] = 1 if obstacleGrid[0][0] == 0 else 0

        for r in range(m):
            for c in range(n):
                if obstacleGrid[r][c] == 1:
                    dp[c] = 0
                elif c > 0:
                    dp[c] += dp[c - 1]

        return dp[-1]
```

## 4. Dry Run (`obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]`)

Path counts for every cell, which is what the memo computes:

```text
1  1  1
1  0  1
1  1  2
```

The obstacle in the middle has `0` paths, so the bottom-right gets `1 + 1 = 2`.

## 5. Complexity

* **States:** `memo` is keyed by `(r, c)`, so at most `m × n` cells.
* **Time:** O(m × n) — each cell is solved once, and each solve is one addition.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep. The full table is O(m × n); the one-row version is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(r, c)` = paths from `(0, 0)` to `(r, c)`, where a blocked cell has `0`.
* **Transition:** `dp(r - 1, c) + dp(r, c - 1)`; check the obstacle **before** the start-cell base case.
* **Pitfall:** don't set the first row and column to `1`; an obstacle blocks everything after it.
