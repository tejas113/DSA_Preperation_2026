# 173. Binary Search Tree Iterator

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Controlled Iterative Inorder Traversal (Controlled Stack)

---

### 1. Core Intuition & Design Concept

Instead of flattening the entire tree into an array in `__init__` (which would take $\mathcal{O}(N)$ space), we simulate the standard iterative inorder traversal lazily:

1. **Stack Representation:** The stack maintains the path to the smallest unvisited node at the top.
2. **`__init__`:** Push the root and all its left descendants onto the stack.
3. **`next()`:** Pop the top node (the current smallest element). Before returning its value, push all left descendants of its **right child** to prepare for the subsequent element in sorted order.
4. **`hasNext()`:** Returns `True` if the stack is non-empty (`len(self.stack) > 0`).

---

### 2. Follow-Up Complexity Justification

#### Memory: $\mathcal{O}(H)$

At any point, the stack contains only nodes along a single path from the root down to a leaf. Therefore, the maximum number of nodes stored simultaneously in `self.stack` is bounded by the height of the tree $H$.

#### Time: Amortized $\mathcal{O}(1)$ for `next()`

Although a single call to `next()` can take up to $\mathcal{O}(H)$ time (when traversing down a right child's left spine), every node in the BST is pushed onto the stack **exactly once** and popped **exactly once** over all $N$ calls to `next()`.

* **Total push/pop operations across $N$ elements:** $2N$
* **Average work per `next()` call:** $\frac{2N}{N} = \mathcal{O}(1)$ amortized time.

---

### 3. Complete Python Code

```python
from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class BSTIterator:

    def __init__(self, root: Optional[TreeNode]):
        self.stack = []
        
        # Step 1: Initialize stack with the leftmost spine (root down to smallest node)
        cur = root
        while cur:
            self.stack.append(cur)
            cur = cur.left

    def next(self) -> int:
        # Step 2: Pop the top node (current smallest element)
        node = self.stack.pop()
        
        # Step 3: If a right child exists, push its leftmost spine onto the stack
        cur = node.right
        while cur:
            self.stack.append(cur)
            cur = cur.left
            
        return node.val

    def hasNext(self) -> bool:
        # Step 4: Returns True if there are remaining elements in the stack
        return len(self.stack) > 0


# Your BSTIterator object will be instantiated and called as such:
# obj = BSTIterator(root)
# param_1 = obj.next()
# param_2 = obj.hasNext()
```

---

### 4. Step-by-Step Dry Run

Tracing **Example 1**: `root = [7, 3, 15, null, null, 9, 20]`

```text
        7
       / \
      3   15
         /  \
        9    20

```

| Operation | Action Taken | `stack` (bottom $\rightarrow$ top) | Output |
| --- | --- | --- | --- |
| `__init__` | Push left spine of root `7` | `[7, 3]` | `None` |
| `next()` | Pop `3`. Right child is `None`. | `[7]` | `3` |
| `next()` | Pop `7`. Right child `15` exists $\rightarrow$ push left spine of `15`. | `[15, 9]` | `7` |
| `hasNext()` | Stack is non-empty. | `[15, 9]` | `True` |
| `next()` | Pop `9`. Right child is `None`. | `[15]` | `9` |
| `hasNext()` | Stack is non-empty. | `[15]` | `True` |
| `next()` | Pop `15`. Right child `20` exists $\rightarrow$ push left spine of `20`. | `[20]` | `15` |
| `hasNext()` | Stack is non-empty. | `[20]` | `True` |
| `next()` | Pop `20`. Right child is `None`. | `[]` | `20` |
| `hasNext()` | Stack is empty. | `[]` | `False` |

---

### 5. Complexity Summary

| Metric | naive Array Flattening | Controlled Stack (Optimized) |
| --- | --- | --- |
| **Constructor Time** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ |
| **`next()` Time** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ amortized |
| **`hasNext()` Time** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Space Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ |

---

### 6. Quick Revision Summary (30-Second Recall)

* **Strategy:** Lazy Inorder Traversal using an explicit stack.
* **Init:** Push all left descendants starting from the root.
* **Next:** Pop node $\rightarrow$ process right child by pushing all its left descendants $\rightarrow$ return popped node value.
* **Space:** $\mathcal{O}(H)$ stack limit.
* **Time:** $\mathcal{O}(1)$ amortized because every node is pushed/popped at most once.

---
