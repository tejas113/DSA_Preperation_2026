# 116 / 117. Populating Next Right Pointers in Each Node

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Breadth-First Search (BFS) / Level Link Pointers

---

### 1. The Problem Statement

* **Question:** Given a binary tree, populate each `next` pointer to point to its next right node. If there is no next right node, the `next` pointer should be set to `NULL`.
* **Initial State:** All `next` pointers are initialized to `NULL`.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> While processing level nodes via BFS:
> 1. Nodes are dequeued from left to right.
> 2. For any node at index `i` (where $i < \text{level\_size} - 1$), the node directly to its right **is currently sitting at `queue[0]**`.
> 3. The last node of the level ($i = \text{level\_size} - 1$) has no right neighbor, so its `next` pointer points to `None`.
> 
> 

#### Visualizing Next Right Pointers

```text
Tree Level Order:                 Pointer Connections:

       (1)                        Level 0: [1]
      /   \                       1.next -> None
    (2)   (3)                     
   /  \   /  \                    Level 1: [2, 3]
 (4)  (5)(6) (7)                  2.next -> queue[0] (which is 3)
                                  3.next -> None

=======================================================================================
Resulting Structure: 1 -> None | 2 -> 3 -> None | 4 -> 5 -> 6 -> 7 -> None
=======================================================================================

```

---

### 3. Code & Line-by-Line Explanation

#### Approach A: Standard BFS using Queue (Your Code)

```python
from collections import deque
from typing import Optional

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        if not root:
            return None

        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                # If not the last node in current level, point to front of queue
                if i < level_size - 1:
                    node.next = queue[0]
                else:
                    node.next = None

                # Enqueue children for the next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return root

```

#### Approach B: $\mathcal{O}(1)$ Space Pointer Traversal (For Perfect Binary Trees - LC 116)

```python
class Solution:
    def connect(self, root: 'Node') -> 'Node':
        if not root:
            return None

        leftmost = root

        # Traverse level by level using already established next pointers
        while leftmost.left:
            head = leftmost
            while head:
                # Connection 1: Connect left child -> right child
                head.left.next = head.right

                # Connection 2: Connect right child -> next sub-tree's left child
                if head.next:
                    head.right.next = head.next.left

                head = head.next

            leftmost = leftmost.left

        return root

```

* **Approach A, Line 17–18:** `queue[0]` peeks at the front of the deque without removing it, giving the exact adjacent right sibling.
* **Approach B:** Uses previously established `next` pointers to walk horizontally without allocating extra memory for a queue.

---

### 4. Step-by-Step Dry Run

Let's trace **Example Tree**: `root = [1, 2, 3, 4, 5, 6, 7]`

* **Init:** `queue = [1]`
* **Level 0:**
* `level_size = 1`
* `i = 0`: Pop `1`. Since `i == level_size - 1`, `1.next = None`.
* Enqueue `2` and `3`. `queue = [2, 3]`


* **Level 1:**
* `level_size = 2`
* `i = 0`: Pop `2`. Since `0 < 1`, `2.next = queue[0]` $\rightarrow$ `2.next = 3`.
* Enqueue `4` and `5`. `queue = [3, 4, 5]`
* `i = 1`: Pop `3`. Since `i == level_size - 1`, `3.next = None`.
* Enqueue `6` and `7`. `queue = [4, 5, 6, 7]`


* **Level 2:**
* `level_size = 4`
* `4.next = 5`, `5.next = 6`, `6.next = 7`, `7.next = None`.


* **Finish:** Returns modified `root`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is enqueued, dequeued, and linked exactly once.
* **Space Complexity:**
* **Approach A (Queue):** $\mathcal{O}(W)$ space where $W$ is the maximum width of the tree ($\mathcal{O}(N)$ at leaf level).
* **Approach B (Pointer Iteration):** $\mathcal{O}(1)$ auxiliary space.



---

### 6. Quick Revision Summary (30-Second Recall)

* **BFS Level Check:** Link `node.next = queue[0]` for all indices `i < level_size - 1`.
* **Edge Node:** Set `node.next = None` for the final element in each level iteration (`i == level_size - 1`).

---
