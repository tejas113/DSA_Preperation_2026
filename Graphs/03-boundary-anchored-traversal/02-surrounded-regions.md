# Surrounded Regions  ·  LeetCode 130  ·  Medium

Group 03 — Boundary-Anchored Traversal  ·  the simpler sibling of Pacific
Atlantic: **one** boundary instead of two, and — unlike that problem — **no
reversal needed**, because "is connected to" is symmetric. Instead of
intersecting two floods, you flip everything the single flood *didn't* reach.

Prereqs: `01-pacific-atlantic-water-flow.md` (read that first — this problem is
its simplified cousin). New idea: **answer by complement** — flood the "safe"
cells, then flip everything else.

---

## 1. Problem

You're given an `m x n` board of characters `'X'` and `'O'`. **Capture** every
region of `'O'`s that is **completely surrounded** by `'X'`s — meaning it has no
`'O'` connected (4-directionally) all the way out to the board's border. Capturing
means flipping every `'O'` in that region to `'X'`. Modify the board **in place**.

Any `'O'` region that touches the border (directly, or through a chain of
connected `'O'`s reaching the border) is **safe** and stays `'O'`.

Constraints:
- `1 <= m, n <= 200`.
- `board[r][c]` is `'X'` or `'O'`.

Example:

```
board = [["X","X","X","X"],
         ["X","O","O","X"],
         ["X","X","O","X"],
         ["X","O","X","X"]]

output = [["X","X","X","X"],
          ["X","X","X","X"],
          ["X","X","X","X"],
          ["X","O","X","X"]]
```

The `'O'` at `(3,1)` is *itself* on the border (last row) → safe, stays `'O'`.
The three `'O'`s at `(1,1),(1,2),(2,2)` form one connected region that never
touches any border cell → captured, flipped to `'X'`.

---

## 2. Explain Like I'm 5

Imagine a fenced field with patches of mud (`'O'`) among the grass (`'X'`). Some
mud patches connect all the way to the fence (the border) — maybe through a
winding trail of connected mud. Those are "outside mud," safe from being paved
over. Any mud patch that's **completely boxed in** — no path of mud reaches the
fence — gets paved over (`'X'`).

How do you find the boxed-in mud without checking every single patch one at a
time? **Stand at the fence.** Walk inward along every trail of mud you find
starting from the fence. Every patch you can reach this way is "safe" — mark it.
When you're done walking, **anything still mud that you never marked** was boxed
in the whole time — pave it. Anything you *did* mark, leave as mud.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Is this region connected to the border?" | ✅ |
| The alternative (per-region simulation) risks being slow or awkward: you'd have
  to flood every `'O'` region and check if ANY of its cells touch the border —
  actually still `O(m*n)` total if done carefully with a visited set... but doing
  it *from the border* is more direct and mirrors Pacific Atlantic | ✅ boundary-anchored |
| The final answer is a **flip of everything not reached**, not an intersection | ✅ — the key difference from Pacific Atlantic |
| "Connected to" — is the relationship directional? | **No** — plain `'O'`-to-`'O'` adjacency is symmetric |

**Reduce it to:** *"Flood every border-touching `'O'` inward (ordinary
connectivity, no reversal needed since the relation is symmetric); every `'O'`
the flood doesn't reach gets flipped."*

**Contrast with Pacific Atlantic (read this carefully):**
- Pacific Atlantic: **two** boundaries, a **directional** relation (downhill),
  which is *why* it needed to reverse the condition, and the answer is an
  **intersection** of two floods.
- Surrounded Regions: **one** boundary, a **symmetric** relation (just
  `'O'`-adjacency — no reversal needed at all, exactly like Scenario 5 of that
  file predicted), and the answer is the **complement** of one flood (flip
  everything *not* reached).

---

## 4. Intuition

1. An `'O'` region is safe **exactly when** it's reachable from the border by a
   path of `'O'`s. That's a pure reachability question — no direction, no height,
   just "is there an `'O'`-path to the edge."
2. So: flood-fill starting from **every** `'O'` cell that sits *on* the border,
   simultaneously (multi-source), moving only through `'O'` cells. Mark everything
   this flood touches as safe.
3. Anything left over that's still `'O'` after the flood was **never reachable**
   from any border cell — by definition, it's a fully surrounded region. Flip it
   to `'X'`.
