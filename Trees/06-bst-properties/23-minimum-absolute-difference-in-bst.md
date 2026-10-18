# 530. Minimum Absolute Difference in BST

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Easy | **Pattern:** Inorder Traversal (BST Property)

---

### 1. The Core Intuition

In any sorted array, the smallest difference between any pair of numbers always lies between two adjacent elements. Since an Inorder Traversal of a BST produces a sorted list of values:

1. Track the **previously visited node's value** (`prev`).
2. Every time you process a new node (`curr`), compute `curr.val - prev`.
3. Update `min_diff = min(min_diff, curr.val - prev)`.
4. Update `prev = curr.val`.

---

### 2. Space Optimization Comparison

#### Array-Based (Your Implementation)

* Collects all $N$ values in `res` array.
* Computes differences in a second pass over `res`.
* **Space Complexity:** $\mathcal{O}(N)$ space for the array + $\mathcal{O}(H)$ stack space.

#### On-the-Fly Pointer Tracking (Optimized)

* Tracks only the previous element value.
* Computes differences inline during traversal.
* **Space Complexity:** $\mathcal{O}(H)$ stack space only ($\mathcal{O}(1)$ auxiliary space if ignoring stack).

---

### 3. Code Implementations

#### Approach 0: Array-Based Iterative Inorder (Baseline)

Collect the full sorted list first via iterative inorder, then walk it once to find the smallest gap between adjacent entries.

```python
from typing import Optional


class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        res = []
        stack = []
        cur = root
        min_diff = float('inf')

        # Pass 1: iterative inorder traversal -> res is sorted ascending
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left

            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right

        # Pass 2: smallest difference is always between adjacent sorted values
        for i in range(1, len(res)):
            current_diff = res[i] - res[i - 1]
            min_diff = min(min_diff, current_diff)

        return min_diff

```

* **Pass 1** is a standard explicit-stack inorder traversal (see Concept 04 / Problem 20) — it does nothing with the values except collect them, so `res` ends up holding every node's value in ascending order.
* **Pass 2** only needs to compare *consecutive* entries in `res`, because in a sorted list the smallest gap between any two numbers is always between two neighbors — never two numbers with something smaller sitting between them.
* **Cost of this approach:** two full passes, and `res` holds all $N$ values — $\mathcal{O}(N)$ space on top of the traversal itself. Approaches A and B below fold both passes into one, dropping the array entirely.

#### Approach A: Optimized Iterative Inorder

```python
from typing import Optional

class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        stack = []
        cur = root
        prev = None
        min_diff = float('inf')

        while cur or stack:
            # Drill down to the leftmost node
            while cur:
                stack.append(cur)
                cur = cur.left

            cur = stack.pop()

            # Process difference with the immediate predecessor in sorted order
            if prev is not None:
                min_diff = min(min_diff, cur.val - prev)
            prev = cur.val

            # Move to right subtree
            cur = cur.right

        return int(min_diff)

```

#### Approach B: Optimized Recursive Inorder

```python
class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        prev = None
        min_diff = float('inf')

        def inorder(node):
            nonlocal prev, min_diff
            if not node:
                return

            inorder(node.left)

            if prev is not None:
                min_diff = min(min_diff, node.val - prev)
            prev = node.val

            inorder(node.right)

        inorder(root)
        return int(min_diff)

```

---

### 4. Step-by-Step Dry Run

Tracing **Example 1**: `root = [4, 2, 6, 1, 3]`

```text
        4
       / \
      2   6
     / \
    1   3

```

| Traversal Step | Node Visited (`cur.val`) | `prev` Before | Difference Computed | `min_diff` | `prev` After |
| --- | --- | --- | --- | --- | --- |
| **1** | `1` | `None` | N/A (first node) | $\infty$ | `1` |
| **2** | `2` | `1` | $2 - 1 = 1$ | $1$ | `2` |
| **3** | `3` | `2` | $3 - 2 = 1$ | $1$ | `3` |
| **4** | `4` | `3` | $4 - 3 = 1$ | $1$ | `4` |
| **5** | `6` | `4` | $6 - 4 = 2$ | $1$ | `6` |

**Final Result:** `1`

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited once during traversal.
* **Space Complexity:** $\mathcal{O}(H)$ — Height of the tree ($\mathcal{O}(\log N)$ for balanced trees, $\mathcal{O}(N)$ for skewed trees).

---

### 6. Quick Revision Summary (30-Second Recall)

* **BST Inorder Traversal** = Sorted Array.
* **Minimum Difference** always occurs between adjacent elements in sorted order.
* Use a `prev` variable during Inorder Traversal to calculate `node.val - prev` dynamically without allocating an array.

---
