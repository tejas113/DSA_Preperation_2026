# 542. 01 Matrix

**LC 542** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Multi-source BFS on a grid (all `0`s start in the queue, separate `dist` matrix)

---

## 1. Intuition

Running a BFS from every `1` to find its nearest `0` is O((M × N)²) and far too slow. Flip it around: start
from **all the `0`s at once** and let the distances spread outward one layer at a time. The first wave that
reaches a `1` comes from its nearest `0`.

* **Every `0` is a source:** step 1 pushes each `(r, c)` with `mat[r][c] == 0` and sets `dist[r][c] = 0`.
* **`-1` means not visited:** `dist = [[-1] * cols ...]` starts every cell as unvisited. The check `dist[nr][nc] == -1` lets each cell be written only once.
* **First visit is the shortest:** `dist[nr][nc] = dist[r][c] + 1`. BFS pops cells in order of distance, so the first write is already the smallest distance possible.
* **The input isn't changed:** the answer goes into a new `dist` grid, so `mat` stays as it was. (Walls and Gates wrote into its input.)

**Recall:** Put every `0` in the queue with `dist = 0`, everything else `-1`. BFS, and each `-1` neighbour gets `dist + 1`.

## 2. Approach

* **Idea:** One BFS that starts from all the `0`s together. The BFS layer at which a cell is first reached is its distance to the nearest `0`.
* **Graph representation:** implicit **grid** graph, undirected and unweighted (every step costs 1). Moves go in **4 directions**, from `directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]` (right, left, down, up). There are no walls, so every cell can be passed through.
* **Data structure / pointers:**
  * `dist`: the answer grid and also the visited marker. `-1` means not reached yet, and any value of 0 or more is final. A cell is marked **when it is pushed**.
  * `queue` (`deque`): the BFS frontier of `(r, c)` cells. It starts with every `0`, and `popleft()` gives first-in, first-out order, so cells come out in distance order.
  * Out-of-bounds is checked with `0 <= nr < rows and 0 <= nc < cols` before `dist[nr][nc]` is read.
* **Invariant:** the queue holds cells whose distances are never more than one apart (some at `d`, the rest at `d + 1`). So when a `-1` cell is first written, no `0` can be closer to it.
* **Edge cases:**
  * All `0`s: every cell is a source, nothing new is pushed, and it returns all `0`s.
  * A single `0` in a big grid of `1`s: it spreads like ripples, and each cell gets its Manhattan distance (`|dr| + |dc|`) to that `0`, because there are no walls.
  * A 1×1 grid: `[[0]]` → `[[0]]`. (LC guarantees at least one `0`.)
  * No `0` at all isn't possible on LeetCode. If it happened, every cell would stay `-1`.
  * Separate groups of `1`s: fine, because every `0` starts at the same time, so each group gets reached from its own nearest `0`.
  * An empty matrix isn't possible (LC guarantees `m, n ≥ 1`). With `[]`, `mat[0]` would raise `IndexError`.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import deque


class Solution:

    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        rows = len(mat)
        cols = len(mat[0])

        # Distance matrix initialized to -1 (unvisited)
        dist = [[-1] * cols for _ in range(rows)]
        queue = deque()

        # Step 1: Add all 0s as sources to the queue and set their distance to 0
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    queue.append((r, c))
                    dist[r][c] = 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Step 2: Multi-source BFS to propagate distances
        while queue:
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # If neighbor is within bounds and unvisited
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))

        return dist
```

## 4. Dry Run

Input (LC Example 2):

```text
r0:  0  0  0
r1:  0  1  0
r2:  1  1  1
```

Neighbours are tried in the order **right, left, down, up**. The table shows only the pops that write something, plus the last one.

| Pop `(r, c)` | `dist[r][c]` | Cells written (`-1` → value) | `queue` after |
| --- | --- | --- | --- |
| (start) | — | all five `0`s get `0` | `(0,0) (0,1) (0,2) (1,0) (1,2)` |
| `(0,0)` | 0 | none (neighbours are `0`s or out of bounds) | `(0,1) (0,2) (1,0) (1,2)` |
| `(0,1)` | 0 | `(1,1) = 1` (down) | `(0,2) (1,0) (1,2) (1,1)` |
| `(0,2)` | 0 | none | `(1,0) (1,2) (1,1)` |
| `(1,0)` | 0 | `(2,0) = 1` (down). Right `(1,1)` is already `1`, so skip | `(1,2) (1,1) (2,0)` |
| `(1,2)` | 0 | `(2,2) = 1` (down) | `(1,1) (2,0) (2,2)` |
| `(1,1)` | 1 | `(2,1) = 2` (down) | `(2,0) (2,2) (2,1)` |
| `(2,0)`, `(2,2)`, `(2,1)` | 1, 1, 2 | none (all neighbours already set) | empty, so the BFS stops |

Returns **`[[0,0,0],[0,1,0],[1,2,1]]`**.

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: every cell goes into the queue exactly once. The `0`s go in at the start, and each `1` goes in the moment its `dist` changes from `-1`, which happens only once. Each pop checks 4 neighbours, which is a fixed amount of work. Add the first scan and the building of `dist`, and the total grows with the number of cells.
* **Space: O(rows × columns)**
  Think of it as: `dist` is a full grid the same size as `mat`. That's the output, so you could count it as required space rather than extra. The real extra memory is `queue`. If the grid is mostly `0`s, almost every cell is in the queue at the start, so the worst case is also O(rows × columns).

## 6. Recall (30 seconds)

* Don't BFS from each `1`. **BFS once from all the `0`s**, and the first time a cell is reached gives its nearest-`0` distance.
* `dist` starts at `-1` (unvisited) and `0` for the sources. Write `dist[nr][nc] = dist[r][c] + 1`, then push, which marks it when pushed.
* O(R·C) time and O(R·C) space. The same pattern as Walls and Gates, but with a separate answer grid and no walls.
