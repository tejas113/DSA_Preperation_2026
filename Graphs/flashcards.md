# Flashcards — all problems, one place

How to use: cover the **A** line, read the **Q**, say your answer out loud, then
check. Do a full pass every day. On Day 5 do two passes.

Cards are grouped by problem in the order we cover them. Each problem's cards are
also at the bottom of that problem's `.md` file.

---

## Concept cards (do these first)

**Q:** BFS vs DFS — which for "shortest / fewest steps" in an unweighted graph?
**A:** BFS. The first time BFS reaches a node it's via the fewest edges. DFS gives
*a* path, not the shortest.

**Q:** BFS data structure and the golden rule?
**A:** A `deque` (FIFO). Mark a node `seen` when you **enqueue** it, never when you
dequeue it.

**Q:** DFS data structure?
**A:** The call stack (recursion) or an explicit `list` used as a stack (LIFO).

**Q:** Time & space of plain BFS/DFS?
**A:** `O(V + E)` time, `O(V)` space. Each node processed once, each edge scanned a
constant number of times.

**Q:** Why isn't BFS/DFS `O(V²)` when each node loops over its neighbors?
**A:** The *sum* of all neighbor-list lengths is `2E` (undirected). So neighbor
scanning is `O(E)` total, not `O(V)` per node × `V`.

**Q:** Grid as a graph: V, E, and the resulting complexity?
**A:** `V = m*n` cells, `E ≈ 2mn`. So BFS/DFS on a grid is `O(m*n)` time and space.

**Q:** Default representation for a non-grid graph, and how to build it?
**A:** Adjacency list = `defaultdict(list)`. `for u, v in edges: graph[u].append(v); graph[v].append(u)` (drop the second line if directed).

**Q:** When adjacency **matrix** instead of list?
**A:** Dense graph (`E ≈ V²`), need `O(1)` edge lookup, small `V`, or the algorithm
is Floyd-Warshall.

**Q:** Multi-source BFS — the one change from normal BFS?
**A:** Push **all** sources into the queue (all marked seen) *before* the loop.
Gives distance to the *nearest* source in one `O(V+E)` pass.

**Q:** Counting connected components — the skeleton?
**A:** Loop all node ids; if a node is unseen, `count += 1` and flood (BFS/DFS) to
mark its whole component.

**Q:** The interview script for stating complexity?
**A:** "A node is ___ so V = ___; an edge is ___ so E = ___. Build adjacency
`O(V+E)`. Traversal visits each node once, each edge once, `O(V+E)`. Extra work per
step is ___. Space = adjacency + visited + queue = `O(V+E)`."

**Q:** Fix for Python `RecursionError` in a deep DFS?
**A:** `import sys; sys.setrecursionlimit(10**6)` at the top, or switch to the
iterative stack version.

---

## 01 · Number of Islands (LeetCode 200)

**Q:** Trigger words for the grid flood-fill pattern?
**A:** 2D grid + "island/region/blob/area", "connected horizontally/vertically",
"how many groups" / "largest", and *no* "shortest path" / "distance".

**Q:** One-line skeleton for counting components on a grid?
**A:** Double-loop every cell; on an unvisited target cell, `count += 1` and flood
(DFS/BFS) to mark the whole blob.

**Q:** Time and space, with derivation?
**A:** `O(m*n)` both. Outer loop `m*n`; `seen` check makes total flood work
`O(m*n)`, not squared. Space = `seen` + recursion/queue, `O(m*n)` worst case.

**Q:** Classic silent bug here?
**A:** `grid[r][c] == 1` (int) when cells are `"1"` (string). Also indexing before
the bounds check — negative index wraps to the last row.

**Q:** When Union-Find instead of flood fill for islands?
**A:** Land/edges added incrementally with a count query after each (Number of
Islands II), or merging results across partitions.

**Q:** DFS vs BFS here — the interview answer?
**A:** Both `O(m*n)`. DFS shorter but risks recursion-limit on a huge solid
island; BFS (explicit queue) has no depth limit. Pick DFS, mention the switch.

**Q:** 10^6 × 10^6 mostly-water grid given as land coordinates — approach?
**A:** Put land cells in a set; DFS/BFS over the set (neighbors = offsets present
in the set). Time `O(L)`, independent of dimensions.

**Q:** "You may flip one water cell to land — maximize island size." Which problem/technique?
**A:** Making a Large Island: label + size every island in pass 1, then for each
water cell sum distinct neighbor-island sizes + 1 in pass 2.

---

## 01 · Flood Fill (LeetCode 733)

**Q:** What makes Flood Fill the simplest member of Group 01?
**A:** You're given the seed pixel → no outer loop. Just one flood.

**Q:** Why doesn't Flood Fill need a `visited` set?
**A:** Recoloring a pixel makes it stop matching `start_color`, so the match test
doubles as the visited check.

**Q:** The #1 bug in Flood Fill and its symptom?
**A:** Forgetting the `start_color == color` guard → infinite recursion
(`RecursionError`/TLE): painting a color onto itself never terminates.

**Q:** Why capture `start_color` before calling `dfs`?
**A:** The first recolor changes `image[sr][sc]`; reading it later gives the wrong
original color.

**Q:** Time and space?
**A:** `O(m*n)` time (each region pixel once), `O(m*n)` space worst case for the
call stack / queue. No extra visited structure.

**Q:** Tolerance version ("fill colors within `t` of the original") — what breaks?
**A:** Mutation no longer forces the match test false → reintroduce an explicit
`visited` set and compare to the original start color.

**Q:** Flood Fill vs Word Search grid DFS?
**A:** Flood Fill never un-marks. Word Search un-marks on the way back
(backtracking) so cells can be reused by other paths.

---

## 01 · Max Area of Island (LeetCode 695)

**Q:** What does this add on top of Number of Islands?
**A:** The flood **returns an int** — `area = 1 + sum(dfs(child))` — and the outer
loop keeps `best = max(best, area)`.

**Q:** Symptom of a return-value bug here?
**A:** `TypeError: int + NoneType` — a base case missing `return 0`, or the
function missing `return area`.

**Q:** Cell type in LeetCode 695?
**A:** Integers `1` / `0`. (Number of Islands used the strings `"1"` / `"0"` —
always check.)

**Q:** Why return the area instead of a `nonlocal` accumulator?
**A:** No `nonlocal` to forget, no per-island reset, and `1 + sum(children)`
composes directly.

**Q:** Time and space?
**A:** `O(m*n)` both. Outer loop `m*n`; `seen` check keeps total flood `O(m*n)`;
recursion/queue `O(m*n)` worst case.

**Q:** Perimeter-instead-of-area — the one change?
**A:** Per cell, base value = number of its 4 sides facing water/border; still
`base + sum(children)`.

**Q:** "Number of distinct island shapes" — technique?
**A:** Record each cell's offset from the island's first cell; sort → tuple → add
to a set. `len(set)`. Rotations/reflections: canonicalize over all 8 transforms.

