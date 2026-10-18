# Concept 06 — Cycle Detection

## Quick Card

A **cycle** is a path that starts and ends at the same node without immediately
backtracking. Detecting one needs a **different technique depending on whether
the graph is directed or undirected** — this is the single most important fact
in this file.

| Graph type | Technique | Key idea |
|---|---|---|
| **Undirected** | DFS with a `parent` argument | seeing an already-visited node that **isn't** your parent = cycle |
| **Undirected** | Union-Find | an edge whose two endpoints are **already in the same set** = cycle |
| **Directed** | DFS with 3 colors (white/gray/black) | reaching a **gray** (currently-on-your-current-path) node = cycle |
| **Directed** | Kahn's BFS (topological sort) | if you can't remove **every** node by repeatedly peeling indegree-0 nodes, what's left is a cycle |

**The #1 mistake:** using a single `visited` set for a **directed** graph and
flagging a cycle whenever you re-reach an already-visited node. That's **wrong**
— a DAG (no cycle) can still visit the same node twice via two different paths
(a "diamond" shape). You must distinguish "visited and currently on my path"
(gray) from "visited and fully done, safe" (black).

---

## Full tutorial

### 1. Undirected cycle detection — DFS with a parent

```python
def has_cycle_undirected(graph, n):
    seen = set()

    def dfs(node, parent):
        seen.add(node)
        for nei in graph[node]:
            if nei not in seen:
                if dfs(nei, node):
                    return True
            elif nei != parent:          # visited, and NOT where I came from -> cycle
                return True
        return False

    for node in range(n):
        if node not in seen:
            if dfs(node, -1):
                return True
    return False
```

**Why check `nei != parent`?** In an undirected graph, every edge is stored
*both* ways (`u` in `graph[v]` and `v` in `graph[u]`). So when you walk from
`parent` to `node`, `node`'s neighbor list contains `parent` right back — that's
not a cycle, it's just the edge you arrived on. You only have a real cycle if you
reach an *already-seen* node that is **not** simply "the edge I just came from."

**Dry run:** graph `0-1, 1-2, 2-0` (a triangle). `dfs(0, -1)`: mark seen `{0}`.
Neighbor `1`: not seen → `dfs(1, 0)`: mark seen `{0,1}`. Neighbor `0` — seen, but
`0 == parent(0)` → skip (that's just the edge back). Neighbor `2`: not seen →
`dfs(2, 1)`: mark seen `{0,1,2}`. Neighbor `1` — seen, `1 == parent` → skip.
Neighbor `0` — seen, and `0 != parent (which is 1)` → **cycle found**.

### 2. Undirected cycle detection — Union-Find

```python
dsu = DSU(n)
for u, v in edges:
    if dsu.find(u) == dsu.find(v):
        return True          # they were already connected -> this edge closes a cycle
    dsu.union(u, v)
return False
```

**Why this works:** if `u` and `v` are already in the same component *before*
you add the edge `(u, v)`, that means a path between them already exists — adding
one more edge between them creates a loop. This is the natural fit whenever
edges arrive **one at a time** and you want to detect the moment a cycle first
appears (Redundant Connection, Group 07, is built entirely around this).

### 3. Directed cycle detection — DFS with 3 colors

```python
WHITE, GRAY, BLACK = 0, 1, 2

def has_cycle_directed(graph, n):
    color = [WHITE] * n

    def dfs(node):
        color[node] = GRAY                     # "currently on my current path"
        for nei in graph[node]:
            if color[nei] == GRAY:
                return True                     # back edge to an ancestor -> cycle
            if color[nei] == WHITE and dfs(nei):
                return True
        color[node] = BLACK                     # "fully explored, safe forever"
        return False

    for node in range(n):
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False
```

- **White** = never visited.
- **Gray** = currently being explored — it's an ancestor of wherever the DFS
  currently is (still "open" on the call stack).
- **Black** = fully explored — every descendant has been checked, it's
  permanently safe to walk into from anywhere else.

**Why gray, not "any visited node," signals a cycle:** reaching a **black** node
again just means two different paths converge on it (totally normal in a DAG —
see the diamond example below). Reaching a **gray** node means you've walked back
to one of your own ancestors — that IS a cycle, by definition.

### 4. The diamond trap — why "one visited set" is wrong for directed graphs

```
A -> B -> D
A -> C -> D
```

No cycle here — `D` is just reachable two ways. Trace with **correct** 3-color
DFS from `A`:

| step | color state | action |
|---|---|---|
| dfs(A) | A=GRAY | visit neighbors B, C |
| dfs(B) | A=GRAY, B=GRAY | visit neighbor D |
| dfs(D) | A=GRAY, B=GRAY, D=GRAY | no neighbors, mark D=BLACK, return |
| back in dfs(B) | B=BLACK | done, return |
| back in dfs(A): visit C | dfs(C) | A=GRAY, C=GRAY |
| dfs(C) visits D | D is **BLACK** | fine — already fully explored, not gray, **not a cycle** |
| dfs(C) finishes | C=BLACK | |
| dfs(A) finishes | A=BLACK | no cycle found ✅ |

Now trace what a **buggy single-`visited`-set** version would do: it marks `D`
"visited" the first time (via `B`), then when `C` tries to visit `D` again, it
sees `D in visited` and — if it doesn't distinguish gray from black — **wrongly
reports a cycle**. This exact bug is the most common mistake in Course
Schedule-style problems. Always use 3 colors (or the Kahn's-algorithm approach
below) for directed graphs, never a plain boolean `seen`.

### 5. Directed cycle detection — Kahn's algorithm (topological sort)

This doubles as the algorithm from `concepts/07`. The intuition: a node with
**indegree 0** has no unprocessed prerequisite, so it's always safe to "remove"
it first. Repeatedly peel off indegree-0 nodes, decrementing their neighbors'
indegree as you go.

```python
from collections import deque

def has_cycle_directed_kahn(graph, indegree, n):
    q = deque(node for node in range(n) if indegree[node] == 0)
    processed = 0
    while q:
        node = q.popleft()
        processed += 1
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)
    return processed != n     # if we couldn't remove everyone, what's left is a cycle
```

**Why this works:** every node in a cycle always has **at least one**
not-yet-removed prerequisite (another node in the same cycle) — so a cycle's
nodes can *never* reach indegree 0 and get peeled. If `processed < n` at the end,
whatever's left over is (part of) a cycle.

### 6. Complexity

All four techniques are `O(V + E)` time. Space: `O(V)` for `seen`/`color`/
`indegree` arrays, plus `O(V)` for the DFS recursion stack or BFS queue.
Union-Find: `O(E α(V))` (amortized near-linear).

### 7. Which one to reach for

| Situation | Use |
|---|---|
| Undirected, one static check | DFS + parent |
| Undirected, edges arrive one at a time, "which edge closes the first cycle?" | Union-Find |
| Directed, just need yes/no | 3-color DFS, or Kahn's (whichever reads more naturally for the problem) |
| Directed, and you *also* need a valid ordering | Kahn's BFS or DFS post-order (`concepts/07`) — cycle detection falls out for free |

### 8. Problems in this repo that drill this

Course Schedule / Course Schedule II (directed, Kahn's or DFS-color, Group 06),
Redundant Connection / Graph Valid Tree (undirected, Union-Find, Group 07),
Alien Dictionary (directed, built from word comparisons, Group 06).
