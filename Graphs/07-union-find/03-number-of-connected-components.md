# Number of Connected Components in an Undirected Graph  ·  LeetCode 323  ·  Medium  ·  🔒 Premium

Group 07 — Union-Find  ·  the group's second idiom in its purest form:
`count = n`, then `count -= 1` on every **successful** `union`.

> Premium on LeetCode — the `.md`/`.py` here run and are tested locally.

Prereqs: `concepts/08-union-find.md`, `concepts/05` (connected components — the
flood-fill way, for the alternative).

---

## 1. Problem

Given `n` nodes labeled `0..n-1` and a list of undirected `edges`, return the
number of **connected components**.

Constraints:
- `1 <= n <= 2000`, `0 <= edges.length <= 5000`. Nodes `0`-indexed, no repeated
  edges, no self-loops.

Example 1:

```
n = 5, edges = [[0,1],[1,2],[3,4]]
answer = 2        # {0,1,2} and {3,4}
```

Example 2:

```
n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
answer = 1        # all in one chain
```

---

## 2. Explain Like I'm 5

You have `n` separate toys. Every string you tie between two toys **merges two
piles into one**. Start by saying "I have `n` piles." Each string that actually
joins **two different** piles: subtract one from your pile count. (A string
between two toys *already in the same pile* changes nothing.)

When you've used all the strings, the number you're left with is how many
separate piles you have.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "How many connected components / groups / clusters?" | ✅ |
| Undirected edges | ✅ → DSU applies |
| No cycle question, no tree question — just *count the groups* | ✅ → idiom #2 |

**Reduce it to:** *"`count = n`; for each edge, if `union` returns `True`,
`count -= 1`. Return `count`."*

**Look-alikes:**
- Number of Islands / Number of Provinces — same "count components" question,
  different input shape (grid, adjacency matrix).
- This is also solvable by the flood-fill skeleton from `concepts/05` — DSU vs
  BFS/DFS is a genuine choice here (both `O(V + E)`); DSU wins if edges are
  incremental.

---

## 4. Intuition

1. If there were no edges, every node is its own component → `n` components.
2. Each edge can only ever **reduce** the component count, and only by `1`, and
   only when it connects **two previously-separate** components.
3. The DSU's `union` tells you exactly that: it returns `True` precisely when it
   merged two different groups.
4. So: start at `n`, and every `True` from `union` costs one component.
   Cycle-closing edges (`union` returns `False`) leave the count alone.

That's the whole algorithm.

---

## 5. Approach (primary): DSU, `count -= 1` per successful union

1. `dsu = DSU(n)` (0-indexed). `count = n`.
2. For each `[u, v]` in `edges`: if `dsu.union(u, v)`: `count -= 1`.
3. Return `count`.

Builds on: `concepts/08` — the canonical DSU, plus idiom #2 from the group
README.

---

## 6. Pseudocode

```
function countComponents(n, edges):
    dsu = DSU(n)
    count = n
    for [u, v] in edges:
        if union(u, v):        # merged two different groups
            count -= 1
    return count
```

---

## 7. Dry Run

```
n = 5, edges = [[0,1],[1,2],[3,4]]
```

`DSU(5)`, `count = 5`.

| edge | union result | count after | parent after |
|---|---|---|---|
| [0,1] | `True` | 4 | `parent[1]=0` |
| [1,2] | `True` (find(1)→0 ≠ 2) | 3 | `parent[2]=0` |
| [3,4] | `True` | 2 | `parent[4]=3` |

Return `2` — components `{0,1,2}` and `{3,4}`. ✅

If we added `[0,2]` next: `find(0)==find(2)==0` → `union` returns `False` →
`count` stays `2`. Correct: connecting two nodes already in the same group
doesn't change the count.

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
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        dsu = DSU(n)
        count = n
        for u, v in edges:
            if dsu.union(u, v):
                count -= 1
        return count


