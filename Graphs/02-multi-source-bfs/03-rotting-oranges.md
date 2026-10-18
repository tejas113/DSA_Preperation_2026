# Rotting Oranges  ·  LeetCode 994  ·  Medium

Group 02 — Multi-Source BFS  ·  same skeleton as the first two problems, but now
the **answer is the number of rounds**, not a per-cell distance — and there's a
genuine "impossible" case to detect.

Prereqs: `01-walls-and-gates.md`, `02-01-matrix.md`, `concepts/03` (BFS, especially
**Flavor B — ring counting**). New idea: **the off-by-one trap in "how many rounds
until done"**, and a cleaner alternative that avoids it entirely.

---

## 1. Problem

You are given an `m x n` grid where each cell is:

- `0` — empty.
- `1` — a fresh orange.
- `2` — a rotten orange.

Every minute, any **fresh** orange **4-directionally adjacent** to a **rotten**
orange becomes rotten too — all such conversions happen **simultaneously** each
minute.

**Return the minimum number of minutes until no cell has a fresh orange. If that's
impossible, return `-1`.**

Constraints:
- `1 <= m, n <= 10`.
- `grid[r][c]` is `0`, `1`, or `2`.

Example 1:

```
grid = [[2,1,1],
        [1,1,0],
        [0,1,1]]
answer = 4
```

Example 2 (impossible):

```
grid = [[2,1,1],
        [0,1,1],
        [1,0,1]]
answer = -1
```

The `1` at `(2,0)` is walled off by `0`s (empty cells block spread) from every
rotten orange — it can never rot.

Example 3:

```
grid = [[0,2]]
answer = 0     # no fresh oranges at all -> 0 minutes needed
```

---

## 2. Explain Like I'm 5

Same "wave spreading from every source at once" idea — except now the sources are
**rotten oranges**, the wave is **rot**, and instead of asking "how far is each
room from a gate," you ask **"how many minutes until the wave has touched
everything it possibly can?"**

Every rotten orange infects its fresh neighbors after exactly one minute. Then
*those* newly-rotten oranges infect *their* neighbors the next minute. You keep a
clock. When there's no fresh orange left, you read the clock. If some fresh
oranges are trapped somewhere the wave can never reach (blocked by empty cells on
every side), it's impossible — answer `-1`.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Multiple sources spreading simultaneously | ✅ every initially-rotten orange |
| "How many minutes/rounds **until everything is done**" (not a per-cell distance) | ✅ → the answer is a single number: the **last** round that changed anything |
| A genuine "impossible" outcome | ✅ some fresh orange unreachable |

**Reduce it to:** *"Multi-source BFS where the answer is the total number of
rounds executed, and you must separately verify every fresh orange got reached."*

**Look-alikes:**
- Walls and Gates / 01 Matrix ask for **each cell's own** distance. Rotting
  Oranges asks for **one number**: the maximum distance reached (equivalently,
  the number of full rounds).
- "Impossible" here is a **first-class output** (`-1`), unlike 01 Matrix which is
  guaranteed always reachable.

---

## 4. Intuition

1. All initially-rotten oranges are sources, all starting at minute `0`.
2. If I BFS ring-by-ring (`concepts/03` Flavor B — freeze the queue's current size,
   process exactly that many, that's one full minute), then **the number of rings
   I process equals the number of minutes elapsed**.
3. I should stop as soon as there's no fresh orange left to convert — continuing
   would just process empty rounds that rot nothing, incorrectly inflating the
   minute count.
4. At the end: if every fresh orange got converted (`fresh == 0`), the number of
   minutes I counted is the answer. If some fresh oranges are still `1` (never
   reached — walled off by empty cells), it's impossible → `-1`.
5. Rotting a cell (`1 → 2`) is irreversible and doubles as its visited mark — the
   same trick as every problem in this group.

**The subtlety that trips people up:** if you don't stop the round-counting the
instant `fresh` hits `0`, you'll process one extra "silent" round at the end (the
last rotten oranges get popped, find no fresh neighbors, nothing happens) and
**overcount by 1**. This is section 12's #1 bug — walk through it there.

---

## 5. Approach (primary): multi-source BFS, ring counting, with a fresh-count guard

