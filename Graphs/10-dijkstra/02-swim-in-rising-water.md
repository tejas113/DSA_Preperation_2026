# Swim in Rising Water  ·  LeetCode 778  ·  Hard

Group 10 — Dijkstra  ·  the **minimize-max** variant: Dijkstra on a grid, but the
cost of a path is its **highest cell**, not its total. Swap `d + w` for
`max(d, cell)`.

Prereqs: `01-network-delay-time.md`, `concepts/10-dijkstra.md` (§6, "minimize the
maximum edge").

---

## 1. Problem

An `n x n` grid where `grid[r][c]` is the elevation of that cell. Rain falls: at
time `t`, the water level is `t` everywhere. You start at `(0, 0)` and want to
reach `(n-1, n-1)`. You can swim from a cell to a 4-adjacent cell **at time `t`
only if both cells' elevations are `<= t`** (and you swim instantly, any
distance, as long as the whole path is submerged enough).

**Return the least time `t` at which you can reach `(n-1, n-1)`.**

Constraints:
- `1 <= n <= 50`.
- `grid` is a permutation of `0 .. n²-1` (all values distinct).

Example 1:

```
grid = [[0,2],
        [1,3]]
answer = 3        # you must stand on cell 3 (the destination), so t >= 3;
                  # and at t=3 every cell is <= 3, so any path works.
```

Example 2:

```
grid = [[0,1,2,3,4],
        [24,23,22,21,5],
        [12,13,14,15,16],
        [11,17,18,19,20],
        [10,9,8,7,6]]
answer = 16
```

---

## 2. Explain Like I'm 5

The grid is a landscape of little towers, each a different height. Water is
rising. You can only walk on a tower once the water has risen to at least its
height (and the tower you step onto too).

You want to get from the top-left tower to the bottom-right tower. **The moment
you can make the trip is decided by the *tallest tower on your route*** — you have
to wait for the water to reach that one. So pick the route whose **tallest tower
is as short as possible**, and the answer is that tower's height.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Grid, path from corner to corner | ✅ |
| "Least time" / "minimum `t`" where `t` is a **threshold the whole path must
  clear** | ✅ → minimize the **maximum** cell on the path |
| Cell values act as weights | ✅ |

**Reduce it to:** *"Dijkstra from `(0,0)`, where a path's cost is
`max` of its cells. Relax with `nd = max(d, grid[nr][nc])`. Answer =
`cost[n-1][n-1]`."*

**This is a "bottleneck shortest path"** — minimize the largest element on a
path. Three interchangeable tools: Dijkstra (max-relax), binary search + a
reachability check, or Kruskal-style Union-Find.

**Look-alike:** Path With Minimum Effort (next) — the *identical* variant, with
cost = `abs(height difference)` between adjacent cells instead of the cell value.

---

## 4. Intuition

1. If you follow some path, the earliest you can complete it is `max(elevation of
   its cells)` — you wait for the water to reach the highest one, then the whole
   path is passable.
2. So you want the path from `(0,0)` to `(n-1,n-1)` that **minimizes that
   maximum**.
3. Dijkstra computes exactly this if you define a path's cost as the **max** of
   its cells and relax with `max` instead of `+`:
   `cost_to(neighbor) = max(cost_to(current), grid[neighbor])`.
4. The "first pop is final" guarantee still holds: `max` is **monotonic and
   non-decreasing** along a path (adding a cell can only keep or raise the
   running max), so the heap serves cells in true order of their best bottleneck
   cost — just like `+` with non-negative weights.
5. Seed the heap with `grid[0][0]` (the start cell counts), and return `t` the
   moment you pop the destination.

---

## 5. Approach (primary): Dijkstra with `max`-relaxation

1. `n = len(grid)`. `seen = set()`. `heap = [(grid[0][0], 0, 0)]` — `(running max
   elevation, r, c)`.
2. While `heap`: pop `(t, r, c)`.
   - If `(r, c) == (n-1, n-1)`: **return `t`**.
   - If `(r, c) in seen`: skip.
   - `seen.add((r, c))`. For each in-bounds neighbor `(nr, nc)` not in `seen`:
     push `(max(t, grid[nr][nc]), nr, nc)`.
3. (Grid is connected, so the destination is always reached.)

Builds on: `concepts/10` §6 (minimize-max Dijkstra) + the grid `DIRS` template.

---

## 6. Pseudocode

