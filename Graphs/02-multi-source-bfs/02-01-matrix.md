# 01 Matrix  ·  LeetCode 542  ·  Medium

Group 02 — Multi-Source BFS  ·  Walls and Gates with the walls removed — the
cleanest possible version of the pattern, plus a classic non-BFS follow-up.

Prereqs: `01-walls-and-gates.md` (same skeleton, read that dry run first). New
ideas here: **picking a sentinel that can't collide with a real answer**, and a
**two-pass DP alternative** that avoids a queue entirely.

---

## 1. Problem

Given an `m x n` binary matrix `mat`, for **every** cell return its distance to the
**nearest `0`** (4-directional steps). The matrix is guaranteed to contain at
least one `0`.

Constraints:
- `1 <= m, n <= 10^4`, `1 <= m * n <= 10^4`.
- `mat[r][c]` is `0` or `1`.
- At least one `0` exists (so every `1` is reachable — no "unreachable" case here,
  unlike Walls and Gates).

Example 1:

```
mat = [[0,0,0],
       [0,1,0],
       [0,0,0]]
output = [[0,0,0],
          [0,1,0],
          [0,0,0]]
```

The single `1` is surrounded by `0`s on all 4 sides → distance `1`.

Example 2:

```
mat = [[0,0,0],
       [0,1,0],
       [1,1,1]]
output = [[0,0,0],
          [0,1,0],
          [1,2,1]]
```

`(2,1)` has no `0` neighbor directly, but `(2,0)` is `1` step from `(1,0)=0`, so
`(2,1)` is `2` steps away via `(2,0)`.

---

## 2. Explain Like I'm 5

Same "open every gate at once and let the wave spread" idea as Walls and Gates —
except this building has **no walls at all**, every room is walkable, and instead
of exits it's `0`-squares. Drop the wave from every `0` at the same time; the
second it reaches a `1`, write that second on the square. There's no "sealed off"
room this time, since nothing blocks the wave — every `1` will eventually be
reached.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Distance to the nearest X" for every cell | ✅ nearest `0` |
| Multiple sources (every `0` cell) | ✅ |
| No obstacles | ✅ (this is what makes the DP alternative possible — see section 9) |

**Reduce it to:** *"Multi-source BFS, sources = every `0` cell, no walls."*
Identical to Walls and Gates minus the wall-check.

**Look-alike, but NOT the same:** Walls and Gates has walls — that rules out the
DP shortcut this problem allows (explained in section 9 and Scenario 5).

---

## 4. Intuition

Exactly Walls and Gates' intuition (section 4 there): seed BFS with every source
at once; first-touch = nearest distance, because BFS explores in non-decreasing
distance order.

**The one new wrinkle:** in Walls and Gates, the "unvisited" sentinel was `INF =
2147483647` — a value that could *never* be a real answer, so `cell == INF` safely
meant "not yet reached." Here, the input only contains `0` and `1`. If we tried to
reuse `mat` itself as both input and answer storage (checking `mat[r][c] == 1` to
mean "not yet visited"), we'd have a **collision**: a cell's *real* final distance
can also be `1`! We can't tell "still unvisited" apart from "computed distance is
exactly 1" using the grid's original values.

**Fix:** build a **separate** `dist` grid, and use a sentinel that a real distance
can never equal — `-1` works (all real BFS distances are `≥ 0`). This is the same
mutation-as-visited-mark trick as before, just done carefully so the sentinel
can't be confused with a legitimate answer.

---

## 5. Approach (primary): multi-source BFS with a `-1` sentinel

1. `m, n = len(mat), len(mat[0])`.
2. `dist = [[-1]*n for _ in range(m)]` (`-1` = "not yet computed").
3. `q = deque()`. For every cell where `mat[r][c] == 0`: set `dist[r][c] = 0`,
   push `(r, c)`.
4. While `q`: pop `(r, c)`. For each of the 4 neighbors `(nr, nc)` in bounds with
   `dist[nr][nc] == -1`: set `dist[nr][nc] = dist[r][c] + 1`, push it.
5. Return `dist`.

Builds on: `01-walls-and-gates.md` — identical skeleton, no wall check, different
(collision-safe) sentinel.

---

## 6. Pseudocode

```
function updateMatrix(mat):
    m, n = rows, cols
    dist = m x n grid of -1
    q = empty queue

    for each cell (r, c):
        if mat[r][c] == 0:
            dist[r][c] = 0
            enqueue (r, c)

    while q not empty:
        (r, c) = dequeue
        for each of 4 neighbors (nr, nc):
            if in bounds and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                enqueue (nr, nc)

    return dist
```

---

## 7. Dry Run

```
mat = [[0,0,0],
       [0,1,0],
       [1,1,1]]
```

