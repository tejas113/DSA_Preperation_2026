# 987. Vertical Order Traversal of a Binary Tree

**Category:** NC150 | **Difficulty:** Hard | **Pattern:** BFS with Coordinate Mapping & Multi-Level Sorting

---

### 1. Visualizing Coordinate Assignment (The Diagonal / Coordinate Math)

When traversing the tree, every node gets a 2D coordinate `(row, col)`:

* **Root** starts at `(0, 0)` (row = 0, col = 0).
* Moving **Left**: `row` increases by 1 (goes down), `col` decreases by 1 (goes left). $\rightarrow (row + 1, col - 1)$
* Moving **Right**: `row` increases by 1 (goes down), `col` increases by 1 (goes right). $\rightarrow (row + 1, col + 1)$

```text
                  (3) [row 0, col 0]
                /     \
    [row 1, col -1]   [row 1, col +1]
         (9)               (20)
                          /    \
            [row 2, col 0]    [row 2, col +2]
                 (15)              (7)

```

---

### 2. How the Dictionary & Tuples are Formed

During BFS, you collect each node into `nodes[col]` as a tuple: `(row, node.val)`.

For **Example 1**:

* `nodes[-1]` $= [(1, 9)]$
* `nodes[0]` $= [(0, 3), (2, 15)]$
* `nodes[1]` $= [(1, 20)]$
* `nodes[2]` $= [(2, 7)]$

Notice that inside `nodes[col]`, you have pairs of `(row, node_value)`.

---

### 3. Demystifying `sorted(nodes[col], key=sort_key)`

Python tuples naturally compare element by element from left to right. When you sort list items of shape `(row, val)`, Python evaluates them using the following rules:

1. **First Priority (`row`):** Top-to-bottom ordering. A node with a smaller row (higher in the tree) comes first.
2. **Second Priority (`val`):** If two nodes have the **same `row` and same `col**` (overlapping in the same physical cell), they tie on `row`, so Python falls back to comparing `val` in ascending order.

#### Writing it explicitly vs. Using standard Tuple Sorting

Your custom key function:

```python
def sort_key(item):
    row = item[0]
    val = item[1]
    return (row, val)

column_nodes = sorted(nodes[col], key=sort_key)

```

returns a tuple `(row, val)`. Python compares these returned tuples automatically:

* Comparing `(1, 6)` vs `(1, 5)`:
* Check 1st element (`row`): `1 == 1` (Tie!)
* Check 2nd element (`val`): `5 < 6` $\rightarrow$ `(1, 5)` comes before `(1, 6)`.



> **Python Pro Tip:** Because your tuples inside `nodes[col]` are already formatted as `(row, val)`, calling standard `sorted(nodes[col])` does the **exact same thing** without needing `key=sort_key`!

---

### 4. Step-by-Step Dry Run (Focusing on Overlapping Nodes)

Let's trace **Example 2**: `root = [1, 2, 3, 4, 5, 6, 7]`

```text
                  (1) (0,0)
               /             \
       (2) (1,-1)           (3) (1,1)
      /          \         /         \
  (4) (2,-2)  (5) (2,0) (6) (2,0)  (7) (2,2)

```

#### Step 1: Queue Collection (BFS Traversal)

Pop order from Queue:

1. `(1, col=0, row=0)` $\rightarrow$ `nodes[0].append((0, 1))`
2. `(2, col=-1, row=1)` $\rightarrow$ `nodes[-1].append((1, 2))`
3. `(3, col=1, row=1)` $\rightarrow$ `nodes[1].append((1, 3))`
4. `(4, col=-2, row=2)` $\rightarrow$ `nodes[-2].append((2, 4))`
5. `(5, col=0, row=2)` $\rightarrow$ `nodes[0].append((2, 5))`  *(Overlap at col 0!)*
6. `(6, col=0, row=2)` $\rightarrow$ `nodes[0].append((2, 6))`  *(Overlap at col 0!)*
7. `(7, col=2, row=2)` $\rightarrow$ `nodes[2].append((2, 7))`

#### Step 2: Unsorted State in `nodes[0]`

```python
nodes[0] = [(0, 1), (2, 5), (2, 6)] 
# Note: What if 6 was added before 5? nodes[0] would be [(0, 1), (2, 6), (2, 5)]

```

#### Step 3: Sorting `nodes[0]`

Executing `column_nodes = sorted(nodes[0], key=sort_key)`:

* Compare `(0, 1)` vs `(2, 5)` $\rightarrow$ `row 0 < row 2` $\rightarrow$ `(0, 1)` goes first.
* Compare `(2, 6)` vs `(2, 5)`:
* `row` comparison: `2 == 2` (Tie!).
* `val` comparison: `5 < 6` $\rightarrow$ `(2, 5)` goes before `(2, 6)`.



Sorted result for Column 0:
`[(0, 1), (2, 5), (2, 6)]`

#### Step 4: Extracting Values Only

Loop over `column_nodes` to pull out `item[1]` (`val`):
`current_column_values = [1, 5, 6]`

---

### 5. Cleaned & Pythonic Version

```python
from collections import defaultdict, deque
from typing import Optional, List

class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        nodes = defaultdict(list)
        queue = deque([(root, 0, 0)])  # (node, col, row)

        while queue:
            node, col, row = queue.popleft()
            nodes[col].append((row, node.val))

            if node.left:
                queue.append((node.left, col - 1, row + 1))
            if node.right:
                queue.append((node.right, col + 1, row + 1))

        ans = []
        # Process columns from leftmost to rightmost
        for col in sorted(nodes.keys()):
            # Sorting directly on (row, val) tuples:
            # Primary sort: row ascending (top to bottom)
            # Secondary sort: val ascending (smaller values first on tie)
            column_nodes = sorted(nodes[col])
            
            # Extract just the values
            ans.append([val for row, val in column_nodes])

        return ans

```
