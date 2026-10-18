# Clone Graph  ·  LeetCode 133  ·  Medium

Group 05 — Hashmap + Traversal (structural copy)  ·  the pattern in its purest
form: an **old-node → new-node map** that is simultaneously your visited set
*and* your output.

Prereqs: `concepts/03`/`04` (BFS/DFS), `04-graph-traversal-connectivity` (your
first non-grid graph). New idea: **the visited structure and the thing you're
building are the same object.**

---

## 1. Problem

You're given a reference to a node in a **connected, undirected** graph. Each
`Node` has an integer `val` and a list `neighbors` of the `Node` objects it's
directly connected to.

**Return a deep copy (clone) of the graph** — a completely new set of `Node`
objects with the same values and the same connections, sharing no references
with the original.

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

Constraints:
- The number of nodes is in `[0, 100]`.
- Each node's value is unique, `1 <= Node.val <= 100`.
- No repeated edges, no self-loops.
- The graph is connected.

Example — a 4-node square, `1-2, 2-3, 3-4, 4-1`:

```
node 1's neighbors: [2, 4]
node 2's neighbors: [1, 3]
node 3's neighbors: [2, 4]
node 4's neighbors: [1, 3]
```

The clone must have the identical shape — but every single `Node` object in it
must be a **new** object, not one of the originals.

---

## 2. Explain Like I'm 5

