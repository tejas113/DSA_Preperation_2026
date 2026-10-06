# 1976. Number of Ways to Arrive at Destination

**LC 1976** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Dijkstra + counting shortest paths (`ways[]` carried alongside `dist[]`)

---

## 1. Intuition

Find the shortest travel time from `0` to `n-1`, and also **how many different routes** take exactly that
time. Run normal Dijkstra, but give every node a counter `ways[x]` = "number of fastest routes to `x` found
so far". When an edge gives a **strictly faster** time to a neighbour, the neighbour's old routes stop
counting, so copy the current node's count. When an edge gives an **equally fast** time, it's another
fastest route, so add the current node's count.

* **`dist` and `ways` start together:** `dist[0], ways[0] = 0, 1`. There's exactly one way to be at the start, and that's to stay there.
* **Strictly faster → replace:** `if new_d < dist[nei]: dist[nei] = new_d; ways[nei] = ways[node]; push`.
* **Equally fast → add:** `elif new_d == dist[nei]: ways[nei] = (ways[nei] + ways[node]) % MOD`. There's no push, because the time didn't change.
* **Why a node's `ways` is complete when it's popped:** every road takes at least 1 minute, so any node *before* it on a fastest route has a strictly smaller `dist` and was popped (and finished adding to it) earlier.
* **Modulo:** the count can be huge (2^100 and up), so every addition is taken `% MOD`.

**Recall:** Dijkstra with `ways[0] = 1`. A strictly shorter route means `dist = new_d`, `ways = ways[node]`, and push. An equal route means `ways += ways[node]`. Return `ways[n-1] % MOD`.

## 2. Approach

* **Idea:** Dijkstra finalises nodes in order of shortest time. Each fastest route to `x` reaches `x` through some neighbour `p`, with `dist[p] + t == dist[x]`. So `ways[x]` = the sum of `ways[p]` over those neighbours, and Dijkstra's pop order guarantees each `ways[p]` is final before it's added.
* **Graph representation:** **adjacency list** (`defaultdict(list)` of `(neighbour, time)`) built from the edge list `roads`. **Undirected** (both directions are added) and **weighted** (`time ≥ 1`). Nodes are `0 … n-1`.
* **Data structure / pointers:**
  * `heap`: a min-heap of **`(time, node)`**. The smallest time pops first, and ties are broken by node number.
  * `dist[x]`: the shortest known time from `0` to `x`.
  * `ways[x]`: the number of routes from `0` to `x` that take exactly `dist[x]` (mod `10^9 + 7`).
  * **When is a node final?** When it's **popped** with `d == dist[node]` (Main), or on its **first pop** (Alternative). Only then does it pass its `ways` on to its neighbours.
* **Invariant:** when `node` is popped (and not stale), `dist[node]` is the true shortest time and `ways[node]` counts **all** fastest routes to it.
* **Edge cases:**
  * `n = 1`: the start is the destination, so `ways[0] = 1` and it returns `1`.
  * A single road `0 – 1`: returns `1`.
  * Many tied routes: the counts multiply quickly (a chain of 100 "diamonds" has 2^100 routes), and the `% MOD` keeps them small.
  * **Why `time ≥ 1` matters:** with a **zero-time** road, a node and its neighbour could have the same `dist`, and the neighbour might be popped (and pass on its `ways`) before it got its last addition. Then counts would be wrong. LC guarantees `time ≥ 1`.
  * The destination is always reachable (LC guarantees a connected graph).
  * Negative times would break Dijkstra itself. They aren't allowed on LC.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

### Main: `dist` + `ways` arrays + min-heap (skip stale entries)

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        MOD = 10**9 + 7
        graph = defaultdict(list)
        for u, v, t in roads:
            graph[u].append((v, t))
            graph[v].append((u, t))

        dist = [float('inf')] * n   # shortest time from 0
        ways = [0] * n              # number of shortest routes from 0
        dist[0], ways[0] = 0, 1
        heap = [(0, 0)]  # (time, node)

        while heap:
            d, node = heapq.heappop(heap)
            if d > dist[node]:
                continue  # stale entry

            for nei, t in graph[node]:
                new_d = d + t
                if new_d < dist[nei]:      # strictly faster: older routes stop counting
                    dist[nei] = new_d
                    ways[nei] = ways[node]
                    heapq.heappush(heap, (new_d, nei))
                elif new_d == dist[nei]:   # another equally fast route
                    ways[nei] = (ways[nei] + ways[node]) % MOD

        return ways[n - 1] % MOD