1. `m, n = len(grid), len(grid[0])`. `q = deque()`. `fresh = 0`.
2. Scan every cell: if `2`, push `(r, c)` into `q`. If `1`, `fresh += 1`.
3. If `fresh == 0` already: return `0` immediately (nothing to wait for).
4. `minutes = 0`. While `q` is non-empty **and** `fresh > 0`:
   - `minutes += 1`.
   - Process exactly `len(q)` cells (one full ring = one minute): for each, look
     at its 4 neighbors; if a neighbor is `1`, set it to `2`, `fresh -= 1`, push it.
5. After the loop: return `minutes` if `fresh == 0`, else `-1`.

Builds on: `concepts/03` BFS Flavor B (ring counting), the mutation-as-visited
trick from every earlier problem in this group.

---

## 6. Pseudocode

```
function orangesRotting(grid):
    m, n = rows, cols
    q = empty queue
    fresh = 0

    for each cell (r, c):
        if grid[r][c] == 2: enqueue (r, c)
        if grid[r][c] == 1: fresh += 1

    if fresh == 0: return 0

    minutes = 0
    while q not empty and fresh > 0:
        minutes += 1
        for each of the current len(q) items:
            (r, c) = dequeue
            for each of the 4 neighbors (nr, nc):
                if in bounds and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    enqueue (nr, nc)

    return minutes if fresh == 0 else -1
```

---

## 7. Dry Run

```
grid = [[2,1,1],
        [1,1,0],
        [0,1,1]]
```

Seed: `(0,0)` is the only `2` → `q = [(0,0)]`. Count the `1`s: `(0,1),(0,2),(1,0),
(1,1),(2,1),(2,2)` → `fresh = 6`.

| minute | ring processed (popped this round) | neighbors rotted this round | fresh after | queue after |
|---|---|---|---|---|
| 1 | (0,0) | (1,0)→2, (0,1)→2 | 4 | [(1,0),(0,1)] |
| 2 | (1,0), (0,1) | (1,1)→2 [from (1,0)]; (0,2)→2 [from (0,1)] | 2 | [(1,1),(0,2)] |
| 3 | (1,1), (0,2) | (2,1)→2 [from (1,1)]; (0,2) has no new fresh neighbor | 1 | [(2,1)] |
| 4 | (2,1) | (2,2)→2 | 0 | [(2,2)] |

After minute 4, `fresh == 0` → the `while` condition fails before a 5th round
starts (even though `q = [(2,2)]` is still non-empty!). Loop stops.

Return `minutes = 4`. ✅ Matches Example 1.

**Notice**: `(2,2)` is left sitting in the queue, unprocessed — and that's fine.
Once `fresh == 0` there is nothing left for it to infect, so processing its round
would find zero fresh neighbors and contribute nothing except an incorrect `+1` to
`minutes`. That's exactly the bug the `fresh > 0` guard prevents.

---

## 8. Python Code (primary — multi-source BFS, ring counting)

```python
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    q.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:                          # nothing to wait for
            return 0

        minutes = 0
        while q and fresh > 0:                  # STOP the instant nothing fresh remains
            minutes += 1
            for _ in range(len(q)):              # process exactly one ring == one minute
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 2         # rot it == mark visited
                        fresh -= 1
                        q.append((nr, nc))

        return minutes if fresh == 0 else -1


if __name__ == "__main__":
    sol = Solution()

    assert sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert sol.orangesRotting([[0, 2]]) == 0
    assert sol.orangesRotting([[1]]) == -1          # a fresh orange with no rotten source at all
    assert sol.orangesRotting([[2]]) == 0            # no fresh oranges
    assert sol.orangesRotting([[0, 0, 0]]) == 0      # no oranges at all

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Store the time with each queue entry (avoids the off-by-one entirely — cleaner code)

Instead of counting rings, carry the current minute along with each cell. The
answer becomes simply "the largest time value ever assigned" — no guard needed,
no risk of an extra silent round.

```python
from collections import deque
from typing import List


class SolutionTimestamped:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    q.append((r, c, 0))          # (row, col, minute it rotted)
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:
            return 0

        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
        minutes = 0
        while q:
            r, c, t = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    minutes = t + 1              # answer = latest rot time seen
                    q.append((nr, nc, t + 1))

        return minutes if fresh == 0 else -1
