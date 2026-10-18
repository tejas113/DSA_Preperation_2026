# Cheapest Flights Within K Stops  ·  LeetCode 787  ·  Medium

> 🔁 **Flagged for revision** — re-derive this from scratch on Day 5, don't
> recite it. The one sentence to hold onto: *"'K stops' means 'K+1 flights', so
> do K+1 rounds; in each round every city may take exactly **one** more flight,
> and the `snapshot` copy is what enforces 'exactly one' — you spend the fares
> that existed at the **start** of the round, not fares that arrived mid-round."*
> If that clicks, the rest is just Bellman-Ford. Everything below re-explains it
> from several angles.

Group 11 — Bellman-Ford / All-Pairs  ·  the problem that shows **why a hop limit
breaks plain Dijkstra**, and the fix: Bellman-Ford run for exactly `K+1` rounds
against a frozen copy of the distances.

Prereqs: `concepts/11-bellman-ford.md` (§4, the hop-limited variant),
`concepts/10-dijkstra.md` (for the contrast).

---

## 1. Problem

`n` cities `0..n-1`. `flights[i] = [from, to, price]` is a **directed** flight.
Given `src`, `dst`, and an integer `k`, **return the cheapest price from `src` to
`dst` using at most `k` stops**, or `-1` if no such route exists.

"At most `k` stops" = at most `k` intermediate cities = **at most `k + 1`
flights**.

Constraints:
- `1 <= n <= 100`, `0 <= flights.length <= n·(n-1)/2`.
- `1 <= price <= 10^4` (positive), `src != dst`, `0 <= k < n`.

Example 1:

```
n = 4
flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
src = 0, dst = 3, k = 1
answer = 700        # 0->1->3 costs 700 (1 stop).
                    # 0->1->2->3 costs 400 but is 2 stops > k.
```

Example 2: `src=0, dst=2, k=1` on `[[0,1,100],[1,2,100],[0,2,500]]` → `200`
(`0→1→2`, 1 stop). With `k=0` → `500` (direct).

---

## 2. Explain Like I'm 5

You want the cheapest plane ticket from city A to city B, but you're only willing
to change planes at most `k` times.

Imagine the cheapest fares "spreading" outward from A, **one flight per round**.
After round 1, you know the cheapest way to reach every city A flies to directly.
After round 2, the cheapest way using two flights. Do exactly `k + 1` rounds
(because `k` stops means `k + 1` flights), then read off the cheapest fare to B.

The catch: in one round you must only add **one** flight. If you let a fare that
just arrived this round immediately buy another flight *this same round*, you've
secretly used two flights in one round and might report a route with too many
stops.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Cheapest / shortest path" + **weighted** | ✅ |
| "**at most `k` stops / moves / edges**" cap | ✅ → this is the tell |
| Directed graph | ✅ |

**Reduce it to:** *"Bellman-Ford, exactly `k + 1` rounds. Each round relaxes
every flight against a **frozen snapshot** of `dist` from the round's start, so
each round adds at most one flight."*

**Why plain Dijkstra fails:** Dijkstra finalizes a city the first time it's
popped — by *cheapest fare*, ignoring stop count. The globally cheapest route to
`dst` might use too many stops, and a pricier-but-fewer-stops route is the real
answer. Dijkstra can't express "cheapest *among routes with ≤ k stops*" without
augmenting the state (Scenario / §9a).

---

## 4. Intuition

1. A route with "at most `k` stops" has at most `k + 1` flights.
2. Bellman-Ford's round `i` makes `dist[v]` correct for the cheapest route to `v`
   **using ≤ `i` flights** — exactly the quantity we want, with `i = k + 1`.
3. **The frozen snapshot** is the crux. Within one round, you relax against
   `snapshot` (the distances as they were when the round began), not the live
   `dist`. So a fare that lands at city `u` *this* round can't be spent on
   another flight *this* round — it has to wait for the next round. That's what
   keeps "one round = one flight."
4. After `k + 1` rounds, `dist[dst]` is the cheapest ≤ `k+1`-flight fare, or still
   `inf` (return `-1`).

---

## 5. Approach (primary): hop-limited Bellman-Ford

