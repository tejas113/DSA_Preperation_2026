# Minimum Height Trees  ·  LeetCode 310  ·  Medium  ·  *(supplementary)*

Group 06 — Topological Sort / Cycle Detection  ·  Kahn's algorithm's **idea**
(peel from the boundary inward) applied to an **undirected tree**, peeling by
**degree** instead of indegree.

Prereqs: `concepts/07` (topological sort — especially the "leaf-peeling variant"
note at the end), `concepts/03` (BFS layer counting). New idea: **the answer is
structurally forced to be 1 or 2 nodes** — the tree's center — so you find it
directly, not by testing all `n` candidates.

---

## 1. Problem

A tree is a connected undirected graph with `n` nodes (labeled `0..n-1`) and
exactly `n - 1` edges. If you pick a node as the **root**, the tree gets a
**height** = the longest downward path from that root to any leaf.

Different roots give different heights. **Return the list of all root choices
that produce the minimum possible height** (a Minimum Height Tree, "MHT"). There
are always **1 or 2** such roots.

Constraints:
- `1 <= n <= 2 * 10^4`.
- `edges.length == n - 1`; the input is guaranteed to be a valid tree.

Example 1:

```
n = 4, edges = [[1,0],[1,2],[1,3]]     (a star with hub 1)
answer = [1]        # rooting at 1 -> height 1; rooting anywhere else -> height 2
```

Example 2:

```
n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
answer = [3, 4]
```

---

## 2. Explain Like I'm 5

Imagine the tree is a real tree branch lying on the ground, with twigs sticking
out. You want to pick the spot to pick it up from so it hangs with the **shortest
possible longest droop**.

The best spot is the **middle** of the branch. To find the middle without a
ruler: grab all the twig-tips (the leaves — nodes with only one connection) and
snip them all off at once. Now the branch is a little shorter and has new tips.
Snip those. Keep snipping whole layers of tips.

Eventually you're left holding just **one** little piece, or **two** pieces stuck
together. That's the middle — the best place(s) to hang the tree from.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Undirected **tree** (n nodes, n-1 edges, connected) | ✅ |
| "Minimize the maximum distance to anything" / "find the center" | ✅ |
| The answer is a small, bounded set (1 or 2) | ✅ → find it directly, don't test all `n` roots |
| Naive "BFS from every node, keep the min height" is `O(n²)` | ✅ (n up to 2×10⁴ → 4×10⁸, too slow) |

**Reduce it to:** *"Repeatedly remove all current leaves (degree-1 nodes) layer
by layer; the 1 or 2 nodes that survive are the answer."* This is **leaf-peeling**
— Kahn's algorithm generalized: instead of "remove indegree-0 nodes from a
directed graph," it's "remove degree-1 nodes from an undirected tree."

