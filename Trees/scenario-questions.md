# Trees: Scenario-Based Interview Question Bank (Google L3 style)

Google doesn't say "tree". It gives a short, vague situation (a reporting line, a menu, a bracket, a set of words with shared beginnings) and waits to see whether **you** notice the hierarchy and pick the right recursion or traversal. This file trains that one skill: **spot the structure with no hints, name the pattern, then say the cost out loud.**

Problem numbers (`#1`-`#38`) match [problems.md](problems.md). `LC` numbers are LeetCode's. Code in **Solve** is lifted from your write-ups, so the helper names and base cases are the ones you already wrote.

**Disguised on purpose:** scenarios never use the words "tree", "node", "root", "leaf", "BST", "ancestor", "traversal" (or "binary"). Each entry has an **Ask first** line (the clarifying questions that reveal the structure) and a **Spot it** line (the clue you should have caught).

**How to use:**

1. Read **Part 1** (the 5-step framework) until you can say it without looking.
2. Skim **Part 2** (signal -> pattern) before every mock.
3. In **Part 4**, cover everything except the **Scenario** line, answer it cold (structure? what does each call return? cost?), then check yourself.
4. Re-read **Part 5** (traps) the night before.

> **One honest warning about the repo.** Your write-ups are all *binary* trees (`left` / `right`). Many Google scenarios (reporting lines, menus, nested comments, folders) are **n-ary**: a node has a *list* of children. The recursion is identical, `left`/`right` just becomes `for child in node.children`. Part 1 step 2 and Part 6 cover this. It is the biggest gap in the repo.

---

## Part 1. The 5-step "is this a tree, and which pattern?" framework

Say these five steps **out loud** on every vague question.

### Step 1. Find the nodes and the "belongs under" relation

Ask: *what are the things, and what makes one thing sit under another?* A tree has **one top**, **exactly one parent for everyone else**, and **no loops**. That means `n` things and `n - 1` relations.

| The question says | Nodes are | Parent -> child means |
|---|---|---|
| "reports to", "manages", "approves for" | people | boss -> direct report |
| "contains", "is inside", "belongs under", "sub-" anything | folders, categories, sections | container -> thing inside it |
| "replies to", "nested", "thread" | comments | comment -> reply |
| "depends only on one thing", "feeds", "is decided by" | matches, formulas, steps | later -> the two earlier things that feed it |
| "words that start the same", "shared beginnings", "autocomplete" | prefixes (one character per step) | prefix -> prefix + one more letter |
| "any choice splits into 2 (or more) options", "yes/no questions" | decisions | question -> its answers |

Say: *"The nodes are ___. A node sits under ___. There is one top and one parent each, so it's a tree."*

### Step 2. Name the shape (this picks the tools)

| Shape | How you know | What it gives you |
|---|---|---|
| **Binary tree** | "at most two", left/right matters | `left`, `right` recursion |
| **BST** | "smaller on one side, larger on the other", "sorted", "ordered lookup" | inorder = sorted; search/insert in O(h); **bounds**, not just local checks |
| **N-ary tree** | "any number of reports / replies / subfolders" | `for child in children`; "top two children" instead of left/right |
| **Trie** | strings, shared prefixes, "starts with" | one character per edge, an `is_word` flag, O(L) operations |
| **Tree hidden in a graph** | `n` items, `n - 1` links, connected, no loops; or an edge list with no designated top | pick any node as the top; the *parent you came from* replaces `visited` |
| **Not a tree any more** | a second parent, cross-links, "dotted lines", "also reachable via" | it's a **graph**: needs a visited set (see #34, and Graphs 2.0 S14/S16/S17) |

