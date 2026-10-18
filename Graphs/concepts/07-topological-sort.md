# Concept 07 — Topological Sort

## Quick Card

A **topological order** of a **directed** graph is an ordering of all nodes such
that for every edge `u -> v`, `u` comes **before** `v` in the ordering. Only
possible when the graph is a **DAG** (Directed Acyclic Graph) — any cycle makes
it impossible (you'd need a node before itself).

Two ways to build one:

```python
from collections import deque

# --- Kahn's algorithm (BFS) ---
def topo_sort_kahn(graph, indegree, n):
    q = deque(node for node in range(n) if indegree[node] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)
    return order if len(order) == n else []       # [] means: not a DAG, no valid order

# --- DFS post-order ---
def topo_sort_dfs(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order = []

    def dfs(node):
        color[node] = GRAY
        for nei in graph[node]:
            if color[nei] == GRAY:
                return False                        # cycle -> no valid order
            if color[nei] == WHITE and not dfs(nei):
                return False
        color[node] = BLACK
        order.append(node)                          # append on FINISH (post-order)
        return True

    for node in range(n):
        if color[node] == WHITE and not dfs(node):
            return []
    return order[::-1]                              # reverse post-order = topo order
```

**Complexity:** `O(V + E)` time, `O(V + E)` space (adjacency list + indegree/
color array + output), for either method.

**Reach for topological sort when:** "prerequisite," "must happen before,"
"build order," "task scheduling with dependencies," "is a valid ordering
possible."

---

## Full tutorial

### 1. The picture

Courses: `0 -> 1` means "0 is a prerequisite of 1" (take 0 before 1).

```
0 -> 1 -> 3
 \        ^
  -> 2 ---/
```

Valid topological orders here: `[0, 1, 2, 3]` or `[0, 2, 1, 3]` — **multiple
valid orders can exist**; the algorithm only needs to find *one*.

### 2. Why it only works on a DAG

If there's a cycle `A -> B -> C -> A`, a valid order would need `A` before `B`
before `C` before `A` — a contradiction. So "does a topological order exist" and
"is this graph acyclic" are **the same question**, which is exactly why
topological sort algorithms double as cycle detectors (`concepts/06`).

### 3. Method 1 — Kahn's algorithm (BFS, indegree-based)

**Intuition:** a node with **indegree 0** (no incoming edges left) has no
unprocessed prerequisite — it's always safe to take it *right now*. Take it,
then "remove" it: decrement the indegree of everything it points to (since one of
their prerequisites is now satisfied). Whenever a node's indegree drops to 0,
it becomes newly safe to take — add it to the queue.

```python
def topo_sort_kahn(graph, indegree, n):
    q = deque(node for node in range(n) if indegree[node] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)
    return order if len(order) == n else []
```

**Dry run** on `0->1, 0->2, 1->3, 2->3`:

`indegree = {0:0, 1:1, 2:1, 3:2}`. `q = [0]` (only node 0 starts at indegree 0).

| pop | order so far | neighbor updates | queue after |
|---|---|---|---|
| 0 | [0] | indeg[1]: 1→0 → enqueue 1; indeg[2]: 1→0 → enqueue 2 | [1, 2] |
| 1 | [0,1] | indeg[3]: 2→1 (not 0 yet) | [2] |
| 2 | [0,1,2] | indeg[3]: 1→0 → enqueue 3 | [3] |
| 3 | [0,1,2,3] | no neighbors | [] |

`len(order) == 4 == n` → valid order `[0, 1, 2, 3]`. If instead the graph had a
cycle, some node's indegree would never reach 0, the queue would empty early, and
`len(order) < n` — that's your "impossible" signal.

### 4. Method 2 — DFS post-order

**Intuition:** if you fully finish exploring everything reachable from a node
before you finish the node itself (post-order — `concepts/04`), then by the time
a node is marked "done," every node *it depends on downstream* is already in the
output. Collecting nodes in **finish order** and then **reversing** the list
gives a valid topological order (a node always finishes *after* everything below
it, so reversing puts it — correctly — before them).

```python
def topo_sort_dfs(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order = []

    def dfs(node):
        color[node] = GRAY
        for nei in graph[node]:
            if color[nei] == GRAY:
                return False
            if color[nei] == WHITE and not dfs(nei):
                return False
        color[node] = BLACK
        order.append(node)          # POST-order: added when fully done
        return True

    for node in range(n):
        if color[node] == WHITE and not dfs(node):
            return []
    return order[::-1]
```

**Dry run**, same graph `0->1, 0->2, 1->3, 2->3`, starting `dfs(0)`:

`dfs(0)` → gray. Visit `1`: `dfs(1)` → gray. Visit `3`: `dfs(3)` → gray, no
neighbors, mark black, `order=[3]`. Back in `dfs(1)`: mark black, `order=[3,1]`.
Back in `dfs(0)`: visit `2`: `dfs(2)` → gray. Visit `3` — already **black**,
skip (not a cycle, just already done). Mark `2` black, `order=[3,1,2]`. Back in
`dfs(0)`: mark black, `order=[3,1,2,0]`.

Reverse: `[0, 2, 1, 3]` — a **different** valid order than Kahn's gave
(`[0,1,2,3]`), and that's fine — both are correct; topological order isn't
unique.

### 5. Kahn's vs DFS post-order — which to use

| | Kahn's (BFS) | DFS post-order |
|---|---|---|
| Natural for | "peel off what's ready" framing, explicit indegree tracking | when you're already doing a DFS for another reason |
| Cycle detection | `len(order) != n` | a gray node re-encountered |
| Extra state | an `indegree` array | a 3-color array + recursion |
| Most common in interviews | slightly more common — reads very naturally as "process what's unblocked" | equally valid, sometimes preferred when recursion is already in play |

Both are `O(V+E)`. Pick whichever matches how you're already thinking about the
problem; we default to **Kahn's** as primary in this repo's Course Schedule
family for its very direct "remove what's ready, repeat" narration.

### 6. A special variant — leaf-peeling (preview of Minimum Height Trees)

Kahn's algorithm generalizes beautifully to **undirected trees**: instead of
"remove indegree-0 nodes," you **repeatedly remove all current leaves** (degree
`1` nodes) layer by layer, like peeling an onion. The **last node(s) left
standing** are the tree's centroid(s) — this is exactly how Minimum Height Trees
(Group 06, supplementary) finds the root(s) that minimize tree height. Full
detail lives in that problem's file; the shape of the algorithm (BFS peeling by
degree, layer by layer) is identical to Kahn's.

### 7. Complexity — derived

- Build adjacency list + indegree array: `O(V + E)`.
- Kahn's: each node enqueued once (`O(V)`), each edge examined once when
  decrementing indegree (`O(E)`) → `O(V + E)`.
- DFS post-order: each node visited once, each edge examined once → `O(V + E)`.
- Space: adjacency list `O(V+E)`, indegree/color array `O(V)`, output `O(V)`.

### 8. Problems in this repo that drill topological sort

Course Schedule (does a valid order exist), Course Schedule II (return the
order), Alien Dictionary (build the edges from word comparisons, then sort the
alphabet), Minimum Height Trees (leaf-peeling variant), Longest Increasing Path
in a Matrix (an implicit DAG + memoization, conceptually related).