Seed: every `0` cell → `(0,0),(0,1),(0,2),(1,0),(1,2)`, all `dist = 0`.

| pop | dist | neighbor checks (only `-1` ones update) | updates | queue after |
|---|---|---|---|---|
| (0,0) | 0 | down(1,0)=0 not -1 skip; right(0,1)=0 skip | — | [(0,1),(0,2),(1,0),(1,2)] |
| (0,1) | 0 | down(1,1)=-1 ✓ | dist[1][1]=1 | [...,(1,1)] |
| (0,2) | 0 | down(1,2)=0 skip | — | [(1,0),(1,2),(1,1)] |
| (1,0) | 0 | down(2,0)=-1 ✓; right(1,1) now 1, skip | dist[2][0]=1 | [(1,2),(1,1),(2,0)] |
| (1,2) | 0 | down(2,2)=-1 ✓ | dist[2][2]=1 | [(1,1),(2,0),(2,2)] |
| (1,1) | 1 | down(2,1)=-1 ✓; others already set | dist[2][1]=2 | [(2,0),(2,2),(2,1)] |
| (2,0) | 1 | right(2,1) now 2, skip | — | [(2,2),(2,1)] |
| (2,2) | 1 | left(2,1) now 2, skip | — | [(2,1)] |
| (2,1) | 2 | no `-1` neighbors left | — | [] |

Final `dist`:

```
[[0,0,0],
 [0,1,0],
 [1,2,1]]
```

Matches Example 2. ✅

---

## 8. Python Code (primary — multi-source BFS)

```python
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        dist = [[-1] * n for _ in range(m)]      # -1 = not yet computed (never a real answer)
        q = deque()

        for r in range(m):
            for c in range(n):
                if mat[r][c] == 0:
                    dist[r][c] = 0
                    q.append((r, c))

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

        return dist


if __name__ == "__main__":
    sol = Solution()

    assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == \
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]

    assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == \
        [[0, 0, 0], [0, 1, 0], [1, 2, 1]]

    assert sol.updateMatrix([[0]]) == [[0]]
    assert sol.updateMatrix([[1, 1], [1, 0]]) == [[2, 1], [1, 0]]
    assert sol.updateMatrix([[0, 0, 0, 0, 0]]) == [[0, 0, 0, 0, 0]]     # all zeros

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Two-pass DP — the "no queue, O(1) extra space" trick (works *because there
### are no walls*)

**Idea:** a cell's true shortest path to a `0` must approach from **some**
direction. Split that into two cases and sweep twice:

- **Forward pass** (top-left → bottom-right): every cell can only "see" the
  neighbors already processed in this sweep — **up** and **left**. Set
  `dist[r][c] = min(dist[r][c], dist[r-1][c] + 1, dist[r][c-1] + 1)`.
- **Backward pass** (bottom-right → top-left): now consider **down** and
  **right**. Set `dist[r][c] = min(dist[r][c], dist[r+1][c] + 1, dist[r][c+1] + 1)`.

Any shortest path's "last turn" is captured by one of these two sweeps, so two
passes are provably enough (this is the classic *chamfer distance transform* from
image processing).

```python
from typing import List


class SolutionDP:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        INF = float("inf")
        dist = [[0 if mat[r][c] == 0 else INF for c in range(n)] for r in range(m)]

        for r in range(m):                            # forward: look up + left
            for c in range(n):
                if r > 0:
                    dist[r][c] = min(dist[r][c], dist[r - 1][c] + 1)
                if c > 0:
                    dist[r][c] = min(dist[r][c], dist[r][c - 1] + 1)

        for r in range(m - 1, -1, -1):                 # backward: look down + right
            for c in range(n - 1, -1, -1):
                if r < m - 1:
                    dist[r][c] = min(dist[r][c], dist[r + 1][c] + 1)
                if c < n - 1:
                    dist[r][c] = min(dist[r][c], dist[r][c + 1] + 1)

        return dist
```

`O(m*n)` time, and **`O(1)` extra space** beyond the output (no queue, no `seen`)
— strictly better memory than BFS. This is a genuinely common Google follow-up:
*"can you do it without the extra queue memory?"*

**Why this does *not* work if walls exist:** with obstacles, a cell's true nearest
`0` might require detouring *around* a wall — information that a fixed two-sweep
raster order can't always propagate correctly in just two passes (the detour's
"shape" isn't guaranteed to align with a pure up/left-then-down/right relaxation).
BFS has no such assumption; it's correct for any obstacle layout. This is exactly
why **Walls and Gates used pure BFS** and this DP shortcut only appears here,
where the grid has no obstacles. (Full reasoning in Scenario 5.)

### The BFS↔DFS(DP) answer the interviewer wants

> "BFS multi-source is the general, always-correct approach — `O(m*n)` time,
> `O(m*n)` space. Because this specific grid has no obstacles, there's also an
> `O(m*n)` time, `O(1)`-extra-space two-pass DP (a distance transform) that avoids
> the queue entirely. I'd mention both, note the DP version breaks the moment
> walls are introduced, and let the interviewer pick which they want to see coded."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = m*n`; edge = 4-neighbor adjacency,
`E ≈ 2mn = O(m*n)`.

