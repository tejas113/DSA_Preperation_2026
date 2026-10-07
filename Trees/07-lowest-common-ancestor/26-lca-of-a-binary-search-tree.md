# 235. Lowest Common Ancestor of a Binary Search Tree

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Binary Search Tree Property / Divergence Point

---

### 1. The Core Intuition

In a BST, values in the left subtree are strictly smaller than the parent, and values in the right subtree are strictly larger. We can leverage this to navigate directly to the LCA without checking the whole tree:

1. **Both $p$ and $q$ are smaller than `root.val`:** The LCA must lie in the **left subtree**.
2. **Both $p$ and $q$ are larger than `root.val`:** The LCA must lie in the **right subtree**.
3. **Split / Match Point:** If one target is on the left and the other is on the right (or if `root` equals $p$ or $q$), current `root` is the **Lowest Common Ancestor**.

---

### 2. Code Implementations

#### Approach A: Recursive (Your Solution)

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # If both nodes lie in the left subtree
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        
        # If both nodes lie in the right subtree
        elif p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        
        # Split point found (or root matches p or q) -> LCA found
        else:
            return root

```

#### Approach B: Iterative ($\mathcal{O}(1)$ Auxiliary Space)

Since we only go down one branch at a time without needing post-order actions, we can convert the recursion to a simple `while` loop to optimize space complexity.

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        cur = root
        
        while cur:
            if p.val < cur.val and q.val < cur.val:
                cur = cur.left
            elif p.val > cur.val and q.val > cur.val:
                cur = cur.right
            else:
                return cur

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**: `root = [6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]`, `p = 2`, `q = 8`

```text
        6
       / \
      2   8
     / \ / \
    0  4 7  9
      / \
     3   5

```

| Step | `cur.val` | Condition Checked | Action |
| --- | --- | --- | --- |
| **1** | `6` | $p.val (2) < 6$ AND $q.val (8) > 6$ | Split point! Returns Node `6`. |

Tracing **Example 2**: `p = 2`, `q = 4`

| Step | `cur.val` | Condition Checked | Action |
| --- | --- | --- | --- |
| **1** | `6` | $p.val (2) < 6$ AND $q.val (4) < 6$ | Both smaller $\rightarrow$ Move to `cur.left` (`2`). |
| **2** | `2` | $p.val (2) == 2$ (Not both strictly smaller/larger) | Split point! Returns Node `2`. |

---

### 4. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(H)$, where $H$ is the height of the tree ($\mathcal{O}(\log N)$ for balanced trees, $\mathcal{O}(N)$ for skewed trees). We visit at most one node per level.
* **Space Complexity:**
* **Recursive:** $\mathcal{O}(H)$ for call stack.
* **Iterative:** $\mathcal{O}(1)$ auxiliary space.



---

### 5. Quick Revision Summary (30-Second Recall)

* **Both $< \text{root}$:** Go left.
* **Both $> \text{root}$:** Go right.
* **Otherwise (Split / Equal):** Current node is the LCA.

---
