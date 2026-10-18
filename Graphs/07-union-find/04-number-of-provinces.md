# Number of Provinces  ·  LeetCode 547  ·  Medium

Group 07 — Union-Find  ·  Number of Connected Components, with the graph handed to
you as an **adjacency matrix** instead of an edge list.

Prereqs: `concepts/08-union-find.md`, `03-number-of-connected-components.md` (this
is that problem with a different input format).

---

## 1. Problem

There are `n` cities. `isConnected` is an `n x n` matrix where
`isConnected[i][j] == 1` means city `i` and city `j` are **directly** connected,
and `0` means they aren't. A **province** is a group of cities connected
directly or indirectly.

**Return the number of provinces.**

Constraints:
- `1 <= n <= 200`.
- `isConnected[i][i] == 1`; `isConnected[i][j] == isConnected[j][i]` (symmetric).

Example 1:

```
isConnected = [[1,1,0],
               [1,1,0],
               [0,0,1]]
answer = 2        # {0,1} and {2}
```

Example 2:

```
isConnected = [[1,0,0],
               [0,1,0],
               [0,0,1]]
answer = 3        # nobody connected -> 3 lone provinces
```

---

## 2. Explain Like I'm 5

Same as "count the piles of connected toys." The only difference: instead of
being handed a list of strings ("toy 0 is tied to toy 1"), you're handed a big
grid where the cell at row `i`, column `j` is `1` if there's a string between
toy `i` and toy `j`.

So you just read the grid to find the strings, then do the exact same thing:
start with `n` piles, and every string that joins **two different** piles drops
your count by one.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "How many provinces / friend circles / clusters?" | ✅ count components |
| Input is an **adjacency matrix** (`isConnected[i][j]`) | ✅ → read edges from `[i][j] == 1` |
| Undirected (symmetric matrix) | ✅ → only scan `j > i` |

**Reduce it to:** *"Number of Connected Components — `count = n`, `count -= 1`
per successful `union` — where the edges are the `1`s in the upper triangle of
the matrix."*

**Look-alikes:** Number of Connected Components (identical, edge-list input);
Number of Islands (components on a grid).

---

## 4. Intuition

Identical to Number of Connected Components. The one adaptation:

- The matrix is **symmetric** and its diagonal is all `1`s (every city is
  "connected to itself"). So you only need to look at `isConnected[i][j]` for
  `j > i` — the lower triangle is a mirror, and the diagonal is meaningless
  (a self-loop, no effect on components).
- Every `1` at `(i, j)` with `j > i` is an edge → `union(i, j)`.

---

## 5. Approach (primary): DSU over the matrix's upper triangle

1. `n = len(isConnected)`. `dsu = DSU(n)`. `count = n`.
2. For `i` in `0..n-1`, for `j` in `i+1..n-1`: if `isConnected[i][j] == 1` and
   `dsu.union(i, j)` returns `True`: `count -= 1`.
3. Return `count`.

Builds on: `03-number-of-connected-components.md` — same algorithm, edges read
from the matrix.

---

## 6. Pseudocode

```
function findCircleNum(isConnected):
    n = len(isConnected)
    dsu = DSU(n)
    count = n
    for i in 0 .. n-1:
        for j in i+1 .. n-1:              # upper triangle only (symmetric matrix)
            if isConnected[i][j] == 1 and union(i, j):
                count -= 1
    return count
```

---

## 7. Dry Run

```
isConnected = [[1,1,0],
               [1,1,0],
               [0,0,1]]
```

`n = 3`, `DSU(3)`, `count = 3`.

| (i, j) | isConnected[i][j] | union | count after |
|---|---|---|---|
| (0,1) | 1 | `True` | 2 |
| (0,2) | 0 | skip | 2 |
| (1,2) | 0 | skip | 2 |

Return `2` — `{0,1}` and `{2}`. ✅

---

## 8. Python Code (primary — DSU)

