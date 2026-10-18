# Max Area of Island  ·  LeetCode 695  ·  Medium

Group 01 — Grid Flood-Fill  ·  Number of Islands, but the flood now **returns a
number** (the island's size) and we keep the biggest.

Prereqs: `01-number-of-islands.md`. New idea here: **a DFS that returns an
aggregate** — `area = 1 + sum(area of each neighbor)`.

---

## 1. Problem

You are given an `m x n` **binary** grid. `grid[r][c]` is `1` (land) or `0`
(water). An **island** is a group of `1`s connected 4-directionally (up, down,
left, right). The **area** of an island is the number of `1` cells in it.

**Return the maximum area of any island. If there is no island, return `0`.**

Constraints:
- `1 <= m, n <= 50`.
- `grid[r][c]` is `0` or `1` — **integers this time**, not the strings `"0"` /
  `"1"` you saw in Number of Islands. Watch that.

Example:

```
grid = [[0,0,1,0,0],
        [0,1,1,1,0],
        [0,0,1,0,0],
        [1,0,0,0,1]]

Island A (a plus shape): (0,2),(1,1),(1,2),(1,3),(2,2)  -> area 5
Island B: (3,0)  -> area 1
Island C: (3,4)  -> area 1

answer = 5
```

---

## 2. Explain Like I'm 5

Same map of green (land) and blue (sea) squares. This time you don't count the
islands — you want to know **which island is the biggest, and how many squares it
has**.

So you go island by island. For each one, you scribble over it like before, but
while you scribble you **count** every square you color. That count is that
island's size. You remember the largest count you've seen. When you've scribbled
every island, the largest count you remembered is the answer.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| 2D grid, land/water | ✅ |
| "island" = 4-directionally connected `1`s | ✅ |
| Asked for a **size / area / max**, not just a count | ✅ → the flood must **return** the size |
| Still one number per island, take the best | ✅ → `best = max(best, flood(...))` |

**Reduce it to:** *"For every connected component, compute its size; return the
maximum."* The flood returns `1 + sum(children)`.

**Look-alikes:**
- Number of Islands → flood returns nothing, `count += 1` per island.
- Making a Large Island → flood returns size **and** stamps an id so you can look
  the size up later.
- Number of Closed Islands / Count Sub-Islands → flood returns a **boolean**
  (`AND` of children) instead of a size.

---

## 4. Intuition

1. An island's area = (this cell: 1) + (area contributed by each of its 4
   neighbors that are also land and not yet counted).
2. That's a recursion: `dfs(cell)` returns the number of *new* land cells reachable
   from `cell`, including `cell` itself.
3. Base cases return `0`: off the board, water, or already counted — they add
   nothing.
4. Mark a cell `seen` the moment you enter it, so each land cell is counted
   exactly once (its `dfs` returns a real number the first time, `0` every time
   after).
5. The outer loop starts a fresh `dfs` at every not-yet-counted land cell; each
   such call returns one whole island's area. Keep the maximum.

**Why correct:** the `seen` guard means every land cell contributes `+1` to
exactly one `dfs` call — the first that reaches it — so each island's returned
number is exactly its cell count.

---

## 5. Approach (primary): DFS returning an area

1. Empty grid → return `0`.
2. `m, n = len(grid), len(grid[0])`; `seen = set()`.
3. `dfs(r, c) -> int`:
   - Off board → return `0`.
   - Water (`grid[r][c] == 0`) or `(r, c) in seen` → return `0`.
   - Add `(r, c)` to `seen`.
   - `area = 1`; for each of the 4 directions, `area += dfs(neighbor)`.
   - Return `area`.
4. `best = 0`. For every cell: if land and not seen, `best = max(best, dfs(r, c))`.
5. Return `best`.

Builds on: `concepts/04` grid-DFS, `concepts/05` loop-and-flood, plus the new
"return an aggregate from recursion" shape.

---

## 6. Pseudocode

