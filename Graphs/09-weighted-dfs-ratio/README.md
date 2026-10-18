# Group 09 — Weighted DFS (ratio propagation)

## What this pattern is

An ordinary BFS/DFS carries a running **sum** (distance) along the path. This
pattern carries a running **product** (a ratio) instead — everything else is the
same traversal.

## How to recognize it

- You're given **relationships between quantities** — `a / b = 2`, `1 gallon = 16
  cups`, exchange rates — and asked to derive an unknown one.
- The answer along a path is the **product** (or the product of inverses) of the
  edge values, not a sum.
- "Express `x` in terms of `y`", "how many `x` per `y`", "given these ratios,
  find that ratio".

## The template

```python
from collections import defaultdict

graph = defaultdict(dict)
for (a, b), v in zip(equations, values):    # a / b = v
    graph[a][b] = v
    graph[b][a] = 1 / v                       # the reverse edge is the inverse

def dfs(src, dst, seen):
    if src not in graph or dst not in graph:
        return -1.0                            # unknown variable
    if src == dst:
        return 1.0                             # x / x = 1  (only after confirming x exists)
    seen.add(src)
    for nei, w in graph[src].items():
        if nei not in seen:
            sub = dfs(nei, dst, seen)
            if sub != -1.0:
                return w * sub                 # accumulate the PRODUCT
    return -1.0
```

## The one structural fact

The graph is **directed but paired**: an equation `a / b = v` adds edge `a→b`
with weight `v` **and** edge `b→a` with weight `1/v`. In a consistent system,
*every* path from `x` to `y` yields the **same** product — so any DFS/BFS path
gives the right answer.

## Complexity

- Building the graph: `O(E)`.
- Per query: `O(V + E)` (a DFS over the relevant component).
- `Q` queries: `O(Q · (V + E))`. If `Q` is large, precompute all-pairs ratios
  once (`O(V³)` Floyd-Warshall) → `O(1)` per query.

## Problems

1. `01-evaluate-division.md` — the canonical (and only) member: answer `x / y`
   queries from a set of `a / b = v` equations (LeetCode 399).
