# Graphs — End-to-End Google Interview Prep

This repo teaches you **graph data structures and algorithms from zero**, in very
simple English, with one consistent code style, so that after reading it once you
can fall back to any file and recall the whole idea in a few minutes.

You have **no prior graph experience** and **no prior Python experience** — that is
assumed everywhere. Nothing is skipped as "obvious".

---

## How to use this repo (your 5-day plan)

You are spending 5 focused days. Here is the route.

| Day | Read these | Goal |
|-----|-----------|------|
| **Day 1** | `concepts/01` → `concepts/05`, `concepts/17`, then pattern group **01** (grid flood-fill) and **02** (multi-source BFS) | Get comfortable with grids, BFS, DFS, and "counting components". This is 60% of easy/medium graph questions. |
| **Day 2** | Groups **03** (boundary DFS), **04** (connectivity), **05** (clone graph), **06** (topological sort) + `concepts/06`, `concepts/07` | Learn non-grid graphs, adjacency lists, and dependency ordering / cycle detection. |
| **Day 3** | Groups **07** (union-find), **08** (bipartite), **09** (weighted DFS) + `concepts/08`, `concepts/09` | Learn Disjoint Set Union — a second way to think about connectivity — and 2-coloring. |
| **Day 4** | Groups **10** (Dijkstra), **11** (Bellman-Ford / Floyd-Warshall), **12** (MST) + `concepts/10`–`concepts/14` | Shortest paths with weights, and minimum spanning trees. |
| **Day 5** | Groups **13** (implicit-graph BFS), **14** (Eulerian), **15** (bridges) + `concepts/15`, `concepts/16`. Then re-read `pattern-identification.md` and `flashcards.md` end to end. | Harder "hidden graph" problems and final pattern drilling. |

**Every day**: after reading a problem file, close it and try to re-derive the
approach out loud in 2 minutes. If you can't, read it again. That "explain it back"
habit is exactly what the interview tests.

---

## Repo layout

```
Graphs/
  README.md                    <- you are here
  pattern-identification.md     <- "given an unseen problem, which pattern is it?" decision tree
  flashcards.md                 <- every problem's flashcards in one place, for quick revision
  problem-sources.md            <- all 40 problems: which list each came from (LeetCode 150 /
                                 NeetCode 150 / Claude add), LeetCode #, and done/pending status

  concepts/                     <- the algorithm tutorials. Each has a short "Quick Card" + a full lesson.
    01-python-for-graphs.md
    02-graph-representations.md
    03-bfs.md
    04-dfs.md
    05-connected-components.md
    06-cycle-detection.md
    07-topological-sort.md
    08-union-find.md
    09-bipartite-coloring.md
    10-dijkstra.md
    11-bellman-ford.md
    12-floyd-warshall.md
    13-0-1-bfs.md
    14-mst-kruskal-prim.md
    15-bridges-articulation-tarjan.md
    16-bitmask-bfs.md
    17-complexity-analysis-for-graphs.md

  01-grid-flood-fill/ ... 15-bridges-articulation/
    README.md                  <- pattern cheat sheet for the group
    01-<problem>.md            <- the full teaching doc (15 fixed sections)
    01-<problem>.py            <- the same code, runnable:  python 01-<problem>.py
```

---

## The 15 pattern groups and their ~40 problems

| # | Pattern | Problems | Core tool |
|---|---------|----------|-----------|
| 01 | Grid flood-fill | Number of Islands, Flood Fill, Max Area of Island, Making a Large Island* | DFS/BFS on a grid, mark visited |
| 02 | Multi-source BFS on grid | Walls and Gates, 01 Matrix, Rotting Oranges, Shortest Bridge* | Push ALL sources into the queue first, then BFS |
| 03 | Boundary-anchored traversal | Pacific Atlantic Water Flow, Surrounded Regions | Start the search from the edges, invert the question |
| 04 | Graph traversal / connectivity | Find if Path Exists in Graph | Build adjacency list, one BFS/DFS |
| 05 | Hashmap + traversal (structural copy) | Clone Graph | Visited map = old node → new node |
| 06 | Topological sort / cycle detection | Course Schedule, Course Schedule II, Alien Dictionary, Minimum Height Trees*, Longest Increasing Path in a Matrix* | Kahn's BFS (indegree) or DFS post-order |
| 07 | Union-Find (Disjoint Set Union) | Redundant Connection, Graph Valid Tree, Number of Connected Components, Number of Provinces, Accounts Merge | `find` + `union` with path compression |
| 08 | Bipartite / 2-coloring | Is Graph Bipartite?, Possible Bipartition | BFS/DFS coloring neighbors the opposite color |
| 09 | Weighted DFS (ratio propagation) | Evaluate Division | DFS carrying a running product along edges |
| 10 | Dijkstra | Network Delay Time, Swim in Rising Water, Path With Minimum Effort, Number of Ways to Arrive at Destination* | Min-heap of (cost, node), pop smallest |
| 11 | Bellman-Ford / all-pairs | Cheapest Flights Within K Stops, Find the City With Smallest Number of Neighbors* | Relax all edges V−1 times / Floyd-Warshall triple loop |
| 12 | Minimum Spanning Tree | Min Cost to Connect All Points | Prim (heap) or Kruskal (sort edges + union-find) |
| 13 | Implicit-graph BFS | Snakes and Ladders, Minimum Genetic Mutation, Word Ladder, Shortest Path in Binary Matrix*, Word Ladder II*, Shortest Path Visiting All Nodes* | The graph is not given — you generate neighbors on the fly |
| 14 | Eulerian path / advanced DFS | Reconstruct Itinerary | Hierholzer's algorithm (DFS, add node to route on the way out) |
| 15 | Bridges / articulation points | Critical Connections in a Network | Tarjan: discovery time vs low-link |

