# Concept 14 — Minimum Spanning Tree (Kruskal & Prim)

## Quick Card

A **spanning tree** of a connected graph: pick a subset of edges that connects
**all** `V` nodes with no cycle — exactly `V - 1` edges. A **minimum spanning
tree (MST)** is the spanning tree with the **smallest total edge weight**.

Two standard algorithms:

| | Kruskal | Prim |
|---|---|---|
| Idea | sort **all edges**, add the cheapest that doesn't make a cycle | grow **one tree** outward, always adding the cheapest edge leaving it |
| Structure | sort + **Union-Find** | **min-heap** (Dijkstra-shaped) |
| Time | `O(E log E)` | `O(E log V)` |
| Best for | **sparse** graphs (few edges), or edges given as a list | **dense** graphs (`E ≈ V²`), especially a complete graph |

```python
# --- Kruskal ---
def kruskal(n, edges):                      # edges = list of (w, u, v)
    dsu = DSU(n)
    edges.sort()
    total, used = 0, 0
    for w, u, v in edges:
        if dsu.union(u, v):                 # returns False if u, v already connected
            total += w
            used += 1
    return total if used == n - 1 else -1   # -1 => graph not connected


# --- Prim (heap) ---
import heapq

def prim(n, adj):                           # adj[u] = list of (v, w)
    seen = {0}
    heap = [(w, v) for v, w in adj[0]]
    heapq.heapify(heap)
    total, count = 0, 1
    while heap and count < n:
        w, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        total += w
        count += 1
        for v, w2 in adj[u]:
            if v not in seen:
                heapq.heappush(heap, (w2, v))
    return total if count == n else -1
```

**Both are greedy and both are provably optimal** (the *cut property*: for any way
of splitting the nodes into two groups, the cheapest edge crossing the split is
in *some* MST).

**Reach for MST when:** "connect all nodes / points / cities at **minimum total
cost**," "cheapest network of cables/pipes/roads that links everything."

---

## Full tutorial

### 1. What "spanning tree" means

- **Spanning:** touches every node.
- **Tree:** connected + acyclic ⟹ exactly `V - 1` edges (from `concepts/08` /
  Graph Valid Tree — any two of {connected, acyclic, `V-1` edges} imply the
  third).

An MST is the cheapest such tree. If the graph isn't connected, no spanning tree
exists (you'd get a spanning *forest*).

### 2. The cut property (why greedy works)

Split the nodes into any two non-empty groups `A` and `B`. Among all edges with
one endpoint in `A` and one in `B` (the "cut"), the **minimum-weight** one is
safe to add — it belongs to at least one MST. Both Kruskal and Prim only ever add
edges that are the cheapest across *some* cut, so they build an MST.

### 3. Kruskal, step by step

1. Sort every edge by weight, ascending.
2. Walk the sorted edges. For each `(u, v)`, if `u` and `v` are **not already
   connected** (`dsu.union(u, v)` returns `True`), take it. If they are, skip it
   (it would close a cycle).
3. Stop when you've taken `V - 1` edges (or run out — then the graph is
   disconnected).

The Union-Find `union`-returns-`False`-on-a-cycle idiom from Group 07 is the
engine. Dry run: edges `(1, 0, 1)`, `(2, 1, 2)`, `(2, 0, 2)`, `(3, 2, 3)`,
`n = 4`.

| edge (sorted) | union? | total | edges used |
|---|---|---|---|
| (1, 0, 1) | `True` | 1 | 1 |
| (2, 1, 2) | `True` | 3 | 2 |
| (2, 0, 2) | `False` — 0,1,2 already connected | 3 | 2 |
| (3, 2, 3) | `True` | 6 | 3 = `n - 1` → done |

MST weight = **6**.

### 4. Prim, step by step

It's Dijkstra with one change: the heap key is the **edge weight to reach a
node**, not the accumulated path cost.

1. Start with node `0` in the tree. Push all its edges `(weight, neighbor)`.
2. Pop the cheapest edge to a node **not yet in the tree**; add that node and
   that edge.
3. Push the new node's edges to outside nodes.
4. Repeat until all `V` nodes are in.

Same dry run: start `{0}`, heap `[(1,1), (2,2)]`.
- pop `(1, 1)` → add node 1, total 1. Push `(2, 2)` (edge 1-2).
- pop `(2, 2)` → add node 2, total 3. Push `(3, 3)` (edge 2-3).
- pop `(2, 2)` (the 0-2 edge) → node 2 already in → skip.
- pop `(3, 3)` → add node 3, total 6. All 4 nodes in → done.

MST weight = **6**. (Same answer — every MST algorithm gives the same total; the
*edge set* can differ if there are ties.)

### 5. Which one to use

- **Complete graph / dense** (`E ≈ V²`), or the graph is defined implicitly by
  points on a plane (every pair has an edge) → **Prim with a heap**:
  `O(E log V) = O(V² log V)`. (Kruskal here is `O(V² log V)` too, dominated by
  sorting `V²` edges — comparable, but Prim doesn't have to materialize all
  `V²` edges up front.)
- **Sparse** (`E ≈ V`), or you're handed an explicit edge list → **Kruskal**:
  `O(E log E)`, and the code is shorter.
- **Very dense, need the absolute best constant** → Prim with an adjacency
  *matrix* and no heap: `O(V²)`.

### 6. MST facts worth knowing

- Every MST has exactly `V - 1` edges.
- If all edge weights are **distinct**, the MST is **unique**.
- The **maximum** spanning tree: negate weights (or sort descending) — same
  algorithms.
- **Minimum bottleneck spanning tree** = the MST also minimizes the *largest*
  edge on the path between any two nodes (ties into the minimize-max problems in
  Group 10).
- Removing the heaviest edge on any cycle never increases the MST cost (the
  *cycle property*).

### 7. Complexity — how to say it

> "Kruskal: sort `E` edges (`O(E log E)`) then a near-linear Union-Find pass
> (`O(E α(V))`), so `O(E log E)`. Prim with a binary heap: each node finalized
> once and each edge pushed once, `O(E log V)`. For a complete graph both are
> `O(V² log V)`; Prim with an adjacency matrix drops to `O(V²)`."

### 8. Common bugs

- [ ] **Kruskal: adding an edge without the `union`-returns-`True` check** — you
      build cycles and overpay.
- [ ] **Prim: marking a node in the tree at *push* time instead of *pop* time** —
      you can lock in a non-cheapest edge (same subtlety as Dijkstra).
- [ ] **Not detecting disconnection** — Kruskal: check you used `V - 1` edges.
      Prim: check all `V` nodes got added.
- [ ] **Heap tuple order** — `(weight, node)`, weight first.
- [ ] **Prim: pushing edges to nodes already in the tree** — harmless (the
      pop-time `if u in seen` skips them) but wasteful; the `if v not in seen`
      guard on push trims it.

### 9. Problems in this repo

Min Cost to Connect All Points (Group 12 — complete graph on plane points, Prim's
natural fit); Redundant Connection / Graph Valid Tree (Group 07 — the Union-Find
building blocks Kruskal reuses); "connect all islands at minimum cost" scenario
in Making a Large Island / Shortest Bridge.
