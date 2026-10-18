# Concept 04 — DFS (Depth-First Search)

## Quick Card

**Idea:** go **as deep as possible** down one path before backing up and trying the
next. "Follow this corridor to the end, then come back and try the next door."

**Data structure:** the **call stack** (recursion), or an explicit `list`/`deque`
used as a stack (last in, first out).

```python
# Recursive (our primary form)
def dfs(node):
    seen.add(node)
    for nei in neighbors(node):
        if nei not in seen:
            dfs(nei)

# Iterative (same result, no recursion-depth risk)
def dfs(start):
    stack = [start]
    seen = {start}
    while stack:
        node = stack.pop()
        for nei in neighbors(node):
            if nei not in seen:
                seen.add(nei)
                stack.append(nei)
```

**Complexity:** `O(V + E)` time, `O(V)` space (recursion stack / explicit stack +
`seen`).

**Reach for DFS when:** "visit everything / is it reachable", flood-fill a region,
count/size a component, detect a cycle, topological sort (post-order), backtracking,
Euler path. **Not** for shortest path in an unweighted graph — that's BFS.

---

## Full tutorial

### 1. The picture

Same graph as the BFS file. DFS from `A` might visit:

```
A -> B -> D -> C   (dead end, back up)  -> ... -> E
```

It plunges down `A→B→D→…` fully before it ever looks at `A`'s second neighbor `C`.
Contrast BFS, which does `A`, then `B` and `C`, then their children.

### 2. Recursion = an automatic stack

When `dfs(A)` calls `dfs(B)`, Python **pauses** `dfs(A)` (remembering where it was)
and starts `dfs(B)`. Those paused calls pile up on the **call stack**. When a call
returns, Python **resumes** the one underneath. That pile is exactly a stack — you
get depth-first behavior for free.

The iterative version just makes that stack explicit with a `list`.

> One real difference: with an explicit `stack` and `pop()` from the end, neighbors
> come off in **reverse** order compared to recursion. It doesn't matter for
> correctness (any DFS order is a valid DFS order), only if a problem demands a
> specific tie-break order.

### 3. Two places you can "do work" in a DFS

```python
def dfs(node):
    # PRE-ORDER: work here happens when you FIRST arrive at node
    seen.add(node)
    for nei in neighbors(node):
        if nei not in seen:
            dfs(nei)
    # POST-ORDER: work here happens when you're DONE with node and all its descendants
```

- **Pre-order** work: counting cells in a flood fill, marking visited.
- **Post-order** work: topological sort (a node is "finished" only after everything
  it points to is finished — see `concepts/07`), and Eulerian path (`concepts/14`
  adds the node to the route in post-order).

### 4. DFS on a grid (Group 01 — the most common use)

```python
def dfs(r, c):
    if not (0 <= r < m and 0 <= c < n):     # 1. off the board -> stop
        return
    if grid[r][c] != "1" or (r, c) in seen: # 2. wall / water / already visited -> stop
        return
    seen.add((r, c))                        # 3. claim this cell
    for dr, dc in DIRS:                     # 4. ask all 4 neighbors to do the same
        dfs(r + dr, c + dc)
```

This "sinks" a whole island. Every problem in Group 01 is a variation of these 6
lines.

Space-optimized variant: instead of a `seen` set, overwrite visited land with
`"0"`. Saves `O(m*n)` memory but destroys the input (mention that trade-off to the
interviewer; ask if mutation is allowed).

### 5. Cycle detection with DFS

**Undirected graph:** you're in a cycle if DFS reaches an already-seen node that is
**not** the neighbor you just came from.

```python
def dfs(node, parent):
    seen.add(node)
    for nei in graph[node]:
        if nei not in seen:
            if dfs(nei, node):
                return True
        elif nei != parent:        # seen AND not where we came from -> cycle
            return True
    return False
```

**Directed graph:** you're in a cycle if DFS reaches a node that is **currently on
the recursion stack** (a "gray" node). Use 3 colors: white = unvisited, gray = in
progress, black = done. Reaching gray = cycle. (Details in `concepts/06`.)

