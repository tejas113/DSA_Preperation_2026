# 222. Count Complete Tree Nodes

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Easy / Medium | **Pattern:** Binary Search / Tree Height Comparison

---

### 1. The Core Logic

A **Complete Binary Tree** has all levels filled except possibly the last level, which is filled from left to right.

1. **Height Comparison:**
* Compute the **left height** by traversing down leftmost edges (`curr = curr.left`).
* Compute the **right height** by traversing down rightmost edges (`curr = curr.right`).


2. **Perfect Subtree Optimization:**
* If `left_h == right_h`: The subtree is completely full. Total nodes = $2^{\text{left\_h}} - 1$.
* If `left_h != right_h`: The last level is incomplete. Recurse on `root.left` and `root.right` and sum their results $+ 1$ for the root.



Because at least one of the two subtrees (`root.left` or `root.right`) is guaranteed to be a perfect binary tree at every step, recursion only continues down **one non-perfect subtree**.

---

### 2. Code Implementation

```python
from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        # Calculate height along the leftmost path
        left_h = 0
        curr = root
        while curr:
            left_h += 1
            curr = curr.left

        # Calculate height along the rightmost path
        right_h = 0
        curr = root
        while curr:
            right_h += 1
            curr = curr.right

        # Perfect binary tree condition
        if left_h == right_h:
            return (1 << left_h) - 1

        # Fallback recursive step for incomplete tree
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**: `root = [1, 2, 3, 4, 5, 6]`

```text
        1
       / \
      2   3
     / \ /
    4  5 6

```

1. **`countNodes(1)`:**
* `left_h` along `1 -> 2 -> 4` = `3`
* `right_h` along `1 -> 3` = `2`
* `left_h != right_h` $\rightarrow$ Return `1 + countNodes(2) + countNodes(3)`.


2. **`countNodes(2)`:**
* `left_h` along `2 -> 4` = `2`
* `right_h` along `2 -> 5` = `2`
* `left_h == right_h` $\rightarrow$ Perfect subtree! Returns `(1 << 2) - 1 = 3` (nodes 2, 4, 5).


3. **`countNodes(3)`:**
* `left_h` along `3 -> 6` = `2`
* `right_h` along `3` = `1`
* `left_h != right_h` $\rightarrow$ Return `1 + countNodes(6) + countNodes(None)`.
* `countNodes(6)` has `left_h = 1`, `right_h = 1` $\rightarrow$ Returns `1`.
* Returns `1 + 1 + 0 = 2` (nodes 3, 6).


4. **Combine at Root `1`:**
* Total = `1 + 3 + 2 = 6`.



---

### 4. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(\log^2 N)$
* Tree height $H = \log N$.
* Finding left and right heights takes $\mathcal{O}(\log N)$ time.
* In each recursive step, at least one half is a perfect binary tree, so we recurse into at most **one** non-perfect subtree.
* Overall recurrence relation: $T(N) = T(N/2) + \mathcal{O}(\log N) \implies \mathcal{O}(\log^2 N)$.


* **Space Complexity:** $\mathcal{O}(\log N)$ for the call stack depth.

---

### 5. Quick Revision Summary (30-Second Recall)

* **Property:** In a complete binary tree, if leftmost height == rightmost height, it's a **perfect tree**.
* **Formula:** Node count of a perfect binary tree of height $h$ is $(2^h - 1)$ or `(1 << h) - 1`.
* **Sub-linear Time:** At each recursive level, at least one child is a perfect tree, giving $\mathcal{O}(\log^2 N)$ performance.

---
