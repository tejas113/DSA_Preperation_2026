# Graphs 2.0 — Topic-by-Topic Roadmap

The full graph problem set (40 problems, 15 topics), carried over from the original `Graphs` repo's
`problem-sources.md`. Every write-up will be redone in the single standard structure used across all
repos (Intuition → Approach → Code → Dry Run → Complexity → Recall), one problem at a time.

This file is the master tracker and the single source of truth. Each problem has a **global number**
(1–40, not reset per topic). Problem files go in a topic folder as `NN-topic-folder/NN-problem-slug.md`.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list |
| **NC150** | On the *NeetCode 150* list |
| **LC150 + NC150** | On **both** lists |
| **[+] Claude** | Not on either list. Added to round out pattern coverage or close a Google-interview gap |

🔒 after an LC # means LeetCode Premium (you can't submit on the site without a subscription, but the write-up is still usable).

**Totals:** 40 problems — 6 on both lists · 3 LC150-only · 13 NC150-only · 18 Claude additions.

**L3 Likelihood:** my judgement of how likely each problem (or a close variant) is in a Google L3
interview. There is **no verified Google data** behind it. It's based on how often the pattern shows up
in public interview reports and how well the problem fits a 45-minute L3 round. High means do it first,
Medium means do it next, and Low means do it last or only if time allows.

> **L3 must-do (the 11 High problems, in suggested order):** 1 Number of Islands → 3 Max Area of Island →
> 7 Rotting Oranges → 36 Shortest Path in Binary Matrix → 13 Course Schedule → 14 Course Schedule II →
> 20 Connected Components → 22 Accounts Merge → 26 Network Delay Time → 25 Evaluate Division → 35 Word Ladder.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority:** not assigned yet (carried over as `TBD`). Set each one to Core or Stretch when you reach it.

> **Note:** source tags, groups and problem order are copied as-is from `Graphs/problem-sources.md`.
> Difficulty is the LeetCode difficulty. The old repo's separate "original" and "supplementary" Claude
> tags are merged into **[+] Claude**, and its ✅ / 🔁 status flags are reset to ☐ because every
> write-up is being redone.

---

## Topic 1 — Grid Flood-Fill (`01-grid-flood-fill/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 1 | Number of Islands | **LC150 + NC150** | 200 | Medium | Core | High | ☑ | [01-number-of-islands.md](01-grid-flood-fill/01-number-of-islands.md) |
| 2 | Flood Fill | **[+] Claude** | 733 | Easy | Stretch | Low | ☑ | [02-flood-fill.md](01-grid-flood-fill/02-flood-fill.md) |
| 3 | Max Area of Island | NC150 | 695 | Medium | Core | High | ☑ | [03-max-area-of-island.md](01-grid-flood-fill/03-max-area-of-island.md) |
| 4 | Making a Large Island | **[+] Claude** | 827 | Hard | TBD | Medium | ☐ | TBD |

## Topic 2 — Multi-Source BFS on a Grid (`02-multi-source-bfs/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 5 | Walls and Gates | NC150 | 286 🔒 | Medium | Core | Medium | ☑ | [05-walls-and-gates.md](02-multi-source-bfs/05-walls-and-gates.md) |
| 6 | 01 Matrix | **[+] Claude** | 542 | Medium | Stretch | Medium | ☑ | [06-01-matrix.md](02-multi-source-bfs/06-01-matrix.md) |
| 7 | Rotting Oranges | NC150 | 994 | Medium | Core | High | ☑ | [07-rotting-oranges.md](02-multi-source-bfs/07-rotting-oranges.md) |
| 8 | Shortest Bridge | **[+] Claude** | 934 | Medium | Core | Medium | ☑ | [08-shortest-bridge.md](02-multi-source-bfs/08-shortest-bridge.md) |

## Topic 3 — Boundary-Anchored Traversal (`03-boundary-anchored-traversal/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 9 | Pacific Atlantic Water Flow | NC150 | 417 | Medium | Core | Medium | ☑ | [09-pacific-atlantic-water-flow.md](03-boundary-anchored-traversal/09-pacific-atlantic-water-flow.md) |
| 10 | Surrounded Regions | **LC150 + NC150** | 130 | Medium | Stretch | Medium | ☑ | [10-surrounded-regions.md](03-boundary-anchored-traversal/10-surrounded-regions.md) |

## Topic 4 — Graph Traversal / Connectivity, non-grid (`04-graph-traversal-connectivity/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 11 | Find if Path Exists in Graph | **[+] Claude** | 1971 | Easy | TBD | Low | ☐ | TBD |

## Topic 5 — Hashmap + Traversal, structural copy (`05-clone-graph/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 12 | Clone Graph | **LC150 + NC150** | 133 | Medium | Core | Medium | ☑ | [12-clone-graph.md](05-clone-graph/12-clone-graph.md) |

## Topic 6 — Topological Sort / Cycle Detection (`06-topological-sort/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 13 | Course Schedule | **LC150 + NC150** | 207 | Medium | Core | High | ☑ | [13-course-schedule.md](06-topological-sort/13-course-schedule.md) |
| 14 | Course Schedule II | **LC150 + NC150** | 210 | Medium | Stretch | High | ☑ | [14-course-schedule-ii.md](06-topological-sort/14-course-schedule-ii.md) |
| 15 | Alien Dictionary | NC150 | 269 🔒 | Hard | Stretch | Medium | ☑ | [15-alien-dictionary.md](06-topological-sort/15-alien-dictionary.md) |
| 16 | Minimum Height Trees | **[+] Claude** | 310 | Medium | Stretch | Low | ☑ | [16-minimum-height-trees.md](06-topological-sort/16-minimum-height-trees.md) |
| 17 | Longest Increasing Path in a Matrix | **[+] Claude** | 329 | Hard | Core | Medium | ☑ | [17-longest-increasing-path-in-a-matrix.md](06-topological-sort/17-longest-increasing-path-in-a-matrix.md) |

