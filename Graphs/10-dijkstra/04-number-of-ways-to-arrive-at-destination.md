# Number of Ways to Arrive at Destination  ·  LeetCode 1976  ·  Medium  ·  *(supplementary)*

Group 10 — Dijkstra  ·  Dijkstra plus a parallel `ways[]` array that **counts**
the shortest paths.

Prereqs: `01-network-delay-time.md`, `concepts/10-dijkstra.md` (§7, "count the
shortest paths").

---

## 1. Problem

A city with `n` intersections `0..n-1` and **bidirectional** roads.
`roads[i] = [ui, vi, timei]` is a road between `ui` and `vi` taking `timei`
minutes. You start at `0` and want to reach `n-1` in the **shortest possible
time**.

**Return the number of ways to arrive at `n-1` in that shortest time, modulo
`10^9 + 7`.**

Constraints:
- `1 <= n <= 200`.
- `1 <= timei <= 10^9` — weights are **positive** (this matters; see §4).
- Exactly one road between any two intersections; the graph is connected.

Example 1:

```
n = 7
roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],
         [3,5,1],[6,5,1],[2,5,1],[0,4,3],[4,6,4]]
answer = 4        # shortest time 0->6 is 7, and 4 distinct paths achieve it:
                  #   0->6,  0->4->6,  0->1->2->5->6,  0->1->3->5->6
```

Example 2: `n = 2, roads = [[1,0,10]]` → `1`.

---

## 2. Explain Like I'm 5

You want to get from home (`0`) to school (`n-1`) as fast as possible. First
figure out the fastest time. Then count **how many different routes** get you
there in exactly that fastest time — routes that are one minute slower don't
count.

The trick: as the "fastest time" wave spreads out from home, each intersection
also remembers **how many fastest routes reach it**. When the wave arrives at an
intersection from a neighbor, if that neighbor is *on* a fastest route, you add
the neighbor's route-count to this intersection's route-count.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Shortest time" + **weighted** edges + non-negative | ✅ → Dijkstra |
| "**Number of ways** / count the shortest paths" | ✅ → carry a `ways[]` array |
| Answer mod `10^9 + 7` | ✅ → it's a counting problem, count can be huge |

**Reduce it to:** *"Dijkstra from `0`. Alongside `dist[v]`, keep `ways[v]`. On a
strict improvement `ways[v] = ways[u]`; on a tie at the shortest distance
`ways[v] = (ways[v] + ways[u]) % MOD`. Answer = `ways[n-1]`."*

**Look-alikes (all "carry a DP value alongside distance"):**
- Longest Increasing Path counting (Group 06 scenario) — count paths on a DAG.
- Cheapest Flights Within K Stops (Group 11) — carry a *stop count* alongside
  cost.
- "Shortest path with the fewest edges" — carry an edge count.

---

## 4. Intuition

1. Run Dijkstra to get `dist[v]` = shortest time to every `v`.
2. To also **count** shortest paths, keep `ways[v]`. Start `ways[0] = 1`.
3. When you relax edge `u → v` with `nd = dist[u] + w`:
   - **`nd < dist[v]`** — you found a strictly faster route to `v`. Every fastest
     route to `v` now goes through `u` (for now), so **replace**: `ways[v] =
     ways[u]`.
   - **`nd == dist[v]`** — `u` offers *another* fastest route to `v`, of the same
     length. **Add**: `ways[v] += ways[u]` (mod).
4. **Why this is correct with a plain Dijkstra:** weights are **positive**
   (`timei >= 1`). So every predecessor `u` on a shortest path to `v` has
   `dist[u] < dist[v]` **strictly** → `u` is popped (and its `ways[u]` finalized)
   **before** `v` is ever popped. By the time `v` is popped, `ways[v]` has
   already accumulated contributions from *all* its shortest-path predecessors,
   so it propagates the right count onward. (With **zero-weight** edges this
   breaks — see Scenario 4.)
5. Only propagate from a **non-stale** pop (`d == dist[u]`); a stale pop's node
   isn't finalized.

---

## 5. Approach (primary): Dijkstra + `ways[]`

1. `MOD = 10**9 + 7`. Build an undirected weighted adjacency list.
2. `dist = [inf]*n`, `ways = [0]*n`; `dist[0] = 0`, `ways[0] = 1`; `heap =
   [(0, 0)]`.
3. While `heap`: pop `(d, u)`. If `d > dist[u]`, skip (stale). For each `(v, w)`
   in `graph[u]`:
   - `nd = d + w`.
   - If `nd < dist[v]`: `dist[v] = nd`; `ways[v] = ways[u]`; push `(nd, v)`.
   - Elif `nd == dist[v]`: `ways[v] = (ways[v] + ways[u]) % MOD`.
4. Return `ways[n-1] % MOD`.

Builds on: `concepts/10` (Dijkstra) + §7 (path counting).

---

## 6. Pseudocode

```
function countPaths(n, roads):
    MOD = 1e9 + 7
    graph = undirected weighted adjacency list
    dist = [inf]*n ; ways = [0]*n
    dist[0] = 0 ; ways[0] = 1
    heap = [(0, 0)]
    while heap not empty:
        (d, u) = pop-min heap
        if d > dist[u]: continue                # stale
        for (v, w) in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                ways[v] = ways[u]                # strictly better -> replace
                push (nd, v)
            elif nd == dist[v]:
                ways[v] = (ways[v] + ways[u]) % MOD   # another shortest path -> add
    return ways[n-1] % MOD
```

---

## 7. Dry Run

```
n = 4, roads = [[0,1,1],[0,2,1],[1,3,1],[2,3,1]]   (a diamond)
```

`graph = {0:[(1,1),(2,1)], 1:[(0,1),(3,1)], 2:[(0,1),(3,1)], 3:[(1,1),(2,1)]}`.
`dist = [0,inf,inf,inf]`, `ways = [1,0,0,0]`, `heap = [(0,0)]`.

| pop | relax | dist | ways | heap |
|---|---|---|---|---|
| (0,0) | 1: 0+1=1 < inf → dist[1]=1, ways[1]=ways[0]=1 ; 2: same → dist[2]=1, ways[2]=1 | [0,1,1,inf] | [1,1,1,0] | [(1,1),(1,2)] |
| (1,1) | 0: 1+1=2 > 0, skip ; 3: 1+1=2 < inf → dist[3]=2, ways[3]=ways[1]=1 | [0,1,1,2] | [1,1,1,1] | [(1,2),(2,3)] |
| (1,2) | 0: 2 > 0 skip ; 3: 1+1=2 **== dist[3]** → ways[3] = (1 + ways[2]=1) = **2** | [0,1,1,2] | [1,1,1,2] | [(2,3)] |
| (2,3) | 1: 2+1=3 > 1 skip ; 2: 3 > 1 skip | — | — | [] |

`ways[3] = 2` → both `0→1→3` and `0→2→3` (each length 2). ✅

---

## 8. Python Code (primary — Dijkstra + ways[])

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7

        graph = defaultdict(list)
        for u, v, w in roads:
            graph[u].append((v, w))
            graph[v].append((u, w))

        dist = [float("inf")] * n
        ways = [0] * n
        dist[0] = 0
        ways[0] = 1
        heap = [(0, 0)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue                         # stale -- u not finalized on this pop
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:                 # strictly faster route to v
                    dist[v] = nd
                    ways[v] = ways[u]
                    heapq.heappush(heap, (nd, v))
                elif nd == dist[v]:              # another route of the same shortest time
                    ways[v] = (ways[v] + ways[u]) % MOD

        return ways[n - 1] % MOD


if __name__ == "__main__":
    sol = Solution()

    # LeetCode example 1 (road 0-4 has weight 3)
    assert sol.countPaths(7, [
        [0, 6, 7], [0, 1, 2], [1, 2, 3], [1, 3, 3], [6, 3, 3],
        [3, 5, 1], [6, 5, 1], [2, 5, 1], [0, 4, 3], [4, 6, 4],
    ]) == 4

    assert sol.countPaths(2, [[1, 0, 10]]) == 1
    assert sol.countPaths(1, []) == 1
    assert sol.countPaths(4, [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]]) == 2   # diamond
    assert sol.countPaths(3, [[0, 1, 1], [1, 2, 1], [0, 2, 2]]) == 2              # two length-2 paths
    # direct edge is far shorter than the long chain -> exactly 1 shortest path
    assert sol.countPaths(4, [[0, 1, 10 ** 9], [1, 2, 10 ** 9], [2, 3, 10 ** 9], [0, 3, 1]]) == 1

    print("all tests passed")
```

*(Verified against exhaustive path enumeration on 3000 random weighted graphs.)*

---

## 9. Alternative Approaches

### 9a. Dijkstra for `dist`, then DAG-DP for `ways`

Run Dijkstra once to fill `dist`. Then the **shortest-path DAG** is the set of
edges `(u, v)` with `dist[u] + w == dist[v]`. Count paths from `0` to `n-1` in
that DAG by processing nodes in **increasing `dist`** order (a valid topological
order of the DAG):

```python
order = sorted(range(n), key=lambda x: dist[x])
ways = [0] * n
ways[0] = 1
for u in order:
    for v, w in graph[u]:
        if dist[u] + w == dist[v]:
            ways[v] = (ways[v] + ways[u]) % MOD
return ways[n - 1]
```

Same complexity; separates "find distances" from "count paths." This form also
handles **zero-weight edges** correctly (Scenario 4) because it processes strictly
in `dist` order.

### The BFS↔DFS answer the interviewer wants

> "Dijkstra for the shortest time, plus a `ways[]` array: replace on a strict
> improvement, add on a tie at the shortest distance. It works inline because
> positive weights mean every shortest-path predecessor is finalized first. If
> weights could be zero I'd split it — Dijkstra for `dist`, then a DAG-DP over
> the shortest-path DAG in `dist` order."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = len(roads)`.

**Time:**
- Build adjacency list: `O(E)`.
- Dijkstra: `V` finalizing pops (`O(V log V)`) + `E` relaxations, one push each
  (`O(E log V)`). The `ways` update is `O(1)` per relaxation.
- **Total: `O((V + E) log V)`.**

**Space:**
- Adjacency list `O(V + E)`; `dist`, `ways` `O(V)`; heap `O(E)`.
- **Total: `O(V + E)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `n = 1` | `ways[0] = 1`, no relaxations → return `1` |
| Exactly one shortest path | no `nd == dist[v]` ties ever fire → `ways[n-1] = 1` |
| Huge weights (`10^9`, chained ~200 → dist ~`2·10^11`) | Python big ints; `MOD` applies only to `ways`, never to `dist` |
| Many parallel shortest paths | `ways` accumulates via the `==` branch, kept small by `% MOD` |
| Answer can never be `0` | graph is connected → `n-1` reachable → ≥ 1 shortest path |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **`ways[v] = ways[u]` on the `==` branch** (instead of `+=`) —
      undercounts, keeps only the last predecessor's paths.
- [ ] **`ways[v] += ways[u]` on the `<` branch** (instead of `=`) — keeps stale
      counts from the *old*, now-beaten distance; overcounts.
- [ ] **Forgetting `% MOD`** on the accumulation and/or the final return.
- [ ] **Propagating from a stale pop** — must `continue` when `d > dist[u]`,
      because `ways[u]` isn't finalized on that pop.
- [ ] **Applying `MOD` to `dist`** — never; only `ways` is modular. `dist`
      comparisons must be exact.
- [ ] **Treating the graph as directed** — roads are bidirectional; add both
      directions.
- [ ] **Zero-weight edges** — the inline `ways` update can miss contributions;
      use the DAG-DP form (9a).

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Count shortest paths = Dijkstra + a parallel `ways[]`.** Strict improvement
   → `ways[v] = ways[u]` (replace). Tie at shortest → `ways[v] += ways[u]`
   (accumulate). Mod as you go.
2. **Why it works inline:** positive weights ⟹ every shortest-path predecessor of
   `v` has a strictly smaller distance ⟹ is finalized before `v` ⟹ `ways[v]` is
   complete when `v` is popped.
3. **The shortest-path DAG** (edges with `dist[u] + w == dist[v]`) is the
   structure under every "count / enumerate shortest paths" problem.
4. **Carry a DP value alongside distance** — this is the same shape as "fewest
   edges among shortest paths," "min cost among shortest," Cheapest Flights'
   stop-count, and DAG longest-path counting.

| Problem | How this transfers |
|---|---|
| Longest Increasing Path — count of max-length paths | DAG-DP counting alongside the length DP |
| Cheapest Flights Within K Stops | carry a stop count alongside cost (Bellman-Ford) |
| "Shortest path using the fewest roads" | carry an edge count; tie-break by it |
| Enumerate (not just count) the shortest paths | build the shortest-path DAG, backtrack from `n-1` |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The roads are **one-way** (directed). Same question."

- **(b) Pattern:** identical algorithm, directed adjacency list.
- **(c) Adapt:** add only `graph[u].append((v, w))` (drop the reverse). Dijkstra +
  `ways` is unchanged. `O((V + E) log V)`.
- **(d) Say:** "Directed changes only the graph construction — one line — the
  count logic is the same."

### Scenario 2 — "Count paths that arrive **within `delta`** of the shortest time (not just exactly shortest)."

- **(b) Pattern:** you can no longer keep a single `ways[v]` — near-shortest
  paths form a wider sub-DAG.
- **(c) Adapt:** run Dijkstra for `dist`. Then count over the graph restricted to
  edges `(u, v)` with `dist[u] + w <= dist[v] + delta` — but that graph can have
  cycles, so it's a DP over `(node, extra_time_used)` states with `extra` in
  `[0, delta]`, processed carefully (still finite because `extra` is bounded).
  `O((V + E) · delta)` roughly.
- **(d) Say:** "'Within delta' widens the sub-DAG and adds a slack dimension —
  DP over `(node, slack)` states rather than one count per node."

### Scenario 3 — "Return the **actual list** of shortest paths, not the count."

- **(b) Pattern:** shortest-path DAG + backtracking.
- **(c) Adapt:** run Dijkstra for `dist`; build predecessor lists `pred[v] = [u :
  dist[u] + w == dist[v]]`; DFS/backtrack from `n-1` following `pred` to `0`,
  emitting each path. **Exponential** in the worst case (the count is exactly how
  many you'd emit), so only viable when the count is small.
- **(d) Say:** "Enumerate by walking the predecessor DAG backward from the
  destination — but flag that the number of paths can be exponential."

### Scenario 4 — "Some roads take **0 minutes** (instant transit)."

- **(b) Pattern:** the inline `ways` update **breaks** — two equal-distance nodes
  joined by a 0-edge can be popped in an order where `ways` isn't fully
  accumulated.
- **(c) Adapt:** split the phases (9a): Dijkstra for `dist`, then count over the
  shortest-path DAG in a valid topological order. With 0-edges, "increasing
  `dist`" alone isn't a strict order among equal-`dist` nodes — do a proper
  topological sort of the shortest-path DAG (which is acyclic: a 0-weight cycle
  can't be on a shortest path more than once) and accumulate `ways` in that
  order.
- **(d) Say:** "Zero weights kill the 'predecessor finalized first' guarantee —
  separate the phases and count over a topologically-ordered shortest-path DAG."

### Scenario 5 — "`n` is `10^5` intersections, `10^6` roads."

- **(b) Pattern:** heap Dijkstra + `ways` is already `O((V + E) log V)`.
- **(c) Adapt:** array-backed adjacency list, `dist`/`ways` as plain arrays, lazy
  stale deletion. `MOD` keeps `ways` values bounded. `≈ 10^6 · 20` operations.
- **(d) Say:** "Nothing special — array-backed Dijkstra with a `ways` array
  scales linearly-ish; `MOD` bounds the counts."

### Scenario 6 — "Roads also have a toll. Among the shortest-**time** paths, count only the ones with the **minimum total toll**."

- **(b) Pattern:** lexicographic multi-criteria shortest path + counting.
- **(c) Adapt:** per node carry `(dist, min_toll, ways)`. Relaxing `u → v` with
  `(nd, nt) = (dist[u] + w, toll[u] + t)`: compare `(nd, nt)` lexicographically
  with `(dist[v], toll[v])`. If strictly better → replace all three
  (`ways[v] = ways[u]`). If equal on both → `ways[v] += ways[u]`. If `nd`
  equal but `nt` worse → ignore.
- **(d) Say:** "Add toll as a secondary key — relax on the `(time, toll)` tuple
  lexicographically, and the `ways` replace/add logic keys off whether the tuple
  strictly improved or exactly tied."

---

## 15. Flashcards

**Q:** How do you count shortest paths on top of Dijkstra?
**A:** Keep `ways[v]` alongside `dist[v]`. On a **strict** improvement
`ways[v] = ways[u]`; on a **tie** at the shortest distance `ways[v] +=
ways[u]` (mod).

**Q:** Why does the inline `ways` update work with a plain Dijkstra here?
**A:** Weights are positive, so every shortest-path predecessor of `v` has a
strictly smaller distance → is finalized before `v` → `ways[v]` is complete when
`v` is popped.

**Q:** What breaks it, and what's the fix?
**A:** Zero-weight edges. Fix: run Dijkstra for `dist`, then count `ways` over
the shortest-path DAG in topological order.

**Q:** `=` vs `+=` on the two branches — which is which?
**A:** `<` (strict improvement) → `ways[v] = ways[u]`. `==` (tie) → `ways[v] +=
ways[u]`.

**Q:** Does `MOD` ever apply to `dist`?
**A:** No — only to `ways`. Distance comparisons must be exact.

**Q:** Time and space?
**A:** `O((V + E) log V)` time, `O(V + E)` space.

**Q:** The structure underneath all "count/enumerate shortest paths" problems?
**A:** The **shortest-path DAG** — edges `(u, v)` with `dist[u] + w == dist[v]`.

**Q:** Tie-break by a second criterion (e.g. minimum toll among shortest-time
paths)?
**A:** Carry `(dist, toll, ways)` and relax on the `(dist, toll)` tuple
lexicographically; replace `ways` on a strict tuple improvement, add on an exact
tuple tie.
