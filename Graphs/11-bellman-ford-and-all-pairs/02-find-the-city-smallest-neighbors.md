# Find the City With the Smallest Number of Neighbors at a Threshold Distance  ·  LeetCode 1334  ·  Medium  ·  *(supplementary)*

> 🔁 **Flagged for revision** (whole of Group 11). The one idea to re-derive on
> Day 5: *Floyd-Warshall asks, for each candidate intermediate city `k`, "does
> `i → k → j` beat my current best `i → j`?" — loop `k` on the **outside**, then
> `i`, then `j`. After every `k` has had its turn, `dist` holds all shortest
> paths. The rest is a plain count over that matrix.*

Group 11 — Bellman-Ford / All-Pairs  ·  the natural home of **Floyd-Warshall**:
compute every pair's shortest distance in `O(V³)`, then a simple per-city count.

Prereqs: `concepts/12-floyd-warshall.md`.

---

## 1. Problem

`n` cities `0..n-1` connected by weighted **undirected** `edges` (`[u, v, w]`).
For each city, count how many *other* cities are reachable within a total road
distance of `distanceThreshold`.

**Return the city with the smallest such count. If several tie, return the one
with the largest index.**

Constraints:
- `2 <= n <= 100` — small, so `O(V³)` Floyd-Warshall is comfortable.
- `1 <= edges.length <= n·(n-1)/2`, `1 <= w, distanceThreshold <= 10^4`.
- At most one edge between any pair.

Example 1:

```
n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
answer = 3
# city 3 reaches {2, 1} within 4  -> count 2 (the smallest); tie? no.
```

Example 2:

```
n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2
answer = 0
# after Floyd-Warshall, counting cities within distance 2 (excluding self):
#   city 0 -> {1}                    -> count 1   <-- the unique minimum
#   city 1 -> {0, 4}                 -> count 2
#   city 2 -> {3, 4}                 -> count 2
#   city 3 -> {2, 4}                 -> count 2
#   city 4 -> {1, 2, 3}              -> count 3
# minimum is 1, held only by city 0 -> answer 0 (no tie).
```

*(The "largest index on a tie" rule only matters when two cities genuinely share
the minimum count — see Example 1's dry run in §7, where cities 0 and 3 tie at
count 2 and city 3 wins.)*

---

## 2. Explain Like I'm 5

Every city wants as few "close friends" as possible — a close friend is another
city you can drive to in under `distanceThreshold` total road-miles.

Step 1: figure out the shortest driving distance between **every pair** of
cities. Step 2: for each city, count its close friends. Step 3: pick the city
with the fewest. If two cities are equally lonely, pick the one with the bigger
number on its sign.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "For **every** city..." / needs shortest distance between **all pairs** | ✅ → Floyd-Warshall |
| `V` is small (`≤ 100`) | ✅ → `O(V³) = 10^6`, trivial |
| Then a simple aggregate per node | ✅ → count + argmin with a tie rule |

**Reduce it to:** *"Floyd-Warshall for the all-pairs distance matrix, then for
each city `i` count `j != i` with `dist[i][j] <= threshold`; return the city with
the minimum count, ties broken toward the larger index."*

**Alternative:** run Dijkstra from each of the `n` sources — `O(V·(V+E) log V)`,
better on sparse graphs but more code. At `n ≤ 100` Floyd-Warshall's three tiny
loops win on simplicity.

---

## 4. Intuition

1. The question is inherently **all-pairs**: you need each city's distance to
   *every* other city.
2. `n ≤ 100`, so `O(n³) = 10^6` operations — Floyd-Warshall's three nested loops
   are the least-code way to get the full distance matrix.
3. Floyd-Warshall's engine: for each possible intermediate city `k`, check
   whether routing `i → k → j` is shorter than the best `i → j` found so far
   (`dist[i][k] + dist[k][j] < dist[i][j]`). After trying every `k`, all shortest
   paths are found. **`k` must be the outermost loop.**
4. Then it's a plain count-and-argmin. The tie rule "largest index wins" falls
   out if you iterate `i` from `0` upward and use `<=` (not `<`) when updating
   the best.

---

## 5. Approach (primary): Floyd-Warshall + per-city count

1. `dist = [[inf]*n for _ in range(n)]`; `dist[i][i] = 0`. For each `[u, v, w]`:
   `dist[u][v] = dist[v][u] = min(existing, w)` (undirected; `min` handles no
   parallel edges but is safe anyway).
