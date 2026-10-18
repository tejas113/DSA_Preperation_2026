# Concept 11 — Bellman-Ford

## Quick Card

**Single-source shortest path that also works with negative edge weights**, and
that naturally supports a **hop limit** ("at most `K` edges"). Slower than
Dijkstra (`O(V·E)` vs `O((V+E) log V)`), but more general.

**Idea:** a shortest path has at most `V-1` edges. So relax **every edge**, and
repeat `V-1` times — after round `i`, every shortest path using `≤ i` edges is
correct.

```python
def bellman_ford(n, edges, src):
    dist = [float("inf")] * n
    dist[src] = 0
    for _ in range(n - 1):                # V-1 rounds
        changed = False
        for u, v, w in edges:             # relax every edge
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                         # converged early
    return dist
```

**Negative-cycle detection:** run one **extra** round. If any edge still relaxes,
a negative cycle is reachable from `src` — no finite shortest path exists.

**Hop-limited shortest path ("≤ K edges"):** run exactly `K` (or `K+1`) rounds,
relaxing against a **snapshot of `dist` from the start of the round** — so each
round adds at most one hop. This is the Cheapest-Flights pattern.

**Complexity:** `O(V·E)` time, `O(V)` space.

**Reach for Bellman-Ford when:** negative edge weights, or a **limit on the
number of edges/stops**, or you need negative-cycle detection. Otherwise (all
non-negative, no hop limit) prefer Dijkstra.

---

## Full tutorial

### 1. Why "relax every edge, V-1 times"

Any shortest path visits each node at most once, so it has at most `V-1` edges.
Claim: after `i` full rounds of "relax every edge," `dist[v]` is correct for
every `v` whose shortest path uses `≤ i` edges.

- Base: after 0 rounds, `dist[src] = 0` (0 edges) is correct.
- Step: if `v`'s shortest path is `src → ... → u → v` with `i` edges, then `u`'s
  shortest path has `i-1` edges and was correct after round `i-1`. Round `i`
  relaxes edge `(u, v)` and fixes `dist[v]`.

After `V-1` rounds, all shortest paths (`≤ V-1` edges) are correct.

### 2. Why Dijkstra fails with negative edges (and Bellman-Ford doesn't)

Dijkstra finalizes a node the first time it's popped, assuming no later path can
beat it — true only when remaining edges add `≥ 0`. A negative edge can undercut
a "finalized" distance. Bellman-Ford never finalizes anything early; it keeps
relaxing every edge until nothing changes.

### 3. Negative-cycle detection

If, after `V-1` rounds, a `V`-th round still relaxes some edge, then there's a
path with `≥ V` edges that's still improving — only possible if it loops through
a **negative-weight cycle**. Such a cycle makes "shortest path" meaningless
(you can loop forever getting cheaper).

```python
for u, v, w in edges:
    if dist[u] + w < dist[v]:
        return "negative cycle reachable from src"
```

### 4. The hop-limited variant (≤ K edges) — the key interview pattern

To answer "cheapest path from `src` to `dst` using **at most `K` edges**," run
exactly `K` rounds — but with a subtlety: within one round you must **not** let
an edge relaxed *this* round feed another relaxation *this* round (that would add
2+ hops in one round). Fix: relax against a **frozen copy** of `dist`:

```python
def cheapest_within_k_edges(n, edges, src, dst, K):
    dist = [float("inf")] * n
    dist[src] = 0
    for _ in range(K):                    # exactly K rounds -> at most K edges
        snapshot = dist[:]               # freeze this round's starting distances
        for u, v, w in edges:
            if snapshot[u] + w < dist[v]:
                dist[v] = snapshot[u] + w
        # (optional early exit if snapshot == dist)
    return dist[dst] if dist[dst] < float("inf") else -1
```

Each round extends every path by exactly one edge, so after `K` rounds `dist[v]`
= cheapest path to `v` using `≤ K` edges. (Cheapest Flights uses `K stops` = `K+1
edges`, so it runs `K+1` rounds.)

### 5. Dry run

Edges (directed): `0→1 (4)`, `0→2 (5)`, `1→2 (-3)`, `2→3 (2)`. Source `0`,
`n = 4`.

```
dist = [0, inf, inf, inf]
```

| round | relaxations | dist after |
|---|---|---|
| 1 | `0→1`: 0+4=4 ; `0→2`: 0+5=5 ; `1→2`: 4-3=1 < 5 ; `2→3`: 1+2=3 | [0, 4, 1, 3] |
| 2 | `0→1`: no ; `0→2`: no ; `1→2`: 4-3=1, no change ; `2→3`: 1+2=3, no change | [0, 4, 1, 3] |

Converged after round 2 (`changed == False`) → stop. `dist = [0, 4, 1, 3]`.
Dijkstra would have finalized `dist[2] = 5` on the first pop and missed the
`1→2 (-3)` shortcut.

### 6. SPFA (a faster Bellman-Ford in practice)

Queue-based Bellman-Ford: only re-relax edges out of nodes whose `dist` just
improved. Often much faster than `O(V·E)` on sparse graphs, though the worst case
is the same. Mention it exists; the plain version is fine for interviews.

### 7. Complexity — how to say it

> "Bellman-Ford relaxes all `E` edges `V-1` times, so `O(V·E)`. Space is `O(V)`
> for the distance array. One extra round detects a negative cycle. For a hop
> limit of `K`, run `K` rounds against a frozen copy of the distances each round,
> giving `O(K·E)`."

### 8. Common bugs

- [ ] **Hop-limited variant without the frozen copy** — relaxing against the
      live `dist` lets one round add multiple hops, undercounting stops.
- [ ] **Running `V` rounds instead of `V-1`** for the plain version (harmless but
      wasteful) — or `V-2` (wrong, misses the longest shortest paths).
- [ ] **Forgetting the negative-cycle check** when the problem allows negative
      weights.
- [ ] **Using it when Dijkstra would do** — `O(V·E)` can be far slower on large
      non-negative graphs.
- [ ] **`dist[u] + w` when `dist[u]` is `inf`** — in Python `inf + w` is `inf`,
      so the comparison is safe; in languages with fixed-width ints, guard
      `dist[u] != inf` first.

### 9. Problems in this repo

Cheapest Flights Within K Stops (hop-limited Bellman-Ford, Group 11); Network
Delay Time (Group 10 — shown as a Bellman-Ford alternative); the "negative edges"
scenario in several Dijkstra problems.
