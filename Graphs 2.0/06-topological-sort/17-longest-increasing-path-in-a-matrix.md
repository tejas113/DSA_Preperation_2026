# 329. Longest Increasing Path in a Matrix

**LC 329** · **Source:** [+] Claude · **Difficulty:** Hard · **Priority:** Core · **Pattern:** DFS + memoization on an implicit DAG (longest path, solving each cell once)

---

## 1. Intuition

From any cell, you may step to a neighbour only if it's **strictly bigger**. The longest climb starting at a
cell is 1 (the cell itself) plus the longest climb from its best bigger neighbour. That answer never changes,
no matter how you reached the cell, so you can work it out **once**, remember it, and reuse it.

* **`dfs(r, c)` = the longest increasing path that *starts* at `(r, c)`.** It starts at `max_len = 1` (just the cell) and takes `max(max_len, 1 + dfs(nr, nc))` over each bigger neighbour.
* **`memo` makes it fast:** `if (r, c) in memo: return memo[(r, c)]`. Each cell's answer is computed only once, and every later call is a dict lookup.
* **No visited set needed:** you can only step to a bigger value (`matrix[nr][nc] > val`), so a path can never come back to a cell it already used. That means there are no cycles, and the graph is a DAG (a directed graph with no cycles).
* **Try every start:** the double loop calls `dfs(i, j)` for every cell, and `max_path` keeps the best. Thanks to `memo`, that doesn't redo any work.

**Recall:** `dfs(cell)` = 1 + the best `dfs` among its strictly larger neighbours, stored in `memo`. The answer is the max over all cells.

## 2. Approach

* **Idea:** Treat each cell as a node with an edge to each strictly larger neighbour. Those edges always go uphill, so there can't be a cycle, and the graph is a DAG. The longest path in a DAG can be found with DFS + memo, solving each node once.
* **Graph representation:** implicit **grid** graph, **directed** (only from smaller to strictly larger) and unweighted. Moves go in **4 directions**, from `[(-1, 0), (1, 0), (0, -1), (0, 1)]` (up, down, left, right).
* **Data structure / pointers:**
  * `memo[(r, c)]`: the length of the longest increasing path **starting** at `(r, c)`. A cell is stored **after** all its bigger neighbours are finished, which is when `dfs` returns.
  * `val`: the current cell's value. A neighbour is used only if it's `> val`.
  * `max_len`: the best path length from this cell found so far. It starts at `1`.
  * `max_path`: the best over all starting cells.
  * Out-of-bounds is checked with `0 <= nr < m and 0 <= nc < n` before `matrix[nr][nc]` is read.
* **Invariant:** whenever `memo[(r, c)]` exists, it's the final, correct answer for that cell. It depends only on strictly larger cells, and their answers were already final when it was computed.
* **Edge cases:**
  * Empty matrix `[]` or `[[]]`: `if not matrix or not matrix[0]` returns `0`.
  * A single cell: `1`.
  * All values equal: no strictly larger neighbour anywhere, so the answer is `1`.
  * Equal neighbours are **not** allowed (it uses strict `>`). That's what rules out cycles. With `>=`, two equal cells would keep calling each other forever.
  * Diagonal steps aren't allowed (4 directions only).
  * **Recursion depth:** `dfs` goes as deep as the path it's following. On a 200 × 200 matrix (the LC maximum), a winding increasing path of about 20,000 cells, where each cell's only bigger neighbour is the next cell on the path, makes `dfs` go about 20,000 calls deep. That's far past Python's default limit of 1,000, so it raises `RecursionError` when you run it locally. (Many large grids are fine, because `memo` fills up early and keeps the stack shallow. It's this worst case that breaks.) Raising `sys.setrecursionlimit`, or the iterative version (Kahn's algorithm: peel cells with no smaller neighbour, level by level, and count the levels), avoids this.

## 3. Code

```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        memo = {}

        def dfs(r, c):
            if (r, c) in memo:
                return memo[(r, c)]

            val = matrix[r][c]
            max_len = 1

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > val:
                    max_len = max(max_len, 1 + dfs(nr, nc))

            memo[(r, c)] = max_len
            return memo[(r, c)]

        max_path = 0

        # Traverse every cell to calculate DFS
        for i in range(m):
            for j in range(n):
                max_path = max(max_path, dfs(i, j))

        return max_path
```

## 4. Dry Run

Input (LC Example 1):

```text
        c0  c1  c2
r0:      9   9   4
r1:      6   6   8
r2:      2   1   1
```

The outer loop goes cell by cell. Each row below is a `memo` entry in the order it gets written. A cell's value is filled in only after all its bigger neighbours are done.

| Order | Cell (value) | Bigger neighbours → their `memo` | `memo` value |
| --- | --- | --- | --- |
| 1 | `(0,0)` 9 | none | **1** |
| 2 | `(0,1)` 9 | none | **1** |
| 3 | `(1,2)` 8 | none (4, 1, 6 are all smaller). Reached while computing `(0,2)` | **1** |
| 4 | `(0,2)` 4 | down `(1,2)`=8 → 1, left `(0,1)`=9 → 1 | 1 + 1 = **2** |
| 5 | `(1,0)` 6 | up `(0,0)`=9 → 1 | **2** |
| 6 | `(1,1)` 6 | up `(0,1)`=9 → 1, right `(1,2)`=8 → 1 | **2** |
| — | `(1,2)` | already in `memo` (lookup only) | 1 |
| 7 | `(2,0)` 2 | up `(1,0)`=6 → 2 | **3** |
| 8 | `(2,1)` 1 | up `(1,1)`=6 → 2, left `(2,0)`=2 → 3 | 1 + 3 = **4** |
| 9 | `(2,2)` 1 | up `(1,2)`=8 → 1 | **2** |

`max_path` reaches **4** at `(2,1)`. That's the path `1 → 2 → 6 → 9`, which is `(2,1) → (2,0) → (1,0) → (0,0)`.

## 5. Complexity

* **Time: O(m × n)**
  Think of it as: each cell is solved once, and then it's just looked up. The first `dfs(r, c)` call checks 4 neighbours and stores the answer. Every later call on that cell, from the outer loop or from a smaller neighbour, returns straight from `memo`. Each cell is asked for at most 5 times (once by the loop and once by each neighbour), so the total work grows with the number of cells.
* **Space: O(m × n)**
  Think of it as: `memo` holds one number per cell. The recursion stack can also go as deep as the longest increasing path, which in the worst case (one long snake) is every cell.

## 6. Recall (30 seconds)

* Strictly increasing moves mean **no cycles** (it's a DAG), so there's no visited set. Plain DFS + memo works.
* `dfs(r, c)` = `1 + max(dfs(bigger neighbour))`, or `1` if there's none. Store it in `memo` before returning.
* Loop over all cells and take the max. O(m·n) time and space. On huge snakes, mind the recursion limit, or use Kahn's peeling as the iterative alternative.
