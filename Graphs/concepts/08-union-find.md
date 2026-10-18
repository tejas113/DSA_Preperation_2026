# Concept 08 — Union-Find (Disjoint Set Union, "DSU")

## Quick Card

Union-Find answers **"are these two things in the same group?"** and **"merge
these two groups"** — both in *near-constant* amortized time — while groups are
built up **incrementally** (edges arriving one at a time).

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))     # parent[x] = x means "x is its own group's root"
        self.rank = [0] * n              # rough tree height, for balancing

    def find(self, x):                    # which group is x in? (returns the root)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression (halving)
            x = self.parent[x]
        return x

    def union(self, a, b):               # merge a's group and b's group
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                  # already same group -> this edge is redundant / a cycle
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra              # attach the shorter tree under the taller one
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True                       # a real merge happened (two groups became one)
```

**The killer idiom:** `union(a, b)` returns `False` when `a` and `b` were
*already* connected — meaning the edge `(a, b)` closes a cycle / is redundant.
Half of Group 07 is built on that one boolean.

**Complexity:** `m` operations on `n` elements → `O(m · α(n))`, where `α(n)` (the
inverse Ackermann function) is `≤ 4` for any `n` in the physical universe. Treat
each `find`/`union` as **amortized O(1)**. Space: `O(n)`.

**Reach for DSU when:** edges arrive incrementally and you need connectivity
*during* the process; you have many "same group?" queries on a graph; you're
detecting the first cycle-closing edge in an undirected graph; or you're doing
Kruskal's MST.

---

## Full tutorial

### 1. The mental model: a forest of "who's my boss" pointers

Every element starts in its **own** group, pointing at itself. `parent[x]` is
"the element one step closer to my group's leader." Follow `parent` pointers up
until you reach an element that points to itself — that's the **root**, the
unique id of the whole group.

```
Initially:   0   1   2   3   4        (5 lonely groups, each parent[x] = x)

