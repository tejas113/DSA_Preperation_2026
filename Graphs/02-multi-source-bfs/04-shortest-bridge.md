# Shortest Bridge  ·  LeetCode 934  ·  Medium  ·  *(supplementary)*

Group 02 — Multi-Source BFS  ·  the finale of this group: a genuine **hybrid**
of Group 01 (DFS flood fill) and Group 02 (multi-source BFS). This is where the
two groups you've just learned literally get glued together into one solution.

Prereqs: `01-grid-flood-fill/01-number-of-islands.md` (DFS flood), all three
earlier files in this group (multi-source BFS). New idea: **flood one whole
component first, then multi-source BFS *from* that entire component** to find its
distance to a *different* target component — not to a fixed value like `0` or a
gate.

---

## 1. Problem

You're given an `n x n` binary grid containing **exactly two islands** (each a
group of `1`s connected 4-directionally; the two islands are not touching each
other). You may flip any number of `0`s to `1`s.

**Return the minimum number of `0`s you must flip to connect the two islands into
one.**

Constraints:
- `n == grid.length == grid[i].length`.
- `2 <= n <= 100`.
- `grid[r][c]` is `0` or `1`.
- The grid contains **exactly two** islands.

Example 1:

```
grid = [[0,1],
        [1,0]]
answer = 1
```

`(0,1)` and `(1,0)` are diagonal neighbors — not 4-connected, so they're two
separate islands. Flipping either `(0,0)` or `(1,1)` connects them: `1` flip.

Example 2:

```
grid = [[0,1,0],
        [0,0,0],
        [0,0,1]]
answer = 2
```

Example 3:

```
grid = [[1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1]]
answer = 1
```

(The ring is one island, the center cell `(2,2)` is the other — one water cell
separates them.)

---

## 2. Explain Like I'm 5

Two islands sit in an ocean. You want to build the **shortest possible bridge** —
made of stepping stones you drop one at a time onto the water — connecting them.

Here's the trick: first, **color in the entire first island** with your crayon —
every cell of it, using flood fill (you already know this from Group 01). Now,
instead of thinking of it as many separate starting points, think of the *whole
colored island* as **one giant starting line**.

Drop stepping stones outward from that entire starting line, all at once, in
rings — exactly like the "wave spreading from every gate at once" idea from
Walls and Gates. The very first moment your wave's ring touches **any** cell of
the *other*, uncolored island, count how many stepping stones (water cells) it
took to get there. That count is your shortest bridge.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Grid, exactly two "blobs" | ✅ two islands |
| "Minimum number of cells to flip to connect them" | ✅ |
| The target isn't a fixed value (`0`, a gate) — it's **membership in a specific
  other component** | ✅ → you must first *identify* that component |
| Needs a **shortest** answer | ✅ → BFS, not DFS, for the second phase |

**Reduce it to:** *"DFS-flood the first island to fully identify and mark it (also
collecting it as the seed set), then multi-source BFS outward from that entire
seed set through water, stopping at the first cell belonging to the second
island."*

**Look-alikes — read this carefully, it's a common mix-up:**
- **Making a Large Island** (Group 01) also involves "islands + flipping cells,"
  but asks a *totally different* question: "what's the best result of flipping
  **one** cell, anywhere?" That's solved by **label + probe** (precompute every
  island's size, then evaluate every water cell as a candidate in `O(1)`) — there
  is no "shortest path between two specific islands" involved.
- **Shortest Bridge** asks: "what's the minimum-length bridge **specifically
  between these two given islands**?" That's a genuine shortest-path search
  (multi-source BFS from one island to the other), and the number of flips is
  *not* bounded to one.
- Don't reach for label+probe here — there's nothing to "probe," you need an
  actual distance.

---

## 4. Intuition

1. There are exactly two islands. Pick **either one** — say, the one containing
   whatever land cell you scan into first. Call it island A.
