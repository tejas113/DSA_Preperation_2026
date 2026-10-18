# Longest Increasing Path in a Matrix  ·  LeetCode 329  ·  Hard  ·  *(supplementary)*

Group 06 — Topological Sort / Cycle Detection  ·  an **implicit DAG**: the
movement rule (strictly increasing) makes cycles *impossible by construction*, so
memoized DFS needs **zero** cycle-handling machinery.

Prereqs: `concepts/04` (DFS), `concepts/07` (topological sort — this is
"longest path in a DAG"), `01-course-schedule.md` (for contrast: there you
*needed* cycle detection; here you provably don't). New idea: **recognize when a
transition rule forbids cycles**, and drop the visited-set / 3-color scheme
entirely.

---

## 1. Problem

Given an `m x n` integer matrix, return the length of the **longest strictly
increasing path**. From a cell you may move to a 4-directional neighbor
(up/down/left/right — no diagonals, no wrapping) only if that neighbor's value is
**strictly greater**.

Constraints:
- `1 <= m, n <= 200`.
- `0 <= matrix[r][c] <= 2^31 - 1`.

Example 1:

```
matrix = [[9,9,4],
          [6,6,8],
          [2,1,1]]
answer = 4        # path 1 -> 2 -> 6 -> 9
```

Example 2:

```
matrix = [[3,4,5],
          [3,2,6],
          [2,2,1]]
answer = 4        # path 3 -> 4 -> 5 -> 6
```

---

## 2. Explain Like I'm 5

Picture the matrix as a landscape where the number is the height of each square.
You're a raindrop, but a weird one that only ever flows **uphill**, one step at a
time, to a strictly taller neighboring square. You want the **longest uphill walk
you can take**, starting anywhere.

The nice thing about only-ever-uphill: **you can never loop back.** To return to a
square you left, you'd have to come back *down* at some point — which you're not
allowed to do. So there are no circles to worry about.

To find the longest walk from a square, ask each taller neighbor "how long is the
longest walk starting from you?", take the best answer, and add 1 for the square
you're standing on. Write that number on the square so you never have to
recompute it. The biggest number you write anywhere is the answer.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Grid, "longest path" under a **monotonic** constraint | ✅ strictly increasing |
| The constraint means you can **never revisit** a cell | ✅ → the state graph is a **DAG** |
| Paths overlap heavily (many share suffixes) | ✅ → **memoize** |

**Reduce it to:** *"Longest path in a DAG. Each cell points to its
strictly-greater neighbors; `f(cell) = 1 + max(f(successor))` (or `1` if no
greater neighbor). Memoize. Answer is `max(f(cell))` over all cells."*

**Why it lives in the topological-sort group:** "longest path in a DAG" is a
topological-order DP. The memoized DFS computes it in a *valid* topological order
implicitly (via the recursion); the Kahn's-algorithm alternative (§9a) computes
it by explicit layer-peeling. Same DP, two framings.

**Contrast with Course Schedule:** there, the graph *could* have a cycle, so you
needed cycle detection (Kahn's leftover count, or 3-color DFS). Here, the
strict-increase rule makes a cycle **structurally impossible** — so you use a
plain memo grid and **no** visited set, **no** colors. Recognizing this is the
whole point of the problem.

---

## 4. Intuition

1. Model each cell as a node with an edge to every strictly-greater 4-neighbor.
2. **This graph is a DAG.** A cycle would require values `a < b < c < ... < a`
   around a loop — impossible for real numbers. So no cell can ever be reached
   again once you leave it.
3. Define `f(r, c)` = length of the longest strictly increasing path **starting**
   at `(r, c)`. Then `f(r, c) = 1 + max(f(nr, nc))` over all strictly-greater
   neighbors, or just `1` if there are none.
4. Many cells' `f` values get asked for repeatedly (paths branch and merge), so
   **memoize** `f` in an `m x n` grid. With memoization, each cell's `f` is
   computed exactly once → `O(m*n)`.
5. **Because the graph is a DAG, memoized DFS is completely safe with no cycle
   guard.** If you recurse into `(nr, nc)` while `f(r, c)` is still being
   computed, `(nr, nc)` is strictly greater than `(r, c)` — you're going "up," and
   you can never come back down to `(r, c)` within that recursion. There is no
   possible infinite loop.
6. `memo[r][c] = 0` doubles as "not computed yet" — safe, because a real answer
   is always `>= 1` (every cell is a path of length 1 by itself).

---

## 5. Approach (primary): memoized DFS

1. Guard the empty matrix. `m, n = len(matrix), len(matrix[0])`.
2. `memo = [[0] * n for _ in range(m)]` (`0` = uncomputed).
3. `dfs(r, c)`:
   - If `memo[r][c]`: return it.
   - `best = 1`. For each of the 4 neighbors `(nr, nc)` in bounds with
     `matrix[nr][nc] > matrix[r][c]`: `best = max(best, 1 + dfs(nr, nc))`.
   - `memo[r][c] = best`; return `best`.
4. Return `max(dfs(r, c) for every cell)`.

> Recursion depth: `m, n` up to `200` → up to `40,000` cells → a monotone
> snake-shaped path recurses `~40,000` deep, past Python's default limit (~1000).
> Add `sys.setrecursionlimit(250_000)` at the top, **or** use the iterative
> Kahn's version (§9a), which has no recursion at all.

Builds on: `concepts/04` (DFS) + memoization (DAG-DP), `concepts/07` (this *is*
longest-path-in-a-DAG).

---

## 6. Pseudocode

```
function longestIncreasingPath(matrix):
    if matrix empty: return 0
    m, n = rows, cols
    memo = m x n grid of 0

    function dfs(r, c):
        if memo[r][c] != 0: return memo[r][c]
        best = 1
        for each of 4 neighbors (nr, nc):
            if in bounds and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        memo[r][c] = best
        return best

    return max(dfs(r, c) for all cells (r, c))
```

---

## 7. Dry Run

```
matrix = [[9,9,4],
          [6,6,8],
          [2,1,1]]
```

`dfs` is called on every cell; memo fills in. Trace the cells on the answer path:

| call | greater neighbors | recurses into | result | memo after |
|---|---|---|---|---|
| dfs(2,1) [val 1] | (1,1)=6, (2,0)=2 | dfs(1,1), dfs(2,0) | 1 + max(f(1,1), f(2,0)) | |
| ↳ dfs(2,0) [val 2] | (1,0)=6 | dfs(1,0) | 1 + f(1,0) | |
| ↳↳ dfs(1,0) [val 6] | (0,0)=9 | dfs(0,0) | 1 + f(0,0) | |
| ↳↳↳ dfs(0,0) [val 9] | none | — | **1** | memo[0][0]=1 |
| ↳↳ dfs(1,0) resolves | | | 1 + 1 = **2** | memo[1][0]=2 |
| ↳ dfs(2,0) resolves | | | 1 + 2 = **3** | memo[2][0]=3 |
| ↳ dfs(1,1) [val 6] | (0,1)=9, (1,2)=8 | dfs(0,1), dfs(1,2) | | |
| ↳↳ dfs(0,1) [val 9] | none | — | **1** | memo[0][1]=1 |
| ↳↳ dfs(1,2) [val 8] | none ((0,2)=4 < 8) | — | **1** | memo[1][2]=1 |
| ↳ dfs(1,1) resolves | | | 1 + max(1,1) = **2** | memo[1][1]=2 |
| dfs(2,1) resolves | | | 1 + max(f(1,1)=2, f(2,0)=3) = **4** | memo[2][1]=4 |

Every other cell's `dfs` reuses memo where possible. `max` over all cells = `4`
(from `(2,1)`, the path `1 → 2 → 6 → 9`). ✅

---

## 8. Python Code (primary — memoized DFS)

```python
import sys
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        sys.setrecursionlimit(250_000)          # a 200x200 monotone path can recurse ~40k deep
        m, n = len(matrix), len(matrix[0])
        memo = [[0] * n for _ in range(m)]       # 0 == not computed yet (real answers are >= 1)

        def dfs(r: int, c: int) -> int:
            if memo[r][c]:
                return memo[r][c]
            best = 1
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            memo[r][c] = best
            return best

        return max(dfs(r, c) for r in range(m) for c in range(n))


if __name__ == "__main__":
    sol = Solution()

    assert sol.longestIncreasingPath([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
    assert sol.longestIncreasingPath([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4
    assert sol.longestIncreasingPath([[1]]) == 1
    assert sol.longestIncreasingPath([[7, 7], [7, 7]]) == 1                 # all equal -> no move
    assert sol.longestIncreasingPath([[1, 2, 3], [6, 5, 4], [7, 8, 9]]) == 9  # spiral, whole grid
    assert sol.longestIncreasingPath([[1, 2], [3, 4]]) == 3                  # 1->2->4 or 1->3->4

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Kahn's algorithm / topological peeling (no recursion — the pure Group 06 framing)

Treat edges as `smaller -> larger`. A cell's **indegree** = how many strictly
*smaller* 4-neighbors it has. Cells with indegree `0` (no smaller neighbor — a
local minimum) are the **starts** of increasing paths. BFS-peel layer by layer;
the number of layers is the longest increasing path length.

```python
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        indegree = [[0] * n for _ in range(m)]

        for r in range(m):
            for c in range(n):
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                        indegree[nr][nc] += 1        # a smaller neighbor points into (nr, nc)

        q = deque((r, c) for r in range(m) for c in range(n) if indegree[r][c] == 0)
        length = 0

        while q:
            length += 1
            for _ in range(len(q)):                  # freeze the layer (Rotting Oranges style)
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                        indegree[nr][nc] -= 1
                        if indegree[nr][nc] == 0:
                            q.append((nr, nc))

        return length
```

Same `O(m*n)`, no recursion, and it makes the "this is topological sort" nature
explicit. Pick this if recursion depth is a concern and you'd rather not fiddle
with `sys.setrecursionlimit`.

### The BFS↔DFS answer the interviewer wants

> "Memoized DFS is the most natural — `f(cell) = 1 + max(f(greater neighbor))` —
> and because the strict-increase rule makes the graph a DAG, it needs no visited
> set at all. Its only wrinkle is recursion depth on a large monotone grid, fixed
> by raising the limit or switching to the Kahn's layer-peeling version, which is
> the same DAG-DP done iteratively. Both `O(m*n)`."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = m*n`; edge = "cell → strictly-greater 4-neighbor,"
so `E ≤ 4 * m*n = O(m*n)`.

**Time:**
- Memoized DFS: `dfs(r, c)`'s body runs **once** per cell (the `memo` check
  short-circuits every later call). Each run does `O(1)` work + 4 neighbor
  checks. The outer `max` iterates all cells. → `O(m*n)`.
- Kahn's: build indegree grid `O(m*n)`; each cell enqueued once, each edge
  relaxed once → `O(m*n)`.
- **Total: `O(m * n)`.** (Without memo, DFS would be exponential — every branch
  re-explored.)

**Space:**
- `memo` (or `indegree`) grid: `O(m*n)`.
- Recursion stack (DFS): `O(m*n)` worst case (a monotone snake). Kahn's queue:
  `O(m*n)`.
- **Total: `O(m * n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| Empty matrix | `if not matrix or not matrix[0]: return 0` |
| Single cell | `dfs` returns `1` (no neighbors) |
| All cells equal | no cell has a strictly-greater neighbor → every `f` is `1` → answer `1` |
| Strictly increasing across the whole grid (a spiral or a raster) | one path covers every cell → answer `m*n` |
| Single row / single column | bounds check handles the missing dimension |
| Large values near `2^31 - 1` | plain integer comparison, no overflow concern in Python |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Adding a visited set / 3-color scheme "to be safe."** Unnecessary — the
      strict-increase rule already forbids cycles. Worse, a mark-and-don't-unmark
      visited set would *wrongly block* legitimate re-entries of a cell from a
      different path, undercounting.
- [ ] **Using `>=` instead of `>`** for the neighbor check. Turns it
      non-strict → equal-valued adjacent cells form cycles → memoized DFS can
      infinite-loop (or, with the recursion limit, crash). See Scenario 2.
- [ ] **`memo` init that can collide with a real answer.** `0` works because
      answers are `>= 1`. Initializing to `1` (or anything a real path could
      equal) breaks the "computed?" check.
- [ ] **Off-by-one:** `best = max(best, dfs(nr, nc))` instead of
      `1 + dfs(nr, nc)` — forgets to count the current cell.
- [ ] **Recursion depth** on a `200 x 200` monotone grid without
      `sys.setrecursionlimit` — `RecursionError`.
- [ ] **Kahn's version: not freezing `len(q)` per layer** — collapses all layers
      into one pass, returns `1` (or a wrong small number). Same trap as Rotting
      Oranges.
- [ ] **Kahn's version: peeling by outdegree when you meant indegree** (or vice
      versa) — get the edge direction straight: `smaller -> larger`, start from
      indegree-0 (local minima).

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Recognize an implicit DAG.** When a transition rule is strictly monotone (or
   otherwise makes returning impossible), the state graph is acyclic *by
   construction* — memoized DFS then needs **no** visited set, **no** colors.
   Spotting this removes a whole layer of machinery.
2. **Longest path in a DAG = topological-order DP:** `f(node) = base +
   max(f(successor))`. Compute it via memoized DFS (implicit topological order) or
   Kahn's layer-peeling (explicit) — same DP.
3. **Objective is separable from structure.** Count cells / sum values / count
   paths — all the same DAG traversal, different accumulator (cf. Max Area of
   Island → perimeter, Clone Graph → serialize).
4. **Sentinel-as-uncomputed:** `memo = 0` is safe when real answers can't be `0`
   — same trick as `dist = -1` (01 Matrix), `INF` (Walls and Gates).

| Situation | How this transfers |
|---|---|
| **Longest Increasing Subsequence** | the 1D cousin — LIS is the longest increasing path in a 1D array; this is its 2D, adjacent-moves-only version (`O(m*n)` DAG-DP; the `O(n log n)` LIS trick doesn't apply) |
| Longest path in any DAG (task critical path) | `f(node) = weight + max(f(successor))` in topological order |
| "Number of increasing paths of max length" | DAG path counting alongside the length DP (Scenario 5) |
| Course Schedule Scenario 3 (min time with parallelism) | also longest-path-in-a-DAG, just on an explicit dependency graph |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Return the actual longest path (the list of cell coordinates), not just its length."

- **(b) Pattern:** DAG-DP + a **choice pointer**, reconstruct at the end.
- **(c) Adapt:** alongside `memo[r][c]`, store `next_cell[r][c]` = which greater
  neighbor produced the max (or `None`). Find the global-max starting cell, then
  follow `next_cell` pointers to emit the path. `O(m*n)` time and space,
  reconstruction `O(path length)`.
- **(d) Say:** "Same as every 'give me the path, not the number' variant — record
  which successor won at each cell, then walk those pointers from the best
  start."

### Scenario 2 — "Allow moving to strictly-greater **or equal** cells (non-strictly increasing)."

- **(b) Pattern:** **the implicit-DAG guarantee breaks.** Equal-valued adjacent
  cells now form cycles — you could bounce between two `5`s forever. Memoized DFS
  with no cycle guard would infinite-loop.
- **(c) Adapt:** first **collapse each connected region of equal values into a
  super-node** (Union-Find or flood fill). Build a DAG on the super-nodes (an
  edge from region A to region B if some cell of A is adjacent to a strictly-
  greater cell of B). Then run the same longest-path DAG-DP on the super-nodes,
  where each super-node's "length contribution" might be `1` (if a path just
  passes through) or more, depending on the exact problem definition of path
  length within an equal region.
- **(d) Say:** "Relaxing `>` to `>=` destroys the acyclic-by-construction
  property — I'd Union-Find the equal-valued regions into super-nodes to recover
  a DAG, then run the same DP. This is the same 'my assumption just broke' move
  as walls breaking the 2-pass DP in 01 Matrix."

### Scenario 3 — "Diagonal moves are allowed too (8-directional)."

- **(b) Pattern:** same algorithm, wider neighbor set.
- **(c) Adapt:** swap `DIRS` for `DIRS8`. Still strictly increasing → still a DAG
  → still `O(m*n)` (constant factor 8 vs 4).
- **(d) Say:** "Neighbor-set change only; the DAG property and the DP are
  untouched."

### Scenario 4 — "The matrix is `10^4 x 10^4` (`10^8` cells). Memory for the memo grid is a concern."

- **(b) Pattern:** the `O(m*n)` memo (or indegree) grid is essentially
  unavoidable — the answer genuinely depends on the whole grid.
- **(c) Adapt:** you can shave constants — store `memo` as a flat array of 32-bit
  ints instead of a list-of-lists, or reuse the indegree grid in-place. If the
  increasing structure is *local* (paths never span more than a bounded window),
  you could tile the grid and stitch results at tile boundaries — but in general,
  `O(m*n)` space is the floor. Time stays `O(m*n)`, which at `10^8` is large but
  linear.
- **(d) Say:** "This is already time- and space-optimal at `O(m*n)`; at `10^8`
  cells I'd focus on constant factors (flat 32-bit array, in-place reuse) rather
  than a better asymptotic, since the answer depends on every cell."

### Scenario 5 — "Count the **number of distinct longest increasing paths** (paths achieving the maximum length)."

- **(b) Pattern:** **DAG path counting** layered on the length DP (the same idea
  as Number of Ways to Arrive at Destination, coming in Group 10).
- **(c) Adapt:** compute `length[r][c]` as before. Also compute `count[r][c]`:
  the number of longest paths starting at `(r, c)`. When a greater neighbor
  achieves `length[r][c] - 1` (i.e. it's on a longest continuation),
  `count[r][c] += count[neighbor]`; if a cell has no greater neighbor,
  `count[r][c] = 1`. The answer is `sum(count[r][c] for cells whose length ==
  global max AND which are path starts — indegree 0)`. `O(m*n)`.
- **(d) Say:** "Counting longest paths in a DAG is the length DP plus a parallel
  count DP: sum the counts of every successor that lies on a longest
  continuation."

### Scenario 6 — "A path's 'value' is the **sum** of cell values along it (not the count of cells). Find the maximum-sum strictly increasing path."

- **(b) Pattern:** identical DAG, different accumulator.
- **(c) Adapt:** change the recurrence to `best[r][c] = matrix[r][c] + max(0,
  max over greater neighbors of best[neighbor])`. Everything else — the DAG
  structure, the memoization, the `O(m*n)` bound — is unchanged.
- **(d) Say:** "The structure is invariant; only the quantity being accumulated
  changes. Path *length* → count of cells; path *value* → sum of cells; one line
  of the recurrence."

---

## 15. Flashcards

**Q:** Why does memoized DFS here need **no** visited set or 3-color scheme?
**A:** Moves are strictly increasing, so a cycle (`a < b < ... < a`) is
impossible — the graph is a DAG by construction.

**Q:** The recurrence?
**A:** `f(r, c) = 1 + max(f(neighbor))` over strictly-greater 4-neighbors, or `1`
if none. Answer = `max(f)` over all cells.

**Q:** Why does `memo[r][c] = 0` work as the "not computed" sentinel?
**A:** A real answer is always `>= 1` (every cell is a length-1 path by itself),
so `0` can't collide with a legitimate value.

**Q:** What breaks if you change `>` to `>=`?
**A:** Equal-valued adjacent cells form cycles → the graph is no longer a DAG →
memoized DFS can infinite-loop. Fix: Union-Find the equal regions into
super-nodes first.

**Q:** The recursion-depth caveat, and the two fixes?
**A:** A `200x200` monotone grid recurses `~40k` deep, past Python's ~1000
limit. Fix: `sys.setrecursionlimit(...)`, or use the iterative Kahn's
layer-peeling version.

**Q:** Time and space, with derivation?
**A:** `O(m*n)` both. Memo makes each cell's `f` compute once; without it DFS is
exponential.

**Q:** How does this relate to Longest Increasing Subsequence?
**A:** LIS is the 1D cousin. This is the 2D, adjacent-moves-only version, solved
by `O(m*n)` DAG-DP (the `O(n log n)` LIS trick doesn't apply).

**Q:** "Max-sum increasing path instead of longest" — the change?
**A:** One line: `best[r][c] = matrix[r][c] + max(0, max over greater neighbors
of best[neighbor])`. Same DAG, different accumulator.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Memoized DFS — same algorithm as the primary,
with the memo as a **dict keyed by `(r, c)` tuples** instead of a 2D list.
`O(m*n)` time and space.

```python
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        maxi = 0
        memo = {}

        rows = len(matrix)
        columns = len(matrix[0])

        def dfs(r, c):
            if (r, c) in memo:
                return memo[(r, c)]

            res = 1
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < columns and matrix[nr][nc] > matrix[r][c]:
                    res = max(res, 1 + dfs(nr, nc))

            memo[(r, c)] = res
            return res

        for r in range(rows):
            for c in range(columns):
                maxi = max(maxi, dfs(r, c))

        return maxi
```

**Correct** — verified against all 6 tests from section 8.

**Two small notes (neither is a bug):**

1. **`dict` memo vs 2D-list memo.** A `dict` keyed by `(r, c)` works fine and
   reads cleanly. A 2D `list` of ints (the primary) is a bit faster
   (no tuple hashing, contiguous memory) and, for a fully-dense grid where every
   cell gets computed anyway, uses comparable memory. Either is a fine
   interview answer; mention the trade-off if asked. The `dict` shines only when
   the grid is huge but you expect to touch just a sparse subset of cells.
2. **No `sys.setrecursionlimit` bump.** Same caveat as the primary's section 5
   note: at the constraint's upper bound (`200×200`), a monotone snake path
   recurses ~40,000 deep and would hit Python's default limit (~1000). For a
   real submission at that size, add `sys.setrecursionlimit(250_000)` at the top,
   or use the iterative Kahn's version (§9a). It passes here because the test
   grids are small.