```

Same `O(m*n)` complexity. This version can't overcount by a silent round because
`minutes` is only ever updated *when an orange actually rots* — there's no "was
this round wasted?" bookkeeping to get wrong. Many engineers prefer this version
specifically because it removes a whole category of off-by-one bug.

### The BFS↔DFS answer the interviewer wants

> "This must be BFS, not DFS — the answer depends on the *round number* (or
> equivalently, the graph distance from the nearest rotten orange), and only BFS
> guarantees cells are reached in true minute-order. I'd write the ring-counting
> version first since it matches how the problem is phrased ('every minute...'),
> then mention the timestamped-queue version as a cleaner alternative that avoids
> the classic off-by-one."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = m*n`; edge = 4-neighbor adjacency,
`E ≈ 2mn = O(m*n)`.

**Time:**
- Initial scan to seed sources and count `fresh`: `O(m*n)`.
- BFS: each cell rots **at most once** (`grid[r][c] == 1` check prevents
  re-processing), and each rot triggers `O(1)` work examining 4 neighbors. Total
  across the whole BFS: `O(m*n)`.
- **Total: `O(m * n)`.**

**Space:**
- No separate `seen` set — rotting a cell (`1 → 2`) *is* the visited mark.
- Queue: up to `O(m*n)` in the worst case.
- **Total: `O(m * n)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| No fresh oranges at all | early `return 0` before the BFS even starts |
| No rotten oranges, but fresh ones exist | `q` starts empty → `while` loop never runs → `fresh` stays `> 0` → returns `-1` |
| A fresh orange walled off by `0`s | never reached by any ripple → still `1` at the end → `-1` |
| Grid is entirely `0`s | `fresh == 0` → `0` |
| Single cell `[[2]]` / `[[1]]` / `[[0]]` | `0` / `-1` / `0` |
| All oranges already rotten | `fresh == 0` → `0` |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **The off-by-one from an extra silent round.** Using `while q:` (without the
      `and fresh > 0` guard) processes one more ring after the last fresh orange
      rots — that ring rots nothing but still increments `minutes`, overcounting
      by exactly `1`. Symptom: your answer is consistently `1` too high on grids
      where the queue isn't empty right when `fresh` hits `0`. Fix: add the guard,
      or switch to the timestamped-queue version (9a) which sidesteps the issue
      entirely.
- [ ] **Forgetting the `fresh == 0` early return.** Without it, a grid with zero
      fresh oranges still enters the `while` loop... actually it won't loop
      (nothing to pop-and-rot), but some incorrect implementations increment
      `minutes` once before checking, giving `1` instead of `0`. Always check
      `fresh == 0` up front.
- [ ] **Not detecting the impossible case.** Forgetting to check `fresh == 0` *at
      the end* and just returning `minutes` unconditionally — silently wrong on
      grids with unreachable fresh oranges (returns some finite number instead of
      `-1`).
- [ ] **Using DFS "for simplicity."** Without careful relaxation (only overwrite
      if the new minute is smaller), DFS can rot a cell via a longer path first,
      giving a minute count larger than the true minimum — same failure mode as
      Walls and Gates' DFS alternative.
- [ ] **Mutating `grid` while also trying to read "original" values elsewhere in
      the same pass** — usually not an issue here since we only ever check
      `== 1`/`== 2`, but be aware if you extend the problem (e.g. Scenario 3).

**Narrate:** "My test expects 4 but I get 5. Let me check my loop condition — I'm
using `while q:` alone. The last round only had one rotten orange left in the
queue with no fresh neighbors, so it did nothing but still counted as a minute.
I need to stop as soon as `fresh` reaches 0, not just when the queue empties."

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **"How many rounds until done" is answered by ring-counting BFS (`concepts/03`
   Flavor B) — but you must stop the instant the goal condition is met**, not just
   when the queue empties, or you overcount by one wasted round.
2. **The timestamped-queue variant** (carry `(node, time)` in the queue, answer =
   max time ever assigned) is a more robust alternative whenever "how many
   rounds" is the question — it structurally can't have the off-by-one bug.
3. **"Impossible" is a real, expected output** whenever a multi-source spread
   might not reach everything — always verify full coverage (`fresh == 0`) rather
   than assuming it.

| Problem | How this transfers |
|---|---|
| Walls and Gates / 01 Matrix | same BFS engine; those ask for *every cell's own* distance, this asks for *one number* (the max distance / round count) |
| Shortest Bridge (next, supplementary) | multi-source BFS again, this time the answer *is* a per-BFS distance (steps to reach the other island), with sources seeded from a DFS-found island |
| Any "simultaneous spread, how long until everything is covered" problem (fire spread, virus spread, signal propagation) | this exact skeleton |
| Any "is it possible" question layered on top of reachability | always check coverage explicitly at the end, don't assume |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Different orange varieties rot at different speeds: some infect a neighbor in 1 minute, others take 2 minutes to infect their neighbors."

- **(b) Pattern:** non-uniform edge weights (`1` or `2`) → plain BFS ring-counting
  breaks (a "round" no longer means one uniform minute for every edge).
- **(c) Adapt:** switch to **multi-source Dijkstra** (heap of `(time, r, c)`), or —
  since weights are only two small integers — a more efficient **bucket queue /
  0-1(-2) BFS**: an array of queues indexed by arrival time (`buckets[t]` holds
  cells finishing at minute `t`), advance `t` one at a time, popping `buckets[t]`
  and pushing discoveries into `buckets[t + weight]`. `O(V + E)`, avoiding the
  heap's `log` factor.
- **(d) Say:** "Non-uniform integer weights don't need a full Dijkstra if the
  weight range is small — a bucket queue (Dial's algorithm) keeps it linear."

### Scenario 2 — "Rotten oranges don't all start at minute 0 — some appear later (e.g. contamination introduced at different times)."

- **(b) Pattern:** multi-source BFS with **non-zero, unequal starting times**.
- **(c) Adapt:** seed the queue (or bucket structure) with each source at its own
  `(r, c, start_time)` instead of all at `0`. A plain FIFO `deque` no longer
  guarantees processing in true chronological order once sources have different
  start times — use a **min-heap** ordered by current time (multi-source
  Dijkstra with all edge weights `1`), or a bucket queue indexed by absolute time
  if start times are small integers.
- **(d) Say:** "The instant sources don't all start at the same time, a plain
  deque's FIFO order stops matching true time order — reach for a heap or a
  time-indexed bucket structure instead."

### Scenario 3 — "For every orange that eventually rots, report which specific rotten neighbor caused it, and at what minute — build an infection trace."

- **(b) Pattern:** BFS + parent/cause pointers (same idea as 01 Matrix Scenario 4).
- **(c) Adapt:** when rotting `(nr, nc)` from `(r, c)`, record
  `cause[nr][nc] = (r, c, current_minute)`. After the BFS, any cell's full
  infection chain is a walk backward through `cause` until you hit an originally-
  rotten cell (`cause` unset). `O(m*n)` extra space, no change to time complexity.
- **(d) Say:** "Recording one 'caused-by' pointer per node during BFS turns a
  reachability/timing answer into a full causal trace, for free."

### Scenario 4 — "Instead of just detecting 'impossible,' list the exact coordinates of every fresh orange that never rots."

- **(b) Pattern:** same BFS; swap the `fresh` **counter** for a `fresh` **set** of
  coordinates.
- **(c) Adapt:** initialize `fresh = {(r, c) for every 1 cell}`; each time a cell
  rots, `fresh.discard((r, c))`. At the end, `fresh` (if non-empty) *is* the
  answer to "which ones never rotted" — no extra pass needed.
- **(d) Say:** "When you need the *identities* of the leftover cells, not just a
  count, swap the counter for a set and read it directly at the end."

### Scenario 5 — "Oranges can also spontaneously **un-rot** back to fresh after some number of minutes if not reinforced by staying adjacent to another rotten orange (a decay rule)."

- **(b) Pattern:** **breaks BFS's core assumption.** Plain multi-source BFS relies
  on each cell changing state **at most once** (fresh → rotten, irreversibly) —
  that's exactly what let a mutation double as the visited mark. A decay rule
  makes state non-monotonic.
- **(c) Adapt:** you can no longer treat this as a single clean BFS. It becomes a
  **minute-by-minute simulation**: at each timestep, compute the *set* of cells
  rotting AND the set of cells decaying back, apply both simultaneously (careful
  about order — compute the next state from the current state entirely before
  applying it, like Conway's Game of Life), and repeat until the grid stabilizes
  or you hit a cycle. Flag that this is fundamentally a different, more expensive
  class of problem (potentially never terminating without a cycle-detection
  safeguard) — not a small tweak to BFS.
- **(d) Say:** "The moment a cell's state isn't monotonic (can revert), you've left
  BFS's territory — you need a generation-by-generation simulation instead, and
  you should check for infinite loops explicitly."

### Scenario 6 — "You'll be given thousands of different starting grids (same dimensions/layout, different fresh/rotten placement) and must answer each quickly. Any way to share work across them?"

- **(b) Pattern:** a caution, not a shortcut — unlike 01 Matrix / Walls and Gates
  (where the *targets* are fixed and many *queries* can share one precomputed
  answer grid), here the **source set itself changes every time**, so there's
  generally nothing to precompute across different grids.
- **(c) Adapt:** each distinct grid needs its own `O(m*n)` BFS — that's already
  optimal per query, so the honest answer is "no algorithmic shortcut without more
  structure." If many queries share most of their rotten cells and differ by only
  a few, you *could* explore incremental recomputation from the differences, but
  call out that this only helps if the problem guarantees small, bounded diffs
  between queries — don't invent structure that isn't given.
- **(d) Say:** "Precompute-once-answer-many-queries only works when what's fixed
  across queries is the *target/source set*, not when the sources themselves are
  the varying input — recognize which one you're in before reaching for that
  trick."

---

## 15. Flashcards

**Q:** How does Rotting Oranges differ from Walls and Gates / 01 Matrix in what
it returns?
**A:** Those return each cell's *own* distance. This returns *one number* — the
number of full rounds (equivalently, the max distance reached) — plus a
possible `-1` for "impossible."

**Q:** The #1 bug in this exact problem?
**A:** Off-by-one from an extra silent round: using `while q:` instead of
`while q and fresh > 0:` processes one more ring after the last fresh orange
already rotted, overcounting `minutes` by 1.

**Q:** How does the timestamped-queue alternative avoid that bug structurally?
**A:** It stores `(cell, minute)` per queue entry and sets `minutes = t + 1` only
when a cell actually rots — there's no "was this round wasted?" bookkeeping to
get wrong.

**Q:** How do you detect the impossible case?
**A:** Track a `fresh` counter (or set); after the BFS, if it's not zero, some
fresh orange was never reached → return `-1`.

**Q:** Time and space, with derivation?
**A:** `O(m*n)` both. Each cell rots at most once (the `== 1` check prevents
reprocessing); rotting doubles as the visited mark, no separate `seen` set.

**Q:** Why is DFS the wrong tool here?
**A:** The answer depends on true round/distance order; DFS without careful
"only update if shorter" relaxation can rot a cell via a longer path first,
inflating the minute count.

**Q:** Different infection speeds (weights ≠ 1) — what replaces plain BFS?
**A:** Multi-source Dijkstra (heap), or a bucket queue / Dial's algorithm if
weights are small integers — stays `O(V+E)` without a heap's log factor.

**Q:** Sources appearing at different start times — why does a plain deque break?
**A:** FIFO insertion order no longer matches true chronological order once
sources don't all start at 0 — need a heap or a time-indexed bucket structure.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Ring-counting multi-source BFS with the
`fresh_count > 0` guard, `O(m*n)` time and space — matches the primary solution.

```python
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        columns = len(grid[0])

        fresh_count = 0

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        queue = deque()
        time = 0
        for i in range(rows):
            for j in range(columns):
                if grid[i][j] == 2:
                    queue.append((i, j))
                if grid[i][j] == 1:
                    fresh_count = fresh_count + 1

        while queue and fresh_count > 0:
            time = time + 1
            for i in range(len(queue)):
                r, c = queue.popleft()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < columns) and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh_count = fresh_count - 1
                        queue.append((nr, nc))

        if fresh_count > 0:
            return -1
        else:
            return time
```

**Correct**, and it dodges the section-12 off-by-one bug exactly right: the
`while queue and fresh_count > 0` guard is there.

**One nice thing worth noticing about your own code:** you didn't write a separate
`if fresh_count == 0: return 0` early check (the primary solution has one) — and
you don't need it. If there are no fresh oranges, `fresh_count > 0` is `False`
from the very first loop check, so the `while` body never runs, `time` stays `0`,
and the final `else: return time` gives `0` anyway. The early return in the
primary version is there for *readability* (it states the "nothing to do" case up
front), not because it's required — your version proves the guard alone already
covers it correctly.
