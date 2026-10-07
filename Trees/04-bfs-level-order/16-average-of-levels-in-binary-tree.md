# 637. Average of Levels in Binary Tree

**Category:** NC150 | **Difficulty:** Easy | **Pattern:** Breadth-First Search (BFS) / Level Aggregation

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, return the average value of the nodes on each level in the form of an array `List[float]`.
* **Constraint:** Answers within $10^{-5}$ of the actual answer are accepted.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> This problem builds directly on **Binary Tree Level Order Traversal (LC 102)** using **BFS with a Queue**:
> 1. Freeze the number of nodes at the current level using `level_size = len(queue)`.
> 2. Maintain a running sum variable `level_sum` for the current level.
> 3. Iterate through `level_size` nodes, popping each node from the queue, adding its value to `level_sum`, and pushing its children into the queue.
> 4. After completing the loop for that level, divide `level_sum` by `level_size` and append the float result to `ans`.
> 
> 

#### Visualizing Level Aggregation

```text
Tree:                   Level Processing:                      Average Calculation:
        (3)            Level 0: sum = 3, size = 1              -> 3 / 1 = 3.0
       /   \
     (9)   (20)        Level 1: sum = 9 + 20 = 29, size = 2    -> 29 / 2 = 14.5
           /  \
         (15)  (7)     Level 2: sum = 15 + 7 = 22, size = 2    -> 22 / 2 = 11.0

=======================================================================================
Result = [3.0, 14.5, 11.0]
=======================================================================================

```

---

### 3. Code & Line-by-Line Explanation

```python
from collections import deque
from typing import Optional, List

class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        # Edge Case: If tree is empty, return empty list
        if not root:
            return []

        # Step 1: Initialize queue with root and container for averages
        queue = deque([root])
        ans = []

        # Step 2: Process tree level by level
        while queue:
            level_size = len(queue)
            level_sum = 0

            # Process all nodes belonging strictly to current depth
            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val

                # Enqueue children for the next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Calculate and store average for this level
            ans.append(level_sum / level_size)

        return ans

```

* **Line 7–8:** Handles null root case.
* **Line 11:** `queue = deque([root])` initializes double-ended queue for fast $\mathcal{O}(1)$ pops from the left.
* **Line 16–17:** `level_size = len(queue)` snapshots level size; `level_sum = 0` resets the accumulator for the current layer.
* **Line 20–21:** Dequeues node and adds `node.val` to `level_sum`.
* **Line 29:** Computes float average `level_sum / level_size` and appends it to `ans`.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 1**: `root = [3, 9, 20, null, null, 15, 7]`

* **Init:** `queue = [3]`, `ans = []`
* **Level 0:**
* `level_size = 1`, `level_sum = 0`
* Pop `3`: `level_sum = 3`. Enqueue `9` and `20`.
* `queue = [9, 20]`
* Append `3 / 1 = 3.0` $\rightarrow$ `ans = [3.0]`


* **Level 1:**
* `level_size = 2`, `level_sum = 0`
* Pop `9`: `level_sum = 9`.
* Pop `20`: `level_sum = 9 + 20 = 29`. Enqueue `15` and `7`.
* `queue = [15, 7]`
* Append `29 / 2 = 14.5` $\rightarrow$ `ans = [3.0, 14.5]`


* **Level 2:**
* `level_size = 2`, `level_sum = 0`
* Pop `15`: `level_sum = 15`.
* Pop `7`: `level_sum = 15 + 7 = 22`.
* `queue = []`
* Append `22 / 2 = 11.0` $\rightarrow$ `ans = [3.0, 14.5, 11.0]`


* **Finish:** Queue is empty $\rightarrow$ Returns `[3.0, 14.5, 11.0]`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Each of the $N$ nodes is enqueued, dequeued, and processed exactly once.
* **Space Complexity:** $\mathcal{O}(W)$ — Max queue size equals tree width $W$ ($\mathcal{O}(N)$ worst-case for a fully balanced binary tree at the leaf level).

---

### 6. Quick Revision Summary (30-Second Recall)

* **BFS Pattern:** Standard level order traversal with `deque`.
* **Aggregation:** Accumulate `level_sum += node.val` across `range(level_size)` and push `level_sum / level_size`.

---
