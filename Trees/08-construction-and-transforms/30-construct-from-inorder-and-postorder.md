# 106. Construct Binary Tree from Inorder and Postorder Traversal

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Divide and Conquer / Index Mapping

---

### 1. The Core Relationship: Inorder vs Postorder

#### Property 1: Postorder Traversal `[Left -> Right -> Root]`

* **The LAST element of any postorder segment is ALWAYS the root of that subtree.**
* Reading postorder backwards: `Root` $\rightarrow$ `Right Subtree` $\rightarrow$ `Left Subtree`.

#### Property 2: Inorder Traversal `[Left -> Root -> Right]`

* **The root node acts as a strict boundary divider.**
* Elements to the **left** of the root in `inorder` belong to the **left subtree**.
* Elements to the **right** of the root in `inorder` belong to the **right subtree**.

```text
Inorder:    [ <---- Left Subtree ----> | ROOT | <---- Right Subtree ----> ]
                                          ^
                                          |
Postorder:  [ <---- Left Subtree ----> | <---- Right Subtree ----> | ROOT ]

```

---

### 2. Code Implementations

#### Approach A: Optimized Hash Map + Pointers ($\mathcal{O}(N)$ Time & Space)

```python
from typing import List, Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        # Hash map for O(1) index lookups in inorder array
        inorder_map = {val: idx for idx, val in enumerate(inorder)}
        
        # Pointer starting from the end of postorder array
        post_idx = len(postorder) - 1

        def helper(in_left: int, in_right: int) -> Optional[TreeNode]:
            nonlocal post_idx
            
            # Base Case: No elements remaining in current boundary
            if in_left > in_right:
                return None

            # Pick current root from postorder end
            root_val = postorder[post_idx]
            root = TreeNode(root_val)
            post_idx -= 1

            # Find split index in inorder array
            mid = inorder_map[root_val]

            # IMPORTANT: Build RIGHT subtree first!
            # Postorder backwards yields: Root -> Right -> Left
            root.right = helper(mid + 1, in_right)
            root.left = helper(in_left, mid - 1)

            return root

        return helper(0, len(inorder) - 1)

```

#### Approach B: Your Array Slicing Solution ($\mathcal{O}(N^2)$ Time)

```python
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        if not inorder or not postorder:
            return None

        # Root is the last element of postorder
        root = TreeNode(postorder[-1])
        mid = inorder.index(postorder[-1])

        # Slice subtrees
        root.left = self.buildTree(inorder[:mid], postorder[:mid])
        root.right = self.buildTree(inorder[mid+1:], postorder[mid:-1])

        return root

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**: `inorder = [9, 3, 15, 20, 7]`, `postorder = [9, 15, 7, 20, 3]`

```text
inorder_map = {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}

```

* **Step 1:** `post_idx = 4` $\rightarrow$ `root_val = 3`.
* `mid = inorder_map[3] = 1`.
* Right boundary: `[2, 4]` (`[15, 20, 7]`).
* Left boundary: `[0, 0]` (`[9]`).


* **Step 2 (Build Right First):** `post_idx = 3` $\rightarrow$ `root_val = 20`.
* `mid = inorder_map[20] = 3`.
* Recurse right: `[4, 4]` $\rightarrow$ Node `7`.
* Recurse left: `[2, 2]` $\rightarrow$ Node `15`.
* Node `20` connected to `root.right`.


* **Step 3 (Build Left):** `post_idx = 0` $\rightarrow$ `root_val = 9`.
* Recurse on `[0, 0]` $\rightarrow$ Node `9` connected to `root.left`.



**Result Tree:**

```text
        3
       / \
      9   20
         /  \
        15   7

```

---

### 4. Complexity Analysis

| Metric | Slicing Approach (Original) | Hash Map + Pointers (Optimized) |
| --- | --- | --- |
| **Time Complexity** | $\mathcal{O}(N^2)$ (due to `.index()` and slicing) | $\mathcal{O}(N)$ (single pass over postorder) |
| **Space Complexity** | $\mathcal{O}(N^2)$ (creates intermediate sliced lists) | $\mathcal{O}(N)$ (hash map + recursion stack) |

---

### 5. Quick Revision Summary (30-Second Recall)

* **Root Location:** `postorder[-1]` is the root.
* **Subtree Order:** Traversing postorder backwards requires building **Right Subtree FIRST**, then **Left Subtree**.
* **Optimization:** Store `inorder` indices in a Hash Map for $\mathcal{O}(1)$ lookups and pass pointers (`in_left`, `in_right`) to avoid slicing.

---