**BFS (primary):**
- Time: seed scan `O(m*n)` + BFS visits each cell once, each edge once →
  `O(m*n)`.
- Space: `dist` grid `O(m*n)` (this **is** the output, so often not counted as
  "extra") + queue up to `O(m*n)`.

**Two-pass DP (9a):**
- Time: two full scans of the grid → `O(m*n)`.
- Space: `dist` grid `O(m*n)` (the output) + **no other structure** → `O(1)`
  extra.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| All cells are `0` | seed step marks everything `dist=0`, BFS loop finds nothing left to relax |
| Single cell `[[0]]` | `dist = [[0]]` |
| A `1` in a corner, only one `0` reachable path | still found correctly, BFS explores all 4 directions |
| Grid guarantees ≥ 1 zero | no "unreachable" case to worry about (contrast Walls and Gates) |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Sentinel collision.** Trying to reuse `mat` in place and treating `1` as
      "unvisited" — breaks the moment a cell's real distance is `1`. Always use a
      dedicated `dist` grid with a sentinel (`-1`) that can't be a real distance.
- [ ] **Forgetting to seed `dist[r][c] = 0`** for source cells before enqueueing —
      leaves them at `-1` and looks like "unreachable."
- [ ] **DP variant: wrong sweep order.** Forward pass must go top-to-bottom,
      left-to-right; backward pass bottom-to-top, right-to-left. Swapping them
      breaks the "already processed" guarantee each pass relies on.
- [ ] **DP variant: using it when walls exist.** Silently wrong answers near
      obstacles — see section 9a's explanation.
- [ ] **Off-by-one:** same as Walls and Gates — always `dist[r][c] + 1`, never a
      manually tracked separate counter that can drift.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Pick a sentinel that cannot collide with a real answer.** `INF` for
   Walls-and-Gates-style large-int problems; `-1` (or `float('inf')`) when real
   answers could plausibly be small numbers like `0` or `1`. Never reuse an input
   value as "unvisited" if a legitimate output could equal that same value.
2. **The two-pass DP / distance-transform trick** is available *whenever a grid
   has no obstacles* and you want nearest-value distances with `O(1)` extra
   space — a strictly better-than-BFS memory bound in that special case.
3. **Recognize when a technique's assumptions break.** The DP trick silently gives
   wrong answers with obstacles; knowing *why* (not just *that*) is what
   distinguishes a strong interview answer.

| Problem | How this transfers |
|---|---|
| Walls and Gates | same BFS skeleton; walls make the DP shortcut invalid |
| Rotting Oranges | same BFS skeleton; report round count instead of per-cell distance |
| Any "distance transform" (nearest edge, nearest feature) in image processing | the two-pass DP by name |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Cells can be `0`, `1`, or `2`. Return each cell's distance to the nearest cell that is **either** `0` or `2`."

- **(b) Pattern:** still multi-source BFS — but unlike Walls and Gates' "two gate
  *types*, need separate answers" scenario, here you only need the **overall**
  minimum across both source types, not a breakdown per type.
- **(c) Adapt:** seed the **same single queue** with every `0` cell **and** every
  `2` cell together, all at distance `0`. Run one BFS. One pass, `O(m*n)`.
- **(d) Say:** "Merge multiple source *types* into one queue when you only need
  the combined nearest-of-any-type distance; keep them in separate queues/passes
  only when you need a *per-type* breakdown (contrast with Walls and Gates
  Scenario 1)."

### Scenario 2 — "The matrix is enormous and streamed row by row from disk; you can do at most two passes over the data. Compute the same distances."

- **(b) Pattern:** the **two-pass DP** is exactly a two-pass streaming algorithm
  already — the forward pass consumes rows top-to-bottom (streamable), the
  backward pass needs the rows again bottom-to-top (a second read, or the data
  buffered in reverse-readable storage).
- **(c) Adapt:** run the forward sweep while streaming forward, writing partial
  `dist` values to disk/output as you go; then re-read in reverse for the
  backward sweep, updating in place. Memory is `O(row width)` at any instant if
  you can seek/re-read; `O(m*n)` if you must buffer everything (no re-read
  possible).
- **(d) Say:** "The two-pass DP *is* a streaming algorithm as long as the medium
  supports a second, reverse-order read; that's the tell for when to reach for it
  over BFS in a memory-constrained setting."

