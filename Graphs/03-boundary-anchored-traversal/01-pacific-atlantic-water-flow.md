# Pacific Atlantic Water Flow  ·  LeetCode 417  ·  Medium

Group 03 — Boundary-Anchored Traversal  ·  the problem that defines this pattern:
flood **from the border inward**, using the **reversed** flow relationship,
instead of simulating "forward" from every single cell.

Prereqs: `concepts/03` (BFS), `01-walls-and-gates.md` (multi-source BFS). New
idea: **the sources are an entire border**, and **you must reverse the
direction** of the real-world relationship to make a single flood answer the
question for every cell at once.

---

## 1. Problem

You are given an `m x n` grid `heights` where `heights[r][c]` is the height of
that cell above sea level. The **Pacific Ocean** touches the grid's **top row and
left column**. The **Atlantic Ocean** touches the **bottom row and right column**.

Water can flow from a cell to any of its 4-directional neighbors if the
neighbor's height is **less than or equal to** the current cell's height (water
flows downhill, or across flat ground — never uphill).

**Return the coordinates of every cell from which water can reach *both* the
Pacific and the Atlantic.**

Constraints:
- `1 <= m, n <= 200`.
- `0 <= heights[r][c] <= 10^5`.

Example:

```
heights = [[1,2,2,3,5],
           [3,2,3,4,4],
           [2,4,5,3,1],
           [6,7,1,4,5],
           [5,1,1,2,4]]

answer = [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]   (any order)
```

---

## 2. Explain Like I'm 5

Picture a big hill-covered island. Rain falls on a square, and it always rolls
downhill (or stays put on flat ground) to a neighboring square, never uphill. The
Pacific touches the top and left edges of the map; the Atlantic touches the
bottom and right edges.

You want to know: **from which squares could a raindrop eventually reach *both*
oceans** (not necessarily the same drop — just: is there *some* downhill path from
this square to the Pacific, and *separately*, is there *some* downhill path from
this square to the Atlantic)?

Checking one square at a time (drop a raindrop, watch where it *could* roll, does
it reach an edge?) means doing that whole "watch it roll" search **once per
square** — way too slow for a big map.

Here's the trick: **stand at the ocean and imagine the water climbing backward,
uphill, into the map.** A square can send water to the Pacific if and only if the
Pacific's "backward-climbing" flood can reach that square (walking only to
neighbors that are the **same height or taller** — the reverse of "downhill").
Flood **once** from every Pacific-touching square simultaneously, and you instantly
know *every* square that can reach the Pacific. Do the same starting from every
Atlantic-touching square. A square that shows up in **both** floods is your
answer.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Can this cell reach the edge?" asked for **every** cell | ✅ |
| A directional relationship between neighbors (downhill only) | ✅ |
| Naive per-cell simulation would be `O((m*n)²)` | ✅ (`m,n` up to 200 → up to 40,000 cells; squared is 1.6 billion — too slow) |
| Multiple named boundaries (two oceans) whose results get **combined** | ✅ → intersection |

**Reduce it to:** *"Multi-source BFS from every Pacific-border cell using the
reversed flow relation; repeat from every Atlantic-border cell; intersect the two
reachable sets."*

**Look-alikes:**
- Walls and Gates / 01 Matrix — multi-source BFS from special *values* (gates,
  zeros). Here the sources are an entire **edge of the grid**, and the traversal
  condition is **reversed** relative to the problem's stated rule — neither of
  those appear in Group 02.
- Surrounded Regions (next problem) — boundary-anchored too, but only **one**
  border and no reversal is needed (its rule has no directionality — connectivity
  is symmetric there).

---

## 4. Intuition

1. **Why not simulate forward from every cell?** For each cell, "can it reach the
   Pacific" requires exploring every downhill path from it — worst case that's
   `O(m*n)` work, and you'd do it for `O(m*n)` cells → `O((m*n)²)`. At `m=n=200`
   that's on the order of `1.6 × 10^9` — too slow.
2. **Key realization:** "cell `X` can flow to the Pacific" is the same fact as
   "the Pacific's backward flood can reach cell `X`" — reachability is symmetric
   in *which end you search from*, as long as you flip the direction of the edges
   you follow.
