# 100. Same Tree

**Category:** LC150 + NC150 | **Difficulty:** Easy

---

### 1. The Problem Statement

* **Question:** Given the root nodes of two binary trees `p` and `q`, write a function to check whether they are identical.
* **Simple Explanation:** Two trees are identical if they have the exact same shape and every corresponding node holds the exact same number. If one tree has a left node while the other doesn't, or if their values don't match, they are not the same.

---

### 2. The Approach & Strategy

#### Approach A: Recursive Depth-First Search (DFS)

* **How to Think About It:** Walk through both trees simultaneously node by node. For any pair of nodes `p` and `q`, check three things: Are both empty? Is one missing? Are their values equal? Then, recursively verify that their left branches match AND their right branches match.
* **Step-by-Step Logic:**
1. **Both Null Base Case:** If both `p` and `q` are `None`, return `True` (both trees ended at the same time).
2. **One Null Base Case:** If one is `None` while the other is not, return `False` (structural mismatch).
3. **Value Check:** If `p.val != q.val`, return `False` (value mismatch).
4. **Recurse:** Check if `isSameTree(p.left, q.left)` is `True` **and** `isSameTree(p.right, q.right)` is `True`.



#### Approach B: Iterative Traversal (Queue / Stack)

* **How to Think About It:** Compare nodes in pairs using an explicit queue (or stack). Store pairs `(p_node, q_node)` and pop them to perform the exact same structural and value checks.
* **Step-by-Step Logic:**
1. Initialize a queue with the tuple `(p, q)`.
2. While the queue is not empty:
* Pop a pair `(p, q)`.
* If both `p` and `q` are `None`, continue to the next iteration (this branch matches so far).
* If only one is `None`, or if `p.val != q.val`, return `False` immediately.
* Enqueue the child pairs: `(p.left, q.left)` and `(p.right, q.right)`.


3. If the loop finishes without returning `False`, return `True`.



---

### 3. Code & Line-by-Line Explanation

#### Solution A: Recursive DFS

```python
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # 1. Both nodes are null -> structural match at leaf level
        if not p and not q:
            return True

        # 2. One is null and the other isn't -> structural mismatch
        if not p or not q:
            return False

        # 3. Values do not match -> value mismatch
        if p.val != q.val:
            return False

        # 4. Check left subtrees AND right subtrees
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)

```

* **Line 4 - 5:** Base case 1. If both pointers reach `None` together, this branch is structurally identical at this point, so return `True`.
* **Line 8 - 9:** Base case 2. If line 4 didn't trigger, but one pointer is `None`, it means one tree is longer or has a branch the other lacks. Return `False`.
* **Line 12 - 13:** Base case 3. If both exist, make sure their values match. If they differ, return `False`.
* **Line 16:** Recursively check both left children together AND both right children together. Both subtrees must return `True` for the result to be `True`.

---

#### Solution B: Iterative BFS/DFS Traversal

```python
from collections import deque

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        queue = deque([(p, q)])

        while queue:
            curr_p, curr_q = queue.popleft()

            # Both nodes are null -> continue to next pair in queue
            if not curr_p and not curr_q:
                continue
            
            # One node is null -> structural mismatch
            if not curr_p or not curr_q:
                return False

            # Value mismatch
            if curr_p.val != curr_q.val:
                return False
            
            # Append corresponding children pairs to keep comparing them together
            queue.append((curr_p.left, curr_q.left))
            queue.append((curr_p.right, curr_q.right))

        return True

```

* **Line 6:** Creates a queue storing tuples of corresponding nodes `(p, q)`.
* **Line 9:** Pops a pair from the queue to process. *(Note: Using `.popleft()` performs a BFS level-by-level comparison, whereas `.pop()` acts as an iterative stack).*
* **Line 12 - 13:** If both nodes are `None`, this specific branch ended validly. `continue` moves to the next pair in the queue.
* **Line 16 - 17:** If one node exists but the other is `None`, the trees are not identical. Return `False`.
* **Line 20 - 21:** If values don't match, return `False`.
* **Line 24 - 25:** Enqueues left children together and right children together so they will be compared in future loop rounds.
* **Line 27:** Returns `True` if all pairs processed successfully without encountering a mismatch.

---

### 4. Step-by-Step Dry Run

Let's use **Example 3**: `p = [1, 2, 1]`, `q = [1, 1, 2]`

```text
  Tree p:        Tree q:
     1              1
    / \            / \
   2   1          1   2

```

#### Dry Run A: Recursive DFS

1. **`isSameTree(p=1, q=1)`**:
* Neither is `None`. Values match (`1 == 1`).
* Recurse on left children: **`isSameTree(p.left=2, q.left=1)`**:
* Neither is `None`.
* Value check: `p.val (2) != q.val (1)`.
* Returns `False`.




2. **`isSameTree(p=1, q=1)`** receives `False` from its left call. Short-circuits and immediately returns `False`.
3. **Final Answer:** `False`.

---

#### Dry Run B: Iterative BFS

* **Initial State:** `queue = [(1, 1)]`
* **Iteration 1:**
* Pop `(1, 1)`. Both exist, `1 == 1`.
* Enqueue `(p.left=2, q.left=1)` and `(p.right=1, q.right=2)`.
* `queue = [(2, 1), (1, 2)]`


* **Iteration 2:**
* Pop `(2, 1)`.
* Both exist.
* Check values: `2 != 1` -> Mismatch found!
* Immediately return `False`.


* **Final Answer:** `False`.

---

### 5. Complexity Analysis

#### DFS Complexity:

* **Time Complexity:** $O(\min(N, M))$ where $N$ and $M$ are the number of nodes in trees `p` and `q`.
* **Why?** We visit nodes in parallel. The recursion stops as soon as a mismatch is found or when the smaller tree terminates.


* **Space Complexity:** $O(\min(H_1, H_2))$ where $H_1$ and $H_2$ are the heights of the trees.
* **Why?** Memory is consumed by the recursion call stack, which goes as deep as the height of the smaller tree.



#### BFS Complexity:

* **Time Complexity:** $O(\min(N, M))$
* **Why?** Each pair is enqueued and dequeued at most once until a mismatch occurs or all nodes are checked.


* **Space Complexity:** $O(\min(W_1, W_2))$ where $W$ is the maximum width of the trees.
* **Why?** The queue stores pairs of nodes at the current level, bounded by the width of the smaller tree ($O(N)$ worst-case).



---

### 6. Quick Revision Summary (30-Second Recall)

* **Check Triple:** For every pair of nodes `(p, q)`:
1. Both `None` $\rightarrow$ valid (`True` / `continue`).
2. One `None` $\rightarrow$ invalid (`False`).
3. `p.val != q.val` $\rightarrow$ invalid (`False`).


* **DFS Strategy:** Compare current pair, then `return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)`.
* **BFS Strategy:** Enqueue pairs `(p, q)`, process pair by pair, and enqueue `(p.left, q.left)` and `(p.right, q.right)`.

---