```
function maxAreaOfIsland(grid):
    if grid empty: return 0
    m, n = rows, cols
    seen = empty set
    best = 0

    function dfs(r, c) -> int:
        if r,c off board: return 0
        if grid[r][c] == 0 or (r,c) in seen: return 0
        add (r,c) to seen
        area = 1
        area += dfs(r+1,c)
        area += dfs(r-1,c)
        area += dfs(r,c+1)
        area += dfs(r,c-1)
        return area

    for r in 0..m-1:
        for c in 0..n-1:
            if grid[r][c] == 1 and (r,c) not in seen:
                best = max(best, dfs(r, c))

    return best
```

---

## 7. Dry Run

```
grid = [[0,0,1,0,0],
        [0,1,1,1,0],
        [0,0,1,0,0],
        [1,0,0,0,1]]
```

Outer loop reaches `(0,2)` first (the earlier cells are water). Call `dfs(0,2)`:

| call | cell | land & unseen? | area so far | returns |
|---|---|---|---|---|
| dfs(0,2) | (0,2)=1 | yes → seen | 1 + children | |
| ↳ dfs(1,2) | (1,2)=1 | yes → seen | 1 + children | |
| ↳↳ dfs(2,2) | (2,2)=1 | yes → seen | 1 + children | |
| ↳↳↳ dfs(3,2) | (3,2)=0 | no | — | 0 |
| ↳↳↳ dfs(1,2) | seen | no | — | 0 |
| ↳↳↳ dfs(2,3) | (2,3)=0 | no | — | 0 |
| ↳↳↳ dfs(2,1) | (2,1)=0 | no | — | 0 |
| ↳↳ dfs(2,2) returns | | | 1+0+0+0+0 | **1** |
| ↳ dfs(1,1) | (1,1)=1 | yes → seen | 1 + children (all water/seen) | **1** |
| ↳ dfs(1,3) | (1,3)=1 | yes → seen | 1 + children (all water/seen) | **1** |
| ↳ dfs(0,2) [from dfs(1,2)] | seen | no | — | 0 |
| ↳ dfs(1,2) returns | | | 1 + 1(from2,2) + 1(from1,1) + 1(from1,3) + 0 | **4** |
| dfs(1,2)'s parent is dfs(0,2); dfs(0,2) other children: (−1,2) off, (0,3)=0, (0,1)=0 | | | 1 + 4 | **5** |

`dfs(0,2)` returns **5**. `best = max(0, 5) = 5`.

The loop continues: `(3,0)` land+unseen → `dfs` returns `1`, `best` stays `5`.
`(3,4)` → returns `1`, `best` stays `5`. Every other land cell is already in
`seen`.

Answer: **5**. ✅

---

## 8. Python Code (primary — DFS)

```python
from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def dfs(r: int, c: int) -> int:
            if not (0 <= r < m and 0 <= c < n):        # off the board
                return 0
            if grid[r][c] == 0 or (r, c) in seen:      # water, or already counted
                return 0
            seen.add((r, c))
            area = 1                                   # count myself
            for dr, dc in DIRS:
                area += dfs(r + dr, c + dc)            # plus everything reachable
            return area

        best = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1 and (r, c) not in seen:
                    best = max(best, dfs(r, c))
        return best


if __name__ == "__main__":
    sol = Solution()

    g = [[0, 0, 1, 0, 0],
         [0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0],
         [1, 0, 0, 0, 1]]
    assert sol.maxAreaOfIsland([row[:] for row in g]) == 5

    assert sol.maxAreaOfIsland([[0, 0, 0], [0, 0, 0]]) == 0      # no island
    assert sol.maxAreaOfIsland([[1, 1], [1, 1]]) == 4            # all land
    assert sol.maxAreaOfIsland([[1]]) == 1
    assert sol.maxAreaOfIsland([[0]]) == 0
    assert sol.maxAreaOfIsland([[1, 0, 1, 0, 1]]) == 1           # single row, 3 islands of 1
    assert sol.maxAreaOfIsland(
        [[1, 1, 0, 0, 0],
         [1, 1, 0, 0, 0],
         [0, 0, 0, 1, 1],
         [0, 0, 0, 1, 1]]) == 4                                  # two equal islands

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. BFS (count cells as you pop) — use when a huge solid island could overflow recursion

```python
from collections import deque
from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def bfs(sr: int, sc: int) -> int:
            q = deque([(sr, sc)])
            seen.add((sr, sc))
            area = 0
            while q:
                r, c = q.popleft()
                area += 1                              # count on pop
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n
                            and grid[nr][nc] == 1 and (nr, nc) not in seen):
                        seen.add((nr, nc))            # mark on enqueue
                        q.append((nr, nc))
            return area

        best = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1 and (r, c) not in seen:
                    best = max(best, bfs(r, c))
        return best
