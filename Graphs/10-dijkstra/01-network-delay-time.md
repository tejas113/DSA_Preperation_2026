# Network Delay Time  ·  LeetCode 743  ·  Medium

Group 10 — Dijkstra  ·  the classic sum-of-weights Dijkstra. Answer = the time
the **last** node receives the signal = the maximum shortest-distance from the
source.

Prereqs: `concepts/10-dijkstra.md`, `concepts/02` (weighted adjacency list).

---

## 1. Problem

A network of `n` nodes labeled `1..n`. `times[i] = [ui, vi, wi]` is a **directed**
edge: a signal from `ui` reaches `vi` after `wi` time.

You send a signal from node `k`. **Return the time for *all* `n` nodes to receive
it**, or `-1` if some node never does.

Constraints:
- `1 <= k <= n <= 100`, `1 <= times.length <= 6000`.
- `0 <= wi <= 100` — weights are **non-negative** (so Dijkstra applies).
- All `(ui, vi)` pairs are distinct.

Example 1:

```
times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
answer = 2        # 2->1: 1, 2->3: 1, 3->4: total 2. The last (node 4) is at t=2.
```

Example 2: `times = [[1,2,1]], n = 2, k = 1` → `1`.
Example 3: `times = [[1,2,1]], n = 2, k = 2` → `-1` (node 1 never hears it).

---

## 2. Explain Like I'm 5

You shout from house `k`. The shout travels along one-way phone lines, each
taking some seconds. It fans out — reaching nearby houses first, then farther
ones.

"When does *everyone* hear it?" = the moment the **slowest-to-reach** house
finally hears it. So find the shout's arrival time at every house, and the answer
is the **latest** of those times. If even one house has no phone line leading to
it from `k`, it never hears the shout → `-1`.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Shortest / minimum time" + **weighted** edges | ✅ |
| Weights **non-negative** | ✅ (`wi >= 0`) → Dijkstra |
| Single source (`k`) | ✅ |
| "Time for *all* to receive" | ✅ → `max` of all shortest distances |

**Reduce it to:** *"Dijkstra from `k`. If every node got a finite distance,
return the maximum; else `-1`."*

**Look-alikes:**
- Cheapest Flights Within K Stops (Group 11) — weighted shortest path too, but a
  **hop limit** breaks plain Dijkstra → Bellman-Ford.
- Multi-source variants — push all sources at cost `0`.

---

## 4. Intuition

1. The signal reaches each node via its **shortest-time path** from `k` — extra
   detours only delay it.
2. So run Dijkstra from `k` to get `dist[v]` = earliest arrival time at every
   `v`.
3. "Everyone has received it" happens at `max(dist[v])` — the last arrival.
4. If Dijkstra never assigns a finite distance to some node (it's unreachable
   from `k`), the answer is `-1`.

Dijkstra is right here (not plain BFS) because edges have different weights, and
right (not Bellman-Ford) because all weights are `>= 0`.

---

## 5. Approach (primary): Dijkstra, answer = max distance

1. Build `graph = defaultdict(list)`; for `[u, v, w]`: `graph[u].append((v, w))`.
2. `dist = {}` (also serves as the "finalized" set). `heap = [(0, k)]`.
3. While `heap`: pop `(d, u)`. If `u in dist`, skip (already finalized). Else
   `dist[u] = d`, and for each `(v, w)` in `graph[u]` with `v not in dist`, push
   `(d + w, v)`.
4. Return `max(dist.values())` if `len(dist) == n`, else `-1`.

Builds on: `concepts/10` (Dijkstra), using the `dist`-dict-as-done-set flavor.

---

## 6. Pseudocode

```
function networkDelayTime(times, n, k):
    graph = adjacency list of (v, w) from times
    dist = {}                         # node -> finalized shortest time
    heap = [(0, k)]
    while heap not empty:
        (d, u) = pop-min heap
        if u in dist: continue         # already finalized
        dist[u] = d
        for (v, w) in graph[u]:
            if v not in dist:
                push (d + w, v)
    return max(dist.values()) if len(dist) == n else -1
```

---

## 7. Dry Run

```
times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
graph = { 2:[(1,1),(3,1)], 3:[(4,1)] }
```

| pop | u in dist? | dist after | relax → push | heap after |
|---|---|---|---|---|
| (0,2) | no | {2:0} | (1,1), (1,3) | [(1,1),(1,3)] |
| (1,1) | no | {2:0, 1:1} | graph[1] empty | [(1,3)] |
| (1,3) | no | {2:0, 1:1, 3:1} | (2,4) | [(2,4)] |
| (2,4) | no | {2:0, 1:1, 3:1, 4:2} | graph[4] empty | [] |

`len(dist) == 4 == n` → `max(0, 1, 1, 2) = 2`. ✅

---

