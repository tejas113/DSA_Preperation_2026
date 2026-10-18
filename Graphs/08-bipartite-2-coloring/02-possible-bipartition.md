# Possible Bipartition  ·  LeetCode 886  ·  Medium

Group 08 — Bipartite / 2-Coloring  ·  Is Graph Bipartite?, but you **build the
graph first** from a list of "dislikes" pairs.

Prereqs: `01-is-graph-bipartite.md` (the 2-coloring is identical),
`concepts/09-bipartite-coloring.md`, `concepts/02` (building an adjacency list).

---

## 1. Problem

There are `n` people labeled `1..n`. You want to split them into **two groups**
of any size. `dislikes[i] = [a, b]` means person `a` and person `b` **cannot be
in the same group**.

**Return `True` if such a split is possible.**

Constraints:
- `1 <= n <= 2000`, `0 <= dislikes.length <= 10^4`.
- People are **1-indexed** (`1..n`).

Example 1:

```
n = 4, dislikes = [[1,2],[1,3],[2,4]]
answer = True         # {1,4} and {2,3}
```

Example 2:

```
n = 3, dislikes = [[1,2],[1,3],[2,3]]
answer = False        # 1-2-3-1 triangle: an odd cycle of dislikes
```

Example 3:

```
n = 5, dislikes = [[1,2],[2,3],[3,4],[4,5],[1,5]]
answer = False        # a 5-cycle of dislikes (odd)
```

---

## 2. Explain Like I'm 5

Exactly the "two fair teams" story from Is Graph Bipartite? — the only new part
is that nobody hands you the graph. You're handed a list of "these two don't get
along," and you have to *draw* the graph yourself: one dot per person, one line
per dislike.

Once you've drawn it, it's the same job: 2-color it. If you can, the two colors
are your two groups. If an odd cycle of dislikes forces a clash, it's
impossible.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Split `n` things into **two** groups" | ✅ |
| Constraints given as **conflict pairs**, not an adjacency list | ✅ → build the graph |
| "Cannot be together" / "dislikes" / "enemies" | ✅ → edges of the conflict graph |

**Reduce it to:** *"Build an adjacency list from `dislikes`, then 2-color it
(BFS/DFS) exactly like Is Graph Bipartite?"*

**Look-alike:** Is Graph Bipartite? — this problem *is* that, plus the
graph-construction step and 1-indexing.

---

## 4. Intuition

1. A "dislike" between `a` and `b` is exactly an edge saying "opposite groups."
   So `dislikes` **is** an edge list of a conflict graph.
2. Build the adjacency list (undirected — add both directions), sized `n + 1`
   because people are `1..n`.
3. Now the question "can everyone be split into two groups with all dislikes
   crossing the divide" is **verbatim** "is this conflict graph bipartite" — 2-
   color it.
4. Loop over people `1..n` as start nodes (there may be several disconnected
   friend/enemy clusters).

---

## 5. Approach (primary): build adjacency list + BFS 2-coloring

1. `graph = defaultdict(list)`; for `[a, b]` in `dislikes`: `graph[a].append(b)`,
   `graph[b].append(a)`.
2. `color = [0] * (n + 1)` (index `0` unused).
3. For `start` in `1..n`: if `color[start] != 0`, skip. Else `color[start] = 1`,
   BFS: color each neighbor `-color[node]`; same-color edge → return `False`.
4. Return `True`.

Builds on: `01-is-graph-bipartite.md` (the coloring), `concepts/02` (edge list →
adjacency list).

---

## 6. Pseudocode

```
function possibleBipartition(n, dislikes):
    graph = adjacency list from dislikes (undirected)
    color = [0] * (n + 1)
    for start in 1 .. n:
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
n = 4, dislikes = [[1,2],[1,3],[2,4]]
```

`graph = {1:[2,3], 2:[1,4], 3:[1], 4:[2]}`. `color = [0,0,0,0,0]`.

`start = 1`: `color[1] = 1`, `q = [1]`.

| pop | node color | neighbors | color after | queue after |
|---|---|---|---|---|
| 1 | 1 | `2`→`-1`, `3`→`-1` | `[_,1,-1,-1,0]` | `[2,3]` |
| 2 | -1 | `1`=`1`=`-color[2]` ✓ ; `4`→`1` | `[_,1,-1,-1,1]` | `[3,4]` |
| 3 | -1 | `1`=`1` ✓ | — | `[4]` |
| 4 | 1 | `2`=`-1` ✓ | — | `[]` |

No conflict. `start = 2,3,4` already colored. Return `True` — groups `{1,4}` and
`{2,3}`. ✅

---

