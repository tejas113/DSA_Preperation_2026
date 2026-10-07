# Concept 02 — Recursion & the Call Stack

> Needed for: Problem 1 (Maximum Depth) and essentially every tree problem after it.
> Read Concept 01 first for the tree vocabulary.

---

## Story-Mode Intuition

You're a manager and your boss asks: **"How many people are in your whole department, top to bottom?"**

You don't personally count all 400 people. Instead you walk to each of your **direct reports** and ask them the *exact same question*: "How many people are in your whole sub-department?" You wait. Each of them does the same thing — asks *their* reports — and so on. Eventually the question reaches someone with **no reports at all**; that person instantly answers "just me, 1." Those 1s travel back up. Each manager adds the numbers their reports handed back, plus 1 for themselves, and passes that total up to their own boss. Finally you get numbers back from your direct reports, add them up plus 1 for yourself, and answer your boss.

That is **recursion**:

- **You solve a big problem by asking smaller copies of yourself to solve smaller versions**, then combining their answers.
- **You trust** that each smaller copy returns the correct answer for its piece. You don't follow them down the hierarchy in your head.
- There must be a **smallest case that answers immediately without asking anyone** (the person with no reports). That's the **base case**. Without it, the questions go down forever.

A tree is *built* out of smaller trees (every child is the root of a subtree — Concept 01), so this "ask the smaller versions" approach fits perfectly.

---

## The Mental Model

### A recursive function has exactly three parts

```python
def count_people(manager):
    # 1. BASE CASE — the smallest input, answered with no further calls.
    if manager is None:
        return 0

    # 2. RECURSE — ask the smaller versions of yourself.
    left_count = count_people(manager.left)
    right_count = count_people(manager.right)

    # 3. COMBINE — build this level's answer from the smaller answers.
    return left_count + right_count + 1
```

- **Base case first, always.** For trees it's almost always `if node is None: return <the "nothing" answer>`. The "nothing" answer is `0` for a count, `[]` for a list, `True` for "all-match" checks, `None` for "not found."
- **Recurse.** Call the same function on `node.left` and on `node.right`. Store each result in a clearly named variable.
- **Combine.** Merge `left` result + `right` result + something about the current node.

If you can fill in those three blanks, you've solved the problem. **You never trace the full recursion by hand** — you trust step 2.

### The call stack: where "wait for the answer" actually lives

The computer needs to remember every unfinished question. It uses a **stack** — think of a stack of sticky notes, newest on top.

Walk through this tree with `count_people`:

```
        A
       / \
      B   C
     /
    D
```

1. Call `count_people(A)`. It needs `left_count`, so it calls `count_people(B)`.
   Sticky note placed: *"A is waiting on B (and still owes a call to C)."*
2. `count_people(B)` calls `count_people(D)`.
   Sticky note: *"B is waiting on D (and still owes a call to B.right = None)."*
3. `count_people(D)` calls `count_people(None)` → returns `0`. Calls `count_people(None)` again → `0`.
   `D` combines: `0 + 0 + 1 = 1`. **Returns 1.** Its sticky note is torn off.
4. Back in `B`: `left_count = 1`. Now `B` calls `count_people(B.right)` = `count_people(None)` → `0`.
   `B` combines: `1 + 0 + 1 = 2`. **Returns 2.** Sticky note torn off.
5. Back in `A`: `left_count = 2`. Now `A` calls `count_people(C)` → (C has no children) returns `1`.
   `A` combines: `2 + 1 + 1 = 4`. **Returns 4.** Done.

The stack **grew** as we dove down (A → B → D), reached its tallest at 3 notes, then **shrank** as answers came back. The tallest the stack ever gets = the **deepest path in the tree** = the tree's **height H**.

```
time ──►
stack   [A]      [A,B]    [A,B,D]   [A,B]   [A]     []
depth    1    →    2    →    3    →   2   →   1   →  0
                          (tallest = H)
```

### Why this controls your space complexity

Each sticky note (each **stack frame**) uses a bit of memory. The most notes that exist at once is `H`. So a recursive tree solution uses **O(H) extra space**, even if it returns nothing.

