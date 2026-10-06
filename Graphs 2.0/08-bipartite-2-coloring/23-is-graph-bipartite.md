# 785. Is Graph Bipartite?

**LC 785** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** BFS 2-colouring: give neighbours opposite colours, and a clash means it isn't bipartite

---

## 1. Intuition

Can you split the nodes into two teams so that every edge goes **between** the teams, never inside one?
Paint a starting node red. Its neighbours must be blue, their neighbours must be red, and so on. If you
ever find an edge whose two ends got the **same** colour, the split is impossible. That happens exactly
when the graph has an odd-length cycle, like a triangle.

* **Three colour states:** `color = [0] * n`, where `0` = not coloured yet, `1` = team A and `-1` = team B.
* **Opposite colour = negate it:** `color[neighbor] = -color[node]` flips 1 ↔ -1 in one step.
* **The clash check:** `elif color[neighbor] == color[node]: return False`. The edge joins two nodes on the same team.
* **Cover every component:** the outer loop `for i in range(n): if color[i] == 0` starts a fresh BFS (colouring `i` as `1`) in each uncoloured part. A graph can be split into pieces, and every piece must be bipartite.

**Recall:** `color` starts as 0s. For each uncoloured node, colour it 1 and BFS, giving each uncoloured neighbour `-color[node]`. If a neighbour already has the same colour, return `False`. Otherwise return `True`.

## 2. Approach

* **Idea:** Try to 2-colour each connected component with BFS. Each component has only two possible colourings (one, or its swap), so if BFS hits a clash, no colouring works.
* **Graph representation:** **adjacency list** given directly (`graph[u]` = the neighbours of `u`). **Undirected** (if `v` is in `graph[u]`, then `u` is in `graph[v]`), unweighted. `adj_list` is just a copy of `graph` in a `defaultdict`.
* **Data structure / pointers:**
  * `color[x]`: `0` means unvisited, and `±1` is its team. It doubles as the visited set. A node is coloured **when pushed**, so it's queued only once.
  * `queue` (`deque`): the BFS frontier inside the current component. It's shared across components, and it's always empty when a new start is pushed.
* **Invariant:** every coloured node has the opposite colour to the node that discovered it. So along any BFS path, the colours alternate.
* **Edge cases:**
  * An empty graph (`n = 0`): the loop doesn't run, so it returns `True`.
  * A single node, or nodes with no edges: each gets colour 1 with no clash, so it returns `True`.
  * **Disconnected** graphs: the outer loop colours every component. A clash in *any* component returns `False`.
  * An odd cycle (a triangle, or LC Example 1): the clash is detected, so it returns `False`. An even cycle (a square): `True`.
  * A self-loop `u ∈ graph[u]` (not allowed on LC, but handled): `color[u] == color[u]`, so it returns `False`, which is correct because such a graph can't be bipartite.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:

        adj_list = defaultdict(list)
        queue = deque()

        for node,neighbors in enumerate(graph):
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

## 4. Dry Run

Input (LC Example 1): `graph = [[1,2,3],[0,2],[0,1,3],[0,2]]`

```text
0 ─── 1
│ ╲   │
│   ╲ │
3 ─── 2        triangle 0-1-2 is an odd cycle, so it can't be 2-coloured
```

| Step | Pop `node` (its colour) | Neighbour checks | `color` after |
| --- | --- | --- | --- |
| Start `i = 0` | — | `color[0] = 1`, push 0 | `[1, 0, 0, 0]` |
| 1 | `0` (1) | `1` uncoloured → `-1`, push. `2` uncoloured → `-1`, push. `3` uncoloured → `-1`, push | `[1, -1, -1, -1]` |
| 2 | `1` (-1) | `0` is 1, fine. `2` is **-1 = same as node 1**, a **clash**, so `return False` | — |

It returns **`False`**. Nodes 1 and 2 are both neighbours of 0, so they both had to be team B, but they're also connected to each other.

## 5. Complexity

* **Time: O(V + E)**, where V = `len(graph)` and E = the number of edges
  Think of it as: each node is coloured and pushed once, and each node's neighbour list is walked once when it's popped. Every undirected edge is in two lists, so that's 2E checks. Copying `graph` into `adj_list` only copies V references, because the neighbour lists themselves are shared, not copied. Total: V + E.
* **Space: O(V)**
  Think of it as: `color` has V entries and `queue` holds at most V nodes. `adj_list` holds V references to the existing neighbour lists, so it doesn't copy the edges.

## 6. Recall (30 seconds)

* Bipartite ⇔ **2-colourable** ⇔ **no odd cycle**. Colour with `1` / `-1`, and `0` = unvisited.
* BFS from every uncoloured node (to cover disconnected parts). An uncoloured neighbour gets `-color[node]`. A same-coloured neighbour means `False`.
* O(V + E) time and O(V) space. DFS colouring or union-find (union each node's neighbours together, and check the node isn't in their group) work too.
