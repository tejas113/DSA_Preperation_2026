# Group 02 — Multi-Source BFS on a Grid

## What this pattern is

Normal BFS starts from **one** node. Here you start from **many at once** — every
"source" cell is pushed into the queue *before* the BFS loop even begins, all
already at distance `0`. BFS then expands outward from all of them
simultaneously, like ripples from several stones dropped in a pond at the same
moment.

The payoff: every cell ends up with its distance to the **nearest** source,
computed in a single `O(m*n)` pass — not one BFS per source.

This is `concepts/03` (BFS) with one change: the queue's *starting contents*.

## How to recognize it

- "Distance from every cell to the **nearest** X" (nearest gate, nearest 0,
  nearest exit).
- "How many minutes/steps until **everything** is reached / infected / rotten."
- There are **multiple starting points**, and they all begin spreading **at the
  same time** (not one after another).
- Words: "nearest", "closest", "minimum distance to any", "spreads/rots/infects
  simultaneously".

**Don't confuse with:** Group 01 (flood fill) counts/measures separate regions and
doesn't care about distance. Group 02 always produces a **distance** (or a
"number of rounds") for every cell.

## The template

```python
from collections import deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def multi_source_bfs(grid, is_source, is_blocked):
    m, n = len(grid), len(grid[0])
    q = deque()

    for r in range(m):                       # seed the queue with EVERY source
        for c in range(n):
            if is_source(r, c):
                q.append((r, c))              # all start at distance 0

    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < m and 0 <= nc < n
                    and not is_blocked(nr, nc) and not_yet_visited(nr, nc)):
                record_distance(nr, nc, distance(r, c) + 1)
                q.append((nr, nc))
```

The one rule that makes this different from single-source BFS: **all sources go
in before the first pop.** If you instead ran a separate BFS per source and took
the minimum, you'd get the same answer but pay `O(sources × m*n)` — multi-source
BFS gets it in one `O(m*n)` pass because the ripples race each other and a cell is
only ever claimed by whichever source reaches it first (which is automatically the
*nearest* one, since BFS explores in order of distance).

## The nice trick this group reuses from Group 01

In Flood Fill, recoloring a cell doubled as its visited mark. Here, **writing the
real distance into the cell doubles as its visited mark** — a cell holding
"unvisited" sentinel (`INF`, or `0` meaning "not yet reached" in Rotting Oranges)
gets overwritten with its distance the first (and only) time it's reached, so
`cell == UNVISITED_SENTINEL` *is* the "not yet in the queue" check. No separate
`seen` set needed.

## Complexity for the whole group

- **Time:** `O(m * n)`. Exactly the same as a single BFS over the grid — seeding
  the queue with `k` sources instead of `1` costs `O(k)` extra up front, which is
  at most `O(m*n)` anyway.
- **Space:** `O(m * n)` for the queue in the worst case, plus the grid itself
  (no extra `seen` structure — see the trick above).

## Problems

1. `01-walls-and-gates.md` — the purest form of the pattern. Sources = gates
   (LeetCode 286, premium). **Start here.**
2. `02-01-matrix.md` — sources = every `0` cell; find each `1` cell's distance to
   the nearest `0` (LeetCode 542).
3. `03-rotting-oranges.md` — sources = every already-rotten orange; answer =
   number of BFS rounds, with an extra check for unreachable fresh oranges
   (LeetCode 994).
4. `04-shortest-bridge.md` *(supplementary)* — a **hybrid**: DFS to find and mark
   one whole island, then multi-source BFS from *every* cell of that island
   outward to the other island (LeetCode 934).
