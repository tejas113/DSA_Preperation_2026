# Concept 09 — Bipartite Graphs & 2-Coloring

## Quick Card

A graph is **bipartite** if you can split its nodes into **two groups** so that
**every edge goes between the groups**, never inside one. Equivalently: you can
color every node **red or blue** with no edge joining two same-colored nodes.

**Test it by 2-coloring** (BFS or DFS): color a start node, color each neighbor
the **opposite** color. If you ever reach a node that's *already* colored the
**same** color you're about to give it → **not bipartite**.

```python
from collections import deque

def is_bipartite(graph, n):
    color = [0] * n                     # 0 = uncolored, 1 and -1 = the two colors
    for start in range(n):              # loop over ALL components
        if color[start] != 0:
            continue
        color[start] = 1
        q = deque([start])
        while q:
            node = q.popleft()
            for nei in graph[node]:
                if color[nei] == 0:
                    color[nei] = -color[node]      # opposite color
                    q.append(nei)
                elif color[nei] == color[node]:
                    return False                    # same color across an edge -> conflict
    return True
```

**Key fact:** a graph is bipartite **⟺ it has no odd-length cycle**. A 2-coloring
conflict *is* an odd cycle you just walked around.

**Complexity:** `O(V + E)` time, `O(V)` space — it's just a BFS/DFS with a color
array.

**Reach for it when:** "split into two groups so [enemies / conflicts] are
separated," "can this be 2-colored," "is this graph bipartite," "assign to two
shifts/rooms/teams without adjacent conflicts."

---

## Full tutorial

### 1. The mental model: two teams, and rivalries between them

Every node is a person. Every edge is a "these two can't be on the same team"
rivalry. **Bipartite = you can split everyone into exactly two teams with every
rivalry crossing the divide.**

```
Bipartite (2 teams work):        NOT bipartite (a 3-cycle):

  A --- B                          A --- B
  |     |                           \   /
  C --- D                            \ /
                                      C
  Team 1: {A, D}                   A-B, B-C, C-A: any 2-coloring
  Team 2: {B, C}                   forces two of them to match.
```

### 2. Why odd cycles are the *only* obstruction

Walk around any cycle, alternating colors: red, blue, red, blue, ... To come back
to the start with a consistent color, the cycle must have an **even** number of
edges. An **odd** cycle forces the last node to clash with the first. That's the
whole theorem: **bipartite ⟺ no odd cycle**, and the 2-coloring BFS/DFS finds an
odd cycle exactly when it hits a same-color conflict.

### 3. BFS coloring (from the Quick Card)

- `color[x]`: `0` (uncolored), `1`, or `-1`. Using `1`/`-1` makes "the opposite
  color" just `-color[x]`.
- Start each uncolored node at color `1`, BFS out, coloring neighbors `-color`.
- Conflict check: neighbor already colored **and** equal to the current node's
  color → return `False`.

### 4. DFS coloring (same logic, recursion)

```python
def is_bipartite(graph, n):
    color = [0] * n

    def dfs(node, c):
        color[node] = c
        for nei in graph[node]:
            if color[nei] == 0:
                if not dfs(nei, -c):
                    return False
            elif color[nei] == c:
                return False
        return True

    return all(dfs(i, 1) for i in range(n) if color[i] == 0)
```

BFS vs DFS: both `O(V + E)`, both correct. DFS is a couple lines shorter; BFS
avoids recursion-depth limits on a huge graph. Pick per the usual trade-off.

### 5. The must-do: loop over *all* components

A graph can be **disconnected**. If you only color from node `0`, you miss every
other component. Always wrap the coloring in `for start in range(n): if
color[start] == 0: ...` — a graph is bipartite only if **every** component is.

### 6. Union-Find alternative (for the enemy-pairs framing)

For "split into two groups so these pairs are enemies" (Possible Bipartition),
you can also use a DSU of size `2n`: node `i` gets a "real" slot `i` and an
"enemy" slot `i + n`. For each dislike pair `(a, b)`: union `a` with `b + n` and
`b` with `a + n` ("a is in b's enemy group and vice versa"). If `find(a) ==
find(b)` ever holds, `a` and `b` are forced into the same group → impossible.
Same `O((V + E) α)`. The coloring BFS/DFS is usually simpler to write.

### 7. Dry run — a conflict

`graph = {0:[1,3], 1:[0,2], 2:[1,3], 3:[0,2]}` (a 4-cycle `0-1-2-3-0`) — plus an
extra edge `0-2` making an odd cycle.

`graph = {0:[1,3,2], 1:[0,2], 2:[1,3,0], 3:[0,2]}`.

- `color[0]=1`, queue `[0]`.
- Pop `0`: `1`→`-1` (queue), `3`→`-1` (queue), `2`→`-1` (queue).
- Pop `1` (color `-1`): neighbor `0` is `1` = `-color[1]` ✓; neighbor `2` is
  `-1` = `color[1]` → **conflict, return `False`.**

The cycle `0-1-2-0` has length 3 (odd) — not bipartite. ✅

### 8. Complexity

- **Time:** `O(V + E)` — each node colored once, each edge checked a constant
  number of times.
- **Space:** `O(V)` for the `color` array, plus `O(V)` for the BFS queue / DFS
  stack.

### 9. Common bugs

- [ ] **Only coloring one component** — missing the `for start in range(n)` loop.
- [ ] **Marking color at dequeue instead of at enqueue** (BFS) — a node can get
      queued twice with different colors before it's processed; color it the
      moment you assign it.
- [ ] **`elif color[nei] != color[node]` when you meant `== `** — inverts the
      conflict test.
- [ ] **Using `0` as one of the two real colors** — then "uncolored" is
      ambiguous. Use `1` / `-1` (or `True`/`False` with a separate "seen" set).
- [ ] **Self-loop in the graph** — an edge `x–x` makes bipartiteness impossible;
      most problems exclude it, but check.

### 10. Problems in this repo that drill this

Is Graph Bipartite? (LC 785, Group 08), Possible Bipartition (LC 886, Group 08 —
build the "dislikes" graph first, then 2-color).
