# Is Graph Bipartite?  ·  LeetCode 785  ·  Medium

Group 08 — Bipartite / 2-Coloring  ·  the pattern in its purest form: you're
handed the adjacency list, return whether it 2-colors.

Prereqs: `concepts/09-bipartite-coloring.md`, `concepts/03`/`04` (BFS/DFS),
`concepts/05` (looping over all components).

---

## 1. Problem

You're given an undirected graph as an adjacency list: `graph[u]` is the list of
nodes adjacent to `u`. Nodes are `0..n-1`.

**Return `True` if the graph is bipartite** — if its nodes can be split into two
sets `A` and `B` such that **every edge has one endpoint in `A` and one in `B`**.

Constraints:
- `1 <= n <= 100`.
- No self-loops, no duplicate edges; `graph` is a valid undirected graph (if
  `v ∈ graph[u]` then `u ∈ graph[v]`).

Example 1:

```
graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
answer = False        # 0-1-2-0 is a triangle (odd cycle)
```

Example 2:

```
graph = [[1,3],[0,2],[1,3],[0,2]]
answer = True         # A = {0,2}, B = {1,3}
```

---

## 2. Explain Like I'm 5

You have kids and a list of "these two don't get along." You want to make **two
teams** so that every pair who doesn't get along is on **opposite** teams.

Pick a kid, put them on the Red team. Everyone they don't get along with goes on
the Blue team. Everyone *those* kids don't get along with goes back on Red. Keep
going.

If you ever have to put a kid on Red when they're **already on Blue** (or vice
versa), it's impossible — no way to make two fair teams. Otherwise, the teams you
built work.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Split into **two** groups" / "is it bipartite" / "2-colorable" | ✅ |
| Undirected graph, edges = conflicts | ✅ |
| The answer hinges on odd cycles | ✅ (bipartite ⟺ no odd cycle) |

**Reduce it to:** *"2-color the graph with BFS/DFS. Color each neighbor the
opposite color; a same-color conflict on any edge → not bipartite. Loop over all
components."*

**Look-alike:** Possible Bipartition (next) — identical 2-coloring, but you first
build the adjacency list from a list of "dislikes" pairs.

---

## 4. Intuition

1. If the graph is bipartite, assign one side color `+1` and the other `-1`.
   Every edge then connects a `+1` to a `-1`.
2. So: pick any uncolored node, give it `+1`, and propagate — every neighbor must
   be the opposite of its predecessor. BFS or DFS both work.
3. The only way this fails is if propagation forces a node to be *both* colors —
   which happens exactly when you walk around a cycle of **odd** length (color
   flips an odd number of times and lands wrong).
4. **Loop over every node as a potential start**, because the graph may be
   disconnected and each component must independently 2-color.

---

## 5. Approach (primary): BFS 2-coloring

1. `n = len(graph)`. `color = [0] * n` (`0` = uncolored, `1` / `-1` = the two
   colors).
2. For `start` in `0..n-1`: if `color[start] != 0`, skip. Else `color[start] =
   1`, `q = deque([start])`.
3. While `q`: pop `node`. For each `nei` in `graph[node]`:
   - `color[nei] == 0` → `color[nei] = -color[node]`, push `nei`.
   - `color[nei] == color[node]` → **return `False`**.
4. Return `True`.

Builds on: `concepts/09` (2-coloring), `concepts/03` (BFS, mark-on-enqueue),
`concepts/05` (loop all components).

---

## 6. Pseudocode

```
function isBipartite(graph):
    n = len(graph)
    color = [0] * n                          # 0 uncolored, 1 / -1 the two colors
    for start in 0 .. n-1:
        if color[start] != 0: continue
        color[start] = 1
        q = queue([start])
        while q not empty:
            node = dequeue
            for nei in graph[node]:
                if color[nei] == 0:
                    color[nei] = -color[node]
                    enqueue nei
                elif color[nei] == color[node]:
                    return False
    return True
```

---

## 7. Dry Run

```
graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
```

`color = [0,0,0,0]`. `start = 0`: `color[0] = 1`, `q = [0]`.

