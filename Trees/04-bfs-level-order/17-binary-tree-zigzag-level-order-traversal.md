# 103. Binary Tree Zigzag Level Order Traversal

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Breadth-First Search (BFS) / Level Direction Alternation

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, return the zigzag level order traversal of its nodes' values.
* **Traversal Rule:** Alternate the direction of node values at each level:
* Even levels ($0, 2, 4, \dots$): Left to Right
* Odd levels ($1, 3, 5, \dots$): Right to Left



---

### 2. The Approach & Strategy

> **Crucial Insight:**
> This problem adapts **Binary Tree Level Order Traversal (LC 102)** with a simple direction toggle:
> 1. Use standard **BFS with a Queue** to process nodes level by level from left to right.
> 2. Maintain a `level` counter (or a boolean flag `left_to_right`).
> 3. Process all nodes for the current level in a loop.
> 4. Once the level list `lis` is completely built, check if it's an odd level (`level % 2 == 1`). If so, reverse `lis` (or insert elements in reverse using `deque`/pre-allocated arrays) before appending it to `ans`.
> 
> 

#### Visualizing Zigzag Direction Switching

```text
Tree:                          Level Processing:             Direction Rule:          Final Result:
        (3)            Level 0: [3]                   Left-to-Right (Even)     -> [3]
       /   \
     (9)   (20)        Level 1: [9, 20] -> reverse   Right-to-Left (Odd)      -> [20, 9]
           /  \
         (15)  (7)     Level 2: [15, 7]               Left-to-Right (Even)     -> [15, 7]

===================================================================================================
Zigzag Output = [[3], [20, 9], [15, 7]]
===================================================================================================

```

---

### 3. Code & Line-by-Line Explanation

#### Approach A: List Reversal (Fixed Version of Your Code)

```python
from collections import deque
from typing import Optional, List

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        queue = deque([root])
        level = 0
        ans = []

        while queue:
            lis = []
            level_length = len(queue)

            # Collect nodes for the current level (always left to right in queue)
            for _ in range(level_length):
                node = queue.popleft()
                lis.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Fix: Place directional reversal OUTSIDE the inner for-loop!
            if level % 2 == 1:
                lis = lis[::-1]

            ans.append(lis)
            level += 1

        return ans

```

#### Approach B: Double-Ended Level Builder (Avoids Reversing Arrays)

```python
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        queue = deque([root])
        ans = []
        left_to_right = True

        while queue:
            level_length = len(queue)
            level_nodes = deque()

            for _ in range(level_length):
                node = queue.popleft()

                # Insert at end for Left-to-Right, or at front for Right-to-Left
                if left_to_right:
                    level_nodes.append(node.val)
                else:
                    level_nodes.appendleft(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            ans.append(list(level_nodes))
            left_to_right = not left_to_right  # Toggle direction flag

        return ans

```

* **Approach A, Line 27–28:** `if level % 2 == 1: lis = lis[::-1]` handles level-wide reversal after all children are safely added to the queue in standard left-to-right order.
* **Approach B, Line 17–20:** Avoids reversing an entire array by using `level_nodes.appendleft()` for odd levels, populating the level list in reverse on-the-fly in $\mathcal{O}(1)$ time per element.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 1**: `root = [3, 9, 20, null, null, 15, 7]`

* **Init:** `queue = [3]`, `level = 0`, `ans = []`
* **Level 0 (Even):**
* `level_length = 1`
* Pop `3`: `lis = [3]`. Enqueue `9` and `20`.
* `level % 2 == 0` $\rightarrow$ Keep `lis = [3]`.
* `ans = [[3]]`, `level = 1`.


* **Level 1 (Odd):**
* `level_length = 2`
* Pop `9`: `lis = [9]`.
* Pop `20`: `lis = [9, 20]`. Enqueue `15` and `7`.
* `level % 2 == 1` $\rightarrow$ Reverse: `lis = [20, 9]`.
* `ans = [[3], [20, 9]]`, `level = 2`.


* **Level 2 (Even):**
* `level_length = 2`
* Pop `15`: `lis = [15]`.
* Pop `7`: `lis = [15, 7]`.
* `level % 2 == 0` $\rightarrow$ Keep `lis = [15, 7]`.
* `ans = [[3], [20, 9], [15, 7]]`, `level = 3`.


* **Finish:** Queue is empty $\rightarrow$ Returns `[[3], [20, 9], [15, 7]]`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited once. Reversing a level list of size $K$ takes $\mathcal{O}(K)$, summing to $\mathcal{O}(N)$ across all levels.
* **Space Complexity:** $\mathcal{O}(W)$ — Max queue size equals tree width $W$ ($\mathcal{O}(N)$ worst-case for balanced trees at the leaf layer).

---

### 6. Quick Revision Summary (30-Second Recall)

* **Standard BFS:** Process tree nodes level by level using a queue.
* **Direction Swap:** Reverse the collected level list `lis[::-1]` (or use `deque.appendleft`) after the inner `for` loop completes when `level % 2 == 1`.

---
