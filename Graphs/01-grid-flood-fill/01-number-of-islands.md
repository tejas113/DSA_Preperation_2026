# Number of Islands  ·  LeetCode 200  ·  Medium

Group 01 — Grid Flood-Fill  ·  the canonical "count connected blobs" problem.
If you truly understand this one, 8 other problems become easy.

Prereqs: `concepts/01` (Python), `concepts/02` (grid as a graph), `concepts/03` or
`concepts/04` (BFS/DFS), `concepts/05` (connected components), `concepts/17`
(complexity).

---

## 1. Problem

You are given an `m x n` grid. Each cell is `"1"` (land) or `"0"` (water). An
**island** is a group of `"1"` cells connected **horizontally or vertically** (not
diagonally). Water surrounds everything, and the grid edge counts as water.

**Return the number of islands.**

Constraints:
- `1 <= m, n <= 300` → up to 90,000 cells.
- Each cell is the character `"1"` or `"0"` (note: **strings**, not ints).

Example 1:

```
grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"],
]
answer = 1        # all the 1s are connected into one blob
```

Example 2:

```
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"],
]
answer = 3        # top-left blob, the single middle 1, the bottom-right pair
```

---

## 2. Explain Like I'm 5

Imagine a paper map. Green squares are land, blue squares are sea. Some green
squares touch each other (side by side, not just corners) — those form one island.

You have a green crayon. You put your finger on a green square you haven't colored
yet, and you **scribble over that whole island**: color this square, then walk to
each green neighbor and color it too, and keep going until the whole island is
crayoned. That was **1 island** — write it down.

Then you scan the map for the next green square that still isn't crayoned. Found
one? That's a **new** island — scribble it, add 1. Repeat until every green square
is crayoned.

The count you wrote down is the answer. "Scribble over the whole island" = flood
fill. "Scan for the next uncrayoned green square" = the outer loop.

---

## 3. Pattern Identification

**Signals that scream "grid flood-fill / count components":**

| Signal | Present here? |
|---|---|
| Input is a 2D grid of two kinds of cells | ✅ `"1"` / `"0"` |
| "connected horizontally/vertically" | ✅ 4-directional |
| Asked to **count** groups ("number of islands") | ✅ |
| No mention of "shortest", "fewest steps", "distance" | ✅ so **not** BFS-for-distance, **not** Dijkstra |
| No weights, no direction | ✅ plain traversal |

**Reduce it to:** *"Count connected components in a graph where nodes are `"1"`
cells and edges connect 4-adjacent `"1"` cells."* → `concepts/05` skeleton, flood =
DFS or BFS.

