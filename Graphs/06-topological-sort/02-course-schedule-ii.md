# Course Schedule II  ·  LeetCode 210  ·  Medium

Group 06 — Topological Sort / Cycle Detection  ·  Course Schedule, but **return
the actual order** instead of a yes/no.

Prereqs: `01-course-schedule.md` (read that first — this is the same algorithm
with the output list kept), `concepts/07` (topological sort).

---

## 1. Problem

Same setup as Course Schedule: `numCourses` courses `0..numCourses-1`, and
`prerequisites[i] = [a, b]` meaning "take `b` before `a`."

**Return an ordering of courses you can take to finish all of them.** If there
are many valid orderings, return **any** of them. If it's impossible (a cycle),
return an **empty array**.

Constraints:
- `1 <= numCourses <= 2000`.
- `0 <= prerequisites.length <= numCourses * (numCourses - 1)`.
- No duplicate pairs.

Example 1:

```
numCourses = 2, prerequisites = [[1,0]]
answer = [0, 1]
```

Example 2:

```
numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
answer = [0,1,2,3]     (also valid: [0,2,1,3])
```

Example 3 (impossible):

```
numCourses = 1, prerequisites = [[0,0]]   # hypothetical self-dependency
answer = []
```

---

## 2. Explain Like I'm 5

Same dominoes as Course Schedule — some can only fall after specific others.
Last time you just wanted to know *"can they all fall?"* This time, **write down
the order in which they fall.**

Knock over every domino that has no prerequisite first, writing each one's name
on your list as it falls. Each fall might free up another domino — when a domino
has all its prerequisites satisfied, knock it over and add it to the list.

If your list ends up with every domino's name on it, that's a valid order. If
you get stuck (some dominoes stuck in a circle waiting on each other), throw the
list away and return nothing.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Prerequisite / before / build order" | ✅ |
| Asks for **the sequence**, not just feasibility | ✅ → keep the order Kahn's builds |
| "Return any valid one" | ✅ → topological order isn't unique; any works |

**Reduce it to:** *"Kahn's algorithm — the sequence in which nodes are dequeued
IS a valid topological order. Return it if all nodes were processed, else `[]`."*

**Look-alike:** Course Schedule (previous) — literally this algorithm with the
output list replaced by a counter.

---

## 4. Intuition

The order in which Kahn's algorithm pops nodes off the queue **is** a valid
topological order, for free:

1. A node is only ever added to the queue once its indegree hits `0` — meaning
   every prerequisite of it has **already been popped** (and thus already
   appended to the order).
2. So whenever you append a node to `order`, everything it depends on is
   guaranteed to be earlier in `order`. That's exactly the definition of a
   topological order.
3. If a cycle exists, some nodes never reach indegree `0`, the queue empties
   early, and `len(order) < numCourses` — return `[]`.

Nothing new versus Course Schedule — just **don't throw away the list**.

---

## 5. Approach (primary): Kahn's algorithm, keep the order

1. Build `graph` and `indegree` exactly as in Course Schedule (`graph[b].append(a)`,
   `indegree[a] += 1` for each `[a, b]`).
2. `q = deque(c for c in range(numCourses) if indegree[c] == 0)`. `order = []`.
3. While `q`: pop `c`, `order.append(c)`; for each `nei` in `graph[c]`:
   `indegree[nei] -= 1`; if `0`, push `nei`.
4. Return `order` if `len(order) == numCourses`, else `[]`.

Builds on: `01-course-schedule.md` — identical up to step 4.

---

## 6. Pseudocode

```
function findOrder(numCourses, prerequisites):
    graph, indegree = build as in Course Schedule
    q = queue of all courses with indegree 0
    order = []
    while q not empty:
        c = dequeue
        order.append(c)
        for nei in graph[c]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                enqueue nei
    return order if len(order) == numCourses else []
```

---

## 7. Dry Run

```
numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
```

