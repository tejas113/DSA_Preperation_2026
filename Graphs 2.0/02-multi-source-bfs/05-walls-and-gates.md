# 286. Walls and Gates

**LC 286 🔒** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Multi-source BFS on a grid (all gates start in the queue together)

---

## 1. Intuition

Picture every gate letting out water at the same moment. The water spreads one room per tick in
all directions, but it can't pass walls. The tick at which water first reaches a room is that room's distance
to the *nearest* gate. You don't need to know which gate it came from.

* **All gates start together:** step 1 puts every `(r, c)` with `rooms[r][c] == 0` into `queue` (and into `visited`) before the BFS starts. That's what "multi-source" means.
* **Distance = parent's distance + 1:** `rooms[nr][nc] = rooms[r][c] + 1`. BFS pops cells in order of distance, so the first time a room is reached is also its shortest distance.
* **`visited` stops repeat visits:** the check `(nr, nc) not in visited` makes sure a room is written only once, by the first (closest) gate wave that reaches it.
* **Walls block the wave:** `rooms[nr][nc] != -1` skips walls. Gates are already in `visited`, so the only cells that pass both checks are unreached empty rooms.

**Recall:** Put every gate in the queue and in `visited`, then BFS. Each unvisited non-wall neighbour gets `current + 1`, is added to `visited`, and is pushed.

## 2. Approach

* **Idea:** Run one BFS that starts from *all* gates at once. It reaches rooms in order of distance from the nearest gate, so each empty room's first write is its final answer.
* **Graph representation:** implicit **grid** graph, undirected and unweighted (every step costs 1). Moves go in **4 directions**, from `directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]` (right, left, down, up). Walls (`-1`) are blocked cells.
* **Data structure / pointers:**
  * `queue` (`deque`): the BFS frontier of `(r, c)` cells. It starts with all gates, and `popleft()` gives first-in, first-out order, which is what makes the distances come out in order.
  * `visited` (a set of `(r, c)`): the cells that have already been given a distance (gates count as distance 0). A cell is marked **when it is pushed**, so it's never queued twice.
  * `rooms`: holds the answer. Each empty room is overwritten once, with its distance.
  * Out-of-bounds is checked with `0 <= nr < rows and 0 <= nc < cols` before `rooms[nr][nc]` is read.
* **Invariant:** the queue holds cells whose distances are never more than one apart (some at `d`, the rest at `d + 1`). So when a room is first written, no gate can be closer to it.
* **Edge cases:**
  * Empty grid `[]` or `[[]]`: `if not rooms or not rooms[0]` returns at once.
  * No gates: `queue` starts empty, so every room stays INF (`2147483647`).
  * A room that walls cut off from every gate: it's never reached, so it stays INF.
  * No empty rooms (only walls and gates): nothing changes.
  * A single cell (`[[0]]`, `[[-1]]`, `[[INF]]`): unchanged.
  * It changes `rooms` in place and returns `None`, as LeetCode requires.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import deque
from typing import List

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        if not rooms or not rooms[0]:
            return

        rows, cols = len(rooms), len(rooms[0])
        queue = deque()
        visited = set()

        # 1. Add all gates (0s) to queue and mark them as visited
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    queue.append((r, c))
                    visited.add((r, c))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # 2. Multi-source BFS
        while queue:
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check boundaries, if unvisited, and if it's an empty room (not a wall)
                if (0 <= nr < rows and 0 <= nc < cols and 
                    (nr, nc) not in visited and 
                    rooms[nr][nc] != -1):
                    
                    visited.add((nr, nc))
                    rooms[nr][nc] = rooms[r][c] + 1  # Update distance
                    queue.append((nr, nc))
```

### Alternative: no `visited` set (the INF value is the visited marker)

This is the same BFS, but `rooms[nr][nc] == 2147483647` does the work of `visited`. Only unreached empty rooms equal INF, and a room stops being INF as soon as it gets a distance. That saves the O(rows × columns) set.

```python
from collections import deque
from typing import List

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        if not rooms or not rooms[0]:
            return

        rows, cols = len(rooms), len(rooms[0])
        queue = deque()

        # 1. Add all gates (0s) to the queue as starting points
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    queue.append((r, c))

        # 4-directional movements: right, left, down, up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # 2. Multi-source BFS from all gates simultaneously
        while queue:
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check boundaries and if the cell is an unvisited empty room
                if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
                    # Update distance to gate
                    rooms[nr][nc] = rooms[r][c] + 1
                    queue.append((nr, nc))
```

## 4. Dry Run

Input (`I` = 2147483647). Gates are at `(0,2)` and `(2,0)`. Neighbours are tried in the order **right, left, down, up**.

```text
r0:  I  -1   0
r1:  I   I   I
r2:  0  -1   I
```

| Pop `(r, c)` | Its distance | Neighbours written (added to `visited`) | `queue` after |
| --- | --- | --- | --- |
| (start) | — | gates pushed, `visited = {(0,2), (2,0)}` | `(0,2) (2,0)` |
| `(0,2)` | 0 | `(1,2) = 1` (down) | `(2,0) (1,2)` |
| `(2,0)` | 0 | `(1,0) = 1` (up) | `(1,2) (1,0)` |
| `(1,2)` | 1 | `(1,1) = 2` (left), `(2,2) = 2` (down) | `(1,0) (1,1) (2,2)` |
| `(1,0)` | 1 | `(0,0) = 2` (up). Right `(1,1)` is already in `visited`, so skip | `(1,1) (2,2) (0,0)` |
| `(1,1)` | 2 | none | `(2,2) (0,0)` |
| `(2,2)` | 2 | none | `(0,0)` |
| `(0,0)` | 2 | none | empty, so the BFS stops |

Final `rooms`:

```text
r0:  2  -1   0
r1:  1   2   1
r2:  0  -1   2
```

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: every cell goes into the queue at most once. Gates go in at the start, and each empty room goes in only the first time it's added to `visited`. Each pop checks 4 neighbours, and a set lookup takes about the same time no matter how big the set is, so it's a fixed amount of work per cell. Add the first scan over the grid and the total grows with the number of cells.
* **Space: O(rows × columns)**
  Think of it as: two things grow with the grid. `visited` ends up holding every reachable cell, and `queue` can hold a large share of the cells at once in the worst case. The Alternative drops `visited` by using the INF value in `rooms` instead, but `queue` keeps it at O(rows × columns) worst case anyway.

## 6. Recall (30 seconds)

* Don't BFS from every room (that's slow, O((R·C)²)). Instead **BFS once from all gates together**, so the first time a room is reached is its nearest-gate distance.
* Mark when pushing: add to `visited`, write `rooms[nr][nc] = rooms[r][c] + 1`, then push. Skip walls with `!= -1`. Gates start in `visited`.
* O(R·C) time and O(R·C) space. Rooms no gate can reach stay INF. Interview bonus: drop `visited` and use `== INF` as the check.