| pop | node color | neighbor checks | color after | queue after |
|---|---|---|---|---|
| 0 | 1 | `1`→`-1`(new), `2`→`-1`(new), `3`→`-1`(new) | `[1,-1,-1,-1]` | `[1,2,3]` |
| 1 | -1 | `0`=`1`=`-color[1]` ✓ ; `2`=`-1`=`color[1]` → **conflict** | | **return `False`** |

The cycle `0–1–2–0` has 3 edges (odd) → not bipartite. ✅

For Example 2 `[[1,3],[0,2],[1,3],[0,2]]`: coloring gives `[1,-1,1,-1]`, no edge
joins two equal colors → `True`.

---

## 8. Python Code (primary — BFS 2-coloring)

```python
from collections import deque
from typing import List


class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [0] * n                       # 0 = uncolored; 1 / -1 = the two sides

        for start in range(n):                # every component must 2-color
            if color[start] != 0:
                continue
            color[start] = 1
            q = deque([start])
            while q:
                node = q.popleft()
                for nei in graph[node]:
                    if color[nei] == 0:
                        color[nei] = -color[node]      # opposite color, marked on enqueue
                        q.append(nei)
                    elif color[nei] == color[node]:
                        return False                    # same color across an edge
        return True


if __name__ == "__main__":
    sol = Solution()

    assert sol.isBipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]) is False
    assert sol.isBipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True
    assert sol.isBipartite([[]]) is True                          # single isolated node
    assert sol.isBipartite([[1], [0], [3], [2]]) is True          # two disjoint edges
    assert sol.isBipartite([[1, 2], [0, 2], [0, 1]]) is False     # triangle
    assert sol.isBipartite([[1], [0], []]) is True                # edge + isolated node
    assert sol.isBipartite([[1, 4], [0, 2], [1, 3], [2, 4], [0, 3]]) is False  # 5-cycle

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS 2-coloring

```python
from typing import List


class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [0] * n

        def dfs(node: int, c: int) -> bool:
            color[node] = c
            for nei in graph[node]:
                if color[nei] == 0:
                    if not dfs(nei, -c):
                        return False
                elif color[nei] == c:
                    return False
            return True

        return all(dfs(i, 1) for i in range(n) if color[i] == 0)
```

Same `O(V + E)`. `n ≤ 100` here so recursion depth is a non-issue.

### 9b. Union-Find (better for *incremental* edges — Scenario 5)

DSU of size `2n`: slot `i` = "node `i` on side A", slot `i + n` = "node `i` on
side B". For each edge `(u, v)`: `union(u, v + n)` and `union(v, u + n)`
("`u` and `v` are on opposite sides"). If `find(u) == find(v)` ever holds, `u`
and `v` are forced onto the *same* side → not bipartite. `O((V + E) α(n))`.

### The BFS↔DFS answer the interviewer wants

> "2-coloring with BFS or DFS, both `O(V + E)` — color each neighbor the opposite
> color, fail on a same-color edge, and loop over all components since the graph
> may be disconnected. For a static check either traversal is fine; for
> *incremental* edges I'd switch to the `2n`-slot Union-Find."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E` = total adjacency-list length / 2.

**Time:**
- Outer loop: `O(V)`.
- BFS/DFS across all components: each node colored once, each edge inspected a
  constant number of times → `O(V + E)`.
- **Total: `O(V + E)`.**

