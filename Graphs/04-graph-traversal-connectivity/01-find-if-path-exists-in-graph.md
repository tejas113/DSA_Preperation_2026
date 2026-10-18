# Find if Path Exists in Graph  ·  LeetCode 1971  ·  Easy

Group 04 — Graph Traversal / Connectivity  ·  your first **non-grid** graph.
Deliberately simple — the point of this problem is to nail the two-step ritual
every non-grid graph problem starts with, before the patterns get harder.

Prereqs: `concepts/01` (Python), `concepts/02` (graph representations —
especially "building an adjacency list from an edge list"), `concepts/03`/`04`
(BFS/DFS).

---

## 1. Problem

You have `n` nodes labeled `0` to `n-1`, and a list of **bidirectional** edges,
each `[u, v]` meaning there's an edge between `u` and `v`. Given a `source` node
and a `destination` node, **return `True` if there is a path between them,
`False` otherwise.**

Constraints:
- `1 <= n <= 2 * 10^5`.
- `0 <= edges.length <= 2 * 10^5`.
- No self-loops, no repeated edges.
- `0 <= source, destination <= n - 1`.

Example 1:

```
n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
answer = True     (0 -> 1 -> 2, or directly via the 0-2 edge)
```

Example 2:

```
n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
answer = False    (two separate components: {0,1,2} and {3,4,5})
```

---

## 2. Explain Like I'm 5

Imagine dots on paper with some strings tied between them. You put your finger on
dot `source` and want to know: **can I walk along the strings and reach dot
`destination`?** You don't care how many strings you cross or which route — just
whether *some* route exists.

Since there's no grid this time — just dots and strings — the first thing you do
is write down, for every dot, the list of dots it's directly tied to. Then you
start at `source` and walk to every dot you can reach, marking each as visited.
If `destination` ever gets marked, the answer is yes.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Input is edges/nodes, not a grid | ✅ |
| Plain yes/no reachability, no weights, no "shortest" | ✅ |
| Single source, single destination | ✅ |

**Reduce it to:** *"Build an adjacency list, run one BFS or DFS from `source`,
check if `destination` gets visited."*

**Look-alikes (previewing what's coming):**
- If this graph were built **incrementally**, or you had to answer **many**
  `(source, destination)` queries against the same fixed graph, you'd reach for
  **Union-Find** instead (Group 07) — see Scenario 1/2 below.
- If edges had **weights** and you needed "reachable within budget `B`", that's
  Dijkstra/Bellman-Ford territory (Groups 10/11) — see Scenario 6.

---

## 4. Intuition

1. There's no 2D array here — the graph is just a bunch of pairs. The very first
   thing to do, always, is turn that edge list into an **adjacency list**
   (`concepts/02`): a dict from each node to the list of nodes it directly
   connects to.
2. Once you have that, "is there a path from `source` to `destination`" is
   *exactly* the same question as "can BFS/DFS starting at `source` ever visit
   `destination`" — no different from any grid traversal, just `graph[node]`
   instead of "4 grid neighbors."
3. `source == destination` is trivially `True` — a node always has a (length-0)
   path to itself, even with zero edges. Notice this falls out automatically:
   BFS starts with `source` in `seen`/the queue, and the very first thing it does
   is check whether the popped node equals `destination`.

---

## 5. Approach (primary): build adjacency list, one BFS

1. `graph = defaultdict(list)`; for each `(u, v)` in `edges`: append `v` to
   `graph[u]` **and** `u` to `graph[v]` (undirected — both directions).
2. `seen = {source}`, `q = deque([source])`.
3. While `q`: pop `node`. If `node == destination`: return `True`. Otherwise, for
   each `nei` in `graph[node]` not yet in `seen`: mark it seen, push it.
4. If the loop finishes without finding `destination`: return `False`.

Builds on: `concepts/02` (adjacency list construction), `concepts/03` (BFS core).

---

## 6. Pseudocode

```
function validPath(n, edges, source, destination):
    graph = empty adjacency list
    for (u, v) in edges:
        graph[u].append(v)
        graph[v].append(u)

    seen = {source}
    q = queue([source])
    while q not empty:
        node = dequeue
        if node == destination: return True
        for nei in graph[node]:
            if nei not in seen:
                seen.add(nei)
                enqueue nei

    return False
```

---

## 7. Dry Run

```
n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
```

`graph = {0: [1, 2], 1: [0, 2], 2: [1, 0]}`.

| pop | == destination(2)? | neighbors examined | newly seen | queue after |
|---|---|---|---|---|
| 0 | no | 1 (new), 2 (new) | 1, 2 | [1, 2] |
| 1 | no | 0 (seen), 2 (seen) | — | [2] |
| 2 | **yes** → return `True` | | | |

Return **True**. ✅

Second example: `n=6, edges=[[0,1],[0,2],[3,5],[5,4],[4,3]], source=0, destination=5`.
`graph = {0:[1,2], 1:[0], 2:[0], 3:[5,4], 5:[3,4], 4:[5,3]}`. BFS from `0` only
ever reaches `{0,1,2}` — `5` is in a completely separate component `{3,4,5}` — the
queue empties without ever popping `5`. Return **False**. ✅

---

## 8. Python Code (primary — adjacency list + BFS)

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        seen = {source}
        q = deque([source])
        while q:
            node = q.popleft()
            if node == destination:      # covers source == destination too, on the first pop
                return True
            for nei in graph[node]:
                if nei not in seen:
                    seen.add(nei)
                    q.append(nei)

        return False


if __name__ == "__main__":
    sol = Solution()

    assert sol.validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2) is True
    assert sol.validPath(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5) is False
    assert sol.validPath(1, [], 0, 0) is True        # single node, trivially reaches itself
    assert sol.validPath(2, [], 0, 1) is False        # no edges, two isolated nodes
    assert sol.validPath(5, [[0, 1], [1, 2], [2, 3], [3, 4]], 0, 4) is True   # a chain

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS instead of BFS