## 8. Python Code (primary — build + BFS 2-color)

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        graph = defaultdict(list)
        for a, b in dislikes:
            graph[a].append(b)
            graph[b].append(a)

        color = [0] * (n + 1)                  # 1-indexed people; index 0 unused

        for start in range(1, n + 1):
            if color[start] != 0:
                continue
            color[start] = 1
            q = deque([start])
            while q:
                node = q.popleft()
                for nei in graph[node]:
                    if color[nei] == 0:
                        color[nei] = -color[node]
                        q.append(nei)
                    elif color[nei] == color[node]:
                        return False
        return True


if __name__ == "__main__":
    sol = Solution()

    assert sol.possibleBipartition(4, [[1, 2], [1, 3], [2, 4]]) is True
    assert sol.possibleBipartition(3, [[1, 2], [1, 3], [2, 3]]) is False
    assert sol.possibleBipartition(5, [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]) is False
    assert sol.possibleBipartition(5, [[1, 2], [3, 4], [4, 5], [3, 5]]) is False   # triangle 3-4-5
    assert sol.possibleBipartition(4, []) is True
    assert sol.possibleBipartition(1, []) is True
    assert sol.possibleBipartition(10, [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]) is True

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS 2-coloring (same graph construction)

Identical to `01-is-graph-bipartite.md` §9a, iterating `range(1, n + 1)`.

### 9b. Union-Find with `2n` slots (natural for streaming / mixed constraints)

