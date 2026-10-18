# Pattern Identification — "Which graph pattern is this?"

The single hardest interview skill is **reading an unfamiliar problem and naming
the pattern in 60 seconds**. Google problems never say "use Dijkstra". They
describe a scenario. You translate.

This file grows as we cover each group. Re-read the whole thing on Day 5.

---

## Step 0 — Is it even a graph problem?

It is a graph problem if you can phrase it as **"things (nodes) connected by
relationships (edges), and I need to move along the relationships."**

Common disguises:

| The problem talks about... | Nodes are... | Edges are... |
|---|---|---|
| A 2D grid / matrix / image / maze | cells `(r, c)` | up/down/left/right (sometimes 8 directions) |
| Courses with prerequisites | courses | "A must come before B" |
| Words that transform one letter at a time | words | "differs by exactly one letter" |
| People who are friends / accounts that share an email | people / accounts | the friendship / shared email |
| Cities with flights, roads with cost/time | cities | flights / roads (weighted) |
| Currency / variable ratios (a/b = 2) | variables | the ratio, and its inverse |
| Board games (Snakes & Ladders) | squares | a dice roll, plus the snake/ladder jump |
| State puzzles (which nodes visited, gene string, lock combo) | a *state* | one legal move to the next state |

If you can fill that table, it's a graph problem.

---

## Step 1 — The decision tree

```
Is the input a 2D grid?
├─ YES
│  ├─ "Count regions" / "how many islands" / "largest area" ......... GROUP 01  grid flood-fill
│  ├─ "Distance from every cell to the nearest X"
│  │   or "how many steps until everything is filled" .............. GROUP 02  multi-source BFS
│  ├─ "Which cells can reach BOTH edges / the border" .............. GROUP 03  boundary-anchored
│  ├─ "Shortest path from A to B on the grid" ..................... GROUP 13  implicit-graph BFS
│  ├─ "Minimize the maximum cell value along a path"
│  │   ("effort", "rising water") ................................ GROUP 10  Dijkstra (min-max variant)
│  └─ "Longest increasing path" .................................. GROUP 06  DAG + memoization
│
└─ NO — it's an explicit or hidden graph
   ├─ "Just tell me if A connects to B" / "count groups" ......... GROUP 04 or 07  traversal / union-find
   ├─ "Copy the graph" ......................................... GROUP 05  hashmap + traversal
   ├─ "Order tasks with prerequisites" / "is there a cycle in
   │   a directed graph" / "valid build order" ................. GROUP 06  topological sort
   ├─ "Add edges one by one; which one closes a loop" .......... GROUP 07  union-find
   ├─ "Split into two teams so enemies are apart" .............. GROUP 08  bipartite / 2-coloring
   ├─ "Given a/b and b/c, find a/c" ........................... GROUP 09  weighted DFS (ratio)
   ├─ Shortest path, edges have NON-negative weights .......... GROUP 10  Dijkstra
   ├─ Shortest path, at most K stops / negative edges ......... GROUP 11  Bellman-Ford
   ├─ Shortest path between EVERY pair, small graph ........... GROUP 11  Floyd-Warshall
   ├─ "Connect everything at minimum total cost" ............. GROUP 12  Minimum Spanning Tree
   ├─ Shortest number of MOVES, each move is a rule .......... GROUP 13  implicit-graph BFS
   ├─ "Use every ticket exactly once" (use every EDGE) ....... GROUP 14  Eulerian path
   └─ "Which single connection, if cut, splits the network" .. GROUP 15  bridges (Tarjan)
```

---

## Step 2 — BFS or DFS? (for a plain traversal)

| Use **BFS** when | Use **DFS** when |
|---|---|
| You need the **shortest path / fewest steps** in an **unweighted** graph | You only need to know **if** something is reachable / to visit everything |
| You process the graph **layer by layer** ("minutes", "levels") | You need to **explore fully and come back** (backtracking, Euler path) |
| Multiple starting points at once (multi-source) | You want the simplest possible code for "flood fill this region" |
| The graph is very deep (recursion would overflow) | The recursion depth is safely bounded |

Both are `O(V + E)` time. They differ in *which* answer they naturally give you.

---

## Step 3 — Trigger-word table (memorize this)

| Phrase in the problem | Almost always means |
|---|---|
| "number of islands / provinces / groups / friend circles" | count connected components (Group 01 / 04 / 07) |
| "nearest", "closest", "minimum distance to any" | multi-source BFS (Group 02) |
| "rot", "spread", "infect", "minutes until" | multi-source BFS, answer = number of layers (Group 02) |
| "can water flow to both oceans", "cells not touching the border" | start from the border, invert (Group 03) |
| "prerequisite", "before", "dependency", "build order", "can you finish" | topological sort / cycle detection (Group 06) |
| "redundant edge", "the edge that creates a cycle", "valid tree" | union-find (Group 07) |
| "two groups", "bipartite", "no two adjacent the same" | 2-coloring (Group 08) |
| "exchange rate", "a / b", "ratio" | weighted DFS product (Group 09) |
| "shortest / cheapest / fastest" + weights, no negatives | Dijkstra (Group 10) |
| "at most K stops", "within K moves", negative weights | Bellman-Ford (Group 11) |
| "minimize the maximum", "path where the largest step is smallest" | Dijkstra where cost = max(so far, edge) (Group 10) |
| "connect all points/cities with minimum total cost" | MST — Prim or Kruskal (Group 12) |
| "fewest moves", "shortest transformation sequence", each move follows a rule | implicit-graph BFS (Group 13) |
| "use all tickets", "traverse every edge once" | Eulerian path, Hierholzer (Group 14) |
| "critical connection", "cutting this disconnects the graph" | bridges, Tarjan (Group 15) |
| "visit all nodes", small N (≤ ~15) | BFS with a bitmask state (Group 13, `concepts/16`) |

---

## Step 4 — Say it out loud in the interview

A strong opening sounds like:

> "The cities and flights form a **weighted directed graph**. I need the cheapest
> path from `src` to `dst` but with **at most K stops**, so plain Dijkstra isn't
> safe here — the stop limit means a longer-hop path can be cheaper. This is a
> **Bellman-Ford** shape: relax all edges `K + 1` times. Time is
> `O(K * E)`, space `O(V)`. Let me code that."

Notice the structure: **name the graph → name the twist → name the algorithm →
give complexity → then code.** Every problem file's sections 3, 4, and 10 give you
the words for exactly this.
