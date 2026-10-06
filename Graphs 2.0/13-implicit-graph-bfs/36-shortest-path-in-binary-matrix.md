# 1091. Shortest Path in Binary Matrix

**LC 1091** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Single-source BFS shortest path on a grid (8 directions)

---

## 1. Intuition

Walk from the top-left corner to the bottom-right corner, only stepping on `0`s. You may move in **8
directions**, diagonals included. Every step costs the same, so the shortest path is whatever BFS reaches
first. BFS spreads out like a ripple, one step-ring at a time, so the first time it touches the target,
no shorter route can exist.

* **Check both ends first:** `if grid[0][0] != 0 or grid[n-1][n-1] != 0: return -1`. If you can't stand on the start or the end, there's no path.
* **The path length counts cells, not moves:** the queue starts at `(0, 0, 1)`, so a 1×1 grid `[[0]]` gives `1`.
* **8 neighbours, not 4:** `directions` lists all 8 offsets. Diagonal moves cost 1 too, which is why `[[0,1],[1,0]]` is `2`.
* **Turning `0` into `1` is the visited mark:** `grid[nr][nc] = 1` happens **when pushed**, so each cell is queued once, and the first push carries its shortest distance.

**Recall:** Return `-1` if either corner is blocked. BFS from `(0, 0, 1)` in 8 directions, marking a cell `1` when you push it. Return `dist` when you pop `(n-1, n-1)`, otherwise `-1`.

## 2. Approach

* **Idea:** Unweighted shortest path from one source is plain BFS. Cells are nodes, and two free cells are connected if they touch, including at a corner.
* **Graph representation:** **grid** graph, undirected and unweighted. Moves go in **8 directions**: the `directions` list has every `(dr, dc)` with `dr, dc ∈ {-1, 0, 1}` except `(0, 0)`.
* **Data structure / pointers:**
  * `queue` (`deque`): `(r, c, dist)`, where `dist` = the number of cells on the path from `(0, 0)` to `(r, c)`, counting both ends.
  * `grid` itself is the visited marker. A `0` means free and not yet reached, and a `1` means blocked **or** already queued. The start is marked before the loop, and every other cell is marked **when it is pushed**.
  * Out-of-bounds is checked with `0 <= nr < n and 0 <= nc < n` before `grid[nr][nc]` is read.
* **Invariant:** cells come off `queue` in order of `dist`, so the first time `(n-1, n-1)` is popped, its `dist` is the shortest.
* **Edge cases:**
  * The start or end cell is blocked: returns `-1` right away.
  * A 1×1 grid: `[[0]]` gives `1`, and `[[1]]` gives `-1`.
  * The target is walled off: the queue empties, so it returns `-1`.
  * A diagonal-only route (`[[0,1],[1,0]]`): `2`, because diagonals are allowed.
  * The grid is changed in place (reached cells become `1`). Pass a copy if the caller needs it.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import deque

class Solution:
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        n = len(grid)
        
        # Check if start or target is blocked
        if grid[0][0] != 0 or grid[n-1][n-1] != 0:
            return -1
            
        queue = deque([(0, 0, 1)])  # (row, col, path_length)
        grid[0][0] = 1  # Mark start as visited
        
        # 8-directional offsets
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        while queue:
            r, c, dist = queue.popleft()
            
            # Destination reached
            if r == n - 1 and c == n - 1:
                return dist
                
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check bounds and if destination cell is clear (0)
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1  # Mark visited on push
                    queue.append((nr, nc, dist + 1))
                    
        return -1
```

## 4. Dry Run

Input (LC Example 2):

```text
     c0  c1  c2
r0:   0   0   0
r1:   1   1   0
r2:   1   1   0
```

Neighbours are tried in `directions` order (top-left, up, top-right, left, right, bottom-left, down, bottom-right).

| Pop `(r, c, dist)` | Free neighbours found (marked `1` and pushed) | `queue` after |
| --- | --- | --- |
| `(0, 0, 1)` | `(0,1)` right. `(1,0)` and `(1,1)` are walls | `(0,1,2)` |
| `(0, 1, 2)` | `(0,2)` right, `(1,2)` bottom-right. `(0,0)` is already marked | `(0,2,3) (1,2,3)` |
| `(0, 2, 3)` | none (`(1,2)` is already marked, and the rest are walls or out of bounds) | `(1,2,3)` |
| `(1, 2, 3)` | `(2,2)` down | `(2,2,4)` |
| `(2, 2, 4)` | it's the target `(n-1, n-1)` | return **4** |

Path: `(0,0) → (0,1) → (1,2) → (2,2)`. That's 4 cells, and it uses one diagonal step.

## 5. Complexity

* **Time: O(n²)**, where the grid is n × n
  Think of it as: each free cell is pushed and popped at most once (it becomes `1` when pushed), and each pop checks 8 neighbours, a fixed amount of work. So the total grows with the number of cells.
* **Space: O(n²)**
  Think of it as: no visited set is needed, because the grid itself is the marker. The only extra memory is `queue`, which in the worst case can hold a large share of the cells at once (a wide-open grid with a big ring of cells all the same distance away).

## 6. Recall (30 seconds)

* Unweighted shortest path from one source, so **BFS**. Return `-1` at once if `grid[0][0]` or `grid[n-1][n-1]` is blocked.
* Start at `(0, 0, 1)`, because the length counts **cells**. Use **8 directions**, and mark `grid = 1` **when you push**.
* Return `dist` when you pop the bottom-right cell, otherwise `-1`. O(n²) time and space.
