# 16. Triangle

**LC 120** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** 2D DP / Grid Min Cost (top-down)

---

## 1. Intuition

Starting at the top of a triangle, you step to one of the two cells directly below (`(r + 1, c)` or `(r + 1, c + 1)`), and you want the smallest total. Instead of asking "how did I get here?", ask **"what's the cheapest way to finish from here?"** From a cell, pay for it, then go on to whichever of the two cells below has the cheaper finish.

* `dp(r, c)` — the minimum path sum from `(r, c)` down to the bottom row.
* `if r == n - 1: return triangle[r][c]` — on the bottom row there is nowhere left to go, so the cost is the cell itself.
* `down = dp(r + 1, c)` and `diag = dp(r + 1, c + 1)` — the two cells you can step to.
* `triangle[r][c] + min(down, diag)` — pay for this cell, then take the cheaper finish.
* `return dp(0, 0)` — the answer is the cheapest finish from the apex.
* `memo[(r, c)]` — two different cells above share the same cell below, so without the cache the paths blow up exponentially.

**Recall:** `dp(r, c) = triangle[r][c] + min(dp(r + 1, c), dp(r + 1, c + 1))`.

## 2. Template

* **State:** `dp(r, c)` = min path sum from `(r, c)` to the bottom row
* **Choice:** step down to `(r + 1, c)` or diagonally to `(r + 1, c + 1)`
* **Recurrence:** `dp(r, c) = triangle[r][c] + min(dp(r + 1, c), dp(r + 1, c + 1))`
* **Base:** on the last row, `dp(n - 1, c) = triangle[n - 1][c]`
* **Guard:** none — row `r` always has the cells `c` and `c + 1` below it

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def minimumTotal(self, triangle: list[list[int]]) -> int:
        n = len(triangle)
        memo = {}

        def dp(r: int, c: int) -> int:
            # Base Case: Reached the bottom row
            if r == n - 1:
                return triangle[r][c]

            if (r, c) in memo:
                return memo[(r, c)]

            # Move down or diagonally down-right
            down = dp(r + 1, c)
            diag = dp(r + 1, c + 1)

            memo[(r, c)] = triangle[r][c] + min(down, diag)
            return memo[(r, c)]

        return dp(0, 0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `(r, c)`) | `dp` — a single row, starting as a copy of the bottom row |
| `if r == n - 1: return triangle[r][c]` | `dp = triangle[-1][:]` (the bottom row is the base) |
| `dp(r + 1, c)` and `dp(r + 1, c + 1)` | `dp[c]` and `dp[c + 1]` (`dp` holds the row below) |
| `dp(r, c)` asks for the row **below** | `for r in range(len(triangle) - 2, -1, -1)` — start at the bottom and go **up** |
| `triangle[r][c] + min(down, diag)` | `dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])` |
| `return dp(0, 0)` | `return dp[0]` |

**Loop-order rule:** the memo asks for the row below, so the table starts at the bottom row and works upward. Overwriting `dp[c]` in place is safe: with `c` ascending, `dp[c]` is read before it's written and `dp[c + 1]` hasn't been overwritten yet.

```python
class Solution:
    def minimumTotal(self, triangle: list[list[int]]) -> int:
        # Start with a copy of the bottom row
        dp = triangle[-1][:]

        # Iterate from second-to-last row up to the top
        for r in range(len(triangle) - 2, -1, -1):
            for c in range(r + 1):
                dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])

        return dp[0]
```

*Also worth knowing:* if you may modify the input, write the same updates into `triangle` itself for O(1) extra space.

## 4. Dry Run (`triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]`)

The cheapest finish from every cell, which is what the memo computes (read from the bottom row up):

```text
row 0:           11
row 1:         9    10
row 2:       7    6    10
row 3:     4    1    8    3
```

For example `6 → 7` because `6 + min(4, 1)`, and the answer is `2 + min(9, 10) = 11`.

## 5. Complexity

* **States:** `memo` is keyed by `(r, c)`, one entry per triangle cell, `n(n + 1) / 2` in total for `n` rows.
* **Time:** O(n²) — each cell is solved once, and each solve is one `min` of two known values.
* **Space:** O(n²) — the memo plus recursion `n` deep. The one-row table is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(r, c)` = cheapest finish from `(r, c)` down to the bottom.
* **Transition:** `triangle[r][c] + min(dp(r + 1, c), dp(r + 1, c + 1))`; the bottom row returns itself.
* **Table:** start from the bottom row and go up, so no boundary checks are needed.
