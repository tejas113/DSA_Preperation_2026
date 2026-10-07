# 129. Sum Root to Leaf Numbers

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Top-Down DFS / Path Accumulation

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree containing single-digit numbers ($0–9$), return the total sum of all **root-to-leaf numbers**.
* **Definition:** Each root-to-leaf path forms a multi-digit integer created by appending node values sequentially (e.g., path `1 -> 2 -> 3` forms integer `123`).
* **Goal:** Calculate the sum of all such formed integers across every leaf in the tree.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> This problem builds directly on **Problem 9: Path Sum (LC 112)** using **Top-Down DFS (Path Accumulation)**:
> 1. As we move down from a parent node to a child node, we shift the accumulated number left by one decimal place (multiply by 10) and add the current node's digit:
> 
> $$\text{current\_num} = \text{current\_num} \times 10 + \text{node.val}$$
> 
> 
> 2. When reaching a **leaf node** (`not node.left and not node.right`), return `current_num`.
> 3. For internal nodes, return the sum of numbers formed by its left and right subtrees (`left + right`).
> 
> 

#### Visualizing Decimal Shift Accumulation

```text
                     (4)  [curr = 4]
                    /   \
  [curr = 4*10+9 = 49] (9)   (0) [curr = 4*10+0 = 40] (Leaf -> Returns 40)
                  /   \
 [curr = 49*10+5] (5)   (1) [curr = 49*10+1 = 491] (Leaf -> Returns 491)
         (Leaf -> Returns 495)

===================================================================
Total Tree Sum = 495 + 491 + 40 = 1026
===================================================================

```

---

### 3. Code & Line-by-Line Explanation

```python
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:

        def dfs(node: Optional[TreeNode], current_sum: int) -> int:
            # Base Case 1: Empty child branch yields 0 contribution
            if not node:
                return 0

            # Step 1: Shift current number left by one digit and add node value
            current_sum = current_sum * 10 + node.val

            # Step 2: Leaf Node Check — return accumulated root-to-leaf number
            if not node.left and not node.right:
                return current_sum

            # Step 3: Recurse subtrees and return combined sum of all child leaf paths
            left = dfs(node.left, current_sum)
            right = dfs(node.right, current_sum)

            return left + right

        return dfs(root, 0)

```

* **Line 5–6:** Guard against null pointers. Returns `0` if a node has only one child branch (ensures non-existent branch adds nothing to the total).
* **Line 9:** Core math formula: `current_sum * 10 + node.val` shifts digits left (e.g., `4` becomes `40`, then `+ 9` gives `49`).
* **Line 12–13:** **Leaf Guard:** Verifies if current node is a terminal leaf. If so, returns the completed root-to-leaf integer.
* **Line 16–19:** Post-order aggregation: sums the results from the left and right subtrees and returns it up to the parent.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 2**: `root = [4, 9, 0, 5, 1]`

* **`dfs(Node 4, current_sum=0)`**:
* `current_sum = 0 * 10 + 4 = 4`
* Recurses: `dfs(Node 9, 4)` and `dfs(Node 0, 4)`


* **`dfs(Node 9, current_sum=4)`**:
* `current_sum = 4 * 10 + 9 = 49`
* Recurses: `dfs(Node 5, 49)` and `dfs(Node 1, 49)`
* **`dfs(Node 5, 49)`** (Leaf): `current_sum = 49 * 10 + 5 = 495` $\rightarrow$ Returns `495`
* **`dfs(Node 1, 49)`** (Leaf): `current_sum = 49 * 10 + 1 = 491` $\rightarrow$ Returns `491`
* `dfs(Node 9)` returns `495 + 491 = 986`


* **`dfs(Node 0, current_sum=4)`** (Leaf):
* `current_sum = 4 * 10 + 0 = 40` $\rightarrow$ Returns `40`


* **Root Return:** `dfs(Node 4)` returns `left (986) + right (40) = 1026`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited exactly once.
* **Space Complexity:** $\mathcal{O}(H)$ — Recursion call stack height $H$ ($\mathcal{O}(N)$ worst-case for skewed trees, $\mathcal{O}(\log N)$ for balanced trees).

---

### 6. Quick Revision Summary (30-Second Recall)

* **Digit Accumulation:** `current_num = current_num * 10 + node.val`.
* **Leaf Check:** Return `current_num` at leaves; return `left + right` at internal nodes.

---
