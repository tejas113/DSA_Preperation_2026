# 695. Max Area of Island

**LC 695** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Connected components on a grid, where the DFS *returns* each component's size

---

## 1. Intuition

This is Number of Islands, but instead of *counting* islands we *measure* each one. When the scan hits
new land, the DFS sinks the island and reports back how many cells it sank. Keep the biggest number you've seen.

* **The size is returned, not counted outside:** `return 1 + dfs(down) + dfs(up) + dfs(right) + dfs(left)`. Each cell counts itself (the `1`) and adds whatever its neighbours report.
* **Water and visited cells are worth 0:** the base case returns `0` for out-of-bounds cells or `grid[r][c] == 0`, so they add nothing to the sum.
* **Sinking is the visited set:** `grid[r][c] = 0` happens *before* the recursive calls, so a neighbour that looks back at this cell sees `0` and doesn't count it twice.
* **The best answer so far:** `max_area = max(max_area, dfs(i, j))` runs once per island, and only when `grid[i][j] == 1` (the island hasn't been seen yet).

**Recall:** `dfs` returns `1 + the four neighbours`. Sink the cell before recursing, and keep the max over all islands.

## 2. Approach

* **Idea:** Scan every cell. Each unvisited land cell starts a DFS that sinks its island and returns the island's area, and `max_area` keeps the largest one.
* **Graph representation:** implicit **grid** graph, undirected and unweighted. Moves go in **4 directions**: `(r±1, c)`, `(r, c±1)`.
* **Data structure / pointers:**
  * `rows`, `columns`: grid size.
  * `max_area`: the largest island area found so far. It starts at `0`, which is also the answer when there's no land.
  * `grid` itself is the visited marker: `0` means water or already counted. A cell is marked **when `dfs` enters it**, before it recurses.
  * Out-of-bounds is checked first in `dfs` (`not (0 <= r < rows and 0 <= c < columns)`), so the code never reads outside the grid.
* **Invariant:** `dfs(r, c)` returns the number of land cells reachable from `(r, c)` that were still `1` when the call started, and it sinks all of them. Each land cell is counted exactly once, in exactly one island.
* **Edge cases:**
  * All water: `dfs` is never called, so it returns `0`.
  * All land: the first `dfs(0, 0)` sinks everything and returns `rows × columns`.
  * A single cell: `[[1]]` → 1, and `[[0]]` → 0.
  * Diagonal land isn't connected: `[[1,0],[0,1]]` → 1.
  * An empty grid isn't possible (LC guarantees `m, n ≥ 1`). With `[]`, `grid[0]` would raise `IndexError`.
  * Recursion depth: a 50×50 all-land grid (the LC maximum) raises `RecursionError` under Python's default limit of 1,000 when you run it locally. An iterative stack or BFS avoids this.
  * **The input is changed:** the grid ends up all `0`. To keep it, pass a copy, or use a `visited` set (which costs O(rows × columns) extra memory).

## 3. Code

```python
class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        rows = len(grid)
        columns = len(grid[0])
        max_area = 0

        # Helper recursive DFS function to traverse and count island size
        def dfs(r: int, c: int) -> int:
            # Base Case: Out of bounds OR water/visited cell
            if not (0 <= r < rows and 0 <= c < columns) or grid[r][c] == 0:
                return 0

            # Mark cell as visited by "sinking" the land to water
            grid[r][c] = 0

            # Count current cell (1) + sum of 4-directional recursive calls
            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

        # Iterate over every cell in the grid
        for i in range(rows):
            for j in range(columns):
                # Trigger DFS only when unvisited land is found
                if grid[i][j] == 1:
                    max_area = max(max_area, dfs(i, j))

        return max_area
```

## 4. Dry Run

Input: `grid = [[1,1,0],[1,0,0],[0,0,1]]`. Each `dfs` call tries **down, up, right, left**, in that order, and adds up what they return.

| Step | What runs | State update | Returns / decision |
| --- | --- | --- | --- |
| Start | `max_area = 0` | grid unchanged | outer loop starts at `(0, 0)` |
| Loop `(0, 0)` | `grid[0][0] == 1`, so call `dfs(0, 0)` | `grid[0][0] = 0` | starts adding up its 4 neighbours |
| ↳ down | `dfs(1, 0)` | `grid[1][0] = 0` | all its neighbours are `0` or out of bounds, so it returns `1` |
| ↳ up | `dfs(-1, 0)` | — | out of bounds, so it returns `0` |
| ↳ right | `dfs(0, 1)` | `grid[0][1] = 0` | all its neighbours are `0` or out of bounds, so it returns `1` |
| ↳ left | `dfs(0, -1)` | — | out of bounds, so it returns `0` |
| Island 1 done | `dfs(0, 0)` returns `1 + 1 + 0 + 1 + 0 = 3` | `(0,0), (1,0), (0,1)` are now `0` | `max_area = max(0, 3) = 3` |
| Loop `(0, 1)` … `(2, 1)` | every cell is `0` | no change | skipped |
| Loop `(2, 2)` | `grid[2][2] == 1`, so call `dfs(2, 2)` | `grid[2][2] = 0` | no land neighbours, so it returns `1` |
| Island 2 done | — | the grid is all `0` | `max_area = max(3, 1) = 3` |
| Finish | — | — | return **`3`** |

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: every land cell is sunk once, and every cell is looked at only a few times. The double loop checks each cell once. `dfs` can be *called* on a cell up to 4 times (once from each neighbour), but only the first call sinks it and recurses. The other calls see `0` and return `0` at once. A fixed amount of work per cell means the total grows with the grid size.
* **Space: O(rows × columns)** in the worst case
  Think of it as: no extra visited set, because the grid is the marker. The only cost is the recursion stack. If the whole grid is one long winding island, `dfs` goes one call deeper per land cell before any call returns.

## 6. Recall (30 seconds)

* Same skeleton as Number of Islands, but `dfs` **returns the area**: `1 + down + up + right + left`, and water or out-of-bounds cells return `0`.
* Sink `grid[r][c] = 0` *before* recursing, so no cell is counted twice. Update `max_area` once per island.
* O(R·C) time and O(R·C) worst-case recursion depth. For big grids, use an iterative stack or BFS.
