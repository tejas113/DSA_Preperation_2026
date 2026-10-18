# Making a Large Island  ·  LeetCode 827  ·  Hard  ·  *(supplementary)*

Group 01 — Grid Flood-Fill  ·  the Google-hard finale of this group. Combines
**every** idea from the first three problems: flood + return-an-aggregate + a
second pass that evaluates candidates in O(1) using precomputed labels.

Prereqs: `01-number-of-islands.md`, `03-max-area-of-island.md`. New idea: **label
each component with an id, then use those ids to answer a "what if" question in a
second pass** — the single most reusable trick in this whole file.

---

## 1. Problem

You are given an `n x n` binary grid. You may change **at most one** `0` to a `1`.

**Return the size of the largest island possible after doing that (optimal)
single change.** (If there is no `0` to change, the answer is just the size of the
existing largest island — which, if the grid is all `1`s, is `n*n`.)

Constraints:
- `1 <= n <= 500`.
- `grid[i][j]` is `0` or `1`.

Example 1:

```
grid = [[1,0],
        [0,1]]
Flip (0,1) or (1,0) -> connects both single-cell islands + the flipped cell.
answer = 3
```

Example 2:

```
grid = [[1,1],
        [1,0]]
Flip (1,1) -> joins the flipped cell to the existing size-3 island.
answer = 4
```

Example 3:

```
grid = [[1,1],
        [1,1]]
No 0 to flip. answer = 4  (the island is already the whole grid)
```

---

## 2. Explain Like I'm 5

You already know how to scribble over islands and measure them (previous two
problems). Now imagine you're allowed **one** magic seed: drop it on any blue (sea)
square and it instantly turns green (land).

You want to drop it where it does the most good — ideally somewhere that **touches
two (or more) different islands at once**, so the seed fuses them together into
one bigger island.

So here's the plan: first, color and **label** every island with its own name
("Island #2", "Island #3", ...) and write down each island's size, like a
scoreboard. Then walk over every blue square and ask: "if I dropped the seed here,
which island-names are touching me?" Add up the sizes of the touching islands, plus
1 for the seed itself. Whichever blue square gives the biggest total — that's where
you'd drop the seed, and that total is the answer.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Grid flood-fill, connected components | ✅ (same skeleton as the whole group) |
| "You may change **one** cell — what's the best outcome?" | ✅ → **label + probe**, not a fresh flood per candidate |
| Need each component's **size**, looked up **by which component a neighbor belongs to** | ✅ → components need **ids**, not just a `seen` set |
| A naive "try flipping every 0, re-flood-fill, take the max" would be `O(n^2)` flips `× O(n^2)` per flood `= O(n^4)` — too slow for `n = 500` | ✅ → must precompute |

**Reduce it to:** *"Precompute connected-component labels and sizes once
(`O(n^2)`). Then, for every candidate change, answer using only the labels of its
immediate neighbors (`O(1)` per candidate) instead of re-running a flood."*

This "precompute once, evaluate every candidate change in O(1)" idea is worth
memorizing on its own — it is asked about directly in Scenario 5 of both earlier
problems, and it recurs constantly (see section 13).

**Look-alikes:**
- Max Area of Island → gives you the sizes; this problem adds the "id" and the
  probe pass.
- Number of Islands → the id-labeling loop is line-for-line the same as its
  counting loop, just storing a size instead of incrementing a counter.
- Shortest Bridge (Group 02, supplementary) → also about connecting two islands,
  but there you must find the *shortest path* between them, not the best single
  merge point.

---

## 4. Intuition

1. If I flip a water cell `(r, c)` to land, the new island it joins is: itself,
   plus every **distinct** island that touches one of its 4 neighbors.
2. "Distinct" matters — if two of its neighbors belong to the *same* island, I must
   not add that island's size twice.
3. So I need, for every land cell, **which island it belongs to** (an id) — a plain
   `seen` set isn't enough, because a set can't tell me *which* component a
   neighbor is in, only *that* it's visited.
4. **Pass 1:** flood every island once (exactly like Max Area of Island), but this
   time stamp every one of its cells with a unique `island_id`, and remember
   `size[island_id]`.
