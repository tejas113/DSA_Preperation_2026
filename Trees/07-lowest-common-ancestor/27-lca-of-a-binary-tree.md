# 236. Lowest Common Ancestor of a Binary Tree

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** DFS / Post-Order Subtree Searching

---

### 1. The Core Logic

The algorithm uses a bottom-up (post-order) traversal to bubble up found targets $p$ and $q$:

1. **Base Case:**
* If `root` is `None`, return `None`.
* If `root` equals $p$ or $q$, return `root` (we found one of the targets).


2. **Recursive Traversal:**
* Recurse on `root.left` $\rightarrow$ `left_res`
* Recurse on `root.right` $\rightarrow$ `right_res`


3. **Subtree Evaluation:**
* **Both non-`None` (`left_res` and `right_res`):** $p$ is in one subtree and $q$ is in the other. Therefore, current `root` is the split point and the **LCA**.
* **One is non-`None`:** Both targets reside within that single subtree (or one target is an ancestor of the other). Bubble that non-`None` result up to the parent.
* **Both `None`:** Neither $p$ nor $q$ exists in this subtree. Return `None`.



---

### 2. Clean Code Implementation

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Base Case: Empty node or target found
        if not root or root == p or root == q:
            return root

        # Post-Order Traversal: Search left and right subtrees
        left_res = self.lowestCommonAncestor(root.left, p, q)
        right_res = self.lowestCommonAncestor(root.right, p, q)

        # Case 1: p and q are found in separate subtrees -> current root is LCA
        if left_res and right_res:
            return root

        # Case 2: Both p and q are in the same subtree -> return the non-None result
        return left_res if left_res else right_res

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 2**: `root = [3, 5, 1, 6, 2, 0, 8, null, null, 7, 4]`, `p = 5`, `q = 4`

```text
        3
       / \
     (5)  1
     / \ / \
    6  2 0  8
      / \
     7  (4)

```

1. **Call `lowestCommonAncestor(3)`:**
* Recurse left on `5`.


2. **Call `lowestCommonAncestor(5)`:**
* Hits base case `root == p` (`5 == 5`).
* **Immediately returns Node `5**` without searching further down `5`'s subtree.


3. **Back at Root `3`:**
* `left_res = Node 5`.
* Recurse right on `1` $\rightarrow$ returns `None` (neither $p$ nor $q$ is under `1`).
* `right_res = None`.


4. **Evaluate Root `3`:**
* `left_res` is Node `5`, `right_res` is `None`.
* Returns `left_res` (Node `5`).



**Final Result:** Node `5` (since $p = 5$ is an ancestor of $q = 4$).

---

### 4. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — In the worst case, every node in the binary tree is visited once.
* **Space Complexity:** $\mathcal{O}(H)$ — Memory used by the recursive call stack, where $H$ is the tree height ($\mathcal{O}(\log N)$ for balanced trees, $\mathcal{O}(N)$ for skewed trees).

---

### 5. Quick Revision Summary (30-Second Recall)

* **Base Cases:** `not root` $\rightarrow$ `None`; `root in (p, q)` $\rightarrow$ `root`.
* **Recurse:** Check both `left` and `right`.
* **Combine Results:**
* Both non-`None` $\rightarrow$ return `root` (split point).
* One non-`None` $\rightarrow$ return the non-`None` node.



---