```

### 9b. Iterative DFS with a `nonlocal` accumulator (a style you'll see on YouTube — we don't prefer it)

```python
def dfs(r, c):
    nonlocal area
    ...
    area += 1
    for dr, dc in DIRS:
        dfs(r + dr, c + dc)
```

Works, but you must remember `nonlocal`, and you must reset `area = 0` before each
island. Returning the value (our way) composes more cleanly and has no reset.

### The BFS↔DFS answer the interviewer wants

> "Both `O(m*n)` time and space. DFS is the natural fit — the recurrence `area = 1
> + sum(children)` falls straight out of the return value. BFS counts on pop
> instead. I use DFS and would switch to BFS if the grid were large enough for a
> ~10^6-deep recursion."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = m*n`; edge = 4-neighbor adjacency, `E ≈ 2mn =
O(m*n)`.

**Time:**
- Outer double loop: `m*n` iterations → `O(m*n)`.
- All `dfs` calls together: each land cell is added to `seen` once and does `O(1)`
  work + 4 child calls; a cell that's water/seen/off returns in `O(1)`. Total calls
  `≤ 5*m*n` → `O(m*n)`.
- `max(best, ...)` in the loop is `O(1)` per island.
- **Total: `O(m * n)`.**

**Space:**
- `seen`: up to `m*n` tuples → `O(m*n)`.
- Recursion stack (DFS) / queue (BFS): worst case one snake island fills the grid →
  `O(m*n)`.
- **Total: `O(m * n)`.**
- In-place variant (set visited land to `0`) removes `seen` but keeps the `O(m*n)`
  recursion worst case.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `grid == []` / `[[]]` | `if not grid or not grid[0]: return 0` |
| No land at all | outer loop never calls `dfs` → `best` stays `0` |
| All land | first `dfs` returns `m*n` |
| Single cell | `[[1]]` → `1`, `[[0]]` → `0` |
| Several islands tied for max | `max` keeps the value, any one is fine |
| Single row / column | bounds check covers the missing dimension |
| Cells are ints `1`/`0` | compare with `== 1` / `== 0`, **not** `"1"` / `"0"` |
| Diagonal-only touch | `DIRS` has no diagonals → separate islands |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **`dfs` returns `None`.** Forgot `return 0` in a base case, or `return area`
      at the end. Symptom: `TypeError: unsupported operand type(s) for +=: 'int'
      and 'NoneType'`.
- [ ] **`area = dfs(...)` instead of `area += dfs(...)`.** Only the last branch
      counts → answer far too small.
- [ ] **String vs int:** `grid[r][c] == "1"` when cells are `1`. Always returns
      `0`.
- [ ] **`best = dfs(r, c)` instead of `best = max(best, dfs(r, c))`.** Returns the
      *last* island's area, not the biggest.
- [ ] **Resetting `seen` inside the loop** → same island recounted from several
      cells, areas overlap, wrong max.
- [ ] **Bounds check after indexing** → `IndexError` or negative-index wrap.
- [ ] **`nonlocal` variant: forgot to reset the accumulator** before each island.

**Narrate:** "My max is 1 but the picture clearly has a size-5 island. My `dfs`
must be returning early — oh, I wrote `area = dfs(...)` in the loop instead of
`area += dfs(...)`, so I only keep the last of the four recursive results."

---

## 13. Learnings & Transfer

**The reusable core: a DFS that returns an aggregate over a component.**

- Recurrence: `f(cell) = base_value + combine(f(child) for each child)`.
  - Area: `1 + sum(children)`.
  - Perimeter: `edges_to_water_or_border + sum(children)`.
  - "Is this island fully inside the grid?": `not_on_border AND all(children)`.
  - Sum of cell values: `grid[r][c] + sum(children)`.
- **Return the value; let the caller aggregate** (`max`, `+`, `and`). Cleaner than
  `nonlocal`, and no per-component reset.
