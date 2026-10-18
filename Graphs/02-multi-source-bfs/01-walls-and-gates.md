# Walls and Gates  ·  LeetCode 286  ·  Medium  ·  🔒 Premium

Group 02 — Multi-Source BFS  ·  the purest form of the pattern: every source at
once, one BFS pass, every cell gets its distance to the nearest source.

> This problem is on LeetCode's premium tier. You may not be able to submit it
> without a subscription — but the code below is fully runnable and tested locally
> (`python 01-walls-and-gates.py`), so you can still learn and drill it.

Prereqs: `concepts/03` (BFS), `01-grid-flood-fill/02-flood-fill.md` (the
mutation-as-visited-mark trick — this problem reuses it for distances instead of
color).

---

## 1. Problem

You are given an `m x n` grid `rooms`. Each cell is one of:

- `-1` — a **wall** (impassable).
- `0` — a **gate**.
- `2147483647` (i.e. `2^31 - 1`, referred to as `INF`) — an **empty room**.

Fill every empty room **in place** with the distance to its **nearest gate**
(moving only up/down/left/right, never through a wall). If a room cannot reach any
gate, leave it as `INF`.

Constraints:
- `1 <= m, n <= 250`.
- `rooms[r][c]` is `-1`, `0`, or `2147483647`.

Example (`INF = 2147483647`):

```
input:
[[INF, -1,   0,   INF],
 [INF, INF,  INF, -1 ],
 [INF, -1,   INF, -1 ],
 [0,   -1,   INF,  INF]]

output:
[[3, -1, 0, 1],
 [2,  2, 1, -1],
 [1, -1, 2, -1],
 [0, -1, 3,  4]]
```

---

## 2. Explain Like I'm 5

Picture a school building. Some rooms have a **fire exit door** (a gate). Some
rooms are just solid **wall** — you can't stand there at all. The rest are normal
rooms.

You want to write, on the floor of every normal room, "the nearest exit is ___
steps away."

Instead of solving one room at a time ("how far is *this* room from *an* exit,
searching from scratch each time"), you do something smarter: **open every exit
door at the same moment**, and let a wave of people walk outward from *all* the
doors simultaneously, one step per second, spreading through the halls (never
through walls). The first time the wave reaches a room, whatever second it is —
that's the room's distance to its nearest exit, guaranteed, because the closest
exit's wave always gets there first.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Grid with 3 kinds of cells: blocked / source / open | ✅ wall / gate / room |
| "distance to the **nearest**" | ✅ nearest gate |
| Multiple sources (could be many gates) | ✅ |
| All sources are equally "step 0" — none is special | ✅ |

**Reduce it to:** *"Multi-source BFS: push every gate into the queue at distance 0,
BFS outward through open rooms, walls block, first-touch = shortest distance."*

**Look-alikes:**
- 01 Matrix — identical shape, sources are all `0`-cells instead of gates, no
  walls to worry about.
- Rotting Oranges — same BFS, but you report the **number of rounds** (max
  distance), not each cell's own distance, plus an "any fresh left over" check.
- A single-source shortest path ("distance from room A to nearest gate") would
  still use BFS, but from **one** start — that's just `concepts/03`, not this
  group.

---

## 4. Intuition

1. If I do a normal BFS from **one** gate, I get that gate's distance to every
   room it can reach. To get the *nearest* gate for every room, the naive way is
   "BFS from each gate separately, keep the minimum per room" — that's `O(gates ×
   m*n)`.
2. Better: run **one** BFS whose queue starts with *every* gate already in it, all
   at distance `0`. BFS always explores in increasing distance order (that's its
   whole superpower, `concepts/03`). So the *first* time any room is reached — no
   matter which gate's ripple got there — it is being reached by the **closest**
   gate. There's no need to compare distances from different gates; whoever
   arrives first automatically wins because nothing arrives later with a *smaller*
   number.
3. So: one queue, seeded with all gates, one `O(m*n)` BFS, done.
4. Reuse the Flood-Fill trick: the moment a room is filled with its real distance,
   it's no longer `INF`, so `room == INF` **is** the "haven't reached this room
   yet" check — no separate `seen` set needed.

---

## 5. Approach (primary): multi-source BFS

1. `m, n = len(rooms), len(rooms[0])`. `INF = 2147483647`.
2. `q = deque()`. Scan every cell; whenever `rooms[r][c] == 0` (a gate), append
   `(r, c)` to `q`. (Its distance is already `0`, sitting right there in the grid.)
3. While `q` is not empty: pop `(r, c)`. For each of the 4 neighbors `(nr, nc)`:
   if in bounds **and** `rooms[nr][nc] == INF` (meaning: not a wall, not a gate,
   and not yet reached): set `rooms[nr][nc] = rooms[r][c] + 1`, push `(nr, nc)`.
4. Nothing to return — `rooms` is modified in place. Any room never reached stays
   `INF`, which is exactly the required behavior for unreachable rooms.

Builds on: `concepts/03` (BFS core rules), the mutation-as-visited-mark trick from
`01-grid-flood-fill/02-flood-fill.md`.

---

## 6. Pseudocode

```
function wallsAndGates(rooms):
    m, n = rows, cols
    INF = 2147483647
    q = empty queue

    for each cell (r, c):
        if rooms[r][c] == 0:
            enqueue (r, c)                     # seed ALL sources first

    while q is not empty:
        (r, c) = dequeue
        for each of the 4 neighbors (nr, nc):
            if in bounds and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                enqueue (nr, nc)
    # rooms is modified in place; unreachable rooms are still INF
