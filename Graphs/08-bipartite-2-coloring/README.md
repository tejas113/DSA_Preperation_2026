# Group 08 — Bipartite / 2-Coloring

## What this pattern is

Split a graph's nodes into **two groups** so that every edge goes *between* the
groups. Test it by **2-coloring**: BFS/DFS from each node, color neighbors the
opposite color, and fail the moment two adjacent nodes end up the same color.

Full mechanics: `concepts/09-bipartite-coloring.md`.

## How to recognize it

- "Split into **two** groups/teams/shifts so [conflicts/enemies/rivalries] are
  separated."
- "Is this graph bipartite / 2-colorable?"
- "No two adjacent X may be the same."
- A hidden version: you're given **conflict pairs** and asked if a 2-way split
  exists (Possible Bipartition) — build the conflict graph, then 2-color it.

**The theorem to say out loud:** *bipartite ⟺ no odd-length cycle*. The coloring
BFS/DFS finds an odd cycle exactly when it hits a same-color conflict.

## The template

```python
from collections import deque

def is_bipartite(graph, n):
    color = [0] * n                       # 0 = uncolored; 1 / -1 = the two colors
    for start in range(n):                # MUST loop all components
        if color[start] != 0:
            continue
        color[start] = 1
        q = deque([start])
        while q:
            node = q.popleft()
            for nei in graph[node]:
                if color[nei] == 0:
                    color[nei] = -color[node]     # opposite color, marked on enqueue
                    q.append(nei)
                elif color[nei] == color[node]:
                    return False                   # conflict -> odd cycle
    return True
```

## Complexity

- **Time:** `O(V + E)` — a BFS/DFS with a color array.
- **Space:** `O(V)` for `color` + `O(V)` frontier.

## Problems

1. `01-is-graph-bipartite.md` — the pattern in its purest form: you're handed the
   adjacency list, return whether it's 2-colorable (LeetCode 785). **Start here.**
2. `02-possible-bipartition.md` — same 2-coloring, but you **build the graph
   first** from a list of "dislikes" pairs (LeetCode 886).
