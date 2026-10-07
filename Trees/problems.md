# Problems — Topic-by-Topic Roadmap

The full problem set, grouped into **12 topics** in study order. Do them top to bottom.
Within each topic, the **Source** column tells you exactly where each problem comes from.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list |
| **NC150** | On the *NeetCode 150* list |
| **LC150 + NC150** | On **both** lists — highest-priority, most-asked |
| **[+] Claude** | Not on either list. Added here to cover a Google pattern the 27 originals miss. The reason is given under each topic. |

**Totals:** 38 problems — 10 on both lists · 15 LC150-only · 5 NC150-only · 8 Claude additions.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

---

## Topic 1 — Structural DFS / Simple Recursion

**Pattern:** recurse into `left` and `right`, then combine the two answers with the current node. The "hello world" of trees.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 1 | Maximum Depth of Binary Tree | **LC150 + NC150** | 104 | Easy | ☑ | [01-maximum-depth-of-binary-tree.md](01-structural-dfs-simple-recursion/01-maximum-depth-of-binary-tree.md) |
| 2 | Invert Binary Tree | **LC150 + NC150** | 226 | Easy | ☑ | [02-invert-binary-tree.md](01-structural-dfs-simple-recursion/02-invert-binary-tree.md) |
| 3 | Same Tree | **LC150 + NC150** | 100 | Easy | ☑ | [03-same-tree.md](01-structural-dfs-simple-recursion/03-same-tree.md) |
| 4 | Symmetric Tree | LC150 | 101 | Easy | ☑ | [04-symmetric-tree.md](01-structural-dfs-simple-recursion/04-symmetric-tree.md) |
| 5 | Subtree of Another Tree | NC150 | 572 | Easy | ☑ | [05-subtree-of-another-tree.md](01-structural-dfs-simple-recursion/05-subtree-of-another-tree.md) |

---

## Topic 2 — Bottom-up DFS / Tree DP (return combined info up)

**Pattern:** the helper returns a fact *to its parent* (e.g. height), while a separate variable tracks the global best answer seen anywhere. One clean pass, no recomputation.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 6 | Balanced Binary Tree | **LC150 + NC150** | 110 | Easy | ☑ | [06-balanced-binary-tree.md](02-bottom-up-dfs-tree-dp/06-balanced-binary-tree.md) |
| 7 | Diameter of Binary Tree | NC150 | 543 | Easy | ☑ | [07-diameter-of-binary-tree.md](02-bottom-up-dfs-tree-dp/07-diameter-of-binary-tree.md) |
| 8 | Binary Tree Maximum Path Sum | **LC150 + NC150** | 124 | Hard | ☑ | [08-binary-tree-maximum-path-sum.md](02-bottom-up-dfs-tree-dp/08-binary-tree-maximum-path-sum.md) |
| 9 | House Robber III | **[+] Claude** | 337 | Medium | ☑ | [09-house-robber-iii.md](02-bottom-up-dfs-tree-dp/09-house-robber-iii.md) |

> **Why #9:** it's the cleanest teacher of a helper that returns a **tuple of states** `(rob_this, skip_this)`. That exact trick reappears in many Google tree-DP questions (e.g. Binary Tree Cameras).
> **Note:** your list tagged #6 as NC150-only; it is actually on **both** lists.

---

## Topic 3 — Root-to-leaf / Path-state DFS (carry state down)

**Pattern:** pass a running value *down* as a function argument (`dfs(child, total + node.val)`). Decisions are made when you hit a leaf.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 10 | Path Sum | LC150 | 112 | Easy | ☑ | [10-path-sum.md](03-path-state-dfs/10-path-sum.md) |
| 11 | Sum Root to Leaf Numbers | LC150 | 129 | Medium | ☑ | [11-sum-root-to-leaf-numbers.md](03-path-state-dfs/11-sum-root-to-leaf-numbers.md) |
| 12 | Count Good Nodes in Binary Tree | NC150 | 1448 | Medium | ☑ | [12-count-good-nodes-in-binary-tree.md](03-path-state-dfs/12-count-good-nodes-in-binary-tree.md) |
| 13 | Path Sum III | **[+] Claude** | 437 | Medium | ☑ | [13-path-sum-iii.md](03-path-state-dfs/13-path-sum-iii.md) |

> **Why #13:** Path Sum I/II are warm-ups; Path Sum III (count *any* downward path summing to target) forces the **prefix-sum-in-a-hashmap on a tree** technique — a genuine, common Google step-up.

---

## Topic 4 — BFS / Level-order Traversal

