# Concept 01 — What Is a Tree?

> Start here. This file gives you the vocabulary and the mental picture every other file assumes.

---

## Story-Mode Intuition

Think of a **company org chart**.

- At the very top there is **one CEO**. That's the **root**.
- The CEO has a few **direct reports**. Each of them has their own direct reports. And so on.
- Everyone (except the CEO) has **exactly one boss**.
- The people at the bottom with nobody reporting to them are the **leaves**.
- There are **no loops** — you can't be your own great-grandboss. Follow "boss of" upward and you always end at the CEO.

A **tree** is exactly this shape: one starting node at the top, every other node hangs below exactly one parent, and there are no cycles.

A **binary tree** just adds one rule: **each node has at most two children**, and we specifically call them `left` and `right`. Left and right are *different* — swapping them gives a different tree. (In the org chart analogy: imagine each manager has a "left hire" and a "right hire" desk, and which desk someone sits at matters.)

---

## The Mental Model

### Picture it top-down

```
            10          <- root (depth 0)
           /  \
          5    15       <- depth 1
         / \     \
        3   7    20     <- depth 2  (3, 7, 20 are leaves)
```

- **Node**: one box. Holds a value (`10`) and two arrows: `left` and `right`.
- **Edge**: one arrow from a parent to a child.
- **Root**: the single node with no parent (`10`). The whole tree is identified by its root — "give me the tree" means "give me the root node."
- **Leaf**: a node with **no children** — both `left` and `right` are `None` (`3`, `7`, `20`).
- **Parent / child**: `5` is the parent of `3` and `7`. `3` and `7` are children of `5`.
- **Subtree**: any node plus everything hanging below it is itself a complete little tree. The node `5` is the root of the subtree `{5, 3, 7}`. **This is the key idea** — every child is the root of a smaller tree, so anything you can do to "a tree" you can do to each child.
- **Depth of a node**: how many edges from the root down to it. Root is depth 0.
- **Height of the tree**: the depth of the deepest leaf = the length of the longest root-to-leaf chain. The tree above has height 2.

### The "missing child" is a real thing

Node `15` has a `right` child (`20`) but its `left` is `None`. `None` is not an error — it's how the tree says "nothing here." Every recursive function you write will check for `None` **first**.

### Why recursion fits trees perfectly

A tree is defined *in terms of itself*: "a tree is a root node whose `left` and `right` are each **either `None` or another tree**."

That self-reference is why nearly every solution looks like:

1. If the node is `None`, return the "empty" answer.
2. Otherwise, get the answer for the `left` subtree and the answer for the `right` subtree (by calling the same function).
3. Combine those two answers with the current node's value.

You solve the whole tree by trusting the function to solve the smaller trees. (Concept 02 goes deep on this trust.)

### Two ways to walk a tree

- **DFS (depth-first search)**: go as deep as possible down one branch before backing up. This is what plain recursion does naturally. Uses a stack (the call stack). → Concepts 03, 04.
- **BFS (breadth-first search)**: visit the tree level by level, top to bottom, left to right. Uses a queue. → Concept 05.

### Shapes you'll be asked about

| Shape | Meaning | Height |
|---|---|---|
| **Balanced** | every node's two sides differ in height by ≤ 1 | ≈ log₂(N) |
| **Complete** | every level full except possibly the last, which fills left-to-right | ≈ log₂(N) |
| **Perfect / full-and-complete** | every level completely full | exactly log₂(N+1) − 1 |
| **Skewed / degenerate** | every node has only one child — a straight line | N − 1 |

`N` = number of nodes, `H` = height. A balanced tree of a million nodes is only ~20 tall. A skewed tree of a million nodes is a million tall (and will blow the recursion stack). This is why "is it balanced?" matters so much in complexity analysis.

---

## Clean Python Template

### The node (memorize this — every file reuses it verbatim)

```python
from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right
```

Plain English:
- `class TreeNode:` — define a new kind of object called `TreeNode`.
- `def __init__(self, ...)` — the setup routine that runs when you write `TreeNode(10)`.
- `val: int = 0` — this node carries a number; if you don't pass one, it defaults to `0`.
- `left: Optional["TreeNode"] = None` — a slot for the left child. `Optional[...]` means "a TreeNode **or** `None`." Defaults to `None` (no child). The quotes around `"TreeNode"` are just Python needing to refer to a class while still defining it.
- The three `self.x = x` lines copy the passed-in values onto this node so we can read them later as `node.val`, `node.left`, `node.right`.

### Building a tree by hand

```python
#        10
#       /  \
#      5    15
root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(15)
```

### The `build_tree` helper (used in every problem file's test block)

It takes a **level-order list** — read top-to-bottom, left-to-right, using `None` for a missing child — and wires up the nodes for you.

```python
from collections import deque
from typing import Optional


def build_tree(values: list[Optional[int]]) -> Optional[TreeNode]:
    """Build a binary tree from a level-order list. None marks a missing child.

    Example: [10, 5, 15, 3, 7, None, 20] builds
                10
               /  \
              5    15
             / \     \
            3   7     20
    """
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    index = 1

    while queue and index < len(values):
        curr_node = queue.popleft()

        if index < len(values) and values[index] is not None:
            curr_node.left = TreeNode(values[index])
            queue.append(curr_node.left)
        index += 1

        if index < len(values) and values[index] is not None:
            curr_node.right = TreeNode(values[index])
            queue.append(curr_node.right)
        index += 1

    return root
```

How it works in plain English:
- If the list is empty or its first item is `None`, there's no tree — return `None`.
- Make the root from the first value. Put it in a queue of "nodes still waiting for their children."
- `index` points at the next value to hand out, starting at position 1.
- Repeatedly: take the front node from the queue. The next list value is its left child (unless it's `None`); the value after that is its right child. Any real child we create also goes into the queue, because it will need children of its own later.
- Stop when we run out of list.

### The traversal skeleton (the shape of ~80% of solutions)

```python
def solve(node: Optional[TreeNode]) -> SomeType:
    # 1. Base case: nothing here.
    if node is None:
        return empty_answer

    # 2. Solve the two smaller trees.
    left_answer = solve(node.left)
    right_answer = solve(node.right)

    # 3. Combine with this node.
    return combine(node.val, left_answer, right_answer)
```

Every problem in Topic 1 is just this skeleton with different choices for `empty_answer` and `combine`. Concept 02 explains *why* trusting step 2 is safe.