- This exact shape is also how you solve **binary-tree** problems: max depth
  (`1 + max(left, right)`), diameter, path sum, count nodes. A grid island is just
  a tree/DAG of cells.

| Problem | How this transfers |
|---|---|
| Number of Islands | drop the return value, `count += 1` per island |
| Making a Large Island | `dfs` returns size **and** writes an `id` into each cell; store `size[id]` |
| Number of Closed Islands (LC 1254) | `dfs` returns bool "never touched the border" (`and` of children) |
| Count Sub-Islands (LC 1905) | `dfs` over grid2, returns bool "every cell is also land in grid1" |
| Number of Enclaves (LC 1020) | total land − land reachable from the border |
| Max depth / diameter / path sum of a binary tree | same "return an aggregate from recursion" |
| Sum of subtree values / count of subtrees with property X | same shape on an explicit tree |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Instead of the max area, return the max **perimeter** among all islands (perimeter = number of unit edges touching water or the grid border)."

- **(b) Pattern:** identical flood, different per-cell quantity to aggregate.
- **(c) Adapt:** in `dfs`, before recursing, compute this cell's edge count:
  `local = sum(1 for dr, dc in DIRS if the neighbor is off-board or water)`. Return
  `local + sum(dfs(child) for land children)`. Track the max as before. Still
  `O(m*n)`.
- **(d) Say:** "Area, perimeter, value-sum, 'is-closed' — all the same flood; only
  the base value and the combine operator change."

### Scenario 2 — "Return the number of **distinct island shapes**. Two islands with the same shape (same set of relative cell offsets) count once. Follow-up: also treat rotations and reflections as the same."

- **(b) Pattern:** flood to enumerate a component, then **canonicalize it into a
  hashable signature** and dedupe in a set. (LeetCode 694 / 711.)
- **(c) Adapt:** during `dfs`, record each visited cell's offset from the island's
  first cell: `(r - sr, c - sc)`. Sort the list, make it a tuple → that's the
  shape key; add to a `set`. Answer = `len(set)`. For rotations/reflections:
  generate all 8 transformed coordinate sets, normalize each (shift so min is
  `(0,0)`, sort), take the lexicographically smallest as the canonical key.
- **(d) Say:** "Comparing components ⇒ turn each into a canonical, translation-
  invariant signature and hash it."

### Scenario 3 — "The grid streams in one row at a time and doesn't fit in memory. Report the max island area using `O(n)` extra space."

- **(b) Pattern:** **scanline connected components** with a Union-Find keyed by
  column, carrying a size counter per root.
- **(c) Adapt:** keep only the previous row's component labels. For each new row:
  create labels for its land cells, `union` horizontally-adjacent ones and each one
  with the label directly above; maintain `size[root]`. When a component has no
  cell in the freshly read row, it's *finalized* — update the global max with its
  size and free it. State is two rows + a DSU over live labels → `O(n)`.
- **(d) Say:** "Huge/streamed grid ⇒ scanline: `O(row)` state, Union-Find keyed by
  column, per-root aggregates, finalize components as they fall out of the window."

### Scenario 4 — "Answer many queries of the form: 'what is the area of the island containing cell `(r, c)`?' (or 0 if it's water). Queries vastly outnumber a single grid."

- **(b) Pattern:** **preprocess** components once, then `O(1)` per query.
- **(c) Adapt:** one pass of flood fill: give each island an integer `id`, fill an
  `island_id[r][c]` grid, and record `size[id]`. A query is
  `size[island_id[r][c]]` if land else `0`. Preprocess `O(m*n)`, each query `O(1)`,
  extra space `O(m*n)`.
- **(d) Say:** "Repeated membership/aggregate queries on static components ⇒
  label every cell with its component id and store per-component aggregates."

### Scenario 5 — "You may change **one** water cell to land. Return the largest island area you can then achieve."

- **(b) Pattern:** this is **Making a Large Island** (next-but-one problem).
- **(c) Adapt:** Pass 1 — flood each island, assign `id` (start at 2), record
  `size[id]`. Pass 2 — for every water cell, gather the **distinct** ids among its
  4 neighbors, candidate `= 1 + sum(size[id] for those ids)`; track the max. Edge
  case: no water cell at all → answer is `m*n`.
