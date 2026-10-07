# 112. Path Sum

**Category:** NC150 | **Difficulty:** Easy | **Pattern:** Top-Down DFS / Path Accumulation

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree and an integer `targetSum`, return `True` if there exists a **root-to-leaf path** where the sum of all node values along the path equals `targetSum`.
* **Constraint:** The path must end specifically at a **leaf node** (a node with no left or right child). An empty tree returns `False` immediately.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> This problem shifts our pattern to **Top-Down DFS (Path Accumulation)**:
> 1. As we move down from parent to child, we pass down the running accumulated sum (or alternatively, subtract `node.val` from `targetSum`).
> 2. We check the target condition **strictly at leaf nodes** (`not node.left and not node.right`).
> 3. If any leaf path satisfies the condition, short-circuit using an `OR` condition across left and right branches.
> 
> 

#### Visualizing Top-Down Accumulation

```text
                     (5)  [accumulated: 5]
                    /   \
  [accumulated: 9] (4)   (8) [accumulated: 13]
                  /       \
[accumulated: 20](11)      (13) [accumulated: 26]
                /  \
               (7)  (2)  <-- Leaf check: 20 + 2 = 22 == targetSum? YES!

```

---

### 3. Code & Line-by-Line Explanation

#### Approach A: Accumulation Parameter (Your Code)

```python
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:

        def dfs(node: Optional[TreeNode], current_sum: int) -> bool:
            # Base Case 1: Empty node path yields False
            if not node:
                return False

            # Add current node's value to accumulated sum
            current_sum += node.val

            # Leaf Node Check: Verify target sum match at terminal node
            if not node.left and not node.right:
                return current_sum == targetSum

            # Recurse down left and right subtrees
            return dfs(node.left, current_sum) or dfs(node.right, current_sum)

        return dfs(root, 0)

```

#### Approach B: Subtraction In-Place (Shorter)

```python
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False

        # Subtract current node value from remaining target
        targetSum -= root.val

        # Leaf node check
        if not root.left and not root.right:
            return targetSum == 0

        # Recurse down subtrees
        return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)

```

* **Approach A, Line 5–6:** Guard against null pointers. Returns `False` if we reach a missing child branch.
* **Approach A, Line 9:** Accumulates `node.val` along the downward path.
* **Approach A, Line 12–13:** **Leaf Guard:** Checks whether the current node is a leaf (`not left and not right`). If yes, verifies if `current_sum == targetSum`.
* **Approach A, Line 16:** Returns `True` if **either** the left or right branch contains a valid path sum.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 1**: `root = [5, 4, 8, 11, null, 13, 4, 7, 2, null, null, null, 1]`, `targetSum = 22`

* **`dfs(Node 5, sum=0)`**:
* `current_sum = 0 + 5 = 5`
* Recurses: `dfs(Node 4, 5)` or `dfs(Node 8, 5)`


* **`dfs(Node 4, sum=5)`**:
* `current_sum = 5 + 4 = 9`
* Recurses: `dfs(Node 11, 9)`


* **`dfs(Node 11, sum=9)`**:
* `current_sum = 9 + 11 = 20`
* Recurses: `dfs(Node 7, 20)` or `dfs(Node 2, 20)`


* **`dfs(Node 7, sum=20)`** (Leaf):
* `current_sum = 20 + 7 = 27` $\neq$ `22` $\rightarrow$ Returns `False`


* **`dfs(Node 2, sum=20)`** (Leaf):
* `current_sum = 20 + 2 = 22 == 22` $\rightarrow$ Returns `True`!


* **Propagation:** `dfs(Node 11)` receives `False or True = True`, returning `True` all the way back up to the root.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited at most once.
* **Space Complexity:** $\mathcal{O}(H)$ — Recursion call stack space proportional to tree height $H$ ($\mathcal{O}(N)$ worst-case for skewed trees, $\mathcal{O}(\log N)$ for balanced trees).

---

### 6. Quick Revision Summary (30-Second Recall)

* **Check condition ONLY at leaves:** `if not node.left and not node.right: return sum == targetSum`.
* **Empty node guard:** `if not node: return False` prevents non-leaf null pointers from returning false positives.

---