1. `dist = [inf] * n`; `dist[src] = 0`.
2. Repeat `k + 1` times:
   - `snapshot = dist[:]` (freeze this round's starting distances).
   - For each `[u, v, w]` in `flights`: if `snapshot[u] + w < dist[v]`, set
     `dist[v] = snapshot[u] + w`.
3. Return `dist[dst]` if it's finite, else `-1`.

Builds on: `concepts/11` §4 (hop-limited Bellman-Ford).

---

## 6. Pseudocode

```
function findCheapestPrice(n, flights, src, dst, k):
    dist = [inf] * n
    dist[src] = 0
    repeat (k + 1) times:
        snapshot = copy of dist                 # freeze -> one flight per round
        for [u, v, w] in flights:
            if snapshot[u] + w < dist[v]:
                dist[v] = snapshot[u] + w
    return dist[dst] if dist[dst] < inf else -1
```

---

## 7. Dry Run

```
n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
src = 0, dst = 3, k = 1   ->  k + 1 = 2 rounds
```

`dist = [0, inf, inf, inf]`.

**Round 1** — `snapshot = [0, inf, inf, inf]`:

| flight | `snapshot[u] + w` | `< dist[v]`? | dist after |
|---|---|---|---|
| 0→1 (100) | 0+100 = 100 | 100 < inf ✓ | dist[1] = 100 |
| 1→2 (100) | inf | no | — |
| 2→0 (100) | inf | no | — |
| 1→3 (600) | inf | no | — |
| 2→3 (200) | inf | no | — |

`dist = [0, 100, inf, inf]`.

**Round 2** — `snapshot = [0, 100, inf, inf]`:

| flight | `snapshot[u] + w` | `< dist[v]`? | dist after |
|---|---|---|---|
| 0→1 (100) | 100 | no | — |
| 1→2 (100) | 100+100 = 200 | 200 < inf ✓ | dist[2] = 200 |
| 2→0 (100) | inf (snapshot[2]) | no | — |
| 1→3 (600) | 100+600 = 700 | 700 < inf ✓ | dist[3] = 700 |
| 2→3 (200) | inf (snapshot[2]) | no | — |

`dist = [0, 100, 200, 700]`. Return `dist[3] = 700`. ✅

Notice: `2→3 (200)` did **not** fire in round 2, because `snapshot[2]` was still
`inf` (city 2 only got its price *during* round 2). Without the snapshot, we'd
have wrongly set `dist[3] = 200 + 200 = 400` — a 2-stop route, over the limit.

---

## 8. Python Code (primary — hop-limited Bellman-Ford)

```python
from typing import List


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        INF = float("inf")
        dist = [INF] * n
        dist[src] = 0

        for _ in range(k + 1):                  # at most k stops => at most k+1 flights
            snapshot = dist[:]                  # freeze -> each round adds one flight
            for u, v, w in flights:
                if snapshot[u] + w < dist[v]:
                    dist[v] = snapshot[u] + w

        return dist[dst] if dist[dst] != INF else -1


if __name__ == "__main__":
    sol = Solution()

    assert sol.findCheapestPrice(
        4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
    assert sol.findCheapestPrice(
        3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
    assert sol.findCheapestPrice(
        3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500
    assert sol.findCheapestPrice(
        3, [[0, 1, 2], [1, 2, 1], [2, 0, 10]], 1, 2, 1) == 1
    assert sol.findCheapestPrice(
        5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1]], 0, 4, 1) == -1   # needs 3 stops
    assert sol.findCheapestPrice(2, [[1, 0, 10]], 0, 1, 0) == -1           # no route

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Dijkstra with an augmented state `(cost, city, stops_used)`

Make the "node" the pair `(city, stops)`. Push `(0, src, 0)`; pop the cheapest.
If `city == dst`, return `cost`. If `stops <= k`, relax each outgoing flight to
`(cost + w, v, stops + 1)`.

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def findCheapestPrice(self, n, flights, src, dst, k):
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))

        heap = [(0, src, 0)]                    # (cost, city, stops used)
        best = {}                               # (city, stops) -> cheapest cost seen

        while heap:
            cost, city, stops = heapq.heappop(heap)
            if city == dst:
                return cost
            if stops > k:
                continue
            if best.get((city, stops), float("inf")) < cost:
                continue
            for nei, w in graph[city]:
                if cost + w < best.get((nei, stops + 1), float("inf")):
                    best[(nei, stops + 1)] = cost + w
                    heapq.heappush(heap, (cost + w, nei, stops + 1))
        return -1
```

Since we pop in cost order, the **first** pop of `dst` is the answer. More
flexible than Bellman-Ford (generalizes to weirder constraints), a bit more
fiddly to get right.

### 9b. DFS + memo on `(city, stops_remaining)`

`cheapest(city, left)` = cheapest fare from `city` to `dst` using `<= left` more
flights. `cheapest(dst, *) = 0`; recurse over outgoing flights with `left - 1`.
Memoize on `(city, left)`. `O(n · k · E / n) = O(k · E)`.

### The BFS↔DFS answer the interviewer wants

> "The 'at most k stops' cap is the tell — plain Dijkstra can't express
> 'cheapest among ≤ k-stop routes' without augmenting its state. Cleanest is
> Bellman-Ford for exactly `k + 1` rounds, relaxing against a frozen `dist` copy
> each round so a round can't chain two flights. Alternatively, Dijkstra where
> the state is `(city, stops)`."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = len(flights)`.

**Time:**
- `k + 1` rounds; each round copies `dist` (`O(V)`) and relaxes every flight
  (`O(E)`).
- **Total: `O((k + 1) · (V + E))` = `O(k · E)`** (since `E >= V - 1` for a
  connected-enough graph; more precisely `O((k+1)(V+E))`).

**Space:**
- `dist` + `snapshot`: `O(V)`.
- **Total: `O(V)`.** (The augmented-Dijkstra alternative is `O(V·k)` for the
  `best` map.)

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `k = 0` | one round → only direct `src → dst` flights count |
| No route within `k + 1` flights | `dist[dst]` stays `inf` → `-1` |
| `dst` reachable but only via more than `k` stops | those relaxations never happen within `k + 1` rounds → `-1` |
| A flight *out of* `dst` | irrelevant; we only read `dist[dst]` |
| `dist[u]` is `inf` during relaxation | Python `inf + w = inf`, comparison stays safe |
| Cycle in the flight graph (e.g. `2→0`) | harmless — the round cap prevents looping forever |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **No frozen snapshot** — relaxing against the live `dist` lets one round
      chain multiple flights, so you accept routes with more than `k` stops.
      Symptom: answer too cheap (e.g. `400` instead of `700` on Example 1). **The
      #1 bug.**
- [ ] **`k` rounds instead of `k + 1`.** "`k` stops" = "`k + 1` flights."
- [ ] **Copying the snapshot inside the flight loop** instead of once per round.
- [ ] **Forgetting the `-1` fallback** for unreachable `dst`.
- [ ] **Using plain Dijkstra** — finalizes by cost, ignores the stop count,
      returns the wrong (too-many-stops) route's price or misses the valid one.
- [ ] **Treating flights as undirected** — they're one-way.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Hop-limited shortest path = Bellman-Ford, exactly `K` rounds, relax against
   a frozen `dist` copy.** The frozen copy is what caps each round at one edge.
2. **"at most `K` stops / moves / edges / transfers" is the tell** for this
   pattern — not plain Dijkstra.
3. **A hop limit neutralizes negative cycles** — you can only take `K + 1`
   edges, so you can't loop a negative-weight cycle forever (Scenario 6).
4. **Augmenting the state** `(node) → (node, resource_used)` turns many
   "shortest path with a budget/limit" problems into ordinary Dijkstra on the
   bigger state space.

| Problem | How this transfers |
|---|---|
| "Minimum cost with at most `K` refuels/recharges" | state = `(node, refuels used)` |
| "Shortest path using at most `K` special edges" | state = `(node, special used)` |
| K-edge shortest path in a general graph | Bellman-Ford, `K` rounds, frozen copy |
| Cheapest path with a total-time budget | state = `(node, time bucket)` |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Remove the stop limit — just the cheapest fare `src → dst`."

- **(b) Pattern:** unconstrained weighted shortest path.
- **(c) Adapt:** prices are positive → **Dijkstra**, `O((V + E) log V)` — faster
  than a full Bellman-Ford (`O(V·E)`). If prices could be negative, full
  Bellman-Ford (`n - 1` rounds) + a negative-cycle check.
- **(d) Say:** "Drop the hop limit and it's back to a plain shortest path —
  Dijkstra for positive prices, Bellman-Ford if any are negative."

### Scenario 2 — "Return the actual itinerary (the list of cities), not just the price."

- **(b) Pattern:** parent pointers on the augmented state.
- **(c) Adapt:** use the `(city, stops)` Dijkstra (§9a) and record
  `parent[(v, s+1)] = (u, s)` on each improving relaxation. From `(dst,
  stops_when_first_popped)`, walk `parent` back to `src` and reverse. (Plain
  Bellman-Ford makes reconstruction awkward because a city's best predecessor
  changes by round.)
- **(d) Say:** "I'd switch to the state-augmented Dijkstra so I can hang a parent
  pointer on each `(city, stops)` state and reconstruct."

### Scenario 3 — "Flights also have a **duration**. Minimize price subject to total duration `<= T` and stops `<= k`."

- **(b) Pattern:** add a DP dimension.
- **(c) Adapt:** state `(city, stops, duration_used)`; `best[state]` = min price.
  Feasible only if `T` (or a bucketed version of it) is small enough that
  `n · k · T` states fit. If `T` is large/continuous, it's a genuinely harder
  constrained-shortest-path problem (weakly NP-hard) — mention Lagrangian
  relaxation or a pareto-frontier approach.
- **(d) Say:** "Each hard constraint adds a state dimension; it stays tractable
  only while the product of the dimensions is small — otherwise it's a
  constrained shortest path, which is NP-hard in general."

### Scenario 4 — "`k` can be as large as `n`, and `n = 10^5` cities with `10^6` flights."

- **(b) Pattern:** `O(k · E)` becomes `10^11` — too slow. Recognize when the cap
  is moot.
- **(c) Adapt:** if `k >= n - 1`, "at most `k` stops" imposes no real limit (a
  simple path has `< n` edges) → it's plain shortest path → **Dijkstra**
  `O((V + E) log V)`. For `k < n - 1` but large, `O(k · E)` is the honest bound;
  a **SPFA-style** Bellman-Ford (queue of improved nodes, only re-relax their
  edges) is far faster in practice on sparse graphs.
- **(d) Say:** "First check whether `k >= n - 1` — then the cap does nothing and
  it's just Dijkstra. Otherwise, SPFA to avoid touching every edge every round."

### Scenario 5 — "Round trip: cheapest `src → dst → src`, with at most `k` stops **each way**."

- **(b) Pattern:** two independent hop-limited searches.
- **(c) Adapt:** run hop-limited Bellman-Ford from `src` to get `out[dst]`; run
  it again on the **same** graph from `dst` to get `back[src]` (flights are
  directed, so this is a genuinely separate search, not just the reverse). Answer
  is `out[dst] + back[src]` (or `-1` if either leg is impossible). If the stop
  budget is *shared* across both legs, it's one search over `(city, leg,
  stops_used)`.
- **(d) Say:** "Independent per-leg budgets → two separate runs, sum the results.
  Shared budget → a single search with the leg folded into the state."

### Scenario 6 — "Some flights are **promotional** with a **negative** price (a fare credit)."

- **(b) Pattern:** Bellman-Ford handles negative weights natively — and the hop
  limit makes negative cycles harmless.
- **(c) Adapt:** no code change. The `snapshot`-based relaxation already works
  with negative `w`. A negative-weight cycle would normally make "cheapest" 
  undefined, but since you can take at most `k + 1` flights, you can't spin a
  negative cycle indefinitely — the answer stays well-defined.
- **(d) Say:** "This is exactly where Bellman-Ford earns its keep over Dijkstra —
  negative fares are fine, and the stop cap means a negative cycle can't be
  exploited forever, so the answer is still well-defined."

---

## 15. Flashcards

**Q:** What's the tell for the hop-limited Bellman-Ford pattern?
**A:** "Shortest / cheapest path" **+ "at most `K` stops / moves / edges."** Plain
Dijkstra can't express "cheapest among ≤ K-hop routes."

**Q:** How many rounds, and why the frozen snapshot?
**A:** `K + 1` rounds ("K stops" = "K+1 flights"). Relax against a copy of `dist`
from the round's start so a round can't chain two edges.

**Q:** The #1 bug, and its symptom?
**A:** No snapshot → one round chains multiple flights → accepts over-the-limit
routes. Symptom: answer too cheap.

**Q:** Why does plain Dijkstra fail here?
**A:** It finalizes a city by cheapest fare, ignoring stop count — the globally
cheapest route may exceed `k` stops, and a pricier valid route is the real
answer.

**Q:** Time and space?
**A:** `O((k + 1)(V + E))` = `O(k · E)` time, `O(V)` space.

**Q:** The augmented-Dijkstra alternative?
**A:** Make the state `(city, stops_used)`; run normal Dijkstra; first pop of
`dst` is the answer.

**Q:** Negative promotional fares — does it still work?
**A:** Yes — Bellman-Ford handles negatives, and the `k + 1`-flight cap means a
negative cycle can't be looped forever, so the answer stays well-defined.

**Q:** `k >= n - 1` — what does that mean?
**A:** The stop cap imposes no real limit (a simple path has `< n` edges) → it's
plain shortest path → use Dijkstra.
