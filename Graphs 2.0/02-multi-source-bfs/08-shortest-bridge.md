# 934. Shortest Bridge

**LC 934** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** DFS to collect one whole island, then multi-source BFS from all its cells (level by level)

---

## 1. Intuition

There are exactly two islands. First, find one of them and paint it a different colour, so the two can be
told apart. Then let that whole island "grow" into the water one layer at a time. The number of layers it
takes to touch the other island is the number of water cells you'd have to flip.

* **DFS collects the sources:** `dfs` paints every cell of the first island `2` *and* does `queue.append((r, c))`. So when the scan ends, `queue` holds the entire first island, and it becomes the starting layer of the BFS.
* **Stop after the first island:** the `found` flag breaks out of *both* loops, so the second island stays as `1`. The BFS uses those `1`s as its target.
* **One BFS level = one more water cell flipped:** `for _ in range(len(queue))` processes one layer, and `distance += 1` runs after each full layer. Water is painted `2` (visited) when it's pushed.
* **`return distance` as soon as a neighbour is `1`:** the first time any cell in the current layer touches a `1`, the bridge length is the number of completed layers. The first island's own cells were already turned into `2`, so any `1` the BFS meets must belong to the second island.

**Recall:** DFS the first island to `2` and push all its cells. BFS through the water in layers. The first `1` you touch → return `distance`.

## 2. Approach

* **Idea:** Island-to-island shortest path = multi-source BFS that starts from **every** cell of island A at distance 0 and stops at the first cell of island B.
* **Graph representation:** implicit **grid** graph (n × n), undirected and unweighted. Moves go in **4 directions**, from `directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]` (right, left, down, up).
* **Data structure / pointers:**
  * `grid` is the visited marker. `2` means "island A, or water already reached", `1` means island B (the target), and `0` means water not yet reached. Island A cells are painted when `dfs` enters them, and water cells are painted **when they are pushed**.
  * `queue` (`deque`): it starts with every island-A cell, then holds each layer of water around it.
  * `distance`: the number of completed BFS layers, which is the number of water cells flipped so far.
  * `found`: breaks out of both scan loops after the first island is painted.
  * Out-of-bounds is checked with `0 <= nr < n and 0 <= nc < n` before `grid[nr][nc]` is read, in both `dfs` and the BFS.
* **Invariant:** at the start of each pass, `queue` holds exactly the cells that are `distance` water-flips away from island A. No cell closer than that touches island B, otherwise the code would have returned already.
* **Edge cases:**
  * Islands one water cell apart: layer 0 (island A) marks that water cell, and layer 1 pops it and sees a `1`, so it returns `1`. It **can't** return `0`, because two land cells that touch would be one island, not two.
  * One island wrapped around the other: fine, because the BFS grows evenly in all directions, so the closest gap is found first.
  * Exactly two islands are guaranteed, so the BFS always reaches a `1` and returns from inside the loop. The final `return distance` only runs if that rule is broken (for example, only one island).
  * **Recursion depth:** `dfs` goes one call deeper per cell of island A. On a 100 × 100 grid (the LC maximum), island A can have thousands of cells, which is above Python's default limit of 1,000. That raises `RecursionError` when you run it locally. An iterative stack or BFS for step 1 avoids this.
  * It changes `grid` in place (island A and every water cell it reaches become `2`).

## 3. Code

```python
from collections import deque


class Solution:

    def shortestBridge(self, grid: list[list[int]]) -> int:
        n = len(grid)
        queue = deque()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        island_id = 2

        # Step 1: DFS helper to explore and mark the entirety of the first island
        def dfs(r: int, c: int, island_id: int):
            grid[r][c] = island_id
            queue.append((r, c))  # Collect all island 1 cells as BFS sources

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                    dfs(nr, nc, island_id)

        # Find the first land cell and trigger DFS to isolate Island 1
        found = False
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    dfs(i, j, island_id)
                    found = True
                    break
            if found:
                break

        distance = 0

        # Step 2: Multi-Source BFS to expand Island 1 level-by-level until it hits Island 2
        while queue:
            for _ in range(len(queue)):
                r, c = queue.popleft()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        # Found the second island (unvisited land cell '1')
                        if grid[nr][nc] == 1:
                            return distance
                        # Expand across water cell '0' and mark visited as '2'
                        if grid[nr][nc] == 0:
                            grid[nr][nc] = 2
                            queue.append((nr, nc))

            # Increment distance after processing each full BFS level
            distance += 1

        return distance
```

## 4. Dry Run

Input (LC Example 2):

```text
r0:  0  1  0
r1:  0  0  0
r2:  0  0  1
```

**Step 1 (DFS):** the scan finds `grid[0][1] == 1`. `dfs(0,1)` paints it `2` and has no land neighbours, so `queue = [(0,1)]`.

**Step 2 (BFS):** neighbours are tried in the order **right, left, down, up**.

| `distance` during pass | Pops this pass | Water painted `2` and pushed (in order) | `queue` after the pass |
| --- | --- | --- | --- |
| 0 | `(0,1)` | `(0,2)` (right), `(0,0)` (left), `(1,1)` (down) | `(0,2) (0,0) (1,1)` |
| 1 | `(0,2)`, `(0,0)`, `(1,1)` | `(1,2)` (down from `(0,2)`), `(1,0)` (down from `(0,0)`), `(2,1)` (down from `(1,1)`) | `(1,2) (1,0) (2,1)` |
| 2 | `(1,2)` | its **down** neighbour `(2,2)` is `1`, so **return `2`** right away | — |

`distance` became 1 after pass 0 and 2 after pass 1. It returns **`2`** during the third pass, while popping the very first cell `(1,2)`.

## 5. Complexity

* **Time: O(n²)** (rows × columns, where the grid is n × n)
  Think of it as: every cell is handled at most once. The scan to find the first `1` looks at each cell at most once. The DFS paints each island-A cell once. The BFS pushes each water cell at most once (it becomes `2` when pushed), and each pop checks 4 neighbours. So the total work grows with the number of cells.
* **Space: O(n²)**
  Think of it as: two things can grow with the grid. The recursion stack during `dfs` can go one call deep per island-A cell (picture a long snake-shaped island). And `queue` starts with *all* of island A, then holds a whole layer of water. Either can be close to n² in the worst case. No separate visited array is needed, because painting cells `2` does that job.

## 6. Recall (30 seconds)

* **Two phases:** DFS paints island A as `2` and pushes every cell. Then multi-source BFS through the `0`s in layers.
* Use `for _ in range(len(queue))` per layer, and `distance += 1` after each layer. The first `1` you see → `return distance`, which is the number of water cells flipped.
* O(n²) time and space. Recursive `dfs` can hit Python's recursion limit on big islands, so use an iterative fill if that matters.
