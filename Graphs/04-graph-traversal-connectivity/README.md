# Group 04 — Graph Traversal / Connectivity (non-grid)

## What this pattern is

Your first graph that **isn't a grid**. There's no 2D array of cells — instead
you're handed a list of **edges** (pairs of node ids), and you must build the
graph yourself before you can traverse it. Everything else — BFS/DFS, `seen`
sets — is exactly `concepts/03`/`concepts/04`, just on a different shape of data.

## How to recognize it

- Input is a list of edges (`[u, v]` pairs), or `n` nodes numbered `0..n-1` plus
  an edge list — **not** a 2D grid.
- The question is a plain reachability/connectivity check: "is there a path from
  A to B?", "are these two nodes in the same group?"
- No weights, no "shortest", just **yes/no** or **which group**.

## The two steps every non-grid graph problem starts with

1. **Build an adjacency list** (`concepts/02`):
   ```python
   from collections import defaultdict
   graph = defaultdict(list)
   for u, v in edges:
       graph[u].append(v)
       graph[v].append(u)          # drop this line if the graph is directed
   ```
2. **Run one BFS or DFS** from the relevant start node(s), exactly like
   `concepts/03`/`concepts/04`, using `graph[node]` in place of "the 4 grid
   neighbors."

## Complexity

- **Time:** `O(V + E)` — build the adjacency list in `O(E)`, then one traversal
  in `O(V + E)`.
- **Space:** `O(V + E)` for the adjacency list, `O(V)` for `seen` and the
  frontier.

## Problems

1. `01-find-if-path-exists-in-graph.md` — the simplest possible version: one
   BFS/DFS (or one Union-Find), does node `source` reach node `destination`?
   (LeetCode 1971).
