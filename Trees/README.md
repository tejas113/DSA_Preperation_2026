# Tree DSA — Google Interview Study Repo

A small, readable set of notes for mastering **binary trees, BSTs, and tries** for a Google SWE interview.
Every file is built to be re-read in ~3 minutes and fully recalled.

---

## How to use this repo

1. Read the **concept guide** for a topic first (`concepts/`).
2. Then work through that topic's **problems** in order (each topic has its own folder in the repo root; see [problems.md](problems.md)).
3. Go topic by topic, 1 → 12. Don't skip the concept guide — the problems assume it.

Each problem file has the same 4 sections:

| Section | What you get |
|---|---|
| **1. What the Question Asks** | Plain-English rules + 3–5 clarifying questions to ask the interviewer |
| **2. The Story & Core Intuition** | A real-world analogy + the one-sentence "Aha!" |
| **3. Plain English Logic** | Step-by-step walkthrough + line-by-line explanation of the code |
| **4. Clean Code & Complexity** | `class Solution` + runnable tests + why the time/space cost is what it is |

---

## House style (one style, whole repo)

**The node** — every file uses this exact definition:

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

**The rules:**

- **Base case first.** The very first lines of any recursive function handle the empty node:
  `if node is None: return 0` (or `[]`, `True`, `None` — whatever "nothing" means here).
- **Explicit names.** `curr_node`, `left_depth`, `right_depth`, `left_sum`, `path_total`, `is_balanced`.
  No single letters except loop counters (`i`, `_`).
- **Type hints** on every function signature and return value.
- **Recursion lives in a nested helper.** The public method sets up; `def dfs(node): ...` does the work.
- **BFS uses a deque.** `from collections import deque`, then `queue = deque([root])`, then an inner
  `for _ in range(len(queue)):` loop to process exactly one level at a time.
- **Every problem file is runnable.** It ends with a `build_tree([...])` helper (builds a tree from a
  level-order list, `None` = missing child) and an `if __name__ == "__main__":` block of `assert`s.

---

## Pattern-recognition cheat sheet

Read the prompt, match a phrase, reach for the pattern.

| If the problem says... | Reach for | Core template |
|---|---|---|
| "maximum depth", "is it the same", "invert", "is it symmetric" | **Simple DFS** — recurse on `left` and `right`, combine the two answers | `return 1 + max(dfs(left), dfs(right))` |
| "diameter", "balanced", "max path sum", "longest ... path" | **Bottom-up DFS** — each call returns info to its parent, a separate variable tracks the global best | helper returns "best straight-line value going up"; update `self.best` inside |
| "return multiple facts" (e.g. rob vs. skip this node) | **Tree DP with a tuple** — helper returns `(state_a, state_b)` | `return (with_node, without_node)` |
| "every root-to-leaf path", "path sum equals target", "sum of numbers formed" | **Top-down DFS** — carry a running value *down* as a parameter | `dfs(node, running_total + node.val)` |
| "level order", "per level", "right side view", "zigzag", "closest to the root" | **BFS level loop** — deque, process `len(queue)` nodes per round | `for _ in range(len(queue)): ...` |
| "without recursion", "O(1) extra space", "iterator", "next smallest" | **Iterative traversal** — explicit stack (or Morris for O(1)) | push-left, pop, go right |
| BST + "kth smallest", "sorted", "closest", "minimum difference", "validate" | **Inorder traversal of a BST = sorted order** | inorder and watch consecutive values |
| BST + "insert", "delete", "search" | **Walk down using the ordering** (`val < node.val` → go left) | recurse into one child only |
| "lowest common ancestor" | BST: walk down by value. General tree: **postorder** — a node that sees both targets below it is the LCA | `if left and right: return node` |
| "construct the tree from preorder/inorder/postorder" | **Divide & conquer** — first/last element is the root, inorder splits left vs. right | recurse on the two halves |
| "sorted array → balanced BST" | **Divide & conquer** — middle element is the root | `mid = (lo + hi) // 2` |
| "nodes at distance K", "burn the tree", "distance between two nodes" | **Treat the tree as a graph** — build a `child → parent` map, then BFS | `parent[child] = node`, then BFS from target |
| "serialize", "deserialize", "encode to a string" | **Preorder with null markers** | `"#"` for `None`, split on write, consume a queue on read |
| "prefix", "starts with", "dictionary of words", "autocomplete" | **Trie** — a tree of character-maps | `node.children[ch]`, `node.is_word` |

---

## Problem index

The full topic-by-topic problem list — with each problem's source (LC150 / NC150 / both / Claude addition),
LeetCode number, difficulty, status, and a link to its file — lives in **[problems.md](problems.md)**.

That file is the single tracker. Each topic gets its own folder in the repo root
(e.g. `01-structural-dfs-simple-recursion/`), and the problem write-ups (`01`–`38`) live inside it.

---

## Complexity quick-reference

Define **N = number of nodes**, **H = height of the tree** (longest root-to-leaf chain).

- **Balanced tree:** H ≈ log₂(N). A tree of 1,000,000 nodes is only ~20 deep.
- **Skewed tree** (every node has one child — basically a linked list): H = N.

| Cost | Where it comes from |
|---|---|
| **Time O(N)** | Almost every tree algorithm visits each node a constant number of times. |
| **Space O(H)** — recursion | The call stack holds one frame per ancestor. Deepest point = the height. Balanced → O(log N); skewed → O(N). |
| **Space O(N)** — BFS | The queue's worst moment holds an entire level. The bottom level of a full tree is ~N/2 nodes. |
| **Space O(N)** — building output | Returning a list of all N values, or a serialized string, is O(N) no matter how you traverse. |

Interview reflex: if asked to reduce space below O(H), the answer is usually **Morris traversal** (O(1)) or an **explicit stack** you control.