- **Balanced tree:** H ≈ log₂(N). A million nodes → ~20 frames. Cheap.
- **Skewed tree** (a straight line of nodes): H = N. A million nodes → a million frames → Python raises `RecursionError` (its default limit is ~1000). This is the #1 thing an interviewer probes: *"what if the tree is a straight line?"*

### The two directions information can flow

This distinction (full guide in Concept 06) starts here:

| | How it works | Example |
|---|---|---|
| **Down (top-down)** | pass data *into* the recursive call as an argument | `dfs(node.left, depth + 1)` — the current depth travels down |
| **Up (bottom-up)** | `return` data *out of* the recursive call | `return 1 + max(left_depth, right_depth)` — the height travels up |

`count_people` above is **bottom-up**: nothing is passed down; the count is built up from the returns.

### Recursion vs. iteration

Anything recursive can be rewritten with an explicit stack or queue that *you* manage (Concepts 04 and 05). Reasons you'd do that in an interview:

- The tree might be deep enough to overflow the call stack.
- You want O(1) space (Morris traversal).
- You're building an iterator that must pause and resume between calls (Problem 24).

But recursion is shorter and clearer, so **write the recursive version first**, then convert only if asked.

---

## Clean Python Template

### The universal tree-recursion skeleton

```python
from typing import Optional


def solve(node: Optional[TreeNode]) -> ResultType:
    # 1. BASE CASE: an empty spot contributes the "nothing" answer.
    if node is None:
        return NOTHING          # 0 | [] | True | None | float("-inf") ...

    # 2. RECURSE: trust these to return correct answers for the subtrees.
    left_result = solve(node.left)
    right_result = solve(node.right)

    # 3. COMBINE: this node's answer, built from the two sub-answers.
    return combine(node.val, left_result, right_result)
```

### Filled in for "maximum depth" (previews Problem 1)

```python
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # BASE CASE: an empty tree is 0 levels tall.
        if root is None:
            return 0

        # RECURSE: how tall is each side?
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)

        # COMBINE: the taller side, plus this node's own level.
        return 1 + max(left_depth, right_depth)
```

Line by line, in plain English:

- `if root is None: return 0` — if there's no node here, this branch adds no height. This is the stopping point that makes the whole thing terminate.
- `left_depth = self.maxDepth(root.left)` — ask the same function for the height of the left subtree. Trust the number it returns.
- `right_depth = self.maxDepth(root.right)` — same for the right subtree.
- `return 1 + max(left_depth, right_depth)` — the height *through this node* is the taller child's height plus one step down to reach this node.

### When you need a helper (to carry data *down*, or to track a global best)

The public method can't easily take extra bookkeeping arguments, so nest a helper:

```python
from typing import Optional


class Solution:
    def deepest_value(self, root: Optional[TreeNode]) -> int:
        best_depth = -1
        best_value = 0

        def dfs(node: Optional[TreeNode], depth: int) -> None:
            nonlocal best_depth, best_value
            if node is None:
                return
            if depth > best_depth:            # first node we reach at this depth
                best_depth = depth
                best_value = node.val
            dfs(node.left, depth + 1)         # depth travels DOWN as an argument
            dfs(node.right, depth + 1)

        dfs(root, 0)
        return best_value
```

- `def dfs(node, depth)` — a function inside a function. It can see `best_depth` / `best_value` from the outer scope.
- `nonlocal best_depth, best_value` — "when I assign to these names, change the outer ones; don't make new local copies."
- `dfs(node.left, depth + 1)` — the `+ 1` is the top-down part: each level down passes a larger depth.
- `dfs(root, 0)` kicks it off; the answer is read from the outer variable afterward.

### Base-case cheat sheet

| The function returns... | Base case (`node is None`) returns |
|---|---|
| a count / a height / a sum | `0` |
| a max-so-far that must lose to any real value | `float("-inf")` |
| a list of values | `[]` |
| "do all nodes satisfy X?" | `True` (an empty tree satisfies everything) |
| "does any node satisfy X?" / "find the node" | `False` / `None` |
| a rebuilt subtree | `None` |