- **(d) Say:** "‘Change one cell’ ⇒ precompute component labels + sizes, then score
  every candidate change in `O(1)` from those labels."

### Scenario 6 — "You may remove **up to K** land cells. Minimize the area of the largest remaining island."

- **(b) Pattern:** trap question — flag that it's combinatorial. For `K = 1` it's
  tractable (this is essentially bridges/articulation on the island graph — a
  removal that splits a big island). For general `K` it's NP-hard-flavored.
- **(c) Adapt:** For `K = 1`: for each island, find its **articulation points**
  (Tarjan, Group 15); removing one splits the island into pieces — the best split
  minimizes the max piece. Compare across islands, also consider that removing a
  non-cut cell just shrinks the island by 1. For general `K`: say so, then offer a
  heuristic (repeatedly remove the articulation point that most reduces the max
  component) or a bounded search if `K` and island sizes are tiny.
- **(d) Say:** "When ‘up to K changes’ makes it exponential, name that, solve the
  `K = 1` case exactly with articulation points, and give a principled heuristic
  for larger `K`."

---

## 15. Flashcards

**Q:** What does Max Area of Island add on top of Number of Islands?
**A:** The flood **returns an int** — `area = 1 + sum(dfs(child))` — and the outer
loop keeps `best = max(best, area)`.

**Q:** Symptom of a return-value bug here?
**A:** `TypeError: int + NoneType` — a base case missing `return 0`, or the
function missing `return area`.

**Q:** Cell type in LeetCode 695?
**A:** Integers `1` / `0`. (Number of Islands used the *strings* `"1"` / `"0"` —
always check.)

**Q:** Why return the area instead of using a `nonlocal` accumulator?
**A:** No `nonlocal` keyword to forget, no per-island reset, and the recurrence
`1 + sum(children)` composes directly.

**Q:** Time and space, with derivation?
**A:** `O(m*n)` both. Outer loop `m*n`; `seen` check keeps total flood `O(m*n)`;
recursion/queue `O(m*n)` worst case.

**Q:** Perimeter-instead-of-area variant — the one change?
**A:** Per cell, base value = number of its 4 sides facing water or the border;
still `base + sum(children)`.

**Q:** "Number of distinct island shapes" — technique?
**A:** During the flood record each cell's offset from the island's first cell;
sort → tuple → add to a set. `len(set)` is the answer. Rotations/reflections:
canonicalize over all 8 transforms.

**Q:** Many "area of the island containing (r,c)?" queries — approach?
**A:** Preprocess once: label every cell with an island `id`, store `size[id]`.
Each query is `O(1)`.

**Q:** General shape this problem teaches for trees too?
**A:** "Return an aggregate from recursion": `f(node) = base + combine(f(child)…)`
— powers max-depth, diameter, path-sum, subtree-size.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Recursive DFS returning an area, `O(m*n)` time and
space — matches the primary solution.

```python
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        max_area = 0
        rows = len(grid)
        columns = len(grid[0])

        visited = set()

        def dfs(r, c):
            if (r < 0 or r >= rows or c < 0 or c >= columns
                    or grid[r][c] == 0 or (r, c) in visited):
                return 0

            visited.add((r, c))
            area = 1

            area += dfs(r, c + 1)
            area += dfs(r, c - 1)
            area += dfs(r + 1, c)
            area += dfs(r - 1, c)

            return area

        for i in range(rows):
            for j in range(columns):
                if grid[i][j] == 1:
                    area = dfs(i, j)
                    if area > max_area:
                        max_area = area
        return max_area
```

**Correct.** The key pieces are all right: base case returns `0` on every dead end,
`area += dfs(...)` (not `=`, the bug that would silently undercount), and
`if area > max_area: max_area = area` instead of overwriting unconditionally.

**One style note (not a bug):** the outer loop calls `dfs(i, j)` for *every* land
cell, including ones already in `visited` from an earlier island's flood — that
call just hits the base case and returns `0` immediately, so it's harmless and
doesn't change the `O(m*n)` bound, but it is a wasted function call. Adding
`and (i, j) not in visited` to the `if` (as the primary solution does) skips it —
worth doing purely for clarity: "only start a flood from an unseen cell" becomes
visible at the call site instead of implicit in the base case.