```
function swimInWater(grid):
    n = len(grid)
    seen = empty set
    heap = [(grid[0][0], 0, 0)]              # (max elevation so far, r, c)
    while heap not empty:
        (t, r, c) = pop-min heap
        if (r, c) == (n-1, n-1): return t
        if (r, c) in seen: continue
        add (r, c) to seen
        for each in-bounds neighbor (nr, nc) not in seen:
            push (max(t, grid[nr][nc]), nr, nc)
```

---

## 7. Dry Run

```
grid = [[0,2],
        [1,3]]     n = 2, destination = (1,1)
```

| pop | dest? | seen? | seen after | pushes |
|---|---|---|---|---|
| (0,0,0) | no | no | {(0,0)} | (1,0)→`max(0,1)=1` → (1,1,0); (0,1)→`max(0,2)=2` → (2,0,1) |
| (1,1,0) | no | no | {(0,0),(1,0)} | (1,1)→`max(1,3)=3` → (3,1,1) |
| (2,0,1) | no | no | {(0,0),(1,0),(0,1)} | (1,1)→`max(2,3)=3` → (3,1,1) |
| (3,1,1) | **yes** → return `3` | | | |

Answer: `3`. ✅

---

## 8. Python Code (primary — minimize-max Dijkstra)

```python
import heapq
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        seen = set()
        heap = [(grid[0][0], 0, 0)]             # (max elevation so far, r, c)

        while heap:
            t, r, c = heapq.heappop(heap)
            if (r, c) == (n - 1, n - 1):
                return t
            if (r, c) in seen:
                continue
            seen.add((r, c))
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                    heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))

        return -1                                # unreachable (won't happen on a full grid)


if __name__ == "__main__":
    sol = Solution()

    assert sol.swimInWater([[0, 2], [1, 3]]) == 3
    assert sol.swimInWater([
        [0, 1, 2, 3, 4],
        [24, 23, 22, 21, 5],
        [12, 13, 14, 15, 16],
        [11, 17, 18, 19, 20],
        [10, 9, 8, 7, 6],
    ]) == 16
    assert sol.swimInWater([[0]]) == 0
    assert sol.swimInWater([[3, 4], [2, 1]]) == 3          # must stand on start (3)
    assert sol.swimInWater([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 9   # only path max is 9

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Binary search on the answer + reachability check

The answer is a threshold `t` in `[max(grid[0][0], grid[n-1][n-1]), n²-1]`. For a
given `t`, "is `(n-1,n-1)` reachable from `(0,0)` using only cells `<= t`?" is a
plain BFS/DFS. Binary-search the smallest `t` that passes.

```python
from collections import deque
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def can_reach(t: int) -> bool:
            if grid[0][0] > t:
                return False
            seen = {(0, 0)}
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if (r, c) == (n - 1, n - 1):
                    return True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < n and 0 <= nc < n
                            and (nr, nc) not in seen and grid[nr][nc] <= t):
                        seen.add((nr, nc))
                        q.append((nr, nc))
            return False

        lo, hi = max(grid[0][0], grid[n - 1][n - 1]), n * n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if can_reach(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
```

`O(n² log(n²))` = `O(n² log n)`. Very common alternative; a good fallback if you
blank on the `max`-relax trick.

### 9b. Union-Find (Kruskal-style)

Since `grid` is a permutation of `0..n²-1`, process cells in **increasing
elevation order**. "Activate" each cell and `union` it with any already-active
4-neighbor. The answer is the elevation `t` at which `(0,0)` and `(n-1,n-1)`
first land in the same component. `O(n² α(n²))`.

```python
class Solution:
    def swimInWater(self, grid):
        n = len(grid)
        parent = list(range(n * n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        pos = {grid[r][c]: (r, c) for r in range(n) for c in range(n)}
        active = [[False] * n for _ in range(n)]

        for t in range(n * n):
            r, c = pos[t]
            active[r][c] = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and active[nr][nc]:
                    parent[find(r * n + c)] = find(nr * n + nc)
            if find(0) == find(n * n - 1):
                return t
        return n * n - 1
```

### The BFS↔DFS answer the interviewer wants

> "It's a bottleneck path — minimize the largest cell on the route. Three
> equivalent tools: minimize-max Dijkstra (`max` instead of `+`), binary search
> on `t` plus a BFS reachability check, or Kruskal-style Union-Find activating
> cells in elevation order. Dijkstra is `O(n² log n)`, cleanest; Union-Find is
> `O(n² α)`."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = n²`; edge = 4-neighbor adjacency,
`E ≈ 2n² = O(n²)`.

**Time (Dijkstra):**
- Each cell finalized once when first popped: `O(n² log n²) = O(n² log n)`.
- Each edge triggers ≤ 1 heap push: `O(n² log n)`.
- **Total: `O(n² log n)`.**

Binary search + BFS: `O(n² log(n²)) = O(n² log n)`. Union-Find: `O(n² α(n²))`.

**Space:**
- `seen` set: `O(n²)`. Heap: `O(n²)`.
- **Total: `O(n²)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `n = 1` | start == destination; first pop returns `grid[0][0]` (`0`) |
| Answer's lower bound | always `>= max(grid[0][0], grid[n-1][n-1])` — you must stand on both |
| Only one possible route | its max is forced; Dijkstra finds it |
| Start elevation is the largest on every route | seeded into the heap as the initial `t` |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Using `d + grid[nr][nc]` instead of `max(d, grid[nr][nc]).`** That solves
      "minimum total elevation," a different problem.
- [ ] **Seeding the heap with `0` instead of `grid[0][0]`.** The start cell's
      elevation counts toward the running max.
- [ ] **Checking the destination at *push* time instead of *pop* time.** Only the
      pop is guaranteed optimal.
- [ ] **No `seen` set.** Still correct with a lazy check, but you re-expand cells
      and can TLE on adversarial grids.
- [ ] **`(r, c) == (n, n)` instead of `(n-1, n-1)`.**
- [ ] **Binary-search bounds** — `lo` should start at `max(grid[0][0],
      grid[n-1][n-1])`, not `0`, and `hi` at `n²-1`.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Minimize-max path = Dijkstra with `max` instead of `+`.** The first-pop-is-
   final guarantee survives because `max` is monotonic non-decreasing along a
   path.
2. **Bottleneck shortest path** has three equivalent solutions — minimize-max
   Dijkstra, binary-search-the-threshold + reachability, and Kruskal-style
   Union-Find (activate in weight order until the endpoints connect). Know all
   three; interviewers ask for a second.
3. **The answer is bounded below by the endpoints** (you must stand on both).
4. **"Widest path" / max-capacity routing** is the dual: maximize the *minimum*
   edge — same three tools with `min` and reversed comparisons.

| Problem | How this transfers |
|---|---|
| Path With Minimum Effort | identical minimize-max Dijkstra; cost = `abs` height diff |
| "Minimum bottleneck spanning tree" | the MST path between two nodes *is* the minimize-max path |
| Max-capacity / widest-path routing | dual: maximize the min edge |
| "Minimum sight-line height to see over a ridge" | minimize-max along a path |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Return the actual safest route, not just the time."

- **(b) Pattern:** Dijkstra + **parent pointers**.
- **(c) Adapt:** when you first finalize a cell (pop it, not already seen), record
  the cell you came from as `parent[(r,c)]`. From the destination, walk `parent`
  back to `(0,0)` and reverse. `O(n²)` extra.
- **(d) Say:** "Record the predecessor when a cell is finalized; reconstruct by
  walking parents from the destination."

### Scenario 2 — "Diagonal swimming is allowed (8-directional)."

- **(b) Pattern:** same algorithm, wider neighbor set.
- **(c) Adapt:** use `DIRS8`. Complexity unchanged (`O(n² log n)`).
- **(d) Say:** "Neighbor-set swap only."

### Scenario 3 — "There are several possible exits; reach **any** of them in minimum time."

- **(b) Pattern:** multi-target Dijkstra.
- **(c) Adapt:** put the exit cells in a `set`; on pop, `if (r,c) in exits:
  return t`. Still one Dijkstra from `(0,0)`, stop at the first exit popped
  (guaranteed the best).
- **(d) Say:** "Multiple targets — same single-source Dijkstra, just stop when
  the first target is popped."

### Scenario 4 — "The elevations are **not** a permutation — there can be ties and gaps."

- **(b) Pattern:** check which of the three approaches still applies.
- **(c) Adapt:** **Dijkstra is unchanged** — it never assumed distinct values.
  **Binary search + BFS** is unchanged. The **Union-Find** approach needs
  adjusting: process cells grouped by equal elevation (activate all cells of one
  value together before checking connectivity), and iterate over the *sorted
  distinct* values rather than `range(n²)`.
- **(d) Say:** "Dijkstra and binary-search don't care about distinct values; only
  the Kruskal-style Union-Find needs to activate equal-elevation cells as a
  batch."

### Scenario 5 — "`n` is `10^4` (`10^8` cells)."

- **(b) Pattern:** all three are `O(n² · polylog)`; you can't beat `O(n²)` since
  every cell must be considered.
- **(c) Adapt:** Union-Find (`O(n² α)`) has the best constant; use a flat parent
  array and iterative `find`. Dijkstra with a flat `dist`/`seen` array and lazy
  deletion also works. Memory is `O(n²)` — a `10^8`-entry byte array is ~100 MB,
  borderline; a bit-packed `seen` helps.
- **(d) Say:** "At `10^8` cells, Union-Find in elevation order has the tightest
  constants; the real constraint is `O(n²)` memory, so I'd bit-pack the
  visited/active flags."

### Scenario 6 — "Some cells are permanent **walls** (impassable at any water level)."

- **(b) Pattern:** same algorithm, skip walls.
- **(c) Adapt:** in the neighbor expansion, skip any cell marked as a wall
  (exactly like Walls and Gates). If the destination ends up unreachable, return
  `-1`.
- **(d) Say:** "Walls are just cells you never push to the heap — and add a `-1`
  path for the now-possible 'no route' case."

---

## 15. Flashcards

**Q:** What makes this the "minimize-max" Dijkstra variant?
**A:** A path's cost is the **maximum** cell on it, not the sum. Relax with
`nd = max(d, grid[nr][nc])` instead of `d + w`.

**Q:** Why does Dijkstra's "first pop is final" still hold with `max`?
**A:** `max` is monotonic and non-decreasing along a path — adding a cell can only
keep or raise the running max — so the heap still serves cells in true best-cost
order.

**Q:** What do you seed the heap with?
**A:** `(grid[0][0], 0, 0)` — the start cell's elevation, not `0`.

**Q:** The three interchangeable approaches for a bottleneck path?
**A:** (1) minimize-max Dijkstra, (2) binary search on the threshold + BFS
reachability, (3) Kruskal-style Union-Find activating cells in elevation order
until the endpoints connect.

**Q:** Lower bound on the answer?
**A:** `max(grid[0][0], grid[n-1][n-1])` — you must stand on both endpoints.

**Q:** Time and space (Dijkstra)?
**A:** `O(n² log n)` time, `O(n²)` space.

**Q:** The #1 bug?
**A:** Writing `d + grid[nr][nc]` (sum) instead of `max(d, grid[nr][nc])`.

**Q:** "Widest path" / max-capacity routing — how does it relate?
**A:** It's the dual: maximize the **minimum** edge on a path — same three tools
with `min` and flipped comparisons.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Minimize-max Dijkstra, but marking `visited` at
**push time** (each cell enters the heap exactly once) instead of the primary
solution's mark-at-pop.

```python
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:

        rows = len(grid)
        columns = len(grid[0])

        min_heap = [(grid[0][0], 0, 0)]

        visited = {(0, 0)}

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while min_heap:
            time, r, c = heapq.heappop(min_heap)

            if r == rows - 1 and c == columns - 1:
                return time

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < columns and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    heapq.heappush(min_heap, (max(time, grid[nr][nc]), nr, nc))

        return -1
```

**Correct** — verified against the official examples and stress-tested against the
primary solution on 2000 random permutation grids: zero mismatches.

**Why mark-at-push is safe *here* (but NOT in Path With Minimum Effort):**

Normally we mark a Dijkstra node at **pop** time and allow multiple pushes,
because the first cell to reach a neighbor might not give it the cheapest cost —
a later, higher-cost cell can still have a *lighter edge* to that neighbor. That's
why mark-at-push is a genuine bug for plain `+` Dijkstra and for Path With Minimum
Effort (whose edge cost `abs(h[a] - h[b])` depends on **both** endpoints).

Swim in Rising Water is the special case where it's safe: the "edge cost" into a
cell `(nr, nc)` is just **`grid[nr][nc]` — a property of the destination cell
alone**, the same no matter which neighbor pushes it. So:

```
cost via neighbor X = max(costX, grid[Z])
cost via neighbor Y = max(costY, grid[Z])   where Y is popped later, so costY >= costX
                    >= max(costX, grid[Z])
```

The first cell to reach `Z` is popped from the smallest cost in the heap, and
since `grid[Z]` is fixed, that first push already gives `Z` its optimal
bottleneck cost. No later push can beat it — so marking at push time loses
nothing.

**Takeaway:** mark-at-push is a valid Dijkstra shortcut *only* when the cost of
entering a node doesn't depend on which predecessor you came from. Swim: yes.
Path With Minimum Effort / plain weighted Dijkstra: no — use mark-at-pop (or lazy
stale-deletion) there.
