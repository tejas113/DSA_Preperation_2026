# Concept 02 — What a graph is, and how we store it

## Quick Card

A **graph** = **nodes** (also called vertices) + **edges** (connections between
nodes).

- **Undirected** edge: friendship. If A–B, then B–A too.
- **Directed** edge: "A must happen before B". One-way.
- **Weighted** edge: the connection has a number (distance, cost, time).

Three ways to store it, plus "implicit":

| Storage | Shape | Space | "Are u and v connected?" | "Give me all neighbors of u" | Use when |
|---|---|---|---|---|---|
| **Adjacency list** | `defaultdict(list)`: node → list of neighbors | `O(V + E)` | `O(deg u)` | `O(deg u)` — fast | **almost always** |
| **Adjacency matrix** | `grid[u][v] = 1` (or weight) | `O(V²)` | `O(1)` | `O(V)` | dense graph, or you need instant edge lookup, or Floyd-Warshall |
| **Edge list** | `[(u, v), (u, v, w), ...]` | `O(E)` | `O(E)` | `O(E)` — slow | Kruskal / Bellman-Ford (they iterate edges anyway) |
| **Implicit** | no storage — a function generates neighbors | `O(1)` structural | — | compute on demand | Snakes & Ladders, Word Ladder, state puzzles |

`V` = number of nodes, `E` = number of edges, `deg u` = how many edges touch `u`.

Our default, every time unless a reason says otherwise: **adjacency list**.

```python
from collections import defaultdict
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)        # <- DELETE this line if the graph is DIRECTED
```

---

## Full tutorial

### 1. Picture it

```
Nodes: 0, 1, 2, 3
Edges (undirected): 0-1, 0-2, 1-2, 2-3

        0
       / \
      1---2
           \
            3
```

### 2. Adjacency list — a dictionary from each node to its neighbor list

```python
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1, 3],
    3: [2],
}
```

Every edge appears **twice** (once from each endpoint) because it's undirected.
Total length of all lists = `2E`. Plus `V` keys. So space is `O(V + E)`.

Building it from an edge list:

```python
edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
```

For a **directed** graph ("u points to v", e.g. "u is a prerequisite of v") you add
only one line:

```python
for u, v in edges:
    graph[u].append(v)          # only this direction
```

For a **weighted** graph, store pairs `(neighbor, weight)`:

```python
for u, v, w in edges:
    graph[u].append((v, w))
    graph[v].append((u, w))     # drop for directed
```

> ⚠️ **defaultdict gotcha:** if a node has *no* edges, it never becomes a key.
> When the problem numbers nodes `0..n-1`, prefer iterating `range(n)` over
> `graph` so you don't skip isolated nodes. Or pre-seed:
> `graph = {i: [] for i in range(n)}`.

### 3. Adjacency matrix — a V×V grid of 0/1 (or weights)

```python
adj = [[0] * n for _ in range(n)]
for u, v in edges:
    adj[u][v] = 1
    adj[v][u] = 1               # drop for directed
```

- `adj[u][v]` tells you in **O(1)** whether the edge exists.
- But it always uses `O(V²)` memory, even if there are only 3 edges.
- Getting all neighbors of `u` costs `O(V)` (scan the whole row).

Use it when: the graph is **dense** (`E` close to `V²`), OR the algorithm is
Floyd-Warshall (which is defined on a matrix), OR `V` is small (≤ ~500).

### 4. Edge list — just the raw list of connections

```python
edges = [(0, 1), (0, 2), (1, 2), (2, 3)]          # unweighted
edges = [(0, 1, 4), (0, 2, 1), (2, 3, 7)]         # weighted: (u, v, w)
```

You don't convert it to anything. Two algorithms *want* the edge list directly:

- **Kruskal's MST**: sort edges by weight, add them one by one.
- **Bellman-Ford**: loop over every edge, `V−1` times.

### 5. Implicit graph — the graph is never built

Sometimes the "nodes" are **states** and the "edges" are **rules**. You don't have
an `edges` array; you have a function that, given a state, returns the states you
can move to.

Examples:
- **Word Ladder**: node = a word. Neighbors of `"hit"` = every valid word that
  differs by one letter (`"hot"`, ...). You generate them by trying each position ×
  each letter `a..z`.
- **Snakes and Ladders**: node = a board square. Neighbors of square `s` =
  `s+1, s+2, ..., s+6`, then follow any snake/ladder.
- **Shortest Path Visiting All Nodes**: node = `(current node, set of visited
  nodes as a bitmask)`.

The traversal code (BFS/DFS) is identical — you just replace `for nei in graph[node]`
with `for nei in generate_neighbors(node)`.

### 6. Grid as a graph (the most common disguise)

A 2D grid **is** a graph:
- node = a cell `(r, c)`
- edge = "you can step to an adjacent cell" — usually the 4 orthogonal neighbors,
  sometimes 8 (with diagonals).

You never build an adjacency list for a grid. The neighbors are computed:

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
for dr, dc in DIRS:
    nr, nc = r + dr, c + dc
    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:   # in bounds AND walkable
        # (nr, nc) is a neighbor
```

For an `m × n` grid: `V = m*n` cells, `E ≈ 2*m*n` edges (each cell links to ~4
neighbors, each edge counted twice → ~2mn). So `O(V + E)` = `O(m*n)`. This is why
every grid BFS/DFS is `O(m*n)`.

### 7. Which representation does each of our patterns use?

| Group | Representation |
|---|---|
| 01, 02, 03 grid patterns | grid directly (implicit, computed neighbors) |
| 04 connectivity, 05 clone, 08 bipartite | adjacency list |
| 06 topological sort | adjacency list + an `indegree` array |
| 07 union-find | **no graph at all** — just the `DSU` arrays |
| 09 evaluate division | adjacency list with weights `(nei, ratio)` |
| 10 Dijkstra, 12 Prim MST | adjacency list with weights, + a heap |
| 11 Bellman-Ford, 12 Kruskal MST | edge list |
| 11 Floyd-Warshall | adjacency **matrix** |
| 13 implicit BFS | implicit — generate neighbors from a rule |
| 14 Eulerian | adjacency list (often sorted / as a heap per node) |
| 15 bridges | adjacency list |

### 8. Common conversions you'll write

**edges → adjacency list** (shown above, the one you'll write most).

**grid of "connections" → components**: don't convert; run flood fill directly.

**`isConnected[i][j]` matrix → adjacency list**:

```python
graph = defaultdict(list)
for i in range(n):
    for j in range(i + 1, n):
        if isConnected[i][j]:
            graph[i].append(j)
            graph[j].append(i)
```

(Number of Provinces gives you the matrix; you can either use it as-is or convert.)
