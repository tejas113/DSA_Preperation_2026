# Graphs: Scenario Question Bank (Google L3 style)

Google doesn't say "graph". It gives a short, vague scenario, and **you** have to spot the graph.
This file has one scenario per solved problem, plus the movie question from the real interview (S0).
Problem numbers match `problems.md`.

**Disguised on purpose:** scenarios never say "adjacent", "neighbour", "graph" or "edge". Each has an **Ask first** line, which is the clarifying questions a good candidate asks. Those questions are how you discover the structure.

**How to use:** read only the **Scenario** line, then say out loud: *nodes? edges? directed? weighted? what am I asking for?* Only then read the rest.

---

## Part 1. The 5-step "is this a graph?" framework

1. **Find the nodes.** What are the "things"? (cells, users, tasks, words, cities, states)
2. **Find the edges.** What relates two things? (adjacent, depends on, similar to, one move away, road)
3. **Directed or undirected? Weighted or not?** ("must come before" = directed, "similar / friends" = undirected, "cost / time / distance" = weighted)
4. **What is being asked?** Pick the pattern from the table in Part 2.
5. **Say complexity in V and E** (or rows × cols for a grid) before you code.

**Questions to ask the interviewer (cheap and impressive):** Is it directed? Can there be cycles or duplicates? Is it connected? Sizes of V and E? One query or many? Can I modify the input?

---

## Part 2. Signal → pattern cheat sheet

| What the question says | It is really | Pattern | Problems |
|---|---|---|---|
| "groups", "clusters", "circles", "how many separate…" | connected components | DFS/BFS count or Union-Find | 1, 3, 20, 21, S0 |
| "transitive": A~B and B~C means A~C | connected components | Union-Find / DFS | S0, 20, 21 |
| "nearest X for every cell", "spreads each day / minute" | shortest distance from many sources | multi-source BFS | 5, 6, 7, 8 |
| "fewest steps / moves / mutations / rolls" with equal cost per step | shortest path, unweighted | BFS (often on an implicit graph) | 33, 34, 35, 36 |
| "A must happen before B", "dependencies", "order", "prerequisite" | directed graph, order or cycle | Topological sort (Kahn) | 13, 14, 15, 17 |
| "can it be done?" with dependencies | cycle detection | Kahn count, or DFS 3-colour | 13 |
| "derive the order from sorted data" | build edges from adjacent pairs, then topo sort | Topological sort | 15 |
| "extra connection", "redundant", "forms a loop" | cycle in undirected graph | Union-Find | 18 |
| "is it a valid tree / hierarchy" | n−1 edges and connected | Union-Find or DFS | 19 |
| "split into two teams / sides", "conflict pairs" | bipartite | BFS 2-colouring | 23, 24 |
| "convert A to B through intermediate rates" | weighted path, multiply | BFS/DFS carrying a product | 25 |
| "minimum time / cost" with different costs per edge | shortest path, weighted, non-negative | Dijkstra | 26 |
| "minimise the worst / highest / steepest step on the route" | minimax path | Dijkstra with `max` (or binary search + BFS) | 27, 28 |
| "how many shortest routes" | count paths | Dijkstra + `ways[]` | 29 |
| "at most K stops / steps" with costs | limited-edge shortest path | Bellman-Ford, K+1 rounds | 30 |
| "reach from the borders / edges / oceans" | reverse search from the boundary | multi-source DFS/BFS from the edge | 9, 10 |
| "copy / duplicate a structure with links" | traversal + map old→new | DFS/BFS + hashmap | 12 |
| "best root / centre of a tree" | peel leaves | Kahn on degree | 16 |
| "longest path where each step must increase" | longest path in a DAG | DFS + memo (or Kahn) | 17 |
| "states and moves" (words, genes, boards, puzzles) | implicit graph | BFS over states | 33, 34, 35 |

**Red flags that you're being tested on graphs:** the question talks about *relationships*, *connections*, *dependencies*, *spreading*, *reachability*, *neighbours*, *grid with moves*, or *"minimum number of steps"*.

---

## Part 3. Complexity patterns

| Pattern | Time | Space | Why (one line) |
|---|---|---|---|
| Grid DFS/BFS (islands, flood fill, area, rotting, 01 matrix, walls and gates, binary matrix) | O(R·C) | O(R·C) | every cell is entered once, 4 or 8 neighbours each. The space is recursion depth (DFS) or the queue (BFS). |
| General DFS/BFS on adjacency list (clone, bipartite, components) | O(V + E) | O(V) | each node once, each edge once or twice. |
| Adjacency **matrix** (provinces) | O(n²) | O(n) | scanning a row costs n, and you do it for every node. |
| Topological sort / Kahn (13, 14, 15, 16) | O(V + E) | O(V + E) | each node popped once, each edge relaxed once. |
| Alien Dictionary | O(C) total characters | O(1) (26 letters) | edges come from adjacent word pairs. |
| DFS + memo on a DAG (17) | O(V + E), or O(R·C) on a grid | O(R·C) | every state solved once. |
| Union-Find with path compression | about O(E · α(n)) with rank, O(E log n) without | O(n) | α is under 5 in practice. |
| Dijkstra (26, 27, 28, 29) | O((V + E) log V) | O(V + E) | one heap operation per improving edge. Grid: O(R·C log(R·C)). |
| Bellman-Ford, K rounds (30) | O(K · E) | O(V) | K+1 passes over every edge. |
| Implicit BFS (33–36) | O(states × transitions per state) | O(states) | 33: n² × 6. 34: B·L². 35: N·L²·26. |
| Weighted ratio graph, per query BFS (25) | O(E + Q·(V + E)) | O(V + E) | a fresh BFS per query. |

**Rules of thumb**
- Every node and edge touched a constant number of times means **O(V + E)**. On a grid, V = R·C and E ≤ 8·V, so **O(R·C)**.
- A heap adds a **log**. Same edge cost on every edge means **BFS (no log)**. Different non-negative costs means **Dijkstra**. Negative costs, or a step limit, means **Bellman-Ford**.
- Recursive DFS **space** = depth of recursion, up to V. Always mention the recursion-limit risk, and offer the iterative version.
- A hashmap or set of visited nodes is O(V) space. Marking the grid in place is O(1) extra, but **say that you are mutating the input**.

---

## Part 4. The scenarios

Each entry has: **Original question** (the formal LeetCode statement), then **Scenario** (what you'd actually hear), **Ask first**, **Spot it** (the graph clue), **Model** (nodes / edges), **Solve** (the answer from your notes), **Cost**, **Follow-up** (what they'd push on), and **two more variants (A and B)** on the same pattern. Each variant gives the formal **Question** first, then the disguised **Scenario**, then the **Pattern and cost**.

---

### S0. Movie recommendations (REAL interview question)

**Original question:** Real interview question. Given movies (title, rating) and a list of pairs the process marked as similar, where similarity is transitive, return the N highest-rated movies similar to a given movie.

