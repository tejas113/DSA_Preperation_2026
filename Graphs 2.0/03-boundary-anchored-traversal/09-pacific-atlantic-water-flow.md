# 417. Pacific Atlantic Water Flow

**LC 417** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Reverse search from the boundaries (DFS "uphill" from each ocean, then intersect)

---

## 1. Intuition

Asking every cell "can my water reach the ocean?" means one search per cell, which is O((M × N)²). Flip it
around: start *at the oceans* and walk **uphill**. Any cell the Pacific can climb up to is a cell whose water
can flow down to the Pacific. Do the same for the Atlantic, and the answer is the cells both oceans reach.

* **Reverse the flow rule:** water flows A → B when `heights[A] >= heights[B]`. Walking backwards, you may step to a neighbour only if it is **at least as high**. The base case `heights[r][c] < prevHeight` blocks the step down.
* **Starting points are the ocean borders:** the top row and left column start `pacific`, and the bottom row and right column start `atlantic`. Each border cell is passed its own height as `prevHeight`, so it always gets in.
* **Each set is its own visited marker:** `visited` is either `pacific` or `atlantic`. `(r, c) in visited` stops repeat visits, so each cell is explored at most once per ocean.
* **Intersect at the end:** step 3 keeps `[i, j]` only if it's in `pacific` **and** in `atlantic`.

**Recall:** DFS uphill (`>=`) from the Pacific borders and from the Atlantic borders into two sets, then return their intersection.

## 2. Approach

* **Idea:** Run two reverse searches, one from each ocean's border, through cells that rise or stay level. A cell can drain to an ocean exactly when that ocean's reverse search reaches it.
* **Graph representation:** implicit **grid** graph, **directed** by height. In the reverse search, an edge `(r, c) → neighbour` exists only if `heights[neighbour] >= heights[r][c]`. Unweighted. Moves go in **4 directions**: down, up, right, left (the order of the `dfs` calls).
* **Data structure / pointers:**
  * `pacific`, `atlantic`: sets of `(r, c)` cells that each ocean's water can reach going uphill. Each is the visited set for its own DFS. A cell is marked **when `dfs` enters it** (`visited.add((r, c))`).
  * `prevHeight`: the height of the cell we came from. A step is allowed only if `heights[r][c] >= prevHeight`.
  * `common`: the answer list of `[i, j]` pairs that are in both sets, in row-major order.
  * Out-of-bounds is checked first (`r < 0 or r >= rows or c < 0 or c >= columns`), before `heights[r][c]` is read.
* **Invariant:** every cell in `pacific` has a path down (each step `>=` the next) to a top-row or left-column cell, so its water reaches the Pacific. The same holds for `atlantic` with the bottom row and right column.
* **Edge cases:**
  * A 1×1 grid: that cell touches both oceans, so it returns `[[0, 0]]`.
  * A flat grid (all heights equal): `>=` lets every step through, so every cell is returned.
  * A single row or single column: every cell touches both oceans, so every cell is returned.
  * Plateaus (equal neighbours): allowed because of `>=` (water flows across level ground). The visited sets stop them from looping forever.
  * A corner cell (top-right or bottom-left) touches both oceans, so it's always in the answer.
  * An empty grid isn't possible (LC guarantees `m, n ≥ 1`). With `[]`, `heights[0]` would raise `IndexError`.
  * **Recursion depth:** `dfs` can go one call deep per cell. On grids up to the LC maximum of 200 × 200, a long winding uphill path or a large flat area can go deeper than Python's default limit of 1,000, which raises `RecursionError` when you run it locally. An iterative stack or a BFS with `collections.deque` avoids this.

## 3. Code

