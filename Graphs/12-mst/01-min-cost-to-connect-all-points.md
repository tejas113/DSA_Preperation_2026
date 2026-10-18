# Min Cost to Connect All Points  ·  LeetCode 1584  ·  Medium

Group 12 — Minimum Spanning Tree  ·  points on a plane, every pair connectable at
Manhattan-distance cost — a **complete graph**, so **Prim** is the natural fit.

Prereqs: `concepts/14-mst-kruskal-prim.md`, `concepts/10-dijkstra.md` (Prim is
Dijkstra-shaped), `concepts/08-union-find.md` (for the Kruskal alternative).

---

## 1. Problem

Given `points`, where `points[i] = [xi, yi]` on a 2D plane. The cost to connect
two points is the **Manhattan distance**: `|xi - xj| + |yi - yj|`.

**Return the minimum total cost to connect all points** so that there is exactly
one simple path between any two of them (i.e. build a spanning tree).

Constraints:
- `1 <= points.length <= 1000`.
- `-10^6 <= xi, yi <= 10^6`. All points are distinct.

Example 1:

```
points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
answer = 20
# edges: (0,0)-(2,2)=4, (2,2)-(3,10)=9, (2,2)-(5,2)=3, (5,2)-(7,0)=4  ->  4+9+3+4 = 20
```

Example 2: `points = [[3,12],[-2,5],[-4,1]]` → `18`.

---

## 2. Explain Like I'm 5

You have some houses on a map and you want to lay cable so **every house is
connected to every other house** (directly or through others). Cable between two
houses costs the walking distance (blocks north/south + blocks east/west).

You want the **cheapest total length of cable**. You don't have to connect every
pair directly — just enough cable so the whole neighborhood is one connected
network with no wasteful loops.