```python
def validPath(self, n, edges, source, destination):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    seen = set()

    def dfs(node):
        if node == destination:
            return True
        seen.add(node)
        for nei in graph[node]:
            if nei not in seen and dfs(nei):
                return True
        return False

    return dfs(source)
```

Equally correct — pure reachability, no shortest-path requirement. **Caution:**
`n` can be up to `2 * 10^5`; a long chain graph (`0-1-2-...-199999`) recurses
`200,000` deep, far past Python's default recursion limit (~1000). Either raise
`sys.setrecursionlimit` or, safer, use the iterative BFS/DFS (primary/9c).

### 9b. Union-Find (foreshadowing Group 07 — the right tool for repeated queries)

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


class SolutionDSU:
    def validPath(self, n, edges, source, destination):
        dsu = DSU(n)
        for u, v in edges:
            dsu.union(u, v)
        return dsu.find(source) == dsu.find(destination)
```

For a **single** query on a **static** graph, this and BFS/DFS are both
`O(V + E)` — no real advantage either way. Union-Find's real strength shows up in
Scenario 1 and 2 below: many queries, or edges arriving incrementally.

### 9c. Iterative DFS (explicit stack) — avoids both recursion limit and BFS's queue if you prefer a stack

```python
def validPath(self, n, edges, source, destination):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    stack = [source]
    seen = {source}
    while stack:
        node = stack.pop()
        if node == destination:
            return True
        for nei in graph[node]:
            if nei not in seen:
                seen.add(nei)
                stack.append(nei)
    return False