**Q:** Many "area of island containing (r,c)?" queries — approach?
**A:** Preprocess once: label every cell with an island `id`, store `size[id]`.
Each query `O(1)`.

**Q:** General shape this problem teaches (also for trees)?
**A:** "Return an aggregate from recursion": `f(node) = base + combine(f(child)…)`
— max-depth, diameter, path-sum, subtree-size.

---

## 01 · Making a Large Island (LeetCode 827, supplementary)

**Q:** The core technique this problem teaches, in one line?
**A:** **Label + probe** — flood every component once with a stable id and a
cached aggregate (size), then answer every "what if I changed this one cell"
candidate in `O(1)` using only its neighbors' ids.

**Q:** Why is a plain `seen` set not enough here, unlike Number of Islands?
**A:** You need to know *which* island a neighbor belongs to (to look up its size
and dedupe), not just *that* it's visited — that requires an id.

**Q:** Why must `neighbor_ids` be a `set`, not a list?
**A:** A water cell can touch the same island from two directions (a "U" shape);
summing a list would double-count that island's size.

**Q:** How do you handle "grid is all land, no water to flip"?
**A:** Seed `best = max(size.values(), default=0)` **before** Pass 2, from Pass
1's results.

**Q:** Time/space, and the naive-approach comparison?
**A:** `O(n^2)` time and space. Naive "flip each 0, re-flood" is `O(n^4)`;
labeling makes each candidate `O(1)`.

**Q:** Why start island ids at `2`, not `0`/`1`?
**A:** `0`/`1` already mean water/land in the input; `2+` avoids ambiguity,
especially when mutating the grid in place.

**Q:** "Connect ALL islands with minimum flips" — which pattern?
**A:** MST over islands: pairwise bridging distances (BFS, like Shortest Bridge),
then Kruskal/Prim.

**Q:** Land removed over time — why is that hard for Union-Find?
**A:** DSU supports `union` (additions) cheaply but not un-union (removals). If
updates are known upfront, process them offline in reverse.

---

## 02 · Walls and Gates (LeetCode 286, premium)

**Q:** The one change from single-source to multi-source BFS?
**A:** Seed the queue with **every** source, all at distance 0, before the main
loop starts.

**Q:** Why does the first ripple to reach a cell always come from the nearest
source?
**A:** BFS explores in non-decreasing distance order, so nothing later beats a
distance that already claimed the cell.

**Q:** Multi-source BFS time vs "BFS from each source, take the min"?
**A:** Multi-source: `O(m*n)`, one pass. Naive per-source: `O(sources × m*n)`.

**Q:** Visited-marking trick borrowed from Flood Fill?
**A:** Overwriting the sentinel (`INF`) with the real distance doubles as the
visited check — no separate `seen` set.

**Q:** Why is DFS the *wrong* tool here, not just slower?
**A:** Without an explicit "only overwrite if shorter" relaxation it isn't even
correct (ripples can overwrite out of order); with relaxation it's correct but can
revisit cells many times, losing `O(m*n)`.

**Q:** Doors with walk-time ≠ 1 — what changes?
**A:** Plain BFS breaks. Switch to multi-source Dijkstra (heap) or 0-1 BFS (deque)
for small integer weights.

**Q:** Classic sentinel bug in this exact problem?
**A:** Comparing against the wrong "empty room" constant — must be the literal
`2147483647`, not `float("inf")`.

---

## 02 · 01 Matrix (LeetCode 542)

**Q:** How does this differ from Walls and Gates?
**A:** No walls; and the sentinel can't be the input's own `1` (a cell's real
answer can also be `1`) — use a separate `dist` grid seeded with `-1`.

**Q:** Non-BFS alternative here, and its complexity?
**A:** Two-pass DP (distance transform): forward sweep looks up+left, backward
sweep looks down+right. `O(m*n)` time, `O(1)` extra space.

**Q:** Why does the two-pass DP break if walls are added?
**A:** A wall can force a detour whose shape two fixed-direction sweeps can't
always capture in two passes; BFS makes no such assumption.

**Q:** Multiple source *types*, need only the overall nearest — one BFS or many?
**A:** One — merge all types into a single queue. Separate passes only when you
need a *per-type* breakdown.

**Q:** Weighted cells/edges — what replaces BFS?
**A:** Multi-source Dijkstra (heap), or 0-1 BFS (deque) for small integer
weights. The two-pass DP does not generalize to weights.

**Q:** How to get the actual shortest path, not just its length?
**A:** Track a `parent` pointer per cell during BFS relaxation; walk it backward
from any cell to a `dist == 0` source.

---

## 02 · Rotting Oranges (LeetCode 994)

**Q:** How does this differ from Walls and Gates / 01 Matrix in what it returns?
**A:** Those return each cell's own distance. This returns *one number* — total
rounds (max distance reached) — plus a possible `-1` for impossible.

**Q:** The #1 bug in this problem?
**A:** Off-by-one from an extra silent round: `while q:` alone processes one more
ring after the last fresh orange already rotted. Fix: `while q and fresh > 0:`.

**Q:** How does the timestamped-queue alternative avoid that bug structurally?
**A:** Stores `(cell, minute)` per entry; `minutes = t + 1` is only set when a
cell actually rots — no "was this round wasted?" bookkeeping to get wrong.

**Q:** How do you detect the impossible case?
**A:** Track a `fresh` counter/set; if it's not zero/empty after the BFS, return
`-1`.

**Q:** Why is DFS the wrong tool here?
**A:** Without careful "only update if shorter" relaxation, DFS can rot a cell via
a longer path first, inflating the minute count.

**Q:** Different infection speeds (weights ≠ 1) — what replaces plain BFS?
**A:** Multi-source Dijkstra (heap), or a bucket queue / Dial's algorithm for
small integer weights — stays `O(V+E)`.

**Q:** Sources appearing at different start times — why does a plain deque break?
**A:** FIFO insertion order no longer matches true chronological order once
sources don't all start at 0 — need a heap or time-indexed buckets.

---

## 02 · Shortest Bridge (LeetCode 934, supplementary)

**Q:** What two techniques does this problem combine, and why both?
**A:** DFS/BFS flood to fully *identify* one island (pure reachability), then
multi-source BFS from that entire island through water to the other island
(needs BFS specifically for the shortest-distance guarantee).

**Q:** How does this differ from Making a Large Island's "best single flip"?
**A:** That's label + probe (precompute sizes, evaluate every water cell O(1),
no path search). This is a genuine shortest-path search between two *specific*
islands, and the flip count isn't capped at one.

**Q:** Why iterative DFS (stack), not the usual recursive default, for Phase 1?
**A:** One island can be up to `n*n = 10^4` cells (`n ≤ 100`) — a long
snake-shaped island could exceed Python's default recursion limit (~1000).

**Q:** What does distance `d` mean when you find an island-B neighbor, and why
return `d` (not `d±1`)?
**A:** `d` = number of water cells already claimed to reach the current frontier
cell; its neighbor is already land, needing no further flip, so `d` is the total.