## 8. Python Code (primary — Dijkstra)

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        dist = {}                              # node -> finalized shortest time; also the done-set
        heap = [(0, k)]

        while heap:
            d, u = heapq.heappop(heap)
            if u in dist:
                continue                        # already finalized (stale heap entry)
            dist[u] = d
            for v, w in graph[u]:
                if v not in dist:
                    heapq.heappush(heap, (d + w, v))

        return max(dist.values()) if len(dist) == n else -1


if __name__ == "__main__":
    sol = Solution()

    assert sol.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert sol.networkDelayTime([[1, 2, 1]], 2, 1) == 1
    assert sol.networkDelayTime([[1, 2, 1]], 2, 2) == -1
    assert sol.networkDelayTime([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1) == 3   # 1->2->3 beats 1->3
    assert sol.networkDelayTime([[1, 2, 0]], 2, 1) == 0                          # zero-weight edge
    assert sol.networkDelayTime([[1, 2, 1], [2, 1, 3]], 2, 1) == 1

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Bellman-Ford (works, `O(V·E)`, no heap — and it's what you'd use with negative weights)

```python
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        dist = [float("inf")] * (n + 1)
        dist[k] = 0
        for _ in range(n - 1):                  # relax all edges V-1 times
            updated = False
            for u, v, w in times:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break
        ans = max(dist[1:])
        return ans if ans < float("inf") else -1
```

Simpler to write, no heap. `O(V·E)` = `100 · 6000` here — fine. This is the tool
of choice the moment weights can be negative (Group 11).

### The BFS↔DFS answer the interviewer wants

> "Weighted, non-negative, single source → Dijkstra, `O((V+E) log V)`. The answer
> isn't the sum of distances — it's the **max**, because 'everyone has it' means
> the last arrival. If weights could be negative I'd switch to Bellman-Ford
> (`O(V·E)`). Plain BFS would be wrong since edge weights differ."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = len(times)`.

**Time:**
- Build adjacency list: `O(E)`.
- Dijkstra: each node finalized once (`V` pops that do work, `O(V log V)`); each
  edge relaxed at most once, one push each (`O(E log V)`). Stale pops are `O(1)`
  each and there are `O(E)` of them.
- `max` over `dist`: `O(V)`.
- **Total: `O((V + E) log V)`.**

**Space:**
- Adjacency list `O(V + E)`; `dist` `O(V)`; heap up to `O(E)`.
- **Total: `O(V + E)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| A node unreachable from `k` | never added to `dist` → `len(dist) < n` → `-1` |
| `k` itself | `dist[k] = 0` |
| `n = 1` | `dist = {k: 0}` → returns `0` |
| Zero-weight edges | Dijkstra handles `w = 0` fine (still non-negative) |
| Multiple edges into one node | the cheapest wins via relaxation |
| Two-way-ish edges (`u→v` and `v→u` both present) | treated as two independent directed edges |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Returning `sum(dist.values())` instead of `max(...)`.** The answer is
      *when the last node receives it*, not a total.
- [ ] **Forgetting the `-1` case** — must check `len(dist) == n` (or `max <
      inf`).
- [ ] **Pushing `(node, cost)` instead of `(cost, node)`** — the heap orders by
      the first element; cost must come first.
- [ ] **Re-relaxing finalized nodes** — harmless but wasteful; the `if u in
      dist: continue` (or `if v not in dist` guard on push) avoids it.
- [ ] **Using plain BFS** — wrong whenever weights differ.
- [ ] **1-indexed nodes with an array `dist`** — size it `n + 1`; the dict form
      sidesteps this.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Dijkstra = BFS with a min-heap.** First pop of a node finalizes its distance
   (non-negative weights only).
2. **"Time for all to receive" = `max` over all shortest distances**, not the
   sum. Unreachable ⟹ `-1`.
3. **`dist` doubles as the done-set** — `if u in dist: continue` on pop.
4. **Non-negative ⟹ Dijkstra; negative ⟹ Bellman-Ford; unweighted ⟹ BFS.** Say
   which and why.

| Problem | How this transfers |
|---|---|
| Swim in Rising Water / Path With Minimum Effort | Dijkstra on a grid, `max` instead of `+` for the cost |
| Cheapest Flights Within K Stops | weighted shortest path with a hop limit → Bellman-Ford |
| "Min time to inform all employees" (tree) | this, on a tree (so BFS/DFS from the root suffices) |
| Multi-source "nearest facility, weighted roads" | push all sources at cost 0 |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Some links have **negative** delay (a booster that speeds the signal up)."

- **(b) Pattern:** Dijkstra's "first pop is final" argument breaks with negative
  edges. Use **Bellman-Ford**.
- **(c) Adapt:** relax all `E` edges `V - 1` times → `O(V·E)`. Then do one more
  pass: if any edge still relaxes, there's a **negative cycle** reachable from
  `k`, so "time for all" is unbounded (answer undefined / `-inf`).
- **(d) Say:** "One negative edge and Dijkstra can finalize a node too early —
  Bellman-Ford relaxes everything `V-1` times, plus a `V`-th pass to detect a
  negative cycle."

### Scenario 2 — "Return the actual path the signal takes to the **slowest** node."

- **(b) Pattern:** Dijkstra + **parent pointers**.
- **(c) Adapt:** on a successful relaxation `dist[v] = d + w`, set
  `parent[v] = u`. After Dijkstra, `argmax` the `dist` values to find the slowest
  node, then walk `parent` back to `k` and reverse. `O(V + E)` extra.
- **(d) Say:** "One parent pointer per relaxation turns the distance into a
  path — walk it back from the slowest node."

### Scenario 3 — "`n` is `10^5` nodes, `10^6` edges."

- **(b) Pattern:** heap Dijkstra is already near-optimal.
- **(c) Adapt:** adjacency list as an array of lists, `dist` as a plain array
  (not dict), lazy deletion. `O((V + E) log V) ≈ 10^6 · 20`. Bellman-Ford's
  `O(V·E) = 10^11` is far too slow at this scale.
- **(d) Say:** "This is exactly where Dijkstra's `log` factor beats
  Bellman-Ford's `V·E` — array-backed heap Dijkstra handles `10^6` edges
  comfortably."

### Scenario 4 — "The signal is broadcast from **several** source nodes at once. When does everyone have it?"

- **(b) Pattern:** **multi-source Dijkstra**.
- **(c) Adapt:** push every source into the heap at cost `0` before the loop.
  Each node's `dist` becomes its time from the *nearest* source. Answer is still
  `max(dist)` (or `-1` if some node is unreachable from all sources).
- **(d) Say:** "Multiple simultaneous sources = seed the heap with all of them at
  cost 0 — same as multi-source BFS, just weighted."

### Scenario 5 — "Each node takes some **processing time** to re-broadcast after receiving (node weights, not just edge weights)."

- **(b) Pattern:** fold the node weight into the edges, or split nodes.
- **(c) Adapt:** simplest — when relaxing `u`'s outgoing edges, use
  `nd = d + delay[u] + w` (the signal must be processed at `u` before it leaves).
  Formally equivalent to **node splitting**: replace node `u` with `u_in → u_out`
  connected by an edge of weight `delay[u]`; incoming edges hit `u_in`, outgoing
  leave `u_out`. Complexity unchanged.
- **(d) Say:** "Node weights become an extra term when relaxing outgoing edges —
  or the textbook node-split into an in/out pair joined by the node's own weight."

### Scenario 6 — "Edge weights change over time (traffic), and you get many queries with different `k`."

- **(b) Pattern:** per-query Dijkstra, or per-snapshot all-pairs.
- **(c) Adapt:** if weights change between nearly every query, just run a fresh
  `O((V + E) log V)` Dijkstra per query. If many queries share one weight
  snapshot and `n` is small (`≤ ~500`), precompute all-pairs with
  **Floyd-Warshall** (`O(V³)`) once per snapshot, then each query (any `k`) is
  `O(V)` to read the row and take its max.
- **(d) Say:** "Frequently-changing weights → Dijkstra per query. Stable snapshot
  + many `k` values + small `n` → one Floyd-Warshall pass per snapshot, then
  `O(V)` per query."

---

## 15. Flashcards

**Q:** Why Dijkstra here, not BFS or Bellman-Ford?
**A:** Edges are weighted (rules out plain BFS) and non-negative (Dijkstra is
valid and faster than Bellman-Ford).

**Q:** What is the answer, exactly?
**A:** `max` over all shortest distances from `k` (the last node to receive the
signal). `-1` if any node is unreachable.

**Q:** How does `dist` double as the visited set?
**A:** On pop, `if u in dist: continue` — a node already in `dist` is finalized;
skip stale heap copies.

**Q:** Time and space?
**A:** `O((V + E) log V)` time, `O(V + E)` space.

**Q:** The tuple order in the heap?
**A:** `(cost, node)` — the heap sorts by the first element, so cost must come
first.

**Q:** Negative edges — what changes?
**A:** Dijkstra is no longer valid. Bellman-Ford: relax all edges `V-1` times
(`O(V·E)`), plus a `V`-th pass to detect a negative cycle.

**Q:** Multiple simultaneous source nodes?
**A:** Push all of them into the heap at cost `0` (multi-source Dijkstra); answer
is still `max(dist)`.

**Q:** Node processing delays (not just edge weights)?
**A:** Add `delay[u]` when relaxing `u`'s outgoing edges, or split `u` into
`u_in → u_out` joined by an edge of weight `delay[u]`.
