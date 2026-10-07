# 1650. Lowest Common Ancestor of a Binary Tree III

**Category:** [+] Claude | **Difficulty:** Medium | **Pattern:** Two Pointers via Parent Pointer (Linked List Intersection)

---

### 1. The Problem Statement

* **Question:** Given two nodes `p` and `q` in a binary tree, return their lowest common ancestor (LCA). Unlike Problems 26 and 27, you are **not given the root**, and each node has an extra pointer: `node.parent`, pointing to its parent (`None` for the root).
* **Simple Explanation:** You can only walk *upward* from `p` and `q` toward the root — you can't walk down from a root you don't have. Find the first node where their upward paths meet.

---

### 2. The Core Intuition

> **Crucial Insight:** This is secretly **LeetCode 160: Intersection of Two Linked Lists**.
> Think of the chain `p -> p.parent -> p.parent.parent -> ... -> root` as one linked list, and `q -> q.parent -> ... -> root` as a second linked list. Above the LCA, both chains walk through the **exact same nodes** (LCA's parent, grandparent, ..., root) — they've merged into a shared tail. Finding "where do these two paths merge" is exactly the classic linked-list-intersection problem.

#### The Two-Pointer Trick (No Extra Space)

The two lists usually have different lengths (`p` and `q` can be at different depths), so naively walking both up one step at a time won't line them up. The standard fix:

1. Start `ptr_a = p` and `ptr_b = q`.
2. Step both up one parent at a time.
3. When `ptr_a` falls off the top (`None`), redirect it to start over at `q`. When `ptr_b` falls off the top, redirect it to start over at `p`.
4. Because each pointer ends up walking **the same total distance** (`depth(p) + depth(q)`) by the time it reaches the LCA, they arrive at the LCA on the **exact same step** — that's where they meet.

```text
Path of ptr_a:  p -> ... -> root -> q -> ... -> LCA
Path of ptr_b:  q -> ... -> root -> p -> ... -> LCA
                 (both walk depth(p) + depth(q) edges total, so they land together)
```

---

### 3. Code & Line-by-Line Explanation

#### Approach A: Two Pointers, O(1) Extra Space (Preferred)

```python
from typing import Optional


class Node:
    def __init__(self, val: int = 0,
                 left: Optional["Node"] = None,
                 right: Optional["Node"] = None,
                 parent: Optional["Node"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent


class Solution:
    def lowestCommonAncestor(self, p: "Node", q: "Node") -> "Node":
        ptr_a, ptr_b = p, q

        # Walk both pointers up. Whichever falls off the top restarts
        # at the OTHER node's starting point.
        while ptr_a != ptr_b:
            ptr_a = ptr_a.parent if ptr_a else q
            ptr_b = ptr_b.parent if ptr_b else p

        return ptr_a

```

* **Line 18:** `ptr_a, ptr_b = p, q` — two "runners" start at the two target nodes.
* **Line 22:** Loop until the runners land on the same node.
* **Line 23:** If `ptr_a` still points at a real node, move it up to its parent. If it just fell off the root (`ptr_a` is `None`), send it back down to restart at `q`.
* **Line 24:** Same idea for `ptr_b`, restarting at `p` instead.
* **Line 26:** Once `ptr_a == ptr_b`, both have arrived at the LCA — return it.

#### Approach B: Ancestor Set (Simpler to Explain, Uses Extra Space)

```python
class Solution:
    def lowestCommonAncestor(self, p: "Node", q: "Node") -> "Node":
        # Step 1: Collect every ancestor of p (including p itself).
        ancestors = set()
        curr_node = p
        while curr_node:
            ancestors.add(curr_node)
            curr_node = curr_node.parent

        # Step 2: Walk up from q. The first node already in the set is the LCA.
        curr_node = q
        while curr_node not in ancestors:
            curr_node = curr_node.parent

        return curr_node

```

* **Line 4–7:** Walk from `p` all the way to the root, dropping every node visited into a `set` for O(1) membership checks.
* **Line 10–11:** Walk from `q` upward. The moment we hit a node that's already in `ancestors`, that node is on both paths — it's the lowest one, so it's the LCA.

---

### 4. Step-by-Step Dry Run (Approach A)

Tree:

```text
            3
           / \
          5   1
         / \
        6   2
           / \
          7   4
```

Trace `lowestCommonAncestor(p=7, q=1)` — expected answer: `3`.

| Iteration | `ptr_a` before | `ptr_b` before | `ptr_a` after | `ptr_b` after |
|---|---|---|---|---|
| 1 | `7` | `1` | `2` (`7.parent`) | `3` (`1.parent`) |
| 2 | `2` | `3` | `5` (`2.parent`) | `None` (`3.parent`, root) |
| 3 | `5` | `None` | `3` (`5.parent`) | `7` (restart at **p**) |
| 4 | `3` | `7` | `None` (`3.parent`, root) | `2` (`7.parent`) |
| 5 | `None` | `2` | `1` (restart at **q**) | `5` (`2.parent`) |
| 6 | `1` | `5` | `3` (`1.parent`) | `3` (`5.parent`) |

`ptr_a == ptr_b == 3` → loop stops → **returns `3`.** ✅

Notice `ptr_a` traced the path `7 → 2 → 5 → 3 → 1 → 3` (restarting at `q`'s value once) and `ptr_b` traced `1 → 3 → 1 → 7 → 2 → 5 → 3` — wait, re-reading the table: `ptr_b`'s restart uses `p`'s original node (`7`), not `q`. Both pointers travel `depth(p) + depth(q) = 3 + 1 = 4` real edges, plus the "free" jump when redirected, landing together on step 6.

---

### 5. Complexity Analysis

Let $d_p$ and $d_q$ be the depths of `p` and `q` from the root.

* **Approach A (Two Pointers):**
* **Time:** $\mathcal{O}(d_p + d_q)$ — each pointer takes at most `depth(p) + depth(q)` steps before they meet. Worst case (skewed tree): $\mathcal{O}(N)$.
* **Space:** $\mathcal{O}(1)$ — only two pointer variables, no extra data structure. This is the strict follow-up requirement Google interviewers usually ask for.


* **Approach B (Ancestor Set):**
* **Time:** $\mathcal{O}(d_p + d_q)$ — one walk up from each node.
* **Space:** $\mathcal{O}(d_p)$ — the `set` stores every ancestor of `p`.



---

### 6. Quick Revision Summary (30-Second Recall)

* **Reframe it:** Two "linked lists" (`p`'s ancestor chain, `q`'s ancestor chain) that share a common tail starting at the LCA — same shape as LC 160.
* **Two-Pointer Trick:** Walk both up one step at a time; when one falls off the root, restart it at the *other* node. They meet exactly at the LCA.
* **Why it works:** Both pointers cover the same total distance (`depth(p) + depth(q)`), so they land on the LCA in the same step.
* **Simpler fallback:** Collect `p`'s ancestors in a `set`, then walk up from `q` until you hit a node already in that set.
