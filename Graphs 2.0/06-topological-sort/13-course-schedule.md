# 207. Course Schedule

**LC 207** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Topological sort (Kahn's algorithm, BFS on indegrees), used here for cycle detection

---

## 1. Intuition

Picture a course catalogue where each course lists the courses you must take first. Start with every course
that needs nothing. Each time you finish a course, cross it off as a requirement for the courses that need it.
Any course whose list becomes empty is now ready. If you can finish every course this way, there's no cycle.
If some courses stay blocked forever, they're waiting on each other in a loop.

* **Edge direction:** a pair `[u, v]` means "take `v` before `u`", so the code adds the edge `v → u` (`graph[v].append(u)`) and counts `indegree[u] += 1`.
* **`indegree[x]` = prerequisites of `x` not finished yet.** A course is ready exactly when this is `0`, so the queue starts with every `i` where `indegree[i] == 0`.
* **Finishing a course unlocks others:** after popping `node`, each `neighbor` gets `indegree[neighbor] -= 1`. When it hits `0`, that course is pushed.
* **The cycle test is just a count:** a course on a cycle (and anything that depends on it) never reaches indegree `0`, so it's never popped. `processed == numCourses` is true exactly when there's no cycle.

**Recall:** Build `v → u` edges and `indegree`. Queue every course with indegree 0, pop, count, and decrease the neighbours' indegrees. Return `processed == numCourses`.

## 2. Approach

* **Idea:** Kahn's algorithm. Keep taking a course with no remaining prerequisites. A graph can be fully "peeled" like this **if and only if** it has no directed cycle.
* **Graph representation:** **adjacency list** (`defaultdict(list)`) built from the edge list `prerequisites`. **Directed** (`prerequisite → course`) and unweighted. Nodes are `0 … numCourses-1`.
* **Data structure / pointers:**
  * `graph[v]`: the courses that list `v` as a prerequisite (`v`'s outgoing edges).
  * `indegree[u]`: how many of `u`'s prerequisites haven't been taken yet.
  * `queue` (`deque`): courses that are ready to take (indegree `0`) but not processed yet. A course is pushed **once**, at the moment its indegree reaches `0`. That's the "visited" rule, and no separate visited set is needed.
  * `processed`: the number of courses popped (taken) so far.
* **Invariant:** every course in `queue` or already processed has all its prerequisites processed (or queued before it). `indegree[x]` always equals the number of `x`'s prerequisites not yet popped.
* **Edge cases:**
  * No prerequisites: every course has indegree `0`, so all are processed and it returns `True`.
  * A 2-cycle `[[1,0],[0,1]]`: neither course ever reaches `0`, so `processed = 0` and it returns `False`.
  * A self-loop `[[0,0]]` (course needs itself): `indegree[0] = 1` and it's never reduced, so it returns `False`.
  * Separate components: fine, because every component without a cycle has at least one indegree-0 course in the starting queue. A cycle in *any* component makes it return `False`.
  * A course that depends on a cycle (for example `2` needs `1`, and `0 ↔ 1`) is also never processed. That's correct, because you couldn't take it either.
  * Duplicate pairs (not allowed on LC, but handled): `indegree` counts each copy, and each copy is decreased once, so it still works.
  * `numCourses = 1`: returns `True` (unless it has a self-loop).
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import defaultdict, deque


class Solution:

    def canFinish(
        self, numCourses: int, prerequisites: list[list[int]]
    ) -> bool:
        # Build adjacency list representation and indegree tracker
        graph = defaultdict(list)
        indegree = [0] * numCourses

        # Populate directed edges b -> a (must take b before a)
        for u, v in prerequisites:
            graph[v].append(u)
            indegree[u] += 1

        # Enqueue all courses with 0 prerequisites
        queue = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)

        processed = 0

        # Process courses level-by-level
        while queue:
            node = queue.popleft()
            processed += 1

            # Decrement indegree for all courses dependent on 'node'
            for neighbor in graph[node]:
                indegree[neighbor] -= 1

                # If all prerequisites for neighbor are satisfied, enqueue it
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        # If processed count equals numCourses, a valid ordering exists (no cycle)
        return processed == numCourses
```

## 4. Dry Run

Input: `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`

```text
graph:  0 → [1, 2]    1 → [3]    2 → [3]        indegree = [0, 1, 1, 2]

    0
   / \
  1   2
   \ /
    3
```

| Step | `node` | `processed` | Indegree changes | `queue` after |
| --- | --- | --- | --- | --- |
| Start | — | 0 | — | `[0]` (only course 0 has indegree 0) |
| Pop | `0` | 1 | `indegree[1]` 1→**0** (push), `indegree[2]` 1→**0** (push) | `[1, 2]` |
| Pop | `1` | 2 | `indegree[3]` 2→1 (still waiting on course 2) | `[2]` |
| Pop | `2` | 3 | `indegree[3]` 1→**0** (push) | `[3]` |
| Pop | `3` | 4 | no outgoing edges | `[]` |

The loop ends, and `processed (4) == numCourses (4)`, so it returns **`True`**.

## 5. Complexity

* **Time: O(V + E)**, where V = `numCourses` and E = `len(prerequisites)`
  Think of it as: every course is touched a fixed number of times, and every prerequisite pair is touched twice. Building the graph walks the pairs once, which is E steps. Setting up the queue checks every course once, which is V steps. In the BFS, each course is popped at most once, and when it's popped its outgoing edges are walked once, so the edges add up to E steps. Total: V + E.
* **Space: O(V + E)**
  Think of it as: `graph` stores every edge once, which is E, and `indegree` and `queue` each hold at most one entry per course, which is V.

## 6. Recall (30 seconds)

* `[u, v]` means **edge `v → u`** and `indegree[u] += 1`. Start the queue with every course that has indegree 0.
* Pop, `processed += 1`, then decrease each neighbour's indegree, and push it when it reaches 0. A course is pushed exactly once, so there's no visited set.
* `return processed == numCourses`. Anything stuck is on a cycle or depends on one. O(V + E) time and space.