3. The real rule is: water flows from `A` to `B` if `height[B] <= height[A]`
   (downhill). If we want to walk **backward** — from the ocean inward — we ask
   "which neighbor `B` *could have* sent water to where I am, `A`?" That's exactly
   the cells `B` with `height[B] >= height[A]` (since forward would need
   `height[A] <= height[B]`). **Reverse the inequality.**
4. So: seed a multi-source BFS with **every** Pacific-touching cell (top row +
   left column) at once, and expand to a neighbor only if the neighbor's height is
   `>=` the current cell's height. Every cell this flood reaches can flow to the
   Pacific (forward), by construction.
5. Do the same, independently, from every Atlantic-touching cell (bottom row +
   right column).
6. A cell that appears in **both** reachable sets is a cell that can flow to
   *both* oceans — the answer is the **intersection**.

---

## 5. Approach (primary): two multi-source BFS floods (reversed condition) + intersect

1. `m, n = len(heights), len(heights[0])`.
2. `pacific_sources` = every `(0, c)` and every `(r, 0)`. `atlantic_sources` =
   every `(m-1, c)` and every `(r, n-1)`.
3. Write `bfs(sources)`: multi-source BFS seeded with `sources` (all marked seen
   at the start); expand to neighbor `(nr, nc)` only if
   `heights[nr][nc] >= heights[r][c]` (the **reversed** flow condition) and not
   yet seen. Return the final `seen` set.
4. `pacific = bfs(pacific_sources)`; `atlantic = bfs(atlantic_sources)`.
5. Return every `[r, c]` in `pacific & atlantic` (set intersection).

Builds on: `concepts/03` BFS, `01-walls-and-gates.md` multi-source seeding — this
time seeding an entire edge of the grid instead of scattered special cells, and
reversing the traversal condition.

---

## 6. Pseudocode

```
function pacificAtlantic(heights):
    m, n = rows, cols

    function bfs(sources):
        seen = set(sources)
        q = queue(sources)
        while q not empty:
            (r, c) = dequeue
            for each of 4 neighbors (nr, nc):
                if in bounds and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]:     # REVERSED condition
                    add (nr, nc) to seen
                    enqueue (nr, nc)
        return seen

    pacific_sources  = all (0, c) and all (r, 0)
    atlantic_sources = all (m-1, c) and all (r, n-1)

    pacific  = bfs(pacific_sources)
    atlantic = bfs(atlantic_sources)

    return list of [r, c] for (r, c) in pacific ∩ atlantic
```

---

## 7. Dry Run

```
heights = [[1,2],
           [4,3]]
```

`m=n=2`. `pacific_sources = {(0,0),(0,1),(1,0)}` (top row + left column).
`atlantic_sources = {(1,0),(1,1),(0,1)}` (bottom row + right column).

**Pacific flood** — `seen` starts as all 3 sources. Queue processes them:
- `(0,0)=1`: neighbors `(1,0)=4` already seen (skip re-add), `(0,1)=2` already
  seen. Nothing new.
- `(0,1)=2`: neighbors `(1,1)=3`: `3 >= 2` ✓ and not seen → add `(1,1)`.
  `(0,0)` seen.
- `(1,0)=4`: neighbors `(1,1)=3` — already just added, skip.
- `(1,1)=3`: neighbors already seen.

`pacific = {(0,0),(0,1),(1,0),(1,1)}` — every cell (makes sense: in a `2x2` grid,
every cell is directly on some part of both borders anyway, but here even the
"far" corner `(1,1)` got pulled in through the flood).

**Atlantic flood** — sources `{(1,0),(1,1),(0,1)}`, `seen` starts with those 3.
- `(1,0)=4`: neighbor `(0,0)=1`: `1 >= 4`? **No** → not added.
- `(1,1)=3`: neighbor `(0,1)` seen.
- `(0,1)=2`: neighbor `(0,0)=1`: `1 >= 2`? **No** → not added.

`atlantic = {(1,0),(1,1),(0,1)}` — `(0,0)` never joins; its height (`1`) is too
low to have "received" water from any neighbor when walking backward from the
Atlantic.

**Intersection:** `pacific ∩ atlantic = {(0,1),(1,0),(1,1)}`.

Sanity-check `(0,0)`: real forward flow from `(0,0)=1` can't go anywhere (both
neighbors are taller) — it's already *on* the Pacific border so it trivially
reaches Pacific, but it has **no downhill path to the Atlantic border** at all
(everything around it is uphill). Correctly excluded. ✅

