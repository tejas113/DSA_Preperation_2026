# Evaluate Division  ·  LeetCode 399  ·  Medium

Group 09 — Weighted DFS (ratio propagation)  ·  a normal DFS, but you carry a
running **product** along the path instead of a running sum.

Prereqs: `concepts/04` (DFS), `concepts/02` (building a weighted adjacency list).

---

## 1. Problem

You're given `equations` — pairs `[Ai, Bi]` of variable names — and `values`,
where `values[i]` means `Ai / Bi = values[i]`.

Answer each `queries[j] = [Cj, Dj]` with the value of `Cj / Dj`, or **`-1.0`** if
it can't be determined (an unknown variable, or no chain of equations connects
them).

Constraints:
- `1 <= equations.length, queries.length <= 20`.
- `0.0 < values[i] <= 20.0` (so no zero denominators, and every real ratio is
  **positive**).
- Variable names are short strings.

Example:

```
equations = [["a","b"],["b","c"]],  values = [2.0, 3.0]
queries   = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
answer    = [6.0,       0.5,       -1.0,     1.0,      -1.0]
```

- `a/c = (a/b)·(b/c) = 2·3 = 6`
- `b/a = 1/(a/b) = 0.5`
- `a/e` — `e` never appears → `-1.0`
- `a/a = 1.0` — but only because `a` **is** a known variable
- `x/x` — `x` is unknown → `-1.0` (not `1.0`!)

---

## 2. Explain Like I'm 5

Each equation is a signpost: "to go from `a` to `b`, multiply by 2." The reverse
signpost is automatic: "to go from `b` to `a`, multiply by 1/2."

To find `a/c`, walk from `a` to `c` following signposts, multiplying every number
you pass. `a→b` (×2), `b→c` (×3) → `a/c = 6`.

If there's no path of signposts from one variable to the other — or one of them
was never on any signpost at all — you just can't know, so the answer is `-1`.
And `x/x` is only `1` if `x` is a place that actually exists on the map.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Relationships between quantities (`a/b = v`) | ✅ |
| The answer along a path is a **product**, not a sum | ✅ |
| "Derive an unknown ratio from known ones" | ✅ |

**Reduce it to:** *"Build a graph: `a→b` weight `v`, `b→a` weight `1/v`. Each
query `x/y` = the product of edge weights along any path from `x` to `y` (DFS
carrying a running product); `-1.0` if `x` or `y` is unknown or unreachable."*

**Look-alikes (same "carry an accumulator along the path" shape):**
- Currency exchange / arbitrage — same product-along-path; arbitrage is a cycle
  with product `> 1` (detected via Bellman-Ford on `-log` weights).
- Unit conversion ("teaspoons per gallon") — chain of conversion factors.
- BFS/DFS for *distance* — the same skeleton, but the accumulator is a **sum**.

---

## 4. Intuition

1. `a / b = v` means: going `a → b` multiplies by `v`; going `b → a` multiplies
   by `1/v`. So each equation is a **pair** of directed weighted edges.
2. Chaining: `a/c = (a/b)·(b/c)`. Along any path `x → ... → y`, multiply the edge
   weights; that product **is** `x/y`.
3. In a consistent system, *every* path gives the same product, so a single DFS
   (first path found) suffices.
4. **Order of checks matters:** confirm both `x` and `y` are known variables
   **before** the `x == y → 1.0` shortcut — otherwise `["x","x"]` for an unknown
   `x` wrongly returns `1.0`.
5. `-1.0` is a safe "impossible" sentinel because every real ratio is
   **positive** (values `> 0`), so `-1.0` can never be a legitimate answer.

---

## 5. Approach (primary): weighted DFS per query

1. `graph = defaultdict(dict)`. For each `([a, b], v)`: `graph[a][b] = v`,
   `graph[b][a] = 1 / v`.
2. `dfs(src, dst, seen)`:
   - `src` or `dst` not in `graph` → return `-1.0`.
   - `src == dst` → return `1.0`.
   - Add `src` to `seen`. For each `(nei, w)` in `graph[src].items()` with `nei`
     not in `seen`: `sub = dfs(nei, dst, seen)`; if `sub != -1.0`, return
     `w * sub`.
   - Return `-1.0` (dead end).
3. Return `[dfs(c, d, set()) for c, d in queries]` — a **fresh** `seen` per
   query.

Builds on: `concepts/04` (DFS), with a product accumulator.

---

## 6. Pseudocode

```
function calcEquation(equations, values, queries):
    graph = {}                                  # graph[a][b] = a / b
    for ([a, b], v) in zip(equations, values):
        graph[a][b] = v
        graph[b][a] = 1 / v

    function dfs(src, dst, seen):
        if src not in graph or dst not in graph: return -1.0
        if src == dst: return 1.0
        add src to seen
        for (nei, w) in graph[src]:
            if nei not in seen:
                sub = dfs(nei, dst, seen)
                if sub != -1.0:
                    return w * sub
        return -1.0

    return [dfs(c, d, new empty set) for (c, d) in queries]
```

