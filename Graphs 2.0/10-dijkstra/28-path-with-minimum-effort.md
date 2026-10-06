# 1631. Path With Minimum Effort

**LC 1631** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Minimax Dijkstra on edges (a path's cost is its **biggest single step**)

---

## 1. Intuition

You're hiking from the top-left to the bottom-right of a height map. A route's "effort" is its **single
steepest step** (the biggest height difference between two neighbouring cells on it), not the total
climbing. You want the route whose worst step is as gentle as possible. It's the same idea as Swim in
Rising Water (#27), but the cost sits on the **edges** (height differences) instead of the cells.

* **Step cost:** `step = abs(heights[nr][nc] - heights[r][c])`, the height difference for this one move.
* **Path effort = max so far:** `new_e = max(e, step)`. A gentle step doesn't lower the effort, and a steep one raises it.
* **The heap gives the gentlest route first:** `heap` holds `(e, r, c)`, so the route with the smallest worst-step-so-far is expanded next.
* **`effort[r][c]` = the best effort found so far for this cell:** the start is `0` (no steps yet), and it's only updated when `new_e < effort[nr][nc]`. When the target is first popped (and not stale), its `e` is the answer.

**Recall:** Dijkstra on the grid with `new_e = max(e, |height difference|)`. Start at `(0, 0, 0)` and return `e` when the bottom-right cell is popped.

## 2. Approach

* **Idea:** Minimise the largest edge on a path. Dijkstra works because a path's effort **never goes down** as it gets longer (`max` only stays the same or grows). That's the same reason non-negative weights work in normal Dijkstra.
* **Graph representation:** implicit **grid** graph (rows × cols), undirected. The weight of moving between neighbours is their **absolute height difference**. Moves go in **4 directions**: `(1,0), (-1,0), (0,1), (0,-1)`. Out-of-bounds is checked with `0 <= nr < rows and 0 <= nc < cols`.
* **Data structure / pointers:**
  * `heap`: a min-heap of **`(e, r, c)`**. Tuples compare by `e` first, so the smallest effort pops first. Ties are broken by `r`, then `c`, which is harmless.
  * `effort[r][c]`: the smallest "worst step" found so far for any route to `(r, c)`.
  * **When is a cell final?** When it's **popped** with `e == effort[r][c]`. A pop with `e > effort[r][c]` is stale and skipped.
* **Invariant:** each non-stale pop `(e, r, c)` has the smallest possible effort for that cell. Every other route goes through something still in the heap, which already has effort ≥ `e`, and a `max` can't bring it back down.
* **Edge cases:**
  * A 1×1 grid: the start is the target, so it returns `0`.
  * A single row or column: there's only one route, so the effort is its biggest step.
  * All heights equal: every step is `0`, so it returns `0`.
  * A detour beats a direct path when the direct path has one steep step (LC Example 1: going around the `8` gives effort 2 instead of 5 or more).
  * The grid is always connected, so the final `return 0` is never reached.
  * It's iterative, so there's no recursion-depth risk.
  * **Other ways to solve it:** binary search on the effort plus a BFS that only allows steps `≤ mid`, or union-find that adds edges from gentlest to steepest until the corners join (Kruskal-style).

## 3. Code

### Main: `effort` grid + min-heap (skip stale entries)

```python
import heapq
from typing import List


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows, cols = len(heights), len(heights[0])
        effort = [[float('inf')] * cols for _ in range(rows)]  # smallest max-step found so far
        effort[0][0] = 0
        heap = [(0, 0, 0)]  # (biggest step on the path so far, row, col)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while heap:
            e, r, c = heapq.heappop(heap)
            if e > effort[r][c]:
                continue  # stale entry
            if r == rows - 1 and c == cols - 1:
                return e

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    step = abs(heights[nr][nc] - heights[r][c])
                    new_e = max(e, step)  # path effort = its biggest single step
                    if new_e < effort[nr][nc]:
                        effort[nr][nc] = new_e
                        heapq.heappush(heap, (new_e, nr, nc))

        return 0  # never reached: the grid is always connected
```

### Alternative: min-heap + `visited` set (finalise on the first pop)

There's no `effort` grid. The first time a cell is popped, its `e` is final, so later copies are skipped.

```python
import heapq
from typing import List


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        rows, cols = len(heights), len(heights[0])
        heap = [(0, 0, 0)]  # (biggest step on the path so far, row, col)
        visited = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while heap:
            e, r, c = heapq.heappop(heap)
            if (r, c) in visited:
                continue  # already finalised with a smaller effort
            visited.add((r, c))
            if r == rows - 1 and c == cols - 1:
                return e

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    step = abs(heights[nr][nc] - heights[r][c])
                    heapq.heappush(heap, (max(e, step), nr, nc))

        return 0  # never reached: the grid is always connected
```

| | Main (`effort` + heap) | Alternative (heap + `visited`) |
| --- | --- | --- |
| Cell is final when… | popped with `e == effort[r][c]` | popped for the **first** time |
| Pushes | only when `new_e < effort[nr][nc]` | every unvisited neighbour |
| Heap size | smaller | larger (more duplicate entries) |

## 4. Dry Run

Input (LC Example 1):

```text
        c0  c1  c2
r0:      1   2   2
r1:      3   8   2
r2:      5   3   5
```

Main version. Neighbours are tried down, up, right, left. `step` = the height difference, and `new_e = max(e, step)`.

| Pop `(e, r, c)` | Pushes | Note |
| --- | --- | --- |
| `(0, 0, 0)` | `(1,0)`: \|3−1\| = 2, so **2**. `(0,1)`: \|2−1\| = 1, so **1** | |
| `(1, 0, 1)` | `(1,1)`: \|8−2\| = 6, so **6**. `(0,2)`: \|2−2\| = 0, so max(1,0) = **1** | |
| `(1, 0, 2)` | `(1,2)`: \|2−2\| = 0, so **1** | |
| `(1, 1, 2)` | `(2,2)`: \|5−2\| = 3, so **3**. `(1,1)`: \|8−2\| = 6, but 6 isn't < 6 | right-side route reaches the target with effort 3 |
| `(2, 1, 0)` | `(2,0)`: \|5−3\| = 2, so **2**. `(1,1)`: \|8−3\| = 5 < 6, so **5** | |
| `(2, 2, 0)` | `(2,1)`: \|3−5\| = 2, so **2** | |
| `(2, 2, 1)` | `(2,2)`: \|5−3\| = 2, so max(2,2) = **2** < 3, which improves the target | the `(3, 2, 2)` entry is now stale |
| `(2, 2, 2)` | **target**, so return **2** | |

The best route is `1 → 3 → 5 → 3 → 5` (down the left side, then along the bottom), and its steepest step is **2**. The route down the right side has a step of 3. The Alternative finalises cells in the same order and also returns 2.

## 5. Complexity

Let **R × C** be the grid size.

* **Time: O(R·C · log(R·C))**
  Think of it as: each cell causes at most a few heap pushes (4 neighbours), and each push or pop costs about log(heap size). With R·C cells, that's R·C × log(R·C).
* **Space: O(R·C)**
  Think of it as: `effort` (or `visited`) has one slot per cell, and the heap holds at most a few entries per cell.

## 6. Recall (30 seconds)

* Route cost = its **steepest single step**. Use Dijkstra with `new_e = max(e, abs(height difference))`, which works because `max` never decreases.
* Heap of `(e, r, c)` from `(0, 0, 0)`. Main: skip `e > effort[r][c]` and push on `new_e < effort[nr][nc]`. Alternative: `visited` on pop.
* Return `e` when the bottom-right cell is popped. O(RC log RC) time and O(RC) space. It's the "edge" version of Swim in Rising Water (#27).
