# 104. Maximum Depth of Binary Tree

**Category:** LC150 + NC150 | **Difficulty:** Easy

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree, return its maximum depth (the total number of nodes along the longest path from the top root node down to the farthest bottom leaf node).
* **Simple Explanation:** Imagine a tree as a multi-story building where the root is the top floor (Level 1). You want to count how many floors down the building goes. If there are no nodes at all (empty tree), the depth is 0.

---

### 2. The Approach & Strategy

We can solve this problem using two different approaches:

#### Approach A: Recursive Depth-First Search (DFS) — *Structural DFS*

* **How to Think About It:** Ask your left child, "What is your max depth?" Ask your right child, "What is your max depth?" Take whichever answer is larger and add 1 (for yourself).
* **Step-by-Step Logic:**
1. **Base Case:** If the current node is `None` (empty space), return `0`.
2. **Recursive Call:** Recursively calculate `maxDepth(root.left)` and `maxDepth(root.right)`.
3. **Combine Step:** Take the maximum of the two subtree depths and add `1` to account for the current node.



#### Approach B: Iterative Breadth-First Search (BFS) — *Level-Order Traversal*

* **How to Think About It:** Explore the tree floor-by-floor (level-by-level). Count how many complete levels you process until there are no nodes left.
* **Step-by-Step Logic:**
1. **Base Case:** If the root is `None`, return `0`.
2. **Initialization:** Put the root into a queue and set `depth = 0`.
3. **Level Processing Loop:** While the queue is not empty:
* Increment `depth` by `1`.
* Take a snapshot of the queue size (`len(queue)`). This tells you how many nodes belong strictly to the current level.
* Pop all nodes of the current level out of the queue and push their valid left and right children into the queue for the next level.


4. **Return:** When the queue becomes empty, return `depth`.



---

### 3. Code & Line-by-Line Explanation

#### Solution A: Recursive DFS

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        return 1 + max(left_depth, right_depth)

```

* **Line 3:** Checks if `root` is `None`. If an empty branch is reached, it returns `0` because an empty tree has no depth.
* **Line 6:** Recurses down the left subtree to find its maximum height.
* **Line 7:** Recurses down the right subtree to find its maximum height.
* **Line 9:** Takes the larger value between left and right subtrees and adds `1` (representing the current node) to send the answer back up to the parent node.

---

#### Solution B: Iterative BFS

```python
from collections import deque

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        queue = deque([root])
        depth = 0

        while queue:
            depth += 1
            for _ in range(len(queue)):
                node = queue.popleft()

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                    
        return depth

```

* **Line 5 - 6:** Handles the empty tree base case.
* **Line 8:** Initializes a double-ended queue (`deque`) containing the `root` node.
* **Line 9:** Initializes the `depth` counter to `0`.
* **Line 11:** Loops as long as there are nodes waiting to be processed in the queue.
* **Line 12:** Increments `depth` by `1` every time a new level begins.
* **Line 13:** `len(queue)` captures the exact number of nodes on this specific level. The `for` loop runs exactly this many times so we don't accidentally mix in children from the next level.
* **Line 14:** Pops the leftmost node from the queue to process it.
* **Line 16 - 19:** If the popped node has left or right children, they are added to the back of the queue to be processed on the next level round.
* **Line 21:** Returns the accumulated count of levels once all nodes have been processed.

---

### 4. Step-by-Step Dry Run

Let's use **Example 1**: `root = [3, 9, 20, null, null, 15, 7]`

```text
       3
      / \
     9   20
        /  \
       15   7

```

#### Dry Run A: Recursive DFS

1. **`maxDepth(3)`** is called.
* Calls **`maxDepth(9)`** (left child).
* `maxDepth(9.left)` -> `maxDepth(None)` returns `0`.
* `maxDepth(9.right)` -> `maxDepth(None)` returns `0`.
* `maxDepth(9)` returns `1 + max(0, 0) = 1`.


* Calls **`maxDepth(20)`** (right child).
* Calls **`maxDepth(15)`** (left child of 20).
* `maxDepth(15.left)` -> `0`, `maxDepth(15.right)` -> `0`.
* `maxDepth(15)` returns `1 + max(0, 0) = 1`.


* Calls **`maxDepth(7)`** (right child of 20).
* `maxDepth(7.left)` -> `0`, `maxDepth(7.right)` -> `0`.
* `maxDepth(7)` returns `1 + max(0, 0) = 1`.


* `maxDepth(20)` returns `1 + max(1, 1) = 2`.




2. **`maxDepth(3)`** combines results: `1 + max(left_depth=1, right_depth=2) = 1 + 2 = 3`.
3. **Final Result:** `3`.

---

#### Dry Run B: Iterative BFS

* **Initial State:** `queue = [3]`, `depth = 0`.
* **Level 1 Iteration:**
* `depth` becomes `1`.
* Snapshot level size = `1` (Node `3`).
* Pop `3`. Append children `9` and `20`.
* `queue` is now `[9, 20]`.


* **Level 2 Iteration:**
* `depth` becomes `2`.
* Snapshot level size = `2` (Nodes `9` and `20`).
* **Pop `9`:** No children to append.
* **Pop `20`:** Append children `15` and `7`.
* `queue` is now `[15, 7]`.


* **Level 3 Iteration:**
* `depth` becomes `3`.
* Snapshot level size = `2` (Nodes `15` and `7`).
* **Pop `15`:** No children to append.
* **Pop `7`:** No children to append.
* `queue` is now empty `[]`.


* **End of Loop:** `queue` is empty.
* **Final Result:** Returns `depth = 3`.

---

### 5. Complexity Analysis

#### DFS Complexity:

* **Time Complexity:** $O(N)$
* **Why?** We visit every node in the binary tree exactly once. If there are $N$ nodes, we make $N$ recursive calls.


* **Space Complexity:** $O(H)$ where $H$ is the height of the tree.
* **Why?** Memory is consumed by the recursion call stack. In a balanced tree, $H = \log N$. In a completely skewed tree (e.g., a linked list shape), $H = N$, making the worst-case space complexity $O(N)$.



#### BFS Complexity:

* **Time Complexity:** $O(N)$
* **Why?** Every node is pushed into and popped from the queue exactly once.


* **Space Complexity:** $O(W)$ where $W$ is the maximum width of the tree.
* **Why?** Memory is consumed by the `queue`. In a full binary tree, the bottom leaf level contains roughly $N / 2$ nodes, making the worst-case space complexity $O(N)$.



---

### 6. Quick Revision Summary (30-Second Recall)

* **DFS Mindset:** Depth of a tree = `1 + max(depth(left), depth(right))`. Use recursion to post-order traverse down and pass height upward.
* **BFS Mindset:** Count the levels! Use a queue with `for _ in range(len(queue))` to process nodes one horizontal level at a time and increment `depth` per outer loop.

---