5. **Pass 2:** for every water cell, look at its ≤4 neighbors, collect the
   **distinct** ids among them (a `set` handles the "distinct" automatically),
   and the candidate value is `1 + sum(size[id] for id in that set)`.
6. Track the maximum candidate across all water cells. Also seed the maximum with
   the largest island from Pass 1, so an all-land grid (no water to flip) still
   returns the right answer.

**Why correct:** step 4 makes every land cell's component membership an `O(1)`
lookup. Step 5 then evaluates *every possible single flip* in `O(1)` each, using
only that lookup — so the whole second pass is `O(n^2)` instead of re-flooding for
every candidate.

---

## 5. Approach (primary): two-pass DFS with a `label` grid

1. `n = len(grid)`. Make a `label` grid of zeros the same size (0 = unlabeled), and
   `size = {}` mapping `island_id -> cell count`.
2. **Pass 1.** `next_id = 2` (`0`/`1` are taken by "water"/"land" in the input, so
   start ids at 2 to avoid any confusion if you ever print both grids side by
   side). For every cell that is land (`grid[r][c] == 1`) and unlabeled
   (`label[r][c] == 0`): flood it with `dfs(r, c, next_id)`, which stamps
   `label[r][c] = next_id` on every cell it visits and returns the island's size;
   store `size[next_id] = area`; `next_id += 1`.
3. `best = max(size.values(), default=0)` — handles "no water cell exists" (all
   land) up front.
4. **Pass 2.** For every water cell `(r, c)`: collect
   `neighbor_ids = {label[nr][nc] for each in-bounds neighbor with label != 0}`.
   `candidate = 1 + sum(size[i] for i in neighbor_ids)`.
   `best = max(best, candidate)`.
5. Return `best`.

Builds on: `concepts/04` (grid DFS), `03-max-area-of-island.md` (DFS returning an
aggregate) — this problem's `dfs` does both: stamps a label **and** returns a size.

---

## 6. Pseudocode

```
function largestIsland(grid):
    n = size of grid
    label = n x n grid of 0
    size = empty map
    next_id = 2

    function dfs(r, c, id) -> int:
        if r,c off board: return 0
        if grid[r][c] == 0 or label[r][c] != 0: return 0
        label[r][c] = id
        area = 1
        area += dfs(r+1,c,id); area += dfs(r-1,c,id)
        area += dfs(r,c+1,id); area += dfs(r,c-1,id)
        return area

    for r in 0..n-1:
        for c in 0..n-1:
            if grid[r][c] == 1 and label[r][c] == 0:
                size[next_id] = dfs(r, c, next_id)
                next_id += 1

    best = max(size.values()) if size else 0

    for r in 0..n-1:
        for c in 0..n-1:
            if grid[r][c] == 0:
                ids = distinct label[nr][nc] over in-bounds neighbors where label != 0
                candidate = 1 + sum(size[i] for i in ids)
                best = max(best, candidate)

    return best
```

---

## 7. Dry Run

```
grid = [[1,1,0],
        [1,0,0],
        [0,0,1]]
```

**Pass 1** — flood from `(0,0)`: reaches `(0,0),(0,1),(1,0)`, stamps them `2`,
`size[2] = 3`. Flood from `(2,2)`: reaches only itself, stamps `3`, `size[3] = 1`.

```
label = [[2,2,0],
         [2,0,0],
         [0,0,3]]
size = {2: 3, 3: 1}
best = max(3, 1) = 3   (initialized from Pass 1)
```

**Pass 2** — walk every water cell:

| water cell | in-bounds neighbors & their label | distinct ids | candidate = 1+Σsize | best |
|---|---|---|---|---|
| (0,2) | (1,2)=0, (0,1)=2 | {2} | 1+3=**4** | 4 |
| (1,1) | (0,1)=2, (2,1)=0, (1,0)=2, (1,2)=0 | {2} | 1+3=4 | 4 |
| (1,2) | (0,2)=0, (2,2)=3, (1,1)=0 | {3} | 1+1=2 | 4 |
| (2,0) | (1,0)=2, (2,1)=0 | {2} | 1+3=4 | 4 |
| (2,1) | (1,1)=0, (2,2)=3, (2,0)=0 | {3} | 1+1=2 | 4 |

