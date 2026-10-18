# Concept 03 — BFS (Breadth-First Search)

## Quick Card

**Idea:** explore the graph in **rings** around the start. First all nodes 1 step
away, then all nodes 2 steps away, and so on.

**Data structure:** a **queue** (`deque`) — first in, first out.

**Superpower:** in an **unweighted** graph, the first time BFS reaches a node, it
has reached it by the **shortest possible number of steps**. So BFS = shortest path
when every edge counts as 1.

```python
from collections import deque

def bfs(start):
    q = deque([start])
    seen = {start}                 # mark the start immediately
    steps = 0
    while q:
        for _ in range(len(q)):    # process exactly one whole ring
            node = q.popleft()
            # ... use node ...
            for nei in neighbors(node):
                if nei not in seen:
                    seen.add(nei)  # MARK WHEN ENQUEUEING
                    q.append(nei)
        steps += 1                 # one more ring done
```

**Complexity:** `O(V + E)` time, `O(V)` space. Each node enters the queue once
(`V`), and we look at each edge once (`E`).

**Reach for BFS when:** "shortest / fewest steps / minimum moves" in an unweighted
graph, "layer by layer", "minutes until…", or multiple starting points at once.

---

## Full tutorial

### 1. The picture

Start at node `A`. BFS visits in this order:

```
ring 0:  A                      (0 steps from A)
ring 1:  B  C                   (1 step)
ring 2:  D  E  F                (2 steps)
ring 3:  G                      (3 steps)
```

It finishes a whole ring before touching the next one. That's why it's called
*breadth*-first (wide before deep).

### 2. Why a queue?

A queue is **FIFO** — first in, first out. You add newly discovered nodes to the
**back**, and you always take the next node to process from the **front**. Because
ring-1 nodes were added before ring-2 nodes, they also come out before ring-2
nodes. The queue naturally keeps the rings in order.

(If you used a **stack** instead — last in, first out — you'd dive deep down one
path first. That's DFS.)

### 3. The three rules that keep BFS correct

1. **Mark a node as seen the moment you put it in the queue**, never when you take
   it out. If you wait until you pop it, the same node can be added by several
   neighbors before it's ever processed, and the queue blows up (and the shortest
   distance you assign can be wrong).
2. **Never re-add a seen node.** `seen` is a `set` for O(1) checks.
3. **The start node is seen from the very beginning.**

### 4. Two flavors of the loop

**Flavor A — I don't care about distance, I just want to visit everything:**

```python
q = deque([start])
seen = {start}
while q:
    node = q.popleft()
    for nei in neighbors(node):
        if nei not in seen:
            seen.add(nei)
            q.append(nei)
```

**Flavor B — I need the number of steps / rings** (shortest path length, "minutes",
levels):

```python
q = deque([start])
seen = {start}
steps = 0
while q:
    for _ in range(len(q)):          # freeze the ring size BEFORE the loop
        node = q.popleft()
        if node == target:
            return steps
        for nei in neighbors(node):
            if nei not in seen:
                seen.add(nei)
                q.append(nei)
    steps += 1
```

The trick in Flavor B: `len(q)` at the top of the `while` is exactly the number of
nodes in the current ring. We pop that many, and everything we add during those
pops belongs to the next ring. After the inner loop, `steps += 1`.

> Alternative to counting rings: store the distance *with* each node in the queue —
> `q.append((nei, dist + 1))` — or keep a `dist` dict/array. Both are common; we
> use the ring-count form when we only need one final number, and the `dist`
> array when we need every node's distance (that's `concepts/05` and Group 02).

### 5. Multi-source BFS (very important — Group 02)

Instead of one start node, you push **all** the sources into the queue *before* the
loop starts, all marked seen. BFS then expands from all of them simultaneously.
Each cell gets discovered by whichever source is closest.

```python
q = deque()
for src in all_sources:
    q.append(src)
    seen.add(src)
# ... then the normal BFS loop
```

This computes "distance from every node to the *nearest* source" in one pass —
same `O(V + E)` cost as single-source. Problems: Rotting Oranges, 01 Matrix, Walls
and Gates.

### 6. Dry run — shortest path on a tiny graph

Graph (undirected): `A-B, A-C, B-D, C-D, D-E`. Find steps from `A` to `E`.

```
neighbors:
  A: B, C
  B: A, D
  C: A, D
  D: B, C, E
  E: D
```

| step (rings done) | queue at start of ring | pop | discover & enqueue | seen |
|---|---|---|---|---|
| 0 | [A] | A | B, C | A,B,C |
| 1 | [B, C] | B, then C | D (from B); C sees A(seen),D(seen) | A,B,C,D |
| 2 | [D] | D | E | A,B,C,D,E |
| 3 | [E] | E == target → return **2**? |

Wait — careful. We `return steps` **when we pop the target**. We pop `E` during the
ring where `steps == 3` at pop time? Let's recount with Flavor B precisely:

