# 543. Diameter of Binary Tree

**Category:** NC150 | **Difficulty:** Easy | **Pattern:** Bottom-Up DFS / Tree DP

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, return the length of its **diameter**.
* **Definition:** The **diameter** is the length of the longest path between *any two nodes* in a tree. This path may or may not pass through the root node.
* **Length Metric:** Path length is measured by the **number of edges** along the path (not the number of nodes).

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> For any node $N$ in the tree:
> * The **longest path passing through $N$ as its highest point** is:
> $$\text{Diameter at } N = \text{height}(\text{left subtree}) + \text{height}(\text{right subtree})$$
> 
> 
> * The **height returned to $N$'s parent** is:
> $$\text{Height at } N = 1 + \max(\text{height}(\text{left subtree}), \text{height}(\text{right subtree}))$$
> 
> 
> 
> 

#### Visual Explanation of the Core Logic

```text
               (Curr Node)  <--- Highest Point of Current Path
               /         \
   height = left        height = right
             /             \
      [ Left Subtree ]   [ Right Subtree ]
             |                  |
      (Deepest Leaf)     (Deepest Leaf)

   =================================================
   Diameter through Curr = left + right (edges)
   Height returned up    = 1 + max(left, right)
   =================================================

```

#### Why Bottom-Up Tree DP?

We compute heights post-order (Bottom-Up):

1. Traverse down to the leaf nodes first.
2. At every node, retrieve the maximum depth/height of its left and right subtrees.
3. Update a global/outer variable (`self.res`) with `left + right`.
4. Return `1 + max(left, right)` so the parent node can compute its own height.

---

### 3. Code & Line-by-Line Explanation

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        # Step 1: Global variable to track the max diameter found so far
        self.res = 0

        def dfs(curr: Optional[TreeNode]) -> int:
            # Base Case: Empty node has a height of 0
            if not curr:
                return 0

            # Step 2: Post-order traversal to get child subtree heights
            left = dfs(curr.left)
            right = dfs(curr.right)

            # Step 3: Update overall max diameter passing through current node
            self.res = max(self.res, left + right)

            # Step 4: Return height of current subtree to the parent node
            return 1 + max(left, right)

        dfs(root)
        return self.res

```

* **Line 4:** Initialize `self.res = 0` to record the maximum diameter across all visited nodes.
* **Line 7–8:** Base case returns height `0` for `None` pointers.
* **Line 11–12:** Recursively fetch heights of left and right branches.
* **Line 15:** Core update formula: `left + right` represents the path length taking `curr` as the turning point.
* **Line 18:** Height propagation formula: returns the depth of the longest single branch + 1 (for the current edge) up to the parent caller.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 1**: `root = [1, 2, 3, 4, 5]`

```text
            1
           / \
          2   3
         / \
        4   5

```

* **`dfs(Node 4)` & `dfs(Node 5)**` (Leaves):
* `left = 0`, `right = 0`
* `self.res = max(0, 0 + 0) = 0`
* Returns `1 + max(0, 0) = 1`


* **`dfs(Node 2)`**:
* `left = 1` (from Node 4), `right = 1` (from Node 5)
* `self.res = max(0, 1 + 1) = 2`
* Returns `1 + max(1, 1) = 2`


* **`dfs(Node 3)`** (Leaf):
* `left = 0`, `right = 0`
* `self.res = max(2, 0 + 0) = 2`
* Returns `1 + max(0, 0) = 1`


* **`dfs(Node 1)`** (Root):
* `left = 2` (from Node 2), `right = 1` (from Node 3)
* `self.res = max(2, 2 + 1) = 3`  $\leftarrow$ **Final Answer**
* Returns `1 + max(2, 1) = 3`



---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node in the tree is visited exactly once during the post-order DFS traversal.
* **Space Complexity:** $\mathcal{O}(H)$ — Where $H$ is the height of the binary tree (used by the recursive call stack). Worst case is $\mathcal{O}(N)$ for a skewed tree, and $\mathcal{O}(\log N)$ for a balanced tree.

---

### 6. Quick Revision Summary (30-Second Recall)

* **Two Responsibilities at Each Node:**
1. **Compute local path:** `left_height + right_height` (updates global maximum).
2. **Return height upward:** `1 + max(left_height, right_height)` (informs parent).


* **Key Distinctions:** Path length = **edges**, not nodes. Diameter does **not** have to pass through the root!

---