No water cell touches **both** id `2` and id `3` here, so the two islands can't be
fused in one flip. Best achievable = **4** (flip `(0,2)`, `(1,1)`, or `(2,0)` — any
one attaches to the size-3 island).

Return **4**. ✅

---

## 8. Python Code (primary — DFS with a separate `label` grid, input untouched)

```python
from typing import List


class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
        label = [[0] * n for _ in range(n)]     # 0 = water / not yet labeled
        size = {}                                # island_id -> cell count
        next_id = 2                              # start above 0/1 so ids are unambiguous

        def dfs(r: int, c: int, island_id: int) -> int:
            if not (0 <= r < n and 0 <= c < n):
                return 0
            if grid[r][c] == 0 or label[r][c] != 0:
                return 0
            label[r][c] = island_id
            area = 1
            for dr, dc in DIRS:
                area += dfs(r + dr, c + dc, island_id)
            return area

        # Pass 1: label every island, remember its size
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1 and label[r][c] == 0:
                    size[next_id] = dfs(r, c, next_id)
                    next_id += 1

        best = max(size.values(), default=0)     # handles "grid is all land"

        # Pass 2: for every water cell, sum the DISTINCT neighboring islands
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    neighbor_ids = set()
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and label[nr][nc] != 0:
                            neighbor_ids.add(label[nr][nc])
                    candidate = 1 + sum(size[i] for i in neighbor_ids)
                    best = max(best, candidate)

        return best


if __name__ == "__main__":
    sol = Solution()

    assert sol.largestIsland([[1, 0], [0, 1]]) == 3
    assert sol.largestIsland([[1, 1], [1, 0]]) == 4
    assert sol.largestIsland([[1, 1], [1, 1]]) == 4
    assert sol.largestIsland([[0]]) == 1
    assert sol.largestIsland([[1]]) == 1
    assert sol.largestIsland([[0, 0], [0, 0]]) == 1
    assert sol.largestIsland([[1, 1, 0], [1, 0, 0], [0, 0, 1]]) == 4

    # far-apart islands (opposite corners of a row) can't be merged by one flip
    far_apart = [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    assert sol.largestIsland(far_apart) == 2

    print("all tests passed")
```

