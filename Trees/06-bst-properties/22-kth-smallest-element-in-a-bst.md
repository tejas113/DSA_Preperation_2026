# 230. Kth Smallest Element in a BST

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Inorder Traversal / Augmented Tree (Order Statistic Tree)

---

### 1. Core Intuition & Optimization

#### Approach 1: Iterative Inorder with Early Stopping (Best for Standard Problem)

Instead of collecting all nodes in an array, use an iterative inorder traversal with a stack. Decrement $k$ every time a node is popped. When $k = 0$, return that node's value immediately without visiting the remaining nodes.

* **Time Complexity:** $\mathcal{O}(H + k)$, where $H$ is the height of the tree.
* **Space Complexity:** $\mathcal{O}(H)$ for the stack.

---

#### Approach 2: Augmented BST / Order Statistic Tree (Follow-Up Solution)

> **Follow-Up Question:** If the BST is modified often with insertions and deletions, and $k$-th smallest queries are frequent, how do you optimize?

Maintain a `left_count` field in each node (or store subtree size `size = left_count + right_count + 1`).

```text
         5 (left_count = 3)
        / \
       3   6
      / \
     2   4
    /
   1

```

When querying the $k$-th smallest at node `curr`:

1. If $k == \text{curr.left\_count} + 1$, `curr` is the $k$-th smallest node.
2. If $k \le \text{curr.left\_count}$, search in `curr.left` for the $k$-th smallest node.
3. If $k > \text{curr.left\_count} + 1$, search in `curr.right` for the $(k - \text{curr.left\_count} - 1)$-th smallest node.

| Operation | Standard BST | Augmented BST (Order Statistic Tree) |
| --- | --- | --- |
| **Insert / Delete** | $\mathcal{O}(H)$ | $\mathcal{O}(H)$ *(Update node subtree sizes during balance/re-linking)* |
| **Find $k$-th Smallest** | $\mathcal{O}(H + k)$ | $\mathcal{O}(H)$ *(Skips entire subtrees in binary search fashion)* |

---

### 2. Implementations

#### Iterative Inorder (Early Stopping)

```python
from typing import Optional

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        curr = root
        
        while curr or stack:
            # Go deep left
            while curr:
                stack.append(curr)
                curr = curr.left
            
            curr = stack.pop()
            k -= 1
            if k == 0:
                return curr.val
            
            curr = curr.right
            
        return -1

```

#### Augmented BST Node Definition (Design Reference)

```python
class AugmentedTreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.size = 1  # Total nodes in subtree rooted at this node

class OrderStatisticTree:
    def find_kth(self, root: Optional[AugmentedTreeNode], k: int) -> int:
        curr = root
        while curr:
            left_size = curr.left.size if curr.left else 0
            
            if k == left_size + 1:
                return curr.val
            elif k <= left_size:
                curr = curr.left
            else:
                k -= (left_size + 1)
                curr = curr.right
                
        return -1

```

---

### 3. Step-by-Step Dry Run

For `root = [5, 3, 6, 2, 4, null, null, 1]`, `k = 3`:

```text
        5
       / \
      3   6
     / \
    2   4
   /
  1

```

1. **Stack left branch:** Stack becomes `[5, 3, 2, 1]`. `curr = None`.
2. **Pop `1`:** $k = 3 - 1 = 2$. `curr = 1.right` (`None`).
3. **Pop `2`:** $k = 2 - 1 = 1$. `curr = 2.right` (`None`).
4. **Pop `3`:** $k = 1 - 1 = 0$. Return `3`.

---