**Q:** Sentinel-safety lesson reused here?
**A:** The claim marker `2` can't collide with the input's own `0`/`1` — same
principle as 01 Matrix's `-1` sentinel.

**Q:** This problem's technique feeds into which later scenario?
**A:** "Connect ALL islands at minimum total cost" (MST over islands) — this
problem computes the pairwise distances MST needs as edge weights.

**Q:** Weighted water cells (deep water costs more) — what changes?
**A:** Phase 1 unaffected. Phase 2 becomes multi-source Dijkstra (heap) instead
of plain BFS (deque).

---

## 03 · Pacific Atlantic Water Flow (LeetCode 417)

**Q:** The core trick this problem introduces?
**A:** Flood **from the boundary inward** using the **reversed** relationship,
instead of simulating forward from every cell — `O((m*n)²)` → `O(m*n)`.

**Q:** Why must the flow condition be reversed for the boundary flood?
**A:** Real rule: flow to a neighbor with `height <= mine` (downhill). Walking
backward from the ocean: "which neighbor could have sent water here" is
`height[neighbor] >= height[mine]` — the inequality flips.

**Q:** Why `>=` and not strict `>`?
**A:** The problem allows flow across equal heights (flat ground); dropping "or
equal" breaks plateau connectivity.

**Q:** How is the final answer computed from the two floods?
**A:** Set intersection: `pacific & atlantic`.

**Q:** Time/space vs the naive approach?
**A:** `O(m*n)` (two multi-source BFS floods + intersection) vs naive
`O((m*n)²)` per-cell simulation.

**Q:** Single-row/column grid — what's special?
**A:** Row 0 *is* row `m-1` (or col 0 *is* col `n-1`), so every cell is a source
for both oceans directly — the whole grid trivially qualifies.

**Q:** When does "reverse the condition" become unnecessary?
**A:** When the relation is symmetric (e.g. `abs(height diff) <= T`) — forward
and backward search use the identical condition.

---

## 03 · Surrounded Regions (LeetCode 130)

**Q:** How does this differ from Pacific Atlantic?
**A:** One boundary instead of two; the "connected to" relation is symmetric (no
reversal needed); the answer is the **complement** of one flood, not an
intersection of two.

**Q:** The core trick — find "boxed in" regions without checking each one?
**A:** Flood from every border-touching `'O'` (multi-source); everything the
flood doesn't reach was boxed in by definition.

**Q:** What does the `'#'` placeholder do?
**A:** Doubles as "safe" and "visited" — same mutation-as-visited-mark trick as
every earlier problem in Groups 01–02.

**Q:** The #1 bug in this problem?
**A:** Forgetting to restore `'#'` back to `'O'` in the cleanup pass — leaves
placeholder characters instead of the required `'O'`/`'X'`.

**Q:** Time and space, with derivation?
**A:** `O(m*n)` both — seed scan `O(m+n)`, BFS visits each `'O'` once, cleanup
scan `O(m*n)`. No separate visited structure needed.

**Q:** Is the naive "flood every region, check border-touch per region"
approach asymptotically worse?
**A:** No — still `O(m*n)`. Just more bookkeeping per region for no benefit.

**Q:** How does this generalize if "the border" isn't the literal grid edge?
**A:** Seed the flood with whatever fixed cell set the problem defines as
"safe" — the algorithm doesn't care what that set is.

---

## 04 · Find if Path Exists in Graph (LeetCode 1971)

**Q:** The two-step ritual every non-grid graph problem starts with?
**A:** (1) Build an adjacency list from the edge list. (2) Run the BFS/DFS you
already know, using `graph[node]` instead of grid neighbors.

**Q:** Why does `source == destination` need no special case?
**A:** BFS starts with `source` in the queue; the first pop already checks
`node == destination`, immediately true.

**Q:** Time and space, with derivation?
**A:** `O(V + E)` both — adjacency list built in `O(E)`, BFS/DFS visits each
node once and each edge a constant number of times.

**Q:** When does Union-Find beat a fresh BFS/DFS here?
**A:** Many queries against a static graph, or edges arriving incrementally —
precompute once (`O(E α(V))`), each query/update near-`O(1)`.

**Q:** Why doesn't Union-Find work for directed reachability?
**A:** DSU models symmetric "same group" equivalence classes; can't represent
one-way ("A reaches B but not vice versa") relationships.

**Q:** Recursion risk in this exact problem?
**A:** `n` up to `2×10^5` — a long chain graph recursed via DFS can exceed
Python's default recursion limit. Prefer BFS or iterative DFS.

**Q:** Weighted "reachable within budget B" — which tool applies?
**A:** Dijkstra/Bellman-Ford (Groups 10/11) — compute cheapest cost to
destination, compare to B.

---

## 05 · Clone Graph (LeetCode 133)

**Q:** The core trick of this problem, in one line?
**A:** An old-node → new-node map that is simultaneously the visited set **and**
the literal output being constructed.

**Q:** The single most important ordering rule, and what breaks without it?
**A:** Register the new clone in the map **before** recursing into its
neighbors. Skip this and any cycle causes infinite recursion.

**Q:** The sneaky bug that "looks" correct but isn't?
**A:** Appending the *original* neighbor object instead of its clone — looks
fine by value, but shares references with the input, so it isn't a real deep
copy.

**Q:** Why is recursion depth a non-issue here, unlike several earlier grid
problems?
**A:** The constraint caps the graph at 100 nodes — check actual constraints
rather than reflexively assuming recursion is risky.

