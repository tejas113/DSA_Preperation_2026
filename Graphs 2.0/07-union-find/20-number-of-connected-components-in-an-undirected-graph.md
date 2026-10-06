# 323. Number of Connected Components in an Undirected Graph

**LC 323 🔒** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Union-Find: start with `n` groups and subtract 1 for every successful merge

---

## 1. Intuition

Start by imagining every node as its own little island, so there are `n` groups. Each edge is a bridge. If it
joins **two different** groups, they become one, and the count drops by 1. If both ends are **already in the
same** group, the bridge adds nothing (it's part of a cycle), so the count stays the same. After all edges,
the count is the number of connected components.

* **Start at `n`:** `res = n`, because before any edge, every node is alone.
* **Subtract only on a real merge:** `if union(u, v): res -= 1`. `union` returns `True` only when `root_u != root_v`.
* **`find` gives a node's group leader:** it follows `parent` up to the root, and path compression (`parent[node] = find(parent[node])`) points every visited node straight at the root.
* **Cycles and repeated edges are free:** an edge inside one group makes `union` return `False`, so `res` doesn't change.

**Recall:** `res = n`. For each edge, if `union(u, v)` merged two different roots, `res -= 1`. Return `res`.

## 2. Approach

* **Idea:** Number of components = `n` minus the number of edges that joined two **different** groups. Union-find tells you, for each edge, whether that happened.
* **Graph representation:** **edge list**, **undirected**, unweighted. Nodes are `0 … n-1`.
* **Data structure / pointers:**
  * `parent[i]`: the next node on the way to `i`'s root. A root has `parent[i] == i`.
  * `find(node)`: **recursive**, with **path compression**.
  * `union(u, v)`: attaches `root_v` under `root_u` when they differ. **No union by rank or size.** It returns `True` on a merge and `False` if they were already in the same group.
  * `res`: the current number of separate groups.
* **Invariant:** after processing some edges, `res` equals the number of separate groups those edges form, and two nodes share a root exactly when they're connected.
* **Edge cases:**
  * No edges: no merges, so it returns `n`.
  * `n = 1`: returns `1`.
  * All nodes connected: it ends at `1`.
  * Cycles (for example `[0,1],[1,2],[2,0]`): the cycle-closing edge doesn't merge anything, so `res` isn't decreased.
  * Self-loops `[x, x]` or repeated edges (not allowed on LC, but handled): `root_u == root_v`, so nothing changes.
  * Isolated nodes (in no edge): never merged, so each one counts as its own component.
  * **Recursion depth:** with no union by rank or size, an unlucky edge order such as `[2,1], [3,2], …, [n-1,n-2], [0,1]` builds a parent chain of length about n, and the last `find(1)` recurses that deep. At n = 2000 (the LC maximum), that raises `RecursionError` under Python's default limit when you run it locally (tested). A simple path order stays shallow. Fixes: union by rank or size, or an iterative `find`.

## 3. Code

```python
class Solution:
    def countComponents(self, n: int, edges: list[list[int]]) -> int:
        parent = [i for i in range(n)]
        
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])  # Path compression
            return parent[node]
            
        def union(u, v):
            root_u = find(u)
            root_v = find(v)
            
            # If nodes are in different components, merge them
            if root_u != root_v:
                parent[root_v] = root_u
                return True  # Successfully merged
            return False     # Already in the same component

        res = n
        for u, v in edges:
            if union(u, v):
                res -= 1
                
        return res
```

### Alternative: DFS (count how many times a new search has to start)

Build an adjacency list. Go through the nodes `0 … n-1`. Every node that isn't `seen` yet starts a **new component** (`components += 1`), and a DFS from it marks the whole component as seen. This is the same idea as Number of Islands (#1), but on an edge list instead of a grid. The DFS is **iterative** (a `stack`, marked when pushed), so there's no recursion-depth risk.

```python
from collections import defaultdict
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        seen = set()
        components = 0

        for start in range(n):
            if start in seen:
                continue
            components += 1  # a new, unseen component starts here

            # Iterative DFS marks this whole component as seen
            seen.add(start)
            stack = [start]
            while stack:
                node = stack.pop()
                for nei in graph[node]:
                    if nei not in seen:
                        seen.add(nei)
                        stack.append(nei)

        return components
```

| | Main (union-find) | Alternative (DFS) |
| --- | --- | --- |
| Counting rule | start at `n`, subtract 1 per successful merge | add 1 per DFS start |
| Time | O(n + E log n) (near-linear with rank or size) | O(n + E) |
| Extra space | `parent` (n), and the edges aren't stored | adjacency list (n + E) + `seen` + `stack` |
| Works on a stream of edges? | **yes**: you can add edges one at a time and keep the count | no, it needs the whole graph first |
| Recursion risk | yes (recursive `find`, no rank) | no (iterative stack) |

## 4. Dry Run

Input (LC Example 1): `n = 5`, `edges = [[0,1],[1,2],[3,4]]`. `parent` starts as `[0, 1, 2, 3, 4]` and `res = 5`.

| Edge | `find(u)` | `find(v)` | Merge? | Action | `parent` after | `res` |
| --- | --- | --- | --- | --- | --- | --- |
| `[0,1]` | 0 | 1 | yes | `parent[1] = 0` | `[0, 0, 2, 3, 4]` | 4 |
| `[1,2]` | `find(1)` → 0 | 2 | yes | `parent[2] = 0` | `[0, 0, 0, 3, 4]` | 3 |
| `[3,4]` | 3 | 4 | yes | `parent[4] = 3` | `[0, 0, 0, 3, 3]` | **2** |

The groups are `{0, 1, 2}` (root 0) and `{3, 4}` (root 3), so it returns **2**.

## 5. Complexity

Let **E** = `len(edges)`.

* **Time: O(n + E log n)** worst case, and close to O(n + E) in practice
  Think of it as: building `parent` touches every node once, which is n. Then each edge does two `find`s. Thanks to path compression, a long path is only slow the first time, because afterwards those nodes point straight at the root. With compression but no rank, that's about log n per `find` on average. Adding union by rank or size makes each `find` almost O(1).
* **Space: O(n)**
  Think of it as: `parent` has one entry per node. The recursive `find` also uses stack space as deep as the longest parent chain, which can be about n in the unlucky edge order from the edge cases. The edges themselves are only read, never stored.
* **DFS alternative: O(n + E) time and space.** Building the adjacency list reads every edge, and the DFS visits each node once and walks each edge twice. The adjacency list itself stores every edge twice.

## 6. Recall (30 seconds)

* **Components = n − (successful merges).** Start `res = n`, and decrease it only when `union` joins two **different** roots.
* `find` with path compression, and `union` returns `True` or `False`. Cycles, repeated edges and self-loops don't change the count.
* O(n + E log n) time (near-linear with rank or size) and O(n) space. Alternative: count DFS/BFS starts, as in Number of Islands.