### Scenario 3 — "Some cells are swampy and take longer to cross (a weight per cell, not per edge). Find nearest-0 distance under that cost model."

- **(b) Pattern:** weighted shortest path from multiple sources → **multi-source
  Dijkstra** (or 0-1 BFS if weights are only 1 or 2).
- **(c) Adapt:** push all `0` cells into a min-heap at cost `0`. Pop smallest,
  relax neighbors by `cost + weight(neighbor)`, push if improved, skip stale
  entries. `O((V+E) log V)`. The two-pass DP does **not** generalize to weights —
  it relies on unit steps.
- **(d) Say:** "The moment costs stop being uniform, BFS (and the DP shortcut)
  are out — multi-source Dijkstra is the tool, same 'seed all sources' idea, just
  a heap instead of a queue."

### Scenario 4 — "Return, for each cell, not just the distance but the actual sequence of cells forming a shortest path to its nearest `0`."

- **(b) Pattern:** BFS + **parent pointers**.
- **(c) Adapt:** keep a `parent` grid alongside `dist`. When relaxing `(nr, nc)`
  from `(r, c)`, set `parent[nr][nc] = (r, c)`. To reconstruct any cell's path,
  follow `parent` backward until you hit a cell with `dist == 0`. `O(m*n)` time
  and space, same as before; each individual path costs `O(path length)` to
  reconstruct on demand.
- **(d) Say:** "BFS shortest-*distance* becomes shortest-*path* for free by
  recording one parent pointer per relaxation — the two-pass DP can't do this as
  naturally since it doesn't process cells in a clean 'discovery order.'"

### Scenario 5 — "Add walls back to this grid (some cells are impassable, like Walls and Gates). Does the two-pass DP trick still give the right answer?"

- **(b) Pattern:** a conceptual check, not a new technique — tests whether you
  understand *why* the DP works, not just that it does.
- **(c) Adapt:** **No, it can break.** With obstacles, a cell's true shortest path
  may need to route *around* a wall in a shape the two fixed sweep directions
  can't always capture in only two passes — the raster-order relaxation assumes
  unobstructed monotone approach directions. The safe, general answer reverts to
  **BFS** (this is precisely why Walls and Gates, which has walls, is solved with
  BFS and not this shortcut).
- **(d) Say:** "The DP shortcut is an optimization valid under a specific
  assumption — no obstacles. The moment that assumption breaks, fall back to the
  general, always-correct tool: multi-source BFS."

### Scenario 6 — "Diagonal moves are now allowed too (8-directional, Chebyshev-style adjacency). Recompute."

- **(b) Pattern:** same BFS, wider neighbor set.
- **(c) Adapt:** use `DIRS8` (8 offsets) instead of `DIRS`. Complexity becomes
  `O(m*n)` still (constant factor of 8 instead of 4 neighbors per cell). The
  two-pass DP also generalizes — forward pass considers up, left, and the two
  upper diagonals; backward pass considers down, right, and the two lower
  diagonals — as long as there are still no walls.
- **(d) Say:** "Changing the neighbor function (4-dir → 8-dir, or any fixed
  offset set) doesn't change the algorithm's shape, only which offsets you loop
  over — true for both the BFS and the DP variant here."

---

## 15. Flashcards

**Q:** How does this problem differ from Walls and Gates?
**A:** No walls, and the sentinel can't just be "the input's own 1 value" — a
`1`-cell's real answer could also be `1`, so use a separate `dist` grid seeded
with `-1` (a value no real distance can equal).

**Q:** Why does mutating `mat` in place (treating `1` as "unvisited") fail here
but `INF` worked for Walls and Gates?
**A:** `INF` (2147483647) can never be a legitimate distance, so it's collision-
free. `1` very much *can* be a legitimate final distance here — collision.

**Q:** The non-BFS alternative for this specific problem, and its complexity?
**A:** Two-pass DP (distance transform): forward sweep looks up+left, backward
sweep looks down+right. `O(m*n)` time, `O(1)` extra space (no queue).

**Q:** Why does the two-pass DP break if walls are added?
**A:** A wall can force a detour whose shape isn't guaranteed to be captured by
just two fixed-direction sweeps; BFS has no such assumption and stays correct.

**Q:** Multiple source *types*, need only the overall nearest — one BFS or many?
**A:** One — merge all source types into a single queue. Use separate BFS passes
only when you need a *per-type* breakdown (contrast Walls and Gates Scenario 1).

**Q:** Weighted cells/edges — what replaces BFS?
**A:** Multi-source Dijkstra (heap), or 0-1 BFS (deque) if weights are small
integers. The two-pass DP does not generalize to weights.

**Q:** How to get the actual shortest path, not just its length?
**A:** Track a `parent` pointer per cell during BFS relaxation; walk it backward
from any cell to a `dist == 0` source.
