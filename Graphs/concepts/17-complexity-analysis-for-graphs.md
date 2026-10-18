# Concept 17 — How to derive time & space complexity for graph problems

Google grades *how you get* the complexity, not just the final `O(...)`. This file
teaches the derivation as a repeatable recipe. Every problem file's section 10 uses
it.

---

## Quick Card

**Recipe:**
1. Define `V` and `E` **for this specific problem** (what is a node? what is an edge?).
2. Time = (setup cost) + (traversal cost) + (per-node/per-edge extra work).
3. Space = (graph storage) + (visited structure) + (frontier: queue/stack/recursion) + (output).
4. Substitute the problem's numbers (grid → `V = m*n`, `E ≈ 4mn`; "complete graph" → `E = V²`).

**The five results you'll quote 90% of the time:**

| Algorithm | Time | Space |
|---|---|---|
| BFS / DFS (plain traversal) | `O(V + E)` | `O(V)` |
| BFS/DFS on `m×n` grid | `O(m*n)` | `O(m*n)` |
| Dijkstra (binary heap) | `O((V + E) log V)` | `O(V + E)` |
| Bellman-Ford | `O(V * E)` | `O(V)` |
| Union-Find (m ops) | `O(m * α(n)) ≈ O(m)` | `O(n)` |
| Topological sort (Kahn / DFS) | `O(V + E)` | `O(V + E)` |
| Floyd-Warshall | `O(V³)` | `O(V²)` |
| Kruskal MST | `O(E log E)` | `O(V + E)` |
| Prim MST (heap) | `O(E log V)` | `O(V + E)` |

---

## 1. Step one: name V and E for *this* problem

The same algorithm gives different final answers depending on what the nodes are.

| Problem | A node is... | An edge is... | V | E |
|---|---|---|---|---|
| Number of Islands | a grid cell | adjacency to a neighbor cell | `m*n` | `≈ 2mn` (each cell ~4 edges, halved) |
| Course Schedule | a course | a prerequisite pair | `numCourses` | `len(prerequisites)` |
| Word Ladder | a word | "differs by one letter" | `N` words | up to `N * L * 25` generated |
| Network Delay Time | a network node | a `(u, v, w)` time | `n` | `len(times)` |
| Clone Graph | a graph node | an undirected link | given `V` | given `E` |
| Accounts Merge | an email (or account) | "appears in the same account" | total emails | total emails (chain per account) |

**Always say this out loud first.** "Here a node is a cell, so `V = m*n`; each cell
has at most 4 neighbors so `E = O(m*n)`."

---

## 2. Step two: derive TIME as a sum of pieces

Write time as:

```
T = setup + traversal + per_element_work
```

### Piece A — setup (building the structure)

- Build adjacency list from an edge list: look at each edge once → `O(E)`.
- Build a `dist` grid of infinities: `O(V)` (or `O(m*n)`).
- Sort edges (Kruskal): `O(E log E)`.
- Nothing to build (implicit graph): `O(1)`.

### Piece B — the traversal itself

The key insight for BFS/DFS: **each node is processed once, each edge is examined a
constant number of times.**

- Why "once"? The `seen`/`visited` check stops repeats. A node enters the queue (or
  gets a `dfs` call) at most one time.
- Summing the neighbor loops over *all* nodes = summing every node's degree =
  `2E` for undirected, `E` for directed. So the neighbor scanning is `O(E)`, not
  `O(V * E)`.
- Total: `O(V) + O(E) = O(V + E)`.

**Common mistake:** thinking "for each of V nodes we loop over its neighbors, and a
node can have up to V neighbors, so it's `O(V²)`." That over-counts. The *sum* of
all neighbor-list lengths is `2E`, period. It's `O(V + E)`. (It only becomes `V²`
when `E` itself is `V²`, i.e. a complete/dense graph — then `O(V + E) = O(V²)` and
both statements agree.)

### Piece C — extra work per node or per edge

Multiply the traversal by whatever you do at each step:

- Heap push/pop in Dijkstra: `O(log V)` per edge relaxation → `O(E log V)`; plus
  `O(V log V)` for popping nodes → `O((V + E) log V)`.
- Generating neighbors in Word Ladder: for each word (`V`), try `L` positions ×
  `25` letters, each a set lookup `O(L)` → `O(V * L² * 25)` = `O(V * L²)`.
- Bellman-Ford: relax **all** `E` edges, and repeat `V - 1` times → `O(V * E)`.
- Floyd-Warshall: three nested loops over all nodes → `O(V³)`.

### Worked example: Dijkstra

