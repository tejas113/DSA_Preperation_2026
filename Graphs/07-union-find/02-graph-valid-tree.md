# Graph Valid Tree  ·  LeetCode 261  ·  Medium  ·  🔒 Premium

Group 07 — Union-Find  ·  a graph is a tree ⟺ **exactly `n-1` edges** *and*
**no cycle**. Two cheap checks; the second is Redundant Connection's `union`
failure.

> Premium on LeetCode — the `.md`/`.py` here run and are tested locally.

Prereqs: `concepts/08-union-find.md`, `01-redundant-connection.md`.

---

## 1. Problem

Given `n` nodes labeled `0..n-1` and a list of undirected `edges`, return whether
they form a **valid tree**.

A valid tree is: **connected** (every node reachable from every other) **and
acyclic** (no cycles).

Constraints:
- `1 <= n <= 2000`, `0 <= edges.length <= 5000`.
- No self-loops, no duplicate edges. Nodes are `0`-indexed.

Example 1:

```
n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
answer = True
```

Example 2:

```
n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
answer = False        # cycle 1-2-3-1
```

Example 3:

```
n = 4, edges = [[0,1],[2,3]]
answer = False        # two separate components, and only 2 edges (need 3)
```

---

## 2. Explain Like I'm 5

A tree of `n` dots is the tidiest possible way to connect them all: **just barely
connected, with nothing extra.**

- "Just barely" means **no loops** — you never connected two dots that were
  already reachable from each other.
- "Connected them all" means one single group at the end, no islands.

There's a magic number: a tree of `n` dots always has **exactly `n - 1`
strings**. Fewer, and some dot is left out (islands). More, and you must have
made a loop somewhere.

So the check is: **exactly `n - 1` strings, and no loop.** If both hold, it *must*
also be fully connected — you can't have `n - 1` strings, no loops, and still
have islands. Two checks give you all three properties.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Is this a valid tree?" (connected + acyclic) | ✅ |
| Undirected edges | ✅ → DSU applies |
| Need a cycle check | ✅ → `union` returning `False` |

**Reduce it to:** *"Return `False` if `len(edges) != n - 1`. Otherwise run a DSU
over all edges; return `False` on any `union` failure (cycle), else `True`."*

**The key fact:** for a graph with `n` nodes, **any two** of {connected, acyclic,
exactly `n-1` edges} imply the **third**. Check the two cheapest: the edge count
(`O(1)`) and "no cycle" (DSU, `O(E α(n))`).

**Look-alikes:**
- Redundant Connection — same `union`-failure cycle check, but there you're
  *given* a tree+1 and asked which edge; here you're validating from scratch.
- Number of Connected Components (next) — drops the acyclic requirement, just
  counts groups.

---

## 4. Intuition