union(0,1):  1        2   3   4
             |
             0                          (0's root is now 1)

union(2,3):  1     3      4
             |     |
             0     2

union(0,2):  1          4
            / \
           0   3
               |
               2                        (find(0)==find(2)==1 now)
```

- **`find(x)`** = walk up to the root. "Which group is `x` in?" → the root's id.
- **`union(a, b)`** = find both roots; if different, hang one root under the
  other. Now everything in both groups shares a root.
- **Same group?** → `find(a) == find(b)`.

### 2. Why the two optimizations matter

Without them, a chain of `union`s can build a tall skinny tree
(`0→1→2→3→...→n`), making `find` cost `O(n)`. Two cheap fixes make it
effectively `O(1)`:

**Path compression** (in `find`): as you walk up to the root, re-point nodes
closer to the top. The line `self.parent[x] = self.parent[self.parent[x]]` is
"path halving" — every node on the path gets pointed at its grandparent. Next
`find` on any of them is much shorter.

**Union by rank** (in `union`): always attach the *shorter* tree under the
*taller* one, so the combined tree stays as flat as possible. `rank[x]` is an
upper bound on the height of `x`'s tree; it only increases when two trees of
*equal* rank merge.

With **both**, the amortized cost per operation is `O(α(n))` — provably
near-constant.

> A common simpler variant is **union by size** (track group sizes, attach the
> smaller group under the larger). It gives the same `O(α(n))` guarantee and the
> size array is often useful anyway (e.g. "how big is this group?"). Use whichever
> the problem makes convenient; this repo uses rank as the default and switches to
> size when a problem needs group sizes.

### 3. The `union` return value — a cycle detector for free

In an **undirected** graph, process edges one at a time with `union(u, v)`:

- Returns `True` → `u` and `v` were in different components; this edge **joined**
  them (a real "tree" edge).
- Returns `False` → `u` and `v` were **already connected**; a path between them
  already existed, so this edge creates a **cycle** — it's redundant.

```python
dsu = DSU(n)
for u, v in edges:
    if not dsu.union(u, v):
        print("edge", (u, v), "closes a cycle")
```

This is exactly Redundant Connection, and the backbone of Graph Valid Tree,
Number of Connected Components, and Kruskal's MST.

### 4. Counting components with DSU

Start `count = n` (everything separate). Every **successful** `union` (returns
`True`) merges two groups into one → `count -= 1`.

```python
dsu = DSU(n)
count = n
for u, v in edges:
    if dsu.union(u, v):
        count -= 1
# count == number of connected components
```

To connect *everything*, you need `count - 1` more edges.

### 5. Dry run — Redundant Connection style

`n = 3`, edges `[(1,2), (2,3), (1,3)]` (1-indexed; use `DSU(n + 1)` and ignore
index 0, or remap).

| edge | find(u) | find(v) | union result | parent after |
|---|---|---|---|---|
| (1,2) | 1 | 2 | `True` (merge) | `parent[2]=1` |
| (2,3) | find(2)→1 | 3 | `True` (merge) | `parent[3]=1` |
| (1,3) | 1 | find(3)→1 | **`False`** — already connected | (unchanged) |

Edge `(1,3)` is the redundant one — the first edge whose two endpoints were
already in the same component.

### 6. When DSU beats flood-fill (BFS/DFS)

| Situation | Winner |
|---|---|
| One static graph, count components once | tie — both `O(V+E)` |
| Edges arrive **incrementally**, answer connectivity **as you go** | **DSU** — `O(α(n))` per edge vs re-running BFS `O(V+E)` each time |
| Many "are u and v connected?" queries on a fixed graph | **DSU** — precompute once, each query `O(α(n))` |
| "Which edge first closes a cycle?" (undirected) | **DSU** — the `union` return value |
| Kruskal's MST | **DSU** — that's the algorithm |
| Need the actual path / distance between nodes | **BFS/DFS** — DSU only knows "same group", not routes |
| **Directed** reachability | **BFS/DFS** — DSU models symmetric equivalence classes only |
| Edges get **removed** over time | **Neither easily** — DSU can't un-merge; use offline reverse-processing or a specialized structure |

### 7. Non-integer elements: remap to indices first

DSU works on `0..n-1`. If your elements are strings (emails, account names,
coordinates), build a `dict` mapping each distinct element to a fresh integer id,
size the DSU to the number of ids, and translate. Accounts Merge (Group 07) does
exactly this with email strings.

### 8. Complexity — how to state it in an interview

> "Union-Find with path compression and union by rank does each `find` and
> `union` in amortized `O(α(n))`, where `α` is the inverse Ackermann function —
> at most 4 for any realistic `n`, so effectively constant. Processing `E` edges
> is `O(E · α(V))`, effectively `O(E)`. Space is `O(V)` for the parent and rank
> arrays."

Always say **amortized** (a single `find` *before* compression can be `O(log n)`;
the near-constant bound is over a sequence of operations).

### 9. Common bugs

- [ ] **Forgetting path compression** *and* **union by rank** — a degenerate
      chain makes `find` `O(n)`; you lose the whole point of DSU.
- [ ] **`union` not comparing roots** — doing `parent[a] = b` instead of
      `parent[find(a)] = find(b)` corrupts the forest.
- [ ] **Off-by-one on 1-indexed input** — size the DSU as `DSU(n + 1)` when nodes
      are `1..n`, or remap to `0..n-1`.
- [ ] **Recursive `find` without a depth guard** — fine with path compression in
      practice, but an unbalanced first call can still recurse deep; the
      iterative `while` form above avoids it entirely.
- [ ] **Using DSU for a directed graph's reachability** — it can't; it only does
      undirected "same component."
- [ ] **Expecting DSU to support deletion** — it doesn't.

### 10. Problems in this repo that drill DSU

Redundant Connection, Graph Valid Tree, Number of Connected Components, Number of
Provinces, Accounts Merge (all Group 07); Min Cost to Connect All Points
(Kruskal's, Group 12); mentioned as an alternative in Number of Islands,
Find if Path Exists, and Making a Large Island.
