# 437. Path Sum III

**Category:** NC150 | **Difficulty:** Medium | **Pattern:** Top-Down DFS / Prefix Sum + Hash Map Backtracking

---

### 1. The Problem Statement

* **Question:** Given the root of a binary tree and an integer `targetSum`, return the total number of paths where the sum of values along the path equals `targetSum`.
* **Constraint:** Paths **do not** need to start at the root or end at a leaf, but must travel strictly **downwards** (parent to child).

---

### 2. The Approach & Strategy: Prefix Sum + Hash Map

> **Crucial Insight:**
> This approach adapts the array pattern from **LeetCode 560: Subarray Sum Equals K** to binary trees.
> Instead of calculating path sums starting from every node ($\mathcal{O}(N^2)$ brute force), maintain a running **accumulated sum** from the root down to the current node and log its frequency in a hash map.
> At any node, the running sum is $\text{current\_sum}$. To check if a downward sub-path ending at this node sums to `targetSum`, rearrange the formula:
> $$\text{current\_sum} - \text{previous\_prefix\_sum} = \text{targetSum}$$
> 
> 
> $$\implies \mathbf{\text{needed\_prefix\_sum} = \text{current\_sum} - \text{targetSum}}$$
> 
> 
> If $\text{needed\_prefix\_sum}$ exists in the hash map, add its frequency count to the total path count in $\mathcal{O}(1)$ time.

#### The Hash Map Concept & Components

1. **Hash Map Key/Value Mapping:**
* **Key:** Prefix sum value encountered on the active branch.
* **Value:** Frequency of how many times that exact prefix sum appears on the path above.


2. **Initialization (`prefix_sum[0] = 1`):**
* If `current_sum == targetSum`, then $\text{needed\_prefix\_sum} = \text{current\_sum} - \text{targetSum} = 0$.
* Setting `prefix_sum[0] = 1` ensures paths starting directly at the root node are properly counted.


3. **Backtracking (`prefix_sum[current_sum] -= 1`):**
* Trees split into separate branches. Prefix sums accumulated along the left subtree are **invalid** for the right subtree.
* Decrementing `prefix_sum[current_sum]` after visiting both children removes the node's contribution before returning to the parent.



```text
                     (10)  [curr_sum = 10]
                    /    \
  [curr_sum = 15] (5)    (-3) [curr_sum = 7]  <-- Backtracking removes left path sums
                 /                            (15, 18...) before traversing right!
 [curr_sum = 18](3) 
                 ^
                 |-- (18 - 8 = 10) exists in map! Path 5 -> 3 matches targetSum (8).

```

---

### 3. Code & Line-by-Line Explanation

```python
from collections import defaultdict
from typing import Optional

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # Step 1: Initialize hash map storing frequency of path prefix sums
        prefix_sum = defaultdict(int)
        prefix_sum[0] = 1  # Base case: handle paths starting directly at root
        paths = 0

        def dfs(node: Optional[TreeNode], current_sum: int) -> None:
            nonlocal paths
            if not node:
                return

            # Step 2: Accumulate running sum along current path
            current_sum += node.val

            # Step 3: Check how many valid sub-paths end at current node
            paths += prefix_sum[current_sum - targetSum]

            # Step 4: Record current running sum into hash map
            prefix_sum[current_sum] += 1

            # Step 5: Recurse into left and right subtrees
            dfs(node.left, current_sum)
            dfs(node.right, current_sum)

            # Step 6: BACKTRACK — Remove current sum frequency before returning to parent
            prefix_sum[current_sum] -= 1

        dfs(root, 0)
        return paths

```

* **Line 7:** `prefix_sum[0] = 1` seeds the map to handle paths starting at the root.
* **Line 16:** `current_sum += node.val` updates running sum from root to current node.
* **Line 19:** `paths += prefix_sum[current_sum - targetSum]` adds the number of valid starting nodes above that form a valid sub-path ending at `node`.
* **Line 22:** `prefix_sum[current_sum] += 1` makes current path total available to child calls.
* **Line 29:** `prefix_sum[current_sum] -= 1` cleans up state so this node's sum doesn't bleed into sibling branches.

---

### 4. Step-by-Step Execution Walkthrough

Trace path: Root ($10$) $\rightarrow$ Node ($5$) $\rightarrow$ Node ($3$), with `targetSum = 8`

| Step / Node | `current_sum` | `needed_sum` (`current_sum - 8`) | Hash Map State (`prefix_sum`) | `paths` Count |
| --- | --- | --- | --- | --- |
| **Start** | $0$ | — | `{0: 1}` | $0$ |
| **Node 10** | $10$ | $10 - 8 = \mathbf{2}$ | `{0: 1, 10: 1}` | $0$ (2 not in map) |
| **Node 5** | $15$ | $15 - 8 = \mathbf{7}$ | `{0: 1, 10: 1, 15: 1}` | $0$ (7 not in map) |
| **Node 3** | $18$ | $18 - 8 = \mathbf{10}$ | `{0: 1, 10: 1, 15: 1, 18: 1}` | **$1$** (10 found! Path: $5 \rightarrow 3$) |
| **Backtrack 3** | $18$ | — | `{0: 1, 10: 1, 15: 1, 18: 0}` | $1$ |
| **Backtrack 5** | $15$ | — | `{0: 1, 10: 1, 15: 0, 18: 0}` | $1$ |

---

### 5. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Every node is visited once, and hash map operations run in $\mathcal{O}(1)$ time.
* **Space Complexity:** $\mathcal{O}(H)$ — Hash map stores at most $H$ entries (tree height) corresponding to active ancestors on the path stack ($\mathcal{O}(N)$ worst-case, $\mathcal{O}(\log N)$ balanced).

---

### 6. Quick Revision Summary (30-Second Recall)

* **Equation:** Look for `current_sum - targetSum` in map before registering `current_sum`.
* **Map Seed:** `prefix_sum[0] = 1` handles root-originating paths.
* **Backtracking:** Always execute `prefix_sum[current_sum] -= 1` post-recurse to prevent sibling cross-talk.

---