```python
from typing import List


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        dsu = DSU(n)
        count = n
        for i in range(n):
            for j in range(i + 1, n):            # upper triangle only
                if isConnected[i][j] == 1 and dsu.union(i, j):
                    count -= 1
        return count


if __name__ == "__main__":
    sol = Solution()

    assert sol.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert sol.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert sol.findCircleNum([[1]]) == 1
    assert sol.findCircleNum([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 1
    assert sol.findCircleNum(
        [[1, 0, 0, 1],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [1, 0, 0, 1]]) == 2                       # {0,3} and {1,2}

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. BFS/DFS flood-fill over the matrix

```python
from collections import deque
from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        seen = set()
        count = 0
        for start in range(n):
            if start in seen:
                continue
            count += 1
            q = deque([start])
            seen.add(start)
            while q:
                i = q.popleft()
                for j in range(n):
                    if isConnected[i][j] == 1 and j not in seen:
                        seen.add(j)
                        q.append(j)
        return count
```

`O(n²)` — you must scan every matrix cell either way, since that's how the edges
are given.

### The BFS↔DFS answer the interviewer wants

> "Same as Number of Connected Components — DSU or flood-fill, both dominated by
> the `O(n²)` matrix scan. DSU is a couple lines and the group's tool. The only
> matrix-specific detail is scanning just the upper triangle since the matrix is
> symmetric."

---

## 10. Complexity — derived step by step

**V and E:** `V = n` cities; `E` = number of `1`s in the upper triangle,
`E ≤ n(n-1)/2 = O(n²)`.

**Time:**
- The double loop scans `O(n²)` matrix cells (unavoidable — that's the input).
- Each `1` triggers a `union`, amortized `O(α(n))`.
- **Total: `O(n² · α(n))` ≈ `O(n²)`** — dominated by reading the matrix.

**Space:**
- DSU `parent` + `rank`: `O(n)`.
- **Total: `O(n)`** (the matrix itself is the input, not counted as extra).

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `n = 1` (`[[1]]`) | `count` starts and stays at `1`; inner loop `range(1, 1)` is empty |
| Fully connected matrix (all `1`s) | every `union` in the upper triangle merges → `count` → `1` |
| Identity matrix (only the diagonal is `1`) | no off-diagonal `1`s → `count` stays `n` |
| Diagonal `1`s | never examined (`j > i` skips `j == i`) — a self-loop has no effect anyway |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Scanning the full matrix (`j in range(n)`) instead of `range(i+1, n)`.**
      Not *wrong* (a symmetric edge just gets unioned twice, second is a no-op),
      but doubles the work and looks careless.
- [ ] **Including `j == i`** — a self-loop; harmless (`union(i, i)` returns
      `False`), but scan `j > i` to skip it cleanly.
- [ ] **Decrementing `count` on every `union` call** instead of only successful
      ones — same bug as Number of Connected Components.
- [ ] **`count` initialized to `0`** instead of `n`.
- [ ] **Confusing "province" with a grid island** — here the connections are
      given explicitly in a matrix, not implied by grid adjacency.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Adjacency matrix → edges = the `1`s in the upper triangle.** For a symmetric
   matrix, scan `j > i` only.
2. Everything else is Number of Connected Components — `count = n`, `count -= 1`
   per successful `union`.
3. **Input format doesn't change the algorithm** — edge list, adjacency matrix,
   or grid, "count components" is the same DSU (or flood-fill) loop with a
   different way of enumerating the edges.

| Problem | How this transfers |
|---|---|
| Number of Connected Components | identical, edge-list input |
| Number of Islands | components on a grid (edges = grid adjacency) |
| Accounts Merge | components of a "shares an email" graph |
| Any "how many clusters" question | enumerate edges however the input gives them, then DSU |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The matrix is `50,000 x 50,000` but very **sparse** (each city connects to only a handful). It's given as a sparse format (list of `(i, j)` pairs), not a dense matrix."

- **(b) Pattern:** now it's literally Number of Connected Components (edge-list
  input) — don't allocate the dense matrix.
- **(c) Adapt:** iterate the sparse pair list directly, `union` each. `O(E α(n))`
  time, `O(n)` space — instead of `O(n²)` to even read a dense matrix.
- **(d) Say:** "A sparse graph should never be materialized as a dense matrix —
  the pair list *is* the edge list, and DSU processes it in `O(E)`."

### Scenario 2 — "Return the **size of the largest** province."

- **(b) Pattern:** DSU with a `size` array.
- **(c) Adapt:** maintain `size[root]` in `union`; after the scan,
  `max(size[dsu.find(i)] for i in range(n))`. `O(n² + n)`.
- **(d) Say:** "Track group sizes in `union`; the largest province is a one-line
  `max` over the roots afterward."

### Scenario 3 — "Friendships form and dissolve over time. After each change, report the province count."

- **(b) Pattern:** additions are DSU's job; **dissolving** a friendship
  (edge removal) is not.
- **(c) Adapt:** additions → `union`, `count -= 1` on success. For removals: DSU
  can't un-merge. If the whole timeline is known, process offline in reverse
  (removals become additions). Online with arbitrary removals → dynamic
  connectivity structure (link-cut / Euler-tour trees).
- **(d) Say:** "Same DSU limitation as always — deletions need offline-reverse or
  a dynamic-connectivity structure, not plain Union-Find."

### Scenario 4 — "Given two cities `a` and `b` not currently in the same province, and you may add **one** friendship edge to connect their provinces plus possibly others — which single edge merges the **most** cities into one province?"

- **(b) Pattern:** DSU + `size`, then evaluate candidate merges.
- **(c) Adapt:** build the DSU. For a candidate edge `(a, b)` between two
  provinces, the merged size is `size[find(a)] + size[find(b)]`. To find the
  single best merge overall, check every pair of distinct roots and take the max
  combined size (`O(#provinces²)`), or just the largest two provinces if any edge
  between them is allowed.
- **(d) Say:** "Precompute component sizes once, then each candidate merge is an
  `O(1)` sum of two root sizes — the same 'label + probe' idea as Making a Large
  Island."

### Scenario 5 — "The relation isn't symmetric — `isConnected[i][j] == 1` means 'i follows j' (directed). Count **strongly connected** components."

- **(b) Pattern:** DSU **can't** do this — it's undirected-only. Strongly
  connected components need Tarjan's SCC or Kosaraju's algorithm.
- **(c) Adapt:** run Kosaraju's — DFS the graph pushing nodes onto a stack by
  finish time; then DFS the **transpose** graph in reverse-finish order; each
  DFS tree in the second pass is one SCC. `O(V + E) = O(n²)` here.
- **(d) Say:** "'Strongly connected' + directed rules out Union-Find entirely —
  that's Kosaraju's or Tarjan's SCC."

### Scenario 6 — "Report, for every city, which province id it belongs to (a canonical label per province)."

- **(b) Pattern:** the DSU root already *is* a canonical per-province label.
- **(c) Adapt:** after the scan, `province_of[i] = dsu.find(i)` for every `i`.
  If you want ids `0..k-1` instead of arbitrary roots, remap the distinct roots
  to a dense range with a dict. `O(n)`.
- **(d) Say:** "`find(i)` already returns a stable id per component — one pass to
  label everyone, plus an optional remap to compact ids."

---

## 15. Flashcards

**Q:** How does Number of Provinces differ from Number of Connected Components?
**A:** Only the input format — an adjacency matrix instead of an edge list. Edges
are the `1`s in `isConnected`; scan the upper triangle (`j > i`) since it's
symmetric.

**Q:** The algorithm?
**A:** `count = n`; for each `1` at `(i, j)` with `j > i`, if `union(i, j)`
returns `True`, `count -= 1`.

**Q:** Why only scan `j > i`?
**A:** The matrix is symmetric (`[i][j] == [j][i]`) and the diagonal is
meaningless self-loops — the upper triangle has every distinct edge exactly once.

**Q:** Time and space?
**A:** `O(n² · α(n)) ≈ O(n²)` time (dominated by scanning the matrix), `O(n)`
space.

**Q:** Sparse `50k x 50k` matrix given as `(i, j)` pairs — what changes?
**A:** Don't build a dense matrix; treat the pair list as an edge list, `union`
each — `O(E)` instead of `O(n²)`.

**Q:** Directed version, "strongly connected components"?
**A:** DSU can't — use Kosaraju's or Tarjan's SCC.

**Q:** Per-city province label?
**A:** `dsu.find(i)` is already a canonical id per province; optionally remap
roots to `0..k-1`.