```

### The BFS↔DFS answer the interviewer wants

> "Pure reachability, so BFS and DFS are equally valid — both `O(V+E)`. I'd use
> BFS (or iterative DFS) rather than recursive DFS here specifically because `n`
> can be `2×10^5` and a long chain graph would blow Python's recursion limit.
> If this were a *static* graph answering *many* connectivity queries, I'd
> switch to Union-Find instead, to pay the `O(V+E)` cost once and answer each
> query in near-`O(1)`."

---

## 10. Complexity — derived step by step

**V and E:** node = a graph node, `V = n`; edge = a given pair, `E =
len(edges)`.

**Time:**
- Building the adjacency list: one pass over `edges` → `O(E)`.
- BFS/DFS: each node visited at most once (`seen` check), each edge examined a
  constant number of times → `O(V + E)`.
- **Total: `O(V + E)`.**

**Space:**
- Adjacency list: `O(V + E)`.
- `seen` + queue/stack: `O(V)`.
- **Total: `O(V + E)`.**

Union-Find variant: `O(E * α(V))` to process all unions (effectively `O(E)`),
`O(V)` space for the DSU arrays.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `source == destination` | first pop immediately matches → `True`, even with zero edges |
| `edges = []` | adjacency list is empty; only `source == destination` returns `True` |
| Disconnected components | BFS/DFS from `source` simply never reaches `destination` → `False` |
| `n = 1` | only node `0`; `source = destination = 0` → `True` |
| Very sparse graph, large `n` | `defaultdict` only ever creates entries for nodes that appear in `edges` — no wasted `O(n)` allocation for untouched nodes |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Forgetting the reverse direction** — `graph[v].append(u)` — for this
      *undirected* graph. Without it, you've built a directed graph by accident;
      reachability can silently fail in one direction.
- [ ] **Recursion depth** if using recursive DFS on a long chain — `n` up to
      `2×10^5` can exceed Python's default limit. Use BFS or iterative DFS, or
      raise the limit explicitly.
- [ ] **Checking `destination in seen` only after the whole traversal**, instead
      of short-circuiting the moment it's found — not wrong, just slower than
      necessary (still `O(V+E)`, just doesn't exit early).
- [ ] **Assuming a `list`-based adjacency (`graph = [[] for _ in range(n)]`)
      always beats `defaultdict`** — fine here (`n ≤ 2×10^5`), but breaks down
      the moment `n` is very large and sparse (Scenario 5) since it force-
      allocates `O(n)` regardless of how many nodes actually appear in edges.

---

## 13. Learnings & Transfer

**The reusable core: the two-step non-grid-graph ritual.**

1. **Build the adjacency list** from whatever raw form the input takes (edge
   list, matrix, pairs).
2. **Run the traversal you already know** (BFS/DFS) — `graph[node]` stands in
   for "neighbors," exactly like a grid's `DIRS`.

Every problem from here through Group 15 starts this way; only the traversal
*details* (weights, direction, what "visited" means) change.

| Situation | How this transfers |
|---|---|
| Many connectivity queries on a fixed graph | Union-Find (Group 07) — pay `O(E)` once, each query near-`O(1)` |
| Edges arrive incrementally | Union-Find again — `union` as each edge arrives |
| Directed edges | drop the reverse `append` — everything else is unchanged |
| Weighted "reachable within budget" | Dijkstra/Bellman-Ford (Groups 10/11) instead of a plain BFS/DFS |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The graph is fixed, but you'll receive 100,000 separate `(source, destination)` queries against it. Answer each quickly."

- **(b) Pattern:** repeated connectivity queries on a **static** graph →
  **Union-Find**, precomputed once.
- **(c) Adapt:** build a `DSU` and `union` every edge **once**, `O(E α(V))`. Each
  query becomes `dsu.find(source) == dsu.find(destination)`, `O(α(V))` — instead
  of paying a fresh `O(V+E)` BFS per query, which would be `O(queries × (V+E))`
  overall.
- **(d) Say:** "One BFS per query is fine for a single question; the instant you
  have many queries against a graph that isn't changing, precompute connectivity
  once with Union-Find and answer each query in near-constant time."

### Scenario 2 — "Edges are added one at a time (a growing network), and after each addition you must answer whether `source` and `destination` are connected *at that moment*."

- **(b) Pattern:** **incremental** connectivity → Union-Find's ideal use case.
- **(c) Adapt:** maintain one `DSU` across the whole stream; `union` each new
  edge as it arrives (`O(α(V))` amortized), and answer each connectivity check
  with two `find` calls. Re-running BFS from scratch after every single edge
  addition would cost `O(edges × (V+E))` — Union-Find keeps it near `O(edges ×
  α(V))`.
- **(d) Say:** "Incrementally growing graphs are exactly what Union-Find is
  built for — it was designed around 'edges arrive one at a time, answer
  connectivity as you go.'"

### Scenario 3 — "The edges are actually directed (one-way streets) — does a path exist from `source` to `destination`?"

- **(b) Pattern:** same traversal, one-line change; and a note on Union-Find's
  limits.
- **(c) Adapt:** drop the reverse append (`graph[v].append(u)`) — only add
  `graph[u].append(v)`. BFS/DFS otherwise unchanged. **Union-Find does not apply
  here** — DSU models symmetric "same group" relationships and can't represent
  one-way reachability (it would incorrectly report `B` reaches `A` whenever `A`
  reaches `B`). For directed reachability, always fall back to BFS/DFS (or, for
  more advanced directed connectivity questions, condense the graph into
  strongly connected components first).
- **(d) Say:** "Union-Find is fundamentally an *undirected* equivalence-class
  tool — the moment edges become directed, that tool no longer applies, and you
  go back to BFS/DFS."

### Scenario 4 — "Return the actual path (sequence of nodes) from `source` to `destination`, not just whether one exists."

- **(b) Pattern:** BFS/DFS + **parent pointers**, the same trick used repeatedly
  in Groups 02–03.
- **(c) Adapt:** maintain `parent = {source: None}`; whenever you mark a new node
  seen via `nei`, set `parent[nei] = node`. Once `destination` is found, walk
  `parent` backward from `destination` to `source` and reverse the collected
  list. `O(V+E)` time and space, same as before.
- **(d) Say:** "Reachability becomes an actual path for free by recording one
  parent pointer per discovery, same as every other 'give me the path, not just
  the yes/no' variant we've seen."

### Scenario 5 — "`n` can be up to `10^9` (node ids are conceptual/sparse), but at most `2 × 10^5` edges are ever given — most possible nodes never appear at all."

- **(b) Pattern:** a check that your solution doesn't secretly assume a dense
  `0..n-1` array.
- **(c) Adapt:** the primary solution already handles this correctly —
  `defaultdict(list)` and a `set` for `seen` only ever create entries for node
  ids that actually appear in `edges` or get visited; there's no `O(n)`
  preallocated array anywhere. If `source` or `destination` never appear in any
  edge, the algorithm still works (their `graph[node]` is simply empty).
- **(d) Say:** "Dict/set-based graph structures scale to sparse, huge id-spaces
  automatically — this is exactly why we default to `defaultdict` and `set`
  instead of arrays sized by `n`, unless the problem guarantees `n` is small and
  dense."

### Scenario 6 — "Edges have a toll cost. Determine if `source` can reach `destination` while spending at most budget `B` in total tolls."

- **(b) Pattern:** no longer plain reachability — a **weighted** shortest-cost
  question. This is Dijkstra/Bellman-Ford territory (Groups 10/11), not Group 04.
- **(c) Adapt:** run Dijkstra from `source` (non-negative weights assumed) to get
  the cheapest cost to every node; the answer is
  `cheapest_cost[destination] <= B` (if the *cheapest* path exceeds `B`, no path
  can be within budget; if it doesn't, you're done — no need to enumerate other
  paths).
- **(d) Say:** "The moment 'is there a path' becomes 'is there a path *within a
  cost budget*,' the question upgrades from plain BFS/DFS reachability to a
  shortest-path algorithm — compute the cheapest cost once and compare it to the
  budget."

---

## 15. Flashcards

**Q:** The two-step ritual every non-grid graph problem starts with?
**A:** (1) Build an adjacency list from the edge list. (2) Run the BFS/DFS you
already know, using `graph[node]` instead of grid neighbors.

**Q:** Why does `source == destination` need no special case in the primary
code?
**A:** BFS starts with `source` in the queue; the very first pop checks
`node == destination`, which is immediately true.

**Q:** Time and space, with derivation?
**A:** `O(V + E)` both — build the adjacency list in `O(E)`, then BFS/DFS visits
each node once and each edge a constant number of times.

**Q:** When does Union-Find beat a fresh BFS/DFS for this exact question?
**A:** When there are many queries against a static graph, or edges arrive
incrementally — precompute once (`O(E α(V))`), each query/update is near-`O(1)`.

**Q:** Why doesn't Union-Find work for directed reachability?
**A:** DSU models symmetric "same group" equivalence classes; it can't represent
one-way ("A reaches B but not vice versa") relationships.

**Q:** Recursion risk in this exact problem, and why?
**A:** `n` up to `2×10^5` — a long chain graph recursed via DFS can exceed
Python's default recursion limit. Prefer BFS or iterative DFS.

**Q:** Weighted "reachable within budget B" — which group's tool applies?
**A:** Dijkstra/Bellman-Ford (Groups 10/11) — compute the cheapest cost to
`destination`, compare to `B`.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Adjacency list + BFS, marking visited on
enqueue — matches the primary solution exactly. `O(V + E)` time and space.

```python
class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:

        queue = deque()
        visited = set()
        visited.add(source)

        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        queue.append(source)

        while queue:
            ele = queue.popleft()
            if ele == destination:
                return True

            for i in graph[ele]:
                if i not in visited:
                    visited.add(i)
                    queue.append(i)

        return False
```

**Correct** — verified against all 5 tests from section 8. Note you also wrote up
a full worked example proving *why* marking visited at enqueue time (which this
code does) is necessary — that belongs to every BFS problem, not just this one,
so it's now recorded in `concepts/03-bfs.md`'s appendix rather than duplicated
here. Worth re-reading there before your next BFS problem.