Imagine a friend-group where everyone is holding hands in a circle (or any tangle
of hand-holding — it doesn't have to be a simple circle). You want to build an
**exact duplicate** of this whole group of people, holding hands in the same
pattern — but using **brand new people**, not the originals.

You walk up to person `1`, make a brand-new twin of them, and write down on a
clipboard: *"original 1 → twin 1."* Then you look at who `1` is holding hands
with, say person `2`. You check your clipboard: have I already made a twin of
`2`? If not, make one, write it down, and connect twin-1 to twin-2. Then go visit
`2`'s other hand-holding friends, and so on.

Here's the important bit: since people are holding hands in a **loop**, you'll
eventually walk back around to person `1` again through someone else. When that
happens, you check your clipboard, see *"oh, I already made a twin of 1,"* and
just connect to the **existing** twin instead of accidentally making a second
one. The clipboard (your map) is what stops you from getting stuck walking around
the loop forever, and it's what stops you from creating duplicate twins.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Deep copy" a structure made of node objects with direct references | ✅ |
| The structure can contain **cycles** (not a tree) | ✅ — a connected undirected graph is not acyclic in general |
| You need genuinely **new objects**, same shape | ✅ |

**Reduce it to:** *"DFS or BFS traversal where the visited-set is a dict from old
node to new node; check-then-create-then-register, and always register before
recursing further."*

**Look-alikes:**
- A tree has no cycles, so a naive recursive copy (no map at all) would still
  terminate — but you'd still want the map if the "tree" might actually share
  subtrees (a DAG). A general graph *always* needs it.
- Copy List with Random Pointer (LeetCode 138) — the *exact same* map idea,
  applied to a linked list with an extra pointer instead of a graph node with a
  neighbor list (Scenario 1).

---

## 4. Intuition

1. Cloning one node in isolation is trivial: `Node(original.val)`.
2. The hard part is **wiring up neighbors correctly** without creating duplicate
   copies of a node you've already cloned, and without recursing forever around a
   cycle.
3. Both problems are solved by the same tool: a **map from original node → its
   clone**. Before making a new clone, check the map. If it's there, reuse it.
4. **The critical ordering:** register the new clone in the map **before**
   recursing into that node's neighbors. If you wait until after, and the
   neighbor traversal loops back to the same node (which it will, in any graph
   with a cycle — and a connected graph with `≥ 3` nodes and no bridges will have
   one), you'd recurse into it again, infinitely.
5. Once every node has been cloned (and registered) exactly once, wiring up
   `copy.neighbors` is just: for each original neighbor, look up its clone in the
   map and append it.

**A relief, for once:** the constraint caps the graph at **100 nodes**. Unlike
several earlier problems (Shortest Bridge, Pacific Atlantic — up to `40,000`
cells), recursion depth here is a complete non-issue. Always check the actual
constraints before reflexively worrying about recursion limits.

---

## 5. Approach (primary): recursive DFS with an old→new map

1. If `node` is `None` (empty graph): return `None`.
2. `old_to_new = {}`.
3. Define `dfs(n)`:
   - If `n` is already a key in `old_to_new`: return `old_to_new[n]` (already
     cloned — reuse it, don't make a duplicate, don't recurse again).
   - `copy = Node(n.val)`.
   - `old_to_new[n] = copy` — **register now, before recursing.**
   - For each `nei` in `n.neighbors`: `copy.neighbors.append(dfs(nei))`.
   - Return `copy`.
4. Return `dfs(node)`.

Builds on: `concepts/04` (DFS), generalized so the "visited check" and "the thing
being built" are the same dict.

---

## 6. Pseudocode

```
function cloneGraph(node):
    if node is None: return None
    old_to_new = empty map

    function dfs(n):
        if n in old_to_new: return old_to_new[n]
        copy = new Node(n.val)
        old_to_new[n] = copy                  # register BEFORE recursing
        for nei in n.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy

    return dfs(node)
```

---

## 7. Dry Run

Graph: `1:[2,4]`, `2:[1,3]`, `3:[2,4]`, `4:[1,3]` (the 4-node square). Start
`dfs(1)`.

| call | in map? | action | `old_to_new` keys after |
|---|---|---|---|
| dfs(1) | no | make copy1; **register 1** | {1} |
| dfs(2) *(from 1)* | no | make copy2; **register 2** | {1,2} |
| dfs(1) *(from 2)* | **yes** | return copy1 — no new work, no infinite loop | {1,2} |
| dfs(3) *(from 2)* | no | make copy3; **register 3** | {1,2,3} |
| dfs(2) *(from 3)* | **yes** | return copy2 | {1,2,3} |
| dfs(4) *(from 3)* | no | make copy4; **register 4** | {1,2,3,4} |
| dfs(1) *(from 4)* | **yes** | return copy1 | {1,2,3,4} |
| dfs(3) *(from 4)* | **yes** | return copy3 | {1,2,3,4} |
| — copy4.neighbors = [copy1, copy3]; dfs(4) returns copy4 | | | |
| — copy3.neighbors = [copy2, copy4]; dfs(3) returns copy3 | | | |
| — copy2.neighbors = [copy1, copy3]; dfs(2) returns copy2 | | | |
| dfs(4) *(from 1's 2nd neighbor)* | **yes** | return copy4 (already registered) | {1,2,3,4} |
| — copy1.neighbors = [copy2, copy4]; dfs(1) returns copy1 | | | |

Final clone: `copy1:[copy2,copy4]`, `copy2:[copy1,copy3]`, `copy3:[copy2,copy4]`,
`copy4:[copy1,copy3]` — same shape as the original, entirely new objects.
Notice the cycle (`1→2→...→1`) was crossed **three separate times** during the
traversal, and each time the map caught it and returned the existing copy instead
of recursing again. ✅

---

## 8. Python Code (primary — recursive DFS + map)

```python
from typing import Optional


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None

        old_to_new = {}

        def dfs(n: 'Node') -> 'Node':
            if n in old_to_new:
                return old_to_new[n]

            copy = Node(n.val)
            old_to_new[n] = copy            # register BEFORE recursing into neighbors
            for nei in n.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy

        return dfs(node)


# --- test helpers: LeetCode gives Node objects, not primitives, so we need a
# --- way to build a graph from a simple adjacency list and to read one back
# --- out for comparison. ---

def build_graph(adj):
    """adj[i] is the list of 1-indexed neighbor values for node i+1."""
    if not adj:
        return None
    nodes = {i + 1: Node(i + 1) for i in range(len(adj))}
    for i, neighbor_vals in enumerate(adj):
        nodes[i + 1].neighbors = [nodes[v] for v in neighbor_vals]
    return nodes[1]


def to_adjlist(start):
    """BFS the graph, return {val: sorted neighbor vals} for structural comparison."""
    if start is None:
        return {}
    seen = {start.val: start}
    q = [start]
    result = {}
    while q:
        node = q.pop()
        result[node.val] = sorted(n.val for n in node.neighbors)
        for nei in node.neighbors:
            if nei.val not in seen:
                seen[nei.val] = nei
                q.append(nei)
    return result


if __name__ == "__main__":
    sol = Solution()

    original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
    clone = sol.cloneGraph(original)

    assert to_adjlist(clone) == to_adjlist(original)   # same shape
    assert clone is not original                        # different object

    # confirm every cloned node is a NEW object, not a reused original
    orig_ids = {id(n) for n in [original] + original.neighbors}
    seen_clone, stack = set(), [clone]
    while stack:
        n = stack.pop()
        if id(n) in seen_clone:
            continue
        seen_clone.add(id(n))
        assert id(n) not in orig_ids
        stack.extend(n.neighbors)

    assert sol.cloneGraph(None) is None                 # empty graph

    single = build_graph([[]])                          # one node, no neighbors
    single_clone = sol.cloneGraph(single)
    assert single_clone.val == 1 and single_clone.neighbors == []
    assert single_clone is not single

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. BFS with the same map

```python
from collections import deque
from typing import Optional


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None

        old_to_new = {node: Node(node.val)}     # seed: mark on "enqueue" as usual
        q = deque([node])

        while q:
            curr = q.popleft()
            for nei in curr.neighbors:
                if nei not in old_to_new:
                    old_to_new[nei] = Node(nei.val)
                    q.append(nei)
                old_to_new[curr].neighbors.append(old_to_new[nei])

        return old_to_new[node]
```

Same complexity, same map. Marking `old_to_new[nei] = Node(nei.val)` at the
moment you first see `nei` (before it's ever dequeued) is exactly the "mark on
enqueue" rule from `concepts/03`'s appendix — here the "mark" *is* creating the
clone, one more example of a visited-mark doing double duty.

### The BFS↔DFS answer the interviewer wants

> "Either works, both `O(V+E)` — this is pure traversal-with-construction, no
> shortest-path requirement. I'd mention that with only up to 100 nodes,
> recursion depth is a non-issue here (unlike some of our grid problems), so
> either style is equally safe to write."

---

## 10. Complexity — derived step by step

**V and E:** node = a graph `Node`, `V ≤ 100`; edge = an entry in some node's
`neighbors` list, `E` = total edges (each undirected edge appears in two
neighbor lists).

**Time:**
- Each node is cloned **exactly once** (the map check prevents duplicates) →
  `O(V)`.
- Each node's neighbor list is iterated once to build the clone's neighbor list
  → summed over all nodes, `O(E)`.
- **Total: `O(V + E)`.**

**Space:**
- `old_to_new` map: `O(V)` entries — this **is** both the visited set and (via
  its values) the entire output graph.
- Recursion stack (DFS) / queue (BFS): `O(V)` worst case.
- **Total: `O(V)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `node is None` (empty graph) | explicit early `return None` |
| Single node, no neighbors | `dfs`/BFS clones just that one node, empty `neighbors` list |
| A cycle passes through the start node itself | the map check on the very first re-visit of `node` returns the already-registered copy — no special-casing needed |
| Graph is a single node referencing itself (a self-loop) — not possible per constraints, but... | ...the register-before-recurse rule would still handle it correctly if it were |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Registering the copy in the map *after* recursing into neighbors instead
      of before.** Symptom: `RecursionError` (infinite recursion) the instant the
      graph has any cycle — which, given the problem guarantees a *connected*
      graph, is essentially always, for any non-trivial input.
- [ ] **Appending the original neighbor instead of its clone.** Writing
      `copy.neighbors.append(nei)` instead of `copy.neighbors.append(dfs(nei))`
      (or the map lookup, in the BFS version). This silently produces a "clone"
      whose neighbor list points at the **original** objects — it looks
      structurally right if you only check `.val`s, but it's not a real deep
      copy, and mutating the "clone" would corrupt the original graph.
- [ ] **Creating a new clone every time a node is visited**, instead of checking
      the map first. Produces multiple distinct copy-objects for the same
      original node — wrong shape (the same logical node now appears as several
      different objects in different neighbor lists), and can still infinite-loop
      if the check-then-create ordering is also wrong.
- [ ] **Forgetting the `node is None` check.** Crashes immediately on the empty
      graph test case.
- [ ] **Testing pitfall (not a code bug):** comparing cloned vs. original graphs
      with `==` — `Node` has no custom `__eq__`, so this compares object
      identity, which is *always* `False` for a real clone and tells you
      nothing. You must traverse both graphs and compare `val`s/shape (as the
      `to_adjlist` helper above does), and separately assert the objects are
      *not* identical, to actually verify a deep copy.

---

## 13. Learnings & Transfer

**The reusable core: the visited structure and the output can be the same
object.**

You've now seen this "one structure, multiple jobs" idea in several forms:

| Problem | The dual-duty structure |
|---|---|
| Flood Fill | the recolored cell — visited mark *and* the answer |
| Making a Large Island | the `label` grid — visited mark *and* component id *and* size lookup key |
| Walls and Gates / 01 Matrix | the distance grid — visited mark *and* the answer |
| **Clone Graph** | the `old_to_new` map — visited set *and* the literal output object |

**"Register before recursing"** is the general fix for constructing something
recursively over a graph that might contain cycles — the same core idea as "mark
visited before diving deeper," just applied to a map whose *values* are the thing
you're building, not booleans.

| Situation | How this transfers |
|---|---|
| Copy List with Random Pointer (LC 138) | identical old→new map pattern, on a linked list with 2 pointers per node instead of a graph node with a neighbor list |
| Clone an N-ary tree | same idea, simpler (no cycles, so the map is really just for correctness-by-habit, not strictly required) |
| Serialize/deserialize any node-and-reference structure | assign each node an id via the same traversal-with-map idea (node → id instead of node → copy), then rebuild in a second pass using id → new-node |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Now clone a linked list where each node has a `next` pointer AND a `random` pointer that can point to *any* node in the list (or `None`)." *(this is LeetCode 138, a very common real follow-up)*

- **(b) Pattern:** the exact same old-node → new-node map technique, just with
  two pointers per node instead of a variable-length neighbor list.
- **(c) Adapt:** `old_to_new = {}`. First pass: walk the list via `next`,
  creating `old_to_new[node] = Node(node.val)` for every node (or do it lazily
  with the same recursive check-then-create as Clone Graph). Second pass (or
  during the same lazy recursion): for each original node, set
  `copy.next = old_to_new.get(node.next)` and
  `copy.random = old_to_new.get(node.random)`. `O(n)` time and space.
- **(d) Say:** "This is the identical pattern — an old→new map preventing
  duplicate clones — just with a fixed 2-pointer shape instead of an arbitrary
  neighbor list. Recognizing 'this is Clone Graph again' is the whole trick."

### Scenario 2 — "The input isn't guaranteed connected — you're given a *list* of starting nodes, each possibly in a different component, and must clone everything reachable from any of them."

- **(b) Pattern:** the loop-and-flood skeleton from Groups 01/04, applied here.
- **(c) Adapt:** keep **one shared** `old_to_new` map across all starting nodes.
  For each start node not already a key in the map, run the same `dfs`/BFS from
  it. The shared map guarantees no node is ever cloned twice, even if two
  "different" start nodes secretly belong to the same component.
- **(d) Say:** "Multi-source cloning is just the ordinary loop-and-flood
  skeleton, wrapped around the same clone routine, sharing one map so work is
  never duplicated across starts."

### Scenario 3 — "Only clone the part of the graph within `K` hops of the start node; drop any edge that would point outside that radius."

- **(b) Pattern:** combine this problem's map with Group 02's **leveled BFS**
  (track distance, stop expanding past a cutoff).
- **(c) Adapt:** BFS from the start, tracking each node's distance; only create
  a clone (and add it to the map) for nodes with `distance <= K`. When wiring a
  cloned node's neighbor list, only include a neighbor if it's **also** in the
  map (i.e., also within `K` hops) — an edge to an excluded node is silently
  dropped because there's no clone to point to. `O(nodes within K hops)` instead
  of `O(V + E)`.
- **(d) Say:** "Bounding a traversal by distance and bounding *what gets built*
  by the same distance are the same change — only register/clone nodes that pass
  the distance check, and neighbor-wiring naturally excludes everything else."

### Scenario 4 — "Clone the graph using `O(1)` *additional* space (beyond the required output) — you may temporarily mutate the original graph if you restore it afterward."

- **(b) Pattern:** a judgment call about whether a classic space trick applies.
- **(c) Adapt:** for the **linked-list** version (LC 138) there's a well-known
  `O(1)`-extra-space trick: splice each clone directly after its original in the
  `next` chain, use those interleaved clones to resolve `random` pointers without
  any map, then de-interleave to restore the original list and detach the
  clones. For a **general graph**, this doesn't transfer cleanly — there's no
  single "next chain" to splice into; a node's neighbor list has no fixed slot to
  temporarily insert a paired clone into without ambiguity. The honest answer:
  name the linked-list trick, explain *why* it relies on the list's linear
  `next`-pointer shape, and conclude that for a general graph the hashmap
  approach's `O(V)` space is close to necessary (you fundamentally need to
  remember which nodes you've already cloned).
- **(d) Say:** "Recognizing when a clever space trick is shape-specific (works on
  a linked list because of its single-`next`-pointer structure) versus when it
  generalizes is itself a signal of understanding, not just knowing tricks."

### Scenario 5 — "Serialize the graph to a string (for storage or network transfer), and later deserialize it back into an equivalent graph."

- **(b) Pattern:** the same old→new map idea, but mapping to **ids** instead of
  copy objects, in both directions.
- **(c) Adapt:** **Serialize:** traverse once (DFS/BFS), assigning each node a
  sequential id via a `node → id` map (built exactly like `old_to_new`, just
  storing an `int` instead of a `Node`); write out `"id:val:neighbor_id,neighbor_id,..."`
  lines. **Deserialize:** parse pass 1 — create every `Node` first, building an
  `id → Node` map; parse pass 2 — wire up each node's `neighbors` list by looking
  up neighbor ids in that map. `O(V + E)` both ways.
- **(d) Say:** "Serialization is the same map-based traversal, just swapping
  'clone object' for 'assign an id' — and deserialization is the mirror image,
  building all nodes first, then wiring references via the id map."

### Scenario 6 — "Multiple threads clone overlapping subgraphs of the same shared graph concurrently. Ensure no node is ever cloned twice due to a race."

- **(b) Pattern:** the `old_to_new` map becomes shared mutable state accessed by
  multiple threads — a concurrency problem layered on top of the graph problem.
- **(c) Adapt:** use a thread-safe **compute-if-absent** operation on the map
  (e.g., a lock guarding "check the map, and if missing, create + insert" as one
  atomic unit, or a concurrent map with a native `computeIfAbsent`). Without
  this, two threads can both see "not yet cloned" for the same node and each
  create a separate copy — a classic **check-then-act race condition**, the same
  category of bug as unsynchronized double-checked locking.
- **(d) Say:** "The map's 'check, then create-and-register' step has to be a
  single atomic operation once it's shared across threads — this is the same
  check-then-act race that shows up in any concurrent memoization or
  singleton-initialization pattern, just wearing a graph-cloning costume."

---

## 15. Flashcards

**Q:** The core trick of this problem, in one line?
**A:** An old-node → new-node map that is simultaneously the visited set **and**
the literal output being constructed.

**Q:** The single most important ordering rule, and what breaks without it?
**A:** Register the new clone in the map **before** recursing into its
neighbors. Skip this and any cycle causes infinite recursion.

**Q:** The sneaky bug that "looks" correct but isn't?
**A:** Appending the *original* neighbor object instead of its clone —
structurally looks fine by value, but shares references with the input, so it
isn't a real deep copy.

**Q:** Why is recursion depth a non-issue here, unlike several earlier grid
problems?
**A:** The constraint caps the graph at 100 nodes — always check the actual
constraints rather than reflexively assuming recursion is risky.

**Q:** Time and space, with derivation?
**A:** `O(V + E)` time (each node cloned once, each edge wired once), `O(V)`
space (the map holds one entry per node; that's also effectively the output).

**Q:** How does this generalize to Copy List with Random Pointer (LC 138)?
**A:** Identical old→new map technique; just two pointers per node (`next`,
`random`) instead of a variable-length neighbor list.

**Q:** How would you serialize/deserialize a graph using this same idea?
**A:** Serialize: traverse once, map node → sequential id, write out each node's
id/val/neighbor-ids. Deserialize: create all nodes first (id → Node map), then a
second pass wires up neighbors via that map.

**Q:** How do you actually *test* that a clone is deep, not shallow?
**A:** Traverse both graphs and compare `val`s/shape (never compare `Node`
objects with `==` — no custom equality is defined), and separately confirm none
of the cloned objects are identical (`is`) to any original object.

---

## Appendix — Tejas's LeetCode Practice Answer

> 🔁 Flagged for revision — see `problem-sources.md`.

Solved and accepted on LeetCode. Recursive DFS with the old→new map, registering
before recursing — matches the primary solution's structure almost line for
line. `O(V + E)` time, `O(V)` space.

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        old_to_new = {}

        def dfs(curr_node):
            if curr_node in old_to_new:
                return old_to_new[curr_node]

            copy = Node(curr_node.val)
            old_to_new[curr_node] = copy

            for neighbours in curr_node.neighbors:
                copy.neighbors.append(dfs(neighbours))

            return copy

        return dfs(node)
```

**Correct** — verified against the full test suite (structural equality, object
identity, empty graph, single node).