if __name__ == "__main__":
    sol = Solution()

    assert sol.countComponents(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert sol.countComponents(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
    assert sol.countComponents(4, []) == 4                         # no edges -> n components
    assert sol.countComponents(1, []) == 1
    assert sol.countComponents(6, [[0, 1], [2, 3], [4, 5], [0, 2], [0, 4]]) == 1
    assert sol.countComponents(5, [[0, 1], [1, 2], [0, 2], [3, 4]]) == 2   # cycle edge ignored

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. BFS/DFS flood-fill counting (the `concepts/05` skeleton)

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        seen = set()
        count = 0
        for start in range(n):                    # iterate ALL node ids (isolated nodes count)
            if start in seen:
                continue
            count += 1
            q = deque([start])
            seen.add(start)
            while q:
                node = q.popleft()
                for nei in graph[node]:
                    if nei not in seen:
                        seen.add(nei)
                        q.append(nei)
        return count
```

`O(V + E)` — same as DSU for a single static count.

### The BFS↔DFS answer the interviewer wants

> "For one static count, DSU and BFS/DFS flood-fill are both `O(V + E)`. I'd use
> DSU here — it's the group's tool, it's a 5-line answer, and it's the one that
> keeps working if edges arrive incrementally (`O(α(n))` per edge vs re-running
> the whole flood-fill)."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = len(edges)`.

**Time:**
- One pass over `E` edges, one `union` each, amortized `O(α(n))`.
- **Total: `O(E · α(n))` ≈ `O(E)`.** (Plus `O(n)` to build the DSU.)

**Space:**
- `parent` + `rank`: `O(n)`.
- **Total: `O(n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| No edges | `count` stays `n` |
| All nodes connected | `count` drops to `1` |
| `n = 1` | `1` |
| Isolated nodes alongside clusters | they're never unioned → each still counts (started at `n`) |
| A cycle edge (`union` returns `False`) | `count` unchanged — correct |
| Duplicate edge (not in this problem's constraints, but) | second `union` returns `False` → no effect |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Decrementing `count` on *every* `union` call** instead of only when it
      returns `True`. A cycle edge would then wrongly cost a component (count can
      even go negative).
- [ ] **Starting `count` at `0` or `len(edges)`** instead of `n`.
- [ ] **`DSU(n + 1)`** — this problem is 0-indexed; `DSU(n)` is right.
- [ ] **Flood-fill version: iterating `for node in graph` instead of
      `range(n)`** — a node with no edges never appears as a key, so isolated
      nodes get missed.
- [ ] **Forgetting isolated nodes count as components** — they do; they're just
      never merged.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **`count = n`, `count -= 1` per successful `union`** — components without a
   graph search.
2. **Edges to make the graph fully connected = `components - 1`.**
3. The three faces of DSU — **count groups** (this), **find the cycle edge**
   (Redundant Connection), **validate a tree** (Graph Valid Tree) — are the
   *same* `union` loop reading a different signal.

| Problem | How this transfers |
|---|---|
| Number of Provinces | this exact idiom, input is an adjacency **matrix** |
| Number of Islands | components on a grid — DSU on `r*n + c` cell ids, or flood-fill |
| Accounts Merge | components of a "shares an email" graph, then group + sort |
| "Min edges to connect everything" | `components - 1` |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Edges arrive one at a time; report the component count **after each edge**."

- **(b) Pattern:** DSU online — its native mode.
- **(c) Adapt:** keep `count` alongside the DSU; on each incoming edge, `union`
  and do `count -= 1` if it returned `True`; emit `count`. `O(α(n))` per edge vs
  re-running an `O(V + E)` flood-fill each time.
- **(d) Say:** "Incremental component count is what DSU is *for* — one amortized
  near-constant operation per edge."

### Scenario 2 — "Also support edge **removal** — after deleting an edge, report the new count."

- **(b) Pattern:** DSU **can't un-merge**. This is the classic limitation.
- **(c) Adapt:** if all operations (adds and removes) are known in advance,
  process them **offline in reverse**: start from the final graph, and each
  "removal" replayed backward becomes an "addition" — plain DSU handles it, and
  you reverse the recorded answers. For truly online deletions with no
  lookahead, you need a fully-dynamic connectivity structure (link-cut trees or
  Euler-tour trees) — beyond DSU.
- **(d) Say:** "DSU supports additions in `O(α(n))` but not deletions —
  offline-reverse if you can see all operations upfront, otherwise a
  dynamic-connectivity structure."

### Scenario 3 — "Return the **size** of every component, not just the count."

- **(b) Pattern:** DSU with a `size` array.
- **(c) Adapt:** track `size[root]`, updated in `union` (add the smaller group's
  size into the larger's root). At the end, `{find(i): size[find(i)]}` gives each
  component's size — or bucket nodes by `find(i)` into a dict of lists.
  `O(E α(n) + n)`.
- **(d) Say:** "Add a `size` array maintained in `union`; then component sizes
  are a one-line read at the end."

### Scenario 4 — "Count only the components with an **odd** number of nodes (or `>= k` nodes, etc.)."

- **(b) Pattern:** same DSU + `size`, filter at the end.
- **(c) Adapt:** after processing all edges, iterate the roots
  (`{find(i) for i in range(n)}`) and count those whose `size` satisfies the
  predicate. `O(n)` for the final pass.
- **(d) Say:** "Any per-component predicate is a final `O(n)` scan over the roots
  once sizes are tracked."

### Scenario 5 — "`n` and edge count are both `10^7`. Handle the scale."

- **(b) Pattern:** DSU is already essentially optimal.
- **(c) Adapt:** iterative `find`, array-backed `parent`/`rank` (not dicts),
  stream edges straight into `union`. `O(E α(V)) ≈ O(E)` time, `O(V)` space. The
  flood-fill alternative needs an `O(V + E)` adjacency list on top.
- **(d) Say:** "Linear time, linear space, and no adjacency list to build — DSU
  is the leaner choice at `10^7`."

### Scenario 6 — "How many edges must you **add** to make the whole graph one connected component? And how many must you **remove** to make it a forest (acyclic)?"

- **(b) Pattern:** two direct corollaries of the DSU run.
- **(c) Adapt:** **To connect:** `components - 1` (each added edge between two
  components merges them). **To make a forest:** the number of `union` calls that
  returned `False` — equivalently `E - (n - components)` — each such edge is a
  redundant/cycle edge that can be removed without disconnecting anything.
- **(d) Say:** "`components - 1` edges to connect everything; `E - (n -
  components)` edges to remove down to a forest — both fall straight out of the
  same DSU pass."

---

## 15. Flashcards

**Q:** The idiom for counting components with DSU?
**A:** `count = n`; for each edge, `count -= 1` **only if** `union` returned
`True`.

**Q:** Why decrement only on a successful `union`?
**A:** A `union` that returns `False` connects two nodes already in the same
component — no merge, so no change to the count.

**Q:** Do isolated nodes count as components?
**A:** Yes. `count` starts at `n`; a node with no edges is never merged, so it
stays its own component.

**Q:** Time and space?
**A:** `O(E · α(n)) ≈ O(E)` time, `O(n)` space.

**Q:** Edges to connect everything into one component?
**A:** `components - 1`.

**Q:** Edges to remove to make the graph a forest?
**A:** The count of `union` calls that returned `False` (= `E - (n -
components)`).

**Q:** DSU vs flood-fill here — the deciding factor?
**A:** For one static count they're both `O(V + E)`. DSU wins if edges arrive
incrementally, or you have many connectivity queries.

**Q:** The three faces of DSU across Group 07?
**A:** Count groups (this), find the cycle-closing edge (Redundant Connection),
validate a tree (Graph Valid Tree) — same `union` loop, different signal read.

---

## Appendix — Tejas's LeetCode Practice Answer (DFS flood-fill, not DSU)

Solved and accepted on LeetCode. This is the **other** valid approach for this
problem — the "loop + flood" counting skeleton from `concepts/05`, using DFS
instead of Union-Find.

```python
from collections import defaultdict


class Solution:
    def countComponents(self, n: int, edges: list[list[int]]) -> int:
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = set()
        components = 0

        def dfs(node):
            visited.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        for i in range(n):                 # outer loop over ALL node ids
            if i not in visited:
                components += 1            # a brand-new, untouched component
                dfs(i)                     # DFS floods the whole component into `visited`

        return components
```

**Correct** — verified against all 6 tests from section 8.

### The logic, step by step

**Two pieces working together:**

1. **The flood (`dfs`)** — starting from one node, recursively visit every node
   reachable from it, adding each to `visited`. When `dfs(i)` finishes, *every
   node in `i`'s connected component* is in `visited`. It's a graph-shaped
   version of "scribble over the whole island" from Number of Islands.

2. **The outer loop** — walk through **every** node id `0..n-1`. For each one:
   - If it's **already in `visited`**, some earlier `dfs` already claimed its
     component → skip it, don't count it again.
   - If it's **not in `visited`**, it belongs to a component **no `dfs` has
     touched yet** → that's a new component we haven't counted, so
     `components += 1`, then `dfs(i)` floods the rest of it so those nodes get
     skipped later.

**Why the count is exactly right:**
- Every component gets counted **at least once** — the outer loop eventually
  reaches *some* node of every component (it visits all `n` ids), and the first
  time it reaches an unvisited node of a component, `components += 1` fires.
- Every component gets counted **at most once** — the moment one node of a
  component triggers the `+= 1`, the `dfs` marks *all* of that component's nodes
  visited, so every later node of the same component hits the `if i not in
  visited` guard and is skipped.
- **Isolated nodes** (no edges) work automatically: such a node is never added to
  `visited` by anyone else's `dfs`, so the outer loop finds it unvisited,
  counts it as its own component, and `dfs(i)` immediately returns (empty
  neighbor list).

**`iterate range(n)`, not `for node in adj`:** a node with no edges never becomes
a key in the `defaultdict`, so looping over `adj` would silently skip isolated
nodes and undercount. Always loop over the full id range.

### DSU vs this

| | DSU (primary) | DFS flood-fill (this) |
|---|---|---|
| Time | `O(E · α(n)) ≈ O(E)` | `O(V + E)` |
| Space | `O(n)` (parent/rank) | `O(V + E)` (adjacency list) + `O(V)` recursion |
| Incremental edges | `O(α(n))` per edge — re-answer instantly | must rebuild + re-flood, `O(V + E)` each time |
| Recursion depth | none | up to `O(n)` — a long chain can `RecursionError`; raise the limit or go iterative |

Both are fine interview answers for a **single static count**. DSU is the group's
tool and the one that stays cheap under incremental edges.
