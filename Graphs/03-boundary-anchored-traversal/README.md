# Group 03 — Boundary-Anchored Traversal

## What this pattern is

Some grid questions are phrased **per-cell**: *"can water starting at this cell
reach the ocean?"*, *"is this cell trapped, unable to reach the border?"* Checked
naively, that's one search **per cell** — `O(m*n)` searches, each up to `O(m*n)`,
so `O((m*n)²)` total. Too slow.

The fix: **flip the question and start from the boundary instead.** Instead of
asking "can cell X reach the edge?" for every X, ask **"which cells can the edge
reach?"** — seed a multi-source flood **from every border cell at once**, and
expand **inward** using the *reversed* relationship. One flood-fill computes the
answer for **every** cell simultaneously, in a single `O(m*n)` pass.

This is Group 02's multi-source BFS again, with two twists:
1. The sources are **the entire border** (or two borders), not scattered special
   values.
2. The edge you traverse is often the **reverse** of the "real" relationship
   described in the problem (see each problem's section 4 for why).

## How to recognize it

- "Can this cell reach the edge/border/ocean?" — for **every** cell.
- "Which cells are safe / not surrounded / not captured?"
- The natural per-cell simulation would be `O((m*n)²)` or worse; the problem's
  constraints hint at needing something close to `O(m*n)`.
- There's a **directional relationship** between neighbors (flows downhill,
  captures uphill, etc.) — this is exactly what makes "start from the boundary
  and reverse the direction" work.

## The template

```python
from collections import deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def flood_from_border(grid, border_cells, can_reverse_step):
    m, n = len(grid), len(grid[0])
    seen = set(border_cells)
    q = deque(border_cells)
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                    and can_reverse_step(r, c, nr, nc)):
                seen.add((nr, nc))
                q.append((nr, nc))
    return seen                      # every cell that can reach this border
```

`can_reverse_step` encodes "could water/whatever have flowed from `(nr, nc)` to
`(r, c)`?" — i.e. the *reverse* of the real flow direction, because you're walking
backward from the destination (the border) toward every possible origin.

## Complexity for the whole group

- **Time:** `O(m * n)` **per boundary flood** (each is a plain multi-source BFS —
  `concepts/03`, Group 02). Pacific Atlantic runs it twice (`O(m*n)` total, the
  constant `2` doesn't change the class); Surrounded Regions runs it once.
  Compare to the naive `O((m*n)²)` — searching from every cell individually.
- **Space:** `O(m * n)` for each flood's visited set / queue.

## Problems

1. `01-pacific-atlantic-water-flow.md` — flood from **two** different borders
   (Pacific: top+left, Atlantic: bottom+right), separately, then **intersect**
   the two reachable sets (LeetCode 417). **Start here.**
2. `02-surrounded-regions.md` — flood from **one** border (any `O` touching the
   edge is "safe"), then flip everything *not* reached (LeetCode 130).
