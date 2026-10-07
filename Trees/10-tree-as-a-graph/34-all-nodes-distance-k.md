# 863. All Nodes Distance K in Binary Tree

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Medium | **Pattern:** Tree to Graph Conversion + BFS

---

### 1. The Core Logic

Finding nodes at distance $K$ in a binary tree is challenging because standard tree pointers only move downwards (`left` and `right`). Distance can also radiate **upwards** through parent nodes.

To solve this:

1. **Annotate Parent Pointers (DFS/BFS):** Traverse the tree once to create a mapping from each node to its `parent`. This effectively turns the binary tree into an **undirected graph**.
2. **Radial BFS from Target:** Treat `target` as the starting vertex in the graph. Perform level-order BFS, expanding to all unvisited neighbors: `left`, `right`, and `parent`.
3. **Stop at Layer $K$:** When `current_distance == k`, the nodes currently remaining in the BFS queue are exactly distance $K$ away. Return their values.

---

### 2. Code Implementation

```python
from collections import deque
from typing import List

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        parent = {}

        # Step 1: DFS to map parent pointers
        def build_parent_map(node: TreeNode, p: TreeNode):
            if not node:
                return
            parent[node] = p
            build_parent_map(node.left, node)
            build_parent_map(node.right, node)

        build_parent_map(root, None)

        # Step 2: Radial BFS starting from target
        queue = deque([target])
        visited = {target}
        current_distance = 0

        while queue:
            # If we've reached distance K, queue contains all answers
            if current_distance == k:
                return [node.val for node in queue]

            # Process layer by layer
            for _ in range(len(queue)):
                curr = queue.popleft()
                neighbors = [curr.left, curr.right, parent[curr]]

                for neighbor in neighbors:
                    if neighbor and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            current_distance += 1

        return []

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**: `root = [3, 5, 1, 6, 2, 0, 8, null, null, 7, 4]`, `target = 5`, `k = 2`

```text
        3
       / \
     (5)  1
     / \ / \
    6  2 0  8
      / \
     7   4

```

1. **Parent Mapping:** `parent[5] = 3`, `parent[6] = 5`, `parent[2] = 5`, `parent[7] = 2`, `parent[4] = 2`, etc.
2. **Distance 0:** `queue = [5]`, `visited = {5}`.
3. **Expand Distance 0 $\rightarrow$ 1:**
* `curr = 5`. Neighbors: `left = 6`, `right = 2`, `parent = 3`.
* `queue = [6, 2, 3]`, `visited = {5, 6, 2, 3}`.
* `current_distance` becomes `1`.


4. **Expand Distance 1 $\rightarrow$ 2:**
* Pop `6`: Neighbors `None`, `None`, `5` (visited).
* Pop `2`: Neighbors `7` (added), `4` (added), `5` (visited).
* Pop `3`: Neighbors `5` (visited), `1` (added), `None`.
* `queue = [7, 4, 1]`, `visited = {5, 6, 2, 3, 7, 4, 1}`.
* `current_distance` becomes `2`.


5. **Distance Check:** `current_distance == k (2)` $\rightarrow$ Returns `[7, 4, 1]`.

---

### 4. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — We visit each node once during DFS to build the parent map and at most once during the BFS traversal.
* **Space Complexity:** $\mathcal{O}(N)$ — Required for the `parent` map, `visited` set, and `queue` storage.

---

### 5. Quick Revision Summary (30-Second Recall)

* **Key Concept:** Treat tree as an undirected graph by tracking `parent` pointers.
* **Algorithm:** DFS to populate `parent` map $\rightarrow$ BFS outward from `target`.
* **Early Stopping:** Return queue contents as soon as `current_distance == k`.

---