**Look-alikes:**
- Course Schedule (Kahn's on a directed graph) — same peel-from-the-outside idea,
  different "what counts as removable."
- Tree **centroid** (minimize the largest component after removing a node) — a
  *different* notion of "center," solved by subtree-size DP, not leaf-peeling
  (Scenario 4).

---

## 4. Intuition

1. **Why the answer is always 1 or 2 nodes.** The height of the best-rooted tree
   is governed by the tree's **longest path** (its diameter). The optimal root
   sits at the **middle** of that longest path — and the middle of a path is
   either one node (if the path has an even number of edges) or two adjacent
   nodes (odd number of edges). No tree has 3+ equally-central nodes.
2. **Why leaf-peeling finds that middle.** Every leaf is, by definition, an
   *endpoint* of some longest-ish path — it's maximally far from the center.
   Removing all leaves at once moves the "frontier" one step inward from every
   extremity simultaneously. After `k` rounds of peeling, you've stripped away
   everything within distance `k` of the original boundary. The last survivors
   are the nodes maximally far from *all* leaves — i.e., the nodes that minimize
   the maximum distance to any leaf — i.e., the minimum-height roots.
3. **Process one whole layer at a time** (freeze the leaf count before the round,
   exactly like Rotting Oranges' ring counting) — if you let newly-created
   leaves be peeled in the same round, you collapse all the layers and get the
   wrong survivors.
4. Stop when `2` or fewer nodes remain.

---

## 5. Approach (primary): leaf-peeling (BFS by degree)

1. If `n <= 2`: return `list(range(n))` (`[0]` or `[0, 1]` — both trivially
   minimum-height).
2. Build adjacency list; `degree[i] = len(graph[i])`.
3. `leaves = deque(i for i in range(n) if degree[i] == 1)`. `remaining = n`.
4. While `remaining > 2`:
   - `layer = len(leaves)`; `remaining -= layer`.
   - Repeat `layer` times: pop a leaf; for its (one) still-connected neighbor,
     `degree[nei] -= 1`; if `degree[nei] == 1`, append it to `leaves`.
5. Return `list(leaves)` — whatever's left is the 1 or 2 centers.

Builds on: `concepts/07` (leaf-peeling), `concepts/03` (freeze-the-layer BFS).

---

## 6. Pseudocode

```
function findMinHeightTrees(n, edges):
    if n <= 2: return [0 .. n-1]

    graph = adjacency list
    degree[i] = number of neighbors of i

    leaves = queue of all nodes with degree 1
    remaining = n

    while remaining > 2:
        layer = len(leaves)
        remaining -= layer
        repeat layer times:
            leaf = dequeue
            for nei in graph[leaf]:
                degree[nei] -= 1
                if degree[nei] == 1:
                    enqueue nei

    return list(leaves)
```

---

## 7. Dry Run

```
n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
```

Adjacency: `0:[3] 1:[3] 2:[3] 3:[0,1,2,4] 4:[3,5] 5:[4]`.
`degree = [1, 1, 1, 4, 2, 1]`. `leaves = [0, 1, 2, 5]`. `remaining = 6`.

**Round 1:** `remaining (6) > 2`. `layer = 4`. `remaining = 6 - 4 = 2`.

| pop leaf | neighbor | degree update | new leaf? | leaves after |
|---|---|---|---|---|
| 0 | 3 | degree[3]: 4→3 | no | [1,2,5] |
| 1 | 3 | degree[3]: 3→2 | no | [2,5] |
| 2 | 3 | degree[3]: 2→1 | **yes** → append 3 | [5,3] |
| 5 | 4 | degree[4]: 2→1 | **yes** → append 4 | [3,4] |

**Round 2 check:** `remaining (2) > 2`? No → stop.

`leaves = [3, 4]` → return `[3, 4]`. ✅

(Star example `n=4, edges=[[1,0],[1,2],[1,3]]`: `degree=[1,3,1,1]`,
`leaves=[0,2,3]`, `remaining=4`. Round 1: `layer=3`, `remaining=1`. Popping `0`
drops `degree[1]` 3→2; popping `2` drops it 2→1 → append `1`; popping `3` drops it
1→0 → **not** appended (0, not 1). `leaves=[1]`. `remaining (1) > 2`? No. Return
`[1]`.)

---

## 8. Python Code (primary — leaf-peeling)

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))

        graph = defaultdict(set)
        for a, b in edges:
            graph[a].add(b)
            graph[b].add(a)

        degree = [len(graph[i]) for i in range(n)]
        leaves = deque(i for i in range(n) if degree[i] == 1)
        remaining = n

        while remaining > 2:
            layer = len(leaves)
            remaining -= layer
            for _ in range(layer):
                leaf = leaves.popleft()
                for nei in graph[leaf]:
                    degree[nei] -= 1
                    if degree[nei] == 1:
                        leaves.append(nei)

        return list(leaves)