```

---

## 7. Dry Run

```
rooms =
[[INF, -1,   0],
 [INF, INF, INF],
 [-1,  INF, INF]]
```

Seed: the only gate is `(0,2)`. `q = [(0,2)]`.

| pop | rooms[r][c] (its own dist) | neighbor checks | updates | queue after |
|---|---|---|---|---|
| (0,2) | 0 | down(1,2)=INF ✓; up off; right off; left(0,1)=-1 wall ✗ | rooms[1][2]=1 | [(1,2)] |
| (1,2) | 1 | down(2,2)=INF ✓; up(0,2)=0 not INF ✗; right off; left(1,1)=INF ✓ | rooms[2][2]=2; rooms[1][1]=2 | [(2,2),(1,1)] |
| (2,2) | 2 | down off; up(1,2) not INF ✗; right off; left(2,1)=INF ✓ | rooms[2][1]=3 | [(1,1),(2,1)] |
| (1,1) | 2 | down(2,1) not INF (just set) ✗; up(0,1)=-1 wall ✗; right(1,2) not INF ✗; left(1,0)=INF ✓ | rooms[1][0]=3 | [(2,1),(1,0)] |
| (2,1) | 3 | down off; up(1,1) not INF ✗; right(2,2) not INF ✗; left(2,0)=-1 wall ✗ | — | [(1,0)] |
| (1,0) | 3 | down(2,0)=-1 wall ✗; up(0,0)=INF ✓; right(1,1) not INF ✗; left off | rooms[0][0]=4 | [(0,0)] |
| (0,0) | 4 | down(1,0) not INF ✗; up off; right(0,1)=-1 wall ✗; left off | — | [] |

Final:

```
[[4, -1, 0],
 [3,  2, 1],
 [-1, 3, 2]]
```

Sanity check `(0,0)`: the only path to the gate at `(0,2)` is blocked directly by
the wall at `(0,1)`, so it must detour: `(0,0)→(1,0)→(1,1)→(1,2)→(0,2)` = 4 steps.
Matches. ✅

---

## 8. Python Code (primary — multi-source BFS)

```python
from collections import deque
from typing import List

INF = 2147483647
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """Do not return anything, modify rooms in-place instead."""
        if not rooms or not rooms[0]:
            return

        m, n = len(rooms), len(rooms[0])
        q = deque()

        for r in range(m):                      # seed the queue with EVERY gate
            for c in range(n):
                if rooms[r][c] == 0:
                    q.append((r, c))

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1     # write distance == mark visited
                    q.append((nr, nc))


if __name__ == "__main__":
    sol = Solution()

    rooms = [
        [INF, -1, 0, INF],
        [INF, INF, INF, -1],
        [INF, -1, INF, -1],
        [0, -1, INF, INF],
    ]
    sol.wallsAndGates(rooms)
    assert rooms == [
        [3, -1, 0, 1],
        [2, 2, 1, -1],
        [1, -1, 2, -1],
        [0, -1, 3, 4],
    ]

    no_gates = [[INF, INF], [INF, INF]]
    sol.wallsAndGates(no_gates)
    assert no_gates == [[INF, INF], [INF, INF]]     # nothing reachable -> unchanged

    all_walls_around = [[0, -1], [-1, INF]]
    sol.wallsAndGates(all_walls_around)
    assert all_walls_around == [[0, -1], [-1, INF]]  # sealed off -> stays INF

    single_gate = [[0]]
    sol.wallsAndGates(single_gate)
    assert single_gate == [[0]]

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS from every gate (works, but is the wrong tool — shown to explain *why not*)

