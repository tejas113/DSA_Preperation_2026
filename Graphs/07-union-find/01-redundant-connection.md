# Redundant Connection  ·  LeetCode 684  ·  Medium

Group 07 — Union-Find  ·  the purest use of the killer DSU idiom: `union(u, v)`
returns `False` exactly when the edge `(u, v)` closes a cycle.

Prereqs: `concepts/08-union-find.md` (read it first — this problem is 4 lines on
top of the canonical `DSU` class).

---

## 1. Problem

You're given a graph that **started as a tree** with `n` nodes labeled `1..n`,
then had **one extra edge added**. The result has `n` nodes and `n` edges, and
exactly one cycle.

**Return an edge that can be removed to make it a tree again.** If several edges
would work, return the one that appears **last** in the input `edges` list.

Constraints:
- `n == edges.length`, `3 <= n <= 1000`.
- Nodes are `1`-indexed (`1..n`).
- The graph is connected and has exactly one cycle.

Example 1:

```
edges = [[1,2],[1,3],[2,3]]
answer = [2,3]     # 1-2-3-1 is the cycle; removing [2,3] leaves a tree
```

Example 2:

```
edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
answer = [1,4]     # the cycle is 1-2-3-4-1; [1,4] is the last of its edges in the input
```

---

## 2. Explain Like I'm 5

You have a bunch of islands and you build bridges between them one at a time. The
rule for a "tree" of islands: every island reachable, and no wasted bridges — you
never build a bridge between two islands that are *already* connected by some
other route.

Go through the bridges in the order they were built. For each one, check: are
these two islands **already connected** (by earlier bridges)? The first time the
answer is "yes, already connected," **that bridge is the wasted one** — it just
created a loop. That's the bridge to remove.

Because you check in build-order, the wasted bridge you find is the *last* bridge
of the loop to be built — which is exactly "the edge that appears last in the
input" that the problem asks for.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Undirected edges arriving **in order** | ✅ |
| "Which edge creates a cycle / is redundant?" | ✅ → `union` returning `False` |
| "Return the last such edge in input order" | ✅ → falls out for free (see §4) |

**Reduce it to:** *"Process edges in order with a DSU. Return the first edge
whose `union` returns `False` (endpoints already connected)."*

**Look-alikes:**
- Graph Valid Tree (next) — same cycle check, plus an edge-count check.
- **Redundant Connection II** (LC 685) — the *directed* version, genuinely harder
  (a node can end up with two parents) — Scenario 1.

---

## 4. Intuition

1. The graph is a tree plus one edge, so there is **exactly one cycle**.
2. Every edge *on that cycle* is a valid answer — remove any one and the cycle
   breaks, leaving a spanning tree.
3. Process edges left to right with a DSU. Each `union(u, v)`:
   - `True` → `u`, `v` were in different components; this edge genuinely connects
     them (a "tree" edge).
   - `False` → `u`, `v` were **already** connected; a path between them already
     exists, so this edge closes the cycle.
4. Since there's exactly one cycle, exactly **one** `union` call returns `False`,
   and it's the edge that "completes" the loop when the scan reaches it. All the
   *other* cycle edges were seen earlier and unioned successfully. So the first
   (and only) `union`-failure is automatically **the last cycle edge in input
   order** — exactly what the problem wants. No extra work needed.

---

## 5. Approach (primary): DSU, return the first `union` failure

1. `dsu = DSU(len(edges) + 1)` — nodes are `1..n`, so size `n + 1` and leave
   index `0` unused.
2. For each `[u, v]` in `edges` (in order): if `dsu.union(u, v)` returns `False`,
   **return `[u, v]`**.
3. (The problem guarantees exactly one cycle, so step 2 always returns.)

Builds on: `concepts/08` — literally the canonical `DSU` class + one loop.

---

## 6. Pseudocode

```
function findRedundantConnection(edges):
    dsu = DSU(len(edges) + 1)          # nodes are 1..n
    for [u, v] in edges:
        if union(u, v) == False:       # u and v already connected -> this edge is redundant
            return [u, v]
```

---

## 7. Dry Run

