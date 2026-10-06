# 743. Network Delay Time

**LC 743** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Dijkstra's shortest path (min-heap), where the answer is the time to reach the *farthest* node

---

## 1. Intuition

A signal leaves node `k` and travels along directed, timed edges. Every node receives it at its
**shortest** travel time from `k`. The whole network has the signal once the **slowest** node gets it, so
the answer is the largest shortest-distance. With non-negative times, Dijkstra finds all the shortest
distances: always expand the node that's closest so far, because nothing can reach it faster later.

* **The min-heap always gives the closest node next:** `heap` holds `(time, node)`, and `heapq.heappop` returns the smallest time first.
* **`dist[x]` = the best time found so far to reach `x`:** it starts as `inf`, except `dist[k] = 0`. An edge improves it when `d + w < dist[nei]`.
* **Skip stale heap entries:** a node can be pushed more than once, each time with a better time. `if d > dist[node]: continue` throws away the older, worse copies.
* **The answer is the max:** `max(dist[1:])`. If it's still `inf`, some node never got the signal, so return `-1`.

**Recall:** `dist[k] = 0`, heap `[(0, k)]`. Pop the smallest, skip it if stale, and relax `d + w < dist[nei]` → push. Answer: `max(dist[1:])`, or `-1` if there's an `inf`.

## 2. Approach

* **Idea:** Single-source shortest paths with non-negative weights is Dijkstra. Then the network delay is the largest of those shortest times.
* **Graph representation:** **adjacency list** (`defaultdict(list)` of `(neighbour, time)`) built from the edge list `times`. **Directed** and **weighted** (`0 ≤ w ≤ 100` on LC). Nodes are `1 … n`.
* **Data structure / pointers:**
  * `heap`: a min-heap of **`(distance, node)` tuples**. Python compares tuples by the first item, so the smallest distance pops first. On a tie it compares `node`, which is just a harmless tie-breaker.
  * `dist[x]`: the best known time from `k` to `x`. Size `n + 1`, because nodes start at 1.
  * **When is a node final?** When it's **popped** with `d == dist[node]`. An entry with `d > dist[node]` is out of date and skipped. A node is **not** final when it's pushed, because a better time can still arrive later.
* **Invariant:** every time a non-stale `(d, node)` is popped, `d` is the true shortest time to `node`. Every edge weight is non-negative, so any other route would go through something still in the heap, which already costs at least `d`.
* **Edge cases:**
  * Some node unreachable from `k`: its `dist` stays `inf`, so it returns `-1`.
  * `n = 1`: `max(dist[1:]) = 0`, so it returns `0`.
  * Cycles: fine. A node is only re-pushed when its time strictly improves, and that can't go on forever with non-negative weights.
  * Self-loops and parallel edges: harmless. A self-loop never improves anything, and the cheapest parallel edge wins.
  * Zero-weight edges: allowed, and Dijkstra still works.
  * **Negative weights:** Dijkstra is **not** correct (a node popped as "final" could later be improved). Use Bellman-Ford (#30) instead. LC guarantees `w ≥ 0`.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

### Main: `dist` array + min-heap (skip stale entries)

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        heap = [(0, k)]  # (time to reach node, node)

        while heap:
            d, node = heapq.heappop(heap)
            if d > dist[node]:
                continue  # stale entry: a shorter time was already found

            for nei, w in graph[node]:
                if d + w < dist[nei]:
                    dist[nei] = d + w
                    heapq.heappush(heap, (dist[nei], nei))

        max_time = max(dist[1:])
        return max_time if max_time < float('inf') else -1
```

### Alternative: min-heap + `visited` set (finalise on the first pop)

There's no `dist` array. The **first** time a node is popped, its `d` is the shortest time, so it goes into `visited` and later copies are skipped. Pops come out in increasing time, so the **last** node finalised has the largest time.

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        heap = [(0, k)]  # (time to reach node, node)
        visited = set()
        max_time = 0

        while heap:
            d, node = heapq.heappop(heap)
            if node in visited:
                continue  # already finalised with a smaller time
            visited.add(node)
            max_time = d  # pops come out in increasing time, so the last one is the max

            for nei, w in graph[node]:
                if nei not in visited:
                    heapq.heappush(heap, (d + w, nei))

        return max_time if len(visited) == n else -1
```

| | Main (`dist` + heap) | Alternative (heap + `visited`) |
| --- | --- | --- |
| Node is final when… | popped with `d == dist[node]` | popped for the **first** time |
| Pushes | only when `d + w < dist[nei]` (a real improvement) | every edge to a not-yet-visited node |
| Heap size | smaller (≤ the number of improvements) | up to about E entries |
| Unreachable check | `max(dist[1:])` is `inf` | `len(visited) < n` |

## 4. Dry Run

Input (LC Example 1): `times = [[2,1,1],[2,3,1],[3,4,1]]`, `n = 4`, `k = 2`

```text
        2
   (1) / \ (1)
      1   3
           \ (1)
            4
```

Main version. `dist[1..4]` starts as `[inf, 0, inf, inf]` and `heap = [(0, 2)]`.

| Pop `(d, node)` | Stale? | Relaxations (`d + w < dist[nei]`) | `dist[1..4]` after | `heap` after |
| --- | --- | --- | --- | --- |
| `(0, 2)` | no | `1`: 0+1 = 1 < inf → push `(1,1)`. `3`: 0+1 = 1 < inf → push `(1,3)` | `[1, 0, 1, inf]` | `(1,1) (1,3)` |
| `(1, 1)` | no | node 1 has no outgoing edges | `[1, 0, 1, inf]` | `(1,3)` |
| `(1, 3)` | no | `4`: 1+1 = 2 < inf → push `(2,4)` | `[1, 0, 1, 2]` | `(2,4)` |
| `(2, 4)` | no | none | `[1, 0, 1, 2]` | empty |

`max(dist[1:]) = 2`, so it returns **2**. The Alternative pops in the same order, `(0,2) → (1,1) → (1,3) → (2,4)`, finalises all 4 nodes, and also returns `max_time = 2`.

(Ties like `(1,1)` vs `(1,3)` are broken by the node number, the second item of the tuple.)

## 5. Complexity

Let **V** = `n` and **E** = `len(times)`.

* **Time: O((V + E) log V)** for the Main version, and **O(E log E)** for the Alternative, which is the same thing in big-O because log E ≤ 2 log V
  Think of it as: every edge can cause at most one push (only when it improves a distance), and every push or pop on the heap costs about log(heap size). So there are about E heap operations of log cost each, plus V pops to finalise the nodes. Building the graph is E, and `max(dist)` is V. The Alternative pushes for every edge to an unvisited node, so its heap gets bigger, but the bound is the same.
* **Space: O(V + E)**
  Think of it as: the adjacency list stores every edge (E). `dist` (or `visited`) has one slot per node (V). The heap can hold up to about E entries in the worst case.

## 6. Recall (30 seconds)

* Non-negative weights and one source means **Dijkstra**. The heap holds `(dist, node)`, smallest first. The answer is the **max** shortest distance, or `-1` if any node is `inf`.
* Main: `if d > dist[node]: continue`, then push on `d + w < dist[nei]`. Alternative: `if node in visited: continue`, then mark it **on pop**.
* O((V + E) log V) time and O(V + E) space. With negative weights, use Bellman-Ford instead.