4. Anything marked safe stays `'O'`.
5. Use the mutation-as-visited-mark trick (Group 01/02's recurring idea): while
   flooding, overwrite each visited `'O'` with a temporary placeholder (e.g.
   `'#'`) so it's simultaneously marked "safe" and "already visited." At the end,
   one pass turns every remaining `'O'` into `'X'` (captured) and every `'#'` back
   into `'O'` (safe).

---

## 5. Approach (primary): multi-source BFS from border `'O'`s + a cleanup pass

1. `m, n = len(board), len(board[0])`.
2. `q = deque()`. Scan the border (row `0`, row `m-1`, column `0`, column `n-1`):
   for every `'O'` found there, set `board[r][c] = '#'` and push `(r, c)`.
3. Standard multi-source BFS: pop `(r, c)`; for each neighbor that's still `'O'`,
   set it to `'#'` and push it.
4. Final pass over the whole board: `'O' → 'X'` (captured — never reached),
   `'#' → 'O'` (safe — restore).

Builds on: `01-walls-and-gates.md` (multi-source seeding), the mutation-as-
visited-mark trick from every earlier problem in Groups 01–02.

---

## 6. Pseudocode

```
function solve(board):
    m, n = rows, cols
    q = empty queue

    for each border cell (r, c):
        if board[r][c] == 'O':
            board[r][c] = '#'
            enqueue (r, c)

    while q not empty:
        (r, c) = dequeue
        for each of 4 neighbors (nr, nc):
            if in bounds and board[nr][nc] == 'O':
                board[nr][nc] = '#'
                enqueue (nr, nc)

    for each cell (r, c):
        if board[r][c] == 'O': board[r][c] = 'X'    # never reached -> captured
        elif board[r][c] == '#': board[r][c] = 'O'  # reached -> safe, restore
```

---

## 7. Dry Run

```
board = [["X","X","X","X"],
         ["X","O","O","X"],
         ["X","X","O","X"],
         ["X","O","X","X"]]
```

**Seed step** — scan the border (row 0, row 3, col 0, col 3): the only border
`'O'` is `(3,1)`. Mark it `'#'`, `q = [(3,1)]`.

**BFS:**

| pop | neighbor checks | updates | queue after |
|---|---|---|---|
| (3,1) | up(2,1)='X' skip; down off; right(3,2)='X' skip; left(3,0)='X' skip | none | [] |

Queue empties immediately — `(3,1)` has no `'O'` neighbors at all.

**Cleanup pass:** every remaining `'O'` — `(1,1),(1,2),(2,2)` — was never reached
→ flip to `'X'`. The one `'#'` at `(3,1)` → restore to `'O'`.

Result:

```
[["X","X","X","X"],
 ["X","X","X","X"],
 ["X","X","X","X"],
 ["X","O","X","X"]]
```

Matches the expected output. ✅ Notice `(1,1),(1,2),(2,2)` **are** connected to
each other (they'd flood together if any one of them touched the border), but
since none of them individually touches the border and they never reach `(3,1)`
(no `'O'` path between the two regions — `(2,1)` and `(3,2)`/`(3,0)` are `'X'`,
blocking it), the whole trio is captured.

---

## 8. Python Code (primary — multi-source BFS + cleanup)

```python
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """Do not return anything, modify board in-place instead."""
        if not board or not board[0]:
            return

        m, n = len(board), len(board[0])
        q = deque()

        for r in range(m):
            for c in range(n):
                if (r == 0 or r == m - 1 or c == 0 or c == n - 1) and board[r][c] == "O":
                    board[r][c] = "#"          # mark safe + visited
                    q.append((r, c))

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                    board[nr][nc] = "#"
                    q.append((nr, nc))

        for r in range(m):
            for c in range(n):
                if board[r][c] == "O":
                    board[r][c] = "X"          # never reached -> captured
                elif board[r][c] == "#":
                    board[r][c] = "O"          # reached -> safe, restore


if __name__ == "__main__":
    sol = Solution()

    board = [["X", "X", "X", "X"],
             ["X", "O", "O", "X"],
             ["X", "X", "O", "X"],
             ["X", "O", "X", "X"]]
    sol.solve(board)
    assert board == [["X", "X", "X", "X"],
                      ["X", "X", "X", "X"],
                      ["X", "X", "X", "X"],
                      ["X", "O", "X", "X"]]

    all_x = [["X"]]
    sol.solve(all_x)
    assert all_x == [["X"]]

    single_o = [["O"]]                 # the only cell IS the border -> safe
    sol.solve(single_o)
    assert single_o == [["O"]]

    ring = [["O", "O", "O"],
            ["O", "X", "O"],
            ["O", "O", "O"]]           # the center X has no O to capture; ring touches border
    sol.solve(ring)
    assert ring == [["O", "O", "O"],
                     ["O", "X", "O"],
                     ["O", "O", "O"]]

    fully_boxed = [["X", "X", "X"],
                   ["X", "O", "X"],
                   ["X", "X", "X"]]
    sol.solve(fully_boxed)
    assert fully_boxed == [["X", "X", "X"],
                            ["X", "X", "X"],
                            ["X", "X", "X"]]

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Recursive DFS instead of BFS for the border flood

```python
import sys
sys.setrecursionlimit(20000)     # up to 200*200 = 40,000 cells

def solve(self, board):
    m, n = len(board), len(board[0])

    def dfs(r, c):
        if not (0 <= r < m and 0 <= c < n) or board[r][c] != "O":
            return
        board[r][c] = "#"
        for dr, dc in DIRS:
            dfs(r + dr, c + dc)

    for r in range(m):
        for c in range(n):
            if (r == 0 or r == m - 1 or c == 0 or c == n - 1) and board[r][c] == "O":
                dfs(r, c)

    for r in range(m):
        for c in range(n):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "#":
                board[r][c] = "O"
```

Same `O(m*n)` complexity; same recursion-depth caution as Pacific Atlantic and
Shortest Bridge at the `200×200` upper bound.

### 9b. The naive per-region approach (why it's more awkward, not just slower)

You *could* flood every `'O'` region once (like Number of Islands), and for each
region check whether *any* of its cells touch the border, capturing the whole
region if not. This is actually still `O(m*n)` overall (each cell flooded once) —
so unlike Pacific Atlantic's naive approach, this isn't asymptotically worse. But
it's **more bookkeeping**: you need to flood each region fully *before* knowing
whether to keep or flip it, track "does this region touch the border" per region,
then do a second pass to apply the decision. The border-anchored version answers
the question directly in one flood with no per-region bookkeeping at all — simpler
code, same complexity. This is a good case for **"correct but needlessly
complicated" vs "the clean way"**, worth naming explicitly if you write the
per-region version first.

### The BFS↔DFS answer the interviewer wants

> "Pure reachability, no shortest-path need — BFS or DFS both work, `O(m*n)`
> either way. I'd default to BFS to sidestep any recursion-depth risk on a
> `200×200` board. The real design decision here isn't BFS vs DFS, it's
> *flooding from the border and flipping the complement*, instead of flooding
> every region and deciding per-region."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = m*n`; edge = 4-neighbor adjacency,
`E ≈ 2mn = O(m*n)`.

**Time:**
- Seeding: scan the border, `O(m + n)`.
- BFS: each `'O'` cell is marked `'#'` (visited) at most once → `O(m*n)`.
- Cleanup pass: one more full scan → `O(m*n)`.
- **Total: `O(m * n)`.**

**Space:**
- No separate `seen` set — the `'#'` placeholder *is* the visited mark (same
  trick as every prior problem in these two groups).
- Queue: up to `O(m*n)` in the worst case.
- **Total: `O(m * n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| Board is all `'X'` | seed step finds nothing, BFS never runs, cleanup pass changes nothing |
| A single `'O'` cell in a `1x1` board | it *is* the border → safe, stays `'O'` |
| A ring of `'O'`s touching the border with `'X'` in the center | ring cells all reached (they touch the border directly) → all stay `'O'`; center `'X'` untouched |
| An `'O'` region fully enclosed by `'X'` with no border contact | never reached → fully flipped to `'X'` |
| Every `'O'` is on the border | all flood-marked safe, nothing captured |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Forgetting the "restore `#` back to `O`" half of the cleanup pass.**
      Flipping unreached `'O'`s to `'X'` but leaving the safe cells as `'#'`
      instead of `'O'` — produces a board with leftover placeholder characters
      instead of the required `'X'`/`'O'` output.
- [ ] **Seeding only *some* of the border** — e.g. forgetting corner cells, or
      only scanning two of the four edges. Use a single clean condition:
      `r == 0 or r == m-1 or c == 0 or c == n-1`.
- [ ] **Flooding before placing the seed marker.** If you enqueue a border cell
      without marking it `'#'` first, and it gets revisited via a neighbor before
      being dequeued, you can double-enqueue it — usually harmless (just wasted
      work) but sloppy; always mark on the same line you enqueue.
- [ ] **Mixing this up with Pacific Atlantic and adding a reversed condition or
      an intersection** — neither is needed here; plain `'O'`-adjacency is
      symmetric, and there's only one boundary.
- [ ] **Off-by-one on border indices** — `c == n - 1`, not `c == n`, etc.

---

## 13. Learnings & Transfer

**The reusable core: answer by complement.** When "safe/valid" means "connected
to a fixed boundary," you don't need to check each region's status individually —
flood the boundary once, and **everything not reached fails the check by
definition**. This is a variant of the boundary-anchored idea from Pacific
Atlantic, simplified because the relation here is symmetric (no reversal) and
there's a single target set (no intersection — just a complement).

**The two boundary-anchored problems, side by side:**

| | Pacific Atlantic | Surrounded Regions |
|---|---|---|
| Boundaries | 2 (Pacific, Atlantic) | 1 (the border) |
| Relation | directional (downhill) | symmetric (adjacency) |
| Needs reversal? | yes | no |
| Final combine step | intersection of 2 floods | complement of 1 flood |

| Situation | How this transfers |
|---|---|
| "Which regions are NOT connected to the outside" (any grid capture/enclosure problem) | flood from the border, flip/report the complement |
| Number of Enclaves (LC 1020) | identical shape: flood from border-touching land, count what's left uncaptured |
| Any "mark reachable-from-fixed-set, everything else fails" question | boundary flood + complement, one pass |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Instead of flipping captured regions to `'X'`, count how many separate captured regions there are, and report each one's size."

- **(b) Pattern:** boundary flood (to find *safe* cells) + a **second**,
  ordinary Group 01 flood-fill (to count/size the *remaining* regions).
- **(c) Adapt:** run the border flood exactly as before to mark safe cells `'#'`.
  Then run the standard "loop + flood" component-counting skeleton
  (`concepts/05`) over the remaining `'O'` cells — each fresh one found starts a
  new captured region; flood it (Max Area of Island style) to get its size.
- **(d) Say:** "This chains two patterns: boundary-flood to filter out the safe
  cells, then ordinary component-counting over what's left."

### Scenario 2 — "Border cells themselves might be `'X'` walls with gaps; 'connected to the outside' means reaching all the way past the board's actual outer wall through the gaps, not just touching row/column 0."

- **(b) Pattern:** the "boundary" is no longer literally "row/column 0/`m-1`/`n-1`"
  — it's a **given, possibly irregular set of gap cells**.
- **(c) Adapt:** seed the multi-source BFS with whatever cells are defined as
  "the gaps to the outside" instead of the literal grid edge. Everything else
  (the flood, the cleanup pass) is unchanged.
- **(d) Say:** "The 'boundary' in boundary-anchored traversal doesn't have to be
  the literal edge of the array — it's whatever fixed set the problem defines as
  the safe/target set."

### Scenario 3 — "Diagonal connections count too (8-directional)."

- **(b) Pattern:** same algorithm, `DIRS8`.
- **(c) Adapt:** swap `DIRS` for `DIRS8` in the BFS step. `O(m*n)` unchanged
  (constant factor of 8 instead of 4).
- **(d) Say:** "Same one-line neighbor-set swap as every other grid problem in
  this repo."

### Scenario 4 — "The board is huge and streamed row by row; you can't hold it all in memory. Determine captured regions with limited memory."

- **(b) Pattern:** scanline connected components (the same idea raised for
  Number of Islands' streaming scenario), specialized to "touches the border."
- **(c) Adapt:** track, per open region as you scan top to bottom, whether it has
  touched the left/right edge or the top row so far (a `touches_border` flag per
  live Union-Find component). A region only gets "resolved" (captured or not)
  once it closes out (no more cells in later rows) — if it never touched a
  border by the time it closes, capture it. `O(row width)` memory instead of
  `O(m*n)`.
- **(d) Say:** "The streaming/scanline version of any grid-boundary problem
  carries a per-component 'has this touched the boundary yet' flag through a
  live Union-Find, resolved region by region as they close out."

### Scenario 5 — "Add a rule: a region is also safe if it's connected to *any* previously-captured region from a prior game state (regions can be 'grandfathered in')."

- **(b) Pattern:** the safe/source set grows to include more than just the
  border — same mechanic as Scenario 2.
- **(c) Adapt:** seed the BFS with the border `'O'`s **plus** every cell in any
  grandfathered region. Everything else is identical.
- **(d) Say:** "Extra 'always safe' sources just mean a bigger seed set for the
  same multi-source flood — the algorithm doesn't change shape."

### Scenario 6 — "This is really a network problem: which internal servers ('O') are NOT reachable from any internet-facing gateway ('border'), and should be flagged as isolated/unreachable (the opposite framing — you want the *captured* ones, not the safe ones)."

- **(b) Pattern:** identical algorithm; this scenario just underlines that the
  "useful" output is the **complement set**, not the flooded set — exactly what
  Surrounded Regions already computes (the captured region *is* "unreachable from
  the border").
- **(c) Adapt:** no algorithmic change — the captured (unreached) cells found
  during cleanup ARE the isolated-server list; just report them directly instead
  of flipping them to `'X'`.
- **(d) Say:** "Recognize when a real-world question is *already* asking for the
  complement of a boundary flood — Surrounded Regions is that pattern in its
  purest form."

---

## 15. Flashcards

**Q:** How does Surrounded Regions differ from Pacific Atlantic?
**A:** One boundary instead of two; the "connected to" relation is **symmetric**
(no reversal needed); the answer is the **complement** of one flood, not an
intersection of two.

**Q:** The core trick — how do you find "boxed in" regions without checking each
one?
**A:** Flood from every border-touching `'O'` (multi-source); everything the
flood *doesn't* reach was boxed in by definition.

**Q:** What does the `'#'` placeholder do here?
**A:** Doubles as both "safe" and "visited" — the same mutation-as-visited-mark
trick as Flood Fill/Walls and Gates/01 Matrix/Rotting Oranges/Shortest Bridge.

**Q:** The #1 bug in this exact problem?
**A:** Forgetting to restore `'#'` back to `'O'` in the cleanup pass — leaves
placeholder characters in the final board instead of the required `'O'`/`'X'`.

**Q:** Time and space, with derivation?
**A:** `O(m*n)` both — seed scan `O(m+n)`, BFS visits each `'O'` once, cleanup
scan `O(m*n)`. No separate visited structure (the `'#'` mark serves that role).

**Q:** Naive alternative (flood every region, check border-touch per region) —
is it asymptotically worse?
**A:** No — still `O(m*n)` overall. It's not slower, just **more bookkeeping**
per region for no benefit; boundary-anchored flooding answers it directly.

**Q:** How does this generalize if "the border" isn't literally row/col 0/m-1/n-1?
**A:** Seed the flood with whatever fixed cell set the problem defines as "safe" —
the algorithm doesn't care whether that set is the literal grid edge.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Multi-source BFS + cleanup pass, using `'T'` as
the placeholder instead of `'#'` — same idea, different marker character.

```python
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows = len(board)
        columns = len(board[0])

        queue = deque()

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for i in range(rows):
            for j in range(columns):
                if (i == 0 or i == rows - 1 or j == 0 or j == columns - 1) and board[i][j] == 'O':
                    queue.append((i, j))

        while queue:
            r, c = queue.popleft()
            board[r][c] = 'T'

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < columns) and board[nr][nc] == 'O':
                    queue.append((nr, nc))

        for i in range(rows):
            for j in range(columns):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == 'T':
                    board[i][j] = 'O'
```

**Correct.** I ran it against every case from section 8's tests (the full
official example, `[["O"]]`, the border-touching ring, the fully-boxed single
cell) plus a 100×100 all-`'O'` stress test, and all match — including the stress
test finishing instantly with no blow-up.

**One efficiency note worth understanding (not a bug):** this marks a cell `'T'`
when it's **dequeued**, not when it's **enqueued** — the opposite of the house
rule from `concepts/03` ("mark visited when you enqueue, never when you
dequeue"). Here's the effect: the enqueue check only tests `board[nr][nc] ==
'O'`, so if two different frontier cells both look at the *same* still-`'O'`
neighbor before either of them gets dequeued, that neighbor gets pushed onto the
queue **twice** (once from each). It's still correct — the second time it's
popped, `board[r][c] = 'T'` just reapplies harmlessly, and by then its neighbors
are already `'T'`, so nothing extra happens — but it means a cell can enter the
queue up to 4 times (once per neighbor) instead of exactly once. That's a
constant-factor blow-up, not a complexity-class one (still `O(m*n)` overall,
just with more queue churn) — which is exactly why the 100×100 stress test above
still finished in a fraction of a second. Marking at enqueue time (the primary
solution's approach) avoids the duplicate pushes entirely and is worth building
as the default habit, but this version isn't wrong.