2. **Fully identify island A** with a flood fill (DFS or BFS — doesn't matter,
   you're not measuring distance yet, just marking "this cell belongs to A").
   While you're at it, mark every one of A's cells as a claimed sentinel (`2`) so
   you never confuse it with unclaimed land (`1`, which must now only mean
   "island B") or water (`0`).
3. Now here's the key move: treat **every single cell of island A** as a
   multi-source BFS **source**, all at distance `0` simultaneously — exactly the
   Walls-and-Gates idea, except the "sources" are an entire component instead of
   scattered gate cells.
4. BFS outward through water (`0`) cells, marking each as claimed (`2`) once
   visited so it's never re-enqueued. The **first** time this wave reaches a cell
   that is still `1` (unclaimed — by the problem's guarantee, that can only be
   island B), the current distance is the number of water cells you crossed to
   get there. Since BFS explores in non-decreasing distance order, this is
   provably the **shortest** possible bridge.
5. You don't need to "flip" island A's cells (already land) or the landing cell
   on island B (already land) — only the water cells strictly in between, and
   there are exactly `d` of them (the distance value at the moment of discovery).

---

## 5. Approach (primary): iterative-DFS flood + multi-source BFS

1. `n = len(grid)`. Scan for the first `1` cell — call it `start`.
2. **Phase 1 (flood island A, iterative DFS with an explicit stack):** push
   `start` onto a stack, mark `grid[start] = 2`. While the stack isn't empty, pop
   a cell, and for each of its 4 unclaimed-land (`== 1`) neighbors: mark it `2`,
   push it onto the stack, **and** append `(r, c, 0)` to a BFS queue.
   > We use an **iterative** stack here rather than recursion — a single island
   > can be up to `n*n = 10^4` cells (a long, snake-shaped island), which can
   > exceed Python's default recursion limit (~1000). This is exactly the "grid
   > can be huge" situation our house rule (`concepts/04`) says to go iterative
   > for.
3. **Phase 2 (multi-source BFS from all of island A):** while the queue isn't
   empty, pop `(r, c, d)`. For each of the 4 neighbors `(nr, nc)`:
   - If `grid[nr][nc] == 1`: this is island B — **return `d`**.
   - If `grid[nr][nc] == 0`: mark it `2` (claimed/visited), push `(nr, nc, d+1)`.
4. (The problem guarantees exactly two islands, so a hit is always found — no
   `-1` case here, unlike Rotting Oranges.)

Builds on: `01-grid-flood-fill/01-number-of-islands.md` (DFS flood),
`01-walls-and-gates.md` (multi-source BFS core), `concepts/04` (iterative-vs-
recursive DFS trade-off).

---

## 6. Pseudocode

```
function shortestBridge(grid):
    n = size of grid
    find any cell (r, c) with grid[r][c] == 1  -> start

    # Phase 1: flood-fill island A, collect it as BFS seeds
    stack = [start]
    grid[start] = 2
    q = queue with (start.r, start.c, 0)
    while stack not empty:
        (r, c) = pop stack
        for each of 4 neighbors (nr, nc):
            if in bounds and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                push (nr, nc) onto stack
                enqueue (nr, nc, 0) into q

    # Phase 2: multi-source BFS outward through water
    while q not empty:
        (r, c, d) = dequeue
        for each of 4 neighbors (nr, nc):
            if in bounds:
                if grid[nr][nc] == 1: return d          # reached island B
                if grid[nr][nc] == 0:
                    grid[nr][nc] = 2
                    enqueue (nr, nc, d + 1)
```

---

## 7. Dry Run

```
grid = [[0,1,0],
        [0,0,0],
        [0,0,1]]
```

**Phase 1:** first `1` found at `(0,1)`. Push, mark `grid[0][1] = 2`. Pop `(0,1)`:
neighbors `(1,1)=0`, off-board up, `(0,2)=0`, `(0,0)=0` — none are `1`. Stack
empties. Island A = `{(0,1)}` only. `q = [(0,1,0)]`.

**Phase 2:**

| pop | d | neighbor checks | action | queue after |
|---|---|---|---|---|
| (0,1) | 0 | down(1,1)=0 → mark2,push d1; right(0,2)=0 → mark2,push d1; left(0,0)=0 → mark2,push d1 | 3 pushes | [(1,1,1),(0,2,1),(0,0,1)] |
| (1,1) | 1 | down(2,1)=0 → mark2,push d2; up(0,1)=2 skip; right(1,2)=0 → mark2,push d2; left(1,0)=0 → mark2,push d2 | 3 pushes | [(0,2,1),(0,0,1),(2,1,2),(1,2,2),(1,0,2)] |
| (0,2) | 1 | down(1,2) now 2, skip; others off/claimed | — | [(0,0,1),(2,1,2),(1,2,2),(1,0,2)] |
| (0,0) | 1 | down(1,0) now 2, skip; right(0,1)=2 skip | — | [(2,1,2),(1,2,2),(1,0,2)] |
| (2,1) | 2 | up(1,1)=2 skip; right(2,2)=**1** → island B found! **return 2** | | |

Return **2**. ✅ Matches Example 2.

---

## 8. Python Code (primary — iterative DFS flood + multi-source BFS)

```python
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)

        # find any cell of island A
        start = None
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    start = (r, c)
                    break
            if start:
                break

        # Phase 1: flood-fill island A (iterative DFS), collect it as BFS seeds
        stack = [start]
        grid[start[0]][start[1]] = 2                    # claimed
        q = deque([(start[0], start[1], 0)])

        while stack:
            r, c = stack.pop()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    stack.append((nr, nc))
                    q.append((nr, nc, 0))

        # Phase 2: multi-source BFS from ALL of island A, through water
        while q:
            r, c, d = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    if grid[nr][nc] == 1:                # reached island B
                        return d
                    if grid[nr][nc] == 0:
                        grid[nr][nc] = 2                 # mark visited water
                        q.append((nr, nc, d + 1))

        return -1     # unreachable; never happens given the problem's guarantee


if __name__ == "__main__":
    sol = Solution()

    assert sol.shortestBridge([[0, 1], [1, 0]]) == 1
    assert sol.shortestBridge([[0, 1, 0], [0, 0, 0], [0, 0, 1]]) == 2
    assert sol.shortestBridge(
        [[1, 1, 1, 1, 1],
         [1, 0, 0, 0, 1],
         [1, 0, 1, 0, 1],
         [1, 0, 0, 0, 1],
         [1, 1, 1, 1, 1]]) == 1
    assert sol.shortestBridge([[1, 0, 0], [0, 0, 0], [0, 0, 1]]) == 3

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Recursive DFS for Phase 1 (matches our usual default — with the recursion-limit caveat)

```python
import sys
sys.setrecursionlimit(20000)     # island can be up to n*n = 10^4 cells

def flood(r, c, grid, q, n):
    if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1:
        return
    grid[r][c] = 2
    q.append((r, c, 0))
    for dr, dc in DIRS:
        flood(r + dr, c + dc, grid, q, n)
```

Cleaner-looking, but genuinely risky at the constraint's upper bound (`n = 100` →
up to `10^4` cells in one island, plausible as a long snake shape) without the
`sys.setrecursionlimit` bump. This is exactly the scenario our house rule warns
about — which is why the primary solution above defaults to the iterative stack
instead, for once breaking from "recursion is our usual primary" because the
input size genuinely calls for it.

### 9b. Phase 1 as BFS too (a fully-BFS solution, no stack/recursion at all)

```python
def flood_bfs(start, grid, n):
    q = deque([start])
    grid[start[0]][start[1]] = 2
    seeds = [(start[0], start[1], 0)]
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                q.append((nr, nc))
                seeds.append((nr, nc, 0))
    return seeds
```

Works identically — Phase 1 only needs *reachability*, not distance, so DFS or
BFS are equally valid there (unlike Phase 2, where BFS is required for
*shortest*). Some interviewers like seeing "I used BFS for both phases" purely for
code consistency; either is a fine answer.

### 9c. Bidirectional BFS (advanced follow-up — worth naming, not required at `n ≤ 100`)

Flood **both** islands first (two colors), then expand BFS frontiers from *both*
simultaneously (alternating or in lockstep), stopping the moment one frontier
touches a cell already claimed by the other. This can shrink the effective search
radius roughly in half in the best case. Not needed at this problem's small
constraints, but the right answer when asked "how would you speed this up on a
huge grid."

### The BFS↔DFS answer the interviewer wants

> "This problem needs **both** tools for **different reasons**: DFS (or BFS —
> doesn't matter) to *fully identify* one island, because that's a pure
> reachability question; then BFS specifically for Phase 2, because that part
> needs a *shortest* distance, and only BFS guarantees first-touch = shortest.
> Using DFS for Phase 2 would risk finding *a* bridge, not the shortest one."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = n^2` (grid is square); edge = 4-neighbor
adjacency, `E ≈ 2n^2 = O(n^2)`.

**Time:**
- Finding the start cell: `O(n^2)` worst case (scan).
- Phase 1 flood: visits each of island A's cells once → bounded by `O(n^2)`.
- Phase 2 BFS: each water cell is claimed (and thus enqueued) **at most once**;
  the moment an island-B cell is found, we return immediately. Worst case (the
  islands are maximally far apart) this still touches every water cell once →
  `O(n^2)`.
- **Total: `O(n^2)`.**

**Space:**
- No separate `seen` set — the shared sentinel `2` (claimed) does triple duty:
  marks island A's cells, marks visited water cells, and is never confused with
  unclaimed land (`1`) or unclaimed water (`0`) — the same collision-safe
  sentinel principle from `02-01-matrix.md`.
- Stack (Phase 1) + queue (Phase 2): each up to `O(n^2)` in the worst case.
- **Total: `O(n^2)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| Islands only diagonally adjacent (e.g. `[[0,1],[1,0]]`) | still 2 separate islands (4-directional rule) → bridge length exactly `1` |
| Minimum possible answer | always `≥ 1` — the problem guarantees the two islands are not already 4-adjacent (else they'd be one island) |
| One island is a single cell | Phase 1's stack starts and ends with just that one cell — works unchanged |
| Islands far apart with a long winding water path | BFS still finds the shortest one; Phase 1's iterative stack avoids recursion-depth issues on a large first island |
| `n = 2` (smallest grid) | both phases run correctly on a `2x2` board |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Using recursion for Phase 1 without raising the recursion limit.**
      `RecursionError` on a large, winding first island. Either raise the limit
      or go iterative (our primary choice).
- [ ] **Forgetting to seed the BFS queue with *every* cell of island A**, not
      just the one you started flooding from. If Phase 1 marks cells `2` but
      only appends the *start* cell to `q`, distances from the rest of island A's
      border are missed, and you might get a bridge length that's too long (or
      even miss the shortest route entirely if it starts from a different part of
      the island).
- [ ] **Off-by-one on the returned distance.** `d` at the moment you find an
      island-B neighbor is already the correct answer — don't add or subtract 1.
      (Trace: island A cells start at `d=0`; the first water cell crossed is
      `d=1`; if that water cell's neighbor is already island B, you return `d=1`
      — exactly one flip, matching Example 1.)
- [ ] **Confusing this with Making a Large Island** and reaching for label+probe
      instead of a shortest-path search — wrong technique for this question.
- [ ] **Not marking water cells as claimed (`2`) once visited** in Phase 2 —
      without it, the same water cell gets enqueued repeatedly from multiple
      directions, blowing up the runtime (though it would still terminate,
      it stops being `O(n^2)`).
- [ ] **Scanning for `start` with the wrong loop structure** (e.g. forgetting the
      `break`s), accidentally picking a cell from island B instead of island A —
      still works by symmetry (either island can be "A"), but confusing if you're
      debugging and expect a specific one.

---

## 13. Learnings & Transfer

**The reusable core: flood one component, then multi-source-BFS *from* it.**

This composition — "fully identify component X (any flood technique), then run
multi-source BFS seeded by *all* of X's cells to find the shortest distance to a
*different specific target set* Y" — is the general tool for **"distance between
two groups"**, as opposed to:
- "distance from a point to a fixed value" (01 Matrix, Walls and Gates) — a plain
  multi-source BFS, no flood-first step needed.
- "best result of one flip, anywhere" (Making a Large Island) — label + probe,
  no shortest-path search at all.

| Situation | How this transfers |
|---|---|
| "Minimum links to connect two specific subnetworks/clusters" | identical shape: flood one cluster, multi-source BFS to the other |
| "Distance between two given regions in a graph" (not grid) | same idea on an adjacency list: flood region A (BFS/DFS), seed a multi-source BFS from all of A's nodes, stop at any node in region B |
| **Connect ALL islands at minimum total cost** (Making a Large Island, Scenario 4) | this problem *is* the pairwise-distance subroutine that scenario needs — compute it between every pair of islands, then run Kruskal/Prim (Group 12) on the resulting complete graph |
| Any "shortest bridge/tunnel/link between two named things" | flood + multi-source BFS, every time |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The grid actually has K islands (K > 2), not exactly 2. Find the minimum bridge connecting island #1 to its single nearest neighboring island (whichever that turns out to be)."

- **(b) Pattern:** the exact same algorithm — nothing about it assumed exactly
  two islands. It only assumed "stop at the first unclaimed land cell reached."
- **(c) Adapt:** flood island #1, multi-source BFS outward, and the first
  unclaimed-`1` cell you hit belongs to *whichever* island is nearest — you get
  the answer to "nearest island to #1" for free, no changes needed.
- **(d) Say:** "This algorithm never actually depended on there being exactly two
  islands — it generalizes immediately to 'nearest island to a given one' with K
  islands present."

### Scenario 2 — "Now connect ALL K islands together with the minimum total number of flips (one connected landmass at the end, not necessarily built as a straight chain)."

- **(b) Pattern:** this is the **MST-over-islands** scenario, forward-linked from
  Making a Large Island's Scenario 4 — and this problem is its core subroutine.
- **(c) Adapt:** compute the pairwise shortest-bridge distance between every pair
  of islands (this algorithm, run `O(K^2)` times, or more efficiently: one
  multi-source BFS seeded by *all* islands simultaneously, each ripple tagged
  with its origin island, recording the first time two different islands' ripples
  meet — giving many pairwise distances in fewer passes). Build a complete graph
  on the `K` islands with these distances as edge weights, then run **Kruskal or
  Prim** (Group 12) for the minimum-cost connecting structure.
- **(d) Say:** "'Connect everything at minimum cost' is the MST signal; the
  per-pair cost function here is exactly a Shortest-Bridge query."

### Scenario 3 — "The grid is huge (say 10,000 x 10,000) and the two islands are known to be very far apart. Speed up the search."

- **(b) Pattern:** **bidirectional BFS** (section 9c).
- **(c) Adapt:** flood and seed *both* islands up front (two distinct claim
  markers). Expand BFS frontiers from both simultaneously (alternate a round on
  each, or run truly in lockstep), and stop the moment a ripple from one side
  reaches a cell already claimed by the other. Roughly halves the effective
  search radius in typical cases (worst case is unchanged, but average case wins).
- **(d) Say:** "When both endpoints of a shortest-path search are known up front
  and the graph is huge, expanding from both ends and meeting in the middle is
  the standard speed-up over a single one-directional BFS."

### Scenario 4 — "Some water cells are 'deep water' and cost 2 flips instead of 1 to convert (shallow water still costs 1)."

- **(b) Pattern:** non-uniform weights → plain BFS breaks in Phase 2.
- **(c) Adapt:** Phase 1 (flood island A) is unaffected — it's still pure
  reachability over land cells. Phase 2 becomes **multi-source Dijkstra**: push
  every island-A cell into a min-heap at cost `0`, relax through water cells by
  their individual cost, stop at the first island-B cell popped (Dijkstra
  guarantees that's the cheapest). `O((V+E) log V)` instead of `O(V+E)`.
- **(d) Say:** "Same seed-the-whole-component idea; the moment costs aren't
  uniform, the second phase's tool changes from a queue to a heap — the same
  swap we've made in every weighted variant across this group."

### Scenario 5 — "Report not just the minimum bridge length, but how many *distinct* shortest bridges of that minimum length exist."

- **(b) Pattern:** BFS shortest-path **counting** — track the number of ways to
  reach each frontier cell at its minimum distance.
- **(c) Adapt:** maintain a `ways[cell]` counter alongside `dist`. When relaxing a
  neighbor at distance `d+1` for the *first* time, set `ways[neighbor] =
  ways[cell]`; if the neighbor is reached *again* at the *same* `d+1` (from a
  different predecessor in the same ring), add: `ways[neighbor] += ways[cell]`.
  When you first reach any island-B cell at the minimal distance, keep scanning
  the rest of that same ring (don't return immediately) and sum `ways` over every
  island-B cell reached at that same minimal distance.
- **(d) Say:** "Counting shortest paths is BFS-with-a-counter: propagate a `ways`
  value alongside distance, summing contributions from every predecessor that
  reaches a cell at the same minimal distance."

### Scenario 6 — "This is really a telecom problem: two data-center clusters need linking through unused conduit cells; some conduit cells are permanently reserved (impassable, like walls in Walls and Gates)."

- **(b) Pattern:** combine this problem's hybrid with Walls and Gates' wall check.
- **(c) Adapt:** add one extra condition to both phases' neighbor checks:
  `grid[nr][nc] != WALL`. Phase 1 still only floods through the first cluster's
  own cells (walls were never part of it anyway). Phase 2's water-cell check
  becomes "is empty conduit AND not a reserved wall." Everything else is
  unchanged — same `O(n^2)`.
- **(d) Say:** "Adding impassable cells to any grid-traversal problem is almost
  always a one-line addition to the neighbor-validity check, not a new
  algorithm."

---

## 15. Flashcards

**Q:** What two techniques does this problem combine, and why does it need both?
**A:** DFS (or BFS) flood-fill to fully *identify* one island (pure reachability),
then multi-source BFS from that entire island through water to find the
*shortest* distance to the other island (needs BFS specifically for the
shortest-path guarantee).

**Q:** How is this different from Making a Large Island's "best single flip"?
**A:** That's label + probe (precompute all islands' sizes, evaluate every water
cell in O(1) — no path search). This is a genuine shortest-path search between
two *specific* islands, and the flip count isn't limited to one.

**Q:** Why iterative DFS (stack) instead of the usual recursive default for
Phase 1 here?
**A:** A single island can be up to `n*n = 10^4` cells (constraint `n ≤ 100`) — a
long snake-shaped island could exceed Python's default recursion limit (~1000).

**Q:** What does the distance `d` represent when you find an island-B neighbor,
and why do you return `d`, not `d+1` or `d-1`?
**A:** `d` is the number of water cells already claimed/flipped to reach the
current frontier cell. Its neighbor is already land (island B), needing no
further flip — so `d` itself is the total flip count.

**Q:** What sentinel-safety lesson (from 01 Matrix) reappears here?
**A:** The shared claim marker `2` can't collide with the input's own `0`/`1`
values, so it safely does triple duty: marks island A, marks visited water, and
is distinguishable from unclaimed land.

**Q:** Time and space, with derivation?
**A:** `O(n^2)` both. `V = n^2`, `E ≈ 2n^2`. Each cell is claimed at most once in
either phase; no separate `seen` structure (the grid's own sentinel does that
job).

**Q:** This problem's technique is the core subroutine for which later scenario?
**A:** "Connect ALL islands at minimum total cost" (MST over islands, Group 12) —
Shortest Bridge computes the pairwise distances that MST needs as edge weights.

**Q:** Weighted water cells (deep water costs more) — what changes?
**A:** Phase 1 is unaffected (still pure reachability). Phase 2 becomes
multi-source Dijkstra (heap) instead of plain BFS (deque).

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Recursive DFS for Phase 1, **ring-counting BFS**
(à la Rotting Oranges' Flavor B) for Phase 2 instead of the primary solution's
per-tuple distance — a genuinely different, equally valid bookkeeping style.
`O(n^2)` time and space.

```python
class Solution:
    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)
        queue = deque()

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        distance = 0
        island_id = 2

        def dfs(r, c, island_id):
            grid[r][c] = island_id
            queue.append((r, c))

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1):
                    dfs(nr, nc, island_id)

        found = False
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    dfs(i, j, island_id)
                    found = True
                    break
            if found:
                break

        distance = 0

        while queue:
            for i in range(len(queue)):
                r, c = queue.popleft()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        if grid[nr][nc] == 1:
                            return distance
                        if grid[nr][nc] == 0:
                            grid[nr][nc] = 2
                            queue.append((nr, nc))
            distance = distance + 1
        return distance
