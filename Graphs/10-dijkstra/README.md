# Group 10 — Dijkstra

## What this pattern is

Shortest path from one source, with **non-negative** edge weights. It's BFS with
the FIFO queue swapped for a **min-heap** that always expands the cheapest-so-far
node.

Full mechanics: `concepts/10-dijkstra.md`.

## How to recognize it

- "Shortest / cheapest / fastest / minimum time" **and** edges have weights.
- **No negative weights** (if there are, or there's a hop limit → Bellman-Ford,
  Group 11).
- Grid variant: a cell's "cost" is its value, and you want the least-cost path
  (or the path minimizing the *largest* cell — the minimize-max variant).

## The template

```python
import heapq

dist = {src: 0}
heap = [(0, src)]
while heap:
    d, u = heapq.heappop(heap)
    if d > dist.get(u, float("inf")):
        continue                              # stale
    for v, w in graph[u]:
        nd = d + w                            # or max(d, w) for the minimize-max variant
        if nd < dist.get(v, float("inf")):
            dist[v] = nd
            heapq.heappush(heap, (nd, v))
```

## Complexity

`O((V + E) log V)` time, `O(V + E)` space.

## Problems

1. `01-network-delay-time.md` — classic sum-of-weights Dijkstra; answer =
   the max finalized distance (LeetCode 743). **Start here.**
2. `02-swim-in-rising-water.md` — grid; minimize the **maximum** cell on the
   path (`max` instead of `+`) (LeetCode 778).
3. `03-path-with-minimum-effort.md` — grid; minimize the **maximum edge
   difference** on the path — the same minimize-max variant (LeetCode 1631).
4. `04-number-of-ways-to-arrive-at-destination.md` *(supplementary)* — Dijkstra
   plus **counting** the shortest paths (LeetCode 1976).