1. A tree on `n` nodes has **exactly `n - 1` edges** — this is a definitional
   invariant. So `len(edges) != n - 1` → immediately not a tree. (`< n-1` →
   can't be connected; `> n-1` → must contain a cycle.)
2. Given the edge count *is* `n - 1`, the only remaining way to fail is a
   **cycle**. And if there's a cycle with only `n - 1` edges, the graph *must*
   also be disconnected (the edges "wasted" on the cycle can't reach everyone) —
   so detecting the cycle catches both failure modes at once.
3. Detect the cycle with a DSU: process edges; if `union(u, v)` returns `False`
   (`u`, `v` already connected), that edge closes a cycle → not a tree.
4. If the edge count is right and no `union` fails → connected + acyclic → valid
   tree.

---

## 5. Approach (primary): edge-count check + DSU cycle check

1. If `len(edges) != n - 1`: return `False`.
2. `dsu = DSU(n)` (0-indexed — size `n`, **not** `n + 1` like Redundant
   Connection).
3. For each `[u, v]`: if `dsu.union(u, v)` returns `False`: return `False`.
4. Return `True`.

Builds on: `concepts/08` (DSU), `01-redundant-connection.md` (the `union`-failure
= cycle idiom).

---

## 6. Pseudocode

```
function validTree(n, edges):
    if len(edges) != n - 1:
        return False                    # wrong count -> islands or a guaranteed cycle
    dsu = DSU(n)
    for [u, v] in edges:
        if union(u, v) == False:
            return False                # cycle
    return True                         # n-1 edges + no cycle => connected + acyclic
```

---

## 7. Dry Run

```
n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
```

`len(edges) == 5`, `n - 1 == 4` → **not equal**? Wait: `5 != 4` → return `False`
immediately.

Hmm — that's the wrong reason. Let's use a fair example where the count is right:

```
n = 4, edges = [[0,1],[1,2],[2,0],[... ]]   -> need exactly 3 edges
n = 4, edges = [[0,1],[1,2],[2,0]]           -> only 3 edges but a triangle + node 3 isolated
```

`len(edges) == 3 == n - 1` ✓. `DSU(4)`, `parent = [0,1,2,3]`.

| edge | find(u) | find(v) | union | parent after |
|---|---|---|---|---|
| [0,1] | 0 | 1 | `True` | `parent[1]=0` |
| [1,2] | find(1)→0 | 2 | `True` | `parent[2]=0` |
| [2,0] | find(2)→0 | 0 | **`False`** | — → **return `False`** |

The triangle `0-1-2-0` is a cycle, caught at the third edge. (Node `3` is also
isolated — but we never even get there; the cycle already disqualifies it.)

Now a valid one — `n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]`:

| edge | union | result |
|---|---|---|
| [0,1] | `True` | merge |
| [0,2] | `True` | merge |
| [0,3] | `True` | merge |
| [1,4] | `True` | merge |

`len(edges) == 4 == n - 1` ✓, no `union` failed → return `True`. ✅

---

## 8. Python Code (primary — edge count + DSU)

```python
from typing import List


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:              # O(1) early-out: wrong count -> not a tree
            return False

        dsu = DSU(n)                          # 0-indexed -> size n
        for u, v in edges:
            if not dsu.union(u, v):
                return False                  # cycle
        return True                           # n-1 edges + no cycle => valid tree


if __name__ == "__main__":
    sol = Solution()

    assert sol.validTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
    assert sol.validTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False   # cycle
    assert sol.validTree(4, [[0, 1], [2, 3]]) is False                            # disconnected
    assert sol.validTree(1, []) is True                                            # single node
    assert sol.validTree(2, []) is False                                           # disconnected
    assert sol.validTree(3, [[0, 1], [1, 2], [2, 0]]) is False                    # triangle
    assert sol.validTree(4, [[0, 1], [1, 2], [2, 3]]) is True                     # a path

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. BFS/DFS — edge count + connectivity

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False

        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        seen = {0}
        q = deque([0])
        while q:
            node = q.popleft()
            for nei in graph[node]:
                if nei not in seen:
                    seen.add(nei)
                    q.append(nei)

        return len(seen) == n            # reached everyone -> connected -> (with n-1 edges) a tree
```

Here the two checked properties are **edge count** + **connectivity**; the "no
cycle" falls out (`n - 1` edges + connected ⟹ acyclic). Same `O(V + E)`.

### The BFS↔DFS answer the interviewer wants

> "It's 'any two of {connected, acyclic, n-1 edges} imply the third.' I check the
> edge count (`O(1)`) plus one of the other two. DSU gives me the acyclic check
> naturally via `union` failures; BFS/DFS gives me connectivity via 'did I reach
> all `n` nodes.' Both are `O(V+E)`; I'd pick DSU here since it's the group's
> tool and the cycle check is a one-liner."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = len(edges)` (and we require `E = n - 1` to proceed).

**Time:**
- Edge-count check: `O(1)`.
- DSU pass: `n - 1` edges, one `union` (two `find`s) each, amortized `O(α(n))`.
- **Total: `O(n · α(n))` ≈ `O(n)`.**

**Space:**
- `parent` + `rank`: `O(n)`.
- **Total: `O(n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `n = 1`, `edges = []` | `len(edges) == 0 == n - 1` ✓; no edges to union → `True` |
| `n = 2`, `edges = []` | `0 != 1` → `False` (disconnected) |
| Exactly `n - 1` edges but a cycle exists (so also disconnected) | the `union` failure catches it |
| More than `n - 1` edges | `len(edges) != n - 1` → `False` (must contain a cycle) |
| Fewer than `n - 1` edges | `len(edges) != n - 1` → `False` (must be disconnected) |
| A simple path `0-1-2-3` | `n - 1` edges, no `union` failure → `True` |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Checking only "no cycle" without the edge count.** A disconnected forest
      (e.g. `n=4, edges=[[0,1],[2,3]]`) has no cycle but isn't a tree. You need
      **two** of the three properties.
- [ ] **Checking only connectivity without the edge count.** Redundant if you
      also check the count, but on its own it misses nothing *only* because the
      count check does the heavy lifting — always pair the count with one other.
- [ ] **`DSU(n + 1)` instead of `DSU(n)`.** This problem is **0-indexed** (unlike
      Redundant Connection). An extra unused slot is harmless but sloppy;
      undersizing would `IndexError`.
- [ ] **`n` edges instead of `n - 1`** in the count check.
- [ ] **Not handling `n = 1`.** Zero edges is *correct* for a one-node tree —
      `0 == 1 - 1` passes, so it's fine as long as you don't special-case it
      wrongly.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **"Tree" = connected + acyclic + exactly `n-1` edges — and any two imply the
   third.** Always check the two cheapest: edge count (`O(1)`) + one of the
   others.
2. **The `n - 1` edge count is a powerful `O(1)` invariant.** It shows up again
   in MST (every spanning tree of `n` nodes has exactly `n - 1` edges — Group 12).
3. **`union`-failure = cycle**, reused verbatim from Redundant Connection.
4. **"Any two of three properties imply the third"** is a recurring discrete-math
   shape — recognizing it lets you skip proving/checking the redundant one.

| Problem | How this transfers |
|---|---|
| Redundant Connection | the cycle-detection half |
| Number of Connected Components / Provinces | drop "acyclic," just count groups |
| Kruskal's MST (Group 12) | builds a spanning tree by adding `n-1` non-cycle-forming edges |
| "Is this a spanning forest?" | `union` every edge, reject cycle-forming ones; a forest has `n - (#components)` edges |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The edges are **directed**. Is it a valid **rooted tree** (arborescence): exactly one root with indegree 0, every other node indegree 1, all reachable from the root, no cycle?"

- **(b) Pattern:** DSU doesn't directly apply (directed). Check structural
  conditions + reachability.
- **(c) Adapt:** verify `len(edges) == n - 1`; compute indegrees — exactly one
  node with indegree `0` (the root), all others exactly `1`. Then BFS/DFS from
  that root; if it reaches all `n` nodes, it's a valid arborescence (the indegree
  conditions + `n-1` edges + full reachability rule out cycles). `O(V + E)`.
- **(d) Say:** "Directed 'tree' means arborescence — swap the DSU cycle check for
  indegree conditions plus a reachability BFS from the unique indegree-0 root."

### Scenario 2 — "Edges arrive one at a time. Maintain a **spanning forest**: accept an edge only if it doesn't create a cycle; reject (drop) the ones that would."

- **(b) Pattern:** DSU online — this is Kruskal's without the weight sort.
- **(c) Adapt:** keep one DSU across the stream. For each incoming edge, call
  `union`; if it returns `True`, the edge joined two trees — keep it; if `False`,
  it would close a cycle — drop it. After accepting `n - 1` edges with all nodes
  in one component, you have a spanning tree. `O(α(n))` per edge.
- **(d) Say:** "Incrementally building a spanning forest is just 'union each edge,
  keep it only if the union succeeded' — the exact skeleton of Kruskal's."

### Scenario 3 — "Given that it *is* a tree, answer many queries: what's the distance between nodes `a` and `b`?"

- **(b) Pattern:** a tree has a **unique path** between any two nodes — LCA /
  distance queries.
- **(c) Adapt:** one query: BFS/DFS from `a`, read off `dist[b]` — `O(n)`. Many
  queries: root the tree, precompute depths + a **binary-lifting LCA** table in
  `O(n log n)`; then `dist(a, b) = depth[a] + depth[b] - 2 * depth[lca(a, b)]` in
  `O(log n)` each. DSU can't give distances — it only knows "same component."
- **(d) Say:** "Tree distance is `depth[a] + depth[b] - 2·depth[LCA(a,b)]` —
  DSU is the wrong tool for distances; you want an LCA structure."

### Scenario 4 — "The graph may be a tree plus up to `K` extra edges. Determine whether deleting exactly `K` edges can make it a tree, and if so, which `K`."

- **(b) Pattern:** DSU, collect the `K` `union` failures.
- **(c) Adapt:** it's "tree + `K`" iff `len(edges) == n - 1 + K` and, running the
  DSU, you get **exactly `K`** `union` failures **and** the final structure is
  one component. The `K` failing edges are the ones to delete. `O(E α(n))`.
- **(d) Say:** "Each `union` failure is one redundant edge closing one cycle —
  collect exactly `K` of them, confirm one component remains, and those are the
  edges to cut."

### Scenario 5 — "`n` is `10^7`. Validate tree-ness at that scale."

- **(b) Pattern:** DSU is already essentially optimal.
- **(c) Adapt:** the edge-count check is `O(1)`. DSU with iterative `find`,
  array-backed `parent`/`rank`, is `O(E α(V)) ≈ O(E)` time and `O(V)` space.
  Fully scalable. (BFS/DFS is also `O(V + E)` but needs an adjacency list of size
  `O(V + E)`.)
- **(d) Say:** "Linear time, linear space, tiny constants — DSU with array
  parent/rank and iterative find handles `10^7` nodes without issue."

### Scenario 6 — "The edge set is a valid spanning tree of a **weighted** graph. Is it also the **minimum** spanning tree?"

- **(b) Pattern:** validity is this problem; minimality is the **cycle property**
  of MSTs.
- **(c) Adapt:** first confirm it's a valid spanning tree (`n - 1` edges,
  connected, acyclic). Then for **every non-tree edge** `(u, v, w)`: the maximum
  edge weight on the tree path from `u` to `v` must be `<= w` (otherwise you
  could swap that heavier tree edge out for `(u, v)` and get a lighter spanning
  tree). Answer the path-max queries with a DFS per edge (`O(E · n)`) or binary
  lifting (`O(E log n)`).
- **(d) Say:** "A spanning tree is minimum iff no non-tree edge is lighter than
  the heaviest edge on the tree path between its endpoints — that's the MST cycle
  property, checked with tree-path-max queries."

---

## 15. Flashcards

**Q:** A graph is a valid tree iff...?
**A:** It's connected **and** acyclic. Equivalently, it has exactly `n - 1` edges
and **any one** of {connected, acyclic}.

**Q:** The "any two imply the third" rule?
**A:** For `n` nodes, any two of {connected, acyclic, exactly `n-1` edges} imply
the third. Check the two cheapest: edge count (`O(1)`) + no-cycle (DSU).

**Q:** The primary check sequence?
**A:** `len(edges) != n - 1` → `False`. Else DSU over all edges; any `union`
failure → `False`; otherwise `True`.

**Q:** Why does `n - 1` edges + no cycle guarantee connectivity?
**A:** With `n - 1` edges and no cycle, if it were disconnected some component
would have a cycle (too many edges for its size) — contradiction. So it's
connected.

**Q:** Index base here vs Redundant Connection?
**A:** Graph Valid Tree is **0-indexed** → `DSU(n)`. Redundant Connection is
1-indexed → `DSU(n + 1)`.

**Q:** Time and space?
**A:** `O(n · α(n)) ≈ O(n)` time, `O(n)` space.

**Q:** BFS/DFS version — which two properties does it check?
**A:** Edge count (`O(1)`) + connectivity ("did I reach all `n` nodes from node
0"). Acyclicity follows.

**Q:** Given it's a tree, how do you get `dist(a, b)`?
**A:** `depth[a] + depth[b] - 2·depth[LCA(a, b)]` after rooting + binary-lifting
LCA preprocessing (`O(n log n)` prep, `O(log n)` per query). DSU can't do this.