```

### Alternative: min-heap + `visited` set (finalise on the first pop)

The `visited` set replaces the stale check. A node passes on its `ways` only on its first pop. Note that this version **still needs `dist`**: the `elif new_d == dist[nei]` check is how a second fastest route is noticed, and a `visited` set alone can't tell you that.

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        MOD = 10**9 + 7
        graph = defaultdict(list)
        for u, v, t in roads:
            graph[u].append((v, t))
            graph[v].append((u, t))

        dist = [float('inf')] * n   # still needed to spot "equally fast" routes
        ways = [0] * n
        dist[0], ways[0] = 0, 1
        heap = [(0, 0)]  # (time, node)
        visited = set()

        while heap:
            d, node = heapq.heappop(heap)
            if node in visited:
                continue  # already finalised
            visited.add(node)

            for nei, t in graph[node]:
                if nei in visited:
                    continue
                new_d = d + t
                if new_d < dist[nei]:
                    dist[nei] = new_d
                    ways[nei] = ways[node]
                    heapq.heappush(heap, (new_d, nei))
                elif new_d == dist[nei]:
                    ways[nei] = (ways[nei] + ways[node]) % MOD

        return ways[n - 1] % MOD
```

| | Main (stale check) | Alternative (`visited` set) |
| --- | --- | --- |
| Node is final when… | popped with `d == dist[node]` | popped for the **first** time |
| Needs `dist`? | yes | **yes**, for the "equally fast" check |
| Skips edges to finished nodes? | no (they just fail both checks) | yes (`if nei in visited: continue`) |

## 4. Dry Run

Input (LC Example 1): `n = 7`

```text
roads (u, v, time):
0-6:7  0-1:2  1-2:3  1-3:3  6-3:3  3-5:1  6-5:1  2-5:1  0-4:5  4-6:2
```

Main version. The table shows each pop and what it changes. A **replace** sets `dist` and `ways = ways[node]` and pushes. An **add** does `ways += ways[node]`.

| Pop `(d, node)` | `ways[node]` | Changes to neighbours | `dist` after | `ways` after |
| --- | --- | --- | --- | --- |
| `(0, 0)` | 1 | replace 6 → 7, replace 1 → 2, replace 4 → 5 | `[0,2,∞,∞,5,∞,7]` | `[1,1,0,0,1,0,1]` |
| `(2, 1)` | 1 | replace 2 → 5, replace 3 → 5 | `[0,2,5,5,5,∞,7]` | `[1,1,1,1,1,0,1]` |
| `(5, 2)` | 1 | replace 5 → 6 | `[0,2,5,5,5,6,7]` | `[1,1,1,1,1,1,1]` |
| `(5, 3)` | 1 | to 6: 8 > 7, no. To 5: 6 == 6, **add**, so `ways[5]` = 2 | same | `[1,1,1,1,1,2,1]` |
| `(5, 4)` | 1 | to 6: 7 == 7, **add**, so `ways[6]` = 2 | same | `[1,1,1,1,1,2,2]` |
| `(6, 5)` | 2 | to 6: 7 == 7, **add 2**, so `ways[6]` = 4 | same | `[1,1,1,1,1,2,4]` |
| `(7, 6)` | 4 | the destination is final, and nothing improves | same | same |

It returns **`ways[6] = 4`**. The four 7-minute routes are `0→6`, `0→4→6`, `0→1→2→5→6` and `0→1→3→5→6`.

## 5. Complexity

Let **V** = `n` and **E** = `len(roads)`.

* **Time: O((V + E) log V)**
  Think of it as: this is plain Dijkstra plus a tiny bit of extra work per edge. Each road is checked from both ends (2E checks), and each check is a comparison plus maybe one heap push, which costs about log V. The `ways` updates are just additions. Building the graph is E.
* **Space: O(V + E)**
  Think of it as: the adjacency list stores every road twice (2E). `dist`, `ways` (and `visited`) have V slots, and the heap holds up to about E entries.

## 6. Recall (30 seconds)

* Dijkstra plus a `ways[]` array, with `ways[0] = 1`. **Strictly shorter** → replace `dist` and copy `ways[node]`, then push. **Equal** → add `ways[node]` (mod 1e9+7).
* A node's count is complete when it's popped, because every road takes ≥ 1 minute, so all its predecessors popped earlier. Zero-time roads would break this.
* O((V + E) log V) time and O(V + E) space. The Alternative still needs `dist` for the "equal" check.
