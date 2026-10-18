# Concept 05 — Connected Components ("how many separate groups?")

## Quick Card

A **connected component** is a maximal group of nodes where every node can reach
every other node in the group. A graph can have several components (separate
"islands" of nodes).

**Counting components:** loop over all nodes; each time you find one that isn't
visited yet, that's a **new** component — run one BFS/DFS from it to mark the whole
group, then keep looping.

```python
seen = set()
components = 0
for node in all_nodes:
    if node not in seen:
        components += 1
        flood(node, seen)        # BFS or DFS that marks the entire component
```

**Complexity:** `O(V + E)` total. The outer loop is `O(V)`; the floods together
visit every node and edge exactly once, `O(V + E)`.

**This is the skeleton behind:** Number of Islands, Max Area of Island, Number of
Provinces, Number of Connected Components, and (with union-find instead of flood)
most of Group 07.

---

## Full tutorial

### 1. The picture

```
0 - 1        3 - 4        6
    |        |
    2        5

component A: {0, 1, 2}
component B: {3, 4, 5}
component C: {6}          (a lone node is its own component)

count = 3
```

### 2. Why the "loop + flood" skeleton works

- The **outer loop** guarantees you *start* a search from every part of the graph,
  even parts disconnected from where you began. Without it you'd only count the one
  component containing node 0.
- The **`if node not in seen`** guard guarantees you only *count* a component once.
  The first node you hit from a fresh component triggers `components += 1`; the
  flood then marks the rest so they're skipped.
- The **flood** (BFS or DFS — your choice, both `O(size of component)`) marks every
  node reachable from the trigger node.

### 3. The generic template (works for any graph shape)

```python
from collections import deque

def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    seen = set()
    components = 0

    def bfs(start):
        q = deque([start])
        seen.add(start)
        while q:
            node = q.popleft()
            for nei in graph[node]:
                if nei not in seen:
                    seen.add(nei)
                    q.append(nei)

    for node in range(n):          # <-- iterate ALL node ids, not just graph keys
        if node not in seen:
            components += 1
            bfs(node)

    return components
```

> Use `range(n)` (all node ids) for the outer loop, not `for node in graph`. A node
> with no edges never appears as a key in a `defaultdict`, but it's still its own
> component.

### 4. The grid version (Number of Islands)

On a grid the "nodes" are cells and "edges" are adjacency. The skeleton is the
same, the outer loop is a double `for` over cells:

```python
count = 0
for r in range(m):
    for c in range(n):
        if grid[r][c] == "1" and (r, c) not in seen:
            count += 1
            flood(r, c)            # DFS/BFS that sinks the whole island
```

### 5. Variations you'll meet

| Problem wants | Change to the skeleton |
|---|---|
| **count** components | `components += 1` per fresh start (base case) |
| **largest** component size | `flood` returns its size; keep a running `max` |
| **all** components listed | `flood` collects nodes into a list; append that list to a result |
| components after **adding edges one at a time** | use **union-find** instead (`concepts/08`), start `count = n`, `count -= 1` on each successful `union` |
| number of edges to **add** to connect everything | `components - 1` |

### 6. Union-Find gives the same answer differently

Flood fill answers "how many components" by *searching*. Union-Find answers it by
*merging*: start with `n` components, and every time you `union` two nodes that
were in different groups, the count drops by 1.

```python
dsu = DSU(n)
count = n
for u, v in edges:
    if dsu.union(u, v):     # returns True only if they were separate
        count -= 1
```

Pick union-find when edges arrive **incrementally** or you need to answer
connectivity queries *during* the process (Group 07). Pick flood fill when you have
the whole graph up front and just want one final count (Groups 01, 04).

### 7. Dry run — count components

`n = 5`, `edges = [(0,1), (1,2), (3,4)]`.

```
graph: 0:[1]  1:[0,2]  2:[1]  3:[4]  4:[3]
```

| outer node | in seen? | action | seen after | components |
|---|---|---|---|---|
| 0 | no | components=1; BFS marks 0,1,2 | {0,1,2} | 1 |
| 1 | yes | skip | {0,1,2} | 1 |
| 2 | yes | skip | {0,1,2} | 1 |
| 3 | no | components=2; BFS marks 3,4 | {0,1,2,3,4} | 2 |
| 4 | yes | skip | — | 2 |

Answer: **2**.

### 8. Complexity — line by line

- Build adjacency list: loop over `E` edges → `O(V + E)` space, `O(E)` time.
- Outer loop: exactly `V` iterations → `O(V)`.
- Floods: across the *entire* outer loop, every node is enqueued once and every
  edge is scanned once (twice for undirected) → `O(V + E)` total, **not** `O(V * (V+E))`.
  The `seen` guard is what collapses it.
- **Total time:** `O(V + E)`. Grid: `O(m*n)`.
- **Space:** `seen` `O(V)` + adjacency list `O(V + E)` + queue/stack `O(V)` → `O(V + E)`.
  Grid without adjacency list: `O(m*n)`.

### 9. Pitfalls checklist

- [ ] Outer loop covers **all** node ids (isolated nodes count).
- [ ] Increment the counter **only** on a fresh (unseen) start.
- [ ] `seen` is shared across all floods (don't reset it per component).
- [ ] Grid: check both `is land` and `not seen` before starting a flood.
- [ ] Don't double count: mark the trigger node seen inside the flood, not just its neighbors.

### 10. Problems in this repo built on this skeleton

Number of Islands, Max Area of Island, Making a Large Island (01); Find if Path
Exists (04, single component check); Number of Provinces, Number of Connected
Components, Graph Valid Tree (07 — via union-find); Accounts Merge (07 — components
of a "shares an email" graph).
