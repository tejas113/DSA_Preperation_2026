# 684. Redundant Connection

**LC 684** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Union-Find (disjoint set union): the first edge whose two ends are already connected closes a cycle

---

## 1. Intuition

You're given a tree with **one extra edge**, and that extra edge creates exactly one cycle. Add the edges one
at a time, keeping track of which nodes are already connected. An edge whose two ends are **already in the
same group** doesn't connect anything new. It closes the cycle, so it's the redundant one.

* **`parent` = each node's link toward its group leader:** at the start, `parent = [i for i in range(n+1)]`, so every node leads its own group. Index 0 isn't used, because nodes are numbered 1…n.
* **`find(i)` returns the group leader (the root):** it follows `parent` links up to the node whose `parent[i] == i`. On the way back it does `parent[i] = find(parent[i])`, which points every node it passed **straight at the root**. That's **path compression**.
* **`union(u, v)` merges two groups, or reports a cycle:** if `find(u) == find(v)`, they're already connected, so it returns `False` and that edge is the answer. Otherwise `parent[root_u] = root_v` joins the groups.
* **Why "first failing edge" = "last edge of the cycle in the input":** the graph has exactly one cycle. The edges before the failing one form no cycle, so the failing edge is the cycle edge that comes **last** in the input, which is what LeetCode asks for.

**Recall:** `parent[i] = i`. For each edge, `union(u, v)`. If `find(u) == find(v)` already, return `[u, v]`. `find` uses path compression.

## 2. Approach

* **Idea:** Process the edges in order and keep connected groups with union-find. The first edge that joins two nodes already in the same group creates a cycle, and that's the redundant connection.
* **Graph representation:** **edge list**, **undirected**, unweighted. The nodes are `1 … n`, where `n = len(edges)` (a tree on n nodes has n − 1 edges, plus the 1 extra).
* **Data structure / pointers:**
  * `parent[i]`: the node `i` points to on the way to its group's root. A node is a root when `parent[i] == i`.
  * `find(i)`: **recursive**, with **path compression**. After the call, every node on the path points directly to the root.
  * `union(u, v)`: links `u`'s root under `v`'s root. **No union by rank or size**, so it always attaches `root_u` under `root_v`, whatever their sizes.
  * No visited set is needed. "Already connected" is just `find(u) == find(v)`.