### 6. The recursion-depth problem (and the fix)

Python's default recursion limit is ~1000. A DFS on a 500×500 grid that is one
giant snake-shaped region can recurse 250000 deep → `RecursionError`.

Fixes, in order of preference:
1. `import sys; sys.setrecursionlimit(10**6)` at the top of the file. Simplest.
2. Use the **iterative stack** version (shown in the Quick Card). No limit at all.
3. If you also risk running out of actual memory, that's a sign BFS or union-find
   fits better.

Every problem file shows both the recursive and the iterative form so you can
switch instantly if the interviewer says "the grid is 10^6 by 10^6".

### 7. Dry run — flood fill one island

Grid (`1` = land):

```
   c0 c1 c2
r0  1  1  0
r1  0  1  0
r2  0  0  1
```

Call `dfs(0, 0)`:

| call | in bounds & land & unseen? | action | seen after |
|---|---|---|---|
| dfs(0,0) | yes | add (0,0); recurse down,up,right,left | {(0,0)} |
| dfs(1,0) | (1,0) is water → return | — | {(0,0)} |
| dfs(-1,0) | off board → return | — | {(0,0)} |
| dfs(0,1) | yes | add (0,1); recurse | {(0,0),(0,1)} |
| dfs(1,1) | yes | add (1,1); recurse | {(0,0),(0,1),(1,1)} |
| dfs(2,1) | water → return | — | same |
| dfs(1,2),(1,0),(0,1)... | water / off / seen → return | — | same |
| back to dfs(0,1): dfs(0,2) water, dfs(-1,1) off, dfs(0,0) seen | return | — | same |
| back to dfs(0,0): up/left off board | return | — | done |

Island size = `len(seen)` = 3. The cell `(2,2)` is a **separate** island, reached
by a different starting `dfs`.

### 8. Complexity — how we get O(V + E)

- **Time.** Each node's `dfs` body runs once (the `seen` check stops repeats). Each
  run loops over that node's neighbors → every edge examined a constant number of
  times → `O(V + E)`. Grid: `O(m*n)`.
- **Space.** The recursion stack can be as deep as the longest path = `O(V)` worst
  case (a straight line of nodes). Plus `seen` = `O(V)`. Total `O(V)`. The
  iterative version has the same `O(V)` for the explicit stack.

### 9. BFS vs DFS — when DFS wins

| Situation | Why DFS |
|---|---|
| flood fill / "sink the island" / size a region | 5 lines, no queue bookkeeping |
| "is there *any* path from A to B" (don't need shortest) | first path found is enough |
| topological order / cycle in a directed graph | post-order + on-stack detection are natural |
| backtracking (try, recurse, undo) | the call stack *is* the backtracking |
| Euler path (Reconstruct Itinerary) | Hierholzer is DFS with post-order append |

DFS does **not** give shortest paths in unweighted graphs. If the question says
"fewest"/"shortest"/"minimum steps", use BFS.

### 10. Pitfalls checklist

- [ ] Marked `seen` **before** recursing into a neighbor (not after), else infinite loop on cycles.
- [ ] Base cases first: off-board check *before* indexing `grid[r][c]`.
- [ ] For undirected cycle detection: passed and checked `parent`.
- [ ] Deep graph? Raised the recursion limit or went iterative.
- [ ] Didn't use DFS for a shortest-path question.
- [ ] Reset global/`nonlocal` state between separate DFS starts if the problem loops over many.

### 11. Problems in this repo that drill DFS

Number of Islands, Flood Fill, Max Area of Island, Making a Large Island (Group 01),
Pacific Atlantic, Surrounded Regions (Group 03), Find if Path Exists (04), Clone
Graph (05), Course Schedule (DFS colors, 06), Longest Increasing Path (06),
Is Graph Bipartite? (08), Evaluate Division (09), Reconstruct Itinerary (14),
Critical Connections (15).
