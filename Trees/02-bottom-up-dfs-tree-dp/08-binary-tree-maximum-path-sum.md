# 124. Binary Tree Maximum Path Sum

**Category:** NC150 | **Difficulty:** Hard | **Pattern:** Bottom-Up DFS / Tree DP

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, return the **maximum path sum** of any non-empty path.
* **Definition:** A path is a sequence of connected nodes where no node is visited twice. The path sum is the total of all node values along that path.
* **Key Twist:** The path does **not** need to pass through the root, nor does it need to reach a leaf node. It can start and end at *any* nodes in the tree, but node values can be **negative**.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> This problem is a direct extension of **Problem 7: Diameter of Binary Tree**.
> At every node $N$, we make two distinct decisions:
> 1. **Split Path (Local Max Update):** Combine $N.\text{val} + \text{left\_gain} + \text{right\_gain}$ to form an upside-down "V" shape path centered at $N$. Update the global maximum sum with this total.
> 2. **Single Branch Return (Propagation to Parent):** Return $N.\text{val} + \max(\text{left\_gain}, \text{right\_gain})$ to $N$'s parent. A path continuing upward can only take **one** branch; it cannot split at $N$ *and* also split higher up without revisiting nodes.
> 
> 

#### Visualizing the Split vs. Branch Return

```text
                  ( Parent )
                     |  <-- Single Branch Return: node.val + max(left, right)
                     |
                  ( Node )  <-- Splitting Point: node.val + left + right
                  /      \
             ( Left )  ( Right )
               /            \
          [ Subtree ]    [ Subtree ]

```

#### Handling Negative Sums (`max(0, ...)`):

If a subtree yields a negative sum, including it will only lower our path total. By using `max(0, dfs(child))`, we effectively **drop** negative subtrees (treat their contribution as `0`).

---

### 3. Code & Line-by-Line Explanation

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # Initialize global maximum to negative infinity (handles all-negative tree nodes)
        max_sum = float('-inf')

        def dfs(node: Optional[TreeNode]) -> int:
            nonlocal max_sum
            if not node:
                return 0

            # Step 1: Bottom-up evaluation. Clamp negative subtree sums to 0.
            left = max(0, dfs(node.left))
            right = max(0, dfs(node.right))

            # Step 2: Calculate path sum splitting at current node (Upside-down 'V')
            cur_sum = node.val + left + right

            # Step 3: Update global maximum path sum found so far
            max_sum = max(max_sum, cur_sum)

            # Step 4: Return single branch path sum to parent node
            return node.val + max(left, right)

        dfs(root)
        return max_sum

```

* **Line 4:** `max_sum = float('-inf')` ensures tree configurations where all node values are negative (e.g., `[-3]`) evaluate correctly.
* **Line 11–12:** `max(0, dfs(...))` ignores negative path sums from children.
* **Line 15:** `cur_sum = node.val + left + right` checks the path that uses `node` as its highest peak/turn.
* **Line 18:** Updates the non-local variable `max_sum`.
* **Line 21:** Returns `node.val + max(left, right)` up to the caller so the parent can extend the path along its optimal branch.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 2**: `root = [-10, 9, 20, null, null, 15, 7]`

```text
             -10
             /  \
            9    20
                /  \
               15   7

```

* **`dfs(Node 9)`**:
* `left = 0`, `right = 0`
* `cur_sum = 9 + 0 + 0 = 9` $\rightarrow$ `max_sum = max(-inf, 9) = 9`
* Returns `9 + max(0, 0) = 9`


* **`dfs(Node 15)`**:
* `left = 0`, `right = 0`
* `cur_sum = 15 + 0 + 0 = 15` $\rightarrow$ `max_sum = max(9, 15) = 15`
* Returns `15`


* **`dfs(Node 7)`**:
* `left = 0`, `right = 0`
* `cur_sum = 7 + 0 + 0 = 7` $\rightarrow$ `max_sum = max(15, 7) = 15`
* Returns `7`


* **`dfs(Node 20)`**:
* `left = 15`, `right = 7`
* `cur_sum = 20 + 15 + 7 = 42` $\rightarrow$ `max_sum = max(15, 42) = 42`
* Returns `20 + max(15, 7) = 35`


* **`dfs(Node -10)`** (Root):
* `left = 9`, `right = 35`
* `cur_sum = -10 + 9 + 35 = 34` $\rightarrow$ `max_sum = max(42, 34) = 42`
* Returns `-10 + max(9, 35) = 25`


* **Final Result:** Returns `42` (Path: `15 -> 20 -> 7`).

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is processed exactly once via post-order traversal.
* **Space Complexity:** $\mathcal{O}(H)$ — Where $H$ is the height of the tree (call stack depth). $\mathcal{O}(N)$ for skewed trees, $\mathcal{O}(\log N)$ for balanced trees.

---

### 6. Quick Revision Summary (30-Second Recall)

* **`max(0, dfs(child))`:** Ignore negative subtrees to avoid decreasing the path total.
* **Split at Current Node:** `node.val + left + right` updates `max_sum`.
* **Return to Parent:** `node.val + max(left, right)` propagates one branch up.

---