2. Floyd-Warshall: `for k: for i: for j: dist[i][j] = min(dist[i][j],
   dist[i][k] + dist[k][j])`.
3. `best_city = -1`, `best_count = inf`. For `i` in `0..n-1`: `cnt = number of j
   != i with dist[i][j] <= threshold`; if `cnt <= best_count`: update `best_count
   = cnt`, `best_city = i`.
4. Return `best_city`.

Builds on: `concepts/12` (Floyd-Warshall).

---

## 6. Pseudocode

```
function findTheCity(n, edges, threshold):
    dist = n x n matrix of infinity
    for i in 0..n-1: dist[i][i] = 0
    for [u, v, w] in edges:
        dist[u][v] = min(dist[u][v], w)
        dist[v][u] = min(dist[v][u], w)

    for k in 0..n-1:                          # k OUTERMOST
        for i in 0..n-1:
            for j in 0..n-1:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    best_city, best_count = -1, infinity
    for i in 0..n-1:
        cnt = count of j != i with dist[i][j] <= threshold
        if cnt <= best_count:                 # <= makes ties prefer the larger i
            best_count = cnt
            best_city = i
    return best_city
```

---

## 7. Dry Run

```
n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], threshold = 4
```

Init `dist` (∞ where no direct edge):

```
     0    1    2    3
0 [  0    3    ∞    ∞ ]
1 [  3    0    1    4 ]
2 [  ∞    1    0    1 ]
3 [  ∞    4    1    0 ]
```

Floyd-Warshall (only the changes):

- `k = 1`: `dist[0][2]` = min(∞, `dist[0][1]+dist[1][2]` = 3+1 = 4) → **4**.
  `dist[0][3]` = min(∞, 3+4 = 7) → **7**.
- `k = 2`: `dist[1][3]` = min(4, `dist[1][2]+dist[2][3]` = 1+1 = 2) → **2**.
  `dist[0][3]` = min(7, `dist[0][2]+dist[2][3]` = 4+1 = 5) → **5**.
- `k = 3`: `dist[1][2]` = min(1, ...) no change. Nothing improves.

Final:

```
     0    1    2    3
0 [  0    3    4    5 ]
1 [  3    0    1    2 ]
2 [  4    1    0    1 ]
3 [  5    2    1    0 ]
```

Counts within threshold 4 (`j != i`, `dist <= 4`):
- city 0: `{1 (3), 2 (4)}` → **2**
- city 1: `{0 (3), 2 (1), 3 (2)}` → **3**
- city 2: `{0 (4), 1 (1), 3 (1)}` → **3**
- city 3: `{1 (2), 2 (1)}` → **2**

Minimum count is `2`, held by cities `0` and `3`. Tie → larger index → **`3`**.
✅

---

## 8. Python Code (primary — Floyd-Warshall + count)

```python
from typing import List


class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        INF = float("inf")
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = min(dist[u][v], w)
            dist[v][u] = min(dist[v][u], w)

        for k in range(n):                       # k MUST be the outermost loop
            for i in range(n):
                dik = dist[i][k]
                if dik == INF:
                    continue
                for j in range(n):
                    if dik + dist[k][j] < dist[i][j]:
                        dist[i][j] = dik + dist[k][j]

        best_city, best_count = -1, INF
        for i in range(n):
            cnt = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if cnt <= best_count:                 # <= => ties resolve to the larger index
                best_count = cnt
                best_city = i
        return best_city


if __name__ == "__main__":
    sol = Solution()

    assert sol.findTheCity(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3
    assert sol.findTheCity(
        5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2) == 0
    assert sol.findTheCity(
        6, [[0, 3, 7], [2, 4, 1], [0, 1, 5], [2, 3, 10], [1, 3, 6], [1, 2, 1]], 417) == 5
    assert sol.findTheCity(2, [[0, 1, 10]], 5) == 1        # both count 0 -> larger index
    assert sol.findTheCity(3, [[0, 1, 1], [1, 2, 1], [0, 2, 1]], 2) == 2   # all count 2, tie -> 2

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Dijkstra from every city

```python
import heapq
from collections import defaultdict