DSU sized `2n` (slots `0..n-1` for "person `i` in group A", `n..2n-1` for "person
`i` in group B", using `i-1` as the base for 1-indexed people). For each
`[a, b]`: `union(a, b + n)` and `union(b, a + n)`. If `find(a) == find(b)` ever
holds, `a` and `b` are forced into the same group → return `False`.
`O((n + E) α(n))`.

### The BFS↔DFS answer the interviewer wants

> "Same as Is Graph Bipartite? once the graph is built: 2-color with BFS or DFS,
> `O(V + E)`, loop over all components since dislike clusters can be
> disconnected. The only extra step is turning the `dislikes` pair list into an
> adjacency list first."

---

## 10. Complexity — derived step by step

**V and E:** `V = n` people, `E = len(dislikes)` edges.

**Time:**
- Build adjacency list: `O(E)`.
- BFS/DFS 2-coloring over all components: `O(V + E)`.
- **Total: `O(V + E)`.**

**Space:**
- Adjacency list: `O(V + E)`.
- `color` array + queue/stack: `O(V)`.
- **Total: `O(V + E)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `dislikes = []` | no edges → everyone in one group → `True` |
| `n = 1` | single person, no constraints → `True` |
| A dislike triangle (3-cycle) | odd cycle → `False` |
| Any odd cycle of dislikes | same-color conflict → `False` |
| Disconnected dislike clusters | outer loop `1..n` colors each |
| A person with no dislikes | never enters anyone's BFS via an edge; the outer loop colors them `1` alone |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **`color = [0] * n` instead of `[0] * (n + 1)`.** People are 1-indexed;
      `color[n]` would `IndexError`.
- [ ] **Looping `range(n)` instead of `range(1, n + 1)`** — skips person `n`,
      processes non-person `0`.
- [ ] **Building the graph one-directional** — `dislikes` is symmetric ("`a`
      dislikes `b`" ⟹ "`b` dislikes `a`"); add both `graph[a].append(b)` and
      `graph[b].append(a)`.
- [ ] **All the Is Graph Bipartite? bugs** — only coloring one component,
      coloring at dequeue, inverted conflict test, `0` as a real color.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **"Conflict pairs" → edge list of a conflict graph → 2-color it.** The problem
   hides the graph; your first move is to build it.
2. Everything downstream is Is Graph Bipartite? — 2-coloring, odd-cycle
   detection, loop all components.
3. **Watch the index base** — 1-indexed people ⟹ arrays sized `n + 1`.
4. **Mixed constraints (must-be-together *and* must-be-apart)** push you toward
   the `2n`-slot Union-Find (Scenario 1).

| Problem | How this transfers |
|---|---|
| Is Graph Bipartite? | this, minus the graph-construction step |
| "Two-shift scheduling with conflict pairs" | conflict graph + 2-coloring |
| "Divide items into two boxes; some pairs can't share a box" | identical |
| 2-SAT-lite / constraint feasibility | equality + inequality constraints → `2n`-slot DSU |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Also given a list of **must-be-together** (friend) pairs — friends share a group, enemies don't."

- **(b) Pattern:** equality *and* inequality constraints → the `2n`-slot
  **Union-Find**.
- **(c) Adapt:** DSU of size `2n`. For a **friend** pair `(a, b)`:
  `union(a, b)` and `union(a + n, b + n)` (same side). For an **enemy** pair
  `(a, b)`: `union(a, b + n)` and `union(b, a + n)` (opposite sides). After
  processing all constraints (or during), if `find(a) == find(a + n)` for any
  `a`, that person is forced into both groups → **impossible**. `O((n + C) α(n))`
  for `C` constraints.
- **(d) Say:** "Friends *and* enemies is the classic `2n`-slot Union-Find — a
  'real' slot and an 'opposite' slot per person; union same-side for friends,
  cross-side for enemies, and a person unioned with their own opposite slot is a
  contradiction."

### Scenario 2 — "Return the actual two groups."

- **(b) Pattern:** partition by color.
- **(c) Adapt:** run the 2-coloring; `group_a = [i for i in 1..n if color[i] ==
  1]`, `group_b = [i for i in 1..n if color[i] == -1]`. Return them if bipartite,
  else `[]`. `O(V + E)`.
- **(d) Say:** "The `color` array *is* the partition — split the people by their
  final color."

### Scenario 3 — "Among all valid splits, minimize the **size difference** between the two groups."

- **(b) Pattern:** per-component the coloring is forced *up to swapping the two
  colors*, so you choose, per component, which color-class goes to group A →
  a **partition / subset-sum** over the components.
- **(c) Adapt:** for each connected component, count `(size_of_color_1,
  size_of_color_-1)`; its contribution to `|A| - |B|` is `±(size_1 - size_-1)`
  depending on the orientation you pick. Minimize `|Σ ± d_component|` — a
  subset-sum DP over the per-component differences `d`. With `n ≤ 2000` the total
  range is bounded, so a pseudo-polynomial `O(n · #components)` DP works;
  in general this is Partition (NP-hard) but pseudo-poly is fine at this scale.
- **(d) Say:** "Each component's coloring is fixed except for a global flip, so
  balancing the groups is a subset-sum over the components' size-differences —
  pseudo-polynomial DP given the bounded total."

### Scenario 4 — "Dislikes **stream in**; after each, report whether a valid split still exists."

- **(b) Pattern:** incremental → `2n`-slot Union-Find.
- **(c) Adapt:** maintain the DSU across the stream. On each `[a, b]`: check
  `if find(a) == find(b): report "impossible"`; then `union(a, b + n)` and
  `union(b, a + n)`. `O(α(n))` per dislike vs re-running the `O(V + E)` coloring.
- **(d) Say:** "Streaming bipartiteness is the `2n`-slot Union-Find — same as the
  incremental version of Is Graph Bipartite?."

### Scenario 5 — "You may **ignore up to `K`** dislikes. Can everyone then be split?"

- **(b) Pattern:** "delete ≤ `K` edges to make the graph bipartite" = **odd cycle
  transversal** — **NP-hard** in general.
- **(c) Adapt:** for small `K`, brute-force which `K` dislikes to drop and test
  each subset (`O(C(E, K) · (V + E))`). For larger `K`, it's fixed-parameter
  tractable in `K` (there's an `O(3^K · (V + E))` algorithm), or you use an
  approximation. Name the hardness rather than pretending it's polynomial.
- **(d) Say:** "Ignoring up to `K` conflicts to force bipartiteness is odd-cycle
  transversal — NP-hard, though FPT in `K`; small `K` is brute-forceable."

### Scenario 6 — "`n` is `10^7` people and `10^7` dislikes."

- **(b) Pattern:** the coloring is already `O(V + E)`.
- **(c) Adapt:** build the adjacency list as arrays (or CSR), iterative BFS,
  byte-array `color`. `O(V + E)` time, `O(V + E)` space. The `2n`-slot DSU is
  also `O(E α(n))` and uses only `O(n)` beyond the input.
- **(d) Say:** "Linear either way — iterative BFS with a byte-array color map, or
  the `2n`-slot DSU if I want to avoid building the adjacency list."

---

## 15. Flashcards

**Q:** How does Possible Bipartition differ from Is Graph Bipartite?
**A:** You build the adjacency list from the `dislikes` pair list first; people
are 1-indexed (arrays sized `n + 1`). Then it's the identical 2-coloring.

**Q:** What does a "dislike" pair `[a, b]` become?
**A:** An undirected edge `a–b` in a conflict graph meaning "opposite groups."

**Q:** The answer is `False` exactly when...?
**A:** The dislike graph has an odd-length cycle (a same-color conflict during
2-coloring).

**Q:** Time and space?
**A:** `O(V + E)` both — build the adjacency list, then a BFS/DFS 2-coloring.

**Q:** Friends (must-be-together) *and* enemies (must-be-apart) — the tool?
**A:** `2n`-slot Union-Find: `union(a, b)` + `union(a+n, b+n)` for friends,
`union(a, b+n)` + `union(b, a+n)` for enemies; `find(a) == find(a+n)` ⟹
impossible.

**Q:** "Ignore up to `K` dislikes" — hardness?
**A:** Odd-cycle transversal — NP-hard in general (FPT in `K`); small `K` is
brute-forceable.

**Q:** The two index-base bugs to avoid?
**A:** `color` sized `n` not `n + 1`; looping `range(n)` not `range(1, n + 1)`.