**Pattern:** a `deque`, and an inner `for _ in range(len(queue)):` loop so you handle exactly one level per round. Reach for this whenever the prompt says "per level" or "closest to the root."

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 14 | Binary Tree Level Order Traversal | **LC150 + NC150** | 102 | Medium | ☑ | [14-binary-tree-level-order-traversal.md](04-bfs-level-order/14-binary-tree-level-order-traversal.md) |
| 15 | Binary Tree Right Side View | **LC150 + NC150** | 199 | Medium | ☑ | [15-binary-tree-right-side-view.md](04-bfs-level-order/15-binary-tree-right-side-view.md) |
| 16 | Average of Levels in Binary Tree | LC150 | 637 | Easy | ☑ | [16-average-of-levels-in-binary-tree.md](04-bfs-level-order/16-average-of-levels-in-binary-tree.md) |
| 17 | Binary Tree Zigzag Level Order Traversal | LC150 | 103 | Medium | ☑ | [17-binary-tree-zigzag-level-order-traversal.md](04-bfs-level-order/17-binary-tree-zigzag-level-order-traversal.md) |
| 18 | Populating Next Right Pointers in Each Node II | LC150 | 117 | Medium | ☑ | [18-populating-next-right-pointers-ii.md](04-bfs-level-order/18-populating-next-right-pointers-ii.md) |
| 19 | Vertical Order Traversal of a Binary Tree | **[+] Claude** | 987 (314) | Hard | ☑ | [19-vertical-order-traversal.md](04-bfs-level-order/19-vertical-order-traversal.md) |

> **Why #19:** column-indexed BFS (`col - 1` left, `col + 1` right) is one of Google's most historically-asked tree questions. LC 314 is the simpler locked version; LC 987 adds a tie-break sort.

---

## Topic 5 — Iterative Traversal & O(1) Space

**Pattern:** replace the call stack with an explicit stack you control — or, for O(1) space, Morris traversal (temporarily rewire leaf pointers).

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 20 | Binary Tree Inorder Traversal (explicit stack + Morris) | **[+] Claude** | 94 | Easy | ☑ | [20-binary-tree-inorder-traversal.md](05-iterative-traversal/20-binary-tree-inorder-traversal.md) |

> **Why #20:** "now do it without recursion" and "can you get O(1) space?" are near-universal Google follow-ups. This is the reference implementation you'll adapt on the spot.

---

## Topic 6 — BST Properties (inorder traversal = sorted order)

**Pattern:** an inorder walk of a Binary Search Tree visits values in ascending order. Almost every BST question is "do an inorder walk and watch consecutive values."

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 21 | Validate Binary Search Tree | **LC150 + NC150** | 98 | Medium | ☑ | [21-validate-binary-search-tree.md](06-bst-properties/21-validate-binary-search-tree.md) |
| 22 | Kth Smallest Element in a BST | **LC150 + NC150** | 230 | Medium | ☑ | [22-kth-smallest-element-in-a-bst.md](06-bst-properties/22-kth-smallest-element-in-a-bst.md) |
| 23 | Minimum Absolute Difference in BST | LC150 | 530 | Easy | ☑ | [23-minimum-absolute-difference-in-bst.md](06-bst-properties/23-minimum-absolute-difference-in-bst.md) |
| 24 | Binary Search Tree Iterator | LC150 | 173 | Medium | ☑ | [24-binary-search-tree-iterator.md](06-bst-properties/24-binary-search-tree-iterator.md) |
| 25 | Delete Node in a BST | **[+] Claude** | 450 | Medium | ☑ | [25-delete-node-in-a-bst.md](06-bst-properties/25-delete-node-in-a-bst.md) |

> **Why #25:** every other BST problem here only *reads* the tree. Deletion (find the node, then splice using its inorder successor) is the one that tests whether you truly understand BST structure.

---

## Topic 7 — Lowest Common Ancestor

**Pattern:** BST → walk down comparing values. General tree → postorder; the node that first sees both targets in its two subtrees is the answer.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 26 | Lowest Common Ancestor of a Binary Search Tree | NC150 | 235 | Medium | ☑ | [26-lca-of-a-binary-search-tree.md](07-lowest-common-ancestor/26-lca-of-a-binary-search-tree.md) |
| 27 | Lowest Common Ancestor of a Binary Tree | LC150 | 236 | Medium | ☑ | [27-lca-of-a-binary-tree.md](07-lowest-common-ancestor/27-lca-of-a-binary-tree.md) |
| 28 | Lowest Common Ancestor with Parent Pointers (LCA III) | **[+] Claude** | 1650 | Medium | ☑ | [28-lca-with-parent-pointers.md](07-lowest-common-ancestor/28-lca-with-parent-pointers.md) |

> **Why #28:** "what if each node has a pointer to its parent?" is *the* standard LCA follow-up at Google. It turns into the "two linked lists intersection" trick — worth having in the bank.

