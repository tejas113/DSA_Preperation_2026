# Concept 10 — Dijkstra's Algorithm

## Quick Card

**Shortest path from one source to every node, when edge weights are
non-negative.** BFS finds shortest paths when every edge costs `1`; Dijkstra
generalizes it to arbitrary non-negative weights by replacing the FIFO queue with
a **min-heap** that always expands the cheapest-so-far node.

```python
import heapq

def dijkstra(graph, src, n):                 # graph[u] = list of (v, weight)
    dist = [float("inf")] * n
    dist[src] = 0
    heap = [(0, src)]                          # (cost so far, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                           # stale entry -> skip
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

**Why it works:** the first time a node is popped from the heap, its distance is
**final** — because every other unfinished path to it goes through some
not-yet-popped node whose cost is already `≥` this one, and edges only add
non-negative weight, so no cheaper route can exist. This is why **negative edges
break Dijkstra** (a later, negative edge could undercut a "finalized" distance) —
use Bellman-Ford (`concepts/11`) then.

**Complexity:** `O((V + E) log V)` with a binary heap. `O(V + E)` space.

**The "skip stale entries" idiom:** a node can be pushed to the heap several
times (once per improvement). When you pop one, `if d > dist[u]: continue` throws
away the outdated copies. (Alternative: a `visited` set — pop, skip if visited,
else mark visited and relax.)

**Reach for Dijkstra when:** "shortest / cheapest / fastest" + weighted edges +
**no negative weights**. Variants: minimize the **maximum** edge on a path
(swap `d + w` for `max(d, w)`), or count shortest paths alongside.

---

## Full tutorial

### 1. From BFS to Dijkstra

BFS processes nodes in order of *hop count* because the FIFO queue keeps them
sorted by distance automatically (every edge = 1). With weights, that ordering
breaks — a 1-hop path can cost more than a 3-hop path. Dijkstra fixes it by
**explicitly** always processing the least-cost unfinished node, using a
min-heap.

| | BFS | Dijkstra |
|---|---|---|
| Frontier structure | FIFO queue (`deque`) | min-heap (`heapq`) |
| Order nodes finalize | by hop count | by total path cost |
| Edge weights | all `1` (implicit) | any non-negative |
| Time | `O(V + E)` | `O((V + E) log V)` |

### 2. The relaxation step

"Relaxing" edge `(u, v, w)` means: *if going to `v` via `u` is cheaper than the
best known path to `v`, record the improvement.*

```python
nd = dist[u] + w
if nd < dist[v]:
    dist[v] = nd
    heapq.heappush(heap, (nd, v))
```

Every push is a "candidate" better path. The heap serves them cheapest-first.

### 3. Why the first pop of a node is final (non-negative weights only)

When you pop `(d, u)`, every node still in the heap has cost `≥ d`. Any
alternative path to `u` must leave the "finalized" set through one of those
nodes, so it already costs `≥ d`, and the remaining edges only add `≥ 0`. Hence
no path to `u` can beat `d` — it's optimal.

Add **one negative edge** and this collapses: a not-yet-explored negative edge
could reduce a path you already declared final. That's the whole reason
Bellman-Ford exists.

### 4. Two ways to handle "a node is in the heap multiple times"

**Lazy deletion (our default):**

```python
d, u = heapq.heappop(heap)
if d > dist[u]:
    continue          # this copy is stale; the good one was processed already
```

**Visited set:**

```python
if u in done:
    continue
