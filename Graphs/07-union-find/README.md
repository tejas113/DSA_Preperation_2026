# Group 07 — Union-Find (Disjoint Set Union)

## What this pattern is

A second way to think about **connectivity** — different from Group 01/04's
flood-fill. Instead of *searching* the graph to see what's connected, you
*merge* groups as edges arrive, and ask "same group?" in near-constant time.

Full mechanics: `concepts/08-union-find.md`. This group is five problems that are
all thin wrappers around the canonical `DSU` class.

## How to recognize it

- Edges arrive **one at a time**, and you need connectivity *during* the process
  (not just at the end).
- "Which edge creates a cycle / is redundant?" (undirected).
- "How many groups / provinces / friend circles / connected components?"
- "Is this a valid tree?" (connected **and** acyclic).
- Many "are X and Y connected?" queries against one graph.
- Kruskal's MST (Group 12).

If instead you need the *path* between two nodes, or the graph is *directed*, use
BFS/DFS — DSU only knows "same undirected component," not routes or direction.

## The canonical class (identical in every file of this group)

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                   # already connected
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True
```

Some problems add a `size` array (attach smaller under larger, track group
sizes). Those are noted per problem.

## The two idioms this group uses over and over

1. **Cycle / redundancy detection:** `union(u, v)` returns `False` ⟺ `u` and `v`
   were already connected ⟺ edge `(u, v)` closes a cycle.
2. **Component counting:** start `count = n`; every `union` that returns `True`
   does `count -= 1`.

## Complexity for the whole group

- **Time:** `O(E · α(V))` ≈ `O(E)` — amortized near-constant per `find`/`union`.
- **Space:** `O(V)` for the `parent` (and `rank`/`size`) arrays.

## Problems

1. `01-redundant-connection.md` — return the edge that closes a cycle. The purest
   use of idiom #1 (LeetCode 684). **Start here.**
2. `02-graph-valid-tree.md` — a tree ⟺ exactly `n-1` edges **and** no cycle
   (LeetCode 261, premium).
3. `03-number-of-connected-components.md` — idiom #2, verbatim (LeetCode 323,
   premium).
4. `04-number-of-provinces.md` — component counting where the graph is given as
   an adjacency **matrix** (LeetCode 547).
5. `05-accounts-merge.md` — DSU over **strings** (emails): remap to integer ids,
   union accounts that share an email, then group and sort (LeetCode 721).
