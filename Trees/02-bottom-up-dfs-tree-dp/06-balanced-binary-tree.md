# 110. Balanced Binary Tree

**Category:** NC150 | **Difficulty:** Easy | **Pattern:** Bottom-Up DFS / Tree DP

---

### 1. The Problem Statement

* **Question:** Given a binary tree, determine if it is **height-balanced**.
* **Definition:** A binary tree is height-balanced if, for **every single node** in the tree, the height difference between its left and right subtrees is **at most 1**.
* **Simple Explanation:** Every node acts as a fulcrum. If any node's left leg and right leg differ in depth by more than 1, the entire tree is unbalanced (`False`).

---

### 2. The Approach & Strategy

#### ⚠️ The Naive / Top-Down Approach ($O(N^2)$ Time)

Both approaches in your code snippet follow the **Top-Down** strategy:

1. At the current node, calculate `height(node.left)` and `height(node.right)` using a recursive helper function ($O(N)$ work).
2. Check if `abs(left_h - right_h) <= 1`.
3. Recurse down to child nodes.

**Why this is suboptimal:**
Because `height()` re-calculates the depth of sub-nodes from scratch for every single parent node, you end up re-visiting lower nodes repeatedly. On a skewed tree, this leads to **$O(N^2)$ time complexity**, which is a major red flag in technical interviews.

---

#### 💡 Optimal Approach: Bottom-Up Tree DP ($O(N)$ Time)

Instead of asking parent nodes to calculate heights from the top down, **we compute heights from the bottom up**.

* **Core Logic:**
1. Recurse down to the leaf nodes first (post-order traversal: Left $\rightarrow$ Right $\rightarrow$ Root).
2. Each node asks its children for their heights:
* If either child is already unbalanced, bubble up `-1` (a sentinel value meaning "unbalanced").
* If the height difference between left and right is $> 1$, bubble up `-1`.
* Otherwise, return the actual height: `1 + max(left_h, right_h)`.


3. If the root returns `-1`, the tree is unbalanced; otherwise, it is balanced!



> **Key Takeaway:** By returning both balance status and height in a single pass, we reduce the time complexity from $O(N^2)$ down to **$O(N)$**.

---

### 3. Code & Line-by-Line Explanation

#### Optimal Solution: Bottom-Up DFS ($O(N)$)

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        # A result of -1 means the tree is unbalanced
        return self.dfs(root) != -1

    def dfs(self, root: Optional[TreeNode]) -> int:
        # Base case: empty node has height 0
        if not root:
            return 0

        # Post-order: process left subtree
        left_h = self.dfs(root.left)
        if left_h == -1:
            return -1  # Early termination: left subtree is already unbalanced

        # Post-order: process right subtree
        right_h = self.dfs(root.right)
        if right_h == -1:
            return -1  # Early termination: right subtree is already unbalanced

        # Check current node's balance
        if abs(left_h - right_h) > 1:
            return -1

        # Return actual height to parent
        return 1 + max(left_h, right_h)

```

* **Line 4:** Checks if the final result of `dfs(root)` is NOT `-1`.
* **Line 8–9:** Base case: an empty node contributes `0` to height.
* **Line 12–14:** Recursively computes left subtree height. If `-1` is returned, immediately short-circuit up the call stack.
* **Line 17–19:** Recursively computes right subtree height with the same short-circuit mechanism.
* **Line 22–23:** If height difference $> 1$, mark this node (and entire subtree above it) as unbalanced (`-1`).
* **Line 26:** If balanced, pass the true height `1 + max(left_h, right_h)` up to the parent node.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 2**: `root = [1, 2, 2, 3, 3, null, null, 4, 4]`

```text
              1
             / \
            2   2
           / \
          3   3
         / \
        4   4

```

* **`dfs(Node 4)`** (Leaf level): `left_h = 0`, `right_h = 0` $\rightarrow$ returns `1`.
* **`dfs(Node 3)`** (Leftmost 3):
* Left child (`Node 4`) returns `1`.
* Right child (`Node 4`) returns `1`.
* `abs(1 - 1) <= 1` $\rightarrow$ returns `1 + max(1, 1) = 2`.


* **`dfs(Node 2)`** (Left child of root):
* Left child (`Node 3`) returns `2`.
* Right child (`Node 3` at height 1) returns `1`.
* `abs(2 - 1) <= 1` $\rightarrow$ returns `1 + max(2, 1) = 3`.


* **`dfs(Node 1)`** (Root):
* Left child (`Node 2`) returns `3`.
* Right child (`Node 2`) returns `1`.
* `abs(3 - 1) = 2 > 1` $\rightarrow$ Condition fails! Returns `-1`.


* **Final Result:** `dfs(root) != -1` evaluates to `False`.

---

### 5. Complexity Analysis

| Metric | Top-Down Approach (Your Code) | Bottom-Up Approach (Optimal) |
| --- | --- | --- |
| **Time Complexity** | $O(N^2)$ (Worst case for skewed trees) | **$O(N)$** (Each node visited exactly once) |
| **Space Complexity** | $O(H)$ (Call stack depth) | **$O(H)$** where $H$ is tree height ($\log N$ balanced, $N$ skewed) |

---

### 6. Quick Revision Summary (30-Second Recall)

* **Top-Down ($O(N^2)$) vs Bottom-Up ($O(N)$):** Top-down recalculates node heights repeatedly. Bottom-up returns height and balance status together from bottom to top.
* **Sentinel Value:** Return `-1` as soon as an imbalance is found to short-circuit further work.

---