```python
class Solution:

    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        rows = len(heights)
        columns = len(heights[0])

        # Sets to store cells reachable from each ocean
        pacific = set()
        atlantic = set()

        # Helper DFS function to flow "uphill" from ocean borders
        def dfs(r: int, c: int, visited: set, prevHeight: int):
            # Base cases: out of bounds, already visited, or cannot flow uphill
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= columns
                or (r, c) in visited
                or heights[r][c] < prevHeight
            ):
                return

            visited.add((r, c))

            # Explore 4-directional neighbors passing current cell's height
            dfs(r + 1, c, visited, heights[r][c])
            dfs(r - 1, c, visited, heights[r][c])
            dfs(r, c + 1, visited, heights[r][c])
            dfs(r, c - 1, visited, heights[r][c])

        # Step 1: DFS from Top (Pacific) and Bottom (Atlantic) rows
        for c in range(columns):
            dfs(0, c, pacific, heights[0][c])
            dfs(rows - 1, c, atlantic, heights[rows - 1][c])

        # Step 2: DFS from Left (Pacific) and Right (Atlantic) columns
        for r in range(rows):
            dfs(r, 0, pacific, heights[r][0])
            dfs(r, columns - 1, atlantic, heights[r][columns - 1])

        # Step 3: Find intersection of cells reachable by both oceans
        common = []
        for i in range(rows):
            for j in range(columns):
                if (i, j) in pacific and (i, j) in atlantic:
                    common.append([i, j])

        return common
```

## 4. Dry Run

Input:

```text
        c0  c1  c2
r0:      1   2   2      Pacific is above and to the left
r1:      3   2   3      Atlantic is below and to the right
r2:      2   4   1
```

Each row of the table is one top-level `dfs` call that adds new cells, in the order the code runs them. A step is allowed only if the neighbour's height is **≥** the current one.

| Call | Set | New cells added (in visit order) | Why it stops |
| --- | --- | --- | --- |
| `dfs(0,0)` (top row, c=0) | `pacific` | `(0,0)` 1 → `(1,0)` 3 → `(0,1)` 2 → `(1,1)` 2 → `(2,1)` 4 → `(1,2)` 3 → `(0,2)` 2 | `(2,0)` 2 < 3 and `(2,2)` 1 < 3, so both are blocked going up |
| `dfs(2,0)` (bottom row, c=0) | `atlantic` | `(2,0)` 2 → `(1,0)` 3 → `(2,1)` 4 | `(0,0)` 1, `(1,1)` 2 and `(2,2)` 1 are all lower |
| `dfs(2,2)` (bottom row, c=2) | `atlantic` | `(2,2)` 1 → `(1,2)` 3 | `(0,2)` 2 < 3 and `(1,1)` 2 < 3 |
| `dfs(0,2)` (right column, r=0) | `atlantic` | `(0,2)` 2 → `(0,1)` 2 → `(1,1)` 2 | `(0,0)` 1 is lower, and everything else is already in the set |
| `dfs(2,0)` (left column, r=2) | `pacific` | `(2,0)` 2 | it's a border cell, so it always gets in |
| every other border call | — | nothing new (the cell is already in its set) | — |

Result:

* `pacific` = every cell **except `(2,2)`**: height 1, and it's surrounded by higher cells, so the Pacific can't climb down to it.
* `atlantic` = every cell **except `(0,0)`**: height 1, with neighbours 3 and 2, so the Atlantic can't climb down to it.
* Intersection, in row-major order: **`[[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1]]`**.

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: each cell is added to `pacific` at most once and to `atlantic` at most once, so there are two passes over the grid at most. `dfs` can be *called* on a cell several times (from each of its 4 neighbours, plus maybe as a border start), but after the first call it hits `(r, c) in visited` and returns at once. The final double loop is one more pass. A few passes over every cell still grows with rows × columns.
* **Space: O(rows × columns)**
  Think of it as: the two sets can each hold every cell. On top of that, the recursion stack can go as deep as a long winding uphill path, which can be most of the grid in the worst case.

## 6. Recall (30 seconds)

* Don't search from every cell. **Search backwards from the oceans, uphill** (`heights[next] >= heights[cur]`). The top row and left column start Pacific, and the bottom row and right column start Atlantic.
* There are two visited sets (`pacific`, `atlantic`), and the answer is their intersection. A cell is marked when `dfs` enters it.
* O(R·C) time and space. Recursive DFS can hit Python's recursion limit on big grids, so use an iterative stack or BFS if that matters.
