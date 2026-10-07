# 105. Construct Binary Tree from Preorder and Inorder Traversal

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Divide and Conquer / Index Mapping

---

### 1. The Core Relationship Between Preorder & Inorder

To build a unique binary tree, a single traversal (like preorder alone) is insufficient because it doesn't specify where left subtrees end and right subtrees begin. Combining **Preorder** and **Inorder** gives us exact boundaries.

#### Property 1: Preorder Traversal `[Root -> Left -> Right]`

* **The first element of any preorder segment is ALWAYS the root of that subtree.**
* After the root, all elements belonging to the left subtree come next, followed by all elements belonging to the right subtree.

#### Property 2: Inorder Traversal `[Left -> Root -> Right]`

* **The root node acts as a strict divider between the left and right subtrees.**
* Find the root in `inorder`:
* Every element to the **left of the root** belongs to the **left subtree**.
* Every element to the **right of the root** belongs to the **right subtree**.



```text
Preorder: [ ROOT | <---- Left Subtree ----> | <---- Right Subtree ----> ]
            |
            v
Inorder:  [ <---- Left Subtree ----> | ROOT | <---- Right Subtree ----> ]

```

---

### 2. How the Logic Works Step-by-Step

1. **Identify Root:** Pick `preorder[0]` as the root of the current (sub)tree.
2. **Find Split Point (`mid`):** Find `preorder[0]` inside the `inorder` array at index `mid`.
3. **Calculate Subtree Size:**
* The number of nodes in the left subtree is `left_size = mid - inorder_start`.


4. **Partition Arrays:**
* **Left Subtree Preorder:** Next `left_size` elements in `preorder`.
* **Left Subtree Inorder:** All elements before `mid` in `inorder`.
* **Right Subtree Preorder:** Remaining elements in `preorder`.
* **Right Subtree Inorder:** All elements after `mid` in `inorder`.


5. **Recursively Repeat** for `root.left` and `root.right`.

---

### 3. Optimized Code ($\mathcal{O}(N)$ Time & Space)

```python
from typing import List, Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Hash map to lookup root indices in inorder array in O(1) time
        inorder_map = {val: idx for idx, val in enumerate(inorder)}
        pre_idx = 0  # Global pointer for preorder array

        def helper(in_left: int, in_right: int) -> Optional[TreeNode]:
            nonlocal pre_idx
            
            # Base Case: No elements left in current inorder boundary
            if in_left > in_right:
                return None

            # Pick current root from preorder
            root_val = preorder[pre_idx]
            root = TreeNode(root_val)
            pre_idx += 1

            # Root's index in inorder divides left and right subtrees
            mid = inorder_map[root_val]

            # Build left subtree first (matches Preorder ordering: Root -> Left -> Right)
            root.left = helper(in_left, mid - 1)
            root.right = helper(mid + 1, in_right)

            return root

        return helper(0, len(inorder) - 1)

```

---

### 4. Step-by-Step Dry Run

Tracing **Example 1**: `preorder = [3, 9, 20, 15, 7]`, `inorder = [9, 3, 15, 20, 7]`

```text
inorder_map = {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}

```

* **Step 1:** `pre_idx = 0` $\rightarrow$ `root_val = 3`.
* `mid = inorder_map[3] = 1`.
* Left subtree in `inorder`: Range `[0, 0]` (`[9]`).
* Right subtree in `inorder`: Range `[2, 4]` (`[15, 20, 7]`).


* **Step 2 (Recurse Left):** `pre_idx = 1` $\rightarrow$ `root_val = 9`.
* `mid = inorder_map[9] = 0`.
* Left boundary `[0, -1]` $\rightarrow$ `None`.
* Right boundary `[1, 0]` $\rightarrow$ `None`.
* Returns Node `9` to `root.left`.


* **Step 3 (Recurse Right):** `pre_idx = 2` $\rightarrow$ `root_val = 20`.
* `mid = inorder_map[20] = 3`.
* Left subtree range `[2, 2]` (`[15]`).
* Right subtree range `[4, 4]` (`[7]`).
* Continues until subtrees for `15` and `7` attach to `20`.



**Constructed Tree:**

```text
        3
       / \
      9   20
         /  \
        15   7

```

---

### 5. Complexity Analysis

| Metric | Your Array Slicing Approach | Hash Map + Pointers (Optimized) |
| --- | --- | --- |
| **Time Complexity** | $\mathcal{O}(N^2)$ (due to `.index()` and slicing) | $\mathcal{O}(N)$ (each node processed once, $\mathcal{O}(1)$ lookup) |
| **Space Complexity** | $\mathcal{O}(N^2)$ (creating sliced list copies) | $\mathcal{O}(N)$ (hash map + recursion stack) |

---

### 6. Quick Revision Summary (30-Second Recall)

* **Preorder** supplies the **Root** (`preorder[0]`).
* **Inorder** supplies the **Subtree Size / Boundaries** via root index (`mid`).
* **Optimization:** Use a **Hash Map** for `inorder` indices to eliminate `.index()` and pass boundary pointers (`in_left`, `in_right`) to avoid slicing arrays.

---