---

## 7. Dry Run

```
equations = [["a","b"],["b","c"]], values = [2.0, 3.0]
query = ["a","c"]
```

`graph = { a:{b:2.0}, b:{a:0.5, c:3.0}, c:{b:0.333...} }`.

`dfs("a", "c", set())`:

| call | src | seen (before adding src) | action |
|---|---|---|---|
| dfs(a,c) | a | {} | a,c both known; a≠c; seen={a}; try nei `b` (w=2.0) |
| ↳ dfs(b,c) | b | {a} | b,c known; b≠c; seen={a,b}; nei `a` in seen — skip; try nei `c` (w=3.0) |
| ↳↳ dfs(c,c) | c | {a,b} | src == dst → **return 1.0** |
| ↳ dfs(b,c) returns | | | `w * sub` = `3.0 * 1.0` = **3.0** |
| dfs(a,c) returns | | | `w * sub` = `2.0 * 3.0` = **6.0** |

Answer: `6.0`. ✅

`query = ["a","a"]`: `a` is in `graph`, `src == dst` → `1.0`.
`query = ["x","x"]`: `x` not in `graph` → `-1.0` (the variable check fires first).

---

## 8. Python Code (primary — weighted DFS)

```python
from collections import defaultdict
from typing import List


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:
        graph = defaultdict(dict)               # graph[a][b] = a / b
        for (a, b), v in zip(equations, values):
            graph[a][b] = v
            graph[b][a] = 1 / v

        def dfs(src: str, dst: str, seen: set) -> float:
            if src not in graph or dst not in graph:
                return -1.0                      # unknown variable -- check BEFORE src == dst
            if src == dst:
                return 1.0
            seen.add(src)
            for nei, w in graph[src].items():
                if nei not in seen:
                    sub = dfs(nei, dst, seen)
                    if sub != -1.0:
                        return w * sub            # accumulate the PRODUCT
            return -1.0

        return [dfs(c, d, set()) for c, d in queries]


if __name__ == "__main__":
    sol = Solution()

    assert sol.calcEquation(
        [["a", "b"], ["b", "c"]], [2.0, 3.0],
        [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
    ) == [6.0, 0.5, -1.0, 1.0, -1.0]

    assert sol.calcEquation(
        [["a", "b"], ["b", "c"], ["bc", "cd"]], [1.5, 2.5, 5.0],
        [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]]
    ) == [3.75, 0.4, 5.0, 0.2]

    assert sol.calcEquation(
        [["a", "b"]], [0.5],
        [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]]
    ) == [0.5, 2.0, -1.0, -1.0]

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. BFS (carry the running product in the queue)

```python
from collections import defaultdict, deque


def calcEquation(self, equations, values, queries):
    graph = defaultdict(dict)
    for (a, b), v in zip(equations, values):
        graph[a][b] = v
        graph[b][a] = 1 / v

    def bfs(src, dst):
        if src not in graph or dst not in graph:
            return -1.0
        q = deque([(src, 1.0)])
        seen = {src}
        while q:
            node, prod = q.popleft()
            if node == dst:
                return prod
            for nei, w in graph[node].items():
                if nei not in seen:
                    seen.add(nei)
                    q.append((nei, prod * w))
        return -1.0

    return [bfs(c, d) for c, d in queries]
```

### 9b. Floyd-Warshall — precompute *all* pairs (best when many queries)

There are at most `~40` distinct variables. Build a `ratio[i][j]` table:
`ratio[i][i] = 1`, `ratio[a][b] = v` (and `1/v`), then

```
for k in variables:
  for i in variables:
    for j in variables:
      if ratio[i][k] and ratio[k][j]:
        ratio[i][j] = ratio[i][k] * ratio[k][j]
