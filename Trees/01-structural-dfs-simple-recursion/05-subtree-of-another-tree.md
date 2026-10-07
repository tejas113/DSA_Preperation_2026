# 572. Subtree of Another Tree

**Category:** NC150 | **Difficulty:** Easy

---

### 1. The Problem Statement

* **Question:** Given the roots of two binary trees `root` and `subRoot`, return `True` if `subRoot` is structurally identical to a subtree inside `root` with matching node values, and `False` otherwise.
* **Simple Explanation:** Imagine taking `subRoot` and holding it up against `root`. Does there exist any node inside `root` where, if you cut off everything above it, the remaining tree looks **100% identical** (same structure and values) to `subRoot`?

---

### 2. The Approach & Strategy

> **Crucial Insight / Core Logic:**
> This problem reuses the helper function from **Problem 3 (Same Tree, LeetCode 100)**.
> To check if `subRoot` is a subtree of `root`:
> 1. Visit each candidate node in `root` (using DFS or BFS).
> 2. Whenever a node's value matches `subRoot.val`, run `isSameTree(node, subRoot)`.
> 3. If `isSameTree` returns `True`, we immediately return `True`. If not, we keep searching through the remaining nodes of `root`.
> 
> 

#### Approach A: Pure Recursive DFS

* **How to Think About It:** A tree `subRoot` is a subtree of `root` if either:
* The tree starting right at `root` is identical to `subRoot`, OR
* `subRoot` is a subtree of `root.left`, OR
* `subRoot` is a subtree of `root.right`.


* **Step-by-Step Logic:**
1. **Base Cases:**
* If `subRoot` is `None`, return `True` (an empty tree is always a subtree of anything).
* If `root` is `None` (but `subRoot` is not), return `False`.


2. **Check Current Node:** If `isSameTree(root, subRoot)` is `True`, return `True`.
3. **Recurse:** Return `isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)`.



#### Approach B: Iterative BFS + Helper DFS (Your Solution)

* **How to Think About It:** Use a queue to traverse `root` level by level. At every visited node whose value matches `subRoot.val`, trigger `isSameTree(node, subRoot)`.
* **Step-by-Step Logic:**
1. Base case checks for empty tree inputs.
2. Initialize a queue with `root`.
3. While queue is not empty:
* Pop the current `node`.
* If `node.val == subRoot.val`, check `if self.isSameTree(node, subRoot): return True`.
* Push `node.left` and `node.right` to the queue to keep searching.


4. If queue empties without finding a match, return `False`.



---

### 3. Code & Line-by-Line Explanation

#### Solution A: Pure Recursive DFS

```python
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        # An empty subRoot is technically a subtree of any tree
        if not subRoot:
            return True
        # If main root is empty but subRoot isn't, subRoot cannot be present
        if not root:
            return False

        # If trees match starting at this node, we found it!
        if self.isSameTree(root, subRoot):
            return True

        # Otherwise, search in left subtree OR right subtree
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def isSameTree(self, s: Optional[TreeNode], t: Optional[TreeNode]) -> bool:
        if not s and not t:
            return True
        if not s or not t:
            return False
        if s.val != t.val:
            return False
        return self.isSameTree(s.left, t.left) and self.isSameTree(s.right, t.right)

```

* **Line 4 - 7:** Base cases handling empty inputs.
* **Line 10 - 11:** Invokes `isSameTree` to check if the tree anchored at `root` matches `subRoot`.
* **Line 14:** Recurses on `root.left` and `root.right`. Returns `True` as soon as either branch finds a match.

---

#### Solution B: Iterative BFS + Helper DFS (Your Code)

```python
from collections import deque

class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if not subRoot:
            return True
        if not root:
            return False

        queue = deque([root])

        while queue:
            node = queue.popleft()

            # Optional optimization: only call isSameTree if values match
            if node.val == subRoot.val:
                if self.isSameTree(node, subRoot):
                    return True

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return False

    def isSameTree(self, s: Optional[TreeNode], t: Optional[TreeNode]) -> bool:
        if not s and not t:
            return True
        if not s or not t:
            return False
        if s.val != t.val:
            return False
        return self.isSameTree(s.left, t.left) and self.isSameTree(s.right, t.right)

```

* **Line 4 - 7:** Guard clauses against `None` inputs.
* **Line 9:** Initializes the BFS queue with `root`.
* **Line 15 - 17:** Optimization: checks `node.val == subRoot.val` first before invoking the `isSameTree` comparison to avoid unnecessary function call overhead.
* **Line 19 - 22:** Traverses down the main tree level by level.
* **Line 26 - 32:** The standard `Same Tree` helper function checking both structure and node values recursively.

---

### 4. Step-by-Step Dry Run

Let's use **Example 2**: `root = [3, 4, 5, 1, 2, null, null, null, null, 0]`, `subRoot = [4, 1, 2]`

```text
       Main Tree (root):         SubTree (subRoot):
              3                         4
             / \                       / \
            4   5                     1   2
           / \
          1   2
             /
            0

```

#### Dry Run B (BFS Traversal):

* **Initial Queue:** `queue = [Node(3)]`
* **Iteration 1:**
* Pop `Node(3)`. `3 != subRoot.val (4)` $\rightarrow$ Skip `isSameTree`.
* Push children: `queue = [Node(4), Node(5)]`.


* **Iteration 2:**
* Pop `Node(4)`. `4 == subRoot.val (4)` $\rightarrow$ Trigger `isSameTree(Node(4), subRoot)`:
* Compare roots: `4 == 4` (OK).
* Compare lefts: `1 == 1` (OK).
* Compare rights: `Node(2)` in main tree vs `Node(2)` in subRoot:
* Main tree's `Node(2)` has a left child `Node(0)`.
* `subRoot`'s `Node(2)` has left child `None`.
* `isSameTree` fails because `2.left` mismatch (`0 != None`).


* `isSameTree` returns `False`.


* Push children of `Node(4)`: `queue = [Node(5), Node(1), Node(2)]`.


* **Iteration 3:**
* Pop `Node(5)`. `5 != 4` $\rightarrow$ Skip `isSameTree`. Push children (`None`).


* **Iteration 4:**
* Pop `Node(1)`. `1 != 4` $\rightarrow$ Skip `isSameTree`.


* **Iteration 5:**
* Pop `Node(2)`. `2 != 4` $\rightarrow$ Skip `isSameTree`.


* **End of Queue:** Queue becomes empty `[]`.
* **Final Result:** Returns `False`.

---

### 5. Complexity Analysis

Let $N$ be the number of nodes in `root` and $M$ be the number of nodes in `subRoot`.

* **Time Complexity:** $O(N \times M)$
* **Why?** In the worst-case scenario (e.g., all nodes in `root` have identical values), we might invoke `isSameTree` (which costs $O(M)$ time) for every node in `root` ($N$ total nodes), leading to $O(N \times M)$ total work.


* **Space Complexity:** $O(H_{root} + H_{subRoot})$ for DFS / $O(W_{root} + H_{subRoot})$ for BFS.
* **Why?** The recursion call stack depth for `isSameTree` takes up to $O(H_{subRoot})$ space, while traversing `root` uses memory proportional to the height/width of `root`.



---

### 6. Quick Revision Summary (30-Second Recall)

* **Two-Level Problem:** Outer function searches for candidate root nodes in `root`; inner function (`isSameTree`) verifies if the tree branches are identical.
* **Key Takeaway:** Always write `isSameTree` cleanly first, then plug it into your traversal loop/recursion!
