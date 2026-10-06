# 547. Number of Provinces

**LC 547** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Count connected components on an adjacency matrix (DFS here; union-find works the same way)

---

## 1. Intuition

Cities that are linked, directly or through other cities, form one province. That's a connected component.
Go through the cities in order. When you reach one you haven't seen, it starts a **new province**, and a DFS
from it marks every city in that province, so none of them is counted again.

* **The graph comes as a matrix:** `isConnected[city][neighbor] == 1` means there's a direct road. So `dfs` checks **every** possible `neighbor in range(n)`, not a neighbour list.
* **`visited` stops double counting:** `visited.add(city)` happens as soon as `dfs` enters a city, and `neighbor not in visited` stops it re-entering.
* **One count per DFS start:** in the outer loop, `if i not in visited: provinces += 1; dfs(i)`. Every city reached during that `dfs` belongs to the same province.
* **Diagonal 1s are harmless:** `isConnected[i][i] == 1`, but `i` is already in `visited` by then, so it's skipped.

**Recall:** For each city not yet visited, `provinces += 1` and DFS through the matrix row, marking cities visited. Return `provinces`.

## 2. Approach

* **Idea:** The number of provinces is the number of connected components, which is the number of times the outer loop has to start a new DFS.
* **Graph representation:** **adjacency matrix** (`n × n`, symmetric), **undirected**, unweighted. Nodes are cities `0 … n-1`.
* **Data structure / pointers:**
  * `visited` (set): the cities already assigned to a province. A city is marked **when `dfs` enters it**.
  * `provinces`: the number of components found so far.
  * `dfs(city)`: a **recursive** DFS that scans row `city` of the matrix for unvisited direct neighbours.
* **Invariant:** when `dfs(i)` returns, every city connected to `i` is in `visited`. So any city still unvisited belongs to a province that hasn't been counted yet.
* **Edge cases:**
  * `n = 1`: `[[1]]` gives `1`.
  * No roads (the identity matrix): every city is its own province, so it returns `n`.
  * All cities linked: returns `1`.
  * Diagonal entries are `1` by definition, and the visited check skips them.
  * **Recursion depth:** `dfs` can go as deep as the number of cities in one province, and LC allows up to 200. That's under Python's default limit of 1,000, so it's safe here (a 200-city chain was tested).
  * **Union-find alternative:** start `count = n`, union `i` and `j` for every `isConnected[i][j] == 1`, and decrease `count` on each successful merge, exactly like #20. It's the same O(n²) cost because the whole matrix still has to be read.

## 3. Code

```python
from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        visited = set()
        provinces = 0

        def dfs(city):
            visited.add(city)
            for neighbor in range(n):
                if isConnected[city][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor)

        for i in range(n):
            if i not in visited:
                provinces += 1
                dfs(i)

        return provinces
```

### Alternative: Union-Find (start with `n` provinces, merge on every road)

Every city starts as its own province (`provinces = n`). For each road `isConnected[i][j] == 1`, union the two cities. If they had different roots, two provinces just became one, so `provinces -= 1`. The matrix is symmetric, so only the pairs `j > i` are checked. `find` uses **path compression**, and there's **no union by rank**. That's safe here, because n ≤ 200 keeps the recursion shallow.

```python
from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # path compression
            return parent[x]

        provinces = n  # every city starts as its own province
        for i in range(n):
            for j in range(i + 1, n):  # matrix is symmetric: check each pair once
                if isConnected[i][j] == 1:
                    root_i, root_j = find(i), find(j)
                    if root_i != root_j:
                        parent[root_j] = root_i
                        provinces -= 1  # two provinces merged into one

        return provinces
```

| | Main (DFS) | Alternative (union-find) |
| --- | --- | --- |
| Counting rule | add 1 per DFS start | start at `n`, subtract 1 per successful merge |
| Time | O(n²) (scan each row once) | O(n² · α(n)), effectively O(n²): every matrix cell is still read once |
| Extra space | `visited` + the recursion stack (n) | `parent` (n) + the recursion stack of `find` |

## 4. Dry Run

Input (LC Example 1):

```text
        c0  c1  c2
c0:      1   1   0        cities 0 and 1 are linked
c1:      1   1   0
c2:      0   0   1        city 2 is alone
```

| Outer `i` | In `visited`? | Action | Cities visited by this DFS | `provinces` |
| --- | --- | --- | --- | --- |
| 0 | no | new province, `dfs(0)` | `dfs(0)`: row 0 has a 1 at col 1, so `dfs(1)`. Row 1's only 1s are at 0 and 1, both visited | 1 |
| 1 | yes | skip | — | 1 |
| 2 | no | new province, `dfs(2)` | `dfs(2)`: row 2 only has itself | **2** |

It returns **2**: `{0, 1}` and `{2}`.

## 5. Complexity

* **Time: O(n²)**
  Think of it as: every city is entered by `dfs` exactly once, and each time it scans its **entire row** of `n` entries looking for roads. n cities × n entries per row = n². With an adjacency matrix you can't skip this, because you have to look at each cell to know whether it's a road.
* **Space: O(n)**
  Think of it as: `visited` holds at most n cities, and the recursion stack is at most n calls deep (one long chain of linked cities). The matrix is the input, so it isn't counted.
* **Union-find alternative: O(n²) time, O(n) space.** It still reads every matrix cell above the diagonal once (about n²/2), and each `find` is close to O(1) thanks to path compression. `parent` holds n entries.

## 6. Recall (30 seconds)

* Provinces = **connected components**. Each time the outer loop finds an unvisited city, `provinces += 1` and DFS marks its whole province.
* It's an **adjacency matrix**, so the DFS scans the whole row (`for neighbor in range(n)`). That's why it's O(n²).
* O(n²) time and O(n) space. Union-find (`count = n`, minus 1 per merge) is the equally good alternative.