```

`O(V³)` once, then each query is an `O(1)` lookup. Worth it when `Q ≫ V`.

### 9c. Weighted Union-Find

Each node stores `weight[x]` = `x / parent[x]`. `find(x)` compresses the path
and multiplies the weights up to the root. `union(a, b, v)` (for `a / b = v`)
links the roots with the weight that keeps ratios consistent. Query `a / b`: if
same root, `weight[a] / weight[b]`; else `-1.0`. `O((E + Q) α(V))` — the online
tool (Scenario 3), and it also catches an inconsistent system (Scenario 2).

### The BFS↔DFS answer the interviewer wants

> "It's a normal traversal with a product accumulator instead of a sum. DFS or
> BFS per query, both `O(V + E)`. For many queries I'd precompute all-pairs
> ratios with a Floyd-Warshall pass (`O(V³)` given only ~40 variables), or use a
> weighted Union-Find if equations stream in."

---

## 10. Complexity — derived step by step

**V and E:** `V` = distinct variables (`≤ 2·equations.length ≤ 40`),
`E` = `2·equations.length` (each equation → 2 directed edges).

**Time:**
- Build graph: `O(E)`.
- Per query: one DFS/BFS over a component → `O(V + E)`.
- `Q` queries: **`O(Q · (V + E))`**. (All tiny here, but that's the general
  bound.) Floyd-Warshall variant: `O(V³ + Q)`.

**Space:**
- Graph: `O(V + E)`.
- `seen` + recursion/queue per query: `O(V)`.
- **Total: `O(V + E)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| Query variable never appears in any equation | `src not in graph` → `-1.0` |
| `["a","a"]` where `a` is known | `src == dst` → `1.0` |
| `["x","x"]` where `x` is unknown | variable check fires **first** → `-1.0` |
| `x` and `y` in different components | DFS exhausts the component, returns `-1.0` |
| Multi-hop path | product accumulates across all hops |
| Reusing `seen` across queries | **don't** — pass a fresh `set()` per query |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Checking `src == dst` before the "known variable" check.** `["x","x"]`
      for an unknown `x` then wrongly returns `1.0` instead of `-1.0`.
- [ ] **Forgetting the reverse edge** `graph[b][a] = 1 / v`. Then `b/a` and any
      path that needs to traverse an equation "backwards" fails.
- [ ] **Sharing one `seen` set across all queries.** After the first query,
      later ones start with nodes already marked — wrong `-1.0`s.
- [ ] **Accumulating a sum instead of a product** — `w + sub` instead of
      `w * sub`.
- [ ] **Returning `sub` instead of `w * sub`** — forgets the current edge.
- [ ] **Worrying about `-1.0` colliding with a real answer** — it can't, all
      ratios are positive; exact `!= -1.0` comparison is safe.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Weighted traversal with an accumulator.** Distance problems carry a **sum**;
   this carries a **product**. Same BFS/DFS skeleton, different combine operator
   (a different monoid).
2. **Directed-but-paired edges:** a symmetric relation with an inverse
   (`a→b` = `v`, `b→a` = `1/v`) — the shape of ratio / exchange-rate / unit-
   conversion graphs.
3. **Safe sentinel by domain knowledge:** `-1.0` works because real answers are
   strictly positive.
4. **Few nodes + many queries → precompute all pairs** (Floyd-Warshall) — a
   recurring trade-off.

| Problem | How this transfers |
|---|---|
| Currency arbitrage detection | product-along-cycle `> 1`; via Bellman-Ford on `-log(rate)` weights (negative cycle) |
| Unit conversion ("how many mm in a mile") | chain of conversion factors — this exact pattern |
| "Given `a = 2b`, `b = 3c`, express `a` in terms of `c`" | product along the path |
| Any "propagate a value along edges" (probabilities, scaling factors) | swap the combine operator, keep the traversal |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "There will be **millions of queries** against the same equation set."

