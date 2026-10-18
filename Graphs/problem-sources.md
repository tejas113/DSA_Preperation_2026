# Problem Sources — all 40 problems, where each one came from

A single reference: every problem in this repo, which list it came from, its
LeetCode number, and whether it's done yet. Cross-reference with `README.md` for
the pattern grouping and `pattern-identification.md` for how to recognize each
pattern.

**Source tags:**

- **LeetCode 150** — from LeetCode's official "Top Interview 150" list.
- **NeetCode 150** — from NeetCode's curated 150 list. `🔒` = LeetCode Premium
  (subscription required to submit; the `.md`/`.py` here are still fully usable —
  you just can't click "Submit" on LeetCode's site without Premium).
- **Claude add (original)** — one of the 8 problems added to your original
  30-problem list to round out pattern coverage, proposed at the start and
  included in the curated 30.
- **Claude add (supplementary)** — one of the 10 problems added afterward,
  identified as genuine Google-interview gaps not covered by the original 30 (see
  the honest coverage assessment in `README.md`). You explicitly approved adding
  all 10.

**Status tags:** ✅ Done · ⏳ Pending · **🔁 Revise** — done and correct, but
flagged by Tejas to re-solve from scratch on a later revision pass (Day 5, or
whenever you circle back). A `🔁` next to a problem is not a correctness issue —
check its `.md` appendix for why it was flagged.

**Summary:**

| Source | Count |
|---|---|
| Appears in LeetCode 150 | 9 |
| Appears in NeetCode 150 | 19 |
| Claude add (original, part of your curated 30) | 8 |
| Claude add (supplementary, closing Google-coverage gaps) | 10 |
| **Total unique problems** | **40** |

(6 problems appear on *both* LeetCode 150 and NeetCode 150 — they're counted in
both rows above, which is why the first two rows sum to more than 30.)

---

## Group 01 — Grid Flood-Fill

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Number of Islands](01-grid-flood-fill/01-number-of-islands.md) | 200 | LeetCode 150 + NeetCode 150 | ✅ Done |
| 2 | [Flood Fill](01-grid-flood-fill/02-flood-fill.md) | 733 | Claude add (original) | ✅ Done |
| 3 | [Max Area of Island](01-grid-flood-fill/03-max-area-of-island.md) | 695 | NeetCode 150 | ✅ Done |
| 4 | [Making a Large Island](01-grid-flood-fill/04-making-a-large-island.md) | 827 | Claude add (supplementary) | ✅ Done |

## Group 02 — Multi-Source BFS on a Grid

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Walls and Gates](02-multi-source-bfs/01-walls-and-gates.md) | 286 🔒 | NeetCode 150 | ✅ Done |
| 2 | [01 Matrix](02-multi-source-bfs/02-01-matrix.md) | 542 | Claude add (original) | ✅ Done |
| 3 | [Rotting Oranges](02-multi-source-bfs/03-rotting-oranges.md) | 994 | NeetCode 150 | ✅ Done |
| 4 | [Shortest Bridge](02-multi-source-bfs/04-shortest-bridge.md) | 934 | Claude add (supplementary) | ✅ Done |

## Group 03 — Boundary-Anchored Traversal

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Pacific Atlantic Water Flow](03-boundary-anchored-traversal/01-pacific-atlantic-water-flow.md) | 417 | NeetCode 150 | ✅ Done |
| 2 | [Surrounded Regions](03-boundary-anchored-traversal/02-surrounded-regions.md) | 130 | LeetCode 150 + NeetCode 150 | ✅ Done |

## Group 04 — Graph Traversal / Connectivity (non-grid)

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Find if Path Exists in Graph](04-graph-traversal-connectivity/01-find-if-path-exists-in-graph.md) | 1971 | Claude add (original) | ✅ Done |

## Group 05 — Hashmap + Traversal (structural copy)

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Clone Graph](05-clone-graph/01-clone-graph.md) | 133 | LeetCode 150 + NeetCode 150 | ✅ Done · 🔁 Revise |

## Group 06 — Topological Sort / Cycle Detection

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Course Schedule](06-topological-sort/01-course-schedule.md) | 207 | LeetCode 150 + NeetCode 150 | ✅ Done |
| 2 | [Course Schedule II](06-topological-sort/02-course-schedule-ii.md) | 210 | LeetCode 150 + NeetCode 150 | ✅ Done |
| 3 | [Alien Dictionary](06-topological-sort/03-alien-dictionary.md) | 269 🔒 | NeetCode 150 | ✅ Done |
| 4 | [Minimum Height Trees](06-topological-sort/04-minimum-height-trees.md) | 310 | Claude add (supplementary) | ✅ Done |
| 5 | [Longest Increasing Path in a Matrix](06-topological-sort/05-longest-increasing-path-in-a-matrix.md) | 329 | Claude add (supplementary) | ✅ Done |