**Scenario:** Each movie has a title and a rating. A separate process marks some pairs of movies as similar. Treat similarity as transitive (A~B and B~C means A~C). Given a movie, return its N most similar movies with the highest ratings.

**Spot it:** "transitive" means everything reachable counts. That is a connected component.
**Model:** nodes = movies, edges = "marked similar" (undirected).
**Solve:** build an adjacency list from the pairs. DFS/BFS from the given movie to collect its whole component, and skip the movie itself. Take the top N by rating. Use `heapq.nlargest(N, ...)`, or a min-heap of size N. Sorting also works.
**Cost:** time O(V + E + K log N) with K = component size (sorting: K log K). Space O(V + E).
**Follow-up:** *Many queries?* Precompute components once with Union-Find or labelling, and store each component's movies sorted by rating. Then each query is O(N). *Similarity is not transitive?* Then it's BFS to depth d, not the whole component. *Ratings change over time?* Keep a heap per component. *Millions of movies?* Union-Find as a stream, since pairs arrive one at a time.

**More scenarios on the same pattern**

**Variant A**
- **Question:** Given account IDs and pairs flagged as 'same customer', return all other accounts of the customer for a given account, newest first.
- **Scenario:** Support has account IDs and a log of 'these two accounts belong to one customer'. For a ticket from one account, list that customer's other accounts, newest first.
- **Pattern and cost:** Connected component of the given account (DFS/BFS or Union-Find), then sort by date. O(V + E + K log K).

**Variant B**
- **Question:** Same as the movie question, but similarity is NOT transitive. Return the N best-rated movies within d links of the given movie.
- **Scenario:** A streaming app shows 'because you watched X'. Only suggest titles within two marked-similar hops of X, best rated first.
- **Pattern and cost:** Depth-limited BFS from the movie, then a heap for the top N. O(V + E + K log N).

---

### S1. Number of Islands (#1)

**Original question:** LC 200. Given an m x n grid of '1' (land) and '0' (water), return the number of islands. An island is land connected horizontally or vertically.

**Scenario:** A binary image is stored as a matrix, where 1 is foreground. Report how many separate objects are in the image.
**Ask first:** Does a diagonal touch join two pixels? Can I modify the matrix?
**Spot it:** "groups of touching things".
**Model:** nodes = occupied cells, edges = 4-neighbour adjacency.
**Solve:** scan every cell. On an unseen `1`, flood it (sink to `0`) and add 1.
**Cost:** O(R·C) time, O(R·C) space worst case (recursion). BFS avoids the recursion limit.
**Follow-up:** Diagonals count? (8 directions.) Can't modify the grid? (use a visited set.) Cells are added one by one and you need the count after each? (Union-Find. That's LC 305.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Given a floor plan with walls and open cells, count the separate rooms.
- **Scenario:** A blueprint is stored as a matrix with # for wall and . for open floor. How many separate rooms does the building have?
- **Pattern and cost:** Components over the open cells. The wall/open flip is the only change from S1. O(R*C).

**Variant B**
- **Question:** Cells turn to land one at a time. After each addition, report the number of islands (LC 305).
- **Scenario:** A reef grows as coral is planted at given spots, one at a time. After each planting, report how many separate reefs exist.
- **Pattern and cost:** Union-Find over a stream. Count goes +1 per new cell and -1 per successful merge. O(K * alpha) plus O(R*C) memory.

### S2. Flood Fill (#2)

**Original question:** LC 733. Given an image (m x n ints), a start pixel (sr, sc) and a colour, recolour the start pixel and every pixel connected to it 4-directionally that has the same original colour. Return the image.