**Space:**
- `color` array: `O(V)`.
- BFS queue / DFS stack: `O(V)`.
- **Total: `O(V)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| Single node, no edges | `color[0] = 1`, no neighbors → `True` |
| `n` isolated nodes | each colored `1`, no conflicts → `True` |
| Disconnected, all components bipartite | outer loop colors each → `True` |
| Disconnected, one component has an odd cycle | that component's BFS hits a conflict → `False` |
| A single edge | `[1, -1]` → `True` |
| Any odd cycle anywhere | same-color conflict → `False` |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Only coloring from node `0`** (missing the `for start in range(n)`
      loop). A disconnected graph with an odd cycle in a later component wrongly
      returns `True`.
- [ ] **Coloring at dequeue instead of enqueue** (BFS). A node can be enqueued
      twice with opposite colors before it's processed, giving a wrong verdict.
      Color it the instant you assign it.
- [ ] **Inverting the conflict test** — `elif color[nei] != color[node]` when you
      meant `==`.
- [ ] **Using `0` as a real color.** Then "uncolored" is indistinguishable from
      one of the two sides. Use `1` / `-1`.
- [ ] **Assuming connected** — the biggest source of a false `True`.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **2-coloring = BFS/DFS + a `color` array; conflict = odd cycle = not
   bipartite.** State the ⟺ with "no odd cycle" out loud.
2. **The `1` / `-1` trick** — "opposite color" is just `-color[node]`, no
   `if/else`.
3. **Loop over all components** — same discipline as component counting; a graph
   is bipartite only if *every* component is.
4. **Bipartite structure unlocks tools** — maximum bipartite matching
   (Hopcroft-Karp), König's theorem (max matching = min vertex cover in bipartite
   graphs), stable-matching-style assignment.

| Problem | How this transfers |
|---|---|
| Possible Bipartition | build the adjacency list from "dislikes" pairs, then this exact 2-coloring |
| "Two-shift / two-room scheduling with conflict pairs" | conflict graph + 2-coloring |
| Detect an odd cycle | the 2-coloring conflict *is* an odd cycle |
| Maximum bipartite matching setups | first confirm/derive the bipartition, then match across it |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Return the actual two groups (the bipartition), not just `True`/`False`."

- **(b) Pattern:** same 2-coloring, collect the colors.
- **(c) Adapt:** after (or during) coloring, `group_a = [i for i in range(n) if
  color[i] == 1]`, `group_b = [i for i in range(n) if color[i] == -1]`. Return
  `[group_a, group_b]` if bipartite, else `[]`. Isolated nodes can go in either
  group (they land in `group_a` since they start at `1`). `O(V + E)`.
- **(d) Say:** "The `color` array *is* the bipartition — just partition the node
  ids by their color at the end."

### Scenario 2 — "The graph is disconnected; for **each component** report whether it's bipartite and its bipartition."

- **(b) Pattern:** the must-loop-all-components structure, with per-component
  bookkeeping.
- **(c) Adapt:** for each fresh `start`, run the coloring but scoped to that
  component (collect the component's nodes as you BFS). Record `(component_nodes,
  is_bipartite, bipartition)` per component. The whole graph is bipartite iff
  every component is.
- **(d) Say:** "It's already component-by-component internally — just don't
  early-return globally; store the result per component."

### Scenario 3 — "Generalize to **K-coloring**: can the graph be colored with `K` colors so no edge is monochromatic?"

- **(b) Pattern:** `K = 2` is *this* problem (polynomial — the odd-cycle test).
  `K ≥ 3` is **graph coloring**, which is **NP-hard** in general.
- **(c) Adapt:** for `K = 2`, the BFS/DFS coloring. For `K ≥ 3` there's no known
  polynomial test in general; you'd use backtracking with pruning (feasible only
  for small graphs), or exploit special structure (bipartite ⟹ 2, planar ⟹ ≤ 4
  by the four-color theorem though 3-coloring planar is still NP-hard, interval /
  chordal graphs colorable greedily in `O(V + E)`).
- **(d) Say:** "2-coloring is the easy case — odd cycles are the only
  obstruction. At `K = 3` it becomes NP-hard, so I'd either backtrack for small
  inputs or lean on graph structure if the problem guarantees any."

### Scenario 4 — "The input might contain a **self-loop** (`u ∈ graph[u]`) or be **non-symmetric** (malformed). Handle it."

- **(b) Pattern:** input validation around the same algorithm.
- **(c) Adapt:** a self-loop makes bipartiteness **impossible** — an edge from a
  node to itself can't cross a divide; detect `nei == node` in the neighbor loop
  and return `False`. For non-symmetric input, either defensively add the reverse
  edge for every edge seen (treat it as undirected) or reject as invalid — state
  the assumption to the interviewer.
- **(d) Say:** "A self-loop is an instant `False`. Asymmetric input either gets
  symmetrized defensively or rejected — I'd confirm which the problem wants."

### Scenario 5 — "Edges are added one at a time; after each edge, report whether the graph is **still** bipartite."

- **(b) Pattern:** incremental → the `2n`-slot **Union-Find** (§9b) is the right
  tool.
- **(c) Adapt:** maintain a DSU of size `2n`. On each new edge `(u, v)`: first
  check `if find(u) == find(v): report "no longer bipartite"`. Otherwise
  `union(u, v + n)` and `union(v, u + n)`. `O(α(n))` per edge, vs re-running the
  whole `O(V + E)` coloring each time.
- **(d) Say:** "Incremental bipartiteness is the `2n`-slot Union-Find — union
  each node with the other's 'enemy' slot, and a `find(u) == find(v)` means
  they've been forced together."

### Scenario 6 — "`V` and `E` are `10^7`. Is it bipartite?"

- **(b) Pattern:** BFS/DFS coloring is already `O(V + E)`, optimal.
- **(c) Adapt:** iterative BFS (no recursion), a flat `array('b', ...)` for
  `color`, stream the adjacency list. `O(V + E)` time, `O(V)` space. The
  `2n`-slot DSU is also `O(E α(V))` and works too.
- **(d) Say:** "Linear time and space — iterative BFS with a byte-array color map
  handles `10^7` fine; no better asymptotic exists since you must look at every
  edge."

---

## 15. Flashcards

**Q:** A graph is bipartite iff...?
**A:** It can be 2-colored with no edge joining same-colored nodes ⟺ it has **no
odd-length cycle**.

**Q:** The algorithm?
**A:** BFS/DFS from each uncolored node; color each neighbor the opposite color
(`-color[node]`); a same-color edge → not bipartite. Loop over all components.

**Q:** Why `1` / `-1` for colors, not `0` / `1`?
**A:** So "opposite color" is just `-color[node]`, and `0` can stay unambiguously
"uncolored."

**Q:** The #1 false-`True` bug?
**A:** Only coloring from node `0` — a disconnected graph with an odd cycle in
another component slips through. Loop `for start in range(n)`.

**Q:** Time and space?
**A:** `O(V + E)` time, `O(V)` space — a BFS/DFS with a color array.

**Q:** Incremental edges, "still bipartite after each"?
**A:** `2n`-slot Union-Find: `union(u, v+n)` and `union(v, u+n)` per edge;
`find(u) == find(v)` ⟹ not bipartite. `O(α(n))` per edge.

**Q:** K-coloring for `K ≥ 3`?
**A:** NP-hard in general. Only `K = 2` (this problem) has the easy odd-cycle
test.

**Q:** How do you get the actual two groups?
**A:** Partition node ids by their value in the `color` array after coloring.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. BFS 2-coloring, loops all components, colors at
enqueue, correct conflict check. `O(V + E)` time, `O(V)` space.

```python
class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:

        adj_list = defaultdict(list)
        queue = deque()

        for node, neighbors in enumerate(graph):
            adj_list[node] = neighbors

        n = len(graph)

        color = [0] * n

        for i in range(n):
            if color[i] == 0:
                color[i] = 1
                queue.append(i)

                while queue:
                    node = queue.popleft()

                    for neighbor in adj_list[node]:
                        if color[neighbor] == 0:
                            color[neighbor] = -color[node]
                            queue.append(neighbor)

                        elif color[neighbor] == color[node]:
                            return False

        return True
```

**Correct** — verified against all 7 tests from section 8 (triangle, 5-cycle,
disconnected, isolated nodes).

**Two small style notes (neither is a bug):**

1. **The `adj_list` copy is unnecessary.** `graph` is *already* an adjacency list
   — `graph[node]` is exactly the neighbor list. The loop
   `for node, neighbors in enumerate(graph): adj_list[node] = neighbors` just
   makes a second reference to the same lists inside a `defaultdict`. You can
   iterate `graph[node]` directly and drop `adj_list` entirely. (Building an
   adjacency list from scratch *is* needed in Possible Bipartition, where the
   input is a pair list — not here.)
2. **`queue` declared outside the outer loop** works only because the inner
   `while queue:` fully drains it before the next component starts. It's correct,
   but `queue = deque([i])` right where you start a component reads more clearly
   and removes any doubt about leftover state.