```python
def wallsAndGates(self, rooms):
    m, n = len(rooms), len(rooms[0])

    def dfs(r, c, dist):
        if not (0 <= r < m and 0 <= c < n):
            return
        if rooms[r][c] < dist:          # already has a shorter (or equal) distance
            return
        rooms[r][c] = dist
        for dr, dc in DIRS:
            dfs(r + dr, c + dc, dist + 1)

    for r in range(m):
        for c in range(n):
            if rooms[r][c] == 0:
                dfs(r, c, 0)
```

This is **correct** (each `dfs` call only overwrites a room if it found a *shorter*
path, so it eventually converges to the true minimum), but it can **revisit the
same room many times** while ripples from different gates cross each other,
costing far more than `O(m*n)` in the worst case — imagine a long corridor with
gates at both ends; cells in the middle get overwritten repeatedly as longer and
shorter estimates race past each other. BFS never has this problem because it
processes cells in strict distance order, so each cell is finalized the first
(and only) time it's reached.

### The BFS↔DFS answer the interviewer wants

> "BFS is not just the faster choice here, it's the **correct-by-construction**
> one for unweighted shortest distance: it visits cells in non-decreasing distance
> order, so the first time a room is reached is provably its shortest distance.
> DFS can still get the right answer by repeatedly relaxing (like a mini
> Bellman-Ford), but it can touch the same cell many times and loses the
> `O(m*n)` guarantee. For 'distance to nearest X', always reach for multi-source
> BFS."

---

## 10. Complexity — derived step by step

**V and E:** node = a room cell, `V = m*n`; edge = 4-neighbor adjacency,
`E ≈ 2mn = O(m*n)`.

**Time:**
- Seeding the queue: scan all `m*n` cells once → `O(m*n)`.
- The BFS itself: each cell is enqueued **at most once** — the
  `rooms[nr][nc] == INF` check guarantees that, exactly like the `seen` check in
  plain BFS. Each dequeue does `O(1)` work plus looks at 4 neighbors → total work
  across the whole BFS is `O(m*n)` (cells) `+ O(m*n)` (edges) = `O(m*n)`.
- **Total: `O(m * n)`** — identical to a *single*-source BFS; multi-source doesn't
  cost more.

**Space:**
- No separate `seen` set — the grid's own values (`INF` sentinel) double as the
  visited marker.