**Look-alikes (don't confuse):**
- "Distance from each water cell to nearest land" → **multi-source BFS** (Group 02).
- "Shortest path from top-left to bottom-right" → **BFS for distance** (Group 13).
- "Largest island" → same pattern, but flood returns a size (next problem).
- "Islands that don't touch the border" → **boundary-anchored** (Group 03).

---

## 4. Intuition

Build it up one sentence at a time:

1. Every `"1"` cell belongs to exactly one island.
2. If I start at some `"1"` cell and visit every `"1"` I can walk to (up/down/left/
   right, only stepping on `"1"`), I have found **one entire island**.
3. If I mark each visited cell so I never visit it again, then a cell is visited
   **exactly once** in its whole life.
4. So: scan the grid. Every time I hit a `"1"` that is **not yet visited**, it must
   be the first cell of an island I haven't counted → add 1, then flood the rest of
   that island so those cells get marked and skipped.
5. When the scan finishes, I've counted each island exactly once.

**Why it's correct:** the flood marks *all* cells of an island, so the outer scan
can only "discover" each island through its first-encountered cell — never twice.
And every `"1"` is reachable from some first cell, so no island is missed.

---

## 5. Approach (primary): DFS flood

1. Handle the empty grid: if `grid` is empty, return `0`.
2. `m, n = len(grid), len(grid[0])`. Make `seen = set()`.
3. Define `dfs(r, c)`:
   - If `(r, c)` is off the board → return.
   - If `(r, c)` is water (`"0"`) or already in `seen` → return.
   - Add `(r, c)` to `seen`.
   - Recurse into all 4 neighbors.
4. `count = 0`. Loop `r` in `0..m-1`, `c` in `0..n-1`:
   - If `grid[r][c] == "1"` and `(r, c) not in seen`: `count += 1`, then `dfs(r, c)`.
5. Return `count`.

Builds on: `concepts/04` (DFS on a grid), `concepts/05` (loop + flood skeleton).

---

## 6. Pseudocode

```
function numIslands(grid):
    if grid is empty: return 0
    m, n = rows, cols
    seen = empty set
    count = 0

    function dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n: return
        if grid[r][c] == "0" or (r, c) in seen: return
        add (r, c) to seen
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in 0..m-1:
        for c in 0..n-1:
            if grid[r][c] == "1" and (r, c) not in seen:
                count = count + 1
                dfs(r, c)

    return count
```

---

## 7. Dry Run

Grid:

```
   c0 c1 c2
r0  1  0  1
r1  1  0  0
r2  0  0  1
```

Expected islands: `{(0,0),(1,0)}`, `{(0,2)}`, `{(2,2)}` → **3**.

Trace the outer loop (`.` = already in `seen`):

| (r,c) | grid | in seen? | action | seen after | count |
|---|---|---|---|---|---|
| (0,0) | 1 | no | count→1; dfs(0,0) floods (0,0),(1,0) | {(0,0),(1,0)} | 1 |
| (0,1) | 0 | — | skip (water) | — | 1 |
| (0,2) | 1 | no | count→2; dfs(0,2) floods (0,2) only (neighbors are water/off) | {(0,0),(1,0),(0,2)} | 2 |
| (1,0) | 1 | **yes** | skip (already flooded) | — | 2 |
| (1,1),(1,2) | 0 | — | skip | — | 2 |
| (2,0),(2,1) | 0 | — | skip | — | 2 |
| (2,2) | 1 | no | count→3; dfs(2,2) floods (2,2) | {...,(2,2)} | 3 |

Return **3**. ✅

Inside `dfs(0,0)` specifically:
- add (0,0). Recurse: (1,0) land+unseen → add (1,0). From (1,0): (2,0) water,
  (0,0) seen, (1,1) water, (1,-1) off. Back to (0,0): (-1,0) off, (0,1) water,
  (0,-1) off. Done — island is `{(0,0),(1,0)}`.

---

## 8. Python Code (primary — DFS)

```python
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def dfs(r: int, c: int) -> None:
            if not (0 <= r < m and 0 <= c < n):        # off the board
                return
            if grid[r][c] == "0" or (r, c) in seen:    # water, or already visited
                return
            seen.add((r, c))
            for dr, dc in DIRS:
                dfs(r + dr, c + dc)

        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1" and (r, c) not in seen:
                    count += 1          # a brand-new island
                    dfs(r, c)           # sink the rest of it
        return count


if __name__ == "__main__":
    sol = Solution()

    g1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert sol.numIslands(g1) == 1

    g2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert sol.numIslands(g2) == 3

    assert sol.numIslands([["0"]]) == 0
    assert sol.numIslands([["1"]]) == 1
    assert sol.numIslands([["1", "0", "1", "0", "1"]]) == 3   # single row
    assert sol.numIslands([]) == 0

    print("all tests passed")
```

> Note: we pass `seen` as a set and **don't** mutate `grid`. If the interviewer
> says "you may modify the input" you can drop `seen` and set `grid[r][c] = "0"`
> when you visit — saves the `O(m*n)` set. Always *ask* before mutating input.

---

## 9. Alternative Approaches

### 9a. BFS flood (use when recursion depth is a worry)

Same skeleton, the flood is a queue instead of recursion. **Mark cells seen when
you enqueue them** (house rule) so they aren't queued twice.

```python
from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def bfs(sr: int, sc: int) -> None:
            q = deque([(sr, sc)])
            seen.add((sr, sc))
            while q:
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n
                            and grid[nr][nc] == "1" and (nr, nc) not in seen):
                        seen.add((nr, nc))     # mark on enqueue
                        q.append((nr, nc))

        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1" and (r, c) not in seen:
                    count += 1
                    bfs(r, c)
        return count
```

When to pick BFS: grid up to `300×300` here is fine for recursion **if** you
`sys.setrecursionlimit(10**6)`; but if the interviewer bumps it to `10^6 × 10^6`
solid land, BFS is the safe answer.

### 9b. Union-Find (overkill here, but shows the connection to Group 07)

Give each cell an id `r*n + c`. For every land cell, `union` it with its right and
down land neighbors. The answer is the number of distinct roots among land cells.

```python
class Solution:
    def numIslands(self, grid):
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        parent = list(range(m * n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            parent[find(a)] = find(b)

        count = sum(row.count("1") for row in grid)
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1":
                    for dr, dc in ((1, 0), (0, 1)):
                        nr, nc = r + dr, c + dc
                        if nr < m and nc < n and grid[nr][nc] == "1":
                            if find(r * n + c) != find(nr * n + nc):
                                union(r * n + c, nr * n + nc)
                                count -= 1
        return count
```

When to pick Union-Find: when land is **added one cell at a time** and you must
report the island count after each addition ("Number of Islands II"). For the
static grid, DFS/BFS is simpler and just as fast.

### The BFS↔DFS answer the interviewer wants

> "Both are `O(m*n)` time and space. DFS is a few lines shorter and reads
> naturally. DFS risks a Python recursion-limit crash on a very large solid island;
> BFS with an explicit queue has no depth limit. I'd write DFS and mention I'd
> switch to BFS or raise the recursion limit for adversarial input sizes."

---

## 10. Complexity — derived step by step

**Define V and E for this problem** (`concepts/17`, step 1):
- A node = a grid cell. `V = m * n`.
- An edge = adjacency between two 4-neighbor cells. Each cell has ≤ 4 edges, each
  edge shared by 2 cells → `E ≈ 2mn = O(m*n)`.

**Time:**
- Outer double loop: exactly `m * n` iterations → `O(m*n)`.
- All `dfs` calls together: each cell is added to `seen` once; a `dfs` call that
  hits a seen/water/off cell returns in `O(1)`. Each cell triggers ≤ 4 child calls.
  Total calls ≤ `5 * m * n` → `O(m*n)`.
- The outer loop and the floods **don't multiply** — the `seen` check means the
  total flooding work is `O(m*n)` no matter how the loop and floods interleave.
- **Total: `O(m * n)`** = `O(V + E)`.

**Space:**
- `seen` set: up to `m*n` tuples → `O(m*n)`.
- Recursion stack (DFS): worst case one snake-shaped island filling the grid →
  depth `O(m*n)`. (BFS queue: same worst-case `O(m*n)`.)
- Output: a single integer → `O(1)`.
- **Total: `O(m * n)`.**
- Space-optimized: mutate `grid` instead of `seen` → still `O(m*n)` recursion worst
  case, but no extra set; iterative BFS with in-place marking → `O(min(m, n))`
  typical queue size, `O(m*n)` worst case.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `grid == []` or `grid == [[]]` | `if not grid or not grid[0]: return 0` |
| All water | outer loop never triggers a flood → returns `0` |
| All land | first cell floods everything → returns `1` |
| Single cell `[["1"]]` / `[["0"]]` | returns `1` / `0` |
| Single row or single column | bounds check `0 <= r < m` / `0 <= c < n` handles the missing dimension |
| Diagonal-only touching `1`s | `DIRS` has no diagonals → correctly counted as separate islands |
| Cells are strings `"1"`, not ints `1` | compare with `"0"` / `"1"` (a classic bug: `grid[r][c] == 1` is always `False`) |
| Very large solid island (recursion depth) | switch to BFS, or `sys.setrecursionlimit` |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **String vs int:** comparing `grid[r][c] == 1` instead of `== "1"`. Silent
      wrong answer (`0`).
- [ ] **Bounds check order:** doing `grid[r][c]` *before* checking `0 <= r < m`.
      Throws `IndexError` (or wraps around with negative indices — even worse,
      silent wrong answer, because `grid[-1]` is the last row!).
- [ ] **Marking seen too late:** in BFS, adding to `seen` after `popleft` instead of
      before `append`. The queue fills with duplicates; usually still correct but
      slow, sometimes TLE.
- [ ] **Forgetting the outer `not in seen` check:** re-flooding an already-counted
      island. Over-counts. (Even though `dfs` would immediately return, the
      `count += 1` already fired.)
- [ ] **Only 2 directions** in `DIRS` (forgot up/left): merges islands incorrectly.
- [ ] **`seen` reset inside the loop:** declaring `seen = set()` inside the double
      loop wipes history every cell → massive over-count.
- [ ] **Mutating `grid` while also iterating the same cells for a second purpose**
      (only relevant in the in-place variant).

**How to narrate debugging to the interviewer:** "My count is 5, expected 3. Let me
print the grid after processing to see which cells got marked… ah, `(0,2)` and
`(0,0)` are in different islands but I only marked one — my `DIRS` is missing the
left direction."

---

## 13. Learnings & Transfer

**What this problem teaches (the reusable core):**
1. **The loop + flood skeleton** for counting/measuring connected components.
2. **Mark-visited discipline**: a cell is processed exactly once; the visited check
   is what makes the whole thing linear.
3. **Grid = graph**: 4 neighbors via a `DIRS` constant, bounds check before index.
4. **DFS vs BFS are interchangeable** for pure connectivity; choose by
   recursion-depth risk.

**Direct reuse in other problems:**

| Problem | How this transfers |
|---|---|
| Max Area of Island (Group 01) | same skeleton; `dfs` returns `1 + sum(children)` instead of `None`; track `max` |
| Flood Fill (Group 01) | just the flood, no outer loop; recolor instead of `seen` |
| Number of Provinces (Group 07) | components again, but nodes are people and "grid" is an adjacency matrix |
| Surrounded Regions (Group 03) | flood, but *seeded from the border* to find the safe cells, then flip the rest |
| Rotting Oranges (Group 02) | grid + neighbors, but BFS from **all** rotten cells at once, counting layers |
| Walls and Gates / 01 Matrix (Group 02) | grid + neighbors + multi-source BFS for distances |
| Making a Large Island (Group 01) | flood to label + size each island, then probe every water cell |
| Word Ladder (Group 13) | same "loop discovers, flood/BFS marks" idea, but the graph is implicit |

---

## 14. Scenario-Based Questions (Google standard)

For each: **(a)** the scenario as an interviewer poses it, **(b)** the pattern it
reduces to, **(c)** how to adapt *this* solution, **(d)** the transferable pattern
to name aloud.

### Scenario 1 — "We're processing satellite imagery. Land pixels are added to the map one at a time as new data streams in. After each new pixel, report the current number of separate land masses."

- **(b) Pattern:** incremental connectivity → **Union-Find** (Group 07), *not*
  flood fill. Flood fill would re-scan the whole grid after every pixel = `O((m*n)²)`.
- **(c) Adapt:** keep a `DSU` over `m*n` cell ids and a running `count`. On each new
  land pixel `(r, c)`: `count += 1`, mark it land, then for each of its 4 neighbors
  that is already land, `if dsu.union(id, nid): count -= 1`. Append `count` to the
  answer list. Each addition is amortized `O(α(m*n)) ≈ O(1)`.
- **(d) Say:** "Dynamic connectivity under edge/vertex insertions is Union-Find's
  home turf; flood fill is for a static snapshot."

### Scenario 2 — "The grid is 10^6 × 10^6 but almost all water, given as a list of the (few) land coordinates. Count islands."

- **(b) Pattern:** same component count, but the grid is **sparse** — you can't
  allocate `10^12` cells.
- **(c) Adapt:** put the land coordinates in a `set`. Run DFS/BFS over the *set*:
  neighbors of `(r, c)` are the 4 offsets that are also *in the set*. `seen` is a
  set of coordinates. Complexity becomes `O(L)` where `L` = number of land cells,
  independent of the `10^6` dimensions.
- **(d) Say:** "When the grid is huge and sparse, drop the 2D array and treat the
  land cells themselves as the node set — a hash set of coordinates."

### Scenario 3 — "Also allow diagonal connections. And later: what if 'connected' means within Chebyshev distance k?"

- **(b) Pattern:** identical, only the neighbor function changes.
- **(c) Adapt:** diagonals → use `DIRS8` (8 offsets). Distance `k` → neighbors are
  all `(r±i, c±j)` with `max(|i|,|j|) <= k`; that's `O(k²)` neighbors per cell, so
  time becomes `O(m * n * k²)`. Everything else is unchanged.
- **(d) Say:** "Connectivity problems are parameterized by the neighbor function;
  the traversal skeleton is invariant."

### Scenario 4 — "The grid doesn't fit in memory — it's streamed to you one row at a time, top to bottom. Count islands using O(n) extra space (n = row width)."

- **(b) Pattern:** components with a **sliding window of two rows** + Union-Find on
  columns (a.k.a. "online" connected components / the classic scanline union-find).
- **(c) Adapt:** keep a `DSU` over just the current row's `n` columns plus labels
  carried from the previous row. For each new row: union horizontally adjacent land
  cells, union with the land cell directly above (from the retained previous row),
  add new island count for land cells with no land left/up neighbor, and when an
  island has no cells in the new row, finalize it. Only two rows of state → `O(n)`.
- **(d) Say:** "Streaming/large-input variants of grid problems become scanline
  algorithms: keep O(row) state and a Union-Find keyed by column."

### Scenario 5 — "Now count islands, but you can flip at most one water cell to land. What's the maximum island size you could achieve?"

- **(b) Pattern:** this is exactly **Making a Large Island** (Group 01,
  supplementary) — flood-fill labeling + a probe pass.
- **(c) Adapt:** Pass 1: DFS each island, give it an `id` (start from 2 to avoid
  clashing with `0`/`1`) and record `size[id]`. Pass 2: for every water cell, look
  at its 4 neighbors, collect the **distinct** island ids, answer candidate =
  `1 + sum(size[id] for those ids)`. Track the max. Edge case: grid all land →
  answer is `m*n`.
- **(d) Say:** "When a problem adds 'you may change one cell', the move is usually:
  precompute component labels + sizes, then evaluate each candidate change in O(1)
  using those labels."

### Scenario 6 — "Parallelize island counting across 8 machines, each owning a horizontal strip of the grid."

- **(b) Pattern:** divide-and-conquer components + **merge along the seams** with
  Union-Find.
- **(c) Adapt:** each machine counts islands in its strip and labels cells with
  `(machine_id, local_label)`. Then a merge step: for each boundary row shared by
  two strips, `union` land cells that are vertically adjacent across the seam.
  Final count = total local islands − number of successful cross-seam unions.
- **(d) Say:** "Component problems parallelize as: solve locally, then union the
  labels that touch across partition boundaries."

---

## 15. Flashcards

**Q:** Trigger words for the grid flood-fill pattern?
**A:** 2D grid + "island/region/blob/area", "connected horizontally/vertically",
"how many groups" / "largest", and *no* mention of shortest path or distance.

**Q:** One-line skeleton for counting components on a grid?
**A:** Double-loop every cell; on an unvisited target cell, `count += 1` and
flood (DFS/BFS) to mark the whole blob.

**Q:** Where do you mark a cell visited in BFS, and why?
**A:** When you enqueue it, not when you dequeue it — otherwise it gets added to
the queue multiple times.

**Q:** Time and space for Number of Islands? Derivation?
**A:** `O(m*n)` both. Outer loop is `m*n`; the `seen` check makes total flood work
`O(m*n)` (not squared). Space = `seen` set + recursion/queue, each `O(m*n)` worst
case.

**Q:** Classic silent bug in this problem?
**A:** Comparing `grid[r][c] == 1` (int) when cells are `"1"` (string). Also
indexing `grid[r][c]` before the bounds check (negative index wraps around).

**Q:** When would you use Union-Find instead of flood fill for islands?
**A:** When land/edges are added incrementally and you must report the count after
each addition (Number of Islands II), or when merging results across partitions.

**Q:** DFS vs BFS here — the interview answer?
**A:** Both `O(m*n)`. DFS shorter; risks Python recursion-limit on a huge solid
island. BFS (explicit queue) has no depth limit. Pick DFS, mention the switch.

**Q:** How to handle a 10^6 × 10^6 mostly-water grid given as land coordinates?
**A:** Put land cells in a set; DFS/BFS over the set (neighbors = offsets present
in the set). Time `O(L)`, independent of the dimensions.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. DFS flood fill, `O(m*n)` time and space — same
pattern as the primary solution.

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows = len(grid)
        columns = len(grid[0])

        count = 0
        visited = set()

        def dfs(r, c):
            if not (0 <= r < rows and 0 <= c < columns):
                return

            if grid[r][c] == "0" or (r, c) in visited:
                return

            visited.add((r, c))
            grid[r][c] = "0"

            dfs(r, c + 1)
            dfs(r, c - 1)
            dfs(r + 1, c)
            dfs(r - 1, c)

        for r in range(rows):
            for c in range(columns):
                if grid[r][c] == "1" and (r, c) not in visited:
                    dfs(r, c)
                    count = count + 1

        return count
```

**Notes for next time (small polish, not bugs):**

1. **The bug that was here first:** `if not 0 <= r < rows and 0 <= c < columns` —
   without the parentheses, `not` only applied to `0 <= r < rows`, so most
   off-board cells slipped through and crashed with `IndexError` (or a negative
   index wrapped to the last row/column and silently merged islands). Fixed by
   wrapping the whole condition: `if not (0 <= r < rows and 0 <= c < columns)`.
   **Lesson:** for a bounds check, always negate the *entire* "in range" condition
   as one parenthesised group.
2. **`visited` and `grid[r][c] = "0"` do the same job.** Keeping both is correct
   but redundant. Pick one:
   - keep `visited`, drop the grid mutation → input stays intact (safer; do this
     unless told mutation is allowed);
   - keep the grid mutation, drop `visited` and the `(r, c) not in visited` check →
     less memory, but you destroy the input.
3. Style nits: `count += 1` reads better than `count = count + 1`; `rows, columns`
   is fine but the house style is `m, n` so it matches every other file.