* **Invariant:** after each successful `union`, two nodes have the same root **exactly when** the edges processed so far connect them. So the processed edges always form a forest (no cycle) until the answer edge.
* **Edge cases:**
  * The smallest input, a triangle (`n = 3`), gives its last edge `[2, 3]` (LC Example 1).
  * The extra edge is the very last one: it's found at the end.
  * The extra edge appears early in the input: it's still found correctly. The cycle closes on whichever cycle edge comes **last** in the input, which may not be the edge that was "added".
  * `return []` is never reached on valid LC input (there's always exactly one extra edge).
  * **Recursion depth, a real local problem:** with no union by rank or size, the edges `[1,2], [2,3], …, [999,1000]` build the parent chain `1 → 2 → … → 1000`. The final edge `[1, 1000]` calls `find(1)`, which recurses 999 levels deep. At n = 1000 (the LC maximum), that raises `RecursionError` under Python's default limit when you run it locally (tested). LeetCode raises its limit, so it passes there. Fixes: **union by rank or size** (keeps every tree about log n deep), or an **iterative** `find`.

## 3. Code

```python
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:

        n = len(edges)
        parent = [i for i in range(n+1)]

        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(u,v):
            root_u = find(u)
            root_v = find(v)

            if root_u == root_v:
                return False
            
            parent[root_u] = root_v
            return True

        for u,v in edges:
            if not union(u,v):
                return [u,v]

        return []
```

### Alternative: DFS (are the two ends already connected?)

Keep an adjacency list of the edges added **so far**. Before adding `[u, v]`, run a DFS from `u`. If it can already reach `v`, this edge closes the cycle, so return it. Otherwise add the edge. `if u in graph and v in graph` skips the DFS when either end is brand new, because a new node can't be connected yet. The DFS is **iterative** (an explicit `stack`, marked when pushed), so unlike the recursive `find` above it has no recursion-depth problem at n = 1000.

```python
from collections import defaultdict
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        graph = defaultdict(list)

        def connected(src: int, target: int) -> bool:
            # Iterative DFS over the edges added so far: can src already reach target?
            stack = [src]
            seen = {src}
            while stack:
                node = stack.pop()
                if node == target:
                    return True
                for nei in graph[node]:
                    if nei not in seen:
                        seen.add(nei)
                        stack.append(nei)
            return False

        for u, v in edges:
            # If u and v are already connected, this edge closes a cycle
            if u in graph and v in graph and connected(u, v):
                return [u, v]
            graph[u].append(v)
            graph[v].append(u)

        return []
```

| | Main (union-find) | Alternative (DFS) |
| --- | --- | --- |
| "Already connected?" check | `find(u) == find(v)`, almost O(1) | a DFS over the edges added so far, up to O(n) |
| Total time | O(n log n) (near O(n) with rank or size) | **O(n²)** |
| Recursion risk | yes (recursive `find`, no rank) | no (iterative stack) |
| When to use | the standard answer, and fast | easy to explain, and fine for n ≤ 1000 |

## 4. Dry Run

Input (LC Example 2): `edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]`, so `n = 5`, and `parent` starts as `[0, 1, 2, 3, 4, 5]` (index 0 unused).

| Edge | `find(u)` | `find(v)` | Same root? | Action | `parent[1..5]` after |
| --- | --- | --- | --- | --- | --- |
| `[1,2]` | 1 | 2 | no | `parent[1] = 2` | `[2, 2, 3, 4, 5]` |
| `[2,3]` | 2 | 3 | no | `parent[2] = 3` | `[2, 3, 3, 4, 5]` |
| `[3,4]` | 3 | 4 | no | `parent[3] = 4` | `[2, 3, 4, 4, 5]` |
| `[1,4]` | `find(1)`: 1 → 2 → 3 → **4**. Path compression points 1, 2 and 3 straight at 4 | 4 | **yes** | return **`[1, 4]`** | `[4, 4, 4, 4, 5]` |

Nodes 1–4 were already connected through 1–2–3–4, so the edge `[1,4]` closes the cycle. Edge `[1,5]` is never looked at.

## 5. Complexity

* **Time: O(n log n)** worst case. In practice it's close to O(n).
  Think of it as: there are n edges, and each one does two `find` calls. Path compression flattens every path it walks, so a long chain is only expensive the **first** time, and later finds on the same nodes are almost instant. Without union by rank or size, the proven bound is about log n per `find` on average, which gives O(n log n). Adding union by rank or size brings it down to almost O(1) per operation, written O(α(n)), where α grows so slowly it's effectively under 5.
* **Space: O(n)**
  Think of it as: `parent` has n + 1 entries. The recursive `find` also uses stack space as deep as the longest parent chain, which can reach about n before compression flattens it. That's the recursion risk described in the edge cases.
* **DFS alternative: O(n²) time, O(n) space.** Each of the n edges may run a DFS over everything added so far (up to n nodes and edges), so the worst case is n × n. The adjacency list, `seen` and `stack` each hold at most about n entries.

## 6. Recall (30 seconds)

* Exactly one extra edge means exactly one cycle. Union edges in order, and the **first edge whose ends already share a root** is the answer, which is also the last cycle edge in the input.
* `parent[i] = i` at the start. `find` with **path compression** (`parent[i] = find(parent[i])`). `union` returns `False` when the roots match.
* O(n log n) time (near O(n) with union by rank or size) and O(n) space. Recursive `find` without rank can go n deep, so use rank/size or an iterative find.