def findTheCity(self, n, edges, distanceThreshold):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    def dijkstra(src):
        dist = [float("inf")] * n
        dist[src] = 0
        heap = [(0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(heap, (d + w, v))
        return dist

    best_city, best_count = -1, float("inf")
    for i in range(n):
        d = dijkstra(i)
        cnt = sum(1 for j in range(n) if i != j and d[j] <= distanceThreshold)
        if cnt <= best_count:
            best_count, best_city = cnt, i
    return best_city
```

`O(V·(V + E) log V)` — better on **sparse** graphs; more code. At `n ≤ 100`,
Floyd-Warshall's `10^6` triple-loop is simpler and plenty fast.

### The BFS↔DFS answer the interviewer wants

> "It's an all-pairs shortest-path question with `n ≤ 100`, so Floyd-Warshall —
> three nested loops, `O(n³) = 10^6`. Then per city, count who's within the
> threshold and take the min, ties toward the larger index. On a much bigger
> sparse graph I'd run Dijkstra from each source instead."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = len(edges)`.

**Time:**
- Init the matrix: `O(V² + E)`.
- Floyd-Warshall: three nested loops over `V` → `O(V³)`.
- Counting per city: `O(V²)`.
- **Total: `O(V³)`** (`= 10^6` at `n = 100`).

Dijkstra-per-source variant: `O(V · (V + E) log V)`.

**Space:**
- The distance matrix: `O(V²)`.
- **Total: `O(V²)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| A city connected to nothing | its row stays `inf` except the diagonal → count `0` → a strong candidate for the answer |
| All cities within threshold of each other | every count is `n - 1`; tie rule → return `n - 1` (largest index) |
| Ties on the minimum count | `<=` in the update + iterating `i` upward → the **largest** index wins |
| `distanceThreshold` smaller than every edge | every count is `0` → return `n - 1` |
| Parallel edges (not in constraints, but) | `min(dist[u][v], w)` keeps the cheapest |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Wrong loop order** — `k` **must** be outermost. `i` or `j` outside `k`
      gives wrong distances on some graphs.
- [ ] **`dist[i][i]` not initialized to `0`.**
- [ ] **Building a directed matrix** — edges are undirected; set both
      `dist[u][v]` and `dist[v][u]`.
- [ ] **Tie rule inverted** — use `<=` and iterate `i` from `0` up so the last
      (largest) index among equal counts is kept. `<` keeps the smallest index
      (wrong).
- [ ] **Counting `j == i`** — exclude self (`dist[i][i] = 0 <= threshold` would
      otherwise inflate every count by 1 equally — harmless to the argmin, but
      wrong as a "number of neighbors").
- [ ] **`inf + w` overflow** — safe in Python; guard `dist[i][k] != inf` in
      fixed-width languages (and it's a nice `O(V²)` speedup anyway).

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **"For every pair" / "for every node, something about all others" + small `V`
   → Floyd-Warshall.** Three loops, `k` outermost, `O(V³)`.
2. **Floyd-Warshall then aggregate** — the all-pairs matrix is often just an
   intermediate; the real answer is a count / min / max over it.
3. **Tie-break by index via `<=` and loop direction** — a clean idiom: `<=` +
   ascending loop keeps the largest tying index; `<` + ascending keeps the
   smallest.
4. **Floyd-Warshall vs Dijkstra-per-source** — dense/small → Floyd-Warshall;
   sparse/large → Dijkstra ×V.

| Problem | How this transfers |
|---|---|
| "Shortest path between many arbitrary pairs, small graph" | Floyd-Warshall once, `O(1)` per query |
| "Graph diameter / radius / center" | all-pairs distances, then max/min over rows |
| Evaluate Division (many queries) | Floyd-Warshall-style all-pairs propagation |
| "Transitive closure" (reachability of all pairs) | Floyd-Warshall with `or`/`and` instead of `min`/`+` |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "`n` is now `2000`."

- **(b) Pattern:** `O(n³) = 8·10⁹` is too slow. Switch to Dijkstra per source.
- **(c) Adapt:** run Dijkstra from each of the `n` cities: `O(V·(V + E) log V)`.
  On a sparse graph (`E ≈ V`) that's `O(V² log V) ≈ 2000² · 11 ≈ 4·10⁷` — fine.
  Only the source loop and the per-city count change; the argmin logic is the
  same.
- **(d) Say:** "Floyd-Warshall's `O(V³)` breaks past a few hundred nodes — beyond
  that, Dijkstra from every source, which is `O(V² log V)` on a sparse graph."

### Scenario 2 — "Also return, for the chosen city, the **list** of its within-threshold neighbors."

- **(b) Pattern:** same computation, just collect instead of count.
- **(c) Adapt:** once `best_city` is found, `neighbors = [j for j in range(n) if
  j != best_city and dist[best_city][j] <= threshold]`. `O(V)` extra.
- **(d) Say:** "The distance matrix already has it — one more row scan to list
  the qualifying `j`s."

### Scenario 3 — "Edges get added/removed over time; re-answer after each change."

- **(b) Pattern:** incremental all-pairs shortest path.
- **(c) Adapt:** an **edge addition** `(u, v, w)` can be folded into an existing
  Floyd-Warshall matrix in `O(V²)`: `for i, j: dist[i][j] = min(dist[i][j],
  dist[i][u] + w + dist[v][j], dist[i][v] + w + dist[u][j])`. **Edge removal /
  weight increase** has no cheap incremental update — you recompute from scratch
  (`O(V³)`) or maintain a more complex dynamic structure. Then redo the `O(V²)`
  count.
- **(d) Say:** "Additions splice into the matrix in `O(V²)`; removals force a
  full `O(V³)` recompute — there's no cheap decremental all-pairs update in
  general."

### Scenario 4 — "Roads are **one-way** (directed)."

- **(b) Pattern:** same algorithm, directed init.
- **(c) Adapt:** set only `dist[u][v] = w` (not the reverse) during init.
  Floyd-Warshall works identically on directed graphs. The "neighbors within
  threshold" count now means "cities *reachable from* `i` within threshold" (or
  *to* `i`, depending on the phrasing — clarify).
- **(d) Say:** "Directed only changes the matrix initialization; Floyd-Warshall
  itself is direction-agnostic."

### Scenario 5 — "Some roads have **negative** length (a scenic detour that's 'worth' negative miles)."

- **(b) Pattern:** Floyd-Warshall handles negative edges natively; watch for
  negative cycles.
- **(c) Adapt:** no code change for negative *edges*. After the algorithm, check
  the diagonal: `any(dist[i][i] < 0)` ⟹ a negative cycle exists, and "distance"
  is undefined for pairs that can route through it — decide with the interviewer
  whether to report that or clamp.
- **(d) Say:** "Negative edges are fine for Floyd-Warshall; I'd add a diagonal
  check afterward — `dist[i][i] < 0` flags a negative cycle."

### Scenario 6 — "Instead of the fewest neighbors, find the city that **minimizes the maximum** distance to any other city it can reach (the graph's center)."

- **(b) Pattern:** same all-pairs matrix, different aggregate — **eccentricity**.
- **(c) Adapt:** for each city `i`, `ecc[i] = max(dist[i][j] for reachable j)`.
  Return the `i` minimizing `ecc[i]` (that's the graph's *center*; `min ecc` is
  the *radius*, `max ecc` the *diameter*). `O(V²)` over the matrix.
- **(d) Say:** "Swap 'count within threshold' for 'max distance in the row' — the
  min over those is the graph center; it's the same matrix, a different
  reduction."

---

## 15. Flashcards

**Q:** When is Floyd-Warshall the right tool?
**A:** You need shortest distances between **all pairs** and `V` is small
(`≤ ~500`, comfortably at `≤ 100`). Three nested loops, `O(V³)`.

**Q:** The loop order — and why it matters?
**A:** `k` (intermediate node) **outermost**, then `i`, then `j`. `k` inside
breaks the "using only nodes `≤ k`" invariant → wrong answers.

**Q:** The relaxation?
**A:** `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.

**Q:** How do you break ties toward the **largest** index?
**A:** Iterate `i` from `0` upward and use `<=` (not `<`) when updating the best.

**Q:** Time and space?
**A:** `O(V³)` time, `O(V²)` space.

**Q:** `n = 2000` — what changes?
**A:** `O(V³)` is too slow; run Dijkstra from each source instead
(`O(V·(V+E) log V)`).

**Q:** Negative edges? Negative cycles?
**A:** Negative edges are fine. A negative cycle shows up as `dist[i][i] < 0` —
check the diagonal afterward.

**Q:** Same matrix, "minimize the max distance to any city" instead?
**A:** Compute each row's max (eccentricity); the min over those is the graph
center.