```
setup:      build adjacency list            O(V + E)
traversal:  each node popped from heap once  V pops   × O(log V) = O(V log V)
            each edge triggers a heap push   E pushes × O(log V) = O(E log V)
total:      O(V + E) + O(V log V) + O(E log V) = O((V + E) log V)
```

(With a Fibonacci heap it's `O(E + V log V)`, but nobody expects that in an
interview — quote the binary-heap number.)

---

## 3. Step three: derive SPACE as a sum of pieces

```
S = graph_storage + visited + frontier + output + recursion
```

| Piece | Typical size |
|---|---|
| adjacency list | `O(V + E)` |
| adjacency matrix | `O(V²)` |
| `visited` / `seen` set or `dist` array | `O(V)` (grid: `O(m*n)`) |
| BFS queue | `O(V)` worst case (a star graph enqueues all neighbors at once; a grid can queue a whole diagonal `O(min(m,n))`, but `O(m*n)` is the safe bound) |
| DFS recursion stack | `O(V)` worst case (a path graph); grid: `O(m*n)` |
| heap (Dijkstra/Prim) | `O(E)` — a node can be pushed multiple times before it's finalized |
| output (e.g. the topological order, the cloned graph) | `O(V)` or `O(V + E)` |

Then take the max / sum. For plain BFS/DFS: `O(V)` (or `O(V + E)` if you also built
an adjacency list). For Dijkstra: `O(V + E)`.

**Don't forget:** if the problem says "don't count the output", drop that term. If
it says "in place", your `visited` might be `O(1)` extra (you overwrite the grid) —
mention that as the space-optimized version.

---

## 4. Substituting the problem's numbers

### Grid problems

```
V = m * n
E: each cell connects to ≤ 4 neighbors, each edge shared by 2 cells → E ≈ 2mn = O(m*n)
BFS/DFS: O(V + E) = O(m*n + m*n) = O(m*n)
space:   O(m*n)
```

### "Complete graph" / "every pair could connect" (Min Cost to Connect All Points)

```
V = n points
E = every pair = n(n-1)/2 = O(n²)
Prim with heap: O(E log V) = O(n² log n)
Kruskal:        O(E log E) = O(n² log n)
```

### "At most K stops" (Cheapest Flights)

```
Bellman-Ford limited to K+1 rounds:
  each round relaxes all E edges → O(E) per round
  K+1 rounds → O(K * E)
space O(V) for the two distance arrays
```

---

## 5. α(n) — the "almost constant" from Union-Find

`α(n)` is the *inverse Ackermann function*. For every `n` that fits in the
universe, `α(n) ≤ 4`. So union-find with **path compression + union by rank** does
each `find`/`union` in `O(α(n))`, which you may treat as `O(1)` amortized.

- `m` operations on `n` elements → `O(m α(n))` ≈ `O(m)`.
- In an interview say: "amortized near-constant per operation, so `O(E α(V))`,
  effectively `O(E)`."

---

## 6. Amortized vs worst-case (say the right word)

- **Amortized**: average over a sequence of operations, even if one operation is
  occasionally slow. Union-Find `find` is amortized `O(α(n))`. `deque.append` is
  amortized `O(1)`.
- **Worst-case per operation**: the single slowest one. A single `find` *before*
  compression can be `O(log n)`.

For Dijkstra, `O((V+E) log V)` is worst-case. For union-find, always say
"amortized".

---

## 7. A script you can say in the interview (fill in the blanks)

> "A node here is ___, so `V = ___`. An edge is ___, so `E = ___`.
> I build an adjacency list, `O(V + E)` time and space.
> The BFS visits each node once and scans each edge once, `O(V + E)`.
> I also do ___ per step, costing `O(___)`, so total time is `O(___)`.
> Space is the adjacency list `O(V + E)` plus the `visited` set `O(V)` plus the
> queue `O(V)`, so `O(V + E)`."

Practice saying that for every problem in this repo. It's worth as many points as
the code.

---

## 8. Quick self-test

1. BFS on a graph with `V = 1000`, `E = 3000`. Time? → `O(V + E) = O(4000)` → linear, `O(V+E)`.
2. Dijkstra, same graph. → `O((V+E) log V) ≈ O(4000 * 10)`.
3. Number of Islands, grid `300 × 400`. → `V = 120000`, `O(m*n)` time and space.
4. Course Schedule with 2000 courses, 5000 prereqs. → Kahn's BFS, `O(V + E) = O(7000)`.
5. Floyd-Warshall on 500 nodes. → `O(V³) = 1.25 × 10⁸` — borderline but usually fine; `O(V²)` space.
6. Union-Find, 10⁶ union calls on 10⁶ nodes. → `O(m α(n)) ≈ O(10⁶)`.
