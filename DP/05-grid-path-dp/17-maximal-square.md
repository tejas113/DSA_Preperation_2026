# 17. Maximal Square

**LC 221** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 2D DP / Largest Square

---

## 1. Intuition

For every cell, ask: what is the side of the biggest all-`1` square whose **bottom-right corner** is this cell? Such a square can only be as large as its three neighbours allow: the square ending just above, the one ending just to the left, and the one ending diagonally up-left. Take the smallest of those three and add one for the current cell. Every cell can be a bottom-right corner, so the answer is the best value over **all** cells.

* `dp(r, c)` — the side length of the largest all-`1` square ending at `(r, c)`.
* `if r < 0 or c < 0 or matrix[r][c] == '0': return 0` — off the grid, or a `0` cell, can't be part of any square.
* `up`, `left`, `diag` — the squares ending at the three neighbours.
* `1 + min(up, left, diag)` — the square is limited by the smallest neighbour; `+ 1` is the current cell.
* the outer double loop with `max_side` — the biggest square can end at any cell, so ask `dp` for every cell (unlike Unique Paths, whose answer is one corner).
* `return max_side * max_side` — the problem wants the **area**, not the side.
* `memo[(r, c)]` — each cell is computed once, even though neighbours ask for it repeatedly.

**Recall:** `dp(r, c) = 1 + min(up, left, diag)` for a `'1'` cell, `0` for a `'0'`.

## 2. Template

* **State:** `dp(r, c)` = side of the largest all-`1` square with bottom-right corner `(r, c)`
* **Choice:** none — it is decided by the three neighbouring squares
* **Recurrence:** `dp(r, c) = 1 + min(dp(r - 1, c), dp(r, c - 1), dp(r - 1, c - 1))`
* **Base:** a `'0'` cell or off-grid gives `0`
* **Guard:** track `max_side` over every cell, and return `max_side * max_side`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        memo = {}
        max_side = 0

        def dp(r: int, c: int) -> int:
            # Base Case: Out of bounds or cell is '0'
            if r < 0 or c < 0 or matrix[r][c] == '0':
                return 0

            if (r, c) in memo:
                return memo[(r, c)]

            up = dp(r - 1, c)
            left = dp(r, c - 1)
            diag = dp(r - 1, c - 1)

            memo[(r, c)] = 1 + min(up, left, diag)
            return memo[(r, c)]

        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                max_side = max(max_side, dp(r, c))

        return max_side * max_side
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `(r, c)`) | `dp` with one extra padding row and column of zeros: `(m + 1) × (n + 1)` |
| `if r < 0 or c < 0: return 0` | the padding row/column (index 0) stays `0`, so no bounds checks |
| `matrix[r][c] == '0'` → `0` | only `'1'` cells are computed; `'0'` cells stay `0` |
| `1 + min(up, left, diag)` | `dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])` |
| the outer double loop with `max_side` | update `max_side` while filling |
| asks for up/left/diag | loop `r` and `c` **ascending** |

The padding shifts every index by one: matrix cell `(r - 1, c - 1)` is table cell `(r, c)`.

```python
class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        if not matrix:
            return 0

        m, n = len(matrix), len(matrix[0])
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_side = 0

        for r in range(1, m + 1):
            for c in range(1, n + 1):
                if matrix[r - 1][c - 1] == '1':
                    dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                    max_side = max(max_side, dp[r][c])

        return max_side * max_side
```

**Shrink to one row:** each cell reads the row above, the cell to its left, and the cell diagonally up-left. Keep one row, and save the old `dp[c]` in `temp` so it can become the **next** cell's diagonal.

```python
class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        if not matrix:
            return 0

        m, n = len(matrix), len(matrix[0])
        dp = [0] * (n + 1)
        max_side = 0

        for r in range(1, m + 1):
            prev_diag = 0                      # dp[r - 1][0]: the padding column is always 0
            for c in range(1, n + 1):
                temp = dp[c]                   # dp[r - 1][c], the next cell's diagonal
                if matrix[r - 1][c - 1] == '1':
                    dp[c] = 1 + min(dp[c], dp[c - 1], prev_diag)
                    max_side = max(max_side, dp[c])
                else:
                    dp[c] = 0
                prev_diag = temp

        return max_side * max_side
```

## 4. Dry Run

```text
matrix                 dp (largest square ending at each cell)
1 0 1 0 0              1 0 1 0 0
1 0 1 1 1              1 0 1 1 1
1 1 1 1 1              1 1 1 2 2
1 0 0 1 0              1 0 0 1 0
```

The largest side is `2` (at row 2, columns 3–4), so the area is `2 × 2 = 4`. The cell `(2, 3)` is `1 + min(up=1, left=1, diag=1) = 2`.

## 5. Complexity

* **States:** `memo` is keyed by `(r, c)`, so at most `m × n` cells.
* **Time:** O(m × n) — each cell is solved once (the outer loops just look them up), and each solve is one `min` of three known values.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep. The full table is O(m × n); the one-row version is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(r, c)` = side of the largest all-`1` square ending at `(r, c)`.
* **Transition:** `1 + min(up, left, diag)` for a `'1'`, else `0`.
* **Pitfalls:** ask `dp` for **every** cell and take the max, and return the **area** (`side * side`).