---

## 8. Python Code (primary — two multi-source BFS floods)

```python
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []

        m, n = len(heights), len(heights[0])

        def bfs(sources):
            seen = set(sources)
            q = deque(sources)
            while q:
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                            and heights[nr][nc] >= heights[r][c]):   # reversed flow
                        seen.add((nr, nc))
                        q.append((nr, nc))
            return seen

        pacific_sources = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
        atlantic_sources = [(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)]

        pacific = bfs(pacific_sources)
        atlantic = bfs(atlantic_sources)

        return [[r, c] for r, c in pacific & atlantic]


if __name__ == "__main__":
    sol = Solution()

    heights = [[1, 2, 2, 3, 5],
               [3, 2, 3, 4, 4],
               [2, 4, 5, 3, 1],
               [6, 7, 1, 4, 5],
               [5, 1, 1, 2, 4]]
    result = sol.pacificAtlantic(heights)
    expected = [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    assert sorted(result) == sorted(expected)

    assert sol.pacificAtlantic([[1]]) == [[0, 0]]

    # small 2x2, every cell qualifies (every cell touches both borders directly)
    assert sorted(sol.pacificAtlantic([[2, 1], [1, 2]])) == \
        sorted([[0, 0], [0, 1], [1, 0], [1, 1]])

    # single row -> row0 IS both the top row and the bottom row -> everything qualifies
    assert sorted(sol.pacificAtlantic([[3, 1, 6, 4]])) == \
        sorted([[0, 0], [0, 1], [0, 2], [0, 3]])

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. The naive per-cell simulation (shown to explain *why not*)

```python
def pacificAtlantic_naive(heights):
    m, n = len(heights), len(heights[0])
    result = []

    def can_reach(r, c, is_target):
        # forward DFS from (r, c): can it reach a cell where is_target(r, c) is True?
        seen = set()

        def dfs(r, c):
            if (r, c) in seen:
                return False
            seen.add((r, c))
            if is_target(r, c):
                return True
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < m and 0 <= nc < n
                        and heights[nr][nc] <= heights[r][c] and dfs(nr, nc)):
                    return True
            return False

        return dfs(r, c)

    is_pacific = lambda r, c: r == 0 or c == 0
    is_atlantic = lambda r, c: r == m - 1 or c == n - 1

    for r in range(m):
        for c in range(n):
            if can_reach(r, c, is_pacific) and can_reach(r, c, is_atlantic):
                result.append([r, c])
    return result
```

This is **correct**, but runs a fresh DFS (up to `O(m*n)`) from **every** cell,
twice → `O((m*n)²)` worst case. At the constraint's upper bound (`200×200 =
40,000` cells), that's roughly `1.6 × 10^9` operations — this is precisely why
boundary-anchored flooding exists.

### 9b. Recursive DFS instead of BFS for the boundary flood

```python
import sys
sys.setrecursionlimit(20000)     # up to 200*200 = 40,000 cells

def dfs_flood(sources, heights, m, n):
    seen = set()

    def dfs(r, c):
        seen.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                    and heights[nr][nc] >= heights[r][c]):
                dfs(nr, nc)

    for r, c in sources:
        if (r, c) not in seen:
            dfs(r, c)
    return seen
```

Same `O(m*n)` complexity. Given the grid can be `200×200 = 40,000` cells (a
possible long snake-shaped equal-height plateau), recursion risks exceeding
Python's default limit without raising it — the same trade-off seen in Shortest
Bridge. BFS (primary) sidesteps this entirely, which is why it's the safer
default here.

### The BFS↔DFS answer the interviewer wants

> "Either works for the boundary flood — it's pure reachability, no shortest-path
> requirement. I'd use BFS by default to avoid any recursion-depth risk on a
> `200×200` grid, and mention recursive DFS with a raised limit as the
> alternative. The real complexity win isn't BFS-vs-DFS — it's **flooding from the
> boundary instead of simulating from every cell**, which turns `O((m*n)²)` into
> `O(m*n)`."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = m*n`; edge = 4-neighbor adjacency,
`E ≈ 2mn = O(m*n)`.

**Time:**
- Building the two source lists: `O(m + n)`.
- Each `bfs()` call: standard multi-source BFS, every cell enqueued at most once,
  every edge examined a constant number of times → `O(m*n)`.
