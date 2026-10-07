# 98. Validate Binary Search Tree

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** DFS with Range Validation / Inorder Traversal

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, determine if it is a valid binary search tree (BST).
* **BST Rules:**
1. Every node in the left subtree must be **strictly less** than the node's value.
2. Every node in the right subtree must be **strictly greater** than the node's value.
3. Both subtrees must also be valid BSTs.



---

### 2. The Approach & Strategy

> **Crucial Pitfall to Avoid:**
> Checking only direct children (e.g., `node.left.val < node.val < node.right.val`) is **insufficient**. A node deep in a right subtree could be smaller than the root, violating global BST properties.

#### Strategy Options

1. **Range Bounds (DFS Top-Down) [Your Approach]:** Pass a valid open interval `(low, high)` down the recursive tree. When going left, update upper bound `high = node.val`. When going right, update lower bound `low = node.val`.
2. **Inorder Traversal (DFS Bottom-Up):** An inorder traversal of a valid BST must yield a **strictly increasing sequence**. Maintain a `prev` variable and check if `current.val > prev.val` at each step.

---

### 3. Code & Line-by-Line Explanation

#### Approach A: DFS Range Boundaries (Your Solution)

```python
from typing import Optional

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        
        def dfs(node, low, high):
            # Base Case: Empty node is a valid BST
            if not node:
                return True

            # Check if current node breaks strict boundary constraints
            if not (low < node.val < high):
                return False

            # Recurse:
            # - Left child must be in range (low, node.val)
            # - Right child must be in range (node.val, high)
            return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)

        return dfs(root, float('-inf'), float('inf'))

```

#### Approach B: Inorder Traversal

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        prev = float('-inf')

        def inorder(node):
            nonlocal prev
            if not node:
                return True

            if not inorder(node.left):
                return False

            if node.val <= prev:
                return False
            prev = node.val

            return inorder(node.right)

        return inorder(root)

```

* **Approach A, Line 12:** `not (low < node.val < high)` enforces strict inequality. Duplicates (`node.val == low` or `node.val == high`) automatically return `False`.
* **Approach A, Line 18:** Short-circuit evaluation (`and`) ensures that if the left subtree fails validation, the right subtree isn't even evaluated.

---

### 4. Step-by-Step Dry Run (Invalid BST Example)

Consider an invalid tree: `root = [5, 1, 4, null, null, 3, 6]`

```text
        5 (-inf, +inf)
       / \
(1, 5) 1   4 (5, +inf)   <-- INVALID! 4 is not in range (5, +inf)
          / \
         3   6

```

* **Step 1:** `dfs(Node(5), -inf, +inf)` $\rightarrow$ `-inf < 5 < +inf` $\rightarrow$ Valid.
* **Step 2:** `dfs(Node(1), -inf, 5)` $\rightarrow$ `-inf < 1 < 5` $\rightarrow$ Valid. Leaves of `1` return `True`.
* **Step 3:** `dfs(Node(4), 5, +inf)`
* Range check: Is `5 < 4 < +inf`? **No!**
* Evaluates to `False`.


* **Return:** The algorithm immediately aborts and returns `False`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited once in the worst case.
* **Space Complexity:** $\mathcal{O}(H)$ — Memory on the call stack proportional to tree height $H$ ($\mathcal{O}(\log N)$ balanced, $\mathcal{O}(N)$ skewed).

---

### 6. Quick Revision Summary (30-Second Recall)

* **Never check only parent vs child.** Pass bounds `(low, high)` down the recursion.
* **Left Subtree Update:** `high = node.val`.
* **Right Subtree Update:** `low = node.val`.
* **Strict Inequality:** Values must be strictly bounded (`low < val < high`); equal values violate BST properties.

---