```

**Correct** — I hand-traced both official examples (`[[0,1],[1,0]]` → `1` and the
3×3 example → `2`) against this exact code and it matches.

**Why the off-by-one doesn't bite you here, even though the increment is at the
*bottom* of the loop:** this is Rotting Oranges' ring-counting style, but with
`distance += 1` moved to *after* processing each ring instead of before. That
shift is exactly correct for *this* problem's question ("how many water cells
must I flip?") — during the processing of the very first ring (island A's direct
neighbors), `distance` is still `0`; if the problem's islands were 4-adjacent
(impossible per the constraints) you'd correctly want `0` flips. Once you've
completed a full ring without finding island B, *then* `distance` should advance
to count that ring's cells as flips, which is exactly what incrementing at the
bottom does. Compare with the primary solution's per-tuple `(r, c, d)` — same
answer, different (and both valid) ways of tracking it. This is worth remembering
as a general lesson: **where** you place a counter's `+= 1` must match **what
moment** you've defined the counter to represent — get that definition straight
before worrying about the exact line it goes on.

**Two small, harmless notes (not bugs):**

1. `distance = 0` is written twice — once before the DFS phase, once again right
   before the `while` loop. The first assignment is dead code (immediately
   overwritten, never read in between). Worth deleting for tidiness, but has zero
   effect on correctness.
2. Phase 1 uses **recursive** DFS with no `sys.setrecursionlimit` adjustment. It
   works fine on these test cases, but per the `.md`'s section 5 note: a single
   island can be up to `n*n = 10^4` cells at the constraint's upper bound
   (`n = 100`), and a long, snake-shaped island of that size can exceed Python's
   default recursion limit (~1000) and crash with `RecursionError`. This is
   exactly why the primary solution defaults to the **iterative** stack version
   for Phase 1 here — the `concepts/04` alternative shown in section 9a (recursive
   + `sys.setrecursionlimit(20000)`) is the minimal fix if you'd rather keep the
   recursive style.
