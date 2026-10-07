# 337. House Robber III

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Bottom-Up DFS / Tree DP

---

### 1. The Problem Statement

* **Question:** Given a binary tree representing houses, return the maximum amount of money you can rob without robbing **two directly-linked houses** (parent and child).
* **Constraint:** If you rob a parent house, you **cannot** rob its immediate left or right children.
* **Goal:** Maximize total stolen value across the tree.

---

### 2. The Approach & Strategy

> **Crucial Insight:**
> At any node $N$, we have exactly two choices:
> 1. **Rob Node $N$ (`withRoot`):** We gain $N.\text{val}$, but we **must skip** both immediate child nodes. Thus, we must take the "without child" values from both subtrees.
> 2. **Skip Node $N$ (`withoutRoot`):** We get $0$ from $N$, which leaves us free to either **rob or skip** each child node independently depending on which option yields more money.
> 
> 

#### Returning a Pair `(withRoot, withoutRoot)`

Instead of making redundant recursive calls or storing state in a separate hashmap, each node returns a tuple of 2 values to its parent:

* `withRoot`: Max money obtainable from this subtree **if we ROB this node**.
* `withoutRoot`: Max money obtainable from this subtree **if we SKIP this node**.

```text
                     ( Node N )
                    /          \
            ( Left Child )   ( Right Child )
            (withL, withoutL) (withR, withoutR)

==================================================================
withRoot    = N.val + withoutL + withoutR
withoutRoot = max(withL, withoutL) + max(withR, withoutR)
==================================================================

```

---

### 3. Code & Line-by-Line Explanation

```python
class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:

        def dfs(node: Optional[TreeNode]) -> tuple[int, int]:
            # Base Case: Empty house yields (0 money if robbed, 0 if skipped)
            if not node:
                return (0, 0)

            # Post-Order Traversal: Get decision pairs from left & right subtrees
            leftPair = dfs(node.left)    # (withLeft, withoutLeft)
            rightPair = dfs(node.right)  # (withRight, withoutRight)

            # Option 1: Rob current node -> MUST skip left and right children
            withRoot = node.val + leftPair[1] + rightPair[1]

            # Option 2: Skip current node -> Pick best option for each child independently
            withoutRoot = max(leftPair) + max(rightPair)

            return (withRoot, withoutRoot)

        # Final answer is the max of robbing or skipping the main root
        return max(dfs(root))

```

* **Line 6:** Base case returns `(0, 0)` for `None` pointers.
* **Line 10–11:** Post-order DFS fetches child decisions first (`leftPair` and `rightPair`).
* **Line 14:** `withRoot`: Takes current node's value + `leftPair[1]` (`withoutLeft`) + `rightPair[1]` (`withoutRight`).
* **Line 17:** `withoutRoot`: We skip `node`, so for the left branch we pick `max(leftPair[0], leftPair[1])` and do the same for the right branch.
* **Line 19:** Returns tuple `(withRoot, withoutRoot)` up to the parent caller.
* **Line 22:** Unpacks and returns `max(withRoot, withoutRoot)` at the tree root.

---

### 4. Step-by-Step Dry Run

Let's trace **Example 1**: `root = [3, 2, 3, null, 3, null, 1]`

```text
              3
             / \
            2   3
             \   \
              3   1

```

* **Leaves (`Node 3` under 2, `Node 1` under 3):**
* `dfs(Leaf 3)` $\rightarrow$ `with = 3 + 0 + 0 = 3`, `without = 0` $\rightarrow$ Returns `(3, 0)`
* `dfs(Leaf 1)` $\rightarrow$ `with = 1 + 0 + 0 = 1`, `without = 0` $\rightarrow$ Returns `(1, 0)`


* **`dfs(Node 2)`** (Left subtree):
* `leftPair = (0, 0)`, `rightPair = (3, 0)`
* `withRoot = 2 + 0 + 0 = 2`
* `withoutRoot = max(0, 0) + max(3, 0) = 3`
* Returns `(2, 3)`


* **`dfs(Node 3)`** (Right subtree):
* `leftPair = (0, 0)`, `rightPair = (1, 0)`
* `withRoot = 3 + 0 + 0 = 3`
* `withoutRoot = max(0, 0) + max(1, 0) = 1`
* Returns `(3, 1)`


* **`dfs(Root 3)`**:
* `leftPair = (2, 3)`, `rightPair = (3, 1)`
* `withRoot = 3 + leftPair[1] (3) + rightPair[1] (1) = 7`
* `withoutRoot = max(2, 3) + max(3, 1) = 3 + 3 = 6`
* Returns `(7, 6)`


* **Final Result:** `max(7, 6) = 7`.

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited exactly once in a single post-order traversal.
* **Space Complexity:** $\mathcal{O}(H)$ — Stack depth proportional to tree height $H$ ($\mathcal{O}(N)$ worst case for skewed trees, $\mathcal{O}(\log N)$ for balanced trees).

---

### 6. Quick Revision Summary (30-Second Recall)

* **Return State:** Return `(rob_this_node, skip_this_node)` tuple at every level.
* **Rob Formula:** `N.val + skip_left + skip_right`
* **Skip Formula:** `max(rob_left, skip_left) + max(rob_right, skip_right)`

---