**Q:** Time and space, with derivation?
**A:** `O(V + E)` time (each node cloned once, each edge wired once), `O(V)`
space (the map holds one entry per node; that's also effectively the output).

**Q:** How does this generalize to Copy List with Random Pointer (LC 138)?
**A:** Identical old→new map technique; two pointers per node (`next`,
`random`) instead of a variable-length neighbor list.

**Q:** How do you actually *test* that a clone is deep, not shallow?
**A:** Traverse both graphs and compare vals/shape (never `==` on `Node`
objects), and separately confirm none of the cloned objects are `is`-identical
to any original.

---

## Concept · Cycle detection & topological sort (concepts/06, concepts/07)

**Q:** The #1 mistake in directed cycle detection?
**A:** Using one `visited` set — re-reaching an already-fully-explored node via
a different path is normal in a DAG, not a cycle. Need 3 colors (white/gray/
black); only a **gray** node signals a cycle.

**Q:** Undirected cycle detection — two techniques?
**A:** DFS with a `parent` arg (seeing a visited non-parent neighbor = cycle),
or Union-Find (an edge whose endpoints already share a root = cycle).

**Q:** Kahn's algorithm — the core idea?
**A:** Repeatedly remove indegree-0 nodes, decrementing neighbors' indegree. If
you can't remove every node, what's left is a cycle. Doubles as topological sort
(the removal order) and cycle detection (`processed != n`).

**Q:** DFS post-order topological sort — why reverse the finish order?
**A:** A node finishes only after everything reachable from it does, so
reversing puts each node before everything it depends on.

**Q:** Time/space for topological sort (either method)?
**A:** `O(V + E)` time, `O(V + E)` space.

---

## 06 · Course Schedule (LeetCode 207)

**Q:** How does "can finish all courses" reduce to a graph question?
**A:** Directed cycle detection — a valid order exists iff the prerequisite
graph has no cycle.

**Q:** Edge direction for pair `[a, b]` ("a requires b")?
**A:** `b -> a` — `graph[b].append(a)`, `indegree[a] += 1`. Reversing this is
the most common bug.

**Q:** How does Kahn's algorithm detect the cycle here?
**A:** Cyclic courses can never reach indegree 0; `processed < numCourses` at
the end means a cycle exists.

**Q:** Time and space?
**A:** `O(V + E)` both.

**Q:** "Also give me a valid order" — what changes?
**A:** Nothing algorithmically — keep the `order` list Kahn's already builds
instead of discarding it (Course Schedule II).

**Q:** Per-course durations, minimize total time, unlimited parallelism?
**A:** Longest path in a DAG: topological order + DP,
`finish_time[node] = duration[node] + max(finish_time[prereq])`.

---

## 06 · Course Schedule II (LeetCode 210)

**Q:** How does this differ from Course Schedule?
**A:** One line — keep the `order` list Kahn's builds (the dequeue sequence);
return `[]` if `len(order) != numCourses`.

**Q:** Why is the dequeue sequence automatically a valid topological order?
**A:** A node is enqueued only once its indegree hits 0 — every prerequisite was
already dequeued (and appended) before it.

**Q:** Is the topological order unique?
**A:** No — any valid order is accepted. For a *specific* one (e.g. lex
smallest), change the queue's selection rule (min-heap), not the algorithm.

**Q:** DFS post-order version — the two easy-to-get-wrong details?
**A:** Append on *finish* (post-order), not on entry; and **reverse** the
finished list at the end.

**Q:** How should you test this, given non-unique output?
**A:** Validate the property (all courses present once, every prerequisite
before its dependent), not equality against one fixed list.

**Q:** "Lexicographically smallest valid order" — the change?
**A:** Swap the FIFO `deque` for a min-heap; `O((V+E) log V)`.

**Q:** Package-manager "install order for only what's needed" — the two steps?
**A:** (1) Reachability to find the needed transitive-dependency subset minus
already-installed; (2) topological sort restricted to that subset.

---

## 06 · Alien Dictionary (LeetCode 269, premium)

**Q:** What's the "new" work vs Course Schedule II?
**A:** Building the graph. Compare **adjacent** words; the **first** position
where they differ gives edge `w1[i] -> w2[i]`.

**Q:** Why only adjacent word pairs, and why only the first differing char?
**A:** The list is already sorted — adjacent pairs + topological transitivity
give all the info. Chars after the first difference are unconstrained by that
pair.

**Q:** The two independent ways the answer can be `""`?
**A:** (1) A cycle (contradictory facts). (2) Invalid prefix — a longer word
before its own prefix (`["abc","ab"]`).

**Q:** Why initialize `indegree` for every character, not just ones with edges?
**A:** A letter with no constraints still appears in the output; if not in
`indegree` at 0, it's never enqueued/emitted.

**Q:** The double-counting bug?
**A:** The same first-difference letter pair can occur in multiple adjacent word
pairs — guard `indegree[...] += 1` with `if w2[i] not in graph[w1[i]]`.

**Q:** Time and space?
**A:** `O(total characters)` = `O(W*L)` time (dominated by reading input),
`O(A²)` graph space (`≈ O(1)` for a bounded alphabet).

**Q:** How does "rank players from match results" relate?
**A:** It's this problem minus graph construction — each "X beat Y" is already a
directed edge; topological sort = the ranking, a cycle = inconsistent results.

---

## 06 · Minimum Height Trees (LeetCode 310, supplementary)

**Q:** What is it, in one line?
**A:** Find the 1 or 2 **center** nodes of an undirected tree by **leaf-peeling**
— repeatedly remove all degree-1 nodes, layer by layer, until ≤ 2 remain.

**Q:** Why is the answer always 1 or 2 nodes?
**A:** The optimal root is the middle of the tree's diameter — one node if the
diameter has an even number of edges, two if odd.

**Q:** How is leaf-peeling related to Kahn's algorithm?
**A:** Same "remove the boundary inward" idea, for undirected trees: peel
degree-1 nodes instead of indegree-0 nodes.

**Q:** The two must-freeze / must-guard details?
**A:** Freeze `len(leaves)` before each round (don't peel newly-made leaves that
round); special-case `n <= 2` (a lone node has degree 0, never a "leaf").

**Q:** Only append a new leaf when its degree becomes exactly what?
**A:** `== 1`. A node hitting degree `0` must not be re-queued.

**Q:** Time/space vs naive?
**A:** `O(n)` both. Naive "BFS from every node" is `O(n²)`.

**Q:** The 2-BFS tree-diameter trick?
**A:** BFS from any node → farthest `u`; BFS from `u` → farthest `v`; `u..v` is
a diameter. MHT roots are its middle 1–2 nodes.

**Q:** "Center by height" vs "centroid by size"?
**A:** MHT minimizes max *distance* (leaf-peeling / diameter midpoint). Centroid
minimizes largest *component* after removal (subtree-size DP). Different centers.

---

## 06 · Longest Increasing Path in a Matrix (LeetCode 329, supplementary)

**Q:** Why does memoized DFS here need **no** visited set or 3-color scheme?
**A:** Strictly-increasing moves make a cycle (`a<b<...<a`) impossible — the
graph is a DAG by construction.

**Q:** The recurrence?
**A:** `f(r,c) = 1 + max(f(strictly-greater 4-neighbor))`, or `1` if none.
Answer = `max(f)` over all cells.

**Q:** Why does `memo[r][c] = 0` work as the "not computed" sentinel?
**A:** Real answers are always `>= 1`, so `0` can't collide.

**Q:** What breaks if you change `>` to `>=`?
**A:** Equal adjacent cells form cycles → not a DAG → memoized DFS can
infinite-loop. Fix: Union-Find the equal-valued regions into super-nodes first.

**Q:** Recursion-depth caveat + two fixes?
**A:** A 200×200 monotone grid recurses ~40k deep. Fix: `sys.setrecursionlimit`,
or the iterative Kahn's layer-peeling version.

**Q:** Time and space?
**A:** `O(m*n)` both. Memo makes each cell compute once; without it, exponential.

**Q:** Relation to Longest Increasing Subsequence?
**A:** LIS is the 1D cousin. This is 2D, adjacent-moves-only, `O(m*n)` DAG-DP
(the `O(n log n)` LIS trick doesn't apply).

**Q:** "Max-SUM increasing path instead of longest" — the change?
**A:** One line: `best[r][c] = matrix[r][c] + max(0, max(best[greater neighbor]))`.
Same DAG, different accumulator.

---

## Concept · Union-Find (DSU)

**Q:** What does DSU do, and how fast?
**A:** "Same group?" (`find(a) == find(b)`) and "merge groups" (`union`), both
amortized `O(α(n)) ≈ O(1)` with path compression + union by rank.

**Q:** The killer idiom?
**A:** `union(a, b)` returns `False` ⟺ `a`, `b` already connected ⟺ edge closes a
cycle / is redundant.

**Q:** Counting components with DSU?
**A:** Start `count = n`; every `union` that returns `True` does `count -= 1`.

**Q:** When does DSU beat BFS/DFS flood-fill?
**A:** Incremental edges (connectivity as you go), many "connected?" queries on a
fixed graph, "first cycle-closing edge," Kruskal's MST.

**Q:** When can DSU *not* help?
**A:** Directed reachability (DSU is undirected-only), needing the actual
path/distance, or edges being removed (DSU can't un-merge).

**Q:** Non-integer elements (strings)?
**A:** Remap each distinct element to an integer id via a dict, size the DSU to
the id count, translate.

---

## 07 · Redundant Connection (LeetCode 684)

**Q:** The core idea?
**A:** Process edges in order with a DSU; return the first edge whose `union`
returns `False` (endpoints already connected → it closes the cycle).

**Q:** Why is the first `union` failure automatically "the last cycle edge in
input order"?
**A:** Every other cycle edge was processed earlier and unioned successfully; the
failure is the one that completes the loop when the scan reaches it.

**Q:** DSU size for `1..n`-indexed nodes?
**A:** `DSU(n + 1)`, index `0` unused (or remap to `0..n-1`).

**Q:** Time and space?
**A:** `O(n · α(n)) ≈ O(n)` time, `O(n)` space.

**Q:** The `O(E²)` alternative and why DSU wins?
**A:** DFS/BFS per edge to test "already connected." DSU makes each test
`O(α(V))` → `O(E)` overall.

**Q:** How does the *directed* version (LC 685) differ?
**A:** Three cases — a node with two parents, a cycle, or both. Find the
two-parent candidate edges first, then use DSU to decide which to drop.

---

## 07 · Graph Valid Tree (LeetCode 261, premium)

**Q:** A graph is a valid tree iff...?
**A:** Connected **and** acyclic. Equivalently: exactly `n - 1` edges + **any
one** of {connected, acyclic}.

**Q:** The "any two imply the third" rule?
**A:** For `n` nodes, any two of {connected, acyclic, exactly `n-1` edges} imply
the third. Check the two cheapest: edge count (`O(1)`) + no-cycle (DSU).

**Q:** The primary check sequence?
**A:** `len(edges) != n - 1` → `False`. Else DSU over all edges; any `union`
failure → `False`; otherwise `True`.

**Q:** Why does `n-1` edges + no cycle guarantee connectivity?
**A:** If it were disconnected, some component would have too many edges for its
size → a cycle → contradiction.

**Q:** Index base here vs Redundant Connection?
**A:** Graph Valid Tree is **0-indexed** → `DSU(n)`. Redundant Connection is
1-indexed → `DSU(n + 1)`.

**Q:** Time and space?
**A:** `O(n · α(n)) ≈ O(n)` time, `O(n)` space.

**Q:** Given it's a tree, how do you get `dist(a, b)`?
**A:** `depth[a] + depth[b] - 2·depth[LCA(a,b)]` after rooting + binary-lifting
LCA prep. DSU can't do distances.

---

## 07 · Number of Connected Components (LeetCode 323, premium)

**Q:** The idiom for counting components with DSU?
**A:** `count = n`; for each edge, `count -= 1` **only if** `union` returned
`True`.

**Q:** Why decrement only on a successful `union`?
**A:** A `union` returning `False` connects two nodes already in the same
component — no merge, no change to the count.

**Q:** Do isolated nodes count as components?
**A:** Yes — `count` starts at `n`; a node with no edges is never merged.

**Q:** Time and space?
**A:** `O(E · α(n)) ≈ O(E)` time, `O(n)` space.

**Q:** Edges to connect everything into one component?
**A:** `components - 1`.

**Q:** Edges to remove to make the graph a forest?
**A:** The count of `union` calls that returned `False` (= `E - (n - components)`).

**Q:** The three faces of DSU across Group 07?
**A:** Count groups (this), find the cycle-closing edge (Redundant Connection),
validate a tree (Graph Valid Tree) — same `union` loop, different signal.

---

## 07 · Number of Provinces (LeetCode 547)

**Q:** How does this differ from Number of Connected Components?
**A:** Only the input format — an adjacency matrix. Edges are the `1`s; scan the
upper triangle (`j > i`) since it's symmetric.

**Q:** The algorithm?
**A:** `count = n`; for each `1` at `(i, j)` with `j > i`, if `union(i, j)` →
`True`, `count -= 1`.

**Q:** Time and space?
**A:** `O(n² · α(n)) ≈ O(n²)` time (dominated by scanning the matrix), `O(n)`
space.

**Q:** Sparse `50k×50k` given as `(i, j)` pairs — what changes?
**A:** Don't build a dense matrix; treat the pairs as an edge list, `union` each
— `O(E)` not `O(n²)`.

**Q:** Per-city province label?
**A:** `dsu.find(i)` is already a canonical id per province; optionally remap
roots to `0..k-1`.

---

## 07 · Accounts Merge (LeetCode 721)

**Q:** What are the graph nodes — accounts or emails?
**A:** **Emails.** Accounts merge *because* they share an email; accounts connect
only transitively.

**Q:** How do you use DSU on strings?
**A:** One pass to assign each distinct string an int id (+ side-maps like
`email -> name`); size the DSU to the id count; translate.

**Q:** The 4 passes?
**A:** (1) build `email_id` + `email_name`; (2) union each account's emails to
its first; (3) group emails by `find(id)`; (4) sort each group, prepend the name.

**Q:** The bug where every email ends up in its own group?
**A:** Grouping by `email_id[email]` instead of `find(email_id[email])` — bucket
by *component root*, not original id.

**Q:** Why is unioning by name wrong?
**A:** Different people can share a name. Only a shared email connects accounts.

**Q:** Time and space?
**A:** `O(E + D log D)` time (per-group sort dominates), `O(D)` space (`E` = total
emails, `D` = distinct).

**Q:** "Bucket by root" — why does it matter beyond this problem?
**A:** It's how any DSU problem produces a *listing* of its clusters, not just a
count: `groups[find(x)].append(x)` for every element, then format each bucket.

---

## Concept · Bipartite / 2-Coloring

**Q:** A graph is bipartite iff...?
**A:** 2-colorable with no edge joining same-colored nodes ⟺ **no odd-length
cycle**.

**Q:** The test?
**A:** BFS/DFS from each uncolored node; color each neighbor `-color[node]`;
same-color edge → not bipartite. **Loop over all components.**

**Q:** Why colors `1` / `-1`?
**A:** "Opposite" is just `-color[node]`; `0` stays unambiguously "uncolored."

**Q:** Incremental edges ("still bipartite after each")?
**A:** `2n`-slot Union-Find: `union(u, v+n)` + `union(v, u+n)` per edge;
`find(u) == find(v)` ⟹ not bipartite.

---

## 08 · Is Graph Bipartite? (LeetCode 785)

**Q:** The #1 false-`True` bug?
**A:** Only coloring from node `0` — a disconnected graph with an odd cycle
elsewhere slips through. Loop `for start in range(n)`.

**Q:** Time and space?
**A:** `O(V + E)` time, `O(V)` space.

**Q:** K-coloring for `K ≥ 3`?
**A:** NP-hard in general. Only `K = 2` has the easy odd-cycle test.

**Q:** How do you get the actual two groups?
**A:** Partition node ids by their value in the `color` array.

---

## 08 · Possible Bipartition (LeetCode 886)

**Q:** How does it differ from Is Graph Bipartite?
**A:** Build the adjacency list from the `dislikes` pair list first; people are
1-indexed (arrays sized `n + 1`). Then identical 2-coloring.

**Q:** The answer is `False` exactly when...?
**A:** The dislike graph has an odd-length cycle.

**Q:** Friends (must-be-together) *and* enemies (must-be-apart) — the tool?
**A:** `2n`-slot Union-Find: `union(a, b)` + `union(a+n, b+n)` for friends,
`union(a, b+n)` + `union(b, a+n)` for enemies; `find(a) == find(a+n)` ⟹
impossible.

**Q:** "Ignore up to K dislikes" — hardness?
**A:** Odd-cycle transversal — NP-hard in general (FPT in `K`); small `K` is
brute-forceable.

**Q:** The two index-base bugs to avoid?
**A:** `color` sized `n` not `n + 1`; looping `range(n)` not `range(1, n + 1)`.

---

## 09 · Evaluate Division (LeetCode 399)

**Q:** What does a normal BFS/DFS carry along the path, vs this one?
**A:** Distance problems carry a running **sum**; this carries a running
**product** (the ratio). Same traversal, different combine operator.

**Q:** What two edges does `a / b = v` create?
**A:** `a → b` weight `v`, and `b → a` weight `1 / v`.

**Q:** The ordering bug that breaks `["x","x"]`?
**A:** Checking `src == dst` **before** confirming both variables exist — an
unknown `x` then returns `1.0` instead of `-1.0`.

**Q:** Why is `-1.0` a safe "impossible" sentinel?
**A:** Every real ratio is positive (`values > 0`), so `-1.0` can never be a
legitimate answer.

**Q:** Time for `Q` queries (DFS approach)?
**A:** `O(Q · (V + E))`. Floyd-Warshall all-pairs precompute is `O(V³ + Q)`.

**Q:** Many queries against a fixed equation set — what do you do?
**A:** Precompute all-pairs ratios (Floyd-Warshall, `O(V³)` for ~40 variables)
→ `O(1)` per query. Or a weighted Union-Find.

**Q:** Detect an inconsistent equation set?
**A:** Every cycle's product must be `1`. Weighted Union-Find flags it when a
union between already-connected nodes implies a different ratio.

**Q:** One absolute value that unlocks the most variables — which?
**A:** Any variable in the **largest connected component**.

---

## Concept · Dijkstra

**Q:** Dijkstra in one line?
**A:** BFS with the FIFO queue replaced by a min-heap that always expands the
cheapest-so-far node. Valid only for **non-negative** weights.

**Q:** Why is the first pop of a node final?
**A:** Every other unfinished path to it goes through a heap entry costing `≥`
this one, and edges add `≥ 0` — so no cheaper route exists. (A negative edge
breaks this.)

**Q:** The "skip stale entries" idiom?
**A:** A node can be pushed multiple times; on pop, `if d > dist[u]: continue`
(or `if u in done: continue`) discards outdated copies.

**Q:** Heap tuple order?
**A:** `(cost, node)` — heap sorts by the first element.

**Q:** Complexity?
**A:** `O((V + E) log V)` time, `O(V + E)` space.

**Q:** Minimize the *maximum* edge on the path instead of the sum?
**A:** Same Dijkstra, `nd = max(d, w)` instead of `d + w`.

---

## 10 · Network Delay Time (LeetCode 743)

**Q:** Why Dijkstra, not BFS or Bellman-Ford?
**A:** Edges weighted (rules out plain BFS), non-negative (Dijkstra valid and
faster than Bellman-Ford).

**Q:** The answer, exactly?
**A:** `max` over all shortest distances from `k` (last node to receive it).
`-1` if any node is unreachable (`len(dist) != n`).

**Q:** The #1 bug?
**A:** Returning `sum(dist.values())` instead of `max(...)`.

**Q:** Negative edges — what changes?
**A:** Dijkstra invalid. Bellman-Ford: relax all edges `V-1` times (`O(V·E)`) +
a `V`-th pass for negative-cycle detection.

**Q:** Multiple simultaneous sources?
**A:** Push all into the heap at cost `0` (multi-source Dijkstra); answer still
`max(dist)`.

**Q:** Node processing delays (not just edge weights)?
**A:** Add `delay[u]` when relaxing `u`'s outgoing edges, or split `u` into
`u_in → u_out` joined by an edge of weight `delay[u]`.

---

## 10 · Swim in Rising Water (LeetCode 778)

**Q:** What makes this the "minimize-max" Dijkstra variant?
**A:** A path's cost is the **maximum** cell on it, not the sum. Relax with
`nd = max(d, grid[nr][nc])` instead of `d + w`.

**Q:** Why does "first pop is final" still hold with `max`?
**A:** `max` is monotonic and non-decreasing along a path, so the heap still
serves cells in true best-cost order.

**Q:** Seed the heap with what?
**A:** `(grid[0][0], 0, 0)` — the start cell's elevation, not `0`.

**Q:** Three interchangeable approaches for a bottleneck path?
**A:** (1) minimize-max Dijkstra, (2) binary search the threshold + BFS
reachability, (3) Kruskal-style Union-Find activating cells in elevation order
until endpoints connect.

**Q:** Lower bound on the answer?
**A:** `max(grid[0][0], grid[n-1][n-1])` — you must stand on both endpoints.

**Q:** Time and space?
**A:** `O(n² log n)` time, `O(n²)` space.

**Q:** The #1 bug?
**A:** `d + grid[nr][nc]` (sum) instead of `max(d, grid[nr][nc])`.

**Q:** "Widest path" / max-capacity routing?
**A:** The dual — maximize the **minimum** edge on a path; same three tools with
`min` and flipped comparisons.

---

## 10 · Path With Minimum Effort (LeetCode 1631)

**Q:** How is it related to Swim in Rising Water?
**A:** The **same** minimize-max Dijkstra. Two changes: cost on **edges** (`abs`
height diff) not cells; start seeded at effort **`0`** not `grid[0][0]`.

**Q:** The relaxation step?
**A:** `ne = max(e, abs(heights[nr][nc] - heights[r][c]))`.

**Q:** The one line separating "minimize the worst step" from "minimize the
total"?
**A:** `max(e, cost)` vs `e + cost`.

**Q:** Why seed the heap with `0`?
**A:** Before taking any step, no height difference has been crossed.

**Q:** Fixed effort budget `B` — still need Dijkstra?
**A:** No — a single BFS stepping only through edges with `abs(diff) <= B`.

**Q:** Many queries on a static grid?
**A:** Build the grid graph's MST (edges = `abs` diffs); minimize-max effort
between two cells = the **max edge on their MST path**.

**Q:** The #1 copy-from-Swim bug?
**A:** Seeding the heap with `heights[0][0]` instead of `0`.

**Q:** When is mark-at-push (each cell pushed once) a safe Dijkstra shortcut?
**A:** Only when the cost of *entering* a node is independent of the predecessor
(Swim: yes — it's the cell's own value. Path With Minimum Effort / plain `+`
Dijkstra: no — mark at pop).

---

## 10 · Number of Ways to Arrive at Destination (LeetCode 1976, supplementary)

**Q:** How do you count shortest paths on top of Dijkstra?
**A:** Keep `ways[v]` alongside `dist[v]`. Strict improvement → `ways[v] =
ways[u]`; tie at shortest distance → `ways[v] += ways[u]` (mod).

**Q:** Why does the inline `ways` update work with a plain Dijkstra?
**A:** Positive weights ⟹ every shortest-path predecessor of `v` has a strictly
smaller distance ⟹ is finalized before `v` ⟹ `ways[v]` is complete when `v` is
popped.

**Q:** What breaks it, and the fix?
**A:** Zero-weight edges. Fix: Dijkstra for `dist`, then count `ways` over the
shortest-path DAG in topological (`dist`) order.

**Q:** `=` vs `+=` on the two branches?
**A:** `<` (strict) → `ways[v] = ways[u]`. `==` (tie) → `ways[v] += ways[u]`.

**Q:** Does `MOD` ever apply to `dist`?
**A:** No — only `ways`. Distance comparisons must be exact.

**Q:** The structure under every "count/enumerate shortest paths" problem?
**A:** The **shortest-path DAG** — edges `(u, v)` with `dist[u] + w == dist[v]`.

**Q:** Tie-break by a second criterion (min toll among shortest-time paths)?
**A:** Carry `(dist, toll, ways)`; relax on the `(dist, toll)` tuple
lexicographically — replace `ways` on a strict tuple improvement, add on an exact
tie.

---

## Concept · Bellman-Ford & Floyd-Warshall

**Q:** The shortest-path decision tree?
**A:** unweighted → BFS; weighted non-negative, no cap → Dijkstra; hop/stop cap
→ Bellman-Ford (K rounds); negative weights → Bellman-Ford; all-pairs, small V →
Floyd-Warshall.

**Q:** Bellman-Ford core idea + complexity?
**A:** A shortest path has ≤ V−1 edges; relax every edge, V−1 times. `O(V·E)`
time, `O(V)` space. One extra round detects a negative cycle.

**Q:** Hop-limited Bellman-Ford (≤ K edges)?
**A:** Exactly K rounds, each relaxing against a **frozen copy** of `dist` from
the round's start — so each round adds at most one edge.

**Q:** Floyd-Warshall invariant + loop order?
**A:** After the k-loop reaches `k`, `dist[i][j]` uses only intermediates
`{0..k}`. Loop order **must** be `k, i, j` (k outermost). `O(V³)` / `O(V²)`.

**Q:** Negative cycle in Floyd-Warshall?
**A:** Shows up as `dist[i][i] < 0` for some `i`.

---

## 11 · Cheapest Flights Within K Stops (LeetCode 787)

**Q:** The tell for this pattern?
**A:** "Cheapest path" **+ "at most K stops / moves / edges."** Plain Dijkstra
can't express "cheapest among ≤ K-hop routes."

**Q:** How many rounds, and why the frozen snapshot?
**A:** `K + 1` rounds ("K stops" = "K+1 flights"). Relax against a copy of `dist`
from the round's start so a round can't chain two edges.

**Q:** The #1 bug + symptom?
**A:** No snapshot → one round chains multiple flights → over-the-limit routes
accepted. Symptom: answer too cheap.

**Q:** Why does plain Dijkstra fail?
**A:** It finalizes a city by cheapest fare, ignoring stop count.

**Q:** Time and space?
**A:** `O((k+1)(V+E)) = O(k·E)` time, `O(V)` space.

**Q:** The augmented-Dijkstra alternative?
**A:** State = `(city, stops_used)`; run normal Dijkstra; first pop of `dst` is
the answer.

**Q:** `k >= n - 1` — what does that mean?
**A:** The cap imposes no real limit (simple path has `< n` edges) → plain
shortest path → Dijkstra.

**Q:** Negative promotional fares — still works?
**A:** Yes — Bellman-Ford handles negatives, and the `k+1`-flight cap means a
negative cycle can't be exploited forever.

---

## 11 · Find the City With the Smallest Number of Neighbors (LeetCode 1334)

**Q:** When is Floyd-Warshall the right tool here?
**A:** Need all-pairs shortest distances + `V` small (`≤ 100` → `O(V³) = 10^6`).
Then a per-city count over the matrix.

**Q:** Loop order, and why?
**A:** `k` (intermediate) **outermost**, then `i`, then `j`. `k` inside breaks
the "using only nodes `≤ k`" invariant.

**Q:** The relaxation?
**A:** `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.

**Q:** Break ties toward the **largest** index — how?
**A:** Iterate `i` ascending and use `<=` (not `<`) when updating the best.

**Q:** Time and space?
**A:** `O(V³)` time, `O(V²)` space.

**Q:** `n = 2000` — what changes?
**A:** `O(V³)` too slow → Dijkstra from every source (`O(V·(V+E) log V)`).

**Q:** Negative edges / negative cycle in Floyd-Warshall?
**A:** Negative edges fine. Negative cycle shows up as `dist[i][i] < 0` — check
the diagonal.

**Q:** Same matrix, "minimize the max distance to any city" instead?
**A:** Each row's max = eccentricity; the min over those is the graph center.

---

## Concept · Minimum Spanning Tree

**Q:** What is an MST, and why is greedy optimal?
**A:** Cheapest set of `V-1` edges connecting all nodes with no cycle. Greedy
works by the **cut property**: for any split of the nodes, the cheapest crossing
edge is in some MST.

**Q:** Kruskal vs Prim?
**A:** Kruskal = sort all edges + Union-Find, skip cycle-forming ones,
`O(E log E)` — best for **sparse**. Prim = grow one tree from a heap, add the
cheapest edge leaving it, `O(E log V)` — best for **dense/complete**.

**Q:** Prim vs Dijkstra?
**A:** Same heap loop; Prim's key = "weight of one edge to reach a node,"
Dijkstra's = "accumulated path cost."

**Q:** MST facts?
**A:** Always `V-1` edges. Distinct weights ⟹ unique MST. Max spanning tree =
negate weights. MST also minimizes the max edge on any node-to-node path.

---

## 12 · Min Cost to Connect All Points (LeetCode 1584)

**Q:** What kind of problem is it?
**A:** MST of the complete graph on the points, edge weight = Manhattan distance.
Not shortest path.

**Q:** Which algorithm, and why?
**A:** Prim — it's a complete graph (`E = n²`), and Prim doesn't have to
materialize/sort all `n²` edges.

**Q:** Manhattan distance?
**A:** `|x1-x2| + |y1-y2|` = `abs(dx) + abs(dy)` — not `abs(dx+dy)`, not
Euclidean.

**Q:** Time and space?
**A:** Heap Prim: `O(n² log n)` / `O(n²)`. Plain `min_dist`-array Prim: `O(n²)` /
`O(n)`.

**Q:** `n = 10^5` — what saves you?
**A:** The Manhattan-MST trick: only each point's nearest neighbor per octant can
be an MST edge → `O(n)` candidate edges → Kruskal → `O(n log n)`.

**Q:** Leave `K` points disconnected to minimize cost?
**A:** Kruskal, stop after `n-1-K` edges (= drop the `K` heaviest MST edges) =
single-linkage clustering into `K+1` clusters.

---

## Concept · Implicit-Graph BFS

**Q:** What makes a problem "implicit-graph BFS"?
**A:** No `edges` array — you're given a start state, a goal test, and a
move rule. Nodes = states, edges = one legal move. BFS = fewest moves.

**Q:** What's the only new skill vs plain BFS?
**A:** Writing `neighbors(state)` — generating the next states from the rule.

---

## 13 · Snakes and Ladders (LeetCode 909)

**Q:** State and move?
**A:** State = board square `1..n²`. Move = one die roll (`+1..+6`, capped),
then the forced snake/ladder at that square (once, no chaining).

**Q:** Why BFS? What does the answer count?
**A:** Every roll costs 1 → BFS gives the minimum rolls. Answer = BFS level where
`n²` is first reached.

**Q:** The boustrophedon square→cell formula?
**A:** `s0 = s-1`; `rfb = s0 // n`; `r = n-1-rfb`; `c = s0 % n` if `rfb` even else
`n-1-(s0 % n)`.

**Q:** The #1 bug?
**A:** The square→cell conversion (off-by-one / column-parity flip). Then:
marking `seen` before resolving the snake/ladder.

**Q:** Time and space?
**A:** `O(n²)` both.

**Q:** Rolls have different costs — what changes?
**A:** Weighted move graph → Dijkstra instead of BFS.

**Q:** Snakes/ladders can chain — where does the loop go?
**A:** Into `get_dest` (follow the chain with cycle protection); BFS unchanged.

---

## 13 · Minimum Genetic Mutation (LeetCode 433)

**Q:** What is this problem, in one line?
**A:** Word Ladder with length fixed at 8 and a 4-letter alphabet — BFS over gene
strings, `neighbors` = one-char changes kept only if in the bank.

**Q:** The two quick exits?
**A:** `start == end` → `0`; `end not in bank` (and `!= start`) → `-1`.

**Q:** How many neighbors per gene, and how filtered?
**A:** `8 × 3 = 24` variants; keep those in the `bank_set` (`O(1)` hash check)
and not `seen`.

**Q:** Two ways to generate neighbors, when to use each?
**A:** (1) Enumerate `L × (Σ-1)` variants + hash-check bank — for a **large**
bank. (2) Scan the bank for "differs by one" — for a **small** bank.

**Q:** Time and space?
**A:** `O(states × L² × Σ)` time, `O(states × L)` space.

**Q:** Per-position mutation costs — what changes?
**A:** Weighted move graph → Dijkstra instead of BFS.

**Q:** Huge bank + large `L` — the optimizations?
**A:** Generate-and-hash-check (bank-size-independent), bidirectional BFS,
wildcard-pattern adjacency index (`"A*CCGGTT" → genes`).

---

## 13 · Word Ladder (LeetCode 127)

**Q:** What's the canonical implicit-graph BFS, and its state?
**A:** Word Ladder. State = a word; `neighbors` = one-letter changes that are in
the word set.

**Q:** Does the answer count words or transformations?
**A:** **Words** (nodes). Seed `(beginWord, 1)`, +1 per level. (Min Genetic
Mutation counts *edges* — that's the difference.)

**Q:** How many neighbors per word, and the filter?
**A:** `L × 25` variants; keep those in `set(wordList)` (`O(1)` hash) and not
`seen`.

**Q:** The two scale optimizations?
**A:** (1) Wildcard-pattern adjacency (`"h*t" → words`) → `O(L)` neighbor lookup.
(2) Bidirectional BFS → halves the shortest-path exponent.

**Q:** Time and space?
**A:** `O(N × L² × 26)` time, `O(N × L)` space. Wildcard variant: `O(N × L)`.

**Q:** The #1 bug?
**A:** Counting edges instead of nodes — start length at `0` → answer one too
small.

**Q:** Return *all* shortest ladders?
**A:** Word Ladder II: leveled BFS recording predecessor lists, then backtrack
from `endWord` (exponential in the number of paths).

**Q:** Huge / unbounded alphabet — what's forced?
**A:** Wildcard-pattern adjacency — can't enumerate letters, derive neighbors
from shared patterns among the word list.

---

## 14 · Reconstruct Itinerary (LeetCode 332)

**Q:** "Use every ticket / edge exactly once" — problem and algorithm?
**A:** Eulerian path. **Hierholzer's**: DFS, append each node **on the way out**
(post-order), reverse at the end.

**Q:** Eulerian vs Hamiltonian?
**A:** Eulerian = every *edge* once → polynomial. Hamiltonian = every *node* once
→ NP-hard.

**Q:** Why post-order + reverse, not just a greedy walk?
**A:** Greedy walking can get stuck with edges unused elsewhere. Appending only
after a node's edges are exhausted, then reversing, splices sub-cycles into place.

**Q:** Lexicographically smallest itinerary — how?
**A:** Min-heap (or sorted list) of destinations per node; always take the
smallest next edge.

**Q:** The #1 bug?
**A:** Appending in pre-order instead of post-order.

**Q:** Time and space?
**A:** `O(E log E)` time, `O(E)` space. Each edge consumed exactly once.

**Q:** Directed Eulerian-path existence conditions?
**A:** Connected + exactly one vertex `out-in = 1` (start), one `in-out = 1`
(end), rest balanced.

**Q:** Tickets have prices — cheapest full itinerary?
**A:** Trick: every full itinerary uses every edge once → all cost `sum(prices)`.
