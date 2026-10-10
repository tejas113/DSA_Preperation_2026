# 18. Longest Increasing Path in a Matrix

**LC 329** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Memoized DFS on a Grid

---

## 1. Intuition

From a cell you may step up, down, left or right, but only onto a **strictly larger** value. The longest path starting at a cell is 1 (the cell itself) plus the longest path from its best larger neighbour. There is no simple top-left-to-bottom-right order here, since the order depends on the values, so let a DFS discover it and **cache** every cell's answer.

* `dfs(r, c)` — the length of the longest strictly increasing path that **starts** at `(r, c)`.
* `val = matrix[r][c]` — store the current cell's value for the direction checks.
* `up`, `down`, `left`, `right` — explore the four directions only if the neighbour exists and is strictly larger than `val`.
* inline `if` checks — `dfs(nr, nc) if bounds_ok and matrix[nr][nc] > val else 0` — step only onto strictly larger neighbours. Because values only go up, a path can never return to a cell, so **no `visited` set is needed**.
* `1 + max(up, down, left, right)` — take the best larger neighbour and add one for the current cell.
* `nonlocal max_path` and update in the dfs — track the longest path found so far globally.
* `if (r, c) in memo: return memo[(r, c)]` — a cell reached from many directions is solved once. This is what makes the whole thing O(m × n) instead of exponential.
* the outer double loop — a path can start anywhere, so try every cell.

**Recall:** `dfs(r, c) = 1 + max(dfs(larger neighbour))`, or `1` if none is larger.

## 2. Template

* **State:** `dfs(r, c)` = longest strictly increasing path starting at `(r, c)`
* **Choice:** which strictly larger neighbour to step onto (up, down, left, right)
* **Recurrence:** `dfs(r, c) = 1 + max(up, down, left, right)`, where each direction is `dfs(nr, nc)` if valid and larger, else `0`
* **Base:** no larger neighbour → `0` for each direction, so `1 + max(0, 0, 0, 0) = 1`
* **Guard:** strictly increasing means no cycles, so no `visited` set; use `nonlocal max_path` to track the overall max

## 3. Code

**Top-down DFS with memoization** (primary solution).

```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        memo = {}
        max_path = 0

        def dfs(r, c):
            nonlocal max_path

            if (r, c) in memo:
                return memo[(r, c)]

            val = matrix[r][c]

            up = dfs(r - 1, c) if r - 1 >= 0 and matrix[r - 1][c] > val else 0
            down = dfs(r + 1, c) if r + 1 < m and matrix[r + 1][c] > val else 0
            left = dfs(r, c - 1) if c - 1 >= 0 and matrix[r][c - 1] > val else 0
            right = dfs(r, c + 1) if c + 1 < n and matrix[r][c + 1] > val else 0

            memo[(r, c)] = 1 + max(up, down, left, right)
            max_path = max(max_path, memo[(r, c)])

            return memo[(r, c)]

        for i in range(m):
            for j in range(n):
                dfs(i, j)

        return max_path
```

### Alternative: Tabulation

Here the recursion order isn't a plain sweep, because the order comes from the **values**. The table makes that order explicit by **sorting the cells from largest value to smallest**, so every larger neighbour is already final when you reach a cell.

| Memoization | Tabulation |
|---|---|
| `memo = {}` keyed by cell | `dp[r][c]` grid |
| `res = 1` | every cell starts at `1` |
| the loop over larger neighbours, `1 + dfs(nr, nc)` | the same loop: `dp[r][c] = max(dp[r][c], 1 + dp[nr][nc])` |
| the DFS reaches larger neighbours first, implicitly | process cells in **descending value order** so larger neighbours are done first |
| the outer double loop with `maxi` | `max` over the whole table |

**Loop-order rule:** a cell depends on strictly larger neighbours, so handle larger values first. Equal values never depend on each other (the comparison is strict), so ties can go in any order.

```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        dp = [[1] * cols for _ in range(rows)]        # every cell alone is a path of length 1

        cells = sorted(((matrix[r][c], r, c) for r in range(rows) for c in range(cols)), reverse=True)
        for _, r, c in cells:                          # largest value first
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    dp[r][c] = max(dp[r][c], 1 + dp[nr][nc])

        return max(max(row) for row in dp)
```

The sort costs O(m·n log(m·n)).

*Also worth knowing:* Kahn's topological sort does the same in O(m·n) without recursion. Repeatedly peel off the cells that have no smaller neighbour; the number of layers peeled is the answer.

## 4. Dry Run (`matrix = [[9,9,4],[6,6,8],[2,1,1]]`)

The longest path starting at each cell, which is what the memo computes:

```text
matrix         dfs
9 9 4          1 1 2
6 6 8          2 2 1
2 1 1          3 4 2
```

The maximum is `4`: the path `1 → 2 → 6 → 9`, starting at the `1` in the bottom row.

## 5. Complexity

* **States:** `memo` is keyed by the cell `(r, c)`, so at most `m × n` entries.
* **Time:** O(m × n) — each cell's `dfs` body runs once (later calls hit the cache), and the body checks a constant 4 neighbours.
* **Space:** O(m × n) — the memo plus the recursion stack, which can be as deep as the longest path (up to `m × n` for a snake-shaped grid). Python's default recursion limit is 1000, so raise it or use the sorted table for big grids.

## 6. Recall (30 seconds)

* **State:** `dfs(r, c)` = longest strictly increasing path starting at `(r, c)`.
* **Transition:** `1 + max(dfs(larger neighbour))`, or `1` if none; cache every cell.
* **Why no `visited`:** strictly increasing values can never form a cycle.