**Scenario:** In an image editor, the user clicks one pixel with the paint-bucket tool and picks a colour. Implement the fill.
**Ask first:** What counts as the same region? What if the new colour equals the old one?
**Spot it:** "everything connected to this pixel with the same property".
**Model:** nodes = pixels, edges = 4-neighbours with the same colour.
**Solve:** save `original`. If it equals the new colour, return. Otherwise DFS and recolour.
**Cost:** O(R·C) time, O(R·C) recursion space.
**Follow-up:** Why the same-colour guard? (infinite recursion). Big image? (iterative stack or BFS.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Minesweeper reveal: clicking a cell with zero adjacent mines reveals it and keeps revealing connected zero cells and their border numbers.
- **Scenario:** In a minesweeper clone, the player clicks a safe tile. Implement what gets revealed.
- **Pattern and cost:** Flood fill with a rule: expand only from zero cells, but reveal the numbered border. DFS/BFS, O(R*C).

**Variant B**
- **Question:** Given two cells of the same grid, decide whether they lie in the same same-valued region. Many queries.
- **Scenario:** A map editor has terrain tiles. The user clicks two tiles. Are they in the same connected stretch of terrain?
- **Pattern and cost:** One query: flood fill, O(R*C). Many queries: label components once with Union-Find, then each query is O(alpha).

### S3. Max Area of Island (#3)

**Original question:** LC 695. Given a binary matrix, return the maximum area of an island (a 4-directionally connected group of 1s). Return 0 if there is none.

**Scenario:** Same binary image. Report the size of the biggest object.
**Ask first:** Do I also need its location? Does size mean pixel count?
**Spot it:** components, but you want a size instead of a count.
**Model:** same as S1.
**Solve:** `dfs` returns `1 + sum of four neighbours`. Sink before recursing. Track the max.
**Cost:** O(R·C) time and space.
**Follow-up:** Return the cells of the largest cluster too? Flip one `0` to get the largest cluster? (LC 827, Hard: label each island with its area, then check each `0`'s neighbours.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the size of the largest connected group of identical values in a matrix.
- **Scenario:** A seating chart colours each seat by department. What is the biggest block of seats belonging to one department?
- **Pattern and cost:** Same DFS that returns a size, with the neighbour check `value == value` instead of `== 1`. O(R*C).

**Variant B**
- **Question:** You may turn one 0 into 1. Return the largest island you can get (LC 827).
- **Scenario:** A developer may bulldoze exactly one empty plot and build there. What is the largest contiguous built-up area they can end with?
- **Pattern and cost:** Label every island with an id and its size. For every 0, add up the sizes of its distinct neighbouring ids, plus 1. O(R*C).

### S4. Walls and Gates (#5)

**Original question:** LC 286. Given an m x n grid where -1 is a wall, 0 is a gate and INF is an empty room, fill each empty room with the distance to its nearest gate. Leave INF if no gate is reachable.

**Scenario:** A warehouse floor is a matrix of shelves, charging docks and free floor. A robot can be on any free cell, and the firmware needs to know how far its closest dock is. Precompute that for the whole floor.
**Ask first:** Can robots pass through shelves? Can there be many docks? Can a cell have no reachable dock?
**Spot it:** "nearest X for **every** cell". Searching from each cell is too slow.
**Model:** nodes = walkable cells, edges = 4-neighbours, sources = all stations.
**Solve:** put **all** stations in the queue at distance 0. One BFS. First reach wins. Unreached cells stay INF.
**Cost:** O(R·C) time and space.
**Follow-up:** Why not BFS from each cell? (O((R·C)²).) A station is added later? (Run a BFS from it that only overwrites larger values.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Find the empty cell farthest from any land cell (LC 1162).
- **Scenario:** A company wants to open a store on an empty plot that is as far as possible from every existing store. How far is the best plot?
- **Pattern and cost:** Multi-source BFS from all stores, answer is the largest distance reached. O(R*C).

**Variant B**
- **Question:** Two sources expand at the same speed. For every cell, report which source reaches it first.
- **Scenario:** Two phone companies expand coverage by one block per day from their existing towers. For each block, which company gets there first?
- **Pattern and cost:** Multi-source BFS where each queue item carries its source label. Ties need a rule. O(R*C).

### S5. 01 Matrix (#6)

**Original question:** LC 542. Given a binary matrix, return for each cell the distance to the nearest 0. Cells that share a side are at distance 1.

**Scenario:** A city map is a matrix of hospitals and houses. For every house, report how far it is from care.
**Ask first:** How is distance measured? Can I walk through other houses?
**Spot it:** same signal as S4.
**Model:** sources = all `0`s, no walls.
**Solve:** `dist` grid starts at `-1`. Push all `0`s. BFS, writing `dist + 1`.
**Cost:** O(R·C) time and space.
**Follow-up:** Distance is not 1 per step (roads have different lengths)? (Then it needs Dijkstra, with all hospitals as sources.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Same as 01 Matrix, but moving between neighbouring cells has different costs.
- **Scenario:** A city has hospitals and houses, and each block has its own driving time to cross. For every house, the least travel time to any hospital.
- **Pattern and cost:** Multi-source Dijkstra, pushing every hospital at cost 0. O(R*C log(R*C)).

**Variant B**
- **Question:** Graph version: given towns and roads, return for every town the number of roads to the nearest depot.
- **Scenario:** A courier company has depots in some towns. For every town, how many road segments away is the nearest depot?
- **Pattern and cost:** Multi-source BFS on an adjacency list. O(V + E).

### S6. Rotting Oranges (#7)

**Original question:** LC 994. A grid has 0 (empty), 1 (fresh orange) and 2 (rotten orange). Every minute, a fresh orange next to a rotten one (4 directions) becomes rotten. Return the minutes until no fresh orange remains, or -1 if impossible.

**Scenario:** A ward has beds in a matrix, some with sick patients. Each day the illness reaches the neighbouring beds of anyone already sick. How many days until every patient is sick, or is that impossible?
**Ask first:** Are some cells empty? Are patients in all the other beds?
**Spot it:** "spreads each day" means BFS levels.
**Model:** nodes = beds, edges = 4-neighbours. Sources = infected.
**Solve:** count fresh. Multi-source BFS, one level per day (`for _ in range(len(queue))`). `fresh_count == 0` means return days, otherwise `-1`.
**Cost:** O(R·C) time and space.
**Follow-up:** Why `while queue and fresh > 0`? (avoids an extra empty minute.) Some patients recover after 2 days? (State now includes time, so the node becomes `(cell, days_infected)`.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the minimum number of rounds for a rumour that starts with several people to reach everyone, passing it along every link each round.
- **Scenario:** A few employees hear a rumour on Monday. Each day, everyone who knows it tells all their coworkers. How many days until the whole company knows?
- **Pattern and cost:** Multi-source BFS by levels on an adjacency list. Unreached nodes mean it is impossible. O(V + E).

**Variant B**
- **Question:** Return the minimum number of rounds to cover all stops when service spreads from several depots along bus routes.
- **Scenario:** A bus company opens service from several depots. Each week, every stop next to an open stop opens. How many weeks until every stop is served?
- **Pattern and cost:** Same BFS-by-levels. The answer is the number of levels, not the largest distance of one node. O(V + E).

### S7. Shortest Bridge (#8)

**Original question:** LC 934. An n x n binary matrix has exactly two islands. You may flip 0s to 1s. Return the smallest number of 0s to flip so the two islands connect.

**Scenario:** A map contains exactly two islands. Engineers can turn water into land. What is the fewest cells they must convert so you can walk from one island to the other?
**Ask first:** Is moving diagonally allowed? What counts as one island?
**Spot it:** shortest distance **between two groups**. Use one whole group as the source.
**Model:** nodes = cells, sources = every cell of island A.
**Solve:** DFS to find and colour island A, pushing its cells. Then BFS in layers through water until you touch a `1`. Return the layer count.
**Cost:** O(n²) time and space.
**Follow-up:** Why not try all pairs of cells? (too slow.) Three islands? (Join them with a minimum spanning tree. It gets harder.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Crossing a trail cell costs 0 and crossing any other cell costs 1. Find the cheapest route between two points.
- **Scenario:** A hiker walks from camp to a ridge. Walking on trails is free, and each off-trail tile costs one effort point. Least total effort?
- **Pattern and cost:** 0-1 BFS with a deque (or Dijkstra). O(R*C).

**Variant B**
- **Question:** Return the fewest introductions needed to connect any person in group A to any person in group B in a social network.
- **Scenario:** Two departments want to start working together. What is the fewest intermediate introductions that link someone in one to someone in the other?
- **Pattern and cost:** Multi-source BFS from all of A, stop at the first member of B. O(V + E).

### S8. Pacific Atlantic (#9)

**Original question:** LC 417. Given a height matrix, the Pacific touches the top and left edges and the Atlantic the bottom and right edges. Water flows to 4-neighbours with height less than or equal to the current cell. Return every cell that can flow to both oceans.

**Scenario:** A terrain height map is a matrix. Rain falls on every cell. The west and north edges are sea A, the east and south edges are sea B. Which cells have rain that can reach both seas?
**Ask first:** Can water move onto a cell of equal height? Does water move diagonally?
**Spot it:** "can reach the boundary". Running a search from every cell is too slow, so **reverse it**.
**Model:** edge from a cell to a neighbour that is **≥** its height (reverse flow). Sources = each ocean's border.
**Solve:** DFS uphill from each ocean's border into two sets. Return the intersection.
**Cost:** O(R·C) time and space.
**Follow-up:** Why `>=` and not `>`? (plateaus.) Three oceans? (Add a set, intersect all.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return every cell from which you can reach the border moving only to cells of equal or lower height.
- **Scenario:** Hikers on a terrain map want to reach a road on the edge of the map without ever climbing. Which starting spots work?
- **Pattern and cost:** Reverse it: search from the border going uphill, and collect the cells reached. O(R*C).

**Variant B**
- **Question:** In a directed service-call graph, return the services that can transitively reach both the payment and the auth service.
- **Scenario:** Microservices call each other. Which services can end up calling both Payments and Auth, directly or through others?
- **Pattern and cost:** Reverse the edges, BFS from each target, intersect the two sets. O(V + E).

### S9. Surrounded Regions (#10)

**Original question:** LC 130. Given a board of X and O, capture every region of O that is completely surrounded by X by flipping it to X. Regions touching the border are not captured.

**Scenario:** In a board game with X and O pieces, every group of O pieces that is completely enclosed by X pieces gets captured. Apply the capture.
**Ask first:** Does being on the edge count as enclosed? Does a diagonal link count?
**Spot it:** "not touching the border" means start from the border.
**Model:** nodes = `O` cells, edges = 4-neighbours.
**Solve:** DFS from every border `O`, marking `T` (safe). Then `O → X` and `T → O`.
**Cost:** O(R·C) time and space.
**Follow-up:** Why not check each region directly? (awkward.) Diagonal touch counts? (No, 4 directions.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Count the water regions that are not connected to the edge of the map (closed islands / lakes, LC 1254).
- **Scenario:** A map shows water and land. How many lakes are fully enclosed by land, so no water reaches the map edge?
- **Pattern and cost:** Flood from the border to remove edge water, then count the components that remain. O(R*C).

**Variant B**
- **Question:** In a directed call graph, find the functions that cannot be reached from any entry point.
- **Scenario:** A code base has public entry points. Which functions can never be called from them (dead code)?
- **Pattern and cost:** Multi-source DFS/BFS from all entry points. Anything unvisited is dead. O(V + E).

### S10. Clone Graph (#12)

**Original question:** LC 133. Given a reference to a node in a connected undirected graph, return a deep copy of the graph. Each node has a value and a list of neighbours.

**Scenario:** You get a reference to one user in a social network. Each user object holds a list of references to their friends. Return an independent copy of the whole network.
**Ask first:** Can the network have cycles? Is it connected? Are there duplicate friendships?
**Spot it:** "deep copy" of linked structures with cycles.
**Model:** nodes = users, edges = friend pointers.
**Solve:** DFS with `old_to_new`. If seen, return its clone. Otherwise create and **register before recursing**, then clone the neighbours.
**Cost:** O(V + E) time, O(V) space.
**Follow-up:** Why register before recursing? (cycles.) Very deep chain? (BFS.) Node pointers vs ids?

**More scenarios on the same pattern**

**Variant A**
- **Question:** Deep copy a linked list where each node also has a random pointer (LC 138).
- **Scenario:** A playlist has songs in order, and each song also points to a 'recommended next' song anywhere in the list. Duplicate the whole playlist.
- **Pattern and cost:** Hashmap old to new in two passes. O(n) time and space.

**Variant B**
- **Question:** Copy a folder structure where shortcuts can point anywhere, including back up the tree.
- **Scenario:** A backup tool must copy a directory tree where symlinks can create loops. Duplicate it without infinite looping or copying a folder twice.
- **Pattern and cost:** DFS/BFS with old to new map, registered before recursing. O(V + E).

### S11. Course Schedule (#13)

**Original question:** LC 207. There are numCourses courses and prerequisite pairs [a, b], meaning take b before a. Return true if you can finish all courses.

**Scenario:** A CI system has jobs, and some jobs can only start after others finish. Given the config, is it valid, meaning can every job run?
**Ask first:** Can a job depend on itself? What does the input look like?
**Spot it:** "must come before" means directed, and "can all finish" means **no cycle**.
**Model:** nodes = tasks, edge `prereq → task`.
**Solve:** Kahn. Indegrees, queue the zeros, pop and decrement. `processed == n` means True.
**Cost:** O(V + E) time and space.
**Follow-up:** Self-dependency? (cycle.) Report **which** tasks are stuck? (those never popped.) DFS version? (3-colour: unvisited, visiting, done.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Detect a circular import and report one cycle.
- **Scenario:** A repo has modules that import each other. Is there a circular import, and which modules form it?
- **Pattern and cost:** DFS with 3 states (unvisited, visiting, done) and a path stack. Finding a 'visiting' node means a cycle. O(V + E).

**Variant B**
- **Question:** A spreadsheet has cells whose formulas reference other cells. Can every cell be evaluated?
- **Scenario:** A spreadsheet cell can reference other cells in its formula. Can the sheet be calculated, or is there a circular reference?
- **Pattern and cost:** Kahn's algorithm. Fewer evaluated cells than total means a cycle. O(V + E).

### S12. Course Schedule II (#14)

**Original question:** LC 210. Same input as Course Schedule. Return an order in which to take all the courses, or an empty list if that is impossible.

**Scenario:** Same CI system. Output an order to run the jobs. Then: if independent jobs can run in parallel, how many rounds does the pipeline need at minimum?
**Ask first:** Is any valid order fine? How many jobs and dependencies?
**Spot it:** "a valid order" means topological sort.
**Solve:** Kahn, appending in pop order. A short list means a cycle, so return `[]`.
**Cost:** O(V + E).
**Follow-up:** Many valid answers? (any is fine.) Run independent tasks in parallel, what's the minimum number of rounds? (Kahn **by levels**, answer = number of levels.) Lexicographically smallest order? (use a min-heap instead of a queue.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the minimum number of semesters to finish all courses if you can take any number each semester (LC 1136).
- **Scenario:** A degree has courses with prerequisites and no limit on how many you take per term. What is the fewest terms to graduate?
- **Pattern and cost:** Kahn by levels. Number of levels is the answer, -1 if a cycle exists. O(V + E).

**Variant B**
- **Question:** Return the valid order that is smallest alphabetically.
- **Scenario:** Services must deploy after the ones they depend on. When several are ready, deploy the alphabetically first. What is the deployment order?
- **Pattern and cost:** Kahn with a min-heap instead of a queue. O(V log V + E).

### S13. Alien Dictionary (#15)

**Original question:** LC 269. You get a list of words sorted by the rules of an unknown language. Return a string of the unique letters in that language's order (any valid one), or an empty string if the input is invalid.

**Scenario:** You find a dictionary of an unknown language. The words are listed in that language's sorted order. Recover the alphabet order.
**Ask first:** Is the answer unique? What if the data is contradictory?
**Spot it:** order is **hidden in the data**. Build the dependency edges yourself.
**Model:** nodes = letters, edge `a → b` from the first differing letter of **adjacent** words.
**Solve:** register every letter. Add edges (skip duplicates). Handle the prefix trap (`"abc"` before `"ab"` means `""`). Kahn. Short result means a cycle, so `""`.
**Cost:** O(C) time (total characters), O(1) space (≤ 26 letters).
**Follow-up:** Why only adjacent pairs? (transitivity.) Is the answer unique? (only if the queue never has 2 items.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Reconstruct a total order from pairwise 'X before Y' facts.
- **Scenario:** An incident log says things like 'A happened before B' and 'B before C', in no particular order. Recover the sequence of events.
- **Pattern and cost:** Build a directed graph from the facts and topologically sort it. O(V + E).

**Variant B**
- **Question:** Return whether a sequence is uniquely determined by a set of observed subsequences (LC 444).
- **Scenario:** You have several partial observations of a sequence of events. Is the full sequence uniquely determined?
- **Pattern and cost:** Kahn, and the order is unique only if the queue never holds more than one node. O(V + E).

### S14. Minimum Height Trees (#16)

**Original question:** LC 310. A tree has n nodes and n-1 edges. Choosing a node as the root gives a tree of some height. Return all roots that give the minimum height.

**Scenario:** n data centres are connected by cables, with no redundant links, and every site can reach every other. Pick the site for the control tower so the worst-case number of hops to any site is as small as possible.
**Ask first:** Can there be several answers? Is every cable the same length?
**Spot it:** "best root" or "centre" of a tree.
**Solve:** peel leaves layer by layer (degree 1) until at most 2 nodes remain. Those are the centres. Handle `n ≤ 2` first.
**Cost:** O(n) time and space.
**Follow-up:** Why at most 2 answers? (the centre of the longest path.) Brute force? (BFS from each node, O(n²).)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the diameter of a tree, meaning the longest path between any two nodes.
- **Scenario:** Offices are linked by cables in a loop-free network. What is the largest hop count between any two offices?
- **Pattern and cost:** BFS from any node to the farthest, then BFS again from there. O(n).

**Variant B**
- **Question:** Return the time to inform every employee when each manager takes a given time to inform their direct reports (LC 1376).
- **Scenario:** A CEO announces news, and each manager takes some minutes to pass it to direct reports. When does the last employee hear?
- **Pattern and cost:** DFS/BFS over the management tree, taking the max of accumulated time. O(n).

### S15. Longest Increasing Path (#17)

**Original question:** LC 329. Given an m x n matrix, return the length of the longest strictly increasing path. You may move in 4 directions, with no wrap-around.

**Scenario:** A hiking map is a matrix of elevations. You only ever step to a strictly higher spot. What is the longest hike possible?
**Ask first:** Can I start anywhere? Is a flat step allowed?
**Spot it:** "strictly increasing" means **no cycles**, so it's a DAG, and "longest path" means DFS + memo.
**Model:** edge from a cell to each strictly larger neighbour.
**Solve:** `dfs(cell) = 1 + max(dfs(bigger neighbours))`, cached in `memo`. Max over all cells.
**Cost:** O(R·C) time and space.
**Follow-up:** Why no visited set? (strict `>` rules out cycles.) Recursion too deep? (Kahn peeling, count the layers.) Allow equal steps? (cycles appear, so it would need Tarjan SCC.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the longest path in a directed acyclic graph with task durations on the nodes.
- **Scenario:** A project has tasks with durations and dependencies. What is the shortest possible project length if independent tasks run in parallel?
- **Pattern and cost:** Topological order plus DP (critical path). O(V + E).

**Variant B**
- **Question:** Count all strictly increasing paths in the matrix, mod 1e9+7 (LC 2328).
- **Scenario:** On a hiking map where you only go uphill, how many different routes exist in total, starting from anywhere?
- **Pattern and cost:** DFS + memo where each cell returns the number of routes starting there. O(R*C).

### S16. Redundant Connection (#18)

**Original question:** LC 684. A graph started as a tree with n nodes, then one extra edge was added. Given the edges, return an edge that can be removed so the result is a tree. If there are several, return the one that appears last in the input.

**Scenario:** You receive a stream of records (a, b) meaning a and b are linked. Exactly one record is redundant, because it adds nothing the earlier records didn't already imply. Find it.
**Ask first:** If several qualify, which one? Is the link directional?
**Spot it:** "loop", "extra", processing edges in order.
**Solve:** Union-Find. For each edge, if the two ends already share a root, return it.
**Cost:** O(n log n), near O(n) with rank. O(n) space.
**Follow-up:** DFS alternative? (O(n²).) Directed version? (LC 685, harder.) Recursive `find` with no rank can go deep, so use rank or iterative.

**More scenarios on the same pattern**

**Variant A**
- **Question:** Directed version (LC 685): a rooted tree gets one extra directed edge. Return the edge to remove.
- **Scenario:** A company's reporting records now contain one extra line: either a person with two managers or a loop. Which record should be deleted?
- **Pattern and cost:** Cases: a node with two parents (try each), or a cycle. Union-Find plus indegree check. O(n alpha). Hard, mention the cases.

**Variant B**
- **Question:** Return the fewest cable moves needed to connect all n computers (LC 1319).
- **Scenario:** A lab has n computers and some cables. You can unplug a cable and re-plug it elsewhere. What is the fewest moves to connect everyone, or is it impossible?
- **Pattern and cost:** Union-Find. Count components c and spare edges. Possible if edges >= n-1, and the answer is c-1. O(n + E alpha).

### S17. Graph Valid Tree (#19)

**Original question:** LC 261. Given n nodes labelled 0 to n-1 and a list of undirected edges, return true if the edges form a valid tree.

**Scenario:** Given n people and a list of direct-report pairs, check whether it describes one valid org chart.
**Ask first:** Can there be multiple roots? Is the link directional?
**Spot it:** "valid tree" means n−1 edges, connected, no cycle.
**Solve:** if `len(edges) != n-1` return False. Then Union-Find (any union that fails means a cycle), or one DFS that must reach all n nodes.
**Cost:** O(n log n) with Union-Find, O(n) with DFS.
**Follow-up:** Why is the count check enough with one more condition? (n−1 edges plus no cycle gives connected. n−1 edges plus connected gives no cycle.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Given left and right child arrays for n nodes, check whether they form exactly one valid binary tree (LC 1361).
- **Scenario:** A tool exports a hierarchy as 'left child' and 'right child' arrays. Does it describe one proper tree?
- **Pattern and cost:** Exactly one node with indegree 0, no node with indegree over 1, and all nodes reachable. O(n).

**Variant B**
- **Question:** Return how many edges must be removed so that n towns with roads form a tree (or say it is impossible).
- **Scenario:** A region has n towns and too many roads. How many roads can be closed while keeping everyone connected with no loops?
- **Pattern and cost:** Union-Find. If not connected, impossible. Otherwise answer is E - (n-1). O(E alpha).

### S18. Number of Connected Components (#20)

**Original question:** LC 323. Given n nodes and a list of undirected edges, return the number of connected components.

**Scenario:** A login log has pairs of account IDs that were used on the same device. Assuming one person owns all linked accounts, how many distinct people are there?
**Ask first:** If A shares with B and B with C, are A and C the same person? Do the pairs arrive as a stream?
**Spot it:** "isolated groups".
**Solve:** Union-Find, start at `n` and subtract 1 for each successful merge. Or DFS counting starts.
**Cost:** O(n + E log n) Union-Find, O(n + E) DFS.
**Follow-up:** Links arrive as a **stream** and you must report the count after each? (Union-Find wins, because DFS would need to restart.) Links can be **removed** too? (offline reverse, or dynamic connectivity.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Merge accounts that share any email, then output each merged account (LC 721).
- **Scenario:** A CRM has customer records, each with several emails. Records sharing any email are the same person. Produce one merged record per person.
- **Pattern and cost:** Union-Find over the records (or emails), group by root, sort emails. O(N L log(NL)).

**Variant B**
- **Question:** Return the size of the largest connected group.
- **Scenario:** Given linked machines, how many machines are in the biggest sub-network?
- **Pattern and cost:** Union-Find with a size array, or DFS tracking component size. O(n + E alpha).

### S19. Number of Provinces (#21)

**Original question:** LC 547. There are n cities and an n x n matrix isConnected. A province is a group of directly or indirectly connected cities. Return the number of provinces.

**Scenario:** You get an n x n matrix where 1 means two people know each other. If you count friend-of-a-friend as in the same circle, how many circles are there?
**Ask first:** Is the matrix symmetric? Do people know themselves?
**Spot it:** components, but the input is an **adjacency matrix**.
**Solve:** DFS over rows, counting starts. Or Union-Find with `count = n`.
**Cost:** O(n²) time because you must read the matrix, O(n) space.
**Follow-up:** Why can't it be faster? (you have to read n² cells.) If given a list of edges instead? (O(n + E).)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Given equations 'a == b' and 'a != b', decide whether they can all be true (LC 990).
- **Scenario:** A config file has rules that say two variables must be equal and others that say they must differ. Is the config consistent?
- **Pattern and cost:** Union all '==' pairs first, then check every '!=' pair is in different groups. O(n alpha).

**Variant B**
- **Question:** Group strings where two strings are similar if one swap of two letters makes them equal (LC 839). Return the number of groups.
- **Scenario:** A spell-checker treats two words as 'close' if swapping two letters turns one into the other. How many families of close words exist?
- **Pattern and cost:** Union-Find, comparing every pair. O(n^2 L).

### S20. Is Graph Bipartite? (#23)

**Original question:** LC 785. Given an undirected graph as an adjacency list, return true if it is bipartite: the nodes can be split into two sets so that every edge connects the two sets.

**Scenario:** Users interact with each other. We want to run an A/B experiment where two users who interact are never in the same arm. Is that possible?
**Ask first:** Can I choose the arms freely? What if it is impossible?
**Spot it:** "two groups, never inside one group".
**Solve:** BFS 2-colouring (`1`, `-1`, `0` = unseen) from every uncoloured node. A same-colour neighbour means False.
**Cost:** O(V + E) time, O(V) space.
**Follow-up:** What does failure mean? (an odd cycle.) Disconnected? (outer loop.) Return the two groups? (collect by colour.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Split teams into two conferences so that no two teams who are rivals are in the same conference, and return an assignment.
- **Scenario:** A league wants two conferences, with every rivalry pair split across them. Produce a split if it exists.
- **Pattern and cost:** BFS 2-colouring, then group by colour. O(V + E).

**Variant B**
- **Question:** Return whether the graph has an odd-length cycle.
- **Scenario:** A checkers-style rotation requires partners to alternate sides. Can everyone alternate, or does some loop of odd length break it?
- **Pattern and cost:** Same as bipartite check: an odd cycle exists if and only if it is not bipartite. O(V + E).

### S21. Possible Bipartition (#24)

**Original question:** LC 886. Split n people (labelled 1 to n) into two groups so that no two people who dislike each other are in the same group. Given the dislike pairs, return whether that is possible.

**Scenario:** An event has two tables and a list of guest pairs who refuse to sit together. Can you seat everyone?
**Ask first:** Is the table size limited? Can a guest have many conflicts?
**Spot it:** conflict pairs and two teams. It's S20 with the graph **built from an edge list**.
**Solve:** build an undirected adjacency list, then BFS 2-colour. People are `1…n`, so size `color` as n+1.
**Cost:** O(n + E).
**Follow-up:** Three teams? (graph colouring is NP-hard in general.) Minimum people to remove? (hard.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Process 'enemy' pairs as they arrive and report the first one that makes a two-group split impossible.
- **Scenario:** Rival logs from a game stream in one at a time. After which log does it become impossible to assign everyone to two gangs consistently?
- **Pattern and cost:** Union-Find with an enemy pointer per node (or parity DSU). O(E alpha).

**Variant B**
- **Question:** Split tournament teams into two pools so no two teams who already played each other are in the same pool.
- **Scenario:** A tournament has two pools, and teams that already met in earlier rounds must go to different pools. Is that possible?
- **Pattern and cost:** Bipartite check on the 'already played' graph. O(V + E).

### S22. Evaluate Division (#25)

**Original question:** LC 399. Given equations like A / B = value, answer queries C / D. Return -1.0 for any query that cannot be determined.

**Scenario:** You are given exchange rates for some pairs of currencies. Answer queries of the form how much X for 1 Y, or say it is unknown.
**Ask first:** Are the rates consistent? Is a query about an unseen currency possible?
**Spot it:** "convert through intermediate steps" with multiplication.
**Model:** nodes = currencies, edges both ways with weights `v` and `1/v`.
**Solve:** per query BFS or DFS carrying the product. Unknown node or no path returns -1.
**Cost:** O(E + Q·(V + E)) time, O(V + E) space.
**Follow-up:** Many queries? (Weighted Union-Find, near O(1) per query.) Rates that change? (rebuild the changed edges.) Find an arbitrage opportunity? (a cycle with product > 1, so use Bellman-Ford on `-log`.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Check whether the given equations contradict each other.
- **Scenario:** A set of unit conversions says 1 km = 1000 m, 1 m = 100 cm and 1 km = 90000 cm. Is the data consistent?
- **Pattern and cost:** Traverse each component computing ratios. A mismatch against an already-assigned ratio means a contradiction. O(V + E).

**Variant B**
- **Question:** Answer 100,000 conversion queries over a fixed set of unit relations.
- **Scenario:** A unit-conversion service handles a huge stream of queries over a fixed table of unit relations. Make each query fast.
- **Pattern and cost:** Weighted Union-Find storing each node's ratio to its root. Query is O(alpha) after O(E alpha) build.

### S23. Network Delay Time (#26)

**Original question:** LC 743. Given directed edges (u, v, w) meaning a signal takes w to travel from u to v, and a start node k, return the time for all n nodes to receive the signal, or -1 if some never do.

**Scenario:** A software update is pushed to one server. Each server forwards it to the servers it is linked to, and each link has a known latency. When has every server got it, or is that impossible?
**Ask first:** Are links one-way? Can latency be zero or negative?
**Spot it:** "minimum time", with different weights, from one source, and the answer is the **slowest** node.
**Solve:** Dijkstra with `dist` and a heap, skipping stale entries. Return `max(dist)`, or -1 if any is `inf`.
**Cost:** O((V + E) log V) time, O(V + E) space.
**Follow-up:** All links have time 1? (plain BFS.) Negative times? (Bellman-Ford.) Why does Dijkstra fail with negatives? (a "final" node can be improved later.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Each edge has a success probability. Return the most reliable path from start to end (LC 1514).
- **Scenario:** Each link in a network drops packets with a known probability. Which route from A to B is the most likely to deliver?
- **Pattern and cost:** Dijkstra with a max-heap on probability (multiply, never increases). O((V + E) log V).

**Variant B**
- **Question:** Return the city with the fewest cities reachable within a distance threshold (LC 1334).
- **Scenario:** A telecom wants the city that has the fewest neighbouring cities within 50 km by road. Which city?
- **Pattern and cost:** Floyd-Warshall O(V^3), or Dijkstra from each city O(V (V + E) log V).

### S24. Swim in Rising Water (#27)

**Original question:** LC 778. In an n x n grid of elevations, at time t the water depth is t everywhere. You can swim between 4-adjacent cells if both elevations are at most t. Return the least time to get from the top-left to the bottom-right.

**Scenario:** In a flood-prone area, the terrain is a matrix of elevations, and the water level rises by one unit per hour. You can only wade through cells at or below the water level. What is the earliest hour you can get from one corner to the opposite corner?
**Ask first:** Can I wait? Are all elevations different?
**Spot it:** the cost of a route is **its worst cell**, not a sum.
**Solve:** Dijkstra with `new_t = max(t, grid[nr][nc])`. Return `t` when the target is popped.
**Cost:** O(n² log n) time, O(n²) space.
**Follow-up:** Another way? (binary search on `t` plus BFS, or Union-Find adding cells in height order.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the maximum, over all routes, of the minimum value on the route (LC 1102).
- **Scenario:** A drone flies from one corner to the opposite on a terrain map. Its safety is the lowest altitude it passes over. Which route maximises that?
- **Pattern and cost:** Dijkstra with a max-heap and `min` instead of `max`. O(R*C log(R*C)).

**Variant B**
- **Question:** In a graph, choose a route so the most expensive single edge on it is as small as possible.
- **Scenario:** A convoy picks a route between two cities. It only cares about the single most expensive toll on the way. Which route minimises that?
- **Pattern and cost:** Dijkstra with `max` on a graph, or Kruskal/Union-Find until the two cities join. O(E log V).

### S25. Path With Minimum Effort (#28)

**Original question:** LC 1631. Given a matrix of heights, the effort of a route is the maximum absolute height difference between consecutive cells. Return the minimum effort from the top-left to the bottom-right.

**Scenario:** A hiker crosses a matrix of heights. The effort of a route is its single largest height jump between consecutive cells. Find the least-effort route from one corner to the opposite.
**Ask first:** Is the effort a sum or a maximum? Can I revisit cells?
**Spot it:** same as S24, with the cost on the **edge**.
**Solve:** Dijkstra with `new_e = max(e, |diff|)`.
**Cost:** O(R·C log(R·C)) time, O(R·C) space.
**Follow-up:** Binary search on the answer plus BFS gives O(R·C log H). Union-Find (Kruskal-style) also works.

**More scenarios on the same pattern**

**Variant A**
- **Question:** Connect all n points at the least total cost, where cost is the Manhattan distance between two points (LC 1584).
- **Scenario:** A company must connect n offices with cable. The cost between two offices is the straight-line distance. Cheapest way to link them all?
- **Pattern and cost:** Minimum spanning tree: Prim's O(n^2) or Kruskal O(E log E). This is problem #32 in your tracker, not yet written up.

**Variant B**
- **Question:** Return the route that maximises the weakest edge on it.
- **Scenario:** A truck's maximum load along a route is limited by the weakest bridge on it. Which route allows the heaviest truck from A to B?
- **Pattern and cost:** Dijkstra with a max-heap and `min`, or Kruskal on edges sorted descending. O(E log V).

### S26. Number of Ways to Arrive (#29)

**Original question:** LC 1976. Given n intersections and bidirectional roads (u, v, time), return the number of ways to get from 0 to n-1 in the shortest possible time, mod 1e9+7.

**Scenario:** Given a road network with travel times, count how many different fastest routes there are from the first intersection to the last. Return it mod 1e9+7.
**Ask first:** Are roads two-way? Can a time be zero?
**Spot it:** "how many fastest ways".
**Solve:** Dijkstra with `ways[]`. A strictly shorter route means copy `ways`. An equal route means add. `ways[0] = 1`.
**Cost:** O((V + E) log V) time, O(V + E) space.
**Follow-up:** Why does it break with zero-time roads? (a node could be popped before getting its last addition.) All times equal? (BFS with counts.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Count the minimum-hop routes between two nodes in an unweighted graph.
- **Scenario:** How many different shortest-hop flight itineraries exist from airport A to airport B?
- **Pattern and cost:** BFS keeping a `ways` array: when reaching a node at the same level, add. O(V + E).

**Variant B**
- **Question:** Return the actual shortest route, not just its length.
- **Scenario:** A navigation app must show the fastest route itself, step by step, not only the arrival time.
- **Pattern and cost:** Dijkstra with a `parent` array, then walk back from the destination. O((V + E) log V).

### S27. Cheapest Flights Within K Stops (#30)

**Original question:** LC 787. Given flights (from, to, price), return the cheapest price from src to dst with at most k stops, or -1.

**Scenario:** Given a list of flights with prices, find the cheapest way from A to B with at most K layovers.
**Ask first:** Is cheapest the same as fewest stops? What if it is impossible?
**Spot it:** a cost **plus a limit on the number of steps**. Plain Dijkstra picks the wrong path.
**Solve:** Bellman-Ford for `K+1` rounds. Each round reads `prices` and writes `temp`.
**Cost:** O(K·(n + E)) time, O(n) space.
**Follow-up:** Why the copy? (otherwise one round chains several flights.) Why not Dijkstra? (the cheapest path may use too many stops, so you'd need state `(node, stops)`.) BFS by levels also works.

**More scenarios on the same pattern**

**Variant A**
- **Question:** You have K coupons that each make one road toll free. Find the cheapest trip (LC 2093).
- **Scenario:** On a road trip, you can use up to K toll coupons, each making one road free. What is the cheapest route?
- **Pattern and cost:** Dijkstra on state (node, coupons used). O(K (V + E) log(K V)).

**Variant B**
- **Question:** Detect a loop of trades that makes a profit, with prices that can be negative.
- **Scenario:** Several markets let you trade goods with fees and bonuses. Is there a loop of trades that ends with more than you began with?
- **Pattern and cost:** Bellman-Ford with a V-th round: if any distance still improves, a negative cycle exists. O(V E).

### S28. Snakes and Ladders (#33)

**Original question:** LC 909. An n x n board is numbered in a zig-zag from the bottom-left. From square x you move to x+1 ... x+6. If the square has a snake or ladder, you move to its end. Return the fewest moves to reach square n squared, or -1.

**Scenario:** A board game has squares numbered 1 to n squared, a six-sided die, and some squares that teleport you forward or back. What is the fewest rolls to finish?
**Ask first:** Can a teleport chain into another? What if the end is unreachable?
**Spot it:** "fewest moves", with a **graph that isn't given**.
**Model:** nodes = squares, edges = rolls 1–6 (to the jump destination).
**Solve:** BFS from square 1 with `(cell, moves)`. Convert a square number to `(row, col)` using the zig-zag formula. Mark the **destination** as visited.
**Cost:** O(n²) time and space.
**Follow-up:** Why not a DP? (jumps back make it cyclic.) Why BFS and not Dijkstra? (every roll costs 1.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the fewest jumps to reach the last index when position i lets you jump to any index within a[i] (LC 45).
- **Scenario:** A frog crosses stepping stones, and each stone says how far it can jump from there. Fewest jumps to the far bank?
- **Pattern and cost:** BFS over indices (or greedy by levels). O(n).

**Variant B**
- **Question:** Return the fewest turns to open a 4-wheel combination lock, avoiding trap combinations (LC 752).
- **Scenario:** A 4-digit lock has wheels 0-9. One move turns one wheel one step. Some codes lock it forever. Fewest moves to open?
- **Pattern and cost:** BFS over states: 10^4 states, 8 moves each. O(10^4 * 8).

### S29. Minimum Genetic Mutation (#34)

**Original question:** LC 433. A gene is 8 characters from A, C, G, T. One mutation changes one character, and the result must be in the bank. Return the fewest mutations from startGene to endGene, or -1.

**Scenario:** A lab tracks DNA strands of 8 bases. One mutation changes one base, and the result must be on an approved list. What is the fewest mutations to turn strand A into strand B?
**Ask first:** Does the start need to be on the list? What if B is not on it?
**Spot it:** "fewest changes", where each state is a string.
**Model:** nodes = valid genes, edge = differ by one letter.
**Solve:** BFS from the start. Try each position × `ACGT`. If it's in the bank set, push it and remove it from the set.
**Cost:** O(B·L²) time, O(B·L) space.
**Follow-up:** Is generating neighbours better than comparing all pairs? (depends on alphabet size vs bank size.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Return the fewest presses to turn x into y on a calculator that can double or subtract one (LC 991).
- **Scenario:** A broken calculator has two buttons: double and minus one. Fewest presses to turn a given number into a target?
- **Pattern and cost:** BFS over numbers (or greedy working backwards from y). States stay bounded.

**Variant B**
- **Question:** Return the fewest moves to solve a 2x3 sliding puzzle (LC 773).
- **Scenario:** A 2x3 tile puzzle has five tiles and a gap. Fewest moves to reach the solved layout, or is it unsolvable?
- **Pattern and cost:** BFS over board strings, at most 720 states. O(states * moves).

### S30. Word Ladder (#35)

**Original question:** LC 127. Given beginWord, endWord and a word list, find the shortest sequence where each step changes one letter and every word is in the list. Return the number of words in it, or 0.

**Scenario:** Transform one word into another by changing one letter at a time, where every intermediate word must be in a dictionary. How long is the shortest sequence?
**Ask first:** Do I count words or steps? Is the start word in the dictionary?
**Spot it:** same as S29, and the answer counts **words**.
**Solve:** BFS with `(word, length)` starting at 1. Try each position × `a–z`. Remove from the set when you push.
**Cost:** O(N·L²·26) time, O(N·L) space.
**Follow-up:** **Bidirectional BFS** (grow the smaller side). Print all shortest ladders? (LC 126: BFS to build parents, then DFS to rebuild.) Wildcard-bucket trick (`h*t`) to avoid 26 tries.

**More scenarios on the same pattern**

**Variant A**
- **Question:** Print every shortest transformation sequence (LC 126).
- **Scenario:** A spell tool wants to list every shortest chain of one-letter edits between two words.
- **Pattern and cost:** BFS to record parents at each level, then DFS back from the end to build all paths. Output-sensitive.

**Variant B**
- **Question:** Find the degrees of separation between two people in a huge social network quickly.
- **Scenario:** A social app with millions of users shows 'you are 4 connections away from X'. Make it fast.
- **Pattern and cost:** Bidirectional BFS, growing the smaller frontier. About O(b^(d/2)) instead of O(b^d).

### S31. Shortest Path in Binary Matrix (#36)

**Original question:** LC 1091. In an n x n binary matrix, return the length of the shortest clear path (all 0s, 8-directionally connected) from the top-left to the bottom-right, or -1.

**Scenario:** A robot moves across free cells of a warehouse matrix, including diagonally. What is the length of its shortest route from the top-left to the bottom-right?
**Ask first:** Can the start or the end be blocked? Do I count cells or moves?
**Spot it:** "shortest path", every step costs the same, on a grid.
**Solve:** if either corner is blocked, return -1. BFS from `(0,0,1)`, mark cells when pushed, return `dist` at the target.
**Cost:** O(n²) time and space.
**Follow-up:** Diagonal moves cost more? (Dijkstra.) Can break one wall? (state `(r, c, broken)`.) Return the path itself? (store parents.)

**More scenarios on the same pattern**

**Variant A**
- **Question:** Same grid, but you may break up to k walls (LC 1293).
- **Scenario:** A robot in a warehouse can smash up to k crates on its way. Shortest route length?
- **Pattern and cost:** BFS over state (r, c, walls used). O(R*C*k).

**Variant B**
- **Question:** Each cell has a toll. Find the cheapest path, not the shortest.
- **Scenario:** Every tile of a map costs a different amount to cross. What is the cheapest route from corner to corner?
- **Pattern and cost:** Dijkstra on the grid. O(R*C log(R*C)).

---

## Part 5. Common traps to say out loud

1. **Mark visited when you push** (BFS), not when you pop, or the queue explodes.
2. **Multi-source BFS** whenever the question says "nearest" or "every cell".
3. **BFS only for equal edge costs.** The moment costs differ, think Dijkstra.
4. **Dijkstra needs non-negative weights.** Negative or a step limit means Bellman-Ford.
5. **Directed graph + cycle question** means Kahn or 3-colour DFS. **Undirected + cycle** means Union-Find (or DFS with parent).
6. **Disconnected input:** loop over every node as a start.
7. **Recursion depth:** big grids or long chains blow Python's limit. Offer the iterative version.
8. **Mutating the input:** say it, and offer a copy or a visited set.

## Part 6. Known gaps (not written up yet)

Problems the repo hasn't covered that Google asks often: **#22 Accounts Merge** (Union-Find on strings), #4 Making a Large Island, #31 Floyd-Warshall (City with Fewest Neighbours), #32 Min Cost to Connect All Points (MST), #37–#40.