Also decide: **Are there parent pointers?** (a record that stores "my manager" and nothing else -> #28, two linked lists meeting) **Is it balanced?** (decides whether `h` is `log n` or `n`)

### Step 3. Decide what each recursive call RETURNS (the contract)

Write one sentence before any code: ***"`dfs(x)` returns ___ about everything at or below x."***

| If the contract is... | Examples | Base case (`x is None`) |
|---|---|---|
| a number (height, size, sum) | #1, #7, #33 | `0` |
| a bool "does the rule hold below?" | #3, #6, #21 | `True` for "all must hold", `False` for "does any exist" |
| "the thing I found, or None" | #27 | `None` |
| a rebuilt piece | #25, #29, #31 | `None` |
| a pair/tuple of facts | #9 (take, skip) | `(0, 0)` |
| nothing (side effect: fill a list, update a best) | #20, #34 | plain `return` |

### Step 4. What flows DOWN and what flows UP?

| Direction | Mechanism | Use it when the answer at a node depends on... | Examples |
|---|---|---|---|
| **Down** | function argument | **what's above it**: depth, running sum, bounds, max so far, the path | #10-#12, #21, #13 |
| **Up** | return value | **what's below it**: height, count, found target, subtree sum | #1, #6, #7, #27 |
| **Both** | argument down + return up | both (e.g. bounds down, bool up) | #21, #12 |

Rule: *if a node needs facts about its ancestors, pass them down. If it needs facts about its descendants, return them up.* Mixing them up is the single most common reason a tree solution is O(n^2).

### Step 5. What is the answer's shape? Then pick the traversal

| The answer is... | Do this |
|---|---|
| **One value** (a number, a bool) | return it up; if the best answer is *not* what the parent needs, keep a separate best (see Part 2) |
| **A path or all paths** | pass the path down, append, recurse, **pop** (backtracking) |
| **One answer per level** | BFS with the `len(queue)` snapshot |
| **A modified tree** | each call returns the new top of its piece: `node.left = fix(node.left)`; or mutate in place and say so |
| **A string / a rebuilt tree** | preorder with explicit null markers, or two traversals that pin the shape |

Then choose the order: preorder (parent first, info flows down), inorder (sorted order of a BST), postorder (need children's answers first), level order (per-level / nearest-to-top). Table in Part 2.

Finish with cost: *"I visit each node once, doing O(1) work per visit, so O(n). The recursion goes as deep as the height, so O(h) space."*

### Questions to ask the interviewer (pick 2-3)

- **Is it a binary tree or can a node have any number of children?** Is there a single top? Can it be **empty**?
- **Is it a BST** (ordered), or arbitrary values? **Duplicates?** (strict `<` or `<=`?) Are values **unique** (needed for rebuilding from traversals)?
- **Is it balanced?** How **deep** can it get? (decides recursion vs iteration)
- Do nodes have **parent pointers**? Is the top node given, or only two nodes inside it?
- Is the path **root-to-leaf**, or can it start and end anywhere? Must it go **downward only**? Can values be **negative**?
- Do I count **nodes or edges**? Is the target **guaranteed to exist**?
- Can I **modify** the structure, or must it stay intact? Is it static, or does it change between queries? **One query or many?**
- Does it fit in **memory**? Is the data across machines?

---

## Part 2. Signal -> pattern cheat sheet

| What the question says | What it really is | Pattern | Problems |
|---|---|---|---|
| "how deep", "how many levels", "longest chain from the top" | height | return-value DFS (postorder): `1 + max(left, right)` | #1 |
| "is it balanced", "no side is much deeper than the other, at every point" | height difference at every node | bottom-up with a `-1` sentinel (not top-down recompute) | #6 |
| "longest route between **any two**", "may bend once" | diameter / max path | **global best** + return the one-armed value | #7, #8 |
| "pick the best set, but no two directly linked", "take it or skip it" | tree DP with states | return a **tuple** `(take, skip)` | #9 |
| "same", "identical", "mirror", "does this layout appear inside that one" | two structures walked in lockstep | parallel recursion `(p, q)` | #2, #3, #4, #5 |
| "route from the top to an end adds up to...", "digits along a route form a number", "compare each with everything above it" | top-down state | argument down, **leaf check** only if "to an end" | #10, #11, #12 |
| "any downward chain, starting anywhere, sums to K" | subarray-sum-equals-K on every root path | prefix-sum hash map with **undo** | #13 |
| "tier by tier", "per level", "waves", "closest to the top", "visible from the side", "alternate direction", "link neighbours on a tier" | level order | BFS, `for _ in range(len(queue))` | #14-#18 |
| "by column", "left-right position", "view from above" | coordinates while walking | BFS carrying `(col, row)`, group in a dict | #19 |
| "no recursion", "O(1) memory", "next on demand", "pause and resume" | iterative / lazy walk | explicit stack; Morris for O(1) | #20, #24 |
| "ordered structure: export sorted, kth, check the ordering, smallest gap, closest" | inorder of a BST is sorted | inorder + a `prev`, or bounds `(low, high)` | #21, #22, #23 |
| "insert / search / remove in an ordered structure" | walk down one side only | O(h); delete = splice with inorder successor | #25 (+ gap) |
| "lowest shared boss", "narrowest group that covers both", "where two upward chains first meet" | LCA | BST: walk by value. General: postorder, `left and right -> me`. Parent pointers: two-pointer | #26, #27, #28 |
| "rebuild from two listings" | divide and conquer; one listing gives the top, the other splits left/right | hashmap of inorder indices + pointers | #29, #30 |
| "balanced index from a sorted list" | middle becomes the top | `mid = (lo + hi) // 2` | #31 |
| "flatten / re-wire in place" | pointer surgery | Morris-style or reverse preorder | #32 |
| "count faster than visiting everything" + guaranteed shape | exploit the shape | perfect subtree = `2^h - 1` | #33 |
| "distance from X in **any** direction", "spreads", "how long to burn" | tree + parent links = graph | parent map + BFS with visited | #34 |
| "save to text and restore" | serialization | preorder with null markers | #35 |
| "starts with", "autocomplete", "words with shared beginnings", "pattern with blanks", "many words on a grid" | trie | `children` dict + `is_word`; DFS at wildcards; trie + backtracking | #36, #37, #38 |
| "`n` items, `n - 1` links, connected" / "exactly one parent, no loops" | **a tree hiding in a graph** | treat as a tree: any start, track the parent you came from | see below |

### When a tree is hiding in a graph

| Clue | What it tells you |
|---|---|
| "`n` nodes and `n - 1` edges" + "everything is reachable" | it is a tree (connected + acyclic) |
| "exactly one thing above each item, one top item" | tree (check: one in-degree-0 item, everyone else in-degree 1) |
| input is an **edge list**, no root given | pick any node as the top; DFS with `parent` instead of a visited set |
| "dotted-line" / "second manager" / "also reachable via" / "shared sub-team" | **not a tree**: you now need a visited set, and shortest-path means BFS (#34 Variant B) |
| "is it a valid hierarchy?" | tree validity = `n - 1` edges + connected (Graphs 2.0 S17) |
| "which link is the extra one?" | union-find (Graphs 2.0 S16) |
| "best centre / minimum height" | peel leaves (Graphs 2.0 S14) |

### Which traversal order fits?

| Order | Fits when | Examples |
|---|---|---|
| **Preorder** (me, left, right) | you act on a node **before** its children: copy, serialize, flatten, print paths, info flowing down | #10-#13, #32, #35 |
| **Inorder** (left, me, right) | a **BST**: values come out sorted | #21, #22, #23, #24 |
| **Postorder** (left, right, me) | you need the **children's answers first**: heights, subtree sums, delete, LCA, tree DP | #1, #6-#9, #27 |
| **Level order** (BFS) | per-level answers, nearest to the top, shortest depth, spread by distance | #14-#19, #34 |

### Global variable vs return value: how to tell

Ask: ***"What does my parent need from me? Is that the same as the final answer?"***

| Situation | Use | Why | Examples |
|---|---|---|---|
| Parent needs exactly the final answer | **Return value only** | nothing to track on the side | #1, #6, #27, #33 |
| Best answer could be **anywhere**, and it is *not* what the parent needs | Return what the parent needs (e.g. one-armed height) **and** update a `best` on the side | a path that bends at me can't be extended upward | #7 diameter, #8 max path sum |
| Parent needs **two options** from me | Return a **tuple** | the parent's choice depends on both | #9 |
| Node needs facts from **above** | **Argument** down | return values only flow up | #10-#12, #21 |
| You're **collecting** (a list, a counter) and no parent consumes it | `nonlocal` / outer list | the traversal is just a visit | #20, #34 |

Traps with globals: set them **inside** the method (not once in `__init__`), or the second test case starts dirty (Part 5, #5). A tuple return avoids the problem entirely, which is why interviewers like it.

---

## Part 3. Time and space complexity patterns

| Pattern | Time | Space | Why (one line) |
|---|---|---|---|
| Visit every node once (height, count, validate, LCA, path sum) | **O(n)** | **O(h)** | one call per node; stack as deep as the height |
| ...balanced tree | O(n) | O(log n) | `h ~ log2 n`; 1,000,000 nodes is only ~20 deep |
| ...skewed tree (a chain) | O(n) | **O(n)** | `h = n`; Python `RecursionError` near 1000 frames |
| BFS / level order | O(n) | **O(w)** | queue holds the widest level; `w ~ n/2` for a full tree |
| Two trees in lockstep (same, symmetric, merge) | O(min(n, m)) | O(min(h1, h2)) | stops at the first mismatch or the smaller tree's end |
| BST search / insert / delete / LCA-in-BST | **O(h)** | O(h) recursive, O(1) iterative | one child per level |
| ...balanced BST / skewed BST | O(log n) / O(n) | | `h` again |
| Inorder with early stop (kth smallest) | O(h + k) | O(h) | descend once, then k pops |
| BST iterator | `next()` amortised O(1) (worst O(h)), init O(h) | O(h) | every node pushed and popped once over n calls |
| Morris traversal | O(n) | **O(1)** | each edge is walked a constant number of times; pointers are rewired then restored |
| Try each node as a start, re-scan a template (subtree match) | O(n * m) | O(h) | n candidates x m work each |
| Top-down check that recomputes height at every node | O(n * h) -> O(n^2) skewed | O(h) | the classic "brute force" in #6 |
| Construct from two traversals, **slicing + `.index()`** | O(n^2) | O(n^2) | scan + list copies at every level |
| Construct from two traversals, **hashmap + pointers** | O(n) | O(n) | O(1) lookup, no copies |
| Prefix-sum hashmap on paths (#13) | O(n) | O(h) (see #13 caveat) | one O(1) map update per node |
| Serialize / deserialize | O(n) | O(n) | `2n + 1` tokens (n values + n + 1 null markers) |
| Count a complete tree with the height trick | **O(log^2 n)** | O(log n) | log n levels x O(log n) to measure the two heights |
| Tree as graph (parent map + BFS) | O(n) | O(n) | map + visited + queue |
| Trie insert / search / startsWith | **O(L)**, `L` = word or prefix length | O(1) extra for search; O(L) new nodes on insert | one step per character, independent of how many words are stored |
| Trie total space | | **O(total characters)** over all stored words (dict children); shared prefixes are stored once | worst case no sharing = sum of word lengths; array-of-26 children is a constant factor more |
| Trie wildcard search with `k` dots | O(L) with no dots; up to O(26^k * L) with dots | O(L) stack | each dot fans out into every child |
| Trie + grid backtracking | O(M * N * 3^(L-1)) worst, far less with pruning | O(W * L) trie + O(L) stack | 3 choices after the first step (not back where you came from) |

### Why the recursion stack counts as space

Every call that has not finished yet is a **stack frame** in memory (arguments, local variables, a return address). A call can't finish until its children return, so the frames of **all ancestors of the current node are alive at once**. The most that ever exist together is the longest chain, which is the **height `h`**. So a recursive tree algorithm uses O(h) extra space even if it returns a single number.

- Balanced: `h ~ log n`, cheap.
- Skewed: `h = n`. A million-node chain means a million frames, so Python raises `RecursionError` at the default ~1000. `sys.setrecursionlimit` is not a real fix (it can crash the C stack). The honest fix is an **iterative** version with an explicit stack (you control the memory) or **Morris** (O(1)).
- Compare with BFS: the queue's peak is the widest level `w`. A **bushy** tree has `w ~ n/2`, so DFS is cheaper. A **skinny** tree has `w ~ 1`, so BFS is cheaper. Say which you'd pick and why.

### The counting recipe (say it every time)

> **Time = (number of nodes visited) x (work per visit).**
> **Space = recursion depth (height) or queue width, plus any output you build.**

**Worked example 1: Diameter (#7).**
1. Every node is visited once -> n visits.
2. Per visit: two returned numbers, one `max`, one addition -> O(1).
3. Time = n x O(1) = **O(n)**.
4. Stack depth = height -> **O(h)** (log n balanced, n skewed).

**Worked example 2: Balanced check, top-down brute force (#6).**
1. At each node we call `height(left)` and `height(right)`. Each call visits the whole sub-piece below.
2. Balanced tree: each level costs ~n, there are log n levels -> **O(n log n)**.
3. Skewed tree: the sizes below are n-1, n-2, ... -> n + (n-1) + ... = **O(n^2)**.
4. Bottom-up returns the height *once* per node, so the repeated work disappears -> **O(n)**.

**Worked example 3: Trie (#36).** 2 million product names, you type a 7-letter prefix. You take 7 steps. The 2 million never enter the formula: **O(L)**, not O(N).

---

## Part 4. Scenario entries (one per write-up)

Entry order: **Original question -> Scenario -> Ask first -> Spot it -> Brute force -> Solve -> Cost -> Follow-up -> Variant A -> Variant B.** Variants marked *(crosses into ...)* deliberately leave the pattern, so you learn where it stops working.

---

### 1. Maximum Depth of Binary Tree (#1, LC 104)

**Original question.** Given the root of a binary tree, return its maximum depth: the number of nodes along the longest path from the root down to the farthest leaf. An empty tree has depth 0.

**Scenario.** *Every manager at a company has at most two direct reports. Finance asks: starting from the CEO, how many people are on the longest reporting chain?*

**Ask first.**
1. Do you want the number of people on the chain or the number of links between them?
2. Can the company be empty (no CEO)?

**Spot it.** "Reports to" with one boss each, and "longest chain downward". That is the height of a hierarchy.

**Brute force.** List every complete chain from the CEO to someone with no reports, measure each, take the max. Materialising each chain costs O(h), so O(L * h) for L ends, up to O(n^2) on a "broom" shape. A plain walk with a depth counter is already O(n); the recursion is the shortest correct form of it.

**Solve** (from [01-maximum-depth-of-binary-tree.md](01-structural-dfs-simple-recursion/01-maximum-depth-of-binary-tree.md)):
```python
def maxDepth(self, root):
    if not root:                      # base: empty piece is 0 tall
        return 0
    left_depth = self.maxDepth(root.left)
    right_depth = self.maxDepth(root.right)
    return 1 + max(left_depth, right_depth)   # returns: height of this piece (in nodes)

# Alternative: BFS, count the levels
queue, depth = deque([root]), 0
while queue:
    depth += 1
    for _ in range(len(queue)):
        node = queue.popleft()
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
return depth
```
Each call **returns** the height of the piece beneath it. Base case: `None` -> 0.

**Cost.** DFS: O(n) time (one call per node), O(h) space (stack as deep as the height). BFS: O(n) time, O(w) space (widest level).

**Follow-up.** *"The chain is 100,000 deep."* -> recursion limit; use the BFS version or an explicit stack of `(node, depth)`. *"Count links instead of people."* -> subtract 1 (and decide what an empty tree returns). *"Any number of reports per manager?"* -> Variant B.

**Variant A. Minimum Depth of Binary Tree (LC 111)**
- **Question.** Return the number of nodes on the shortest path from the root down to the nearest leaf (a node with no children).
- **Scenario.** *A request enters at the CEO's desk and can be closed by anyone who has nobody left to forward it to. What is the fewest hands it can pass through?*
- **Pattern and cost.** BFS and stop at the first person with no reports (early exit), or DFS with the trap that a person with only one report is **not** an end, so you can't take `min(0, x)`. O(n) worst, O(w) space for BFS.

**Variant B. Maximum Depth of N-ary Tree (LC 559)** *(crosses into: n-ary)*
- **Question.** Given an n-ary tree (each node has a list `children`), return its maximum depth.
- **Scenario.** *A discussion forum lets anyone reply to any comment, with no limit on replies. How many levels deep does the longest argument go?*
- **Pattern and cost.** Same recursion: `1 + max(dfs(c) for c in children, default=0)`. Base: no children -> 1 (or `None` -> 0). Watch `max()` of an empty list. O(n) time, O(h) space.

---

### 2. Invert Binary Tree (#2, LC 226)

**Original question.** Given the root of a binary tree, invert it (swap the left and right children of every node) and return its root.

**Scenario.** *A knockout bracket is printed left to right. For a right-to-left edition, every match must swap which of its two feeder matches is drawn on top. Produce the mirrored bracket.*

**Ask first.**
1. Mirror in place, or return a new copy and leave the original alone?
2. Can the bracket be empty or a single match?

**Spot it.** The same operation ("swap the two sides") applies at every level, and each smaller piece is a smaller bracket of the same kind. That is simple recursion.

**Brute force.** Build a brand-new mirrored structure by reading every match and recreating it: O(n) time but O(n) extra memory. In place needs no new nodes.

**Solve** (from [02-invert-binary-tree.md](01-structural-dfs-simple-recursion/02-invert-binary-tree.md)):
```python
def invertTree(self, root):
    if not root:                       # base: nothing to swap
        return None
    root.left, root.right = root.right, root.left   # swap at this node
    self.invertTree(root.left)
    self.invertTree(root.right)
    return root                        # returns: the (now inverted) top of this piece

# Alternative: BFS, pop a node, swap, enqueue children
queue = deque([root])
while queue:
    node = queue.popleft()
    node.left, node.right = node.right, node.left
    if node.left:  queue.append(node.left)
    if node.right: queue.append(node.right)
```

**Cost.** O(n) time (every node swapped once), O(h) stack for DFS, O(w) for BFS.

**Follow-up.** *"Does swap-before or swap-after the recursive calls matter?"* No, the swap is local. *"Do it iteratively."* -> the BFS/stack form. *"Is the mirror of a valid BST still a BST?"* It becomes a descending-ordered BST, so the usual validation fails.

**Variant A. Flip Equivalent Binary Trees (LC 951)**
- **Question.** Two trees are flip equivalent if one can become the other by swapping the children of any number of nodes. Given two roots, return whether they are flip equivalent.
- **Scenario.** *Two clerks each drew the same competition, but each was free to swap which feeder match goes on top at any match. Could the two drawings describe the same event?*
- **Pattern and cost.** Parallel recursion on two structures: values equal and ((left,left and right,right) or (left,right and right,left)). O(min(n, m)) time, O(h) space.

**Variant B. Merge Two Binary Trees (LC 617)** *(crosses into: two structures in lockstep, #3)*
- **Question.** Merge two trees: where nodes overlap, sum the values; otherwise use the existing node.
- **Scenario.** *Two clerks each filled in part of the same bracket with match scores. Combine them: where both recorded a match, add the scores; where only one did, keep it.*
- **Pattern and cost.** Recurse on `(a, b)`; base: if one is `None`, return the other. O(min(n, m)) time, O(h) space. Say whether you mutate an input.

---

### 3. Same Tree (#3, LC 100)

**Original question.** Given the roots of two binary trees `p` and `q`, return whether they are the same: structurally identical, with equal values at every position.

**Scenario.** *Two offices each exported their reporting lines (every manager has a left-hand and a right-hand deputy slot). Are the two exports identical, slot by slot?*

**Ask first.**
1. Does the left/right position matter, or only who reports to whom?
2. Compare by ID only, or the whole record?

**Spot it.** "Compare two structures position by position" -> walk both at once.

**Brute force.** Serialize both (with null markers) and compare the lists: O(n + m) time and space, no early exit. **Trap:** comparing only the inorder value lists gives false positives, because inorder alone loses the shape.

**Solve** (from [03-same-tree.md](01-structural-dfs-simple-recursion/03-same-tree.md)):
```python
def isSameTree(self, p, q):
    if not p and not q: return True      # both ended together
    if not p or not q:  return False     # shape mismatch
    if p.val != q.val:  return False     # value mismatch
    return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)

# Alternative: queue of pairs
queue = deque([(p, q)])
while queue:
    a, b = queue.popleft()
    if not a and not b: continue
    if not a or not b or a.val != b.val: return False
    queue.append((a.left, b.left)); queue.append((a.right, b.right))
return True
```
Returns a bool for "the pieces under this pair match". Base: both `None` -> True, one `None` -> False.

**Cost.** O(min(n, m)) time (stops at the first mismatch or the smaller tree's end), O(min(h1, h2)) space.

**Follow-up.** *"Compare two trees on different machines."* -> hash every subtree (Merkle style) and compare root hashes. *"Left/right order doesn't matter."* -> flip equivalence (#2 Variant A). *"Iterative."* -> the pair queue.

**Variant A. Leaf-Similar Trees (LC 872)** *(crosses into: compares a derived sequence, not the shape)*
- **Question.** Two trees are leaf-similar if their leaf values, read left to right, form the same sequence. Return whether `root1` and `root2` are.
- **Scenario.** *Two departments are "equivalent" if the people who have nobody reporting to them, read left to right, are the same sequence, even if the management layers above them look different.*
- **Pattern and cost.** The shape can differ, so lockstep compare fails. Collect leaves with DFS (or compare two generators). O(n + m) time, O(h) with generators, O(leaves) with lists.

**Variant B. Find Duplicate Subtrees (LC 652)** *(crosses into: serialization and hashing)*
- **Question.** Return the roots of all duplicate subtrees: subtrees with the same structure and values as another subtree.
- **Scenario.** *A reorg tool wants to find teams whose internal reporting layout is an exact copy of another team's. Report one representative of each repeated layout.*
- **Pattern and cost.** Same Tree for every pair would be O(n^2 * m). Instead postorder-serialize each piece into a key and count in a hashmap. String keys cost O(n^2) worst case; give each distinct `(left_id, val, right_id)` an integer id for O(n).

---

### 4. Symmetric Tree (#4, LC 101)

**Original question.** Given the root of a binary tree, check whether it is a mirror of itself.

**Scenario.** *A tournament draw is "fair" if the left half is an exact mirror of the right half (same seeds in mirrored positions). Is a given draw fair?*

**Ask first.**
1. Must the mirror match on seed values, or only on shape?
2. Is an empty draw, or a single match, fair?

**Spot it.** "Compare the structure with a mirrored copy of itself" is Same Tree with the pairs **crossed**.

**Brute force.** Invert a copy (#2), then Same Tree (#3): O(n) time, O(n) extra memory. **Trap:** comparing the inorder list with its reverse is wrong (`[1,2,2,null,3,null,3]` fools it).

**Solve** (from [04-symmetric-tree.md](01-structural-dfs-simple-recursion/04-symmetric-tree.md)):
```python
def isSymmetric(self, root):
    if not root: return True
    def dfs(left, right):
        if not left and not right: return True
        if not left or not right:  return False
        if left.val != right.val:  return False
        return dfs(left.left, right.right) and dfs(left.right, right.left)  # outer, then inner
    return dfs(root.left, root.right)

# Alternative: queue of mirrored pairs
queue = deque([(root.left, root.right)])
# pop (l, r); enqueue (l.left, r.right) and (l.right, r.left)
```
Returns a bool. Base: both `None` -> True, one `None` -> False. A helper with **two** parameters is the point.

**Cost.** O(n) time, O(h) space (DFS) or O(w) (BFS).

**Follow-up.** *"Why can't one pointer do it?"* You need two cursors moving in opposite directions. *"Iterative?"* -> pair queue.

**Variant A. Check Whether Two Trees Are Mirrors**
- **Question.** Given roots `a` and `b`, return whether `b` is the mirror image of `a`.
- **Scenario.** *A second store must lay out its shelf hierarchy as the mirror image of the flagship store's. Does it?*
- **Pattern and cost.** The same crossed-pair recursion, with two separate tops instead of one. O(min(n, m)) time, O(h) space.

**Variant B. Pseudo-Palindromic Paths in a Binary Tree (LC 1457)** *(crosses into: top-down path state, #10)*
- **Question.** Each node holds a digit 1-9. Count root-to-leaf paths whose digits can be rearranged into a palindrome.
- **Scenario.** *Each route down a company hierarchy collects department codes (1-9). Count the complete routes whose codes could be rearranged to read the same forwards and backwards.*
- **Pattern and cost.** Not a mirror problem. Carry a bitmask down (toggle bit `val`), and at an end check `mask & (mask - 1) == 0` (at most one odd count). O(n) time, O(h) space.

---

### 5. Subtree of Another Tree (#5, LC 572)

**Original question.** Given the roots of two binary trees `root` and `subRoot`, return whether `root` contains a subtree with exactly the same structure and values as `subRoot`.

**Scenario.** *Head office has a template of a team layout (one manager and everyone beneath, exactly). Does any team in the franchise's full hierarchy match the template exactly, including everyone below?*

**Ask first.**
1. Must the match include everything below the matching top, or may it be a partial top part?
2. Can values repeat? Can the template be empty?

**Spot it.** "Does a smaller copy of this layout appear inside the bigger one" -> try each candidate top, and check each with Same Tree.

**Brute force.** The repo's solution *is* the straightforward one: for each of n candidates run Same Tree against the template, O(n * m). Be honest about that, then name the upgrade (below).

**Solve** (from [05-subtree-of-another-tree.md](01-structural-dfs-simple-recursion/05-subtree-of-another-tree.md)):
```python
def isSubtree(self, root, subRoot):
    if not subRoot: return True           # empty template matches anything
    if not root:    return False          # nothing left to search
    if self.isSameTree(root, subRoot): return True
    return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

# Alternative: BFS over root; only run isSameTree when node.val == subRoot.val
```
Returns a bool. Two levels: the **outer** search picks a candidate top, the **inner** `isSameTree` verifies.

**Cost.** O(n * m) time worst case (every value equal), O(h_root + h_sub) space.

**Follow-up.** *"Faster?"* -> serialize both with null markers and delimiters (so `12` is not `1,2`) and use KMP/substring search, O(n + m); or hash every subtree. *"A million templates against one hierarchy?"* -> precompute every subtree's hash into a set.

**Variant A. Linked List in Binary Tree (LC 1367)** *(crosses into: a different shape on the inside)*
- **Question.** Given the head of a linked list and the root of a binary tree, return whether the list's values appear as a downward path in the tree.
- **Scenario.** *A log says a customer visited pages A, B, C in that order. The site's navigation is a hierarchy where each page links to at most two sub-pages. Does that sequence follow a downward route somewhere?*
- **Pattern and cost.** Same two levels: outer "try every start", inner "match here". O(n * min(L, h)) time, O(h) space.

**Variant B. Count Univalue Subtrees (LC 250)** *(crosses into: bottom-up, one pass)*
- **Question.** Count the subtrees in which every node has the same value.
- **Scenario.** *Count the "unanimous teams": a manager plus everyone under them, all on the same job grade.*
- **Pattern and cost.** Trying every top and re-scanning is O(n^2). Postorder instead: each call returns whether its piece is unanimous (and the value), the count lives on the side. O(n) time, O(h) space.

---

### 6. Balanced Binary Tree (#6, LC 110)

**Original question.** Given a binary tree, determine whether it is height-balanced: at **every** node, the heights of the left and right subtrees differ by at most 1.

**Scenario.** *A support-escalation setup lets each agent pass a ticket to at most two specialists. Policy: at every agent, the deepest escalation path through one specialist must not be more than one step longer than through the other. Does a given setup comply?*

**Ask first.**
1. Is the rule required at every agent, or only overall from the top?
2. Does an empty setup count as compliant?

**Spot it.** "At every position, compare the two sides" needs both heights at every node -> bottom-up (postorder). A top-down check would recompute heights again and again.

**Brute force.** At each node call `height(left)` and `height(right)` (each scans the whole piece), then recurse. O(n log n) on a balanced tree and **O(n^2)** on a skewed one, because the same nodes are re-measured at every ancestor.

**Solve** (from [06-balanced-binary-tree.md](02-bottom-up-dfs-tree-dp/06-balanced-binary-tree.md)):
```python
def isBalanced(self, root):
    return self.dfs(root) != -1

def dfs(self, root):                  # returns: height, or -1 meaning "already unbalanced"
    if not root:
        return 0
    left_h = self.dfs(root.left)
    if left_h == -1: return -1        # short-circuit
    right_h = self.dfs(root.right)
    if right_h == -1: return -1
    if abs(left_h - right_h) > 1: return -1
    return 1 + max(left_h, right_h)
```

**Cost.** O(n) time (each node measured once), O(h) space.

**Follow-up.** *"Tell me which node broke the rule."* -> return `(height, bad_node)` or record on the side. *"One pass without a sentinel."* -> return a tuple `(is_balanced, height)`. *"Why is the early `-1` exit useful?"* It stops all further work as soon as one violation appears.

**Variant A. Binary Tree Tilt (LC 563)** *(return value is not the answer)*
- **Question.** The tilt of a node is the absolute difference between the sum of its left subtree and the sum of its right subtree. Return the sum of every node's tilt.
- **Scenario.** *Each team lead gets an "imbalance score": the absolute difference between the total salary of their left-hand group and their right-hand group. Report the sum of imbalance scores across the company.*
- **Pattern and cost.** Postorder returns the subtree **sum** (what the parent needs); the answer accumulates on the side. O(n) time, O(h) space.

**Variant B. Largest BST Subtree (LC 333)** *(crosses into: BST validity + bottom-up tuple)*
- **Question.** Return the size of the largest subtree that is a valid BST.
- **Scenario.** *Part of an inventory hierarchy was accidentally sorted by price. Find the biggest manager-and-everyone-below group where everything on the left side is cheaper and everything on the right is dearer.*
- **Pattern and cost.** Validating each candidate top-down is O(n^2). Bottom-up: return `(is_bst, size, min, max)` from each call. O(n) time, O(h) space.

---

### 7. Diameter of Binary Tree (#7, LC 543)

**Original question.** Return the length (in **edges**) of the longest path between any two nodes of a binary tree. The path may or may not pass through the root.

**Scenario.** *A telecom network is wired so that every relay station feeds at most two stations below it. Engineers want the worst-case latency: the largest number of cables on a path between any two stations.*

**Ask first.**
1. Count cables (edges) or stations (nodes)?
2. Must the path touch the top station? (No.)

**Spot it.** "Longest route between **any two**" that can bend once. At a node the best bending path is `left height + right height`, but the parent can use only **one** arm, so two different quantities are needed.

**Brute force.** For every node compute `height(left) + height(right)` separately: O(n * h), O(n^2) skewed. Or a BFS from every node: O(n^2).

**Solve** (from [07-diameter-of-binary-tree.md](02-bottom-up-dfs-tree-dp/07-diameter-of-binary-tree.md)):
```python
def diameterOfBinaryTree(self, root):
    self.res = 0                          # reset per call
    def dfs(curr):                        # returns: height (edges to deepest end) of this piece
        if not curr:
            return 0
        left = dfs(curr.left)
        right = dfs(curr.right)
        self.res = max(self.res, left + right)   # best path that bends HERE (kept on the side)
        return 1 + max(left, right)              # what the parent can use: one arm
    dfs(root)
    return self.res
```

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"Return the actual path."* -> track the two end nodes. *"N-ary."* -> keep the two largest child heights. *"Weighted edges."* -> add the edge weight when returning. *"Skewed 10^6."* -> iterative postorder.

**Variant A. Longest Univalue Path (LC 687)**
- **Question.** Return the length (in edges) of the longest path in which every node has the same value.
- **Scenario.** *In a call-routing hierarchy find the longest run of connected stations all running the same firmware version. The run may bend at one station.*
- **Pattern and cost.** Same "global best + one-arm return", but an arm extends only if the child's value equals the node's. O(n) time, O(h) space.

**Variant B. Tree Diameter (LC 1245)** *(crosses into: a tree hidden in a graph)*
- **Question.** Given `n` nodes and `n - 1` undirected edges forming a tree, return its diameter.
- **Scenario.** *A road network joins n villages with exactly n - 1 roads and every village can be reached from every other. What is the longest shortest-route between any two villages?*
- **Pattern and cost.** No root is given: "n - 1 edges, connected" is the clue. Either the same DFS from any start with `parent` instead of visited, or BFS to the farthest node, then BFS again from it. O(n) time and space.

---

### 8. Binary Tree Maximum Path Sum (#8, LC 124)

**Original question.** A path is a sequence of connected nodes where each node appears at most once. Given the root, return the maximum path sum of any non-empty path (it need not pass through the root or end at a leaf; values may be negative).

**Scenario.** *Each office in a regional hierarchy has a profit or loss figure (which may be negative). A consultant may choose one continuous chain of connected offices, starting and ending anywhere and going up and down at most once, and adds up the figures. Which chain gives the biggest total?*

**Ask first.**
1. Must the chain contain at least one office? Can every figure be negative?
2. Does "connected" mean directly linked offices only?

**Spot it.** Diameter with weights and negatives: "best chain that can bend once, anywhere".

**Brute force.** Sum the path for every pair of nodes: O(n^2) pairs times path length, up to O(n^3). Or, per node, recompute the best downward arms again and again: O(n^2).

**Solve** (from [08-binary-tree-maximum-path-sum.md](02-bottom-up-dfs-tree-dp/08-binary-tree-maximum-path-sum.md)):
```python
def maxPathSum(self, root):
    max_sum = float('-inf')               # handles all-negative trees
    def dfs(node):                        # returns: best chain going DOWN from here (one arm)
        nonlocal max_sum
        if not node:
            return 0
        left = max(0, dfs(node.left))     # drop a negative arm
        right = max(0, dfs(node.right))
        max_sum = max(max_sum, node.val + left + right)   # chain that bends here
        return node.val + max(left, right)
    dfs(root)
    return max_sum
```

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"All values negative?"* `-inf` start; clamping drops the arm, not the node itself. *"The path must end at a leaf."* -> no clamp. *"Return the path."* -> remember the best bending node and rebuild. *"Avoid the global."* -> return `(best_down, best_overall)`.

**Variant A. Longest Path With Different Adjacent Characters (LC 2246)** *(crosses into: tree given as a parent array, n-ary)*
- **Question.** Given a tree as `parent[]` (parent[0] = -1) and a string `s` of node labels, return the longest path where no two adjacent nodes share a label.
- **Scenario.** *A company chat hierarchy gives each person a team letter. Find the longest connected chain in which no two neighbours have the same letter.*
- **Pattern and cost.** Build children lists from the parent array, then "top two arms" at each node (n-ary diameter). O(n) time and space.

**Variant B. Maximum Product of Splitted Binary Tree (LC 1339)** *(crosses into: two passes)*
- **Question.** Remove exactly one edge to split the tree into two trees; maximise the product of their sums (mod 1e9+7).
- **Scenario.** *A company must split into two independent divisions by cutting exactly one reporting link. Maximise (payroll of one) x (payroll of the other).*
- **Pattern and cost.** Pass 1: total sum. Pass 2: postorder subtree sums `s`, candidate `s * (total - s)`. The answer needs a value (the total) that isn't known until a whole pass finishes. O(n) time, O(h) space.

---

### 9. House Robber III (#9, LC 337)

**Original question.** The houses form a binary tree. You may not rob two directly linked houses (a parent and its child). Return the maximum amount you can rob.

**Scenario.** *Each vendor in a street-sales network recruited at most two others. A promoter sponsors vendors to hand out samples, but a vendor and the person who recruited them can't both be sponsored (conflict of interest). Every vendor has a value. Maximise the total value of sponsored vendors.*

**Ask first.**
1. Does "linked" mean only direct recruiter/recruit pairs, not siblings or friends-of-friends?
2. Can values be negative (then never pick them)?

**Spot it.** "Pick the best set where no two directly linked are chosen" -> at each node there are two options (take / skip), and the parent's decision depends on **both** outcomes.

**Brute force.** `rob(node) = max(node.val + rob(grandchildren), rob(left) + rob(right))` without memoisation re-solves grandchildren twice and blows up (exponential). A memo dict makes it O(n); the tuple removes the dict.

**Solve** (from [09-house-robber-iii.md](02-bottom-up-dfs-tree-dp/09-house-robber-iii.md)):
```python
def rob(self, root):
    def dfs(node):                        # returns: (best if I take this, best if I skip this)
        if not node:
            return (0, 0)
        left_pair = dfs(node.left)
        right_pair = dfs(node.right)
        with_root = node.val + left_pair[1] + right_pair[1]     # take me -> children must be skipped
        without_root = max(left_pair) + max(right_pair)          # skip me -> children free
        return (with_root, without_root)
    return max(dfs(root))
```

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"Which houses?"* -> keep the choice (a set) with each state. *"N-ary."* -> `with = val + sum(skip_c)`, `without = sum(max(take_c, skip_c))`. *"Exactly k houses?"* -> add a dimension to the state.

**Variant A. Binary Tree Cameras (LC 968)**
- **Question.** Install cameras on nodes. A camera at a node monitors itself, its parent and its children. Return the minimum number of cameras to monitor every node.
- **Scenario.** *Security wants the fewest guards in a corridor network so every junction is covered. A guard covers their own junction and the ones directly above and below.*
- **Pattern and cost.** Same idea with three states per node (has a guard, covered, needs cover); a greedy postorder also works. O(n) time, O(h) space.

**Variant B. Maximum-weight independent set on a general graph** *(crosses into: it stops being a tree)*
- **Question.** Given an undirected graph with weighted vertices, choose vertices of maximum total weight with no two adjacent.
- **Scenario.** *Same sponsorship rule, but vendors now also recruit across teams, so a vendor can be linked to people in several teams.*
- **Pattern and cost.** The tuple DP relied on **one parent and no loops**, which makes children independent. With cross-links that independence breaks and the problem is NP-hard in general (polynomial only on special graphs, e.g. small treewidth). Say this out loud: *a hierarchy that gains cross-links is a graph.*

---

### 10. Path Sum (#10, LC 112)

**Original question.** Given the root of a binary tree and an integer `targetSum`, return whether there is a **root-to-leaf** path whose node values add up to `targetSum`.

**Scenario.** *A delivery planner starts at the central depot; each stop leads on to at most two further stops, and every stop charges a fee. Is there a complete route from the depot to a final stop (one with nothing beyond it) whose fees total exactly the customer's budget?*

**Ask first.**
1. Must the route end at a final stop, or may it stop anywhere?
2. Can fees be zero or negative (so you can't stop early when the total passes the budget)?

**Spot it.** "Complete route from the top to an end" plus a running total: state flows **down**, the decision is made at an end.

**Brute force.** Build every root-to-leaf path as a list and sum each: O(n * h) time and space. Carrying the running total instead is O(n).

**Solve** (from [10-path-sum.md](03-path-state-dfs/10-path-sum.md)):
```python
def hasPathSum(self, root, targetSum):
    def dfs(node, current_sum):           # returns: does any end-route below reach the target?
        if not node:
            return False                  # a missing child is NOT a valid end
        current_sum += node.val
        if not node.left and not node.right:
            return current_sum == targetSum
        return dfs(node.left, current_sum) or dfs(node.right, current_sum)
    return dfs(root, 0)

# Alternative: subtract instead of accumulate
# targetSum -= root.val; at a leaf return targetSum == 0
```

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"Return all such routes."* (Path Sum II) -> keep a path list, `append`, recurse, `pop`. *"Negative fees."* -> no pruning. *"Iterative."* -> stack of `(node, sum)`.

**Variant A. Binary Tree Paths (LC 257)**
- **Question.** Return all root-to-leaf paths as strings like `"1->2->5"`.
- **Scenario.** *Print every complete route from the depot to a final stop as a readable itinerary.*
- **Pattern and cost.** Same top-down walk, carrying the path; emit at an end. O(n * h) time (each path is built), O(h) space plus output.

**Variant B. All Paths From Source to Target (LC 797)** *(crosses into: it stops being a tree)*
- **Question.** Given a directed acyclic graph of `n` nodes, return all paths from node 0 to node n - 1.
- **Scenario.** *Departments may share a sub-team, so a team can be reached through two different managers. List every route from the CEO to one particular team.*
- **Pattern and cost.** It's a DAG: the DFS is the same, but each route is still valid even if a node was seen on another route, so a global `visited` would wrongly drop paths. Count could be exponential: O(2^n * n) worst. For *counting* only, memoise per node.

---

### 11. Sum Root to Leaf Numbers (#11, LC 129)

**Original question.** Each node holds a digit 0-9. Each root-to-leaf path forms a number (path 1 -> 2 -> 3 is 123). Return the sum of all those numbers.

**Scenario.** *A phone menu system: each option is a digit, and pressing options from the main menu down to a final option dials an extension number. Add up all the extension numbers.*

**Ask first.**
1. Can an extension start with 0 (leading zeros)?
2. How deep can the menu be (overflow in other languages)?

**Spot it.** "Digits along a route form a number" -> carry `value * 10 + digit` **down**; sum at the ends.

**Brute force.** Build each route as a string, `int()` it, add: O(n * h). Arithmetic carry is O(n).

**Solve** (from [11-sum-root-to-leaf-numbers.md](03-path-state-dfs/11-sum-root-to-leaf-numbers.md)):
```python
def sumNumbers(self, root):
    def dfs(node, current_sum):           # returns: total of all numbers formed below
        if not node:
            return 0                      # a missing child adds nothing (no double count)
        current_sum = current_sum * 10 + node.val
        if not node.left and not node.right:
            return current_sum
        return dfs(node.left, current_sum) + dfs(node.right, current_sum)
    return dfs(root, 0)
```

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"A path 1000 digits long?"* Python big ints cope; elsewhere use modulo. *"Iterative."* -> stack. *"Digits are bits."* -> Variant A.

**Variant A. Sum of Root To Leaf Binary Numbers (LC 1022)**
- **Question.** Each node is 0 or 1; each root-to-leaf path is a binary number (most significant bit first). Return the sum of these numbers.
- **Scenario.** *Each switch along a route is on (1) or off (0), and the route's switches read as one number in base 2. Add up the numbers over all complete routes.*
- **Pattern and cost.** `cur = cur * 2 + bit` (or `(cur << 1) | bit`). O(n) time, O(h) space.

**Variant B. Binary Tree Longest Consecutive Sequence (LC 298)** *(crosses into: any node counts, not only ends)*
- **Question.** Return the length of the longest downward path in which each value is exactly one more than its parent's.
- **Scenario.** *Staff ID numbers run along reporting lines. Find the longest downward run where each ID is exactly one more than the person above.*
- **Pattern and cost.** Pass the current run length **down** and update a global best at **every** node: there is no end-check because the run may stop anywhere. O(n) time, O(h) space.

---

### 12. Count Good Nodes in Binary Tree (#12, LC 1448)

**Original question.** A node X is good if no node on the path from the root to X has a value greater than X's. Return the number of good nodes.

**Scenario.** *A hiking trail fans out from the trailhead. A viewpoint is "worth it" if no earlier point on the way from the trailhead is higher. Count the worth-it viewpoints.*

**Ask first.**
1. Does a viewpoint exactly as high as the highest earlier one count?
2. Is the trailhead itself counted?

**Spot it.** "Compared with everything above it on the way down" -> carry `max_so_far` **down**; every node is judged, not just the ends.

**Brute force.** For each node, collect its path to the top (needs parent pointers or a stored path) and take the max: O(n * h). Carrying the max is O(n).

**Solve** (from [12-count-good-nodes-in-binary-tree.md](03-path-state-dfs/12-count-good-nodes-in-binary-tree.md)):
```python
def goodNodes(self, root):
    def dfs(node, max_so_far):            # returns: number of good nodes in this piece
        if not node:
            return 0
        is_good = 1 if node.val >= max_so_far else 0
        max_so_far = max(max_so_far, node.val)
        return is_good + dfs(node.left, max_so_far) + dfs(node.right, max_so_far)
    return dfs(root, root.val)

# Alternative: nonlocal counter, seed with float('-inf'), update max THEN compare (same result)
```

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"Strictly greater only?"* change `>=` to `>`. *"Return the nodes."* -> append instead of count. *"Update-then-check vs check-then-update?"* equivalent; be consistent.

**Variant A. Maximum Difference Between Node and Ancestor (LC 1026)**
- **Question.** Return the maximum `|a.val - b.val|` where `a` is an ancestor of `b`.
- **Scenario.** *Salaries run along reporting lines. Find the biggest gap between any person and anyone above them.*
- **Pattern and cost.** Carry `(min_so_far, max_so_far)` down; return the best gap at the ends. O(n) time, O(h) space.

**Variant B. Count Nodes Equal to Average of Subtree (LC 2265)** *(crosses into: info comes from below)*
- **Question.** Return the number of nodes whose value equals the (floored) average of all values in their subtree (including themselves).
- **Scenario.** *Count the managers whose own salary equals the average salary of their whole team, themselves included.*
- **Pattern and cost.** The direction flips: the comparison needs **descendants**, not ancestors. Postorder returns `(sum, count)`, a counter lives on the side. O(n) time, O(h) space.

---

### 13. Path Sum III (#13, LC 437)

**Original question.** Return the number of downward paths (parent to child, starting and ending anywhere) in a binary tree whose values sum to `targetSum`.

**Scenario.** *Each team in a hierarchy has a monthly net figure. Finance wants the number of downward chains of directly connected teams, starting and ending anywhere, whose figures total exactly the quarterly target.*

**Ask first.**
1. Must chains go strictly downward (no bending up)?
2. Can figures be negative or zero (so a sliding window won't work)?

**Spot it.** "Start anywhere, end anywhere, going down" = **subarray sum equals K** on every top-to-node path.

**Brute force.** Treat every node as a start and DFS down counting sums: O(n * h), i.e. O(n^2) skewed.

**Solve** (from [13-path-sum-iii.md](03-path-state-dfs/13-path-sum-iii.md)):
```python
def pathSum(self, root, targetSum):
    prefix_sum = defaultdict(int)
    prefix_sum[0] = 1                     # a path may start at the very top
    paths = 0
    def dfs(node, current_sum):           # returns nothing; counts on the side
        nonlocal paths
        if not node:
            return
        current_sum += node.val
        paths += prefix_sum[current_sum - targetSum]   # how many starts end a valid path here
        prefix_sum[current_sum] += 1
        dfs(node.left, current_sum)
        dfs(node.right, current_sum)
        prefix_sum[current_sum] -= 1      # BACKTRACK so siblings don't see this path
    dfs(root, 0)
    return paths
```

**Cost.** O(n) time. Space: your write-up says O(h). Careful: `-= 1` leaves **zero-count keys** in the dict, so the dict can hold O(n) distinct keys. To make the O(h) claim true, `del prefix_sum[current_sum]` when it reaches 0. Say that if asked.

**Follow-up.** *"Why decrement after the children?"* A sibling's path must not see this branch's prefix sums. *"No negative values?"* a two-pointer window along each path would work. *"Paths that bend up and down?"* much harder (combine left and right maps).

**Variant A. Subarray Sum Equals K (LC 560)** *(crosses into: arrays)*
- **Question.** Given an integer array and `k`, return the number of contiguous subarrays summing to `k`.
- **Scenario.** *Daily revenue figures: how many stretches of consecutive days add up to exactly the target?*
- **Pattern and cost.** The same prefix-sum map on a line; the tree version is this plus the **undo**. O(n) time, O(n) space.

**Variant B. Equal Tree Partition (LC 663)** *(crosses into: subtree sums in a set)*
- **Question.** Return whether you can remove exactly one edge to split the tree into two trees with equal sums.
- **Scenario.** *Can a company be split in two by cutting exactly one reporting link so both halves have identical total payroll?*
- **Pattern and cost.** Postorder subtree sums stored in a set; check whether `total / 2` is one of them (not counting the whole thing, careful when total = 0). O(n) time and space.

---

### 14. Binary Tree Level Order Traversal (#14, LC 102)

**Original question.** Return the level order traversal of a binary tree's node values: a list of lists, one per level, left to right.

**Scenario.** *A company announcement is sent in waves: first the CEO, then everyone who reports directly to the CEO, then everyone who reports to those people, and so on. Produce the waves, each as a left-to-right list.*

**Ask first.**
1. Is the order inside a wave left to right?
2. What do you return for an empty company?

**Spot it.** "Wave by wave", "tier by tier", "by distance from the top" -> BFS with a level snapshot.

**Brute force.** For each level L run a separate DFS that collects the nodes at depth L: O(n * h). (A single DFS with `res[depth].append` is also O(n); BFS is just the natural fit.)

**Solve** (from [14-binary-tree-level-order-traversal.md](04-bfs-level-order/14-binary-tree-level-order-traversal.md)):
```python
def levelOrder(self, root):
    if not root: return []                # base: empty -> no waves
    queue, result = deque([root]), []
    while queue:
        level_vals = []
        for _ in range(len(queue)):       # snapshot: exactly this level
            node = queue.popleft()
            level_vals.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level_vals)         # returns: list of levels
    return result
```

**Cost.** O(n) time (each node enqueued and dequeued once), O(w) queue space plus the output.

**Follow-up.** *"Bottom-up order."* (LC 107) reverse the result. *"Do it with DFS."* `res[depth].append(val)`. *"Very wide but shallow?"* DFS uses less memory; *"very deep and skinny?"* BFS does.

**Variant A. N-ary Tree Level Order Traversal (LC 429)** *(crosses into: n-ary)*
- **Question.** Given an n-ary tree, return its level order traversal.
- **Scenario.** *The same waves, but a manager can have any number of direct reports.*
- **Pattern and cost.** Same loop with `queue.extend(node.children)`. O(n) time, O(w) space.

**Variant B. All vertices grouped by distance from a start (BFS on a graph)** *(crosses into: it stops being a tree)*
- **Question.** Given an undirected graph and a start vertex, return the vertices grouped by their shortest distance from it.
- **Scenario.** *Starting from one web page, list the pages reachable in one click, then two clicks, and so on, where pages can link back to ones you already saw.*
- **Pattern and cost.** The level loop is the same, but links can point backwards, so without a **visited set** you loop forever and the "levels" repeat. O(V + E) time, O(V) space (see Graphs 2.0 S29/S30).

---

### 15. Binary Tree Right Side View (#15, LC 199)

**Original question.** Imagine standing on the right side of a binary tree. Return the values of the nodes you can see, top to bottom.

**Scenario.** *A company's reporting diagram is pinned to a wall. Looking at it from the right-hand edge, you can see only the person drawn furthest right on each tier. List who you'd see, from the top tier down.*

**Ask first.**
1. If a tier's right-hand side has a gap (a short branch ends), is the next person to the left visible? (Yes.)
2. Empty diagram -> empty list?

**Spot it.** "One answer per tier" and "the last one on each tier" -> BFS and keep the last, or DFS going right first.

**Brute force.** Build all levels as lists (#14), then take the last of each: O(n) time, O(n) space. Keeping only the last element needs only O(w) or O(h).

**Solve** (from [15-binary-tree-right-side-view.md](04-bfs-level-order/15-binary-tree-right-side-view.md)):
```python
# A: BFS, keep the last node of each level
queue = deque([root])
while queue:
    level_size = len(queue)
    for i in range(level_size):
        node = queue.popleft()
        if i == level_size - 1:
            right_side_view.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)

# B: DFS, right child FIRST; first node seen at each depth is the visible one
def dfs(node, depth):
    if not node: return
    if depth == len(right_side_view):
        right_side_view.append(node.val)
    dfs(node.right, depth + 1)
    dfs(node.left, depth + 1)
```
Returns a list with one value per level. Base: `None` -> nothing.

**Cost.** BFS O(n) time, O(w) space. DFS O(n) time, O(h) space.

**Follow-up.** *"Left side view?"* mirror it. *"View from above?"* -> #19. *"Which to pick?"* DFS for wide trees, BFS for tall skinny ones.

**Variant A. Find Bottom Left Tree Value (LC 513)**
- **Question.** Return the value of the leftmost node in the last row.
- **Scenario.** *On the bottom tier of the company diagram, who is drawn furthest left?*
- **Pattern and cost.** BFS right-to-left and return the last node popped, or DFS tracking the first node at the greatest depth. O(n) time.

**Variant B. Maximum Width of Binary Tree (LC 662)** *(crosses into: positions matter, not just counts)*
- **Question.** The width of a level is the distance between its leftmost and rightmost non-null nodes, counting the null gaps between them. Return the maximum width.
- **Scenario.** *The widest tier of the poster decides how big the paper must be, and gaps between people on a tier count as space.*
- **Pattern and cost.** `len(queue)` no longer works. Give each node a position index (`2i`, `2i + 1`) and take `last - first + 1` per level (subtract the first index to keep numbers small). O(n) time, O(w) space.

---

### 16. Average of Levels in Binary Tree (#16, LC 637)

**Original question.** Return the average value of the nodes on each level, as an array of doubles.

**Scenario.** *A knockout tournament is stored from the final backwards: the final, then the two semi-finals that fed it, then the four quarter-finals, and so on. Every match has an attendance figure. Report the average attendance per round.*

**Ask first.**
1. What precision is acceptable?
2. Can matches be missing in a round (an uneven bracket)?

**Spot it.** "Aggregate per round" -> BFS snapshot, aggregate inside the level loop.

**Brute force.** Build per-level lists (#14), then average each: O(n) time but O(n) extra memory. A running sum per level needs only O(w).

**Solve** (from [16-average-of-levels-in-binary-tree.md](04-bfs-level-order/16-average-of-levels-in-binary-tree.md)):
```python
queue, ans = deque([root]), []
while queue:
    level_size, level_sum = len(queue), 0
    for _ in range(level_size):
        node = queue.popleft()
        level_sum += node.val
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    ans.append(level_sum / level_size)
return ans
```

**Cost.** O(n) time, O(w) space.

**Follow-up.** *"Overflow in other languages?"* use `long`/`double`. *"Median per level?"* needs the values: O(n log n) overall. *"With DFS."* `sums[depth]`, `counts[depth]`.

**Variant A. Find Largest Value in Each Tree Row (LC 515)**
- **Question.** Return the largest value in each row.
- **Scenario.** *Report the highest attendance in each round of the tournament.*
- **Pattern and cost.** Same loop with `max` instead of a sum. O(n) time, O(w) space.

**Variant B. Maximum Level Sum of a Binary Tree (LC 1161)** *(crosses into: DFS can do per-level too)*
- **Question.** Return the smallest level whose sum is the maximum.
- **Scenario.** *Which round drew the biggest total crowd (the earliest, if tied)?*
- **Pattern and cost.** BFS with a per-level sum and an argmax, or DFS with `sums[depth] += val`. BFS isn't required: depth passed down is enough. O(n) time, O(w) or O(h + levels) space.

---

### 17. Binary Tree Zigzag Level Order Traversal (#17, LC 103)

**Original question.** Return the zigzag level order traversal: left to right on level 0, right to left on level 1, and so on, alternating.

**Scenario.** *A fire-drill roll call goes tier by tier through the company, alternating direction on every tier (left-to-right, then right-to-left, and so on). Produce the call order.*

**Ask first.**
1. Does the first tier run left to right?
2. Do you want each tier as its own list?

**Spot it.** "Per tier" and "alternate" -> BFS plus a direction flag. The queue order itself never changes.

**Brute force.** BFS to get the tiers, then reverse the odd ones. That *is* the solution and it's O(n). Trap: reversing the **queue** instead of the finished list corrupts the next level.

**Solve** (from [17-binary-tree-zigzag-level-order-traversal.md](04-bfs-level-order/17-binary-tree-zigzag-level-order-traversal.md)):
```python
# A: collect left-to-right, reverse odd levels AFTER the inner loop
if level % 2 == 1:
    lis = lis[::-1]
ans.append(lis); level += 1

# B: build the level with a deque, no reversing
level_nodes = deque()
for _ in range(level_length):
    node = queue.popleft()
    if left_to_right: level_nodes.append(node.val)
    else:             level_nodes.appendleft(node.val)
    ...                                   # children still enqueued left then right
ans.append(list(level_nodes)); left_to_right = not left_to_right
```

**Cost.** O(n) time (a reversal of a level of size k is O(k), summing to O(n)), O(w) space.

**Follow-up.** *"Avoid reversing."* `appendleft`, or write into a preallocated list at index `size - 1 - i`. *"Two-stack version."* alternate pushing left-first and right-first.

**Variant A. Reverse Odd Levels of Binary Tree (LC 2415)** *(crosses into: mirrored pairs, #4)*
- **Question.** In a perfect binary tree, reverse the node *values* at every odd level (positions stay).
- **Scenario.** *In a perfectly symmetric bracket, the labels on every second round must be reversed in place while the slots stay where they are.*
- **Pattern and cost.** DFS on a mirrored pair `(left, right)` and swap values at odd depth, recursing on `(l.left, r.right)` and `(l.right, r.left)`. O(n) time, O(h) space.

**Variant B. Longest ZigZag Path in a Binary Tree (LC 1372)** *(crosses into: DFS with a direction state)*
- **Question.** A zigzag path goes left, right, left, ... or right, left, ... downward. Return the length (in edges) of the longest one anywhere.
- **Scenario.** *A trail must alternate: turn left, then right, then left, and so on. What is the longest such trail anywhere in the system, going only downward?*
- **Pattern and cost.** Not BFS at all. Pass the last direction and the current length down (or return `(len_if_left, len_if_right)`). O(n) time, O(h) space.

---

### 18. Populating Next Right Pointers in Each Node II (#18, LC 117)

**Original question.** Populate each node's `next` pointer to point to the node on its right on the same level, or `NULL` if there is none. (The write-up covers LC 117 for any shape, with an O(1)-space version only for the perfect tree, LC 116.)

**Scenario.** *Each usher needs to know who stands immediately to their right on the same tier of the staff diagram, so a message can pass along a tier without going back up. Fill in "the next person on my tier" for everyone; the last on each tier points nowhere.*

**Ask first.**
1. Is the diagram always completely full, or any shape?
2. Is extra memory allowed, or must it be O(1)?

**Spot it.** "Link neighbours across a tier" -> BFS, where the next person in the queue **is** the right neighbour.

**Brute force.** Queue-based BFS is O(n) time but O(w) space. (Searching each node's tier separately is O(n * h).) The improvement is O(1) space using the links you've just made.

**Solve** (from [18-populating-next-right-pointers-ii.md](04-bfs-level-order/18-populating-next-right-pointers-ii.md)):
```python
# A: BFS, peek the front of the queue
for i in range(level_size):
    node = queue.popleft()
    node.next = queue[0] if i < level_size - 1 else None
    if node.left:  queue.append(node.left)
    if node.right: queue.append(node.right)

# B: O(1) space, PERFECT tree only (LC 116)
leftmost = root
while leftmost.left:
    head = leftmost
    while head:
        head.left.next = head.right
        if head.next:
            head.right.next = head.next.left
        head = head.next
    leftmost = leftmost.left
```
Returns the (modified) top. Base: empty -> `None`.

**Cost.** A: O(n) time, O(w) space. B: O(n) time, O(1) space.

**Follow-up.** *"O(1) space for ANY shape (LC 117)?"* Not in your write-up. Walk each level through its `next` links with a dummy head:
```python
head = root
while head:
    dummy = Node(0); tail = dummy
    cur = head
    while cur:
        if cur.left:  tail.next = cur.left;  tail = tail.next
        if cur.right: tail.next = cur.right; tail = tail.next
        cur = cur.next
    head = dummy.next
```

**Variant A. Populating Next Right Pointers in Each Node (LC 116)**
- **Question.** The same, but the tree is perfect (every parent has two children, all leaves on one level).
- **Scenario.** *The same usher problem, but the diagram is completely full on every tier.*
- **Pattern and cost.** The shape guarantee gives the O(1) shortcut above. O(n) time, O(1) space.

**Variant B. Cousins in Binary Tree (LC 993)** *(crosses into: needs depth and parent)*
- **Question.** Two nodes are cousins if they are on the same depth but have different parents. Given `x` and `y`, return whether they are cousins.
- **Scenario.** *Two employees are "peers" if they are on the same tier but report to different managers.*
- **Pattern and cost.** BFS recording each target's parent, or DFS passing `(depth, parent)`. O(n) time, O(w) or O(h) space.

---

### 19. Vertical Order Traversal of a Binary Tree (#19, LC 987)

**Original question.** Return the vertical order traversal: nodes grouped by column from left to right; within a column, top to bottom; nodes sharing the same row and column sorted by value.

**Scenario.** *A mapping tool draws a company's reporting diagram on a grid. Each person sits in a column: a left-hand report goes one column left, a right-hand report one column right. Print the names column by column, left to right; within a column, top to bottom, with ties broken by ID.*

**Ask first.**
1. When two people share the same column and tier, order by ID or by arrival (left-to-right)?
2. Are empty columns skipped?

**Spot it.** "By horizontal position" -> assign `(row, col)` while walking and group by column.

**Brute force.** Collect every `(col, row, val)` and sort the lot: O(n log n). Grouping into a column dict and sorting inside each column is the same order of cost.

**Solve** (from [19-vertical-order-traversal.md](04-bfs-level-order/19-vertical-order-traversal.md)):
```python
nodes = defaultdict(list)
queue = deque([(root, 0, 0)])             # (node, col, row)
while queue:
    node, col, row = queue.popleft()
    nodes[col].append((row, node.val))
    if node.left:  queue.append((node.left,  col - 1, row + 1))
    if node.right: queue.append((node.right, col + 1, row + 1))
ans = []
for col in sorted(nodes):
    ans.append([val for row, val in sorted(nodes[col])])   # (row, val) tuple sort handles ties
return ans
```
Returns a list of columns. Base: empty -> `[]`.

**Cost.** O(n log n) time (the sorts), O(n) space.

**Follow-up.** *"LC 314: no tie-break."* BFS order already gives top-to-bottom within a column, so no per-column sort, just the column keys (or track min/max column), O(n). *"Why BFS rather than DFS for 314?"* DFS would put a deep left node before a shallower one in the same column.

**Variant A. Top View of a Binary Tree**
- **Question.** Return the nodes visible when the tree is viewed from above: the first node (smallest row) seen in each column.
- **Scenario.** *A drone photographs the diagram from above, and in each column only the person nearest the top is visible.*
- **Pattern and cost.** BFS with columns, keep the first per column. O(n) time, O(n) space.

**Variant B. Diagonal Traversal of a Binary Tree** *(crosses into: a different coordinate rule)*
- **Question.** Group nodes by diagonals running top-left to bottom-right: a right child stays on the same diagonal, a left child starts the next one.
- **Scenario.** *Staff are grouped into "lines of influence": your right-hand report is on your line, and your left-hand report begins a new line one step over. List each line.*
- **Pattern and cost.** Same coordinate trick with different rules: `right: diag, left: diag + 1`. O(n) time and space.

---

### 20. Binary Tree Inorder Traversal (#20, LC 94)

**Original question.** Return the inorder traversal (left, node, right) of a binary tree's values. Follow-up: do it iteratively. (The write-up also covers preorder LC 144 and postorder LC 145.)

**Scenario.** *A contact book is filed so that, at every entry, everything alphabetically before it is filed to one side and everything after it to the other. Export all names in alphabetical order without recursion, because the book can be millions of entries deep.*

**Ask first.**
1. Which order exactly: before, between or after an entry's two sides?
2. May I temporarily modify the structure, or is it read-only (shared with other readers)?

**Spot it.** "Alphabetical order out of an ordered structure" = inorder; "no recursion" = your own stack; "no extra memory" = Morris.

**Brute force.** Recursive inorder is O(n) time, O(h) call stack. Or dump everything and sort: O(n log n), ignoring the ordering you were given.

**Solve** (from [20-binary-tree-inorder-traversal.md](05-iterative-traversal/20-binary-tree-inorder-traversal.md)):
```python
# Inorder, explicit stack
res, stack, cur = [], [], root
while cur or stack:
    while cur:                    # go as far left as possible
        stack.append(cur); cur = cur.left
    cur = stack.pop()             # process
    res.append(cur.val)
    cur = cur.right               # then the right side

# Preorder: push RIGHT first so LEFT pops first
stack = [root]
while stack:
    node = stack.pop(); res.append(node.val)
    if node.right: stack.append(node.right)
    if node.left:  stack.append(node.left)

# Postorder: preorder with (node, right, left), then reverse the result
```
Returns the list of values. Base: empty -> `[]`.

**Cost.** O(n) time, O(h) space for the explicit stack (log n balanced, n skewed).

**Follow-up.** *"O(1) extra space?"* Morris. **Your write-up doesn't contain Morris inorder**, although problems.md says it does. It is:
```python
res, cur = [], root
while cur:
    if not cur.left:
        res.append(cur.val); cur = cur.right
    else:
        pred = cur.left
        while pred.right and pred.right is not cur:
            pred = pred.right
        if pred.right is None:        # first visit: thread back to cur
            pred.right = cur; cur = cur.left
        else:                         # second visit: remove thread, process
            pred.right = None; res.append(cur.val); cur = cur.right
```
O(n) time (each edge walked at most ~3 times), O(1) space. Downside: it **temporarily mutates** the structure, so it's unsafe with concurrent readers.

**Variant A. N-ary Tree Preorder Traversal (LC 589)** *(crosses into: n-ary)*
- **Question.** Return the preorder traversal of an n-ary tree.
- **Scenario.** *A folder-listing tool prints each folder's name and then its subfolders in order, with arbitrarily many subfolders each, and no recursion.*
- **Pattern and cost.** Stack; push the children in **reverse** so the first child pops first. O(n) time, O(n) worst-case stack (a wide node pushes all its children).

**Variant B. Recover Binary Search Tree (LC 99)**
- **Question.** Exactly two nodes of a BST were swapped by mistake. Recover the BST without changing its structure.
- **Scenario.** *An alphabetical index had two entries swapped by a bad edit. Put the two names back, using only constant extra memory.*
- **Pattern and cost.** Inorder with a `prev` pointer: the sequence has one or two descents; the first and last offenders are the swapped pair. Use Morris to hit O(1) space. O(n) time.

---

### 21. Validate Binary Search Tree (#21, LC 98)

**Original question.** Given the root of a binary tree, return whether it is a valid BST: for every node, all values in its left subtree are strictly smaller and all in its right subtree strictly greater, and both subtrees are valid BSTs.

**Scenario.** *A price lookup promises that, at every entry, every price filed on the left is lower and every price filed on the right is higher. After a bad migration, a QA script must confirm that promise holds everywhere.*

**Ask first.**
1. Can two entries have the same price (strict or non-strict)?
2. Can a price equal the smallest/largest integer (so `-inf`/`inf` sentinels matter)?

**Spot it.** "**Everything** on one side" is stronger than "my two neighbours": carry a **range** down, or check that the inorder sequence is strictly increasing.

**Brute force.** For each node, scan its whole left side for a bigger value and its right side for a smaller one: O(n * h), O(n^2) skewed. The tempting local check (child vs parent only) is **wrong**: `[5,1,4,null,null,3,6]` passes it but 3 sits in the right side of 5.

**Solve** (from [21-validate-binary-search-tree.md](06-bst-properties/21-validate-binary-search-tree.md)):
```python
# A: bounds flow DOWN
def dfs(node, low, high):             # returns: is this piece valid inside (low, high)?
    if not node:
        return True
    if not (low < node.val < high):
        return False
    return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)
return dfs(root, float('-inf'), float('inf'))

# B: inorder must be strictly increasing
prev = float('-inf')
def inorder(node):
    nonlocal prev
    if not node: return True
    if not inorder(node.left): return False
    if node.val <= prev: return False
    prev = node.val
    return inorder(node.right)
```

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"Duplicates allowed on the left?"* use `low <= val < high`. *"Values equal to INT_MIN?"* use `None` bounds. *"Iterative?"* explicit-stack inorder with early exit.

**Variant A. Two Sum IV, Input is a BST (LC 653)**
- **Question.** Given a BST and `k`, return whether two distinct elements sum to `k`.
- **Scenario.** *A price lookup is filed in order. Is there a pair of items whose prices add up to exactly the gift-card value?*
- **Pattern and cost.** Inorder gives a sorted list, then two pointers, O(n) time, O(n) space. Or a hash set while walking. For O(h) space, run a forward and a reverse BST iterator (#24) from both ends.

**Variant B. Validate Binary Tree Nodes (LC 1361)** *(crosses into: it might not be a tree at all)*
- **Question.** Given `n` nodes and arrays `leftChild`, `rightChild`, return whether they form exactly one valid binary tree.
- **Scenario.** *An import file lists, for each employee ID, up to two direct reports. Is it a valid single hierarchy: one top, nobody with two bosses, no loops, everyone reachable?*
- **Pattern and cost.** Count in-degrees (exactly one node with 0, all others 1), then DFS/BFS from that node with a **visited** set; you must reach all `n`. When links arrive as raw data, "is it a tree" is a graph check. O(n) time and space.

---

### 22. Kth Smallest Element in a BST (#22, LC 230)

**Original question.** Given the root of a BST and an integer `k`, return the k-th smallest value (1-indexed).

**Scenario.** *A leaderboard is filed so that lower scores sit to one side and higher scores to the other. Support asks "who is 7th lowest?" Return the score at rank `k` without exporting the whole leaderboard.*

**Ask first.**
1. Is `k` 1-indexed and always valid?
2. Is this a one-off, or many queries on a structure that keeps changing?

**Spot it.** "Rank in sorted order" from an ordered structure -> inorder, **stop after k**.

**Brute force.** Dump all values with a recursive inorder and index `res[k - 1]`: O(n) time, O(n) space. Ignoring the ordering and sorting, O(n log n). Both keep going long after the k-th is found.

**Solve** (from [22-kth-smallest-element-in-a-bst.md](06-bst-properties/22-kth-smallest-element-in-a-bst.md)):
```python
stack, curr = [], root
while curr or stack:
    while curr:
        stack.append(curr); curr = curr.left
    curr = stack.pop()
    k -= 1
    if k == 0:
        return curr.val               # early stop
    curr = curr.right

# Follow-up structure: every node stores size of its subtree
left_size = curr.left.size if curr.left else 0
if k == left_size + 1: return curr.val
elif k <= left_size:   curr = curr.left
else:                  k -= left_size + 1; curr = curr.right
```

**Cost.** Iterative with early stop: O(h + k) time, O(h) space. Augmented (size) version: O(h) per query.

**Follow-up.** *"The tree changes a lot and the queries are frequent."* -> store subtree sizes, updated on insert and delete (balanced so h = log n). *"Kth largest."* reverse inorder (right, node, left). *"Not a BST."* a heap of size k, O(n log k).

**Variant A. Kth Largest Element in a Stream (LC 703)** *(crosses into: a heap beats the ordered structure)*
- **Question.** Design a class that accepts values one at a time and returns the k-th largest after each.
- **Scenario.** *Scores keep arriving. After each, report the current 3rd highest.*
- **Pattern and cost.** A min-heap of size k: O(log k) per add, O(1) to read. Cheaper and simpler than an augmented BST.

**Variant B. Inorder Successor in BST (LC 285)**
- **Question.** Given a BST and a node `p`, return the node with the smallest key greater than `p.val`.
- **Scenario.** *Given a customer's ticket number in an ordered filing structure, return the next-higher ticket present.*
- **Pattern and cost.** No full inorder: walk down, `if p.val < cur.val: candidate = cur; go left else go right`. O(h) time, O(1) space.

---

### 23. Minimum Absolute Difference in BST (#23, LC 530)

**Original question.** Given the root of a BST, return the minimum absolute difference between the values of any two different nodes.

**Scenario.** *Taxi fares are filed so that cheaper trips sit to one side and pricier ones to the other. What is the smallest gap in price between any two different trips?*

**Ask first.**
1. Any two trips, not just neighbours in the structure?
2. Can two trips cost the same (gap 0)?

**Spot it.** "Smallest gap between any two" in sorted data is between **adjacent** values, and inorder of a BST is sorted.

**Brute force.** Compare every pair: O(n^2). Or dump inorder to an array and scan neighbours: O(n) time, O(n) space.

**Solve** (from [23-minimum-absolute-difference-in-bst.md](06-bst-properties/23-minimum-absolute-difference-in-bst.md)):
```python
prev, min_diff = None, float('inf')
def inorder(node):
    nonlocal prev, min_diff
    if not node: return
    inorder(node.left)
    if prev is not None:
        min_diff = min(min_diff, node.val - prev)   # neighbour in sorted order
    prev = node.val
    inorder(node.right)
inorder(root)
return int(min_diff)
# Baseline: iterative inorder into res[], then min(res[i] - res[i-1])
```

**Cost.** O(n) time, O(h) space (no array).

**Follow-up.** *"The structure isn't a BST."* sort the values, O(n log n). *"Return the pair."* keep the best `(prev, cur)`. *"Early exit?"* if the diff hits 1 with integers.

**Variant A. Closest Binary Search Tree Value (LC 270)**
- **Question.** Given a BST and a target, return the value in the BST closest to the target.
- **Scenario.** *Given a budget, find the filed price closest to it.*
- **Pattern and cost.** A search, not a sweep: walk down, track the best, go left or right by comparison. O(h) time, O(1) space.

**Variant B. Smallest gap in an unordered hierarchy** *(crosses into: the BST property is gone)*
- **Question.** Given any binary tree (no ordering), return the minimum absolute difference between two different nodes' values.
- **Scenario.** *The same smallest-gap question, but the structure was filed by department, not by price.*
- **Pattern and cost.** With no inorder shortcut, collect all values and sort: O(n log n) time, O(n) space. Say that the saving in #23 came entirely from the ordering.

---

### 24. Binary Search Tree Iterator (#24, LC 173)

**Original question.** Implement `BSTIterator`: constructor takes the root; `next()` returns the next smallest number; `hasNext()` tells whether more remain. `next` and `hasNext` should be O(1) average with O(h) memory.

**Scenario.** *A billing screen shows invoices in ascending amount, 20 at a time with a "load more" button. The invoices live in a very large ordered structure. The screen must not load everything up front, and "give me the next one" must be cheap.*

**Ask first.**
1. Can the data change while someone is paging through it?
2. How much memory is acceptable: O(n) or O(h)?

**Spot it.** "Next one on demand" over an ordered structure = a **paused** inorder traversal.

**Brute force.** Flatten everything into a list in the constructor: O(n) time and O(n) space before the first `next()`, even if the caller wants only 3 items.

**Solve** (from [24-binary-search-tree-iterator.md](06-bst-properties/24-binary-search-tree-iterator.md)):
```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        cur = root
        while cur:                        # push the left spine
            self.stack.append(cur); cur = cur.left

    def next(self):
        node = self.stack.pop()           # smallest remaining
        cur = node.right                  # prepare the following one
        while cur:
            self.stack.append(cur); cur = cur.left
        return node.val

    def hasNext(self):
        return len(self.stack) > 0
```
Contrast: the baseline flattens with a recursive inorder in `__init__` and just walks an index.

**Cost.** `__init__` O(h); `next()` O(1) amortised (worst O(h)); space O(h). Over n calls every node is pushed once and popped once, i.e. 2n operations, so O(1) each on average.

**Follow-up.** *"Add `peek()` or `prev()`."* cache visited values (Variant B). *"Iterate in descending order."* mirror left/right. *"The tree changes mid-iteration."* iterators are fail-fast or snapshot. *"O(1) space?"* Morris can't pause safely (the structure is rewired); with parent pointers a successor is O(1) space.

**Variant A. Flatten Nested List Iterator (LC 341)** *(crosses into: n-ary, lazy DFS)*
- **Question.** Implement an iterator over a nested list of integers (lists can contain integers or lists).
- **Scenario.** *A config file allows lists inside lists, to any depth. Build a reader that hands out the numbers one at a time, in order, without flattening everything first.*
- **Pattern and cost.** An explicit stack of iterators (a list is an n-ary node, a number is an end). Expand lazily inside `hasNext`. O(1) amortised, O(depth) space.

**Variant B. Binary Search Tree Iterator II (LC 1586)**
- **Question.** Extend the iterator with `hasPrev()` and `prev()`.
- **Scenario.** *The invoice viewer now needs a Back button.*
- **Pattern and cost.** Same lazy stack plus a list of values already produced and a pointer into it. `prev` is O(1); extra memory O(number visited).

---

### 25. Delete Node in a BST (#25, LC 450)

**Original question.** Given the root of a BST and a key, delete the node with that key (if present) and return the BST's (possibly updated) root, keeping it a valid BST.

**Scenario.** *A customer index is filed so that smaller IDs sit to one side and larger IDs to the other. When a customer closes their account, their record must vanish while the index stays correctly ordered and in one piece. Remove the record for a given ID.*

**Ask first.**
1. If the ID isn't present, return it unchanged?
2. May I copy another record's value into this slot, or must I re-link records (other things may point to them)?

**Spot it.** "Remove from an ordered structure while keeping it ordered" = find by the ordering, then splice, using the **inorder successor** when there are two children.

**Brute force.** Dump all values, drop one, rebuild a balanced BST (#31): O(n) time and space. The ordering lets you do it in O(h).

**Solve** (from [25-delete-node-in-a-bst.md](06-bst-properties/25-delete-node-in-a-bst.md)):
```python
def deleteNode(self, root, key):      # returns: the new top of this piece
    if not root:
        return None                   # key not found
    if key < root.val:
        root.left = self.deleteNode(root.left, key)
    elif key > root.val:
        root.right = self.deleteNode(root.right, key)
    else:
        if not root.left:  return root.right      # 0 or 1 child: promote the other
        if not root.right: return root.left
        curr = root.right                          # 2 children: inorder successor
        while curr.left:
            curr = curr.left
        root.val = curr.val
        root.right = self.deleteNode(root.right, root.val)   # delete the duplicate
    return root
```

**Cost.** O(h) time (search plus successor walk), O(h) stack. log n balanced, n skewed.

**Follow-up.** *"Iterative."* track the parent while searching. *"Re-link the successor instead of copying the value."* needed if nodes are referenced elsewhere. *"Keep it balanced."* AVL / red-black rotations (out of scope for this repo). *"Predecessor instead of successor?"* equally valid.

**Variant A. Insert into a Binary Search Tree (LC 701)** *(a gap in the repo)*
- **Question.** Insert a value into a BST (the value isn't already present) and return the root.
- **Scenario.** *Add a new customer ID so the index stays correctly ordered.*
- **Pattern and cost.** Walk down by comparison; attach at the first empty slot. O(h) time, O(1) iterative.

**Variant B. Trim a Binary Search Tree (LC 669)** *(crosses into: each call returns the new piece)*
- **Question.** Given a BST and `[low, high]`, trim it so all remaining values lie in the range, keeping relative structure. Return the new root.
- **Scenario.** *Archive the index: keep only invoices between $100 and $500 and drop the rest, keeping the ordering intact.*
- **Pattern and cost.** If `val < low` return `trim(right)`; if `val > high` return `trim(left)`; else re-attach the trimmed children. O(n) time worst, O(h) space.

---

### 26. Lowest Common Ancestor of a Binary Search Tree (#26, LC 235)

**Original question.** Given a BST and two nodes `p` and `q`, return their lowest common ancestor: the lowest node that has both as descendants (a node may be a descendant of itself).

**Scenario.** *A library catalog narrows by ID ranges: the main desk splits all IDs into a lower and a higher group, each of those is split again, and so on. Given two book IDs, find the narrowest range-desk that still covers both.*

**Ask first.**
1. Can one of the two books itself be the desk (a book is its own range)?
2. Are both guaranteed to exist, and are IDs unique?

**Spot it.** "Narrowest group covering both" is the LCA, and the **ordering** tells you which way to go: if both values are smaller go left; if both are larger go right; otherwise you are at the split.

**Brute force.** Find the path to `p` and the path to `q` (O(h) each), compare for the last shared node: O(h) time and O(h) space. The ordering removes the need to store paths.

**Solve** (from [26-lca-of-a-binary-search-tree.md](07-lowest-common-ancestor/26-lca-of-a-binary-search-tree.md)):
```python
def lowestCommonAncestor(self, root, p, q):   # returns: the split point
    if p.val < root.val and q.val < root.val:
        return self.lowestCommonAncestor(root.left, p, q)
    elif p.val > root.val and q.val > root.val:
        return self.lowestCommonAncestor(root.right, p, q)
    else:
        return root                           # split, or root is p or q

# Iterative, O(1) space
cur = root
while cur:
    if p.val < cur.val and q.val < cur.val:   cur = cur.left
    elif p.val > cur.val and q.val > cur.val: cur = cur.right
    else: return cur
```

**Cost.** O(h) time (one node per level), O(h) recursive or O(1) iterative space.

**Follow-up.** *"Either might be missing."* verify existence first. *"Not a BST."* -> #27. *"Millions of queries on a static tree."* Euler tour + sparse table (O(1) per query) or binary lifting (O(log n)).

**Variant A. Lowest Common Ancestor of Deepest Leaves (LC 1123)** *(crosses into: general postorder plus depth)*
- **Question.** Return the lowest common ancestor of the deepest leaves of a binary tree.
- **Scenario.** *Find the smallest group that contains every person on the bottom tier of the company.*
- **Pattern and cost.** Postorder returns `(depth, lca)`: if the two sides are equally deep this node is the answer, otherwise take the deeper side's. O(n) time, O(h) space.

**Variant B. Distance Between Two Values in a BST**
- **Question.** Given a BST and two values present in it, return the number of edges on the path between them.
- **Scenario.** *How many shelf-to-shelf hops separate two books in the catalog?*
- **Pattern and cost.** Find the LCA by value, then `dist = depth(p) + depth(q) - 2 * depth(lca)`, or count steps from the LCA to each. O(h) time, O(1) space.

---

### 27. Lowest Common Ancestor of a Binary Tree (#27, LC 236)

**Original question.** Given a binary tree and two nodes `p` and `q`, return their lowest common ancestor (a node can be its own descendant).

**Scenario.** *Two employees are named in an incident report. The company wants the most junior manager who is, directly or indirectly, above both (or one of them, if one oversees the other). The hierarchy isn't sorted in any way.*

**Ask first.**
1. Can one of them be the other's boss (then that boss is the answer)?
2. Are both guaranteed to be present, and are IDs unique?

**Spot it.** "Lowest shared boss" with no ordering to steer you: search both sides; the first node that sees one target in each side is the answer.

**Brute force.** Store the path to each target, compare: O(n) time, O(h) space. A worse idea is checking at every node whether both are inside it: O(n^2).

**Solve** (from [27-lca-of-a-binary-tree.md](07-lowest-common-ancestor/27-lca-of-a-binary-tree.md)):
```python
def lowestCommonAncestor(self, root, p, q):
    if not root:
        return None                   # base: nothing here
    if root == p or root == q:
        return root                   # found one target (compare by identity)
    left_res = self.lowestCommonAncestor(root.left, p, q)
    right_res = self.lowestCommonAncestor(root.right, p, q)
    if left_res and right_res:
        return root                   # one in each side: I am the split
    return left_res or right_res      # bubble up whichever found something
```
Returns "the target found below me, or the LCA if both were found, else `None`".

**Cost.** O(n) time, O(h) space.

**Follow-up.** *"Either may be missing."* a plain run can return a node even when the other target doesn't exist; count how many targets were seen (Variant A). *"Parent pointers."* -> #28. *"Many queries."* binary lifting: O(n log n) build, O(log n) query. *"Duplicate values."* compare identity, not value.

**Variant A. Lowest Common Ancestor of a Binary Tree II (LC 1644, premium)**
- **Question.** Same, but `p` or `q` might not be in the tree; return `null` if either is missing.
- **Scenario.** *The incident report names two people, but one of them may not work at this company at all. Return the shared manager only if both actually exist.*
- **Pattern and cost.** Don't stop at the first target found: keep a count (or return flags) of how many were seen, and accept the answer only if the count is 2. O(n) time, O(h) space.

**Variant B. Lowest Common Ancestor of a Binary Tree IV (LC 1676, premium)** *(crosses into: many targets)*
- **Question.** Return the LCA of an **array** of nodes (all present).
- **Scenario.** *The incident now names a whole group. Who is the most junior manager above all of them?*
- **Pattern and cost.** Same recursion with `if root in node_set: return root`. O(n + k) time, O(h + k) space. It extends to n-ary (loop over children; if two or more return non-null, this node is the answer).

---

### 28. Lowest Common Ancestor with Parent Pointers (#28, LC 1650)

**Original question.** Given two nodes `p` and `q` of a binary tree where each node has a `parent` pointer (and you are **not** given the root), return their lowest common ancestor.

**Scenario.** *Each employee record stores only "my manager", with no list of who reports to them, and you aren't told who the CEO is. Two record IDs are given. Find the closest manager they share.*

**Ask first.**
1. Is the CEO's manager field empty (`None`)?
2. Is extra memory limited (O(1))?

**Spot it.** "Records point upward only" -> each record starts a chain up to the top; two chains that **merge** into one shared tail = **intersection of two linked lists** (LC 160).

**Brute force.** Put every ancestor of `p` in a set, then walk up from `q` until you hit one: O(d_p + d_q) time, O(d_p) space.

**Solve** (from [28-lca-with-parent-pointers.md](07-lowest-common-ancestor/28-lca-with-parent-pointers.md)):
```python
# A: two pointers, O(1) space. Each pointer walks up, then restarts at the OTHER start.
ptr_a, ptr_b = p, q
while ptr_a != ptr_b:
    ptr_a = ptr_a.parent if ptr_a else q
    ptr_b = ptr_b.parent if ptr_b else p
return ptr_a

# B: ancestor set
ancestors, curr = set(), p
while curr: ancestors.add(curr); curr = curr.parent
curr = q
while curr not in ancestors: curr = curr.parent
return curr
```
Both pointers travel `depth(p) + depth(q)` steps in total, so they arrive at the LCA on the same step.

**Cost.** A: O(d_p + d_q) time (O(n) worst), **O(1)** space. B: same time, O(d_p) space.

**Follow-up.** *"What if they're in different trees?"* both pointers become `None` on the same step and the loop ends returning `None`. *"Alternative to the trick?"* compute both depths, lift the deeper one, then walk together. *"Many queries?"* binary lifting (Variant B).

**Variant A. Intersection of Two Linked Lists (LC 160)** *(crosses into: lists)*
- **Question.** Given the heads of two singly linked lists, return the node where they intersect, or `null`.
- **Scenario.** *Two delivery routes eventually merge into one shared stretch of highway. Where do they first join?*
- **Pattern and cost.** The same two-pointer swap. O(m + n) time, O(1) space.

**Variant B. Kth Ancestor of a Tree Node (LC 1483)** *(crosses into: preprocessing for many queries)*
- **Question.** Given a tree as a `parent[]` array, answer `getKthAncestor(node, k)` queries (return -1 if there is none).
- **Scenario.** *Given an employee, find the manager exactly k levels above them. There will be many such lookups.*
- **Pattern and cost.** Binary lifting: `up[j][v]` is the `2^j`-th ancestor. O(n log n) to build, O(log k) per query, O(n log n) space.

---

### 29. Construct Binary Tree from Preorder and Inorder Traversal (#29, LC 105)

**Original question.** Given two integer arrays `preorder` and `inorder`, the preorder and inorder traversals of the same binary tree (unique values), construct and return the tree.

**Scenario.** *A crash left two logs describing the same reporting hierarchy. Log 1 lists each manager before their two teams; log 2 lists each manager between their two teams. Everyone's ID is unique. Rebuild the exact hierarchy.*

**Ask first.**
1. Are IDs guaranteed unique (otherwise the logs are ambiguous)?
2. Are the logs guaranteed consistent with a real tree?

**Spot it.** "Two different orderings of the same structure": the first item of log 1 is the top, and its position in log 2 splits left people from right people.

**Brute force.** Slicing: `.index()` to find the split (O(n)) and list copies at every call, so O(n^2) time and space. Hashmap + index pointers removes both.

**Solve** (from [29-construct-from-preorder-and-inorder.md](08-construction-and-transforms/29-construct-from-preorder-and-inorder.md)):
```python
inorder_map = {val: idx for idx, val in enumerate(inorder)}
pre_idx = 0
def helper(in_left, in_right):        # returns: the rebuilt piece for inorder[in_left..in_right]
    nonlocal pre_idx
    if in_left > in_right:
        return None                   # base: empty range
    root_val = preorder[pre_idx]; pre_idx += 1
    root = TreeNode(root_val)
    mid = inorder_map[root_val]       # splits left from right
    root.left = helper(in_left, mid - 1)      # LEFT first: preorder order is root, left, right
    root.right = helper(mid + 1, in_right)
    return root
return helper(0, len(inorder) - 1)

# Baseline: root = TreeNode(preorder[0]); mid = inorder.index(preorder[0])
# root.left = build(preorder[1:mid+1], inorder[:mid]); root.right = build(preorder[mid+1:], inorder[mid+1:])
```

**Cost.** Optimised: O(n) time, O(n) space (map plus O(h) stack). Slicing: O(n^2) time and space.

**Follow-up.** *"Why isn't preorder alone enough?"* it doesn't say where the left side ends. *"Duplicates?"* ambiguous. *"Iterative?"* a stack with the inorder pointer. *"Why build left before right?"* `pre_idx` is shared; the order must match the preorder.

**Variant A. Construct Binary Search Tree from Preorder Traversal (LC 1008)** *(crosses into: BST needs only one listing)*
- **Question.** Given the preorder of a BST, construct it.
- **Scenario.** *One log lists the order in which entries were added to an ordered index. Rebuild the index.*
- **Pattern and cost.** The ordering replaces the second listing: recurse with an upper bound, consuming values while they are below it. O(n) time, O(h) space.

**Variant B. Construct Binary Tree from Preorder and Postorder Traversal (LC 889)** *(crosses into: ambiguity)*
- **Question.** Given preorder and postorder traversals (distinct values), construct any binary tree matching both.
- **Scenario.** *A crash left a log listing each manager before their teams and another listing each manager after their teams. Rebuild a hierarchy consistent with both.*
- **Pattern and cost.** Without inorder, a node with a single child can't say which side it is on, so more than one answer exists (the problem accepts any). `preorder[1]` is the left child's top; find it in postorder to size the left side. O(n) with a map. The lesson: *two traversals pin a tree only if one of them is inorder (or the tree is full).*

---

### 30. Construct Binary Tree from Inorder and Postorder Traversal (#30, LC 106)

**Original question.** Given `inorder` and `postorder` arrays for the same binary tree (unique values), construct and return the tree.

**Scenario.** *The same crash, different logs: one lists each manager between their two teams, the other lists each manager after both their teams. Rebuild the hierarchy.*

**Ask first.**
1. Which end of the post-order log holds the top?
2. Unique IDs, consistent logs?

**Spot it.** The mirror of #29: the **last** element of postorder is the top. Read it backwards and you get "top, right, left", so build **right first**.

**Brute force.** Slicing with `.index()`: O(n^2) time and space.

**Solve** (from [30-construct-from-inorder-and-postorder.md](08-construction-and-transforms/30-construct-from-inorder-and-postorder.md)):
```python
inorder_map = {val: idx for idx, val in enumerate(inorder)}
post_idx = len(postorder) - 1
def helper(in_left, in_right):        # returns: rebuilt piece
    nonlocal post_idx
    if in_left > in_right:
        return None
    root_val = postorder[post_idx]; post_idx -= 1
    root = TreeNode(root_val)
    mid = inorder_map[root_val]
    root.right = helper(mid + 1, in_right)    # RIGHT first (postorder read backwards)
    root.left = helper(in_left, mid - 1)
    return root
return helper(0, len(inorder) - 1)
```

**Cost.** O(n) time, O(n) space (slicing version: O(n^2)).

**Follow-up.** *"Why right first?"* postorder backwards is root, right, left. *"Why is slicing quadratic?"* every level copies O(n) elements.

**Variant A. Verify Preorder Serialization of a Binary Tree (LC 331)** *(crosses into: serialization, #35)*
- **Question.** Given a comma-separated preorder string with `#` for null, return whether it is a valid serialization, without rebuilding the tree.
- **Scenario.** *A backup file lists a hierarchy with "#" for "nobody here". Check that the file is well-formed without rebuilding anything.*
- **Pattern and cost.** Count open slots: start at 1; each token uses one; a number adds two; slots must stay positive until the last token and end at 0. O(n) time, O(1) space.

**Variant B. Maximum Binary Tree (LC 654)** *(crosses into: stack-based construction)*
- **Question.** Build a tree from an array: the maximum becomes the root, the part to its left builds the left subtree, the part to its right builds the right subtree.
- **Scenario.** *Given a ranking array, the top-ranked person becomes the head; those listed to their left form the left team and those to their right the right team, recursively. Build the chart.*
- **Pattern and cost.** Direct recursion is O(n^2) worst (sorted input). A monotonic stack builds it in O(n) time, O(n) space.

---

### 31. Convert Sorted Array to Binary Search Tree (#31, LC 108)

**Original question.** Given an integer array sorted in ascending order, convert it to a height-balanced binary search tree.

**Scenario.** *A product catalog arrives as a flat list sorted by price. Build a lookup index where cheaper items sit to one side and pricier ones to the other, and any lookup takes about log2(n) steps.*

**Ask first.**
1. Is any balanced shape acceptable, or a specific one?
2. For an even count, pick the left or right middle?

**Spot it.** "Flat sorted data -> fast lookup structure": the **middle** becomes the top, so each half is about the same size; recurse on both halves.

**Brute force.** Insert the items one at a time into a BST: sorted input produces a **chain**, O(n^2) time and height n. Building from the middle is O(n).

**Solve** (from [31-convert-sorted-array-to-bst.md](08-construction-and-transforms/31-convert-sorted-array-to-bst.md)):
```python
def helper(left, right):              # returns: balanced piece built from nums[left..right]
    if left > right:
        return None
    mid = (left + right) // 2
    root = TreeNode(nums[mid])
    root.left = helper(left, mid - 1)
    root.right = helper(mid + 1, right)
    return root
return helper(0, len(nums) - 1)
# Slicing version: mid = len(nums)//2; build(nums[:mid]), build(nums[mid+1:]) -> copies
```

**Cost.** Pointers: O(n) time, O(log n) stack. Slicing: O(n log n) time and space.

**Follow-up.** *"Sorted linked list instead?"* Variant A. *"Keep it balanced after inserts?"* AVL / red-black. *"Does it have to be height-balanced?"* choosing the middle is what guarantees it.

**Variant A. Convert Sorted List to Binary Search Tree (LC 109)** *(crosses into: no random access)*
- **Question.** Given the head of a singly linked list sorted ascending, convert it to a height-balanced BST.
- **Scenario.** *The sorted catalog arrives as a chain you can only read one entry at a time, front to back.*
- **Pattern and cost.** Find the middle with slow/fast pointers (O(n log n) overall), or build bottom-up by simulating inorder with a global list pointer (O(n) time, O(log n) space).

**Variant B. Balance a Binary Search Tree (LC 1382)**
- **Question.** Given a BST, return a balanced BST with the same node values.
- **Scenario.** *After many insertions the index degraded into a long chain. Rebuild it so lookups are fast again.*
- **Pattern and cost.** Inorder walk into a sorted array (#20/#21 idea), then build from the middle (#31). O(n) time, O(n) space.

---

### 32. Flatten Binary Tree to Linked List (#32, LC 114)

**Original question.** Flatten a binary tree to a "linked list" in place: the right pointer is the next item, the left is always `null`, and the order is the preorder traversal.

**Scenario.** *A department's reporting structure must become a single onboarding queue, in place: the manager first, then everyone in the left-hand team (recursively), then everyone in the right-hand team. Each person's "next" is their right link, and no left links remain.*

**Ask first.**
1. In place with O(1) extra memory?
2. Is the order manager -> left team -> right team (preorder)?

**Spot it.** "Turn a hierarchy into one chain, in place, manager first" = pointer surgery: hang the right side off the **last** person of the left side.

**Brute force.** Preorder into a list, then re-link from the list: O(n) time, O(n) space.

**Solve** (from [32-flatten-binary-tree-to-linked-list.md](08-construction-and-transforms/32-flatten-binary-tree-to-linked-list.md)):
```python
# A: Morris-style, O(1) space
curr = root
while curr:
    if curr.left:
        prev = curr.left
        while prev.right:             # rightmost node of the left side
            prev = prev.right
        prev.right = curr.right       # hang the old right side after it
        curr.right = curr.left        # move left over to the right
        curr.left = None
    curr = curr.right

# B: reverse preorder (right, left, node) with a prev pointer
def helper(node):
    nonlocal prev
    if not node: return
    helper(node.right); helper(node.left)
    node.right = prev; node.left = None; prev = node
```
Returns nothing (in place).

**Cost.** A: O(n) time (each node is walked a constant number of extra times), O(1) space. B: O(n) time, O(h) space.

**Follow-up.** *"Why reverse preorder?"* by the time you re-link a node, everything after it in the final order is already linked. *"Flatten in inorder?"* a different rewiring. *"Doubly-linked circular list from a BST?"* Variant A.

**Variant A. Convert Binary Search Tree to Sorted Doubly Linked List (LC 426, premium)**
- **Question.** Convert a BST in place into a sorted circular doubly linked list (left = prev, right = next); return the smallest element.
- **Scenario.** *Turn the ordered index into a circular list you can browse forwards and backwards, without allocating anything new.*
- **Pattern and cost.** Inorder with a `prev` pointer, linking `prev.right = node`, `node.left = prev`, then close the ring. O(n) time, O(h) space.

**Variant B. Flatten a Multilevel Doubly Linked List (LC 430)** *(crosses into: n-ary, same re-wiring)*
- **Question.** Each node may have a `child` list; flatten it so each child list sits right after its parent node.
- **Scenario.** *A playlist where any track can expand into its own sub-playlist. Flatten into one list, with each sub-playlist right after its track.*
- **Pattern and cost.** Same "splice the inner part between me and my next" as #32, with a stack or recursion. O(n) time, O(depth) space.

---

### 33. Count Complete Tree Nodes (#33, LC 222)

**Original question.** Given the root of a **complete** binary tree, return the number of nodes, in less than O(n) time.

**Scenario.** *A cloud provider allocates machine slots in layers: each layer is completely full before the next begins, and the last layer fills from the left. There are hundreds of millions of machines. The inventory API must report the total in much less time than visiting every one.*

**Ask first.**
1. Is the shape guaranteed (every level full except possibly the last, packed to the left)?
2. How big can it get: is O(n) too slow?

**Spot it.** "Faster than linear" plus a **guaranteed shape**: a piece whose leftmost depth equals its rightmost depth is perfect, and a perfect piece's size is a formula.

**Brute force.** Count everything with DFS or BFS: O(n) time.

**Solve** (from [33-count-complete-tree-nodes.md](09-counting-shortcut/33-count-complete-tree-nodes.md)):
```python
def countNodes(self, root):           # returns: node count of this piece
    if not root:
        return 0
    left_h, curr = 0, root
    while curr: left_h += 1; curr = curr.left       # leftmost height
    right_h, curr = 0, root
    while curr: right_h += 1; curr = curr.right     # rightmost height
    if left_h == right_h:
        return (1 << left_h) - 1                    # perfect: 2^h - 1
    return 1 + self.countNodes(root.left) + self.countNodes(root.right)
```

**Cost.** **O(log^2 n)** time: about log n levels of recursion, and each level costs O(log n) to measure the two heights (at each step one side is perfect and returns at once, so only one side keeps recursing). O(log n) space.

**Follow-up.** *"Another O(log^2 n) way?"* binary search on the last level's slots using a root-to-slot path by bits. *"What if it isn't complete?"* O(n) again.

**Variant A. Check Completeness of a Binary Tree (LC 958)** *(crosses into: the shape becomes the question)*
- **Question.** Return whether a binary tree is complete.
- **Scenario.** *Is the rack layout "properly packed": all layers full except the last, which is packed to the left? Validate it.*
- **Pattern and cost.** BFS including `None` slots; once a `None` appears, no real node may follow. O(n) time, O(w) space.

**Variant B. Complete Binary Tree Inserter (LC 919)** *(crosses into: array-backed layout)*
- **Question.** Design a structure initialised with a complete tree that supports `insert(val)` (keeping it complete, returning the new node's parent value) and `get_root()`.
- **Scenario.** *Add a new machine to the rack in the correct slot and report which machine it attaches to.*
- **Pattern and cost.** Keep a queue of nodes that still have a free child slot; O(1) per insert. A complete tree is also an array where the parent of index `i` is `(i - 1) // 2` (a heap).

---

### 34. All Nodes Distance K in Binary Tree (#34, LC 863)

**Original question.** Given the root, a target node and an integer `k`, return the values of all nodes at distance `k` from the target (distance = number of edges, in any direction).

**Scenario.** *An outbreak starts at one office. It spreads to anyone directly connected by a management line: to your manager, and to your reports. Which employees are exactly 2 reporting steps from the first case, in either direction?*

**Ask first.**
1. Is distance counted along reporting lines in both directions (up and down)?
2. Can `k` be 0, or larger than the structure?

**Spot it.** "Distance from X in **any** direction" includes going UP, which plain `left`/`right` can't do. Add parent links and the tree becomes an **undirected graph**: BFS with a visited set.

**Brute force.** For each node compute its distance to the target via LCA or paths: O(n * h), up to O(n^2).

**Solve** (from [34-all-nodes-distance-k.md](10-tree-as-a-graph/34-all-nodes-distance-k.md)):
```python
parent = {}
def build_parent_map(node, p):        # 1) DFS: child -> parent
    if not node: return
    parent[node] = p
    build_parent_map(node.left, node); build_parent_map(node.right, node)
build_parent_map(root, None)

queue, visited, current_distance = deque([target]), {target}, 0
while queue:                          # 2) BFS outward from the target
    if current_distance == k:
        return [node.val for node in queue]
    for _ in range(len(queue)):
        curr = queue.popleft()
        for neighbor in (curr.left, curr.right, parent[curr]):
            if neighbor and neighbor not in visited:
                visited.add(neighbor); queue.append(neighbor)
    current_distance += 1
return []
```
Returns the values left in the queue at distance `k`.

**Cost.** O(n) time (one DFS plus one BFS), O(n) space (map, visited, queue).

**Follow-up.** *"Why is visited needed?"* once parent links exist, a child points back to its parent: loops. *"Without the extra map?"* a recursive solution returning "distance to the target" (O(h) space). *"Many queries?"* keep the parent map.

**Variant A. Amount of Time for Binary Tree to Be Infected (LC 2385)**
- **Question.** The infection starts at the node with value `start` and spreads each minute to adjacent nodes (parent or children). Return the number of minutes for the whole tree to be infected.
- **Scenario.** *How many days until the whole company has caught it, if each day it spreads one management link in any direction from patient zero?*
- **Pattern and cost.** Parent map plus BFS, counting levels until the queue is empty (the answer is the max distance). O(n) time and space.

**Variant B. Vertices at distance k in a general graph** *(crosses into: the hierarchy gained cross-links)*
- **Question.** Given an undirected graph and a start vertex, return all vertices at shortest-path distance exactly `k`.
- **Scenario.** *The same outbreak, but some employees also have dotted-line links to other departments, so there is more than one way to reach someone.*
- **Pattern and cost.** It isn't a tree any more. BFS with a visited set is now **required**, not just convenient, and "distance" is the **shortest** route. O(V + E) time, O(V) space (Graphs 2.0 S29/S30).

---

### 35. Serialize and Deserialize Binary Tree (#35, LC 297)

**Original question.** Design an algorithm to serialize a binary tree to a string and deserialize that string back to the original tree.

**Scenario.** *A company's reporting structure must be saved to a text file and later restored exactly, with every person in the same position. The saved form must be a single line of text.*

**Ask first.**
1. Any constraints on the format (human-readable, size, negative numbers, a delimiter)?
2. Can values contain the delimiter? Is the structure huge?

**Spot it.** "Save a structure to a string and rebuild it" -> a traversal plus an explicit **null marker**, because values alone don't say where each side ends.

**Brute force.** Save inorder and preorder lists and rebuild with #29: needs unique values and stores 2n numbers. Preorder with markers stores each position exactly once.

**Solve** (from [35-serialize-and-deserialize-binary-tree.md](11-serialization/35-serialize-and-deserialize-binary-tree.md)):
```python
def serialize(self, root):
    vals = []
    def dfs(node):
        if not node:
            vals.append('N'); return          # null marker
        vals.append(str(node.val))
        dfs(node.left); dfs(node.right)       # preorder
    dfs(root)
    return ",".join(vals)

def deserialize(self, data):
    vals = data.split(',')
    self.i = 0
    def dfs():                                # returns: the rebuilt piece
        if vals[self.i] == "N":
            self.i += 1; return None
        node = TreeNode(int(vals[self.i])); self.i += 1
        node.left = dfs()                     # left before right, matching the write order
        node.right = dfs()
        return node
    return dfs()
```

**Cost.** O(n) time, O(n) space (`2n + 1` tokens, plus an O(h) stack).

**Follow-up.** *"A level-order (BFS) format?"* a queue instead of recursion; matches LeetCode's own format (not in your repo). *"Compact for a BST?"* Variant A. *"Very deep?"* iterative with a stack. *"Values contain commas?"* escape or length-prefix. *"Too big for memory?"* stream preorder directly to disk and read it back lazily.

**Variant A. Serialize and Deserialize BST (LC 449)**
- **Question.** Serialize and deserialize a BST, making the string as compact as possible.
- **Scenario.** *Save the ordered index to a file as compactly as you can.*
- **Pattern and cost.** The ordering makes null markers unnecessary: write the preorder values only, and rebuild with bounds (#29 Variant A). O(n) time, O(n) space, about half the tokens.

**Variant B. Serialize and Deserialize N-ary Tree (LC 428, premium)** *(crosses into: n-ary)*
- **Question.** Serialize and deserialize an n-ary tree.
- **Scenario.** *Save an org chart where managers can have any number of reports.*
- **Pattern and cost.** Preorder, writing each value followed by its child **count** (or a sentinel after the last child) instead of null markers. O(n) time and space.

---

### 36. Implement Trie (Prefix Tree) (#36, LC 208)

**Original question.** Implement a Trie with `insert(word)`, `search(word)` (is exactly this word stored?) and `startsWith(prefix)` (is any stored word starting with it?).

**Scenario.** *A shop's search box has 2 million product names. As the user types, show whether any product starts with what they've typed so far, and whether what they typed is an exact product name. Both checks must be fast regardless of catalog size.*

**Ask first.**
1. Which alphabet: lowercase only, Unicode, case-sensitive?
2. Do we also need delete, counts, or an upper limit on memory?

**Spot it.** "Starts with" and "shared beginnings" -> a tree whose edges are **characters**, one step per character. The cost depends on the typed length, not on how many words exist.

**Brute force.** A hash set gives exact search in O(L) but `startsWith` means scanning every word: O(N * L). A **sorted list + binary search** gives O(L log N), a legitimate alternative to mention.

**Solve** (from [36-implement-trie.md](12-trie-prefix-tree/36-implement-trie.md)):
```python
# A: TrieNode with children dict and is_end_of_word
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

def insert(self, word):
    curr = self.root
    for char in word:
        if char not in curr.children:
            curr.children[char] = TrieNode()
        curr = curr.children[char]
    curr.is_end_of_word = True

def search(self, word):               # path must exist AND end a word
    curr = self.root
    for char in word:
        if char not in curr.children: return False
        curr = curr.children[char]
    return curr.is_end_of_word

def startsWith(self, prefix):         # path must exist; word flag doesn't matter
    ...same walk...; return True

# B: nested dicts, '.' as the word-end sentinel (d['.'] = '.'; search checks '.' in d)
```
Returns a bool. Base: a missing character on the path -> `False`.

**Cost.** insert, search, startsWith are all O(L). Extra space: O(L) per insert for new nodes, O(1) for the lookups. Total space: O(total characters), because shared prefixes are stored once.

**Follow-up.** *"Delete a word."* clear the flag and prune dead branches. *"Autocomplete top-k."* store counts or top-k at nodes, or DFS under the prefix. *"Memory."* a radix/compressed trie; array-of-26 vs dict; disk-backed. *"Unicode."* dict children.

**Variant A. Replace Words (LC 648)**
- **Question.** Given a dictionary of roots (word stems) and a sentence, replace every word with the shortest root that is its prefix.
- **Scenario.** *A text cleaner has a list of word stems. Replace each word in a sentence with its shortest matching stem.*
- **Pattern and cost.** Insert the stems in a trie; for each word walk until the first `is_word`. O(total characters) time and space.

**Variant B. Longest Common Prefix (LC 14)** *(crosses into: a trie is overkill)*
- **Question.** Return the longest common prefix of an array of strings.
- **Scenario.** *Find the longest shared beginning of every product code in a batch.*
- **Pattern and cost.** A trie works (walk while there is one child and no word end) but is more machinery than needed. Compare the first and last of the sorted strings, or scan column by column. O(S) time where S is the total characters, O(1) space. Know where a trie stops paying off.

---

### 37. Design Add and Search Words Data Structure (#37, LC 211)

**Original question.** Design a structure that supports `addWord(word)` and `search(word)`, where `search` may contain `'.'` that matches any single letter.

**Scenario.** *A crossword helper stores a big word list. A solver types a pattern with some unknown letters shown as dots (never more than two) and asks whether any stored word fits.*

**Ask first.**
1. Does a dot match exactly one character? What's the maximum number of dots?
2. Must the pattern match the whole word (not just a prefix)?

**Spot it.** "A pattern with blanks over many words with shared beginnings" -> trie, where a literal letter follows one edge and a dot **branches into every child**.

**Brute force.** Scan every stored word and compare it to the pattern: O(N * L) per search (bucketing by length helps a little). The trie prunes whole branches.

**Solve** (from [37-design-add-and-search-words.md](12-trie-prefix-tree/37-design-add-and-search-words.md)):
```python
def search(self, word):
    def dfs(index, node):             # returns: does any stored word fit word[index:] under node?
        curr = node
        for i in range(index, len(word)):
            char = word[i]
            if char == '.':
                for child in curr.children.values():
                    if dfs(i + 1, child):
                        return True
                return False
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_word           # base: pattern consumed
    return dfs(0, self.root)

# B: nested dict version; in the dot branch skip the sentinel: `if key != '.' and dfs(i + 1, d[key])`
```
`addWord` is the same as #36's `insert`.

**Cost.** `addWord` O(L). `search`: O(L) with no dots; with `k` dots up to O(26^k * L), and in the worst case it can visit the whole trie. O(L) recursion stack.

**Follow-up.** *"Many dots?"* worst case scans everything; bucket by length first. *"Wildcard that matches many characters (`*`)?"* backtracking or DP. *"Prefix and suffix?"* Variant A.

**Variant A. Prefix and Suffix Search (LC 745)** *(crosses into: a trie of rotations)*
- **Question.** Design `WordFilter(words)` with `f(prefix, suffix)` returning the index of the word with the largest index that has both (or -1).
- **Scenario.** *Contact search: given how a name starts and how it ends, return the most recently added matching name.*
- **Pattern and cost.** For each word insert every `suffix + '{' + word` into one trie; query `suffix + '{' + prefix`. O(L^2) per word to insert, O(L) per query; space grows by a factor of L.

**Variant B. Map Sum Pairs (LC 677)** *(crosses into: data stored at nodes)*
- **Question.** Implement `insert(key, val)` (overwrites) and `sum(prefix)` returning the total of values of all keys starting with `prefix`.
- **Scenario.** *Sales are recorded per product code. Report the total sales across every code that starts with a given prefix.*
- **Pattern and cost.** Store a running total at every trie node; on overwrite add the *difference* along the path. insert and sum are O(L).

---

### 38. Word Search II (#38, LC 212)

**Original question.** Given an `m x n` board of letters and a list of words, return all words that can be formed by sequentially adjacent cells (horizontal or vertical), using each cell at most once per word.

**Scenario.** *A word-puzzle app has a grid of letters and a dictionary of 30,000 words. Find every dictionary word that can be traced by moving between touching cells, never reusing a cell within one word. Running a separate search for each word is far too slow.*

**Ask first.**
1. Are diagonals allowed? May a cell be reused within one word?
2. Can the dictionary contain duplicates? Does the output order matter?

**Spot it.** "Many words, shared beginnings, and a **path** through a space": build a trie of the words, then explore the grid once and abandon any path whose prefix isn't in the trie.

**Brute force.** Run a single-word search (LC 79) for each of W words from every cell: O(W * M * N * 3^(L-1)). One walk guided by a trie shares all the work between words with common prefixes.

**Solve** (from [38-word-search-ii.md](12-trie-prefix-tree/38-word-search-ii.md)):
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None              # full word stored at its last letter

def dfs(r, c, parent):                # returns nothing; appends to res
    char = board[r][c]
    curr = parent.children[char]
    if curr.word:
        res.append(curr.word); curr.word = None      # avoid duplicates
    board[r][c] = '#'                                # mark visited in place
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] in curr.children:
            dfs(nr, nc, curr)
    board[r][c] = char                               # backtrack
    if not curr.children:
        del parent.children[char]                    # prune exhausted branches

for r in range(ROWS):
    for c in range(COLS):
        if board[r][c] in root.children:
            dfs(r, c, root)
```

**Cost.** Worst case O(M * N * 3^(L-1)) (3 forward choices after the first step). Pruning brings it close to O(total letters in the grid) in practice. Space: O(W * L) for the trie plus O(L) recursion.

**Follow-up.** *"Don't mutate the board."* use a visited set (extra O(L) or O(M * N)). *"Huge dictionary, small board."* flip it: enumerate board paths up to length L and look each up in the trie or a set. *"Why prune the trie?"* so found words' branches are never re-searched.

**Variant A. Word Search (LC 79)** *(crosses into: no trie needed)*
- **Question.** Return whether a single word exists in the grid.
- **Scenario.** *Is one particular word hidden in the letter grid?*
- **Pattern and cost.** Plain backtracking from every cell, O(M * N * 3^L). A trie adds nothing for one word: it pays off only when many words share prefixes.

**Variant B. Concatenated Words (LC 472)** *(crosses into: DP)*
- **Question.** Return all words in the list that are concatenations of at least two shorter words from the same list.
- **Scenario.** *Find product names that are really two or more other product names glued together.*
- **Pattern and cost.** Word Break per word, using a set (or a trie) for prefix checks. O(N * L^2) time. The trie gives pruning, but the real engine is DP over prefixes.

---

## Part 5. Common traps to say out loud

1. **Forgetting the empty / null base case.** Say: *"First, what if this is empty?"* Pick the right "nothing" answer: `0` for count/height/sum, `True` for "all must hold", `False` for "does any exist", `None` for "find it", `float('-inf')` for a max that must lose to any real value. A node with **one** child has a `None` on the other side, so that base case is hit constantly.
2. **Height in nodes vs edges.** #1 counts nodes (leaf = 1); #7 counts edges (leaf = 0). Say which one you're returning *before* you code, and what an empty tree returns (0 or -1).
3. **Root-to-leaf vs any-to-any.** "Root to leaf" means check `not node.left and not node.right`. A node with one child is **not** a leaf (this is also the Minimum Depth trap, and why `if not node: return target == 0` gives false positives on `[1, 2]`). "Any-to-any" needs a global best plus a one-armed return (#7, #8).
4. **Using the BST property only locally.** Parent-vs-child is not enough: carry `(low, high)` or check that inorder is strictly increasing (#21). Decide on duplicates, and use `None`/`-inf`/`inf` bounds if values can equal INT_MIN/INT_MAX.
5. **Global variables not reset.** Set `self.res = 0` (or the `nonlocal` variable) **inside** the method, never once in `__init__` or the class body, or the second test case starts dirty. Better: return a tuple and avoid the global.
6. **Mutating the tree.** Invert, flatten, delete, Morris and Word Search II's `'#'` marking all change the input. Say so, restore what you must (Morris threads, the board cell), and offer a copy or a visited set if the input is shared.
7. **Recursion depth on a skewed tree.** Python's default is ~1000 frames. Say: *"If it can be a chain of 100k, I'll go iterative (stack or BFS)."* Don't offer `sys.setrecursionlimit` as the fix.
8. **Backtracking without the undo.** Mutable state passed down (a path list, the prefix-sum map in #13) must be undone after the recursive calls (`pop`, `-= 1`), and a stored path must be **copied**. Ints passed as arguments undo themselves.
9. **Value vs identity.** LCA's `root == p` compares nodes. With duplicate values compare identity, never `.val`.
10. **Inorder alone doesn't fix a shape.** Comparing inorder lists (same tree, symmetric) gives false positives. Preorder needs null markers (#35). Two traversals rebuild a tree only if values are unique and one is inorder (#29, #30).
11. **BFS slips.** Take the `len(queue)` snapshot *before* the inner loop; use `deque` (`list.pop(0)` is O(n)); never reverse the queue itself for zigzag, reverse the finished level.
12. **Trie slips.** `search` needs the end-of-word flag, `startsWith` doesn't. In the nested-dict version, the `'.'` sentinel and the `'.'` wildcard collide unless you skip the sentinel key (#37). Mention memory per node.
13. **Treating a graph as a tree.** Parent pointers, cross-links, second managers: you need a visited set (#34). Check "one parent each, no loops" before assuming a tree.
14. **Complexity slips.** Say **O(h)**, then "which is log n if balanced and n if skewed", never a bare O(log n). Watch hidden costs: slicing is O(n) per call, `.index()` is O(n), string building in serialization can be O(n^2).

---

## Part 6. Known gaps (not written up yet)

**Mismatches in the repo itself (fix or be ready for them):**

- **No Morris inorder.** problems.md lists #20 as "explicit stack + Morris", but the write-up has no Morris code (only #32 uses a Morris-style rewiring). The code is in #20's Follow-up above.
- **LC 117 with O(1) space** isn't covered: #18's O(1) version works only for the *perfect* tree (LC 116). The general version is in #18's Follow-up above.
- **#13 space claim:** the write-up says O(h), but leftover zero-count keys can make the dict O(n). Delete the key at 0 (see #13).
- **#6 write-up** discusses the top-down code but only contains the bottom-up solution.
- **No n-ary tree at all.** Every file uses `left`/`right`. Reporting lines, folders, menus and comments are n-ary in Google-style questions.
- **No BST search / insert** write-up (README mentions it; only delete #25 exists).

**Important problems missing, in the order I'd write them up:**

| Priority | Problem | Why it matters |
|---|---|---|
| 1 | **LC 700 / 701** BST search, insert | the basics are not written up; every BST variant assumes them |
| 2 | **N-ary basics:** LC 429, 559, 589/590, 1522 | covers the "any number of children" scenarios; `for child in children` |
| 3 | **LC 113 / 257** Path Sum II, Binary Tree Paths | backtracking with a path list (append, recurse, pop) |
| 4 | **LC 642** Design Search Autocomplete System | the classic Google trie question: top-k at each prefix |
| 5 | **LC 652** Find Duplicate Subtrees | serialization + hashing for "same layout appears twice" |
| 6 | **LC 1376** Time Needed to Inform All Employees, **LC 690** Employee Importance | a literal org chart: n-ary DFS from a parent array |
| 7 | **LC 285 / 270** Inorder Successor, Closest BST Value | BST search path, O(h) |
| 8 | **LC 99** Recover BST (with Morris) | inorder + prev + O(1) space |
| 9 | **LC 1123 / 1644 / 1676** LCA variants | the LCA follow-ups Google pushes on |
| 10 | **LC 662** Maximum Width, **LC 111** Minimum Depth, **LC 993** Cousins | position indices; the one-child-is-not-a-leaf trap |

**Also worth adding:**

- **Path / DP:** LC 298 longest consecutive, LC 687 longest univalue path, LC 1372 longest zigzag, LC 968 Binary Tree Cameras (the repo promises it), LC 1026, LC 1339.
- **BST:** LC 653 Two Sum IV, LC 669 Trim, LC 1382 Balance, LC 333 Largest BST Subtree, LC 538, LC 96 / 95 Unique BSTs (DP).
- **Construction / serialization:** LC 449 (BST), LC 428 (n-ary), LC 1008, LC 889, LC 331, LC 654.
- **Nested structure and "file system" scenarios:** LC 341 Flatten Nested List Iterator, LC 339 Nested List Weight Sum, LC 588 Design In-Memory File System (trie), LC 1233 Remove Sub-Folders, LC 2331 Evaluate Boolean Binary Tree and expression-tree design (the "an expression" scenario).
- **Trie:** LC 648 Replace Words, LC 677 Map Sum, LC 720 Longest Word in Dictionary, LC 745, LC 1268 Search Suggestions System, LC 421 (bitwise trie), LC 472.
- **Tree as a graph:** LC 2385 (time to infect), LC 1245 (tree diameter), LC 1361 (valid binary tree nodes); neighbours in Graphs 2.0: S14 (Minimum Height Trees), S16 (Redundant Connection), S17 (Graph Valid Tree).
- **Level / shape:** LC 107, 958 (completeness), LC 515.

**Deliberately out of scope** (per problems.md): segment trees / Fenwick trees, AVL / red-black rotations, B-trees, suffix trees.