## Topic 7 — Union-Find (`07-union-find/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 18 | Redundant Connection | NC150 | 684 | Medium | Core | Medium | ☑ | [18-redundant-connection.md](07-union-find/18-redundant-connection.md) |
| 19 | Graph Valid Tree | NC150 | 261 🔒 | Medium | Stretch | Medium | ☑ | [19-graph-valid-tree.md](07-union-find/19-graph-valid-tree.md) |
| 20 | Number of Connected Components in an Undirected Graph | NC150 | 323 🔒 | Medium | Stretch | High | ☑ | [20-number-of-connected-components-in-an-undirected-graph.md](07-union-find/20-number-of-connected-components-in-an-undirected-graph.md) |
| 21 | Number of Provinces | **[+] Claude** | 547 | Medium | Stretch | Medium | ☑ | [21-number-of-provinces.md](07-union-find/21-number-of-provinces.md) |
| 22 | Accounts Merge | **[+] Claude** | 721 | Medium | TBD | High | ☐ | TBD |

## Topic 8 — Bipartite / 2-Coloring (`08-bipartite-2-coloring/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 23 | Is Graph Bipartite? | **[+] Claude** | 785 | Medium | Core | Medium | ☑ | [23-is-graph-bipartite.md](08-bipartite-2-coloring/23-is-graph-bipartite.md) |
| 24 | Possible Bipartition | **[+] Claude** | 886 | Medium | Stretch | Low | ☑ | [24-possible-bipartition.md](08-bipartite-2-coloring/24-possible-bipartition.md) |

## Topic 9 — Weighted DFS, ratio propagation (`09-weighted-dfs-ratio/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 25 | Evaluate Division | LC150 | 399 | Medium | Core | High | ☑ | [25-evaluate-division.md](09-weighted-dfs-ratio/25-evaluate-division.md) |

## Topic 10 — Dijkstra (`10-dijkstra/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 26 | Network Delay Time | NC150 | 743 | Medium | Core | High | ☑ | [26-network-delay-time.md](10-dijkstra/26-network-delay-time.md) |
| 27 | Swim in Rising Water | NC150 | 778 | Hard | Core | Low | ☑ | [27-swim-in-rising-water.md](10-dijkstra/27-swim-in-rising-water.md) |
| 28 | Path With Minimum Effort | **[+] Claude** | 1631 | Medium | Stretch | Medium | ☑ | [28-path-with-minimum-effort.md](10-dijkstra/28-path-with-minimum-effort.md) |
| 29 | Number of Ways to Arrive at Destination | **[+] Claude** | 1976 | Medium | Core | Low | ☑ | [29-number-of-ways-to-arrive-at-destination.md](10-dijkstra/29-number-of-ways-to-arrive-at-destination.md) |

## Topic 11 — Bellman-Ford / All-Pairs Shortest Path (`11-bellman-ford-and-all-pairs/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 30 | Cheapest Flights Within K Stops | NC150 | 787 | Medium | Core | Medium | ☑ | [30-cheapest-flights-within-k-stops.md](11-bellman-ford-and-all-pairs/30-cheapest-flights-within-k-stops.md) |
| 31 | Find the City With the Smallest Number of Neighbors at a Threshold Distance | **[+] Claude** | 1334 | Medium | TBD | Low | ☐ | TBD |

## Topic 12 — Minimum Spanning Tree (`12-mst/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 32 | Min Cost to Connect All Points | NC150 | 1584 | Medium | TBD | Medium | ☐ | TBD |

## Topic 13 — Implicit-Graph BFS (`13-implicit-graph-bfs/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 33 | Snakes and Ladders | LC150 | 909 | Medium | Core | Low | ☑ | [33-snakes-and-ladders.md](13-implicit-graph-bfs/33-snakes-and-ladders.md) |
| 34 | Minimum Genetic Mutation | LC150 | 433 | Medium | Stretch | Low | ☑ | [34-minimum-genetic-mutation.md](13-implicit-graph-bfs/34-minimum-genetic-mutation.md) |
| 35 | Word Ladder | **LC150 + NC150** | 127 | Hard | Stretch | High | ☑ | [35-word-ladder.md](13-implicit-graph-bfs/35-word-ladder.md) |
| 36 | Shortest Path in Binary Matrix | **[+] Claude** | 1091 | Medium | Core | High | ☑ | [36-shortest-path-in-binary-matrix.md](13-implicit-graph-bfs/36-shortest-path-in-binary-matrix.md) |
| 37 | Word Ladder II | **[+] Claude** | 126 | Hard | TBD | Low | ☐ | TBD |
| 38 | Shortest Path Visiting All Nodes | **[+] Claude** | 847 | Hard | TBD | Low | ☐ | TBD |

## Topic 14 — Eulerian Path / Advanced DFS (`14-eulerian-path/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 39 | Reconstruct Itinerary | NC150 | 332 | Hard | TBD | Low | ☐ | TBD |

## Topic 15 — Bridges / Articulation Points (`15-bridges-articulation-points/`)

| # | Problem | Source | LC # | Difficulty | Priority | L3 Likelihood | Status | File |
|---|---|---|---|---|---|---|---|---|
| 40 | Critical Connections in a Network | **[+] Claude** | 1192 | Hard | TBD | Low | ☐ | TBD |

---

## Progress

**31 / 40 done.**
