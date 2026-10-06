# 261. Graph Valid Tree

**LC 261 🔒** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Union-Find: count the edges, then check for a cycle

---

## 1. Intuition

A tree is a graph that's **connected with no cycles**. A neat fact makes this easy: with `n` nodes, a graph is
a tree **exactly when it has `n - 1` edges and no cycle**. Check the edge count first, then add the edges one
at a time with union-find. If an edge joins two nodes that are already connected, there's a cycle, so it's
not a tree.

* **The edge count rules out half the cases:** `if len(edges) != n - 1: return False`. Fewer edges means it can't be connected, and more edges means there must be a cycle.
* **Union-find spots the cycle:** `union` returns `False` when `find(u) == find(v)`. Those nodes were already connected, so this edge closes a loop.
* **Why connected comes for free:** if there are exactly `n - 1` edges and **every** union succeeded, each edge merged two separate groups. Starting from `n` groups, `n - 1` merges leave exactly **1** group, so the graph is connected.
* **`find` uses path compression:** `parent[node] = find(parent[node])` points every node it passes straight at the root.

**Recall:** If `len(edges) != n - 1`, return `False`. Union every edge, and if any edge's ends already share a root, return `False`. Otherwise return `True`.

## 2. Approach

* **Idea:** Tree ⇔ exactly `n - 1` edges **and** no cycle. Union-find checks for a cycle while it adds the edges.
* **Graph representation:** **edge list**, **undirected**, unweighted. Nodes are `0 … n-1`.
* **Data structure / pointers:**
  * `parent[i]`: the node `i` points to on the way to its root. A root has `parent[i] == i`.
  * `find(node)`: **recursive**, with **path compression**.
  * `union(u, v)`: attaches `root_v` under `root_u`. **No union by rank or size.** It returns `False` if they already share a root (a cycle).
* **Invariant:** after `k` successful unions, the processed edges form a forest with `n - k` separate groups, and two nodes share a root exactly when those edges connect them.
* **Edge cases:**
  * `n = 1, edges = []`: `0 == 1 - 1`, the loop doesn't run, so it returns `True` (a single node is a tree).
  * Too few edges, for example `n = 4` with 2 edges: it can't be connected, so it returns `False` from the count check.
  * Too many edges (LC Example 2): returns `False` from the count check, before any union.
  * Exactly `n - 1` edges but with a cycle (so some part is disconnected): `union` catches the cycle and returns `False`.
  * A self-loop `[x, x]` or a repeated edge (not allowed on LC, but handled): `find(u) == find(v)`, so it returns `False`.
  * **Recursion depth:** with no union by rank or size, an unlucky edge order such as `[2,1], [3,2], …, [n-1,n-2]` builds the parent chain `1 → 2 → … → n-1`. Then `[0,1]` calls `find(1)`, which recurses n − 2 levels. At n = 2000 (the LC maximum), that raises `RecursionError` under Python's default limit when you run it locally (tested). Many orders, like a simple path `[0,1],[1,2],…`, stay shallow. Fixes: union by rank or size, or an iterative `find`.

## 3. Code

```python
class Solution:
    def validTree(self, n: int, edges: list[list[int]]) -> bool:
        # A valid tree with n nodes MUST have exactly n - 1 edges
        if len(edges) != n - 1:
            return False
            
        parent = [i for i in range(n)]
        
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])  # Path compression
            return parent[node]
            
        def union(u, v):
            root_u = find(u)
            root_v = find(v)
            
            # If both nodes share the same root, a cycle is formed
            if root_u == root_v:
                return False
                
            # Simple union without rank
            parent[root_v] = root_u
            return True

        for u, v in edges:
            if not union(u, v):
                return False  # Cycle detected
                
        return True
```

### Alternative: DFS (count the edges, then check that everything is reachable)

The same "exactly `n - 1` edges" check comes first. Then, instead of looking for a cycle, check **connected**: build an adjacency list and run one DFS from node `0`. With exactly `n - 1` edges, "every node is reachable" is enough to prove it's a tree. A graph that's connected with `n - 1` edges can't have a cycle. The DFS is **iterative** (a `stack`, marked when pushed), so there's no recursion-depth risk.

```python
from collections import defaultdict
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # A valid tree with n nodes MUST have exactly n - 1 edges
        if len(edges) != n - 1:
            return False

        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        # Iterative DFS from node 0: with n - 1 edges, reaching all n nodes means it's a tree
        seen = {0}
        stack = [0]
        while stack:
            node = stack.pop()
            for nei in graph[node]:
                if nei not in seen:
                    seen.add(nei)
                    stack.append(nei)

        return len(seen) == n
```

| | Main (union-find) | Alternative (DFS) |
| --- | --- | --- |
| After the `n - 1` check, it proves… | **no cycle** (every union succeeds) | **connected** (DFS reaches all `n` nodes) |
| Time | O(n log n) (near O(n) with rank or size) | O(n) |
| Extra space | `parent` (n) | adjacency list + `seen` + `stack` (n) |
| Recursion risk | yes (recursive `find`, no rank) | no (iterative stack) |

## 4. Dry Run

Input (LC Example 1): `n = 5`, `edges = [[0,1],[0,2],[0,3],[1,4]]`

The count check: `len(edges) = 4 = n - 1`, so continue. `parent` starts as `[0, 1, 2, 3, 4]`.

| Edge | `find(u)` | `find(v)` | Same root? | Action | `parent` after |
| --- | --- | --- | --- | --- | --- |
| `[0,1]` | 0 | 1 | no | `parent[1] = 0` | `[0, 0, 2, 3, 4]` |
| `[0,2]` | 0 | 2 | no | `parent[2] = 0` | `[0, 0, 0, 3, 4]` |
| `[0,3]` | 0 | 3 | no | `parent[3] = 0` | `[0, 0, 0, 0, 4]` |
| `[1,4]` | `find(1)` → 0 | 4 | no | `parent[4] = 0` | `[0, 0, 0, 0, 0]` |

All 4 unions succeeded, and 5 groups minus 4 merges leaves 1 group, so it returns **`True`**.

## 5. Complexity

Let **E** = `len(edges)`. After the count check, E = n − 1.

* **Time: O(n log n)** worst case, and close to O(n) in practice
  Think of it as: the count check is instant. Then each of the `n - 1` edges does two `find`s. Path compression means a long path is only slow the first time it's walked, and after that those nodes point straight at the root. With compression but no rank, that works out to about log n per `find` on average. Adding union by rank or size brings it to almost O(1) per call.
* **Space: O(n)**
  Think of it as: `parent` has n entries. The recursive `find` also uses stack space as deep as the longest parent chain, which can be up to about n in the unlucky order described in the edge cases.
* **DFS alternative: O(n) time and space.** After the count check there are exactly `n - 1` edges, so building the adjacency list and one DFS that visits each node once and each edge twice is all linear.

## 6. Recall (30 seconds)

* Tree ⇔ **exactly `n - 1` edges and no cycle**. Check the count first, then union-find for a cycle.
* If a union finds `find(u) == find(v)`, that's a cycle, so `False`. If all `n - 1` unions succeed, there's 1 group, so it's connected.
* O(n log n) with path compression only (near O(n) with rank or size), and O(n) space. Recursive `find` without rank can go n deep, so use rank/size or an iterative find.
