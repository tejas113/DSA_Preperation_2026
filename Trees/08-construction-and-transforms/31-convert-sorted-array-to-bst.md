# 108. Convert Sorted Array to Binary Search Tree

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Easy | **Pattern:** Divide and Conquer / Binary Search Strategy

---

### 1. The Core Intuition

To make a Binary Search Tree **height-balanced** (where the depth of the two subtrees of every node never differs by more than one):

1. Pick the **middle element** of the sorted array as the root node. This evenly divides the remaining elements into two halves.
2. Recursively apply the same logic to the left half to construct `root.left`.
3. Recursively apply the same logic to the right half to construct `root.right`.

```text
Array:  [ -10,  -3,   0,   5,   9 ]
                ^
             Middle (Root = 0)
            /                 \
  Left: [-10, -3]        Right: [5, 9]

```

---

### 2. Code Implementations

#### Approach A: Optimized Pointer Approach ($\mathcal{O}(N)$ Time, No Slicing)

```python
from typing import List, Optional

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        
        def helper(left: int, right: int) -> Optional[TreeNode]:
            # Base Case: Invalid range boundary
            if left > right:
                return None

            # Always pick the middle element as root
            mid = (left + right) // 2
            root = TreeNode(nums[mid])

            # Recursively build left and right subtrees using boundary pointers
            root.left = helper(left, mid - 1)
            root.right = helper(mid + 1, right)

            return root

        return helper(0, len(nums) - 1)

```

#### Approach B: Your Array Slicing Solution

```python
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None

        mid = len(nums) // 2

        root = TreeNode(nums[mid])
        root.left = self.sortedArrayToBST(nums[0:mid])
        root.right = self.sortedArrayToBST(nums[mid+1:])

        return root

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**: `nums = [-10, -3, 0, 5, 9]`

* **Call 1:** `helper(0, 4)`
* `mid = (0 + 4) // 2 = 2` $\rightarrow$ `root = TreeNode(0)`.
* Recurse left: `helper(0, 1)`.
* Recurse right: `helper(3, 4)`.


* **Call 2 (Left Branch):** `helper(0, 1)`
* `mid = (0 + 1) // 2 = 0` $\rightarrow$ `root.left = TreeNode(-10)`.
* Recurse left: `helper(0, -1)` $\rightarrow$ `None`.
* Recurse right: `helper(1, 1)` $\rightarrow$ `TreeNode(-3)`.


* **Call 3 (Right Branch):** `helper(3, 4)`
* `mid = (3 + 4) // 2 = 3` $\rightarrow$ `root.right = TreeNode(5)`.
* Recurse left: `helper(3, 2)` $\rightarrow$ `None`.
* Recurse right: `helper(4, 4)` $\rightarrow$ `TreeNode(9)`.



**Constructed Tree:**

```text
        0
       / \
    -10   5
      \    \
      -3    9

```

---

### 4. Complexity Analysis

| Metric | Array Slicing (Original) | Pointer Boundary (Optimized) |
| --- | --- | --- |
| **Time Complexity** | $\mathcal{O}(N \log N)$ (due to slicing $N$ elements across $\log N$ levels) | $\mathcal{O}(N)$ (each element visited once) |
| **Space Complexity** | $\mathcal{O}(N \log N)$ (copies created during slicing) | $\mathcal{O}(\log N)$ (recursion stack depth for balanced tree) |

---

### 5. Quick Revision Summary (30-Second Recall)

* **Height Balance:** Pick `mid = (left + right) // 2` as root.
* **Divide & Conquer:** `root.left = helper(left, mid - 1)`, `root.right = helper(mid + 1, right)`.
* **Optimization:** Use index boundaries (`left`, `right`) to avoid $\mathcal{O}(N)$ array slicing overhead.

---
