# 886. Possible Bipartition

**LC 886** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** BFS 2-colouring on a graph you build from an edge list

---

## 1. Intuition

Split `n` people into two groups so that no two people who dislike each other end up together. Draw an
edge between every pair that dislikes each other. Then it's exactly Is Graph Bipartite? (#23): colour one
person, give everyone they dislike the opposite colour, and keep going. If two people who dislike each
other end up with the **same** colour, no split works.

* **Build the graph first:** each `[u, v]` in `dislikes` becomes `graph[u].append(v)` and `graph[v].append(u)`. "Dislike" goes both ways for grouping, so the graph is undirected.
* **Colours `0 / 1 / -1`:** `color = [0] * (n + 1)` has room for people numbered `1 … n`. `0` means not placed yet.
* **The opposite group = negate:** `color[neighbor] = -color[node]`, and `color[neighbor] == color[node]` is a clash, so `return False`.
* **Cover every group of people:** the outer loop starts a BFS from every uncoloured person, so people who are split into separate dislike-groups are all checked.

**Recall:** Build an undirected graph from `dislikes`. 2-colour it with BFS (`1` / `-1`, and `0` = unplaced). A neighbour with the same colour means `False`. Otherwise `True`.

## 2. Approach

* **Idea:** "Two groups with no dislike inside a group" means the dislike graph is **bipartite**. Check it by BFS 2-colouring each connected part.
* **Graph representation:** **adjacency list** (`defaultdict(list)`) built from the **edge list** `dislikes`. **Undirected**, unweighted. People are nodes `1 … n`.
* **Data structure / pointers:**
  * `graph[p]`: the people `p` dislikes or who dislike `p`.
  * `color[p]`: `0` means not placed, and `1` / `-1` is the group. It doubles as the visited set. A person is coloured **when pushed**.
  * `queue` (`deque`): the BFS frontier, shared across starts. The `while queue` loop sits outside the `if`, but `queue` is only non-empty right after a new start, so the behaviour is the same.
* **Invariant:** every coloured person has the opposite colour to the person who discovered them, so along any BFS path the groups alternate.
* **Edge cases:**
  * No dislikes: no edges, so it returns `True`.
  * `n = 1`: returns `True`.
  * A dislike triangle (an odd cycle, LC Example 2): clash, so it returns `False`.
  * Separate groups of people: each one is coloured from its own start, and a clash in any group returns `False`.
  * **The `range(n)` detail:** people are `1 … n`, but the loop runs `i = 0 … n-1`. So index `0` (nobody) gets coloured `1` harmlessly, and person `n` is never a *starting* point. That's still correct. If `n` dislikes anyone, it gets coloured when BFS starts from that person (who has a number below `n`). If `n` dislikes nobody, there's nothing to check. `range(1, n + 1)` would read more naturally, with the same result.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        graph = defaultdict(list)

        queue = deque()

        for u,v in dislikes:
            graph[u].append(v)
            graph[v].append(u)

        color = [0] * (n + 1)

        for i in range(n):
            if color[i] == 0:
                color[i] = 1
                queue.append(i)

            while queue:
                node = queue.popleft()

                for neighbor in graph[node]:
                    if color[neighbor] == 0:
                        color[neighbor] = -color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
        return True
```

## 4. Dry Run

Input (LC Example 1): `n = 4`, `dislikes = [[1,2],[1,3],[2,4]]`

```text
graph:  1 → [2, 3]    2 → [1, 4]    3 → [1]    4 → [2]

3 ── 1 ── 2 ── 4
```

`color` (indices 0…4) starts as `[0, 0, 0, 0, 0]`.

| Step | What happens | `color[0..4]` after |
| --- | --- | --- |
| `i = 0` | uncoloured, so colour it `1`, push 0. Pop 0: no neighbours (nobody is person 0) | `[1, 0, 0, 0, 0]` |
| `i = 1` | uncoloured, so colour it `1`, push 1 | `[1, 1, 0, 0, 0]` |
| pop `1` | `2` → `-1` (push), `3` → `-1` (push) | `[1, 1, -1, -1, 0]` |
| pop `2` | `1` is `1`, fine. `4` → `1` (push) | `[1, 1, -1, -1, 1]` |
| pop `3` | `1` is `1`, fine | same |
| pop `4` | `2` is `-1`, fine | same |
| `i = 2, 3` | already coloured, so skip | same |

No clash, so it returns **`True`**. The groups are `{1, 4}` and `{2, 3}`.

## 5. Complexity

Let **E** = `len(dislikes)`.

* **Time: O(n + E)**
  Think of it as: building `graph` reads each dislike once (E). The outer loop checks each person once (n). In the BFS, each person is coloured and pushed once, and when they're popped their list is walked once. Every dislike is in two lists, so that's 2E checks. Total: n + E.
* **Space: O(n + E)**
  Think of it as: `graph` stores each dislike twice (2E), and `color` and `queue` hold at most one entry per person (n).

## 6. Recall (30 seconds)

* Two groups with no dislike inside a group ⇔ the dislike graph is **bipartite**. Build an undirected adjacency list from `dislikes`.
* BFS 2-colouring with `1` / `-1` (`0` = unplaced), starting from every uncoloured person. A same-colour neighbour means `False`.
* O(n + E) time and space. People are numbered from 1, so size `color` as `n + 1`.
