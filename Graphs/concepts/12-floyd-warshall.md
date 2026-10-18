# Concept 12 — Floyd-Warshall

## Quick Card

**All-pairs shortest paths** in one shot: `dist[i][j]` for *every* pair `(i, j)`.
Three nested loops. Handles negative edges (not negative cycles). `O(V³)` time,
`O(V²)` space — only practical for small `V` (roughly `≤ 500`).

```python
def floyd_warshall(n, edges):
    INF = float("inf")
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)          # keep the cheapest parallel edge
        dist[v][u] = min(dist[v][u], w)          # drop this line if directed

    for k in range(n):                            # intermediate node
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

**The invariant:** after the `k`-loop reaches value `k`, `dist[i][j]` is the
shortest path from `i` to `j` using only intermediate nodes from `{0, 1, ...,
k}`. After `k = n-1`, all nodes are allowed → true shortest paths.

**Reach for it when:** you need *many* shortest-path queries between arbitrary
pairs, `V` is small, and the code-simplicity is worth the `O(V³)`. Otherwise run
Dijkstra per source.

---

## Full tutorial

### 1. The idea: "am I allowed to route through node k?"

Process the intermediate nodes one at a time. When you "unlock" node `k`, check
for every pair `(i, j)` whether going `i → k → j` beats the best path found so
far (which only used nodes `< k` as intermediates):

```
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

`dist[i][k]` and `dist[k][j]` on the right-hand side are already correct for the
"nodes `< k` allowed" subproblem, and `k` itself appears only once on the path
`i → k → j` — so this correctly extends to "nodes `≤ k` allowed."

### 2. Loop order matters: `k` **must** be the outermost loop

`k` outermost is the whole algorithm. If you put `i` or `j` outside `k`, the
invariant breaks and you get wrong answers on some graphs. Memorize: **k, i, j**.

### 3. Initialization

- `dist[i][i] = 0`.
- `dist[u][v] = w` for each edge (take the `min` if parallel edges exist).
- Everything else `inf`.

### 4. Negative edges and negative cycles

Negative **edges** are fine. A negative **cycle** shows up as `dist[i][i] < 0`
for some `i` after the algorithm — check the diagonal to detect one. (With a
negative cycle, "shortest path" is undefined for any pair that can route through
it.)

### 5. Dry run

`n = 3`, edges (directed): `0→1 (3)`, `1→2 (1)`, `0→2 (10)`.

```
dist:
     0    1    2
0 [  0    3   10 ]
1 [ inf   0    1 ]
2 [ inf  inf   0 ]
```

- `k = 0`: routing through 0 helps no pair (nothing points *into* 0). Unchanged.
- `k = 1`: `dist[0][2]` = min(10, `dist[0][1] + dist[1][2]` = 3+1 = 4) → **4**.
- `k = 2`: routing through 2 helps no pair. Unchanged.

Final `dist[0][2] = 4` (path `0→1→2`). ✅

### 6. Path reconstruction (optional)

Keep `nxt[i][j]` = the first node after `i` on the shortest `i→j` path.
Initialize `nxt[i][j] = j` for each edge. When you relax via `k`, set `nxt[i][j]
= nxt[i][k]`. Reconstruct by following `nxt` from `i` to `j`.

### 7. Complexity — how to say it

> "Floyd-Warshall is three nested loops over all nodes — `O(V³)` time, `O(V²)`
> space for the distance matrix. It's the right call when `V` is a few hundred
> and I need many arbitrary-pair queries; beyond that I'd run Dijkstra per
> source (`O(V · (V+E) log V)`), which is better on sparse graphs."

### 8. Floyd-Warshall vs running Dijkstra V times

| | Floyd-Warshall | Dijkstra ×V |
|---|---|---|
| Time | `O(V³)` | `O(V·(V+E) log V)` |
| Negative edges | yes | no |
| Best when | dense, small `V`, simple code | sparse, larger `V`, non-negative |
| Space | `O(V²)` | `O(V²)` for the output |

On a **sparse** graph (`E ≈ V`), Dijkstra ×V is `O(V² log V)` — beats `O(V³)`.
On a **dense** graph (`E ≈ V²`), they're comparable and Floyd-Warshall's tiny
constant + trivial code often wins.

### 9. Common bugs

- [ ] **Wrong loop order** — `k` must be outermost.
- [ ] **`dist[i][i]` not set to 0.**
- [ ] **Not taking `min` for parallel edges** during init.
- [ ] **`inf + inf` / `inf + w`** — in Python it's `inf` and the `<` comparison
      is safe; in fixed-width languages, guard against overflow.
- [ ] **Using it when `V` is large** — `500³ = 1.25 × 10⁸` is borderline;
      `2000³` is `8 × 10⁹`, too slow.

### 10. Problems in this repo

Find the City With the Smallest Number of Neighbors at a Threshold Distance
(Group 11 — Floyd-Warshall is the natural fit); mentioned as an option in Network
Delay Time and Evaluate Division (many-query scenarios).
