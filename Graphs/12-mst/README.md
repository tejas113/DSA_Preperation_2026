# Group 12 — Minimum Spanning Tree

## What this pattern is

Connect **all** nodes with the **cheapest possible set of edges** — a spanning
tree (`V - 1` edges, connected, acyclic) of minimum total weight.

Full mechanics: `concepts/14-mst-kruskal-prim.md`.

## How to recognize it

- "Connect all points / cities / computers / houses at **minimum total cost**."
- "Cheapest network of wires / pipes / roads that links everything."
- You're free to choose *which* connections to build, and you pay the sum of what
  you build.
- **Not** shortest path (that's one source to one target). MST is "cheapest way
  to wire the whole thing together."

## Two algorithms

- **Kruskal** — sort all edges, add the cheapest that doesn't form a cycle
  (Union-Find). `O(E log E)`. Best for **sparse** graphs / explicit edge lists.
- **Prim** — grow one tree from a heap, always adding the cheapest edge leaving
  it (Dijkstra-shaped). `O(E log V)`. Best for **dense** graphs, especially a
  complete graph.

## Complexity

`O(E log E)` (Kruskal) or `O(E log V)` (Prim). For a complete graph on `n` nodes
(`E = n²`), both are `O(n² log n)`; Prim with an adjacency matrix is `O(n²)`.

## Problems

1. `01-min-cost-to-connect-all-points.md` — points on a plane, edge weight =
   Manhattan distance between every pair (a **complete graph**, `E = n²`), so
   **Prim** is the natural fit (LeetCode 1584).
