# Group 01 — Grid Flood-Fill

## What this pattern is

You have a 2D grid. Some cells "belong together" (same color, both land, same
value). You want to **find, count, or measure connected blobs of cells**.

The tool: pick a starting cell, then **flood** outward to every connected same-kind
cell (DFS or BFS), marking each as visited so you never process it twice. Wrap that
flood in a loop over all cells to handle multiple blobs.

This is `concepts/05` (connected components) applied to a grid, using `concepts/03`
(BFS) or `concepts/04` (DFS) as the flood.

## How to recognize it

- Input is a grid / matrix / image / map of characters or 0-1s.
- Words: "island", "region", "blob", "area", "connected", "same color", "how many
  groups", "largest".
- You move between **4-directionally** (sometimes 8) adjacent cells of the same
  kind.
- You do **not** need a shortest path — just "what's connected to what".

## The template (memorize this — all 4 problems are edits of it)

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def solve(grid):
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    seen = set()

    def dfs(r, c):
        if not (0 <= r < m and 0 <= c < n):
            return 0
        if (r, c) in seen or grid[r][c] != TARGET:
            return 0
        seen.add((r, c))
        size = 1
        for dr, dc in DIRS:
            size += dfs(r + dr, c + dc)
        return size

    result = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == TARGET and (r, c) not in seen:
                blob = dfs(r, c)
                result = handle(result, blob)   # count: result += 1 ; area: result = max(result, blob)
    return result
```

## What changes per problem

| Problem | TARGET | `handle` | Extra |
|---|---|---|---|
| Number of Islands | `"1"` | `result += 1` | — |
| Flood Fill | old color of the start pixel | — (single flood, no outer loop) | recolor while flooding |
| Max Area of Island | `1` | `result = max(result, blob)` | flood returns size |
| Making a Large Island | `1` | — | give each island an id + size, then for every `0` cell sum the distinct neighbor island sizes + 1 |

## Complexity for the whole group

- **Time:** `O(m * n)`. The outer double loop is `m*n`. Every cell is flooded at
  most once (the `seen` check), so all the floods together are also `O(m*n)`, not
  `O((m*n)²)`.
- **Space:** `O(m * n)` for `seen` plus, in the worst case (one giant snake-shaped
  island), `O(m*n)` for the recursion stack / BFS queue.
  - Space-optimized: overwrite visited cells in the grid instead of a `seen` set →
    `O(m*n)` recursion in the worst case still, but no separate set. Iterative BFS
    caps recursion at 0.

## BFS or DFS here?

Either works and both are `O(m*n)`. DFS (recursion) is shorter and reads naturally
("sink this cell, then sink its neighbors"). Use BFS (iterative) if the grid could
be so large that recursion depth (~1000 in Python) would crash — a 1000×1000 solid
island recurses a million deep. Every problem file shows both.

## Problems

1. `01-number-of-islands.md` — the canonical count-the-blobs problem. **Start here.**
2. `02-flood-fill.md` — single flood, recolor as you go. The simplest possible member.
3. `03-max-area-of-island.md` — flood returns a size; track the max.
4. `04-making-a-large-island.md` *(supplementary)* — the Google-hard version: label
   islands with sizes, then test each water cell as a bridge. Two passes.