- Two calls → `O(m*n)` (the constant factor `2` doesn't change the complexity
  class).
- Intersecting two sets of size up to `m*n`: `O(m*n)`.
- **Total: `O(m * n)`** — versus the naive approach's `O((m*n)²)`.

**Space:**
- Two `seen` sets, each up to `O(m*n)`.
- Two queues, each up to `O(m*n)`.
- Result list up to `O(m*n)`.
- **Total: `O(m * n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `1x1` grid | that cell is on every border simultaneously → both floods start already containing it → answer `[[0,0]]` |
| Single row or single column | row `0` **is** row `m-1` (or col `0` **is** col `n-1`) → every cell is a source for *both* oceans directly → entire grid qualifies |
| All cells the same height | the reversed condition `>=` holds for every neighbor pair → both floods spread through the entire grid → likely (depending on shape) most/all cells qualify |
| A "bowl" shape (high rim, low center) | rim cells may reach both oceans easily; deep interior cells might only reach one or neither, depending on the downhill path out |
| No cell reaches both oceans | returns `[]` — perfectly valid |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Forgetting to reverse the inequality.** Using
      `heights[nr][nc] <= heights[r][c]` (the *forward*, "real" flow condition)
      instead of `>=` while flooding *from* the border. This is the single most
      important conceptual step in the whole problem — get it backward and the
      floods compute something close to nonsense (roughly "who could the border
      flow into," the opposite of what's needed).
- [ ] **Using strict `>` instead of `>=`.** The problem allows flow across *equal*
      heights (flat ground) — dropping the "or equal" breaks plateaus, silently
      shrinking both reachable sets.
- [ ] **Missing corner cells or double-counting them.** `(0,0)` is Pacific-only,
      `(m-1,n-1)` is Atlantic-only, but `(0,n-1)` and `(m-1,0)` belong to *both*
      oceans' source lists — using a `set` (which the primary solution does)
      makes duplicates harmless; a bug appears if you use a `list` and then treat
      membership with `==` checks expecting no duplicates elsewhere.
- [ ] **Forgetting the intersection step** — returning one flood's result alone
      (e.g. just `pacific`) instead of `pacific & atlantic`.
- [ ] **Running the `O((m*n)²)` naive approach** on the full constraint size —
      correct but too slow; recognize the boundary-flood trick is required, not
      optional, once `m, n` approach `200`.

**Narrate:** "My answer includes way too many cells, almost the whole grid. Let
me check my flood's neighbor condition... I have `<=` — that's the *forward* flow
rule. Since I'm walking backward from the ocean, I need the reverse: `>=`."

---

## 13. Learnings & Transfer

**The reusable core: flood from the boundary, reverse the relation, avoid
per-cell simulation.**

1. Whenever a question is "can every cell reach some target set?" and the target
   set is *fixed* (a border, a set of special cells), don't search forward from
   every cell — **flood backward from the target set once**, using the reversed
   edge relation if the relationship is directional.
2. **Reversing a directional relation**: if the rule is "A can act on B when
   `condition(A, B)`", walking backward from B asks "which A satisfies
   `condition(A, B)`", which — when the condition is a simple comparison like
   `height[B] <= height[A]` — just means solving for `A` instead of `B`, i.e.
   flipping the inequality.
3. **Multiple named boundaries → run the flood once per boundary, then combine**
   with the set operation the question actually asks for (intersection here;
   union or difference would look identical in code, just swap `&` for `|` or
   `-`).

| Situation | How this transfers |
|---|---|
| Surrounded Regions (next) | one boundary (any border-touching `O`), no reversal needed (symmetric relation) — flip the *rest* of the grid instead of intersecting two sets |
| "Which servers can reach both Region A and Region B's gateway" (networking) | same shape on a general directed graph: flood backward from each gateway set through reversed edges, intersect |
| Any "reachable from a fixed target set, for every node" question | boundary/target-anchored flood, not per-node search |
| Symmetric relations (e.g. "within threshold `T`") | no reversal needed at all — forward and backward floods use the *same* condition (see Scenario 5) |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Add a third 'ocean' — an inland lake occupying a specific, given set of cells. Find cells that can reach all three."

- **(b) Pattern:** the technique generalizes immediately to **any number** of
  fixed target sets, not just two grid edges.
- **(c) Adapt:** run the same `bfs()` a third time, seeded with the lake's cells
  (still using the reversed condition — the lake is just another "destination").
  Intersect all three resulting sets (`pacific & atlantic & lake`). Still
  `O(k * m*n)` for `k` target sets — linear in `k`.
- **(d) Say:** "Nothing about this technique is specific to 'exactly two, and
  they're grid edges' — any fixed set of destinations gets its own flood, and the
  final combine step (intersection here) is just a set operation over as many
  floods as you have destinations."

### Scenario 2 — "Water can also flow diagonally, not just up/down/left/right."

- **(b) Pattern:** same algorithm, wider neighbor set.
- **(c) Adapt:** use `DIRS8` instead of `DIRS` in both floods. Complexity stays
  `O(m*n)` (constant factor of 8 instead of 4 neighbors per cell).
- **(d) Say:** "Changing the adjacency definition is a one-line swap of the
  offsets iterated — doesn't change the algorithm's shape."

### Scenario 3 — "For every cell that reaches both oceans, also report one valid downhill path to each."

- **(b) Pattern:** BFS + **parent pointers**, same idea as 01 Matrix Scenario 4.
- **(c) Adapt:** during each flood, record `parent[nr][nc] = (r, c)` when first
  visiting `(nr, nc)`. Because we walked *backward* from the ocean, following
  `parent` from a qualifying cell back to its source cell gives the path **in
  reverse** — read it backward (or reverse the collected list) to present it as
  "downhill from the cell to the ocean." `O(m*n)` extra space, no time-complexity
  change.
- **(d) Say:** "The backward flood naturally hands you a path to the boundary for
  free via parent pointers — you just have to remember the path comes out
  reversed relative to the real, forward flow direction."

### Scenario 4 — "The grid is enormous (say `10^4 x 10^4`) and memory is tight. Reduce memory use."

- **(b) Pattern:** the same algorithm, with a **more compact visited
  representation**.
- **(c) Adapt:** replace the Python `set` of `(r, c)` tuples (heavy — each tuple
  and set entry carries real object overhead) with a **flat bitset**: a single
  `bytearray` or integer of `m*n` bits, indexed by `r*n + c`. Checking/setting a
  bit is `O(1)`, and memory drops from tens of bytes per cell (Python `set`
  overhead) to `1` bit per cell. Complexity class is unchanged (`O(m*n)` time and
  space), but the constant factor shrinks drastically.
- **(d) Say:** "When the algorithm is already optimal but memory constants matter
  at scale, swap the visited *data structure* (set of tuples → bitset), not the
  algorithm."

### Scenario 5 — "Change the flow rule: water can move to a neighbor if the **absolute height difference** is within a threshold `T` (uphill or downhill, as long as it's not too steep)."

- **(b) Pattern:** a conceptual check — does the reversal trick still apply, and
  is it even still *necessary*?
- **(c) Adapt:** the new relation `|height[A] - height[B]| <= T` is **symmetric**
  — if `A` can move to `B`, then `B` can just as validly move to `A` (the
  absolute difference doesn't care about direction). So the "reversed" condition
  is **identical** to the forward one — you don't need to flip anything, just
  flood from the border using `abs(heights[nr][nc] - heights[r][c]) <= T`
  directly. This still needs to start from the boundary (not per-cell) for the
  same `O(m*n)` vs `O((m*n)²)` reason, but the *reversal* step specifically
  becomes moot.
- **(d) Say:** "Reversal is only needed because the original relation
  (strictly downhill) is asymmetric. The moment a relation is symmetric, forward
  and backward search are the same search — recognizing that distinction is the
  real test of whether you understood *why* we reversed the condition, not just
  memorized that we did."

### Scenario 6 — "This is really a network-security question: 'ocean' = a trust boundary (a fixed set of gateway hosts), 'downhill' = 'this host's access level lets it escalate into that host'. Find every host that can escalate into **both** of two separate trust boundaries."

- **(b) Pattern:** the exact same algorithm, mapped from a grid onto a general
  directed graph.
- **(c) Adapt:** build a reversed adjacency list (edges pointing the opposite way
  from "can escalate into"). Multi-source BFS from each trust boundary's gateway
  set over the reversed graph; intersect the two reachable sets. `O(V+E)` per
  boundary instead of `O(m*n)` (grid-specific), same shape otherwise.
- **(d) Say:** "This pattern was never really about grids — 'reachable from a
  fixed set, for every node, over a directional relation' is a general-graph
  technique that happens to appear on a grid here."

---

## 15. Flashcards

**Q:** The core trick this problem introduces?
**A:** Flood **from the boundary inward** using the **reversed** relationship,
instead of simulating forward from every individual cell — turns `O((m*n)²)`
into `O(m*n)`.

**Q:** Why must the flow condition be reversed for the boundary flood?
**A:** The real rule is "flow to a neighbor with `height <= mine`" (downhill).
Walking backward from the ocean, you need "which neighbor *could have* sent water
here" — that's `height[neighbor] >= height[mine]`: the inequality flips.

**Q:** Why `>=` and not strict `>` (or `<=` not `<` forward)?
**A:** The problem allows flow across equal heights (flat ground) — dropping "or
equal" breaks plateau connectivity.

**Q:** How is the final answer computed from the two floods?
**A:** Set intersection: `pacific & atlantic` — cells reachable from *both*
boundary floods.

**Q:** Time and space, with derivation, vs the naive approach?
**A:** `O(m*n)` time and space (two multi-source BFS floods + an intersection).
Naive per-cell simulation is `O((m*n)²)` — a full search from every cell.

**Q:** Single-row or single-column grid — what's special?
**A:** Row 0 *is* row `m-1` (or col 0 *is* col `n-1`), so every cell is
simultaneously a source for both oceans — the entire grid trivially qualifies.

**Q:** When does the "reverse the condition" step become unnecessary?
**A:** When the relation is symmetric (e.g. `abs(height difference) <= T`) —
forward and backward search use the identical condition.

**Q:** How does this generalize beyond "exactly two ocean borders"?
**A:** Flood once per fixed target set (any number, any shape — not just grid
edges), then combine with whatever set operation the question needs
(intersection, union, difference).

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Recursive DFS, with the reversed condition
implemented as an explicit `prevHeight` parameter instead of a pre-check before
each recursive call. `O(m*n)` time and space — matches the primary solution.

```python
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:

        rows = len(heights)
        columns = len(heights[0])
        common = []

        pacific = set()
        atlantic = set()

        def dfs(r, c, visited, prevHeight):
            if r < 0 or r >= rows or c < 0 or c >= columns or (r, c) in visited or heights[r][c] < prevHeight:
                return

            visited.add((r, c))

            dfs(r + 1, c, visited, heights[r][c])
            dfs(r - 1, c, visited, heights[r][c])
            dfs(r, c + 1, visited, heights[r][c])
            dfs(r, c - 1, visited, heights[r][c])

        for c in range(columns):
            dfs(0, c, pacific, heights[0][c])
            dfs(rows - 1, c, atlantic, heights[rows - 1][c])

        for r in range(rows):
            dfs(r, 0, pacific, heights[r][0])
            dfs(r, columns - 1, atlantic, heights[r][columns - 1])

        for i in range(rows):
            for j in range(columns):
                if (i, j) in pacific and (i, j) in atlantic:
                    common.append([i, j])

        return common