## Group 07 — Union-Find

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Redundant Connection](07-union-find/01-redundant-connection.md) | 684 | NeetCode 150 | ✅ Done |
| 2 | [Graph Valid Tree](07-union-find/02-graph-valid-tree.md) | 261 🔒 | NeetCode 150 | ✅ Done |
| 3 | [Number of Connected Components in an Undirected Graph](07-union-find/03-number-of-connected-components.md) | 323 🔒 | NeetCode 150 | ✅ Done |
| 4 | [Number of Provinces](07-union-find/04-number-of-provinces.md) | 547 | Claude add (original) | ✅ Done |
| 5 | [Accounts Merge](07-union-find/05-accounts-merge.md) | 721 | Claude add (original) | ✅ Done |

## Group 08 — Bipartite / 2-Coloring

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Is Graph Bipartite?](08-bipartite-2-coloring/01-is-graph-bipartite.md) | 785 | Claude add (original) | ✅ Done |
| 2 | [Possible Bipartition](08-bipartite-2-coloring/02-possible-bipartition.md) | 886 | Claude add (original) | ✅ Done |

## Group 09 — Weighted DFS (ratio propagation)

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Evaluate Division](09-weighted-dfs-ratio/01-evaluate-division.md) | 399 | LeetCode 150 | ✅ Done |

## Group 10 — Dijkstra

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Network Delay Time](10-dijkstra/01-network-delay-time.md) | 743 | NeetCode 150 | ✅ Done |
| 2 | [Swim in Rising Water](10-dijkstra/02-swim-in-rising-water.md) | 778 | NeetCode 150 | ✅ Done |
| 3 | [Path With Minimum Effort](10-dijkstra/03-path-with-minimum-effort.md) | 1631 | Claude add (original) | ✅ Done |
| 4 | [Number of Ways to Arrive at Destination](10-dijkstra/04-number-of-ways-to-arrive-at-destination.md) | 1976 | Claude add (supplementary) | ✅ Done |

## Group 11 — Bellman-Ford / All-Pairs Shortest Path

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Cheapest Flights Within K Stops](11-bellman-ford-and-all-pairs/01-cheapest-flights-within-k-stops.md) | 787 | NeetCode 150 | ✅ Done · 🔁 Revise |
| 2 | [Find the City With the Smallest Number of Neighbors at a Threshold Distance](11-bellman-ford-and-all-pairs/02-find-the-city-smallest-neighbors.md) | 1334 | Claude add (supplementary) | ✅ Done · 🔁 Revise |

## Group 12 — Minimum Spanning Tree

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Min Cost to Connect All Points](12-mst/01-min-cost-to-connect-all-points.md) | 1584 | NeetCode 150 | ✅ Done |

## Group 13 — Implicit-Graph BFS

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Snakes and Ladders](13-implicit-graph-bfs/01-snakes-and-ladders.md) | 909 | LeetCode 150 | ✅ Done |
| 2 | [Minimum Genetic Mutation](13-implicit-graph-bfs/02-minimum-genetic-mutation.md) | 433 | LeetCode 150 | ✅ Done |
| 3 | [Word Ladder](13-implicit-graph-bfs/03-word-ladder.md) | 127 | LeetCode 150 + NeetCode 150 | ✅ Done |
| 4 | Shortest Path in Binary Matrix | 1091 | Claude add (supplementary) | ⏳ Pending |
| 5 | Word Ladder II | 126 | Claude add (supplementary) | ⏳ Pending |
| 6 | Shortest Path Visiting All Nodes | 847 | Claude add (supplementary) | ⏳ Pending |

## Group 14 — Eulerian Path / Advanced DFS

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | [Reconstruct Itinerary](14-eulerian-path/01-reconstruct-itinerary.md) | 332 | NeetCode 150 | ✅ Done |

## Group 15 — Bridges / Articulation Points

| # | Problem | LeetCode # | Source | Status |
|---|---|---|---|---|
| 1 | Critical Connections in a Network | 1192 | Claude add (supplementary) | ⏳ Pending |

---

## Progress

**36 / 40 done** (Groups 01–12 + 14 complete; Group 13: 3/6 — remaining 3 are
supplementary, deferred). 4 remaining (Group 13 ×3 supplementary + Group 15
Tarjan).

**🔁 Flagged for revision on Day 5:** all of Group 11 (Cheapest Flights, Find the
City), Clone Graph.
