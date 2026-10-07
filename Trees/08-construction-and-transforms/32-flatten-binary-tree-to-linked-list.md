# 114. Flatten Binary Tree to Linked List

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Medium | **Pattern:** Morris Traversal Pointer Manipulation / Reversed Pre-Order DFS

---

### 1. The Core Logic

The goal is to re-wire nodes in-place to form a linked list matching **Pre-Order Traversal** (`Root -> Left -> Right`).

#### Morris Traversal Approach ($\mathcal{O}(1)$ Space):

For any node `curr` with a non-empty left subtree:

1. Find the **rightmost node in the left subtree** (`prev`). This node will be the last node visited in the left subtree under Pre-Order.
2. Connect `prev.right` to `curr.right` (attaching the original right subtree after the end of the left subtree).
3. Move `curr.left` over to `curr.right`.
4. Clear `curr.left = None`.
5. Advance `curr = curr.right`.

```text
       curr                           curr
        /  \                           \
      left  right  =========>          left
       \                                 \
       prev                             prev
                                           \
                                          right

```

---

### 2. Code Implementations

#### Approach A: Morris Traversal (Your Solution — $\mathcal{O}(1)$ Space)

```python
from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        curr = root

        while curr:
            if curr.left:
                # Find the rightmost node of the left subtree
                prev = curr.left
                while prev.right:
                    prev = prev.right

                # Attach original right subtree to the rightmost node
                prev.right = curr.right

                # Move left subtree to right, then erase left pointer
                curr.right = curr.left
                curr.left = None

            # Move to the next node in the flattened chain
            curr = curr.right

```

#### Approach B: Reverse Pre-Order DFS ($\mathcal{O}(H)$ Stack Space)

Process nodes in reverse Pre-Order (`Right -> Left -> Root`) while keeping track of the previously visited node.

```python
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        prev = None

        def helper(node: Optional[TreeNode]):
            nonlocal prev
            if not node:
                return

            # Traversal order: Right -> Left -> Root
            helper(node.right)
            helper(node.left)

            # Rewire pointers
            node.right = prev
            node.left = None
            prev = node

        helper(root)

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**: `root = [1, 2, 5, 3, 4, null, 6]`

```text
        1
       / \
      2   5
     / \   \
    3   4   6

```

1. **`curr = Node 1`:**
* Has left subtree (`2`).
* Rightmost node of left subtree is `4`.
* Wire `4.right = 5`.
* Set `1.right = 2`, `1.left = None`.
* Tree shape: `1 -> 2 -> (3, 4 -> 5 -> 6)`.
* Move `curr = 2`.


2. **`curr = Node 2`:**
* Has left subtree (`3`).
* Rightmost node of left subtree is `3`.
* Wire `3.right = 4`.
* Set `2.right = 3`, `2.left = None`.
* Move `curr = 3`.


3. **`curr = Node 3, 4, 5, 6`:**
* None of these have left children; loop simply advances `curr = curr.right`.



**Final Linked List:** `1 -> 2 -> 3 -> 4 -> 5 -> 6`.

---

### 4. Complexity Analysis

| Metric | Morris Traversal (Your Solution) | Reverse Pre-Order DFS |
| --- | --- | --- |
| **Time Complexity** | $\mathcal{O}(N)$ (each edge is visited at most twice) | $\mathcal{O}(N)$ |
| **Space Complexity** | $\mathcal{O}(1)$ auxiliary space | $\mathcal{O}(H)$ call stack depth |

---

### 5. Quick Revision Summary (30-Second Recall)

* **Goal:** Turn tree into a single right-skewed linked list in **Pre-Order** sequence (`Root -> Left -> Right`).
* **Morris Key Steps:**
1. Find rightmost node of `curr.left`.
2. Connect `prev.right = curr.right`.
3. Move `curr.left` to `curr.right` and set `curr.left = None`.
4. Move `curr = curr.right`.



---