- Enter `while`, `steps = 0`. Ring size 1. Pop `A` (not target). Enqueue B, C. End inner loop. `steps = 1`.
- Ring size 2. Pop `B` (not target), enqueue D. Pop `C` (not target), D already seen. `steps = 2`.
- Ring size 1. Pop `D` (not target), enqueue E. `steps = 3`.
- Ring size 1. Pop `E` — target! `return steps` → returns **3**.

Hmm, but the true shortest `A→E` is `A-B-D-E` = 3 edges. ✅ Correct, 3.

(If instead you check `if node == target` **at enqueue time** you'd return
`steps + 1` a ring earlier — both styles work, just be consistent. We check at
**pop** time.)

### 7. Complexity — how we get O(V + E)

- **Time.** Every node is enqueued at most once (rule 2), so the `while` body runs
  `V` times total across all rings. For each popped node we loop over its
  neighbors; summed over all nodes that's every edge looked at twice (undirected)
  or once (directed) → `O(E)`. Total `O(V + E)`.
  - On a grid: `V = m*n`, `E ≈ 2mn`, so `O(m*n)`.
- **Space.** The `seen` set holds up to `V` nodes. The queue also holds up to `V`
  in the worst case (imagine a star graph: the center's neighbors all get enqueued
  at once). So `O(V)`.

### 8. BFS vs DFS — when BFS wins

| Situation | Why BFS |
|---|---|
| "fewest moves", "shortest transformation", unweighted | BFS reaches each node by the shortest step count, first try |
| "minutes until all oranges rot", "levels" | rings = minutes/levels, fall out for free |
| many starting points | multi-source BFS handles them in one pass |
| graph is extremely deep / could be a long chain | queue uses heap memory, no recursion-depth crash |

DFS wins for "just visit everything" flood fill (shorter code), backtracking, and
Euler paths. See `concepts/04`.

### 9. Pitfalls checklist

- [ ] Marked `seen` at **enqueue**, not at pop.
- [ ] Start node added to `seen` before the loop.
- [ ] In Flavor B, froze `len(q)` **before** the inner `for`.
- [ ] Used `deque` + `popleft`, not `list` + `pop(0)` (that's O(n)).
- [ ] For weighted edges: **BFS is wrong** — use Dijkstra (`concepts/10`). BFS only
      gives shortest path when every edge = 1 step.
- [ ] For grids: bounds-checked `0 <= nr < m and 0 <= nc < n` before indexing.

### 10. Problems in this repo that drill BFS

Number of Islands (02), Rotting Oranges, 01 Matrix, Walls and Gates (Group 02),
Find if Path Exists (04), Clone Graph (05), Course Schedule (Kahn's BFS, 06),
Is Graph Bipartite? (08), Snakes and Ladders, Minimum Genetic Mutation, Word
Ladder, Shortest Path in Binary Matrix (Group 13).

---

## Appendix — Tejas's Worked Example: why mark-on-enqueue, not mark-on-pop

Written while working through Find if Path Exists in Graph, but this is general
BFS knowledge that applies to *every* BFS you'll ever write — kept here, not in
that one problem's file, so it's in the first place you'd look back for it.

**Setup.** Graph: `0-1, 0-2, 1-3, 2-3`. Adjacency: `0:[1,2]`, `1:[0,3]`,
`2:[0,3]`, `3:[1,2]`. BFS from `0`.

**Scenario A — marking visited when POPPING (the bad way):**

```python
queue = [0]
visited = set()
while queue:
    node = queue.popleft()
    visited.add(node)              # marked AFTER popping!
    for neighbor in graph[node]:
        if neighbor not in visited:
            queue.append(neighbor)
```

- Pop `0` → `visited={0}`. Neighbors `1, 2` not in `visited` → `queue=[1,2]`.
- Pop `1` → `visited={0,1}`. Neighbor `3` not in `visited` → `queue=[2,3]`.
- Pop `2` → `visited={0,1,2}`. Neighbor `3` — **still not in `visited`**, because
  `3` is only *sitting in the queue*, not yet marked! → `queue=[3,3]` ⚠️ **`3` was
  just added twice.**

On a larger or densely-connected graph, nodes get added many times redundantly —
wasted work at best, `TLE`/`MLE` at worst.

**Scenario B — marking visited when ENQUEUING (the correct way):**

```python
queue = [0]
visited = {0}                       # marked IMMEDIATELY when queued!
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)   # marked IMMEDIATELY before queuing!
            queue.append(neighbor)
```

- Pop `0`. Neighbors `1, 2` not in `visited` → mark both →
  `visited={0,1,2}`, `queue=[1,2]`.
- Pop `1`. Neighbor `3` not in `visited` → mark it → `visited={0,1,2,3}`,
  `queue=[2,3]`.
- Pop `2`. Neighbors `0` and `3` are **both already** in `visited` → skip both →
  `queue=[3]`. No duplicate.

**The core difference, in one line each:**
- **Mark on pop** = "I'll claim this node when I process it" → other nodes can
  still push the *same* node onto the queue multiple times while it waits its
  turn.
- **Mark on enqueue** = "I reserve this node the instant I see it, so nobody else
  can add it again" → guarantees every node enters the queue **exactly once**.

This is exactly rule #1 from section 3 above, now with a concrete trace proving
*why* it matters, not just stating that it does.
