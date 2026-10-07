# 101. Symmetric Tree

**Category:** LC150 | **Difficulty:** Easy

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, check whether it is a mirror image of itself (i.e., symmetric around its central vertical axis).
* **Simple Explanation:** Imagine folding the tree down the middle like a piece of paper. The left branch must overlap perfectly with the right branch. This means the **outer child on the left side** must match the **outer child on the right side**, and the **inner child on the left side** must match the **inner child on the right side**.

---

### 2. The Approach & Strategy

> **Crucial Insight / Core Logic:**
> A tree is symmetric if its left and right subtrees are mirror images of each other. For two subtrees `left` and `right` to be mirrors:
> 1. Their root values must be equal (`left.val == right.val`).
> 2. The **far-left** branch of `left` must match the **far-right** branch of `right` (`left.left` with `right.right`).
> 3. The **inner-right** branch of `left` must match the **inner-left** branch of `right` (`left.right` with `right.left`).
> 
> 

#### Approach A: Recursive DFS (Helper Function)

* **How to Think About It:** Split the problem into comparing two distinct nodes at a time—`left` and `right`. Pass them into a helper function `dfs(left, right)` that checks their values and recursively checks their mirrored children.
* **Step-by-Step Logic:**
1. **Base Case:** If `root` is `None`, return `True`.
2. **Helper Function `dfs(left, right)`:**
* If both `left` and `right` are `None`, return `True`.
* If only one is `None`, return `False` (structural asymmetry).
* If `left.val != right.val`, return `False` (value asymmetry).
* **Cross-comparison recurse:** Return `dfs(left.left, right.right) and dfs(left.right, right.left)`.





#### Approach B: Iterative BFS (Queue)

* **How to Think About It:** Queue up pairs of nodes that *should* be identical mirror copies. Pop each pair, perform symmetry checks, and enqueue their children in mirrored order: `(left.left, right.right)` and `(left.right, right.left)`.
* **Step-by-Step Logic:**
1. Initialize a queue with `(root.left, root.right)`.
2. While the queue is not empty:
* Pop a pair `(left, right)`.
* If both are `None`, `continue` (valid branch end).
* If one is `None` or values differ, return `False`.
* Enqueue outer mirror pair: `(left.left, right.right)`.
* Enqueue inner mirror pair: `(left.right, right.left)`.


3. Return `True` if the queue drains completely without mismatch.



---

### 3. Code & Line-by-Line Explanation

#### Solution A: Recursive DFS

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        def dfs(left, right):
            # 1. Both nodes are null -> mirror match at leaf level
            if not left and not right:
                return True

            # 2. One node is null -> structural mismatch
            if not left or not right:
                return False

            # 3. Values do not match -> value mismatch
            if left.val != right.val:
                return False

            # 4. Mirror cross-check: outer branches AND inner branches
            return dfs(left.left, right.right) and dfs(left.right, right.left)
        
        return dfs(root.left, root.right)

```

* **Line 3 - 4:** An empty tree is trivially symmetric.
* **Line 8 - 9:** Base case 1. If both mirror pointers reach `None` together, this branch is structurally symmetric.
* **Line 12 - 13:** Base case 2. If one node exists while its mirror counterpart is missing, symmetry is broken.
* **Line 16 - 17:** Base case 3. Values must match across the mirror line.
* **Line 20:** Cross-compares children: pairs `left.left` with `right.right` (outer edges) and `left.right` with `right.left` (inner edges).
* **Line 22:** Initiates the mirror check starting from the root's direct left and right children.

---

#### Solution B: Iterative BFS

```python
from collections import deque

class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        queue = deque([(root.left, root.right)])

        while queue:
            left, right = queue.popleft()

            # Both null -> mirror match so far
            if not left and not right:
                continue

            # Structural mismatch
            if not left or not right:
                return False

            # Value mismatch
            if left.val != right.val:
                return False

            # Pair outer children together, and inner children together
            queue.append((left.left, right.right))
            queue.append((left.right, right.left))

        return True

```

* **Line 8:** Places the initial pair `(root.left, root.right)` into the queue.
* **Line 11:** Pops the pair currently being evaluated.
* **Line 14 - 15:** If both nodes are `None`, this branch ends safely; move to the next queued pair.
* **Line 18 - 22:** Fails fast if structure or values do not mirror each other.
* **Line 25:** Enqueues outer mirror pair `(left.left, right.right)`.
* **Line 26:** Enqueues inner mirror pair `(left.right, right.left)`.
* **Line 28:** Returns `True` if no symmetry violations were encountered.

---

### 4. Step-by-Step Dry Run

Let's use **Example 1**: `root = [1, 2, 2, 3, 4, 4, 3]`

```text
        1
      /   \
     2     2
    / \   / \
   3   4 4   3

```

#### Dry Run A: Recursive DFS

1. **`isSymmetric(1)`** calls **`dfs(left=2, right=2)`**.
* Values match (`2 == 2`).
* Calls **Outer Pair:** `dfs(left.left=3, right.right=3)`:
* Values match (`3 == 3`).
* Children are `None` $\rightarrow$ Returns `True`.


* Calls **Inner Pair:** `dfs(left.right=4, right.left=4)`:
* Values match (`4 == 4`).
* Children are `None` $\rightarrow$ Returns `True`.


* Combines results: `True and True` $\rightarrow$ Returns `True`.


2. **Final Output:** `True`.

---

#### Dry Run B: Iterative BFS

* **Initial State:** `queue = [(2_left, 2_right)]`
* **Iteration 1:**
* Pop `(2_left, 2_right)`. Values match (`2 == 2`).
* Enqueue outer pair: `(2_left.left [3], 2_right.right [3])`.
* Enqueue inner pair: `(2_left.right [4], 2_right.left [4])`.
* `queue = [(3, 3), (4, 4)]`


* **Iteration 2:**
* Pop `(3, 3)`. Values match (`3 == 3`).
* Enqueue `(None, None)` and `(None, None)`.
* `queue = [(4, 4), (None, None), (None, None)]`


* **Iteration 3:**
* Pop `(4, 4)`. Values match (`4 == 4`).
* Enqueue `(None, None)` and `(None, None)`.
* `queue = [(None, None), (None, None), (None, None), (None, None)]`


* **Remaining Iterations:**
* All remaining pairs are `(None, None)` $\rightarrow$ `continue` skips through them.


* **Final Output:** Returns `True`.

---

### 5. Complexity Analysis

#### DFS Complexity:

* **Time Complexity:** $O(N)$
* **Why?** We visit every node in the tree once to compare it with its corresponding mirror node.


* **Space Complexity:** $O(H)$ where $H$ is the height of the tree.
* **Why?** The recursion stack depth is equal to the height of the tree ($O(\log N)$ for a balanced tree, $O(N)$ worst-case for a skewed tree).



#### BFS Complexity:

* **Time Complexity:** $O(N)$
* **Why?** Every pair of nodes is enqueued and dequeued once.


* **Space Complexity:** $O(W)$ where $W$ is the maximum width of the tree.
* **Why?** The queue holds pairs of nodes at the current level, bounded by $O(N)$ worst-case.



---

### 6. Quick Revision Summary (30-Second Recall)

* **The Key Shift:** Same Tree compares `(left, left)` and `(right, right)`. Symmetric Tree compares **mirrored** pairs: `(left.left, right.right)` and `(left.right, right.left)`.
* **Mental Rule:** Outer matches Outer, Inner matches Inner!

---
