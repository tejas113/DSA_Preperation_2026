# 399. Evaluate Division

**LC 399** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Weighted graph traversal, multiplying edge weights along a path (BFS here; DFS works the same way)

---

## 1. Intuition

Each equation `a / b = 2` is a road between `a` and `b` with an exchange rate, like currencies: going
`a → b` multiplies by 2, and coming back `b → a` multiplies by 1/2. To answer `a / c`, find **any** route
from `a` to `c` and multiply the rates along the way. If `a` and `b` are both known, any route gives the
same answer, so the first route BFS finds is good enough.

* **Two edges per equation:** `adj[a].append([b, values[i]])` and `adj[b].append([a, 1/values[i]])`. Division can go both ways, so the graph is undirected, but each direction has its own weight.
* **Carry the running product:** each queue item is `[node, w]`, where `w` = `start / node` so far. A step to `nei` pushes `w * weight`.
* **Unknown variables mean -1:** `if start not in adj or target not in adj: return -1.0`. This also makes `x / x` return `-1.0` when `x` never appeared in any equation.
* **Found it, or ran out of routes:** `if n == target: return w`. If the queue empties without reaching `target`, the two variables are in different groups, so it returns `-1`.

**Recall:** Add the edge `a → b` with weight `v` and `b → a` with `1/v`. For each query, BFS from `start` carrying the product, and return it when you reach `target`, otherwise `-1`.

## 2. Approach

* **Idea:** `start / target` = the product of the edge ratios along any path from `start` to `target`. One BFS per query either finds a path (the product is the answer) or proves there isn't one (`-1`).
* **Graph representation:** **adjacency list** (`defaultdict(list)`) built from the edge list `equations`. **Weighted**, and each pair has an edge in both directions with weights `v` and `1/v`. The nodes are variable names (strings).
* **Data structure / pointers:**
  * `adj[x]`: a list of `[neighbour, ratio]`, where `ratio = x / neighbour`.
  * `q` (`deque`): items `[n, w]`, where `w = start / n` along the path that BFS took to reach `n`.
  * `visited`: the variables already queued in this query. A node is marked **when pushed**, so each variable is queued at most once per query. A **new** `visited` is made for each query.
  * There's no `dist` table. BFS order doesn't matter here (we want *a* path, not the shortest one). `visited` just stops loops.
* **Invariant:** for every `[n, w]` in the queue, `w == start / n` (multiplying the ratios along the path to `n` gives exactly that).
* **Edge cases:**
  * A variable not in any equation (for example `["a", "e"]`): returns `-1.0`.
  * `x / x` where `x` is known: `start == target`, so the first pop returns `w = 1`. Where `x` is unknown: returns `-1.0`.
  * Both variables known but in **different groups** (no path): BFS runs out, so it returns `-1`.
  * The reverse query (`b / a` when only `a / b` was given): the `1/values[i]` edge handles it.
  * Cycles (for example `a/b`, `b/c`, `c/a`): `visited` prevents infinite loops. The input is guaranteed to be consistent, so any path gives the same product.
  * The same pair given twice: two parallel edges, which is harmless.
  * Returns: the found value is a number, and "not found" returns `-1.0` or `-1`. Both equal `-1.0`, so LeetCode accepts them.
  * Floating point: products of ratios can be off in the last digits (for example `0.5 * 3.0 * ...`). Compare results with a tolerance, not `==`.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:

        adj = defaultdict(list)

        for i,eq in enumerate(equations):
            a,b = eq
            adj[a].append([b,values[i]])
            adj[b].append([a,1/values[i]])

        def bfs(start,target):
            if start not in adj or target not in adj:
                return -1.0

            q = deque([[start,1]])
            visited = {start}

            while q:
                n,w = q.popleft()

                if n == target:
                    return w

                for nei,weight in adj[n]:
                    if nei not in visited:
                        q.append([nei,w*weight])
                        visited.add(nei)
            return -1
            

        return [bfs(q[0],q[1]) for q in queries]
```

## 4. Dry Run

Input (LC Example 1): `equations = [["a","b"],["b","c"]]`, `values = [2.0, 3.0]`

```text
adj:  a → [b, 2.0]
      b → [a, 0.5], [c, 3.0]
      c → [b, 0.333…]

   a ──2.0──▶ b ──3.0──▶ c        (reverse edges: ×0.5, ×1/3)
```

**Query `["a", "c"]`:**

| Pop `[n, w]` | `n == target`? | Neighbours pushed (`w × weight`) | `queue` after | `visited` |
| --- | --- | --- | --- | --- |
| (start) | — | — | `[[a, 1]]` | `{a}` |
| `[a, 1]` | no | `b`: 1 × 2.0 = 2.0 | `[[b, 2.0]]` | `{a, b}` |
| `[b, 2.0]` | no | `a` already visited, so skip. `c`: 2.0 × 3.0 = 6.0 | `[[c, 6.0]]` | `{a, b, c}` |
| `[c, 6.0]` | **yes** | — | — | return **6.0** |

**The other queries:**

| Query | What happens | Result |
| --- | --- | --- |
| `["b", "a"]` | `[b, 1]` → push `a` with 1 × 0.5. Pop `[a, 0.5]`, which is the target | `0.5` |
| `["a", "e"]` | `"e"` is not in `adj`, so the early return fires | `-1.0` |
| `["a", "a"]` | the first pop `[a, 1]` is already the target | `1` |
| `["x", "x"]` | `"x"` is not in `adj` | `-1.0` |

It returns **`[6.0, 0.5, -1.0, 1, -1.0]`**, which LeetCode treats as `[6.0, 0.5, -1.0, 1.0, -1.0]`.

## 5. Complexity

Let **E** = `len(equations)`, **V** = the number of distinct variables (at most 2E), and **Q** = `len(queries)`.

* **Time: O(E + Q × (V + E))**
  Think of it as: you build the graph once, then run a fresh BFS for every query. Building `adj` reads each equation once, which is E. Each BFS can, in the worst case, visit every variable once and look at every edge once, which is V + E. There are Q queries, and nothing is shared between them, so it's Q × (V + E). (A weighted union-find could answer each query in close to O(1), but with LC's limits of at most 20 equations and 20 queries, per-query BFS is plenty.)
* **Space: O(V + E)**
  Think of it as: `adj` stores two entries per equation (2E), and during one query `q` and `visited` hold at most V variables each. They're thrown away after each query, so they don't add up. The output list is Q numbers.

## 6. Recall (30 seconds)

* Each equation `a / b = v` gives **two edges**, `a → b` with weight `v` and `b → a` with `1/v`. Then the answer to `x / y` is the **product of weights along any path**.
* BFS per query with `[node, product]` and a fresh `visited` (marked when pushed). Return the product at `target`, and return `-1` if a variable is unknown or there's no path.
* O(E + Q·(V + E)) time and O(V + E) space. Compare floats with a tolerance. Weighted union-find is the faster follow-up when there are many queries.
