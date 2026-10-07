# 226. Invert Binary Tree

**Category:** LC150 + NC150 | **Difficulty:** Easy

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, mirror the entire tree by swapping every node's left and right subtrees, and return the root.
* **Simple Explanation:** Imagine holding a mirror up to the tree. Every single node has its left and right arms swapped. What was on the far left ends up on the far right.

---

### 2. The Approach & Strategy

#### Approach A: Recursive Depth-First Search (DFS)

* **How to Think About It:** At any node, swap its left and right child pointers. Then, tell your left child to invert itself, and tell your right child to invert itself.
* **Step-by-Step Logic:**
1. **Base Case:** If `root` is `None`, return `None`.
2. **Swap Step:** Swap `root.left` and `root.right` using a temporary variable (or Python tuple swapping).
3. **Recursive Step:** Recursively call `invertTree(root.left)` and `invertTree(root.right)`.
4. **Return:** Return the modified `root`.



#### Approach B: Iterative Breadth-First Search (BFS)

* **How to Think About It:** Visit every node level by level using a queue. Whenever you visit a node, immediately swap its left and right children, then add any existing children to the queue so their children can be swapped next.
* **Step-by-Step Logic:**
1. **Base Case:** If `root` is `None`, return `None`.
2. **Initialization:** Add `root` to a queue.
3. **Queue Processing:** While the queue is not empty:
* Pop the current node.
* Swap its `left` and `right` pointers directly.
* If `node.left` exists, add it to the queue.
* If `node.right` exists, add it to the queue.


4. **Return:** Return `root`.



---

### 3. Code & Line-by-Line Explanation

#### Solution A: Recursive DFS

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        
        # Swap left and right children at the current node
        temp = root.left
        root.left = root.right
        root.right = temp

        # Recursively invert both subtrees
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root

```

* **Line 3 - 4:** If the tree or branch is empty (`None`), stop recursion and return `None`.
* **Line 7 - 9:** Store `root.left` in a `temp` variable before reassigning `root.left` to `root.right`. Then assign `root.right` to `temp`. This completes the physical swap of child pointers.
* **Line 12 - 13:** Perform the exact same mirror operation on the newly placed left and right child branches.
* **Line 15:** Return `root` after all descendant nodes are fully inverted.

---

#### Solution B: Iterative BFS

```python
from collections import deque

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        queue = deque([root])

        while queue:
            node = queue.popleft()
            
            # Tuple swap in Python: swaps left and right child pointers
            node.left, node.right = node.right, node.left
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return root

```

* **Line 5 - 6:** Handles empty tree input cleanly.
* **Line 8:** Creates a queue initialized with the `root` node.
* **Line 10 - 11:** Continuously processes nodes until no more remain in the queue.
* **Line 14:** Uses Python's multiple assignment tuple swap (`a, b = b, a`) to swap `node.left` and `node.right` in a single line without needing an explicit `temp` variable.
* **Line 16 - 19:** Adds existing children to the queue so their children will be swapped in future loop iterations.
* **Line 21:** Returns the root of the now fully inverted tree.

---

### 4. Step-by-Step Dry Run

Let's use **Example 1**: `root = [4, 2, 7, 1, 3, 6, 9]`

```text
Original:
       4
     /   \
    2     7
   / \   / \
  1   3 6   9

```

#### Dry Run A: Recursive DFS

1. **`invertTree(4)`**:
* Swap children: `root.left` becomes `7`, `root.right` becomes `2`.
* Recurse on new left: **`invertTree(7)`**:
* Swap children: `7.left` becomes `9`, `7.right` becomes `6`.
* Recurse **`invertTree(9)`**: Swap children (both `None`). Return `9`.
* Recurse **`invertTree(6)`**: Swap children (both `None`). Return `6`.
* Return `7`.


* Recurse on new right: **`invertTree(2)`**:
* Swap children: `2.left` becomes `3`, `2.right` becomes `1`.
* Recurse **`invertTree(3)`**: Swap children (both `None`). Return `3`.
* Recurse **`invertTree(1)`**: Swap children (both `None`). Return `1`.
* Return `2`.




2. **`invertTree(4)` finishes** and returns `4`.

---

#### Dry Run B: Iterative BFS

* **Initial State:** `queue = [4]`.
* **Step 1:**
* Pop `4`.
* Swap `4.left` and `4.right`. Now `4.left = 7`, `4.right = 2`.
* Append `7` and `2`. `queue = [7, 2]`.


* **Step 2:**
* Pop `7`.
* Swap `7.left` and `7.right`. Now `7.left = 9`, `7.right = 6`.
* Append `9` and `6`. `queue = [2, 9, 6]`.


* **Step 3:**
* Pop `2`.
* Swap `2.left` and `2.right`. Now `2.left = 3`, `2.right = 1`.
* Append `3` and `1`. `queue = [9, 6, 3, 1]`.


* **Step 4, 5, 6, 7:**
* Pop `9`, `6`, `3`, `1` one by one. Each has `left = None` and `right = None`, so swapping changes nothing, and no children are added.
* `queue` becomes empty `[]`.


* **Final Result Tree Structure:**

```text
Inverted:
       4
     /   \
    7     2
   / \   / \
  9   6 3   1

```

---

### 5. Complexity Analysis

#### DFS Complexity:

* **Time Complexity:** $O(N)$
* **Why?** We visit every node in the tree once to swap its pointers.


* **Space Complexity:** $O(H)$ where $H$ is the height of the tree.
* **Why?** The space is used by the call stack. For a balanced tree, $H = \log N$. For a completely skewed tree, $H = N$.



#### BFS Complexity:

* **Time Complexity:** $O(N)$
* **Why?** Each node is queued and dequeued exactly once.


* **Space Complexity:** $O(W)$ where $W$ is the maximum width of the tree.
* **Why?** The queue stores nodes at the widest level, which can hold up to $N / 2$ nodes in a full binary tree ($O(N)$ worst-case).



---

### 6. Quick Revision Summary (30-Second Recall)

* **Core Action:** Swap `node.left` and `node.right` at every node!
* **DFS Strategy:** Swap current pointers, then recurse left and right.
* **BFS Strategy:** Queue nodes, pop a node, swap its left and right children, then enqueue non-null children.

---