```

**Correct** — I ran it against all four cases from section 8's tests (the full
official example, the `1x1` grid, the `2x2` grid, and the single-row grid) and
every one matches exactly.

**A nice stylistic difference worth noticing:** instead of checking the reversed
condition *before* each recursive call (the way the primary solution's `bfs`
does, and the way section 9b's recursive alternative does), you check it as the
**first lines inside `dfs` itself**, by threading the previous cell's height
through as an explicit `prevHeight` parameter. Functionally identical — a cell
either satisfies `heights[r][c] >= prevHeight` or it doesn't, checked at the same
logical moment either way — but passing `prevHeight` explicitly makes the
"conditioned on where I came from" idea very readable, arguably clearer for a
first read than reaching into `heights[r][c]` from inside a neighbor loop.

**One thing to watch on a bigger grid:** this uses plain recursion with no
`sys.setrecursionlimit` bump. It's fine at the tested sizes, but per the `.md`'s
section 9b note: at the constraint's upper bound (`200×200 = 40,000` cells), a
large flat plateau could recurse deep enough to risk Python's default
recursion limit (~1000). If you keep this recursive style for the real submission,
add `sys.setrecursionlimit(20000)` (or similar) at the top, or fall back to the
primary solution's iterative BFS version, which has no such risk.
