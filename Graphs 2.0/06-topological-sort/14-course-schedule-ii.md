# 210. Course Schedule II

**LC 210** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Topological sort (Kahn's algorithm), returning the order itself

---

## 1. Intuition

This is Course Schedule (#13), but instead of answering "can I finish?" you hand back the actual timetable.
Kahn's algorithm already takes the courses in a valid order: a course is popped only after all its
prerequisites were popped. So just write down each course as you pop it.

* **Same graph as #13:** `[u, v]` becomes the edge `v → u` (`graph[v].append(u)`), and `indegree[u] += 1` counts `u`'s unfinished prerequisites.
* **The pop order is the answer:** `topo_order.append(node)` right after `queue.popleft()`. A course can only be in `queue` once its indegree is `0`, meaning every prerequisite is already in `topo_order`.
* **A cycle shows up as a short list:** courses on a cycle never reach indegree `0`, so `len(topo_order) < numCourses`, and the code returns `[]`.
* **Many orders can be correct:** any course with indegree `0` may go next. This code always returns the one that FIFO `deque` order produces, and LeetCode accepts any valid order.

**Recall:** Kahn's algorithm. Append each popped course to `topo_order`. Return it if it has all `numCourses` courses, otherwise `[]`.

## 2. Approach

* **Idea:** Run Kahn's algorithm (BFS on indegrees) and record the pop order. That order is a topological sort exactly when every course gets popped.
* **Graph representation:** **adjacency list** (`defaultdict(list)`) built from the edge list. **Directed** (`prerequisite → course`) and unweighted. Nodes are `0 … numCourses-1`.
* **Data structure / pointers:**
  * `graph[v]`: the courses that need `v` first.
  * `indegree[u]`: the number of `u`'s prerequisites not yet in `topo_order`.
  * `queue` (`deque`): ready courses (indegree `0`). Each course is pushed **once**, when its indegree hits `0`. That's the visited rule, so no visited set is needed.
  * `topo_order`: the courses in the order they're taken. It also replaces the `processed` counter from #13 (`len(topo_order)`).
* **Invariant:** for every course in `topo_order`, all its prerequisites appear **earlier** in `topo_order`.
* **Edge cases:**
  * No prerequisites: every course starts in the queue, so it returns `[0, 1, …, numCourses-1]`.
  * A cycle (for example `[[1,0],[0,1]]`) or a self-loop (`[[0,0]]`): the list comes up short, so it returns `[]`.
  * A course that depends on a cycle: never popped either, so it returns `[]`.
  * Separate components: every acyclic component has a starting course, and they get mixed together in queue order.
  * A single course: `[0]`.
  * Duplicate pairs (not allowed on LC, but handled): counted twice and decreased twice, so it still works.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import defaultdict, deque
from typing import List


class Solution:

    def findOrder(
        self, numCourses: int, prerequisites: List[List[int]]
    ) -> List[int]:
        graph = defaultdict(list)
        indegree = [0] * numCourses
        topo_order = []

        # Build directed graph (v -> u: course v is prerequisite for course u)
        for u, v in prerequisites:
            graph[v].append(u)
            indegree[u] += 1

        # Enqueue all courses with no prerequisites (indegree == 0)
        queue = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)

        # BFS Topological Traversal
        while queue:
            node = queue.popleft()
            topo_order.append(node)

            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        # Return full order if valid; empty array if a cycle prevented taking all courses
        return topo_order if len(topo_order) == numCourses else []
```

## 4. Dry Run

Input (LC Example 2): `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`

```text
graph:  0 → [1, 2]    1 → [3]    2 → [3]        indegree = [0, 1, 1, 2]
```

| Step | `node` | `topo_order` | Indegree changes | `queue` after |
| --- | --- | --- | --- | --- |
| Start | — | `[]` | — | `[0]` |
| Pop | `0` | `[0]` | `indegree[1]` → **0** (push), `indegree[2]` → **0** (push) | `[1, 2]` |
| Pop | `1` | `[0, 1]` | `indegree[3]` 2 → 1 | `[2]` |
| Pop | `2` | `[0, 1, 2]` | `indegree[3]` 1 → **0** (push) | `[3]` |
| Pop | `3` | `[0, 1, 2, 3]` | no outgoing edges | `[]` |

`len(topo_order) == 4 == numCourses`, so this code returns **`[0, 1, 2, 3]`**. (`[0, 2, 1, 3]` is also a valid answer that LeetCode would accept, but this code always produces `[0, 1, 2, 3]`, because `1` was pushed before `2`.)

## 5. Complexity

* **Time: O(V + E)**, where V = `numCourses` and E = `len(prerequisites)`
  Think of it as: each course is pushed, popped and appended once, and each prerequisite pair is touched twice. Building the graph walks the pairs once, and the BFS walks each popped course's outgoing edges once. Add the V-step scan for starting courses, and you get V + E.
* **Space: O(V + E)**
  Think of it as: `graph` stores every edge (E), and `indegree`, `queue` and `topo_order` each hold at most one entry per course (V).

## 6. Recall (30 seconds)

* Same setup as #13: edge `v → u`, `indegree[u] += 1`, and the queue starts with every course at indegree 0.
* **Append each popped course to `topo_order`.** The pop order is a valid schedule, because a course is only popped after all its prerequisites.
* Return `topo_order` if its length is `numCourses`, otherwise `[]` (there's a cycle). O(V + E) time and space.