Edges: `0->1, 0->2, 1->3, 2->3`. `indegree = [0,1,1,2]`. `q = [0]`.

| pop | order | neighbor updates | queue after |
|---|---|---|---|
| 0 | [0] | indeg[1]:1→0 → enqueue 1; indeg[2]:1→0 → enqueue 2 | [1, 2] |
| 1 | [0,1] | indeg[3]:2→1 | [2] |
| 2 | [0,1,2] | indeg[3]:1→0 → enqueue 3 | [3] |
| 3 | [0,1,2,3] | — | [] |

`len(order) == 4 == numCourses` → return `[0, 1, 2, 3]`.

(If `1` and `2` had been enqueued in the other order — which depends only on
which edge from `0` was processed first — you'd get `[0, 2, 1, 3]`, equally
valid.)

---

## 8. Python Code (primary — Kahn's algorithm)

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        indegree = [0] * numCourses

        for a, b in prerequisites:            # "a requires b" -> edge b -> a
            graph[b].append(a)
            indegree[a] += 1

        q = deque(course for course in range(numCourses) if indegree[course] == 0)
        order = []

        while q:
            course = q.popleft()
            order.append(course)
            for nei in graph[course]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        return order if len(order) == numCourses else []


def _is_valid_order(order, numCourses, prerequisites) -> bool:
    if sorted(order) != list(range(numCourses)):
        return False
    position = {course: i for i, course in enumerate(order)}
    return all(position[b] < position[a] for a, b in prerequisites)