- Queue: up to `O(m*n)` cells in the worst case (e.g. one ring-shaped frontier).
- **Total: `O(m * n)`** for the queue (`O(1)` extra beyond the input, if you don't
  count the queue as "extra" since it's proportional to output size anyway).

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| No gates at all | queue starts empty → BFS loop never runs → every room stays `INF` |
| A room fully sealed off by walls | never reached by any ripple → stays `INF` |
| Grid is all gates | queue has every cell, but each pop finds no `INF` neighbors → nothing changes |
| Grid is all walls | queue starts empty → nothing changes |
| Single cell `[[0]]` | queue = `[(0,0)]`, pops, no neighbors, done — stays `0` |
| Multiple gates equidistant from a room | whichever ripple's `popleft()` happens to reach it first sets it — the *value* is correct either way since both are the same minimum distance |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Using the wrong INF sentinel.** The problem's "empty room" value is the
      *specific* integer `2147483647`, not Python's `float("inf")`. If you compare
      against the wrong sentinel, the `== INF` check silently never matches (or
      always fails) and no room gets filled.
- [ ] **Seeding the queue with only the first gate found**, e.g. `break`-ing after
      one, or writing single-source BFS by accident. Produces distances relative
      to the wrong gate for rooms nearer a different gate.
- [ ] **Treating `-1` (wall) as a valid neighbor.** Must explicitly exclude it —
      here, the `== INF` check on the neighbor already excludes both walls (`-1`)
      and gates (`0`) and already-filled rooms automatically, so this is usually
      safe *only if* you use that exact check; a bug arises if you instead check
      `!= -1`, which would let you overwrite a gate's `0` or re-visit filled rooms.
- [ ] **Off-by-one on distance:** writing `rooms[nr][nc] = distance` instead of
      `rooms[r][c] + 1`. Since gates start at `0` already in the grid, you never
      manually assign `0` — only `+1` relative to the popped cell's *current*
      value.
- [ ] **Forgetting this is an in-place / `None`-returning function** — accidentally
      `return`-ing a new grid instead of mutating `rooms`, breaking the expected
      signature.
- [ ] **Using DFS "for simplicity"** without the `dist <` relaxation check — will
      overwrite a room with a *longer* path if that gate's DFS happens to arrive
      second, giving a wrong (non-minimal) final answer.

**Narrate:** "Room `(0,0)` shows `INF` but should be reachable. Let me check my
seed step — did I collect *every* cell equal to `0`, or did I only grab the first
one? ... I see it, I had `if rooms[0][0] == 0: q.append(...)` outside the loop
instead of inside the double loop over all cells."

---

## 13. Learnings & Transfer

**The reusable core:**

1. **Multi-source BFS = seed the queue with every source before the loop starts.**
   That single change turns "distance from A" into "distance from the *nearest* of
   many sources", for the same `O(V+E)` cost as single-source BFS.
2. **Mutation-as-visited-and-answer**, extended from Flood Fill: the sentinel value
   (`INF`) being overwritten with the real answer (distance) *is* the visited
   check. No separate `seen` structure.
3. **Why BFS and not DFS for "nearest/shortest" is a correctness argument, not
   just a speed one** — BFS explores in strict distance order, so first-touch =
   shortest, guaranteed. DFS needs an explicit "only overwrite if shorter"
   relaxation to even be correct, and still isn't linear-time.

| Problem | How this transfers |
|---|---|
| 01 Matrix | same skeleton; sources = all `0` cells, no walls |
| Rotting Oranges | same skeleton; sources = rotten oranges; report the round count (max distance) instead of per-cell distance, plus check for leftover unreached fresh oranges |
| Shortest Bridge | DFS first to *find* one island's cells (they become the multi-source seeds), then this exact BFS to the other island |
| Any "nearest facility / nearest checkpoint" grid problem | this template, verbatim |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "There are two kinds of gates — fire exits and first-aid stations. For every room, report the distance to the nearest fire exit AND, separately, the nearest first-aid station."

- **(b) Pattern:** still multi-source BFS, but you need **two independent
  distance fields**, one per gate type.
- **(c) Adapt:** run the exact same algorithm **twice**, once seeding the queue
  with only fire-exit cells (into a `dist_fire` grid), once with only first-aid
  cells (into `dist_aid`). They can't be combined into a single BFS pass because a
  cell's nearest fire exit and nearest first-aid station are generally reached by
  different ripples that would interfere if merged. Cost: `O(2 * m*n)` — still
  linear, just with a constant factor per gate type.
- **(d) Say:** "Independent 'nearest of type K' queries ⇒ one multi-source BFS per
  type; they don't share a queue because different types' distances are unrelated
  quantities."

### Scenario 2 — "Some doors take 2 minutes to walk through instead of 1 (they're heavy fire doors). Recompute the distances."

- **(b) Pattern:** the edge weights are no longer uniformly `1` — plain BFS is
  **no longer correct**. This is now a **multi-source Dijkstra** (Group 10), or,
  since weights are only `1` or `2`, a more efficient **0-1(-2) BFS** using a
  deque (`concepts/13`).
- **(c) Adapt:** push all gates into a min-heap `(0, r, c)`. Pop the smallest;
  relax neighbors with `new_dist = dist + edge_weight`; push `(new_dist, nr, nc)`
  if it improves the best known distance; skip stale heap entries. `O((V+E) log
  V)` instead of `O(V+E)`.
- **(d) Say:** "The instant an edge weight stops being uniformly 1, BFS's
  distance-order guarantee breaks — the multi-source idea (seed all sources)
  carries over, but the traversal itself must become Dijkstra (or 0-1 BFS for
  small integer weights)."

### Scenario 3 — "The building's walls change over time (renovations). After each wall added/removed, serve 'distance to nearest gate' queries efficiently."

- **(b) Pattern:** dynamic multi-source BFS — a genuinely hard dynamic-graph
  problem, flag that plainly.
- **(c) Adapt:** the pragmatic answer: if wall changes are infrequent relative to
  queries, just **recompute the full `O(m*n)` BFS** after each change and cache
  the result until the next change — simple and correct. If changes are frequent
  and only local, note that a *general* efficient incremental update is hard
  (removing one wall can shorten distances for a large, unpredictable region), so
  without further constraints (e.g. bounded change radius) a full recompute is the
  honest, defensible answer rather than a fragile incremental patch.
- **(d) Say:** "I'd rather recompute correctly in `O(m*n)` than ship a fragile,
  possibly-wrong incremental update — I'd only build incremental maintenance if the
  interviewer confirms the update pattern makes it safe (e.g. only additions, never
  removals, which *can* be handled by capping each cell's distance downward with a
  fresh partial BFS from the new wall's neighbors)."

### Scenario 4 — "The building is enormous (a 10,000-floor space station, gates sparse) and you only care about rooms within 50 steps of a gate (an evacuation-time cutoff); anything farther is 'too far, don't bother computing.'"

- **(b) Pattern:** **bounded** multi-source BFS.
- **(c) Adapt:** same algorithm, but stop expanding a ripple once its distance
  would exceed the cutoff `D`: track distance with each queue entry (or by ring),
  and skip pushing a neighbor if `dist + 1 > D`. Cost becomes proportional to the
  number of cells within distance `D` of *some* gate, not the whole grid — huge
  savings when gates are sparse and `D` is small relative to the grid.
- **(d) Say:** "A distance cutoff turns an `O(m*n)` full-grid BFS into an
  `O(area within D)` bounded BFS — just stop enqueueing past the limit."

### Scenario 5 — "For every room, also report *which* gate is nearest (its coordinates), not just the distance — for wayfinding signage."

- **(b) Pattern:** same multi-source BFS, carrying one extra piece of state.
- **(c) Adapt:** keep a parallel `nearest_gate` grid. When you seed the queue, set
  `nearest_gate[gate_r][gate_c] = (gate_r, gate_c)`. When relaxing a neighbor,
  propagate: `nearest_gate[nr][nc] = nearest_gate[r][c]`. No asymptotic change —
  still `O(m*n)` time and space.
- **(d) Say:** "Multi-source BFS naturally carries any 'which source' label
  alongside the distance — just copy it forward every time you relax an edge."

### Scenario 6 — "Civilians may only use civilian-accessible doors; staff can use all doors including restricted ones. Compute nearest-gate distance for both groups."

- **(b) Pattern:** same BFS, run **twice** with a different definition of "wall"
  per profile (a restricted door counts as a wall for civilians, a normal room for
  staff).
- **(c) Adapt:** parameterize the neighbor check's "is this passable" test by a
  `profile` argument (civilian vs staff), and run the whole multi-source BFS once
  per profile. `O(m*n)` per profile.
- **(d) Say:** "Different 'who can walk where' rules ⇒ same traversal, different
  passability predicate, run once per rule-set."

---

## 15. Flashcards

**Q:** What's the one change from single-source to multi-source BFS?
**A:** Seed the queue with **every** source, all at distance 0, **before** the
main loop starts — instead of one starting node.

**Q:** Why does the first BFS ripple to reach a cell always come from the
*nearest* source?
**A:** BFS explores in strictly non-decreasing distance order, so nothing arrives
later with a smaller distance than what already claimed the cell.

**Q:** Time cost of multi-source BFS vs running single-source BFS from each source
and taking the min?
**A:** Multi-source: `O(m*n)`, one pass. Naive per-source: `O(sources × m*n)`.

**Q:** What visited-marking trick does this problem borrow from Flood Fill?
**A:** Overwriting the sentinel (`INF`) with the real answer (distance) doubles as
the visited check — no separate `seen` set.

**Q:** Why is DFS the *wrong* tool here, not just a slower one?
**A:** Without an explicit "only overwrite if shorter" relaxation, DFS isn't even
correct — ripples from different gates can overwrite each other out of order. With
relaxation it's correct but can revisit cells many times, losing the `O(m*n)`
bound.

**Q:** Doors with different walk times (weight ≠ 1) — what changes?
**A:** Plain BFS breaks (no longer distance-ordered). Switch to multi-source
Dijkstra (heap) or 0-1 BFS (deque) if weights are small integers.

**Q:** Time and space, with derivation?
**A:** `O(m*n)` time (seed `O(m*n)`, BFS visits each cell/edge once). `O(m*n)`
space for the queue; no extra `seen` array needed.

**Q:** The classic sentinel bug in this exact problem?
**A:** Comparing against the wrong "empty room" constant — must be the literal
`2147483647`, not `float("inf")`.