> We deliberately keep `grid` untouched and stamp a **separate** `label` grid
> instead — matches our house rule of not mutating input unless told to, and it
> doubles as the id lookup Pass 2 needs (a plain `seen` set couldn't answer "which
> island is this?"). The classic LeetCode-accepted solution mutates `grid` itself
> to save that array — shown as 9b.

---

## 9. Alternative Approaches

### 9a. BFS labeling (same two-pass idea, iterative flood)

```python
from collections import deque
from typing import List


class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
        label = [[0] * n for _ in range(n)]
        size = {}
        next_id = 2

        def bfs(sr: int, sc: int, island_id: int) -> int:
            q = deque([(sr, sc)])
            label[sr][sc] = island_id
            area = 0
            while q:
                r, c = q.popleft()
                area += 1
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < n and 0 <= nc < n
                            and grid[nr][nc] == 1 and label[nr][nc] == 0):
                        label[nr][nc] = island_id
                        q.append((nr, nc))
            return area

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1 and label[r][c] == 0:
                    size[next_id] = bfs(r, c, next_id)
                    next_id += 1

        best = max(size.values(), default=0)
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    ids = {label[r + dr][c + dc]
                           for dr, dc in DIRS
                           if 0 <= r + dr < n and 0 <= c + dc < n and label[r + dr][c + dc] != 0}
                    best = max(best, 1 + sum(size[i] for i in ids))
        return best
```

### 9b. In-place mutation (the classic LeetCode-accepted version — saves the `label` array)

Same algorithm, but stamp the island id directly into `grid` (ids `2, 3, 4, ...`
are safely distinguishable from `0`/`1`), skipping the separate array:

```python
def largestIsland(self, grid):
    n = len(grid)
    DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    size = {}
    next_id = 2

    def dfs(r, c, island_id):
        if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1:
            return 0
        grid[r][c] = island_id              # mutate the input itself
        area = 1
        for dr, dc in DIRS:
            area += dfs(r + dr, c + dc, island_id)
        return area

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                size[next_id] = dfs(r, c, next_id)
                next_id += 1

    best = max(size.values(), default=0)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                ids = {grid[r + dr][c + dc]
                       for dr, dc in DIRS
                       if 0 <= r + dr < n and 0 <= c + dc < n and grid[r + dr][c + dc] > 1}
                best = max(best, 1 + sum(size[i] for i in ids))
    return best
```

Saves `O(n^2)` space; destroys the input. Ask the interviewer before mutating.

### 9c. Union-Find (ties this problem to Group 07)

Give every land cell id `r*n+c`. Union each land cell with its **right** and
**down** land neighbor (checking those two directions from every cell covers every
adjacent pair exactly once). Extend the house `DSU` with a `size` array
(`self.size = [1]*n`, updated in `union`). Pass 2 is identical: for each water
cell, take the **distinct roots** among its land neighbors,
`candidate = 1 + sum(dsu.size[find(root)] for those roots)`.

When to prefer this over DFS/BFS labeling: when islands are also being **built up
incrementally** elsewhere in the same system (e.g. land is added over time) and you
already maintain a `DSU` for that — reuse it here instead of a fresh flood. For a
single static query, DFS/BFS labeling is simpler.

### The BFS↔DFS answer the interviewer wants

> "Both passes are `O(n^2)` regardless of BFS or DFS — the flood in Pass 1 and the
> neighbor scan in Pass 2 don't change complexity class. I'd use DFS for Pass 1
> (shorter), and mention BFS as the safe alternative for very large solid islands
> to avoid Python's recursion limit."

---

## 10. Complexity — derived step by step

**V and E:** node = a cell, `V = n^2` (grid is square here); edge = 4-neighbor
adjacency, `E ≈ 2n^2 = O(n^2)`.

**Time:**
- Pass 1 (labeling flood): identical analysis to Max Area of Island — every land
  cell is labeled exactly once, all floods together cost `O(n^2)`.
- Pass 2: outer double loop is `n^2`; for each water cell we look at ≤4 neighbors
  (`O(1)`) and sum over a set of size ≤4 (`O(1)`). So Pass 2 is `O(n^2)`.
- **Total: `O(n^2)`.** (Contrast the naive approach — "flip each 0, re-run a full
  flood-fill" — which is `O(n^2)` candidates `× O(n^2)` per flood `= O(n^4)`; the
  labeling trick removes that extra factor.)

**Space:**
- `label` grid: `O(n^2)`.
- `size` dict: at most `O(n^2)` entries (a checkerboard grid has up to `~n^2/2`
  single-cell islands).
- Recursion stack (DFS): `O(n^2)` worst case (one giant snake island).
- **Total: `O(n^2)`.**
- In-place variant (9b) removes the separate `label` array but is still `O(n^2)`
  overall because of `size` and the recursion stack.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| All land, no `0` anywhere | `best` initialized from Pass 1's `max(size.values())`; Pass 2 loop never triggers |
| All water | `size` is empty → `best = 0` from `default=0`; every water cell's candidate is `1` (no land neighbors) → answer `1` |
| Single cell `[[0]]` / `[[1]]` | → `1` / `1` |
| Two islands with **no** common water neighbor | Pass 2 never finds a cell touching both ids → best = larger single island + 1 (from an adjacent flip), never their sum |
| A water cell touching the **same** island via two directions (e.g. a "U" shape) | `neighbor_ids` is a `set` → counted once, not twice |
| `n = 1` | both passes run over a `1x1` grid correctly |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Not deduplicating neighbor ids.** Using a `list` instead of a `set`, or
      summing without dedup, double-counts an island touched from two directions
      (a classic "U"-shaped island around one water cell). Answer too large.
- [ ] **Forgetting to seed `best` from Pass 1.** If the grid is all land, `best`
      would stay `0` (or crash) because Pass 2 never runs — must be
      `max(size.values(), default=0)` computed *before* Pass 2.
- [ ] **Starting `next_id` at `0` or `1`.** Collides with water/land encoding if
      you mutate `grid` in place (9b) — `grid[r][c] == 1` would then also match a
      stamped island id `1`. Start at `2`.
- [ ] **`label`/`grid` check ordering** — testing `grid[r][c] == 1` without also
      checking "not already labeled" re-floods (wastes time, though the base case
      usually catches it) or, worse, re-adds to `size` with a fresh id, corrupting
      the size table.
- [ ] **`dfs` returns `None`** (same bug family as Max Area of Island) — missing a
      `return 0` or `return area`.
- [ ] **Square vs rectangular grid assumption.** This problem guarantees `n x n`;
      if you reuse this code for a rectangular grid, use `m, n` and bounds-check
      both independently.

**Narrate:** "My answer is bigger than the grid itself — I must be double-counting
an island. Let me check: am I using a `set` for `neighbor_ids`, or am I summing a
list where the same id appears twice because a water cell has two neighbors in the
same island?"

---

## 13. Learnings & Transfer

**The reusable core: label + probe.**

1. **Precompute:** flood every component once, giving each a stable `id` and
   caching whatever aggregate you need (`size` here; could be `sum`, `max value`,
   a boolean, ...).
2. **Probe:** for every *candidate change*, look only at its immediate neighbors'
   ids (`O(deg)`, not `O(V)`), deduplicate with a `set`, and combine the cached
   aggregates. This turns an `O(candidates × flood)` algorithm into
   `O(V + E) + O(candidates × deg)`.

This is one of the highest-value patterns in this repo — it comes back constantly
under the disguise "you may change one X, what's the best result?"

| Situation | How this transfers |
|---|---|
| "Flip one water cell to land, maximize island size" | exactly this problem |
| "Remove one edge, does the graph stay connected?" (bridges) | precompute discovery/low-link once (Group 15, Tarjan), instead of removing-and-re-checking each edge |
| "Add one flight route, minimize the new shortest path" | precompute all-pairs distances (Floyd-Warshall, Group 11) once, evaluate each candidate edge in `O(1)`: `min(dist[u][v], dist[u][x] + w + dist[y][v])` |
| "Which single node, if removed, disconnects the most pairs?" (articulation points) | precompute once via DFS (Group 15) instead of `O(V)` separate removals |
| "Given many queries 'which component is cell (r,c) in, and how big?'" | exactly Pass 1 here — label once, answer each query `O(1)` |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Generalize: you may flip up to **K** water cells (not just one). Maximize the resulting island size."

- **(b) Pattern:** flag it — this is no longer a clean `O(1)`-per-candidate probe.
  Choosing the *best set* of `K` cells to connect multiple islands is a
  combinatorial optimization (related to Steiner-tree-style problems), not a
  simple extension.
- **(c) Adapt:** for `K = 1` this problem is exact and optimal (label + probe). For
  general `K`, propose: (i) if `K` is small (≤ 3) and islands are few, brute-force
  over combinations of promising bridge cells; (ii) a greedy heuristic — repeatedly
  apply the `K=1` solution and re-run label+probe, `K` times (not guaranteed
  optimal, but a reasonable interview answer); (iii) note the exact version is
  equivalent to finding a minimum-cost way to connect a subset of islands using at
  most `K` "stepping stones", which smells like Steiner tree (NP-hard in general).
- **(d) Say:** "I can solve K=1 exactly with label+probe in O(n²). For general K I'd
  name it as combinatorial, and offer a greedy or bounded-search approximation
  rather than pretend there's a clean polynomial exact algorithm."

### Scenario 2 — "This is a live map-editing tool. As the user's cursor hovers over each water cell, show the resulting island size in real time, without lag."

- **(b) Pattern:** the same label+probe, but you need the **per-cell answer for
  every water cell**, not just the overall max.
- **(c) Adapt:** run Pass 1 once. Instead of tracking only `best` in Pass 2, store
  the candidate value for *every* water cell in a `hover_value` grid
  (`O(n^2)` extra space). A hover event is then an `O(1)` lookup — no
  recomputation as the mouse moves.
- **(d) Say:** "Precompute-once-answer-every-query — same trick as Scenario 4/5 of
  the earlier flood-fill problems, just materialize the whole answer grid instead
  of only the max."

### Scenario 3 — "Land is added and removed over time (e.g. flooding/erosion simulation). After each change, report the best possible single flip."

- **(b) Pattern:** dynamic connectivity. **Additions** are Union-Find's strength
  (`O(α(n))` amortized per union); **removals** are the hard part — classic DSU
  cannot undo a union efficiently.
- **(c) Adapt:** if all updates are known in advance, process them **offline in
  reverse**: start from the final state, and turn each "removal" into an
  "addition" as you replay backward, using Union-Find normally, recording answers,
  then reverse the recorded answer list. If updates must be handled truly online
  (arbitrary future removals unknown), say plainly that you'd need a dynamic
  connectivity structure (e.g. a link-cut tree or a fully-dynamic connectivity
  data structure) — beyond what a DSU offers.
- **(d) Say:** "DSU handles incremental *additions* beautifully; *deletions* need
  the offline-reverse trick, or a genuinely dynamic connectivity structure if
  online."

### Scenario 4 — "Instead of one flip, find the **minimum number of flips** needed to connect *all* islands into a single island."

- **(b) Pattern:** this becomes a **Minimum Spanning Tree over islands**, where the
  "distance" between two islands is the fewest water cells you'd need to flip to
  bridge them (their grid distance minus 1).
- **(c) Adapt:** label islands as in Pass 1. For every pair of islands, compute
  their shortest bridging distance — reuse the **Shortest Bridge** technique
  (multi-source BFS from one island's border toward the other, Group 02) or a
  single multi-source BFS from *all* land cells that records, for each water cell,
  which island reached it first and at what distance, letting you read off
  inter-island distances efficiently. Build a complete graph on islands with those
  distances as weights, then run **Kruskal or Prim** (Group 12) to find the
  minimum total flips connecting them all.
- **(d) Say:** "‘Connect everything at minimum cost’ is the MST signal — compute
  pairwise costs (here, via BFS distances between islands) and hand them to
  Kruskal/Prim."

### Scenario 5 — "Some islands are marked 'restricted' (owned by someone else). You may flip one water cell, but the result must not touch any restricted island."

- **(b) Pattern:** same label+probe, with a **filter** on which candidates count.
- **(c) Adapt:** mark each island's id as restricted or not (a `set` of restricted
  ids from Pass 1). In Pass 2, when building `neighbor_ids` for a water cell, skip
  it entirely (candidate invalid) if any neighboring id is restricted; otherwise
  score it normally.
- **(d) Say:** "Business-rule filters ride on top of label+probe for free — just
  reject or skip a candidate based on the labels touching it."

### Scenario 6 — "The grid is `10^5 x 10^5` but land covers under 0.01% of it, given as a list of `(r, c)` coordinates. Solve the same problem without allocating the full grid."

- **(b) Pattern:** sparse grid — same as Number of Islands' Scenario 2.
- **(c) Adapt:** store land cells in a `dict` mapping `(r, c) -> island_id` (instead
  of a 2D `label` array). Flood using that dict (neighbors are just coordinate
  math; "in bounds" no longer needs an array — just check the coordinate is a valid
  index if the problem still bounds it). For Pass 2, you cannot iterate "every
  water cell" (there could be `10^10` of them) — instead, iterate only the
  **neighbors of land cells** (at most `4 × (number of land cells)` candidate water
  cells), building `neighbor_ids` for just those. Complexity becomes `O(L)` where
  `L` = number of land cells, independent of the grid's nominal size.
- **(d) Say:** "Sparse grid ⇒ don't enumerate the whole grid at all; enumerate
  candidates only from the land cells' neighborhoods."

---

## 15. Flashcards

**Q:** The core technique this problem teaches, in one line?
**A:** **Label + probe** — flood every component once with a stable id and a
cached aggregate (size), then answer every "what if I changed this one cell"
candidate in `O(1)` using only its neighbors' ids.

**Q:** Why is a plain `seen` set not enough here, unlike Number of Islands?
**A:** You need to know *which* island a neighbor belongs to (to look up its size
and to deduplicate), not just *that* it's visited — that requires an id, not a
boolean.

**Q:** Why must `neighbor_ids` be a `set`, not a list?
**A:** A water cell can touch the same island from two different directions (a "U"
shape); summing a list would double-count that island's size.

**Q:** How do you handle "the grid is all land, no water to flip"?
**A:** Seed `best = max(size.values(), default=0)` **before** Pass 2, from Pass
1's results.

**Q:** Time and space, with the naive-approach comparison?
**A:** `O(n^2)` time, `O(n^2)` space. Naive "flip each 0 and re-flood" would be
`O(n^2) × O(n^2) = O(n^4)`; labeling removes that extra factor by making each
candidate `O(1)`.

**Q:** Why start island ids at `2`, not `0` or `1`?
**A:** `0`/`1` already mean water/land in the input; starting at `2` avoids
ambiguity, especially in the in-place-mutation variant.

**Q:** "Connect ALL islands with the minimum number of flips" — which pattern?
**A:** Minimum Spanning Tree over islands: compute pairwise bridging distances
(via BFS, like Shortest Bridge), then run Kruskal/Prim (Group 12).

**Q:** Land removed over time (not just added) — why is that harder for
Union-Find, and the standard workaround?
**A:** DSU supports `union` (additions) in ~O(1) but not un-union (removals). If
all updates are known in advance, process them offline in reverse, turning
removals into additions.

---

## Appendix — Tejas's Thought-Process Notes

Written in your own words while working through *why* the label+probe idea is the
right move — this is the same reasoning as sections 4 and 13 above, in your voice.
Keeping it because "why did I abandon the naive approach" is exactly what an
interviewer wants you to narrate out loud, and your own phrasing is what you'll
actually remember under pressure.

**1. Identify the bottleneck in the naive solution**

What you noticed: flipping a `0` to a `1` merges adjacent component areas.

Why the naive way is slow: re-running DFS/BFS for every single `0` repeatedly
recounts the exact same islands of `1`s over and over again. You are throwing away
work you already did.

**2. Shift from "recompute" to "precalculate & look up"**

The core realization: an island of `1`s doesn't change its size just because you
look at a different neighboring `0`.

The fix: calculate the area of every connected island of `1`s once beforehand, and
store it so any adjacent `0` can query it instantly (`O(1)` lookup time).

**3. Resolve the overlap problem (the need for island IDs)**

The dilemma: if a `0` has two neighbors belonging to `1`s, how do you know if
those neighbors belong to two different islands, or are just two different sides
of the same island?

The solution: assign a unique ID (e.g. `2, 3, 4, ...`) to each island during the
precalculation pass. Either mutate the grid in place — replace the `1`s of the
first island with `2`, the second island with `3`, etc. — or keep a separate
mapping. Store the sizes in a hash map: `{2: area1, 3: area2, ...}`.

**4. Build the final recipe**

- **Pass 1 (precompute):** traverse the grid. When you hit an unvisited `1`, run a
  standard DFS/BFS to find its total size and mark all its cells with a unique ID.
  Save `{id: area}` in a hash map.
- **Pass 2 (query):** traverse the grid again. When you hit a `0`: look at its 4
  orthogonal neighbors; collect their neighbor IDs into a hash **set** (this
  automatically prevents double-counting the same island); potential size =
  `1 + sum(map[id] for id in unique_neighbor_ids)`; track the maximum potential
  size found.
- **Pass 3 (edge case):** check if the grid had no `0`s at all (all `1`s), in
  which case the answer is `N × N`.

**Matches the primary solution exactly.** One small note on "Pass 3": in the code
above it isn't a separate traversal — it falls out for free by seeding
`best = max(size.values(), default=0)` from Pass 1's results *before* Pass 2 runs,
so an all-land grid returns the right answer without a dedicated third loop. Same
idea, one fewer pass.
