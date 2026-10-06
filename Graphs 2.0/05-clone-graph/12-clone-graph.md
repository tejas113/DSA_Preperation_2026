# 133. Clone Graph

**LC 133** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Graph traversal + hash map (`old node → its clone`)

---

## 1. Intuition

Copying a graph is like copying a group of friends' phone contacts. For each person you make a new card,
but their "friends" entries must point to the *new* cards, not the old ones. The graph can have cycles, so
you need a notebook that says "I already made a card for this person, here it is." That notebook is a hash map.

* **`old_to_new` is the notebook and the visited set:** `if curr_node in old_to_new: return old_to_new[curr_node]` means each original node is cloned only once, and any later visit gets the same clone back.
* **Register *before* recursing:** `old_to_new[curr_node] = copy` runs **before** the `for neighbor` loop. When a cycle leads back to `curr_node`, the lookup finds `copy` instead of recursing forever.
* **Neighbours are wired with clones:** `copy.neighbors.append(dfs(neighbor))`. `dfs` always returns a *cloned* node, so the new graph never points back into the old one.
* **The returned clone is the entry point:** `return dfs(node)` gives the clone of the given node, and the rest of the copy is reachable from it.

**Recall:** DFS with `old_to_new`. If the node was seen, return its clone. Otherwise create the clone, store it, then append `dfs(neighbor)` for each neighbour.

## 2. Approach

* **Idea:** DFS over the original graph. The first time you meet a node, create its clone and save it in the map *before* visiting its neighbours. Each neighbour slot is filled with that neighbour's clone, which is new or looked up.
* **Graph representation:** **adjacency list stored in the objects.** Each `Node` has `val` and a `neighbors` list. The graph is undirected (each edge shows up in both nodes' lists) and unweighted.
* **Data structure / pointers:**
  * `old_to_new`: a dict from an **original node object** to its **clone**. It doubles as the visited set. A node is marked **when `dfs` enters it, before its neighbours are processed**. The keys are the node objects themselves (Python hashes them by identity), so two different nodes with the same `val` would still be kept apart.
  * `copy`: the clone being built for `curr_node`. Its `neighbors` list fills up as the recursive calls return.
* **Invariant:** each original node has **at most one** clone, the one in `old_to_new`. Every clone's `neighbors` list holds only clones, in the same order as the original's `neighbors`.
* **Edge cases:**
  * Empty graph (`node is None`): `if not node: return None`.
  * A single node with no neighbours (`[[]]`): the loop doesn't run, so it returns a lone `Node(1)`.
  * Cycles (for example 1–2–3–4–1): ended by the lookup, because each node is registered before its neighbours are visited.
  * Self-loop (not allowed on LC, but handled): `dfs(curr_node)` finds itself in the map, so `copy` gets itself as a neighbour.
  * Parallel edges (not allowed on LC, but handled): each one appends the same clone again, so the duplicates are kept.
  * Disconnected graph: only the part reachable from `node` is cloned. (LC guarantees the graph is connected.)
  * **Recursion depth:** `dfs` can go as deep as the longest simple path, up to V. LC allows only 100 nodes, so it's fine there. A long chain of a few thousand nodes would raise `RecursionError` under Python's default limit. A BFS version with a `deque` (clone on push) avoids that.

## 3. Code

`Node` is normally provided by LeetCode (shown in the docstring). The real class is added below it so this file runs on its own.

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional


class Node:  # runnable copy of LeetCode's definition above
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:

    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None

        # Hash map to track visited nodes and map original -> cloned
        old_to_new = {}

        def dfs(curr_node: "Node") -> "Node":
            # Base Case: If node is already cloned, return the cloned instance
            if curr_node in old_to_new:
                return old_to_new[curr_node]

            # Create clone for current node and register in map before recurring
            copy = Node(curr_node.val)
            old_to_new[curr_node] = copy

            # Deep copy all neighbors recursively
            for neighbor in curr_node.neighbors:
                copy.neighbors.append(dfs(neighbor))

            return copy

        return dfs(node)
```

## 4. Dry Run

Input (LC Example 1): `adjList = [[2,4],[1,3],[2,4],[1,3]]`

```text
1 --- 2
|     |
4 --- 3
```

| Call | `curr_node` | What happens | `old_to_new` keys after |
| --- | --- | --- | --- |
| 1 | `1` | new → create `1'`, register it, then loop over `[2, 4]` | `{1}` |
| 2 | `2` (from 1) | new → create `2'`, register it, then loop over `[1, 3]` | `{1, 2}` |
| 3 | `1` (from 2) | **already there** → return `1'` (cycle stopped), so `2'.neighbors = [1']` | `{1, 2}` |
| 4 | `3` (from 2) | new → create `3'`, register it, then loop over `[2, 4]` | `{1, 2, 3}` |
| 5 | `2` (from 3) | already there → return `2'`, so `3'.neighbors = [2']` | `{1, 2, 3}` |
| 6 | `4` (from 3) | new → create `4'`, register it, then loop over `[1, 3]`: both are already there, so `4'.neighbors = [1', 3']` | `{1, 2, 3, 4}` |
| — | back in 3 | `3'.neighbors = [2', 4']`, return `3'` | |
| — | back in 2 | `2'.neighbors = [1', 3']`, return `2'` | |
| 7 | `4` (from 1) | already there → return `4'`, so `1'.neighbors = [2', 4']` | `{1, 2, 3, 4}` |

It returns `1'`. Reading the clone back gives `[[2,4],[1,3],[2,4],[1,3]]`, with 4 new node objects.

## 5. Complexity

* **Time: O(V + E)**
  Think of it as: each node is cloned once, and each neighbour entry is looked at once. The first visit to a node does the cloning, and every later visit is a single dict lookup. Each node's loop walks its `neighbors` list once. In an undirected graph each edge shows up in two lists, so that's 2E steps. V clones plus 2E lookups grows like V + E.
* **Space: O(V)** (not counting the new graph you return)
  Think of it as: `old_to_new` holds one entry per node, and the recursion stack can be as deep as a long path through the graph, up to V calls. The cloned graph itself takes O(V + E), but that's the required output.

## 6. Recall (30 seconds)

* `old_to_new` maps each original node to its clone, and it's the visited set too.
* **Register the clone before visiting neighbours**, otherwise a cycle recurses forever. Append `dfs(neighbor)`, which always returns a clone.
* O(V + E) time and O(V) extra space. For long chains, use BFS with a `deque` to avoid the recursion limit.
