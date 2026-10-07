# 450. Delete Node in a BST

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Binary Search Tree / Recursion

---

### 1. The Core Logic & 3 Deletion Cases

Deleting a node requires two phases: **Searching** for the node using BST properties, and then **Deleting** it while preserving BST order.

Once `key == root.val`, we handle one of **three possible structural cases**:

#### Case 1: Node has No Left Child (or is a Leaf Node)

If `root.left` is `None`, return `root.right` to the parent.

* If `root` is a leaf, `root.right` is also `None`, effectively deleting the leaf.
* If `root` has only a right child, returning `root.right` directly connects the parent to that child.

#### Case 2: Node has No Right Child

If `root.right` is `None`, return `root.left` to the parent. This bypasses the deleted node and promotes its left child.

#### Case 3: Node has Two Children (The Tricky Case)

You cannot simply delete the node without disconnecting whole subtrees. To fix this:

1. Find the **In-Order Successor**: The smallest node in the right subtree (i.e., keep going left from `root.right`).
2. Overwrite the target node's value with the successor's value (`root.val = curr.val`).
3. Recursively delete the successor node from the right subtree (`root.right = self.deleteNode(root.right, root.val)`).

---

### 2. Code Breakdown

```python
from typing import Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None

        # Step 1: Search for the target node
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        
        # Step 2: Target node found (key == root.val)
        else:
            # Cases 1 & 2: Missing one child (or no children)
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            # Case 3: Two children
            # Find the in-order successor (minimum node in right subtree)
            curr = root.right
            while curr.left:
                curr = curr.left

            # Overwrite current node's value with successor value
            root.val = curr.val

            # Recursively delete the duplicate successor node from right subtree
            root.right = self.deleteNode(root.right, root.val)

        return root

```

---

### 3. Step-by-Step Dry Run (Case 3 - Node with 2 Children)

Consider **Example 1**: `root = [5, 3, 6, 2, 4, null, 7]`, `key = 3`

```text
        5
       / \
     (3)  6      <-- Target node to delete = 3
     / \    \
    2   4    7

```

* **Step 1 (Search):** Starts at `5`. Since `3 < 5`, call `deleteNode(3, key=3)` on `root.left`.
* **Step 2 (Target Found):** `root.val == 3`. Node `3` has both left (`2`) and right (`4`) children.
* **Step 3 (Find In-Order Successor):**
* `curr = root.right` $\rightarrow$ Node `4`.
* Node `4` has no left child, so `4` is the smallest value in the right subtree.


* **Step 4 (Value Replacement):** Overwrite Node `3`'s value with `4`.
```text
        5
       / \
     (4)  6    <-- Value 3 replaced with 4 (temporarily duplicate 4 exists)
     / \    \
    2   4    7

```


* **Step 5 (Delete Successor):** Call `deleteNode(root.right, 4)` to delete the original Node `4` from the right subtree. Node `4` is a leaf, so it simply returns `None`.
* **Final Tree:**
```text
        5
       / \
      4   6
     /     \
    2       7

```



---

### 4. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(H)$, where $H$ is the height of the tree.
* Searching takes $\mathcal{O}(H)$.
* Finding the successor and deleting it takes at most $\mathcal{O}(H)$.
* Best/Average Case (Balanced Tree): $\mathcal{O}(\log N)$
* Worst Case (Skewed Tree): $\mathcal{O}(N)$


* **Space Complexity:** $\mathcal{O}(H)$ for the recursive call stack.

---

### 5. Quick Revision Summary (30-Second Recall)

* **0 or 1 Child:** Return the non-`None` child (or `None` if leaf).
* **2 Children:**
1. Find **In-order Successor** (leftmost node of `root.right`).
2. Copy successor value to current node.
3. Recursively delete successor node from right subtree.



---
