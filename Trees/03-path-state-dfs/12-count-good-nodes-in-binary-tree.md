# 1448. Count Good Nodes in Binary Tree

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Top-Down DFS / Path State Tracking

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, return the number of **good nodes**.
* **Definition:** A node $X$ is named **good** if in the path from the root to $X$, there are no nodes with a value strictly greater than $X$'s value.
* **Equivalently:** Node $X$ is good if $X.\text{val} \ge \max(\text{all node values along path from root to } X)$.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> This problem follows the **Top-Down DFS (Path State Tracking)** pattern:
> 1. As we traverse down from parent to child, we maintain a state variable: `max_so_far` (the maximum node value encountered along the current path from the root).
> 2. At every node $N$, we check:
> $$\text{Is } N.\text{val} \ge \text{max\_so\_far}?$$
> 
> 
> * If **yes**, increment our count of good nodes and update `max_so_far = N.val`.
> * If **no**, do not increment count, but pass the existing `max_so_far` down to child calls.
> 
> 
> 3. Unlike Path Sum problems, **every node** is evaluated (not just leaf nodes).
> 
> 

#### Visualizing Path Max State

```text
                     (3) [max_so_far = 3]  <-- 3 >= 3? YES (Good = 1)
                    /   \
 [max_so_far = 3] (1)   (4) [max_so_far = 4]  <-- 4 >= 3? YES (Good = 2)
                 /     /   \
  (3) [max = 3] (3)   (1)  (5) [max = 5]  <-- 5 >= 4? YES (Good = 4)
  <-- 3 >= 3? YES           <-- 1 >= 4? NO
    (Good = 3)

```

---

### 3. Code & Line-by-Line Explanation

#### Solution A: Pure Functional DFS (No Global/Nonlocal State)

```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:

        def dfs(node: Optional[TreeNode], max_so_far: int) -> int:
            if not node:
                return 0

            # Step 1: Check if current node is a good node
            is_good = 1 if node.val >= max_so_far else 0

            # Step 2: Update path max for child calls
            max_so_far = max(max_so_far, node.val)

            # Step 3: Combine good node counts from subtrees
            return is_good + dfs(node.left, max_so_far) + dfs(node.right, max_so_far)

        return dfs(root, root.val)

```

#### Solution B: Helper with State Accumulation (Your Approach Refined)

```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        good_count = 0

        def dfs(node: Optional[TreeNode], max_so_far: int) -> None:
            nonlocal good_count
            if not node:
                return

            # Check if current node value is greater than or equal to path maximum
            if node.val >= max_so_far:
                good_count += 1
                max_so_far = node.val  # Update path state

            dfs(node.left, max_so_far)
            dfs(node.right, max_so_far)

        dfs(root, root.val)
        return good_count

```

* **Line 5–6:** Guard clause for `None` pointers.
* **Line 9:** `node.val >= max_so_far` verifies the good node condition. Note: in your original code, updating `root_max = max(root.val, root_max)` *before* checking `root.val >= root_max` caused `root.val >= root_max` to always evaluate to `True` for that specific line check—checking the condition first or explicitly setting `max_so_far = max(max_so_far, node.val)` handles this cleanly.
* **Line 13–14:** Recurses down left and right branches carrying the updated path maximum forward.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 1**: `root = [3, 1, 4, 3, null, 1, 5]`

* **`dfs(Node 3, max_so_far = 3)`** (Root):
* `3 >= 3` $\rightarrow$ **Good Node!** (`good_count = 1`). `max_so_far = 3`.
* Recurses: `dfs(Node 1, 3)` and `dfs(Node 4, 3)`.


* **Left Subtree — `dfs(Node 1, max_so_far = 3)**`:
* `1 >= 3` is `False` $\rightarrow$ Not good (`good_count = 1`). `max_so_far` remains `3`.
* Recurses: `dfs(Node 3, 3)`.
* **`dfs(Node 3, max_so_far = 3)`**:
* `3 >= 3` $\rightarrow$ **Good Node!** (`good_count = 2`). `max_so_far = 3`.




* **Right Subtree — `dfs(Node 4, max_so_far = 3)**`:
* `4 >= 3` $\rightarrow$ **Good Node!** (`good_count = 3`). `max_so_far = 4`.
* Recurses: `dfs(Node 1, 4)` and `dfs(Node 5, 4)`.
* **`dfs(Node 1, 4)`**: `1 >= 4` is `False` $\rightarrow$ Not good (`good_count = 3`).
* **`dfs(Node 5, 4)`**: `5 >= 4` $\rightarrow$ **Good Node!** (`good_count = 4`).


* **Final Result:** Returns `4`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node in the tree is visited exactly once.
* **Space Complexity:** $\mathcal{O}(H)$ — Recursion stack depth proportional to tree height $H$ ($\mathcal{O}(N)$ for skewed trees, $\mathcal{O}(\log N)$ for balanced trees).

---

### 6. Quick Revision Summary (30-Second Recall)

* **Path State Pattern:** Pass `max_so_far` down through recursion arguments.
* **Good Node Condition:** `node.val >= max_so_far`.
* **Propagation:** Update `max_so_far = max(max_so_far, node.val)` before passing to child calls.

---