```
edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
```

`DSU(6)`, `parent = [0,1,2,3,4,5]`.

| edge | find(u) | find(v) | union | parent after |
|---|---|---|---|---|
| [1,2] | 1 | 2 | `True` | `parent[2]=1` |
| [2,3] | find(2)→1 | 3 | `True` | `parent[3]=1` |
| [3,4] | find(3)→1 | 4 | `True` | `parent[4]=1` |
| [1,4] | 1 | find(4)→1 | **`False`** | — → **return `[1,4]`** |

`[1,5]` is never processed. Answer: `[1,4]`. ✅

---

## 8. Python Code (primary — DSU)

```python
from typing import List


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]     # path compression
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                     # already connected -> cycle edge
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        dsu = DSU(len(edges) + 1)                # nodes are 1..n
        for u, v in edges:
            if not dsu.union(u, v):
                return [u, v]
        return []                                # unreachable given the problem's guarantee


if __name__ == "__main__":
    sol = Solution()

    assert sol.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert sol.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    assert sol.findRedundantConnection([[1, 2], [2, 3], [1, 3]]) == [1, 3]
    assert sol.findRedundantConnection([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]]) == [2, 5]
    assert sol.findRedundantConnection(
        [[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]) == [1, 3]

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS per edge (the "without DSU" version — correct but `O(E²)`)

Build the graph incrementally. Before adding edge `(u, v)`, run a DFS/BFS on the
graph built **so far** to check if `u` can already reach `v`. If yes, `(u, v)` is
the redundant edge.

```python
from collections import defaultdict
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        graph = defaultdict(set)

        def connected(u, v, seen):
            if u == v:
                return True
            seen.add(u)
            return any(connected(nei, v, seen) for nei in graph[u] if nei not in seen)

        for u, v in edges:
            if u in graph and v in graph and connected(u, v, set()):
                return [u, v]
            graph[u].add(v)
            graph[v].add(u)
        return []