---

## Topic 8 — Construction & Structural Transforms

**Pattern:** divide & conquer. One element of the traversal is the root; it splits the rest into a left part and a right part; recurse.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 29 | Construct Binary Tree from Preorder and Inorder Traversal | **LC150 + NC150** | 105 | Medium | ☑ | [29-construct-from-preorder-and-inorder.md](08-construction-and-transforms/29-construct-from-preorder-and-inorder.md) |
| 30 | Construct Binary Tree from Inorder and Postorder Traversal | LC150 | 106 | Medium | ☑ | [30-construct-from-inorder-and-postorder.md](08-construction-and-transforms/30-construct-from-inorder-and-postorder.md) |
| 31 | Convert Sorted Array to Binary Search Tree | LC150 | 108 | Easy | ☑ | [31-convert-sorted-array-to-bst.md](08-construction-and-transforms/31-convert-sorted-array-to-bst.md) |
| 32 | Flatten Binary Tree to Linked List | LC150 | 114 | Medium | ☑ | [32-flatten-binary-tree-to-linked-list.md](08-construction-and-transforms/32-flatten-binary-tree-to-linked-list.md) |

> **Note:** #31 **is** on LeetCode 150 — it was simply missing from your 27-item list, so it's folded in here.

---

## Topic 9 — Structural Counting Shortcut

**Pattern:** exploit a guaranteed shape (here: *complete* tree) to beat the naive O(N) count.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 33 | Count Complete Tree Nodes | LC150 | 222 | Medium | ☑ | [33-count-complete-tree-nodes.md](09-counting-shortcut/33-count-complete-tree-nodes.md) |

---

## Topic 10 — Tree as a Graph

**Pattern:** build a `child → parent` map so you can move *upward* too, then run ordinary BFS from a starting node.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 34 | All Nodes Distance K in Binary Tree | **[+] Claude** | 863 | Medium | ☑ | [34-all-nodes-distance-k.md](10-tree-as-a-graph/34-all-nodes-distance-k.md) |

> **Why #34:** "find every node exactly K edges away" (and its cousin "how long to burn the whole tree") is a Google favorite. The unlock — a tree becomes an undirected graph once you add parent links — is a reusable idea.

---

## Topic 11 — Serialization / Design

**Pattern:** preorder walk with an explicit marker (e.g. `"#"`) for `None`; rebuild by consuming that stream left to right.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 35 | Serialize and Deserialize Binary Tree | NC150 | 297 | Hard | ☑ | [35-serialize-and-deserialize-binary-tree.md](11-serialization/35-serialize-and-deserialize-binary-tree.md) |

---

## Topic 12 — Trie / Prefix Tree

**Pattern:** a tree where each node is a map from a character to a child node, plus an `is_word` flag. Built for prefix queries.

| # | Problem | Source | LC # | Difficulty | Status | File |
|---|---|---|---|---|---|---|
| 36 | Implement Trie (Prefix Tree) | LC150 | 208 | Medium | ☑ | [36-implement-trie.md](12-trie-prefix-tree/36-implement-trie.md) |
| 37 | Design Add and Search Words Data Structure | LC150 | 211 | Medium | ☑ | [37-design-add-and-search-words.md](12-trie-prefix-tree/37-design-add-and-search-words.md) |
| 38 | Word Search II | LC150 | 212 | Hard | ☑ | [38-word-search-ii.md](12-trie-prefix-tree/38-word-search-ii.md) |

> **Why this topic:** Google asks Trie heavily (autocomplete, spell-check, word games). It's a distinct tree family, so it gets its own block at the end.

---

## Coverage check — is this enough for a Google tree interview?

**Yes, for the tree portion.** After these 12 topics you will have hands-on reps in every pattern Google draws from:

- traversal — DFS (all 3 orders, recursive **and** iterative **and** O(1) Morris) and BFS (plain, per-level, column-indexed);
- information flowing **down** the tree (path state) and **up** the tree (tree DP / combined returns, including tuple-of-states);
- BST order properties — validate, kth, min-diff, iterator, **and** mutation (insert/delete);
- ancestor queries — LCA in a BST, in a general tree, and with parent pointers;
- building trees — from two traversals, and from a sorted array;
- in-place restructuring (flatten), shape-based shortcuts (complete-tree count);
- tree-as-graph (distance-K), serialization, and tries.

**Deliberately out of scope** (different unit, not "binary trees"): segment trees / Fenwick trees, balancing rotations (AVL / red-black internals), B-trees, suffix trees, and heavy graph algorithms. Google's *tree* rounds don't go there; if you want the competitive-programming structures, that's a separate study set.
