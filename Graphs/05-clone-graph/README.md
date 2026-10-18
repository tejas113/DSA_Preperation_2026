# Group 05 — Hashmap + Traversal (structural copy)

## What this pattern is

You're handed a graph built out of actual node objects (not just ids), and asked
to produce a **deep copy** — an entirely new set of node objects with the same
structure, sharing no references with the original.

The tool: a **hashmap from old node → new node**, filled in as you traverse. This
map does **three jobs at once**:
1. It's the "have I already made a copy of this node?" check (i.e. it **is** your
   visited set).
2. It's how you find the right new-node object to attach as a neighbor, without
   creating duplicates.
3. It's what lets you handle **cycles** safely — a graph, unlike a tree, can have
   cycles, so "visited" is not optional here the way it might feel optional on a
   simple tree copy.

## How to recognize it

- "Deep copy this graph/structure," where nodes hold direct references to their
  neighbors (not ids).
- The structure may contain cycles (that's precisely why you need the map, not
  just recursion).
- You need the *same shape*, but entirely new objects.

## The template

```python
def clone(start):
    old_to_new = {}

    def dfs(node):
        if node in old_to_new:            # already cloned -> return the existing copy
            return old_to_new[node]

        copy = Node(node.val)
        old_to_new[node] = copy           # register BEFORE recursing into neighbors!
        for nei in node.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy

    return dfs(start) if start else None
```

**The one rule that makes this safe on cyclic graphs:** register `old_to_new[node]
= copy` **before** recursing into that node's neighbors. If a neighbor's path
leads back to `node` (a cycle), the recursive call finds `node` already in the
map and returns the existing copy instead of infinitely recursing.

## Complexity

- **Time:** `O(V + E)` — each node cloned once, each edge attached once.
- **Space:** `O(V)` for the map (doubling as both output and visited-set), plus
  `O(V)` recursion stack worst case.

## Problems

1. `01-clone-graph.md` — the pattern in its purest form (LeetCode 133).
