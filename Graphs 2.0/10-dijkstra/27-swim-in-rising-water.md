# 778. Swim in Rising Water

**LC 778** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Minimax Dijkstra (a path's cost is its **highest** cell, not the sum)

---

## 1. Intuition

The water level rises by 1 every second, and you can swim into a cell once the water is at least as high as
that cell. So a route is usable at time `t` exactly when **every cell on it is ≤ t**. The time a route needs
is its **highest cell**, and you want the route whose highest cell is as low as possible. That's Dijkstra
with one change: instead of *adding* a cost at each step, you take the **max**.

* **Path cost = max so far:** `new_t = max(t, grid[nr][nc])`. Stepping into a higher cell raises the cost, and stepping into a lower cell keeps it the same.
* **The heap gives the "lowest highest point" first:** `heap` holds `(t, r, c)`, so the route with the smallest highest-cell-so-far is always expanded next.
* **`dist[r][c]` = the best `t` found so far to reach `(r, c)`:** it starts as `grid[0][0]` at the start (you must wait for your own cell too), and an update only happens when `new_t < dist[nr][nc]`.
* **Stop as soon as the target is popped:** the first real (non-stale) pop of `(n-1, n-1)` carries the smallest possible `t`.

**Recall:** Dijkstra on the grid with `cost = max(t, grid[nr][nc])` instead of `t + w`. Start at `(grid[0][0], 0, 0)` and return `t` when the bottom-right cell is popped.

## 2. Approach

* **Idea:** Minimise the maximum cell along a path. Dijkstra works because a path's cost **never goes down** as it gets longer (a `max` can only stay the same or grow). That's the same property that non-negative weights give normal Dijkstra.
* **Graph representation:** implicit **grid** graph (n × n), undirected, with the "weight" on each **cell** (its elevation). Moves go in **4 directions**: `(1,0), (-1,0), (0,1), (0,-1)`. Out-of-bounds is checked with `0 <= nr < n and 0 <= nc < n`.
* **Data structure / pointers:**
  * `heap`: a min-heap of **`(t, r, c)`**. Tuples compare by `t` first, so the lowest highest-point pops first. Ties are broken by `r`, then `c`, which is harmless.
  * `dist[r][c]`: the lowest "highest elevation" found so far for any route to `(r, c)`.
  * **When is a cell final?** When it's **popped** with `t == dist[r][c]`. A pop with `t > dist[r][c]` is stale and skipped.
* **Invariant:** each non-stale pop `(t, r, c)` has the smallest possible `t` for that cell. Any other route would have to go through something still in the heap, which already costs at least `t`, and taking a `max` can't make it smaller.
* **Edge cases:**
  * `n = 1`: the start is the target, so it returns `grid[0][0]` (here, `0`).
  * The answer is always at least `max(grid[0][0], grid[n-1][n-1])`, because you have to stand on both corners.
  * The grid is always connected (every cell can eventually be swum into), so the final `return -1` is never reached.
  * The elevations are a permutation of `0 … n²-1` on LC, so all values are different, but the code doesn't rely on that.
  * It's iterative, so there's no recursion-depth risk.
  * **Other ways to solve it:** binary search on `t` plus a BFS that only uses cells `≤ t`, or union-find that adds cells from lowest to highest elevation until the two corners join.

## 3. Code

### Main: `dist` grid + min-heap (skip stale entries)

```python
import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        dist = [[float('inf')] * n for _ in range(n)]  # lowest "highest elevation" found to reach each cell
        dist[0][0] = grid[0][0]
        heap = [(grid[0][0], 0, 0)]  # (highest elevation on the path so far, row, col)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while heap:
            t, r, c = heapq.heappop(heap)
            if t > dist[r][c]:
                continue  # stale entry
            if r == n - 1 and c == n - 1:
                return t  # first real pop of the target is the answer

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    new_t = max(t, grid[nr][nc])  # path cost = highest cell on it
                    if new_t < dist[nr][nc]:
                        dist[nr][nc] = new_t
                        heapq.heappush(heap, (new_t, nr, nc))

        return -1  # never reached: the grid is always connected
```

### Alternative: min-heap + `visited` set (finalise on the first pop)

There's no `dist` grid. The first time a cell is popped, its `t` is final, so later copies are skipped.

```python
import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        heap = [(grid[0][0], 0, 0)]  # (highest elevation on the path so far, row, col)
        visited = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while heap:
            t, r, c = heapq.heappop(heap)
            if (r, c) in visited:
                continue  # already finalised with a lower t
            visited.add((r, c))
            if r == n - 1 and c == n - 1:
                return t

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                    heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))

        return -1  # never reached: the grid is always connected
```

| | Main (`dist` + heap) | Alternative (heap + `visited`) |
| --- | --- | --- |
| Cell is final when… | popped with `t == dist[r][c]` | popped for the **first** time |
| Pushes | only when `new_t < dist[nr][nc]` | every unvisited neighbour |
| Heap size | smaller | larger (more duplicate entries) |

## 4. Dry Run

Input (a small example where the obvious route isn't the best one):

```text
        c0  c1  c2
r0:      0   3   8
r1:      1   7   4
r2:      6   5   2
```

Main version. Neighbours are tried down, up, right, left.

| Pop `(t, r, c)` | Pushes (`new_t = max(t, cell)`) | Heap after (smallest first) |
| --- | --- | --- |
| `(0, 0, 0)` | `(1,0)`: max(0,1) = **1**. `(0,1)`: max(0,3) = **3** | `(1,1,0) (3,0,1)` |
| `(1, 1, 0)` | `(2,0)`: max(1,6) = **6**. `(1,1)`: max(1,7) = **7** | `(3,0,1) (6,2,0) (7,1,1)` |
| `(3, 0, 1)` | `(1,1)`: max(3,7) = 7, not < 7, so no. `(0,2)`: max(3,8) = **8** | `(6,2,0) (7,1,1) (8,0,2)` |
| `(6, 2, 0)` | `(2,1)`: max(6,5) = **6** | `(6,2,1) (7,1,1) (8,0,2)` |
| `(6, 2, 1)` | `(2,2)`: max(6,2) = **6**. `(1,1)`: max(6,7) = 7, not < 7 | `(6,2,2) (7,1,1) (8,0,2)` |
| `(6, 2, 2)` | **target**, so return **6** | — |

The best route is `0 → 1 → 6 → 5 → 2` (down the left side, then along the bottom), and its highest cell is **6**. The route along the top would need 8, and any route through the middle needs 7. The Alternative pops in exactly the same order and also returns 6.

## 5. Complexity

* **Time: O(n² log n)**
  Think of it as: there are n² cells, and each one causes at most a few heap pushes (4 neighbours). Every push or pop costs about log(heap size), and the heap never holds more than about 4n² entries, so that's log(n²) = 2 log n. In total, about n² × log n.
* **Space: O(n²)**
  Think of it as: `dist` (or `visited`) has one slot per cell, and the heap can hold several entries per cell in the worst case.

## 6. Recall (30 seconds)

* The cost of a route = its **highest cell**. Dijkstra still works, because `max` never decreases along a path.
* Heap of `(t, r, c)` starting at `(grid[0][0], 0, 0)`. Relax with `new_t = max(t, grid[nr][nc])`. Main: skip `t > dist[r][c]`. Alternative: `visited` on pop.
* Return `t` when the bottom-right cell is popped. O(n² log n) time and O(n²) space. Other ways: binary search + BFS, or union-find.