done.add(u)
```

Both are correct; lazy deletion is one line and doesn't need an extra set. The
heap can hold up to `O(E)` entries either way.

### 5. Dry run

Graph: `0→1 (4)`, `0→2 (1)`, `2→1 (2)`, `1→3 (1)`, `2→3 (5)`. Source `0`.

```
dist = [0, inf, inf, inf]   heap = [(0,0)]
```

| pop | d>dist? | relax | dist after | heap after |
|---|---|---|---|---|
| (0,0) | no | 1: 0+4=4 < inf ✓ ; 2: 0+1=1 < inf ✓ | [0,4,1,inf] | [(1,2),(4,1)] |
| (1,2) | no | 1: 1+2=3 < 4 ✓ ; 3: 1+5=6 < inf ✓ | [0,3,1,6] | [(3,1),(4,1),(6,3)] |
| (3,1) | no | 3: 3+1=4 < 6 ✓ | [0,3,1,4] | [(4,1),(4,3),(6,3)] |
| (4,1) | **yes** (4 > dist[1]=3) | skip (stale) | — | [(4,3),(6,3)] |
| (4,3) | no | 3 has no out-edges | — | [(6,3)] |
| (6,3) | **yes** (6 > dist[3]=4) | skip | — | [] |

Final `dist = [0, 3, 1, 4]`. Shortest `0→1` is `0→2→1` = 3, not the direct
edge 4. The stale `(4,1)` and `(6,3)` were harmlessly skipped.

### 6. Variant A — minimize the *maximum* edge on the path

Some problems (Swim in Rising Water, Path With Minimum Effort) want "the path
whose largest single step is as small as possible," not "the path with the
smallest total." Dijkstra still works — change the cost combine from `+` to
`max`:

```python
nd = max(d, w)            # cost of a path = its heaviest edge
if nd < cost[v]:
    cost[v] = nd
    heapq.heappush(heap, (nd, v))
```

The first-pop-is-final argument still holds because `max` is monotonic and
non-decreasing along a path.

### 7. Variant B — count the shortest paths

Track `ways[v]` alongside `dist[v]`:

```python
if nd < dist[v]:
    dist[v] = nd
    ways[v] = ways[u]
    heapq.heappush(heap, (nd, v))
elif nd == dist[v]:
    ways[v] = (ways[v] + ways[u]) % MOD
```

(Number of Ways to Arrive at Destination, Group 10.)

### 8. Multi-source Dijkstra

Push **all** sources into the heap at cost `0` (or their individual starting
costs) before the loop — same as multi-source BFS, but weighted. Computes each
node's distance to the *nearest* source.

### 9. Complexity — how to say it

> "Binary-heap Dijkstra: each of the `V` nodes is popped and finalized once
> (`O(V log V)`), and each of the `E` edges triggers at most one heap push
> (`O(E log V)`), so `O((V + E) log V)` total. Space is `O(V)` for `dist` plus
> `O(E)` for heap entries."

(A Fibonacci heap gives `O(E + V log V)` — mention it exists, don't implement
it.)

### 10. Common bugs

- [ ] **Using it with negative edges** — silently wrong. Use Bellman-Ford.
- [ ] **No stale check** — still correct, but you re-relax finalized nodes;
      wasteful, and on some inputs blows the time budget.
- [ ] **Marking a node done at push time instead of pop time** — you might
      finalize it before its cheapest path is found. (Exception: it's safe *only*
      when the cost of *entering* a node doesn't depend on which predecessor you
      came from — e.g. Swim in Rising Water, where the entering cost is the
      destination cell's own value. For plain `+` Dijkstra and Path With Minimum
      Effort, mark at pop.)
- [ ] **`dist` not initialized to infinity** (or the source not to `0`).
- [ ] **Pushing `(node, cost)` instead of `(cost, node)`** — the heap orders by
      the first tuple element; cost must come first.
- [ ] **Forgetting unreachable nodes** — they stay at `inf`; translate that to
      whatever the problem wants (`-1`, etc.).

### 11. Problems in this repo that drill Dijkstra

Network Delay Time (classic sum, Group 10), Swim in Rising Water & Path With
Minimum Effort (minimize-max variant, Group 10), Number of Ways to Arrive at
Destination (path counting, Group 10), Cheapest Flights Within K Stops (Group 11
— why plain Dijkstra *fails* there), Min Cost to Connect All Points (Prim's MST
is Dijkstra-shaped, Group 12).