The greedy trick: keep one growing blob of connected houses. Each step, add the
**single cheapest cable** that reaches a house *not yet in the blob*. Repeat until
every house is in.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Connect **all** points/houses/nodes at **minimum total cost**" | ✅ → MST |
| You choose which connections to build; you pay the sum | ✅ |
| **Every** pair is connectable (a complete graph, defined by geometry) | ✅ → **Prim** (don't materialize all `n²` edges) |
| Not "shortest path from A to B" | ✅ — MST is "wire the whole thing together" |

**Reduce it to:** *"Minimum Spanning Tree of the complete graph on the points,
edge weight = Manhattan distance. Use Prim with a heap: grow one tree, always add
the cheapest edge to an outside point."*

---

## 4. Intuition

1. The points form a **complete graph**: every pair has an edge, weight =
   Manhattan distance. `n ≤ 1000` → `~500,000` edges.
2. You want the cheapest set of `n - 1` edges that connects everything with no
   cycle — an MST.
3. **Prim** grows one tree: start with point `0`, and repeatedly pull in the
   nearest not-yet-connected point (by the cheapest single edge). The *cut
   property* guarantees each such edge is safe (it's the cheapest across the cut
   between "in the tree" and "not in the tree").
4. Prim is **Dijkstra with a different heap key**: Dijkstra's key is "total path
   cost to reach a node"; Prim's key is just "the weight of one edge connecting a
   node to the tree."
5. Kruskal also works (sort all `~500k` edges + Union-Find), but Prim doesn't
   need to build and sort the whole edge list — better for a dense/complete
   graph.

---

## 5. Approach (primary): Prim with a min-heap

1. `n = len(points)`. If `n <= 1`: return `0`.
2. `dist(i, j) = |xi - xj| + |yi - yj|`.
3. `seen = {0}`. `heap = [(dist(0, j), j) for j in 1..n-1]`; heapify.
4. While `len(seen) < n`:
   - Pop `(w, u)`. If `u in seen`, skip (stale).
   - `seen.add(u)`; `total += w`.
   - For every `v not in seen`: push `(dist(u, v), v)`.
5. Return `total`.

Builds on: `concepts/14` Prim template, `concepts/10` (Dijkstra-shaped heap
loop, mark-at-pop).

---

## 6. Pseudocode

```
function minCostConnectPoints(points):
    n = len(points)
    if n <= 1: return 0

    seen = {0}
    heap = [(dist(0, j), j) for j in 1..n-1]
    total = 0

    while size(seen) < n:
        (w, u) = pop-min heap
        if u in seen: continue
        add u to seen
        total += w
        for v in 0..n-1 not in seen:
            push (dist(u, v), v)

    return total
```

---

## 7. Dry Run

```
points = [[0,0],[2,2],[3,10],[5,2],[7,0]]   (label them 0..4)
```

Manhattan distances from each point (only what we need):

```
d(0,1)=4  d(0,2)=13  d(0,3)=7  d(0,4)=7
d(1,2)=9  d(1,3)=3   d(1,4)=7
d(3,2)=10 d(3,4)=4
```

Start `seen = {0}`, heap = `[(4,1),(13,2),(7,3),(7,4)]`, `total = 0`.

| pop | in seen? | seen after | total | push (v not in seen) |
|---|---|---|---|---|
| (4, 1) | no | {0,1} | 4 | (9,2), (3,3), (7,4) |
| (3, 3) | no | {0,1,3} | 7 | (10,2), (4,4) |
| (4, 4) | no | {0,1,3,4} | 11 | (d(4,2)=13, 2) |
| (7, 4) | **yes** | — | — | (stale, skip) |
| (9, 2) | no | {0,1,2,3,4} | 20 | — (all seen) |

`len(seen) == 5 == n` → return **20**. ✅

---

## 8. Python Code (primary — Prim with a heap)

```python
import heapq
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        def dist(i: int, j: int) -> int:
            return abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])

        seen = {0}
        heap = [(dist(0, j), j) for j in range(1, n)]
        heapq.heapify(heap)
        total = 0

        while len(seen) < n:
            w, u = heapq.heappop(heap)
            if u in seen:
                continue                         # stale edge to an already-connected point
            seen.add(u)
            total += w
            for v in range(n):
                if v not in seen:
                    heapq.heappush(heap, (dist(u, v), v))

        return total


if __name__ == "__main__":
    sol = Solution()

    assert sol.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
    assert sol.minCostConnectPoints([[3, 12], [-2, 5], [-4, 1]]) == 18
    assert sol.minCostConnectPoints([[0, 0]]) == 0
    assert sol.minCostConnectPoints([[0, 0], [1, 1]]) == 2
    assert sol.minCostConnectPoints([[-1000000, -1000000], [1000000, 1000000]]) == 4000000
    assert sol.minCostConnectPoints([[0, 0], [1, 0], [2, 0], [3, 0]]) == 3   # collinear -> a chain

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Prim without a heap — `O(n²)` (best constant for a complete graph)

Maintain `min_dist[v]` = cheapest edge connecting `v` to the current tree. Each
of `n` iterations: scan for the unvisited `v` with the smallest `min_dist`, add
it, then update `min_dist` for all others against the new node.

```python
def minCostConnectPoints(self, points):
    n = len(points)
    INF = float("inf")
    min_dist = [INF] * n
    min_dist[0] = 0
    in_tree = [False] * n
    total = 0

    for _ in range(n):
        u = min((v for v in range(n) if not in_tree[v]), key=lambda v: min_dist[v])
        in_tree[u] = True
        total += min_dist[u]
        for v in range(n):
            if not in_tree[v]:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if d < min_dist[v]:
                    min_dist[v] = d
    return total
```

No heap, no log factor: `O(n²)`. For `n ≤ 1000` (`10^6` ops) this is the fastest
and simplest.

### 9b. Kruskal — sort all edges + Union-Find

```python
def minCostConnectPoints(self, points):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((w, i, j))
    edges.sort()

    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, used = 0, 0
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            total += w
            used += 1
            if used == n - 1:
                break
    return total
```

`O(n² log n)` — has to build and sort all `~500k` edges. Fine here, but Prim
avoids materializing the full edge list.

### The BFS↔DFS answer the interviewer wants

> "It's an MST of the complete graph on the points, weights = Manhattan distance.
> Prim fits a complete graph best — grow one tree from a heap, always add the
> cheapest edge to an outside point, `O(n² log n)`, or `O(n²)` with a plain
> `min_dist` array and no heap. Kruskal works too but has to sort all `n²`
> edges."

---

## 10. Complexity — derived step by step

**V and E:** `V = n` points; `E = n(n-1)/2 = O(n²)` (complete graph).

**Time (heap Prim):**
- Each point is finalized once when popped (`O(n log ...)`).
- Each time a point joins the tree, we push edges to all `≤ n` outside points →
  `O(n²)` pushes total, each `O(log)` → **`O(n² log n)`**.

Prim without a heap (9a): `O(n²)`. Kruskal (9b): `O(n² log n)` (edge sort
dominates).

**Space:**
- Heap holds up to `O(n²)` entries. `seen`: `O(n)`.
- **Total: `O(n²)`** (heap version). `O(n)` for the no-heap version.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `n = 1` (or `0`) | `if n <= 1: return 0` |
| `n = 2` | one edge = the Manhattan distance between the two points |
| Collinear points | MST is a chain along the line — handled normally |
| Points far apart (coords `±10^6`) | Manhattan distances up to `4·10^6`, total up to `~4·10^9` — fits a Python int / int64 |
| All points distinct (guaranteed) | no zero-weight edges to worry about |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Manhattan distance wrong** — it's `abs(dx) + abs(dy)`, **not**
      `abs(dx + dy)` and not the Euclidean `sqrt(dx² + dy²)`.
- [ ] **Prim: marking a node `seen` at push time instead of pop time** — can
      lock in a non-cheapest edge (same subtlety as Dijkstra).
- [ ] **Prim: no `if u in seen: continue`** on pop — you'd re-add points and
      overcount `total`.
- [ ] **Kruskal: generating both `(i,j)` and `(j,i)`** — use `j in range(i+1,
      n)`.
- [ ] **Kruskal: adding an edge without checking `find(i) != find(j)`** — builds
      cycles, overpays.
- [ ] **Forgetting `n <= 1 → 0`** — an empty heap / immediate loop exit can
      still be fine, but be explicit.
- [ ] **Heap tuple order** — `(weight, node)`, weight first.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **"Connect everything at minimum total cost" = MST.** Greedy, provably
   optimal (cut property). Not shortest path.
2. **Complete / geometric graph → Prim** (grow one tree from a heap, don't
   materialize all `n²` edges). **Sparse / explicit edge list → Kruskal** (sort +
   Union-Find).
3. **Prim ≈ Dijkstra** with the heap key = "weight of one edge to reach a node"
   instead of "accumulated path cost."
4. **MST edge count is always `V - 1`** — a useful sanity check and stop
   condition.

| Problem | How this transfers |
|---|---|
| "Connect all islands at min cost" (Making a Large Island scenario) | MST over islands; edge weight = bridging distance |
| Network / pipeline / power-grid design | MST directly |
| Single-linkage clustering into `k` groups | build the MST, then cut the `k - 1` heaviest edges |
| Minimum bottleneck spanning tree | the MST also minimizes the largest edge on any node-to-node path |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Cost is **Euclidean** distance, not Manhattan."

- **(b) Pattern:** the MST algorithm is unchanged — only the `dist` function.
- **(c) Adapt:** `dist(i, j) = sqrt(dx² + dy²)` (or compare squared distances to
  stay in integers, since `sqrt` is monotonic — but the *total* needs the real
  distances). Prim/Kruskal otherwise identical. For very large `n`, a Euclidean
  MST can be found in `O(n log n)` via **Delaunay triangulation** (which has only
  `O(n)` edges and is guaranteed to contain the MST).
- **(d) Say:** "Swap the distance function. And for huge `n`, the Euclidean MST
  lives inside the Delaunay triangulation, giving an `O(n log n)` route instead
  of `O(n²)`."

### Scenario 2 — "Some pairs are **already connected for free** (a list of pre-existing links)."

- **(b) Pattern:** pre-merge the free connections, then MST the rest.
- **(c) Adapt:** **Kruskal:** initialize the Union-Find by `union`-ing every free
  pair (cost `0`), then run Kruskal on the remaining edges as usual — it'll skip
  any edge whose endpoints are already connected via free links. **Prim:** seed
  `seen` with a whole free-connected component and push its boundary edges.
- **(d) Say:** "Free edges are just edges of weight `0` — union them first, then
  the MST fills in the cheapest way to link the remaining components."

### Scenario 3 — "`n` is `10^5` points."

- **(b) Pattern:** `O(n²)` (`10^10`) is too slow — the *complete* graph is the
  problem, not the algorithm.
- **(c) Adapt:** for **Manhattan** distance specifically, the MST needs at most
  `O(n)` candidate edges: for each point, only its nearest neighbor in each of a
  few directional regions (octants) can be an MST edge. Generate those `O(n)`
  edges (with a sweep + sorted structure, `O(n log n)`), then run Kruskal on
  them. This is the **Manhattan MST** algorithm.
- **(d) Say:** "The blow-up is the `n²` edges, not the MST. For Manhattan
  distance you only need each point's nearest neighbor per octant — `O(n)`
  candidate edges, then Kruskal, all in `O(n log n)`."

### Scenario 4 — "Return **which edges** the MST uses, not just the total cost."

- **(b) Pattern:** track the chosen edges.
- **(c) Adapt:** **Prim:** when you pop `(w, u)` and add `u`, also record which
  in-tree node `u` connected to (store a `from` alongside each heap entry).
  **Kruskal:** collect `(i, j)` every time `union` succeeds. Either way you get
  the `n - 1` MST edges.
- **(d) Say:** "Hang the source node on each heap entry (Prim) or collect
  successful unions (Kruskal) — the MST edge set drops out."

### Scenario 5 — "Points are **added one at a time**; keep the MST current."

- **(b) Pattern:** dynamic MST — genuinely hard.
- **(c) Adapt:** adding a point adds `n` new candidate edges. Its cheapest
  connection to the existing tree, plus the cycle that would form, means at most
  one existing MST edge gets swapped out for a new one (the heaviest edge on the
  cycle the new edge closes). Maintaining this in `O(log n)` per insertion needs
  a **link-cut tree** (dynamic tree). Without that, recompute (`O(n²)` or
  `O(n log n)` for Manhattan).
- **(d) Say:** "Each new point either extends the tree or replaces the heaviest
  edge on the cycle it creates — `O(log n)` per update with link-cut trees,
  otherwise recompute."

### Scenario 6 — "You may leave up to `K` points in separate networks (build a spanning **forest** with `K + 1` trees) to minimize cost."

- **(b) Pattern:** stop the MST early / cut the heaviest edges.
- **(c) Adapt:** run Kruskal but **stop after adding `n - 1 - K` edges** (leaving
  `K + 1` components). Equivalently: build the full MST, then **remove the `K`
  heaviest** of its `n - 1` edges. This is exactly single-linkage clustering into
  `K + 1` clusters.
- **(d) Say:** "Allowing `K` disconnections = Kruskal stopping `K` edges early,
  or dropping the `K` heaviest MST edges — that's single-linkage clustering."

---

## 15. Flashcards

**Q:** What kind of problem is "connect all points at minimum total cost"?
**A:** Minimum Spanning Tree. Greedy, provably optimal (cut property). **Not**
shortest path.

**Q:** Complete/geometric graph vs sparse edge list — which MST algorithm?
**A:** Complete/dense → **Prim** (grow one tree from a heap, don't materialize
`n²` edges). Sparse/explicit edges → **Kruskal** (sort + Union-Find).

**Q:** How is Prim related to Dijkstra?
**A:** Same heap loop; Prim's key is "weight of one edge to reach a node,"
Dijkstra's is "accumulated path cost to a node."

**Q:** Manhattan distance formula?
**A:** `|x1 - x2| + |y1 - y2|` — `abs(dx) + abs(dy)`, not `abs(dx + dy)`, not
Euclidean.

**Q:** Time and space (heap Prim on `n` points)?
**A:** `O(n² log n)` time, `O(n²)` space (heap). Plain `min_dist`-array Prim:
`O(n²)` time, `O(n)` space.

**Q:** How many edges does an MST have?
**A:** Exactly `V - 1` — a stop condition and a sanity check.

**Q:** `n = 10^5` — what saves you?
**A:** The Manhattan MST trick: only each point's nearest neighbor per octant can
be an MST edge → `O(n)` candidate edges → Kruskal → `O(n log n)`.

**Q:** Leave `K` points disconnected to minimize cost?
**A:** Kruskal, stop after `n - 1 - K` edges (= drop the `K` heaviest MST
edges). Same as single-linkage clustering into `K + 1` clusters.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Prim with a heap, but building an **explicit
adjacency list** of all `n²` edges up front (the primary computes distances
on the fly). `O(n² log n)` time.

```python
class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        adj = defaultdict(list)
        n = len(points)

        for i in range(n):
            for j in range(i + 1, n):
                dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                adj[i].append((dist, j))
                adj[j].append((dist, i))

        seen = set()
        heap = [[0, 0]]
        total_cost = 0

        while heap and len(seen) < n:
            dist, u = heapq.heappop(heap)
            if u in seen:
                continue
            seen.add(u)
            total_cost += dist
            for weight, v in adj[u]:
                if v not in seen:
                    heapq.heappush(heap, (weight, v))
        return total_cost
```

**Correct** — verified against all the section-8 tests (5-point example,
3-point example, `n=1`, `n=2`, collinear).

**Two small notes (neither breaks it):**

1. **Explicit adjacency list = `O(n²)` extra memory.** For `n = 1000` that's
   ~1M `(dist, node)` pairs across the `adj` lists. The primary solution's
   `dist(i, j)` helper computes the same numbers on demand for `O(n)` space.
   Both are `O(n² log n)` time; at this `n` the memory is fine, but computing
   on the fly is the leaner habit for a complete graph.
2. **`heap = [[0, 0]]` (a list) mixed with `(weight, v)` tuple pushes.** In
   Python 3, comparing a `list` to a `tuple` raises `TypeError` — this only
   *doesn't* blow up because the initial `[0, 0]` is popped before any tuple is
   ever pushed, so the heap never has to compare the two types. It works by
   ordering luck. Use `heap = [(0, 0)]` (a tuple) to be safe.