if __name__ == "__main__":
    sol = Solution()

    assert sorted(sol.findMinHeightTrees(4, [[1, 0], [1, 2], [1, 3]])) == [1]
    assert sorted(sol.findMinHeightTrees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]])) == [3, 4]
    assert sol.findMinHeightTrees(1, []) == [0]
    assert sorted(sol.findMinHeightTrees(2, [[0, 1]])) == [0, 1]
    assert sorted(sol.findMinHeightTrees(5, [[0, 1], [1, 2], [2, 3], [3, 4]])) == [2]      # path of 5
    assert sorted(sol.findMinHeightTrees(4, [[0, 1], [1, 2], [2, 3]])) == [1, 2]           # path of 4

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Find the diameter, take its middle (two BFS passes)

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))

        graph = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        def bfs_farthest(start):
            parent = {start: None}
            q = deque([start])
            last = start
            while q:
                node = q.popleft()
                last = node
                for nei in graph[node]:
                    if nei not in parent:
                        parent[nei] = node
                        q.append(nei)
            return last, parent

        u, _ = bfs_farthest(0)          # farthest node from an arbitrary start
        v, parent = bfs_farthest(u)     # farthest from u  ->  u..v is a diameter

        path = []
        cur = v
        while cur is not None:
            path.append(cur)
            cur = parent[cur]

        L = len(path)
        return [path[L // 2]] if L % 2 else [path[L // 2 - 1], path[L // 2]]
```

The "2 BFS to find a tree's diameter" trick (BFS from anywhere → farthest node
`u`; BFS from `u` → farthest node `v`; `u..v` is a longest path) is worth
knowing on its own. The MHT roots are just its 1 or 2 middle nodes. Also `O(n)`.

### The BFS↔DFS answer the interviewer wants

> "Leaf-peeling is BFS by degree — `O(n)`, and it directly hands you the 1–2
> center nodes. The diameter-midpoint approach is also `O(n)` and gives more
> insight into *why* the answer is the center. I'd code leaf-peeling for its
> directness and mention the diameter view as the intuition."

---

## 10. Complexity — derived step by step

**V and E:** `V = n`, `E = n - 1` (it's a tree).

**Time:**
- Build adjacency list + degree array: `O(n)`.
- Leaf-peeling: every node is enqueued **at most once** (when its degree drops to
  1), dequeued once, and each edge is examined once (when one of its endpoints is
  peeled and decrements the other) → `O(n)`.
- **Total: `O(n)`.** (Naive "BFS from every node" would be `O(n²)`.)

**Space:**
- Adjacency list: `O(n)`. Degree array + queue: `O(n)`.
- **Total: `O(n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `n = 1` (single node, degree 0) | `if n <= 2: return list(range(n))` → `[0]` (without this, `leaves` is empty and you'd return `[]`) |
| `n = 2` (one edge) | `n <= 2` guard → `[0, 1]` (both are minimum-height roots) |
| A path graph, odd number of nodes | one center — e.g. `0-1-2-3-4` → `[2]` |
| A path graph, even number of nodes | two centers — e.g. `0-1-2-3` → `[1, 2]` |
| A star | the hub is the sole center |
| Peeling a node whose degree drops to `0` (last node standing in some branch collapse) | **not** re-added as a leaf — only `degree == 1` triggers an append |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Missing the `n <= 2` guard.** `n = 1` has a degree-`0` node, never a
      "leaf," so `leaves` starts empty and you'd return `[]` instead of `[0]`.
- [ ] **Not freezing `len(leaves)` before the round.** If you loop
      `while leaves` and let newly-appended leaves be processed in the same pass,
      all layers collapse into one and the survivors are wrong. Freeze the count
      (like Rotting Oranges' ring counting).
- [ ] **Decrementing `remaining` one node at a time and re-checking mid-round.**
      You can stop partway through a layer and return an inconsistent set.
      Subtract the whole `layer` at once, then check.
- [ ] **Appending a new leaf on `degree <= 1` instead of `== 1`.** A node whose
      degree hits `0` would get wrongly re-queued.
- [ ] **Testing `while remaining >= 2` instead of `> 2`.** With `>= 2` you'd
      peel one round too many when exactly 2 nodes remain, returning `[]` or a
      single wrong node.
- [ ] **Using `list` neighbor lists and trying to `.remove()` peeled leaves** —
      unnecessary and `O(degree)` each; just decrement a `degree` counter.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Leaf-peeling is Kahn's algorithm for undirected trees** — "repeatedly
   remove the boundary" where the boundary is degree-1 nodes (vs indegree-0 for
   directed graphs).
2. **When the answer is structurally bounded, find it directly.** A tree's
   minimum-height roots *must* be 1 or 2 central nodes — so an `O(n)` peel beats
   an `O(n²)` "try every root."
3. **The 2-BFS tree-diameter trick** (BFS to a farthest node, BFS again from
   there) is a standalone tool for any "longest path in a tree" question.
4. **Freeze-the-layer BFS** (Rotting Oranges) reused again — process a whole
   frontier before advancing.

| Situation | How this transfers |
|---|---|
| "Longest path / diameter of a tree" | the 2-BFS trick from 9a |
| "Best place on a tree to build a facility, minimizing worst-case travel" | this exact problem — the MHT center is the 1-center of the tree |
| "Trim a tree to its core / find its skeleton" | leaf-peeling, stopping at a chosen layer instead of at 2 nodes |
| Tree centroid (minimize largest component after removal) | a *different* center — subtree-size DP, not peeling (Scenario 4) |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Also return the minimum height value itself, not just the root(s)."

- **(b) Pattern:** count the peel layers.
- **(c) Adapt:** keep a `layers` counter, `+= 1` each round of peeling. When you
  stop, the minimum height is exactly `layers` (if one center remains) or
  `layers` as well (if two remain — rooting at either, the far side is `layers`
  deep). Equivalently, `min_height = (diameter_in_edges + 1) // 2`. `O(n)`,
  unchanged.
- **(d) Say:** "The number of peeling rounds *is* the minimum height — each round
  strips one level off the deepest branches."

### Scenario 2 — "The input is a **forest** (several disconnected trees), not one tree. Return the MHT root(s) for each component."

- **(b) Pattern:** leaf-peeling per component.
- **(c) Adapt:** first identify components (one pass of BFS/DFS or Union-Find).
  Then run leaf-peeling **within each component**, stopping each one at its own
  1–2 survivors (track `remaining` per component). Return a list of results, one
  per component. `O(n)` total.
- **(d) Say:** "A forest is just 'do the tree algorithm once per component' —
  identify components first, then peel each independently."

### Scenario 3 — "Edges have **weights** (lengths); minimize the *weighted* height."

- **(b) Pattern:** **leaf-peeling breaks** — a single long edge shifts the true
  center, and degree no longer tracks distance. You need eccentricity
  computation.
- **(c) Adapt:** compute each node's **eccentricity** (max weighted distance to
  any other node) and return the node(s) minimizing it. Efficiently: find a
  weighted diameter via two Dijkstra/BFS-on-tree passes (the same
  farthest-then-farthest trick, with weights); the center lies on that diameter
  path. If the exact center falls *between* two nodes (possible with weights) and
  only node roots are allowed, pick the diameter-path endpoint of that segment
  with the smaller eccentricity. A rerooting tree-DP also computes all
  eccentricities in `O(n)`.
- **(d) Say:** "Weights sever the link between degree and distance, so
  leaf-peeling stops working — I'd switch to computing eccentricities via the
  weighted-diameter path, or an O(n) rerooting DP."

### Scenario 4 — "Instead of minimizing height, find the node whose removal splits the tree into components whose **largest part is smallest** (the tree's centroid)."

- **(b) Pattern:** a *different* notion of center — the **centroid**, solved by
  **subtree-size DP**, not leaf-peeling.
- **(c) Adapt:** root the tree anywhere, compute `subtree_size[v]` for all `v`
  via one DFS. For each node `v`, the largest piece if `v` is removed is
  `max( max over children c of subtree_size[c],  n - subtree_size[v] )`. Return
  the `v` minimizing that. Also 1 or 2 nodes, also `O(n)` — but a genuinely
  different computation from MHT's peeling.
- **(d) Say:** "'Center by height' (this problem) and 'centroid by component
  size' are two different centers of a tree — one is leaf-peeling / diameter
  midpoint, the other is subtree-size DP. Worth clarifying which the interviewer
  means."

### Scenario 5 — "`n` is `10^7` and edges are streamed. Handle the scale."

- **(b) Pattern:** same algorithm, tighter data structures.
- **(c) Adapt:** the algorithm is already `O(n)` time and space. For `10^7`
  nodes, use array-of-lists (or a CSR/flat adjacency representation) instead of a
  `defaultdict(set)` to cut constant-factor memory, and an integer `degree`
  array. Edges can be consumed straight from the stream into the adjacency
  structure. Nothing about the leaf-peeling logic changes.
- **(d) Say:** "It's already linear — at `10^7` I'd only swap the hash-based
  adjacency for flat arrays to shrink the constant factor; the peel itself is
  untouched."

### Scenario 6 — "The tree grows over time: new leaf nodes get attached one at a time. After each attachment, report the current MHT root(s)."

- **(b) Pattern:** incremental **diameter maintenance**.
- **(c) Adapt:** maintain the current diameter's two endpoints `(a, b)`. When a
  new node `x` is attached, compute `dist(x, a)` and `dist(x, b)` (via a distance
  query — `O(log n)` with binary-lifting LCA, or `O(current diameter)` naively).
  If either exceeds the current diameter, the new diameter is `x..a` or `x..b`;
  update the endpoints and recompute the midpoint(s). Only a bounded amount of
  work per insertion.
- **(d) Say:** "Adding a leaf can only extend the diameter through that leaf, so
  I maintain the two diameter endpoints and, on each insertion, check the new
  node's distance to both — if it makes a longer path, re-center on the new
  diameter."

---

## 15. Flashcards

**Q:** What is Minimum Height Trees, in one line?
**A:** Find the 1 or 2 **center** nodes of an undirected tree by **leaf-peeling**
— repeatedly remove all degree-1 nodes, layer by layer, until ≤ 2 remain.

**Q:** Why is the answer always 1 or 2 nodes?
**A:** The optimal root is the middle of the tree's longest path (diameter) —
one node if the diameter has an even number of edges, two if odd.

**Q:** How is leaf-peeling related to Kahn's algorithm?
**A:** It's Kahn's "remove the boundary inward" idea for undirected trees:
peel degree-1 nodes instead of indegree-0 nodes.

**Q:** The two must-freeze / must-guard details?
**A:** Freeze `len(leaves)` before each round (don't peel newly-created leaves
in the same round); and special-case `n <= 2` (a single node has degree 0, never
a "leaf").

**Q:** Only append a new leaf when its degree becomes exactly what?
**A:** `== 1`. A node hitting degree `0` must **not** be re-queued.

**Q:** Time and space, vs the naive approach?
**A:** `O(n)` both. Naive "BFS from every node, keep the min height" is `O(n²)`.

**Q:** The 2-BFS tree-diameter trick?
**A:** BFS from any node → farthest node `u`; BFS from `u` → farthest node `v`;
`u..v` is a diameter. The MHT roots are its middle 1–2 nodes.

**Q:** "Center by height" vs "centroid by size" — the difference?
**A:** MHT center minimizes max *distance* (leaf-peeling / diameter midpoint).
The centroid minimizes the largest *component* after removal (subtree-size DP).
Different centers, both `O(n)`, both 1–2 nodes.
