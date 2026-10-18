# Group 14 — Eulerian Path / Advanced DFS

## What this pattern is

Find a path (or circuit) that uses **every edge exactly once** — an **Eulerian
path**. The tool is **Hierholzer's algorithm**: a DFS where you add a node to the
route **on the way back out** (post-order), then reverse at the end.

**Contrast:**
- **Eulerian** = every *edge* once → **polynomial** (Hierholzer, `O(E)` / `O(E log E)` with a sort).
- **Hamiltonian** = every *node* once → **NP-hard**.

## How to recognize it

- "Use **every ticket / every road / every edge** exactly once."
- "Reconstruct the tour / itinerary / route that covers all connections."
- "Valid arrangement of all the given pairs."

## Hierholzer's algorithm

```python
import heapq
from collections import defaultdict

def eulerian_path(graph, start):          # graph[u] = min-heap of destinations
    route = []
    def dfs(node):
        while graph[node]:
            dfs(heapq.heappop(graph[node]))   # consume an edge, go deeper
        route.append(node)                    # POST-ORDER: node is done -> record it
    dfs(start)
    return route[::-1]                         # built backwards -> reverse
```

**Why post-order + reverse:** when the DFS gets "stuck" at a node (no edges
left), that node is either the path's end or a dead-end of a fully-explored
branch. Recording stuck nodes and reversing splices any sub-cycles into their
correct positions automatically.

**Why the min-heap:** always taking the lexicographically smallest next edge
yields the **lexicographically smallest** Eulerian path (which Reconstruct
Itinerary asks for).

## Existence conditions (directed graph)

An Eulerian **path** exists iff, ignoring isolated vertices, the graph is
connected **and**:
- exactly one vertex has `out - in = 1` (the start), and
- exactly one has `in - out = 1` (the end), and
- every other vertex has `in = out`.

(All balanced ⟹ an Eulerian **circuit** — start anywhere.)

## Complexity

`O(E)` for the DFS; `O(E log E)` total if you sort/heap the adjacency lists for
lexicographic order. Space `O(E)`.

## Problems

1. `01-reconstruct-itinerary.md` — the canonical Eulerian-path problem:
   reconstruct the flight itinerary that uses all tickets, starting from `"JFK"`,
   lexicographically smallest (LeetCode 332).