```

Each connectivity check is `O(V + E)`; doing it per edge is `O(E · (V + E)) =
O(E²)`. Fine for `n ≤ 1000`, but DSU's `O(E · α(V)) ≈ O(E)` is the right answer,
and it's the one that scales (Scenario 6).

### The BFS↔DFS answer the interviewer wants

> "DSU is the natural fit — the `union` return value *is* a cycle detector, and
> processing edges in order means the first failure is exactly the last cycle
> edge in the input, which is what's asked. DFS-per-edge also works but is
> `O(E²)`. I'd code DSU."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = n` (a tree's `n-1` edges plus one).

**Time:**
- One pass over `n` edges. Each does one `union` = two `find`s = amortized
  `O(α(n))`.
- **Total: `O(n · α(n))` ≈ `O(n)`.**

**Space:**
- `parent` and `rank` arrays: `O(n)`.
- **Total: `O(n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| Smallest cycle (a triangle, `n = 3`) | first two edges union; third fails → returned |
| Redundant edge is the very last edge | scan reaches it, `union` fails, returned |
| Redundant edge is in the middle (Example 2) | earlier cycle edges union fine; the middle one fails |
| 1-indexed nodes | `DSU(n + 1)`, index `0` unused |
| Guaranteed exactly one cycle | exactly one `union` failure — no ambiguity |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Sizing the DSU as `DSU(n)` instead of `DSU(n + 1)`.** Nodes are `1..n`;
      `find(n)` would `IndexError`. Either size `n + 1`, or remap nodes to
      `0..n-1`.
- [ ] **Inverting the `union` return convention.** `True` = a real merge
      happened; `False` = already connected (this edge is redundant). Return on
      `False` / `not union(...)`.
- [ ] **Continuing the scan after the first failure and returning the last
      failure.** There's only one cycle, so only one failure — harmless here, but
      the *intent* is "return on first failure."
- [ ] **Returning a tuple `(u, v)` when the judge expects a list `[u, v]`** — or
      returning `[v, u]` in the wrong order. Return the edge as it appears in the
      input.
- [ ] **Recursive `find` without path compression** on a long chain — slow;
      use the iterative `while` form.
- [ ] **Forgetting path compression / union by rank entirely** — still correct,
      but `find` degrades toward `O(n)`; you lose the reason to use DSU.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **`union(u, v) == False` is a cycle detector** — the single most-used DSU
   idiom. If the endpoints were already connected, this edge closes a cycle.
2. **Process edges in order → the first cycle-closing edge is the last cycle
   edge in the input.** All other cycle edges were unioned before you reached it.
3. **DSU is the tool for incremental undirected connectivity** — `O(α(n))` per
   edge, versus re-running a search each time.

| Problem | How this transfers |
|---|---|
| Graph Valid Tree | same cycle check + "exactly `n-1` edges" check |
| Kruskal's MST (Group 12) | sort edges by weight, `union` each; skip the ones where `union` returns `False` (they'd close a cycle) |
| Number of Connected Components / Provinces | `count = n`, `count -= 1` per successful `union` |
| Cycle detection in any streaming undirected graph | report each `union` failure as it happens |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The graph is **directed** — it started as a rooted tree (every node has one parent except the root) plus one extra directed edge. Return the edge to remove." *(this is LeetCode 685)*

- **(b) Pattern:** the directed version needs a **3-case analysis**, because the
  extra edge can cause (a) a node with **two parents**, (b) a **cycle**, or (c)
  both.
- **(c) Adapt:** First scan for a node with indegree 2 → it has two candidate
  incoming edges, `cand1` (earlier) and `cand2` (later). Then:
  - If **no** node has two parents → it's a pure cycle; run part-I-style DSU and
    return the first `union` failure.
  - If a node has two parents → try building the DSU while **skipping `cand2`**.
    If that succeeds with no cycle, `cand2` is the answer. Otherwise the problem
    is in `cand1` (the two-parent edge plus a cycle), so return `cand1`.
- **(d) Say:** "Directed makes it a case split: two-parents, cycle, or both.
  Union-Find still does the cycle detection, but you first identify the
  two-parent candidate edges and test which one to drop."

### Scenario 2 — "There are **K** extra edges (K independent cycles), not just one. Return all K edges to remove."

- **(b) Pattern:** same DSU, collect **every** `union` failure.
- **(c) Adapt:** don't return on the first failure — append each failing edge to
  a result list and keep scanning. Each failure closes a distinct cycle (given
  the K extra edges each add an independent cycle). Return the list. Still
  `O(E · α(V))`.
- **(d) Say:** "One cycle → return the first `union` failure; K cycles → collect
  them all. The algorithm doesn't change, just when you stop."

### Scenario 3 — "Given a query `(a, b)`, is the edge `(a, b)` part of **the** cycle?"

- **(b) Pattern:** reconstruct the cycle explicitly, then answer queries in
  `O(1)`.
- **(c) Adapt:** run the DSU to find the redundant edge `(u, v)`. The cycle is
  `(u, v)` plus the unique path from `u` to `v` in the spanning tree formed by
  the *successful* edges. Find that path with a BFS/DFS on the spanning tree.
  Store the cycle's edges in a `set`; each query is a membership check.
- **(d) Say:** "The cycle is the redundant edge plus the tree path between its
  endpoints — one BFS on the spanning tree materializes it, then queries are set
  lookups."

### Scenario 4 — "Edges are **weighted**. Remove the **minimum-weight** edge on the cycle (not the last-in-input one)."

- **(b) Pattern:** find the cycle (as in Scenario 3), then pick its cheapest
  edge.
- **(c) Adapt:** DSU to locate the redundant edge; reconstruct the cycle (tree
  path + redundant edge); scan the cycle's edges for the minimum weight; return
  that one. `O(E · α(V))` to find the cycle, `O(cycle length)` to scan.
- **(d) Say:** "Once you have the actual cycle, 'which edge to remove' is just a
  scan of the cycle under whatever objective — last-in-input, min-weight,
  max-weight — the finding-the-cycle part is unchanged."

### Scenario 5 — "Edges arrive as a **stream**; report the redundant edge the moment it appears, and keep going for future ones."

- **(b) Pattern:** DSU is **already** online — this is its native mode.
- **(c) Adapt:** maintain the DSU across the stream; on each incoming edge, call
  `union` and immediately emit the edge if it returns `False`. No re-scanning, no
  buffering. `O(α(n))` per edge.
- **(d) Say:** "Union-Find is inherently incremental — streaming edge input needs
  zero adaptation, which is exactly the case where DSU crushes the DFS-per-edge
  approach."

### Scenario 6 — "`n` is `10^7` nodes and `10^7` edges. Optimize."

- **(b) Pattern:** DSU is already essentially optimal; the DFS approach is
  infeasible.
- **(c) Adapt:** DSU with iterative `find` (no recursion), plain integer arrays
  for `parent`/`rank` (not dicts). Time `O(E · α(V)) ≈ 10^7`, space `O(V)`. The
  DFS-per-edge alternative would be `O(E²) = 10^14` — not an option at this
  scale.
- **(d) Say:** "This is the scale where the DSU-vs-DFS choice stops being
  stylistic: `O(E)` versus `O(E²)`. DSU with array-backed parent/rank and
  iterative find handles `10^7` edges comfortably."

---

## 15. Flashcards

**Q:** The core DSU idiom this problem is built on?
**A:** `union(u, v)` returns `False` ⟺ `u` and `v` were already connected ⟺ the
edge `(u, v)` closes a cycle.

**Q:** Why is the first `union` failure automatically "the last cycle edge in
input order"?
**A:** All the *other* cycle edges were processed earlier and unioned
successfully; the failure is the edge that completes the loop when the scan
reaches it.

**Q:** DSU size for `1..n`-indexed nodes?
**A:** `DSU(n + 1)`, leaving index `0` unused (or remap to `0..n-1`).

**Q:** Time and space, with derivation?
**A:** `O(n · α(n)) ≈ O(n)` time (one `union` per edge, amortized near-constant),
`O(n)` space (`parent` + `rank`).

**Q:** The `O(E²)` alternative, and why DSU wins?
**A:** DFS/BFS per edge to test "already connected" — `O(E · (V+E))`. DSU makes
each test `O(α(V))`, so `O(E)` overall.

**Q:** How does the *directed* version (LC 685) differ?
**A:** Three cases — a node with two parents, a cycle, or both. First find the
two-parent candidate edges, then use DSU to decide which one to drop.

**Q:** How does this extend to K cycles?
**A:** Don't stop at the first `union` failure — collect every failing edge; each
closes a distinct cycle.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. DSU with **recursive** `find` (full path
compression) and **no union by rank** — a common, perfectly valid simplification.
`O(n · log n)` amortized here, effectively `O(n)`.

```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:

        n = len(edges)
        parent = [i for i in range(n + 1)]

        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])       # recursive full path compression
            return parent[i]

        def union(u, v):
            root_u = find(u)
            root_v = find(v)

            if root_u == root_v:
                return False

            parent[root_u] = root_v            # no rank/size balancing -- just attach
            return True

        for u, v in edges:
            if not union(u, v):
                return [u, v]

        return []
```

**Correct** — verified against all 5 tests from section 8.

**Two deviations from the house `DSU` class (neither is a bug):**

1. **Recursive `find` with full path compression** vs the house style's iterative
   `while` loop with path *halving*. Recursive full compression flattens the path
   completely in one call (slightly better compression), reads very cleanly, and
   is fine for `n ≤ 1000`. The risk it carries: on a pathological long chain
   *before* any compression has happened, the recursion can go deep — for very
   large `n` (Scenario 6's `10^7`), prefer the iterative form to avoid
   `RecursionError`. At this problem's scale it's a non-issue.
2. **No union by rank / size.** You always attach `root_u` under `root_v`, so
   trees can grow unbalanced. With path compression *alone*, each operation is
   amortized `O(log n)` (vs `O(α(n))` with both optimizations) — for `n ≤ 1000`
   the difference is invisible. Adding rank or size gets you the full
   near-constant guarantee and is worth the 3 extra lines if you expect large or
   adversarial input. "Path compression only" is a widely-accepted interview
   answer, though.