if __name__ == "__main__":
    sol = Solution()

    assert sol.findOrder(2, [[1, 0]]) == [0, 1]
    assert _is_valid_order(sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
                           4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert sol.findOrder(1, []) == [0]
    assert sol.findOrder(2, [[0, 1], [1, 0]]) == []        # cycle -> empty
    assert sorted(sol.findOrder(3, [])) == [0, 1, 2]        # no prereqs -> any order of all
    assert sol.findOrder(3, [[1, 0], [2, 1], [0, 2]]) == []  # 3-cycle

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS post-order

```python
def findOrder(self, numCourses, prerequisites):
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * numCourses
    order = []

    def dfs(node):
        color[node] = GRAY
        for nei in graph[node]:
            if color[nei] == GRAY:
                return False
            if color[nei] == WHITE and not dfs(nei):
                return False
        color[node] = BLACK
        order.append(node)          # post-order
        return True

    for c in range(numCourses):
        if color[c] == WHITE and not dfs(c):
            return []
    return order[::-1]              # reverse the finish order
```

Produces a valid order too — often a **different** one from Kahn's, which is
fine (any valid order is accepted). Same `O(V + E)`.

### The BFS↔DFS answer the interviewer wants

> "Both `O(V+E)`. Kahn's BFS gives the topological order directly as the dequeue
> sequence and detects cycles via `len(order) != numCourses`. DFS post-order
> builds it as reversed finish-order and detects cycles via a gray node. I'd use
> Kahn's for the very natural 'process what's unblocked' narration; DFS is
> equally valid."

---

## 10. Complexity — derived step by step

**V and E:** `V = numCourses`, `E = len(prerequisites)`.

**Time:**
- Build graph + indegree: `O(E)`.
- Kahn's BFS: each node enqueued/dequeued once (`O(V)`), each edge relaxed once
  (`O(E)`).
- Final validity check (`len(order) == numCourses`): `O(1)`.
- **Total: `O(V + E)`.**

**Space:**
- Adjacency list `O(V + E)`, `indegree` array `O(V)`, `order` output `O(V)`,
  queue `O(V)`.
- **Total: `O(V + E)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| No prerequisites | every course indegree `0` → `order` is `[0, 1, ..., numCourses-1]` (in enqueue order) |
| Cycle (any size) | `len(order) < numCourses` → return `[]` |
| Single course | `[0]` |
| Multiple valid orders exist | returns whichever one the queue order produces — all accepted |
| Disconnected DAG components | all get processed independently; interleaved in `order` by indegree timing |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Returning `order` even when a cycle exists.** Forgetting the
      `len(order) == numCourses` guard → returns a partial (invalid) order
      instead of `[]`.
- [ ] **Edge direction reversed** (same as Course Schedule) — `[a, b]` → edge
      `b -> a`.
- [ ] **DFS post-order: forgetting to reverse** the finish list — gives the
      *exact reverse* of a valid order (dependents before prerequisites).
- [ ] **DFS: appending in pre-order instead of post-order** — appends a node
      before its dependencies are resolved, producing an invalid order.
- [ ] **Testing pitfall:** asserting against one specific expected list. Valid
      topological orders aren't unique — validate the *property* (every
      prerequisite appears before its dependent, all courses present once), as
      the `_is_valid_order` helper does.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Kahn's dequeue sequence IS a topological order** — you don't build the
   order separately, you just record the order nodes come out.
2. **"Feasible?" and "give me the schedule" are the same algorithm** — the
   difference is one line (keep the list vs. count).
3. **Topological order is not unique** — if a problem wants a *specific* one
   (lexicographically smallest, minimize some cost), you change the queue's
   *selection rule* (min-heap, LIFO, greedy), not the overall algorithm.

| Problem | How this transfers |
|---|---|
| Course Schedule | this minus the order list |
| Alien Dictionary | build edges from word comparisons, then this exact algorithm on the alphabet |
| "Smallest valid order" | swap `deque` for a min-heap |
| Build systems / task runners / package managers | topological order of a dependency DAG is the execution order |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Return the **lexicographically smallest** valid order (when several courses are ready, prefer the smallest-numbered one)."

- **(b) Pattern:** Kahn's algorithm with a **priority queue** instead of a plain
  FIFO queue.
- **(c) Adapt:** replace `deque` with a min-heap (`heapq`). Whenever multiple
  courses have indegree `0`, `heappop` always returns the smallest-numbered one.
  Complexity rises to `O((V + E) log V)` for the heap operations.
- **(d) Say:** "Any tie-breaking rule on a topological order is just a change to
  *which* ready node you pick next — swap the FIFO queue for a min-heap for
  lexicographically smallest, a max-heap for largest, and so on. The rest of the
  algorithm is untouched."

### Scenario 2 — "Return **every** valid topological order, not just one."

- **(b) Pattern:** **backtracking** over Kahn's choices.
- **(c) Adapt:** at each step, the set of indegree-`0` nodes are all valid next
  choices. Try each one: append it to the current path, decrement its neighbors'
  indegrees, recurse, then undo (restore indegrees, pop from path). Collect a
  full path whenever its length reaches `numCourses`. **Complexity is
  exponential** — the number of valid orders can be up to `V!` (e.g., no
  prerequisites at all) — so this is only viable for small graphs; say so
  explicitly.
- **(d) Say:** "Enumerating all topological orders is backtracking over the
  'which ready node next' choice, and it's inherently exponential — I'd flag the
  blow-up and confirm the input is small before committing to it."

### Scenario 3 — "Each course has a duration. Return a valid order **and** the earliest possible start time for each course, assuming unlimited parallelism."

- **(b) Pattern:** topological order + **longest-path DP** (the critical-path
  method from Course Schedule Scenario 3).
- **(c) Adapt:** process courses in Kahn's dequeue order. `start[course] =
  max(start[p] + duration[p] for each prerequisite p of course, default 0)`.
  Emit both the order and the `start` array. `O(V + E)`.
- **(d) Say:** "Adding durations turns this into a project-scheduling problem:
  the topological order gives the sequence, and one DP relaxation per edge gives
  each task's earliest start."

### Scenario 4 — "Some prerequisite entries reference course numbers `>= numCourses` (bad data). Ignore those and still return a valid order for the real courses."

- **(b) Pattern:** defensive input handling wrapped around the same algorithm.
- **(c) Adapt:** while building the graph, skip any pair `[a, b]` where `a` or
  `b` is out of `[0, numCourses)`. Everything downstream is unchanged. (Decide
  with the interviewer whether a malformed pair should be silently dropped or
  should invalidate the whole input — both are defensible; state your
  assumption.)
- **(d) Say:** "Malformed edges get filtered at graph-construction time; the
  core algorithm shouldn't have to know about bad input. I'd confirm whether
  'ignore' or 'reject the whole thing' is the desired behavior."

### Scenario 5 — "Among all valid orders, prefer one where each course is taken **as soon as possible after** its last prerequisite (minimize how 'stale' a course's prerequisites are by the time you take it)."

- **(b) Pattern:** a selection-rule change on Kahn's — this time favoring
  recency.
- **(c) Adapt:** use a **stack (LIFO)** instead of a FIFO queue: after finishing
  a course, its freshly-unblocked dependents go on top and get taken next, so a
  dependent tends to immediately follow the prerequisite that unblocked it. This
  is a heuristic (it doesn't provably minimize a formal staleness metric for all
  graphs), so name it as such; a fully optimal version would require defining the
  exact objective and likely a more involved search.
- **(d) Say:** "FIFO Kahn's spreads work out breadth-first; LIFO Kahn's keeps
  dependents right behind their prerequisites. Which 'flavor' of valid order you
  want is a queue-discipline choice — but I'd be upfront that LIFO is a heuristic
  for 'minimize staleness,' not a proven optimum."

### Scenario 6 — "This is a package manager. Given the set of already-installed packages and a list of new packages to install (with the full dependency graph), produce an install order covering only the new packages and their not-yet-installed transitive dependencies."

- **(b) Pattern:** **topological sort on an induced subgraph** — first compute
  *which* nodes matter, then sort only those.
- **(c) Adapt:** (1) From the requested packages, DFS/BFS along dependency edges
  to collect the full set of transitive dependencies; subtract the
  already-installed set → that's the "needed" node set `S`. (2) Build the
  subgraph induced by `S` (only edges with both endpoints in `S`), compute
  indegrees within `S`, and run Kahn's algorithm on `S` alone. `O(|S| +
  edges within S)`.
- **(d) Say:** "Real dependency-resolution problems are two steps: reachability
  to figure out the relevant subset, then a topological sort restricted to that
  subset — never sort the whole universe when only a slice needs installing."

---

## 15. Flashcards

**Q:** How does Course Schedule II differ from Course Schedule?
**A:** One line — keep the `order` list Kahn's builds (the dequeue sequence)
instead of just counting; return `[]` if `len(order) != numCourses`.

**Q:** Why is the dequeue sequence automatically a valid topological order?
**A:** A node is only enqueued once its indegree hits 0, meaning every
prerequisite was already dequeued (and appended) before it.

**Q:** Is the topological order unique?
**A:** No. Any valid order is accepted. To get a *specific* one (e.g.
lexicographically smallest), change the queue's selection rule (min-heap), not
the algorithm.

**Q:** DFS post-order version — the two easy-to-get-wrong details?
**A:** Append on *finish* (post-order), not on entry; and **reverse** the
finished list at the end.

**Q:** Time and space?
**A:** `O(V + E)` both.

**Q:** How should you test this, given non-unique output?
**A:** Validate the property — all courses present once, every prerequisite
before its dependent — not equality against one fixed expected list.

**Q:** "Lexicographically smallest valid order" — the change?
**A:** Swap the FIFO `deque` for a min-heap; complexity becomes
`O((V+E) log V)`.

**Q:** Package-manager "install order for only what's needed" — the two steps?
**A:** (1) Reachability to find the needed transitive-dependency subset minus
already-installed; (2) topological sort restricted to that subset.
