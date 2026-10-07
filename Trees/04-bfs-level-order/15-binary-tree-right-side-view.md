# 199. Binary Tree Right Side View

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Breadth-First Search (BFS) / Level Last Element

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, imagine yourself standing on the right side of it. Return the values of the nodes you can see, ordered from top to bottom.
* **Goal:** Return a list `List[int]` containing the rightmost visible node value at each depth level.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> This problem directly adapts **Problem 13: Binary Tree Level Order Traversal (LC 102)**:
> 1. Use **BFS with a Queue** to traverse the tree level by level.
> 2. At each level, capture `level_size = len(queue)`.
> 3. As you process nodes from left to right within that level (`i` from `0` to `level_size - 1`), the **last node processed** (`i == level_size - 1`) will be the rightmost node visible from that level.
> 
> 

#### Visualizing Rightmost Selection

```text
Tree:                          Level Snapshot (BFS):            Right Visible Element:
          (1)                  Level 0: [1]                     -> 1
        /     \
      (2)     (3)              Level 1: [2, 3]                  -> 3
     /   \       \
   (4)   (5)     (4)           Level 2: [4, 5, 4]               -> 4
  /
(5)                            Level 3: [5]                     -> 5

=======================================================================================
Right Side View Result = [1, 3, 4, 5]
=======================================================================================

```

---

### 3. Code & Line-by-Line Explanation

#### Approach A: BFS Level Order Traversal (Your Solution)

```python
from collections import deque
from typing import Optional, List

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        queue = deque([root])
        right_side_view = []

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                # Pick the last element processed in current level snapshot
                if i == level_size - 1:
                    right_side_view.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return right_side_view

```

#### Approach B: Optimized DFS (Right-to-Left Traversal)

```python
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        right_side_view = []

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return

            # If visiting this depth for the first time, record node
            if depth == len(right_side_view):
                right_side_view.append(node.val)

            # Traverse RIGHT child first so right side elements are recorded first
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return right_side_view

```

* **Approach A, Line 16:** `if i == level_size - 1:` checks if the node currently dequeued is the final element of the current level layer.
* **Approach B, Line 11:** `if depth == len(right_side_view):` ensures only the first node visited at any depth gets added to the result. By prioritizing `dfs(node.right)` before `dfs(node.left)`, the rightmost node is guaranteed to hit each depth level first.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 2**: `root = [1, 2, 3, 4, null, null, null, 5]`

* **Level 0:** `queue = [1]`, `level_size = 1`.
* `i = 0` (`level_size - 1 = 0`): Append `1`. Enqueue `2` and `3`.
* `right_side_view = [1]`.


* **Level 1:** `queue = [2, 3]`, `level_size = 2`.
* `i = 0`: Pop `2`. Enqueue `4`.
* `i = 1` (`level_size - 1 = 1`): Pop `3`. Append `3`.
* `right_side_view = [1, 3]`.


* **Level 2:** `queue = [4]`, `level_size = 1`.
* `i = 0` (`level_size - 1 = 0`): Pop `4`. Append `4`. Enqueue `5`.
* `right_side_view = [1, 3, 4]`.


* **Level 3:** `queue = [5]`, `level_size = 1`.
* `i = 0` (`level_size - 1 = 0`): Pop `5`. Append `5`.
* `right_side_view = [1, 3, 4, 5]`.



---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited once in both BFS and DFS solutions.
* **Space Complexity:**
* **BFS:** $\mathcal{O}(W)$ — Max queue size equals tree width $W$ ($\mathcal{O}(N)$ worst-case).
* **DFS:** $\mathcal{O}(H)$ — Stack depth equals tree height $H$ ($\mathcal{O}(\log N)$ balanced, $\mathcal{O}(N)$ skewed).



---

### 6. Quick Revision Summary (30-Second Recall)

* **BFS Check:** `if i == level_size - 1:` captures the last node in the current level snapshot.
* **DFS Alternative:** Recurse `right` child first, append value when `depth == len(result)`.

---