`*` = supplementary problem added on top of your original 30 to close a known Google gap.

**Honest note on coverage.** Your original 30 covered ~85% of what Google asks in
graphs. The 10 starred problems close the remaining gaps: bridges (Tarjan), 0-1
BFS, DFS+BFS hybrids, DAG + memoization, BFS + bitmask state, Dijkstra + path
counting, all-pairs shortest path, and leaf-peeling topological sort. With all 40
you have full pattern coverage. If you run out of time, the 30 unstarred problems
are still the priority.

---

## House code style (read once — every file obeys this)

Consistency matters more than cleverness. The interviewer should see the *same*
clean habits in every answer. These are **our** rules; YouTube solutions will look
different — ignore theirs, follow ours.

### Imports (only the standard library, always these names)

```python
from collections import deque, defaultdict
import heapq
import sys
```

### Grids

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))          # down, up, right, left  (4-directional)
DIRS8 = ((1, 0), (-1, 0), (0, 1), (0, -1),
         (1, 1), (1, -1), (-1, 1), (-1, -1))        # add diagonals when the problem says "8-directional"

m, n = len(grid), len(grid[0])                       # m = rows, n = columns
```

Bounds check for a neighbor cell `(nr, nc)`:

```python
if 0 <= nr < m and 0 <= nc < n:
    ...
```

### BFS — always a `deque`, always mark visited **when you enqueue**

```python
q = deque([start])
seen = {start}
while q:
    node = q.popleft()
    for nei in neighbors(node):
        if nei not in seen:
            seen.add(nei)          # <-- mark HERE, not after popleft
            q.append(nei)
```

Marking when you enqueue (not when you dequeue) stops the same node being added to
the queue many times.

### DFS on a grid — recursion is our primary form

```python
def dfs(r, c):
    if not (0 <= r < m and 0 <= n and 0 <= c < n):   # off the board
        return
    if (r, c) in seen or grid[r][c] == "0":          # already done, or a wall
        return
    seen.add((r, c))
    for dr, dc in DIRS:
        dfs(r + dr, c + dc)
```

Recursion reads like a story ("visit me, then ask each neighbor to visit itself").
When the grid can be huge (about 10^6 cells or a very long path), Python's default
recursion limit (~1000) can crash. We then either raise it with
`sys.setrecursionlimit(10**6)` **or** switch to the iterative stack version, which
every file also shows.

### Non-grid graph — adjacency list is a `defaultdict(list)`

```python
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)            # both directions for an UNDIRECTED graph; only one line for DIRECTED
```

### Visited set

Primary: `seen = set()` holding node ids, or `(r, c)` tuples for grids.
Space-optimized alternative (shown per problem): overwrite the input grid in place
(e.g. set visited land to `"0"`).

### Dijkstra — min-heap of `(cost, node)`

```python
dist = {start: 0}
heap = [(0, start)]
while heap:
    d, node = heapq.heappop(heap)
    if d > dist.get(node, float("inf")):
        continue                                     # stale entry, skip
    for nei, w in graph[node]:
        nd = d + w
        if nd < dist.get(nei, float("inf")):
            dist[nei] = nd
            heapq.heappush(heap, (nd, nei))
```

### Union-Find — one class, copied verbatim into every union-find problem

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression (halving)
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                   # already connected -> this edge makes a cycle
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True
```

### Naming

`r, c` for a cell; `nr, nc` for a neighbor cell; `node`, `nei` for graph nodes;
`dist` for distances; `seen` for visited; `q` for a BFS queue; `indeg` for
indegree. Short, but always the same.

### Every `.py` file is runnable

Each solution file ends with:

```python
if __name__ == "__main__":
    sol = Solution()
    assert sol.method(sample_input) == expected
    print("all tests passed")
```

Run it with `python 01-number-of-islands.py`. Google now runs your code live, so we
practice with real, executing code every time.

---

## The fixed 15-section template (every problem file has exactly these, in order)

1. **Problem** — the statement in plain words + constraints + a worked example
2. **Explain Like I'm 5** — a real-world analogy
3. **Pattern Identification** — the signals that point to this pattern; look-alikes
4. **Intuition** — the core idea, built one sentence at a time
5. **Approach (primary)** — numbered steps in plain English
6. **Pseudocode** — language-neutral
7. **Dry Run** — a tiny input, traced step by step in a table
8. **Python Code** — the primary solution, `class Solution`, house style, + `__main__` tests
9. **Alternative Approach(es)** — the BFS↔DFS twin, and any other valid method
10. **Complexity** — time and space, *derived step by step*, with V and E defined for this problem
11. **Edge Cases** — and how the code handles each
12. **Debugging Checklist** — the bugs most likely in this exact problem
13. **Learnings & Transfer** — what it teaches, and which other problems reuse it
14. **Scenario-Based Questions (Google standard)** — 5+, each with how to adapt this solution
15. **Flashcards** — 6–10 quick Q/A pairs (also collected in `flashcards.md`)

---

## What Google actually grades (keep this in mind on every problem)

1. **Problem clarification** — restate it, ask about constraints, confirm examples *before* coding.
2. **Approach out loud** — name the pattern, state the plan, give complexity *before* writing code.
3. **Code quality** — clean names, small helper functions, no dead code, handles empty input.
4. **Debugging** — when a test fails, narrate how you localize the bug; don't just stare.
5. **Complexity** — not just the answer; *how you got it* (count work per node/edge).
6. **Follow-ups** — "what if the graph is weighted / huge / streaming / has negative edges?" Every problem file's section 14 rehearses these.