- **(b) Pattern:** precompute all-pairs ratios once.
- **(c) Adapt:** with `V ≤ ~40` variables, run a **Floyd-Warshall** pass to fill
  `ratio[x][y]` for every connected pair — `O(V³)`. Each query is then an `O(1)`
  table lookup (`-1.0` if the pair isn't in the table). Alternatively a weighted
  Union-Find: `O(E α)` to build, `O(α)` per query.
- **(d) Say:** "Few variables, many queries → amortize with an `O(V³)`
  all-pairs precompute (or a weighted DSU), turning each query into `O(1)`."

### Scenario 2 — "The equation set might be **inconsistent** (`a/b=2`, `b/c=3`, but `a/c=5`). Detect it."

- **(b) Pattern:** every cycle's product must be `1` (within float tolerance).
- **(c) Adapt:** with a **weighted Union-Find**, when a `union(a, b, v)` connects
  two nodes already in the same component, check whether the implied ratio
  matches `v` (up to `1e-6`); a mismatch flags inconsistency. Without DSU: for
  each equation `[a, b, v]`, run the DFS `a → b` on the rest of the graph and
  verify the product ≈ `v`.
- **(d) Say:** "Consistency = every cycle multiplies to 1. Weighted Union-Find
  catches it naturally: a union between already-connected nodes whose implied
  ratio disagrees with the new equation."

### Scenario 3 — "Equations **stream in**, interleaved with queries."

- **(b) Pattern:** online → **weighted Union-Find**.
- **(c) Adapt:** maintain the weighted DSU; `union` each incoming equation
  (`O(α)`), answer each query with two `find`s and a ratio of weights. Re-running
  a DFS per query as the graph grows would be `O(V + E)` each time.
- **(d) Say:** "Streaming equations is weighted Union-Find's home turf —
  amortized near-constant per equation and per query."

### Scenario 4 — "Variables can also be **removed** (an equation retracted)."

- **(b) Pattern:** Union-Find **can't un-merge**.
- **(c) Adapt:** if the operation timeline is known, process offline in reverse
  (retractions become additions). Otherwise, fall back to **rebuilding the graph
  and running a fresh DFS per query** — `O(V + E)` per query, but correct under
  arbitrary removals. For rare removals, periodic full rebuilds of the DSU are
  pragmatic.
- **(d) Say:** "Retractions break Union-Find — offline-reverse if possible, else
  a fresh-graph DFS per query, which tolerates any removal at `O(V + E)` cost."

### Scenario 5 — "Ratios must be **exact** — no floating-point drift over long chains."

- **(b) Pattern:** same algorithm, exact arithmetic.
- **(c) Adapt:** store each weight as an exact fraction (`fractions.Fraction`, or
  a `(num, den)` pair reduced by `gcd`). Multiplication stays exact; consistency
  checks become exact equality (`==`), no tolerance needed. Slower per operation
  but no accumulated error.
- **(d) Say:** "Swap `float` for `Fraction` — the traversal is identical, you
  just trade speed for exactness and drop the `1e-6` tolerance."

### Scenario 6 — "If you could learn the **absolute value** of exactly one variable, which one unlocks the most others?"

- **(b) Pattern:** connected-component analysis.
- **(c) Adapt:** within a connected component, all variables' values are
  determined *relative* to each other, so knowing **any one** absolute value
  fixes the **whole component**. So the best variable to learn is any variable in
  the **largest connected component** — compute component sizes (DSU or
  flood-fill), pick a variable from the biggest. `O(V + E)`.
- **(d) Say:** "Ratios pin every variable in a component to every other, so one
  absolute value unlocks an entire component — the answer is any variable in the
  largest one."

---

## 15. Flashcards

**Q:** What does a normal BFS/DFS carry along the path, and what does this one
carry instead?
**A:** Distance problems carry a running **sum**; Evaluate Division carries a
running **product** (the ratio). Same traversal, different combine operator.

**Q:** What two edges does the equation `a / b = v` create?
**A:** `a → b` with weight `v`, and `b → a` with weight `1 / v`.

**Q:** The ordering bug that breaks `["x","x"]`?
**A:** Checking `src == dst` **before** confirming both variables exist — an
unknown `x` then returns `1.0` instead of `-1.0`.

**Q:** Why is `-1.0` a safe "impossible" sentinel?
**A:** Every real ratio is positive (`values > 0`), so `-1.0` can never be a
legitimate answer.

**Q:** Time for `Q` queries with the DFS approach?
**A:** `O(Q · (V + E))` — one traversal per query. Floyd-Warshall precompute is
`O(V³ + Q)`.

**Q:** Many queries against a fixed equation set — what do you do?
**A:** Precompute all-pairs ratios (Floyd-Warshall, `O(V³)` for ~40 variables),
then `O(1)` per query. Or a weighted Union-Find.

**Q:** How do you detect an inconsistent equation set?
**A:** Every cycle's product must be `1`. Weighted Union-Find flags it when a
union between already-connected nodes implies a different ratio.

**Q:** One absolute value that unlocks the most variables — which?
**A:** Any variable in the **largest connected component** (ratios fix a whole
component relative to one known value).

---

## Appendix — Tejas's LeetCode Practice Answer (BFS)

BFS variant — carry the running product in the queue. The draft as first written
had three issues, corrected below:

- `q.append([nei,w*weight)` — mismatched bracket (`[` open, `)` close).
- `bfs` had **no `return -1.0`** after the `while` loop → returned `None` when
  the target wasn't reachable.
- `calcEquation` never iterated `queries` / returned results → the method
  returned `None`.

Corrected and verified against all 3 tests:

```python
class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:

        adj = defaultdict(list)

        for i, eq in enumerate(equations):
            a, b = eq
            adj[a].append([b, values[i]])
            adj[b].append([a, 1 / values[i]])

        def bfs(start, target):
            if start not in adj or target not in adj:
                return -1.0

            q = deque([[start, 1.0]])
            visited = {start}

            while q:
                n, w = q.popleft()

                if n == target:
                    return w

                for nei, weight in adj[n]:
                    if nei not in visited:
                        q.append([nei, w * weight])
                        visited.add(nei)

            return -1.0                       # queue drained, target unreachable

        return [bfs(c, d) for c, d in queries]
```

**Notes:**
- Seed the queue with `[start, 1.0]` (float), not `[start, 1]` — with the int
  `1`, a query like `["a","a"]` returns the int `1` instead of `1.0`. LeetCode's
  judge accepts `1 == 1.0`, but returning the right type is cleaner.
- This is the same as the primary solution's §9a BFS alternative; both are
  `O(Q · (V + E))` and correct.
