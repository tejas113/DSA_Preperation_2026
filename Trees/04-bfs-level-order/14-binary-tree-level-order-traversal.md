# 102. Binary Tree Level Order Traversal

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Breadth-First Search (BFS) / Level Snapshot

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, return the level-order traversal of its nodes' values (i.e., grouped level by level, from left to right).
* **Goal:** Return a 2D list `List[List[int]]` where each inner list contains all node values at that specific depth.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> BFS uses a **Queue (FIFO)** structure to process nodes horizontally across tree levels.
> To isolate levels into distinct sublists, capture the queue length **at the start of each iteration**:
> 1. `level_size = len(queue)` locks in how many nodes belong to the *current* level.
> 2. Process exactly `level_size` nodes in a loop (`for _ in range(level_size)`), popping nodes off the left and appending their non-null children to the right.
> 3. Append the inner level list to the final output list before starting the next depth layer.
> 
> 

#### Visualizing Level Snapshots

```text
Tree:                   Queue Snapshot at loop start:
        (3)            Level 0: [3]          -> Process 1 node  -> Output: [[3]]
       /   \
     (9)   (20)        Level 1: [9, 20]      -> Process 2 nodes -> Output: [[3], [9, 20]]
           /  \
         (15)  (7)     Level 2: [15, 7]      -> Process 2 nodes -> Output: [[3], [9, 20], [15, 7]]

```

---

### 3. Code & Line-by-Line Explanation

```python
from collections import deque
from typing import Optional, List

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # Edge Case: Return empty list if tree is empty
        if not root:
            return []

        # Step 1: Initialize double-ended queue with root node
        queue = deque([root])
        result = []

        # Step 2: Process levels sequentially while queue is non-empty
        while queue:
            level_vals = []
            
            # Key Trick: Freeze current level size to process only nodes of this layer
            for _ in range(len(queue)):
                node = queue.popleft()
                level_vals.append(node.val)

                # Push children into queue for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Store completed level snapshot
            result.append(level_vals)

        return result

```

* **Line 7–8:** Handles empty tree guard clause cleanly upfront.
* **Line 11:** `deque([root])` initializes double-ended queue with $\mathcal{O}(1)$ pops from the left.
* **Line 19:** `for _ in range(len(queue))` snapshot evaluates `len(queue)` once per outer loop iteration. Nodes added inside the `for` loop do not alter the loop bound.
* **Line 20:** `queue.popleft()` ensures FIFO (First-In-First-Out) execution ordering.
* **Line 24–27:** Appends existing left and right child references for the next depth tier.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 1**: `root = [3, 9, 20, null, null, 15, 7]`

* **Init:** `queue = [3]`, `result = []`
* **Outer Iteration 1:**
* `len(queue) = 1`
* Pop `3`, `level_vals = [3]`. Append left (`9`) and right (`20`).
* `queue = [9, 20]`, `result = [[3]]`


* **Outer Iteration 2:**
* `len(queue) = 2`
* Pop `9`, `level_vals = [9]`. (No children).
* Pop `20`, `level_vals = [9, 20]`. Append left (`15`) and right (`7`).
* `queue = [15, 7]`, `result = [[3], [9, 20]]`


* **Outer Iteration 3:**
* `len(queue) = 2`
* Pop `15`, `level_vals = [15]`.
* Pop `7`, `level_vals = [15, 7]`.
* `queue = []`, `result = [[3], [9, 20], [15, 7]]`


* **Finish:** `queue` is empty $\rightarrow$ Returns `[[3], [9, 20], [15, 7]]`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is enqueued and dequeued exactly once.
* **Space Complexity:** $\mathcal{O}(W)$ — Max queue size equals tree width $W$. For a balanced binary tree, max width at leaf level is $\mathcal{O}(N/2) = \mathcal{O}(N)$.

---

### 6. Quick Revision Summary (30-Second Recall)

* **Data Structure:** Use `collections.deque` for efficient $\mathcal{O}(1)$ `popleft()`.
* **Level Isolation:** Snapshot `range(len(queue))` before popping inside the inner loop.

---
