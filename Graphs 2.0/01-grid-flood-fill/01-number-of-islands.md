# 200. Number of Islands

**LC 200** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Connected components on a grid (DFS flood fill, sink in place)

---

## 1. Intuition

Picture the grid as a map, where every `'1'` is land and every `'0'` is water. Walk the map cell by cell.
When you step on land you haven't seen before, you've found a new island. Flood the whole island to water
so you never count it again, then keep walking. The number of floods is the number of islands.

* **Grid = undirected graph:** each `'1'` cell is a node connected to up to 4 neighbours (right, left, down, up), which are the four `dfs(...)` calls. Counting islands means counting **connected components**.
* **Sink in place = visited set:** `grid[r][c] = "0"` marks a cell as visited without a separate `visited` set. Once a cell is sunk, the base case `grid[r][c] == "0"` stops any later visit.
* **One flood per island:** in the double loop, `if grid[i][j] == "1"` is only true for the first cell of a not-yet-seen island. `dfs(i, j)` sinks the whole island, then `count += 1`.
* **No diagonals:** `dfs` only moves in 4 directions, so `[["1","0"],["0","1"]]` is 2 islands.

**Recall:** Scan every cell. On a `'1'`, flood the island to `'0'` and add 1 to `count`.

## 2. Approach

* **Idea:** Scan every cell. Each unvisited land cell starts a DFS that sinks its whole island, and each DFS start counts as one island.
* **Graph representation:** implicit **grid** graph, undirected and unweighted. Moves go in **4 directions**: `(r, c±1)`, `(r±1, c)`.
* **Data structure / pointers:**
  * `rows`, `columns`: grid size.
  * `count`: the number of islands found so far.
  * `grid` itself is the visited marker: `"0"` means water *or* already visited. The DFS marks a cell **when it enters `dfs`**. The BFS alternative marks a cell **when it is pushed**, so a cell is never queued twice.
  * The out-of-bounds check `not (0 <= r < rows and 0 <= c < columns)` runs first in `dfs`, so the code never indexes outside the grid.
* **Invariant:** after `dfs(i, j)` returns, every land cell connected to `(i, j)` is now `"0"`. So every `"1"` still left in the grid belongs to an island that hasn't been counted yet.
* **Edge cases:**
  * Empty grid `[]` or `[[]]`: `if not grid or not grid[0]` returns `0`.
  * A single cell: `[["1"]]` → 1, and `[["0"]]` → 0.
  * All water: the loop never calls `dfs`, so it returns 0.
  * Diagonal-only land: it isn't connected, so `[["1","0"],["0","1"]]` → 2.
  * Very large islands: recursive `dfs` can go one call deep per land cell, up to `rows × columns`. Python's default recursion limit is about 1000, so a big island can raise `RecursionError` when you run it locally. A 300 × 300 all-land grid does exactly that. It works after `sys.setrecursionlimit(200000)` (tested on Python 3.12), and LeetCode's judge usually accepts it. The BFS alternative has no depth limit.
  * **The input is destroyed:** the grid ends up all `"0"`. If the caller needs the grid afterwards, pass in a copy.

## 3. Code

```python
class Solution:

    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows = len(grid)
        columns = len(grid[0])
        count = 0

        def dfs(r: int, c: int) -> None:
            # Base case: Out of bounds or encountered water '0'
            if not (0 <= r < rows and 0 <= c < columns) or grid[r][c] == "0":
                return

            # Mark cell as visited by sinking it to '0'
            grid[r][c] = "0"

            # Traverse all 4 adjacent directions
            dfs(r, c + 1)  # Right
            dfs(r, c - 1)  # Left
            dfs(r + 1, c)  # Down
            dfs(r - 1, c)  # Up

        for i in range(rows):
            for j in range(columns):
                if grid[i][j] == "1":
                    dfs(i, j)
                    count += 1

        return count
```

### Alternative: Iterative BFS (no recursion-depth risk)

Use this if a large island could overflow the recursion limit. It marks cells as visited **when they are pushed** onto the `deque`.

```python
from collections import deque


class SolutionBFS:

    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        count = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    grid[r][c] = "0"  # Mark as visited
                    queue = deque([(r, c)])

                    while queue:
                        curr_r, curr_c = queue.popleft()
                        for dr, dc in [
                            (0, 1),
                            (0, -1),
                            (1, 0),
                            (-1, 0),
                        ]:
                            nr, nc = curr_r + dr, curr_c + dc
                            if (
                                0 <= nr < rows
                                and 0 <= nc < cols
                                and grid[nr][nc] == "1"
                            ):
                                grid[nr][nc] = "0"  # Mark as visited on push
                                queue.append((nr, nc))

        return count
```

## 4. Dry Run

Input (LC Example 2):

```text
    c: 0    1    2    3    4
r0: ["1", "1", "0", "0", "0"]
r1: ["1", "1", "0", "0", "0"]
r2: ["0", "0", "1", "0", "0"]
r3: ["0", "0", "0", "1", "1"]
```

| Loop reaches `(i, j)` | `grid[i][j]` | Action | `count` after | Grid state |
| --- | --- | --- | --- | --- |
| `(0, 0)` | `"1"` | `dfs(0,0)` sinks `(0,0) → (0,1) → (1,1) → (1,0)`, then `count += 1` | `1` | Top-left block is now `"0"` |
| `(0, 1)` … `(2, 1)` | `"0"` | skip (water or already sunk) | `1` | — |
| `(2, 2)` | `"1"` | `dfs(2,2)` sinks `(2,2)` only (no land neighbours), then `count += 1` | `2` | Middle cell is now `"0"` |
| `(2, 3)` … `(3, 2)` | `"0"` | skip | `2` | — |
| `(3, 3)` | `"1"` | `dfs(3,3)` sinks `(3,3) → (3,4)`, then `count += 1` | `3` | Whole grid is `"0"` |
| `(3, 4)` | `"0"` | skip (already sunk) | `3` | — |

Returns **3**.

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: every cell is sunk at most once, and each cell is looked at only a few times. The double loop looks at each cell once. `dfs` can be *called* on a cell up to 4 times (once from each neighbour), but only the first call sinks it and makes 4 more calls. Every later call hits `grid[r][c] == "0"` and returns at once. A fixed amount of work per cell means the total grows with the number of cells.
* **Space: O(rows × columns)** in the worst case
  Think of it as: nothing extra is stored, because the grid itself is the visited marker. The only cost is the recursion stack. If the whole grid is one big snake-shaped island, `dfs` goes one call deeper for each land cell before it returns, which is up to `rows × columns` calls deep. The BFS alternative replaces the stack with a `queue`. It usually holds just a "frontier" of cells, but O(rows × columns) is the safe bound to say in an interview.

## 6. Recall (30 seconds)

* Grid = graph, island = connected component. Scan every cell, and each `'1'` you find starts one flood, so `count += 1`.
* Sinking cells to `"0"` is the visited set, with no extra memory. Check bounds and water before touching a cell, and only move in 4 directions.
* O(R·C) time and O(R·C) worst-case recursion depth. If the grid is big, switch to BFS with a `deque` and mark cells when you push them.
