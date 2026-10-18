# Course Schedule  ·  LeetCode 207  ·  Medium

Group 06 — Topological Sort / Cycle Detection  ·  the yes/no version: **is it
even possible** to complete every course given the prerequisites?

Prereqs: `concepts/02` (graph representations), `concepts/06` (cycle detection —
especially the directed-graph pitfall), `concepts/07` (topological sort, Kahn's
algorithm). This problem is Kahn's algorithm with the output list discarded —
you only need to know *whether* it completes, not the order itself.

---

## 1. Problem

There are `numCourses` courses, labeled `0` to `numCourses - 1`. You're given
`prerequisites`, where `prerequisites[i] = [a, b]` means **you must take course
`b` before course `a`**.

**Return `True` if you can finish all courses, `False` if it's impossible**
(i.e., there's a circular dependency).

Constraints:
- `1 <= numCourses <= 2000`.
- `0 <= prerequisites.length <= 5000`.
- No duplicate edges, no self-loops (`a != b`).

Example 1:

```
numCourses = 2, prerequisites = [[1,0]]
answer = True     # take 0, then 1
```

Example 2:

```
numCourses = 2, prerequisites = [[1,0],[0,1]]
answer = False    # 1 needs 0, but 0 needs 1 -> circular, impossible
```

---

## 2. Explain Like I'm 5

Imagine a row of dominoes representing courses, where some dominoes can only
fall after certain other specific dominoes have already fallen (their
"prerequisite" dominoes). You want to know: **can every single domino
eventually fall?**

Start by finding every domino that has **no prerequisite at all** — those can
fall immediately. Knock them over. Falling a domino might satisfy the
prerequisite for some other domino — if that domino now has *all* its
prerequisites satisfied, it can fall too. Keep going.

If every domino eventually falls, you're done — `True`. But if you get stuck with
some dominoes still standing, each still waiting on a prerequisite that itself
is *also* still waiting (a circle of dominoes all waiting on each other) — those
will **never** fall. `False`.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Prerequisite," "before," "can you finish" | ✅ |
| Directed relationship (`a` needs `b`, not symmetric) | ✅ |
| Plain yes/no, no order requested (yet) | ✅ |

**Reduce it to:** *"Build a directed graph from the prerequisite pairs; run
Kahn's algorithm; if every node gets processed, it's possible — otherwise a
cycle exists and it's impossible."* Equivalently: **this is directed cycle
detection** — "can finish" means "no cycle."

**Look-alikes:**
- Course Schedule II (next) — identical setup, but return the actual order
  instead of just `True`/`False`.
- Redundant Connection / Graph Valid Tree (Group 07) — cycle detection too, but
  on an **undirected** graph, so Union-Find is the natural tool there instead.

---

## 4. Intuition

1. Model it as a graph: `b -> a` for every pair `[a, b]` (b must come before a).
2. A valid course order exists **if and only if this graph has no cycle** — a
   cycle would mean some set of courses all transitively require each other,
   with no valid starting point.
3. Kahn's algorithm (`concepts/07`) both **detects the cycle** and **would build
   the order**, in one pass: repeatedly take a course with no remaining
   unsatisfied prerequisite (indegree `0`), "take" it (which satisfies it as a
   prerequisite for its dependents — decrement their indegree), and repeat.
4. If every course eventually gets processed this way, no cycle existed. If some
   courses are left over at the end, they (and whatever they depend on) form a
   cycle — each is permanently stuck waiting on the others.

---

## 5. Approach (primary): Kahn's algorithm (BFS)

1. Build `graph = defaultdict(list)` and `indegree = [0] * numCourses`. For each
   `[a, b]` in `prerequisites`: `graph[b].append(a)`, `indegree[a] += 1`.
2. `q = deque(course for course in range(numCourses) if indegree[course] == 0)`.
3. `processed = 0`. While `q`: pop `course`, `processed += 1`; for each `nei` in
   `graph[course]`: `indegree[nei] -= 1`; if it hits `0`, push `nei`.
4. Return `processed == numCourses`.

Builds on: `concepts/07` Kahn's algorithm, verbatim — this problem only needs the
final count, not the order.

---

## 6. Pseudocode

```
function canFinish(numCourses, prerequisites):
    graph = adjacency list, indegree = array of 0s, size numCourses
    for (a, b) in prerequisites:
        graph[b].append(a)
        indegree[a] += 1

    q = queue of all courses with indegree 0
    processed = 0
    while q not empty:
        course = dequeue
        processed += 1
        for nei in graph[course]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                enqueue nei

    return processed == numCourses
```

---

## 7. Dry Run

```
numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
```

Edges (`b -> a`): `0->1, 0->2, 1->3, 2->3`. `indegree = [0,1,1,2]`.
`q = [0]` (only course `0` starts with no prerequisite).

| pop | processed | neighbor updates | queue after |
|---|---|---|---|
| 0 | 1 | indeg[1]: 1→0 → enqueue 1; indeg[2]: 1→0 → enqueue 2 | [1, 2] |
| 1 | 2 | indeg[3]: 2→1 (not yet 0) | [2] |
| 2 | 3 | indeg[3]: 1→0 → enqueue 3 | [3] |
| 3 | 4 | no neighbors | [] |

`processed == 4 == numCourses` → **True**.

Now the cyclic example: `numCourses = 2, prerequisites = [[1,0],[0,1]]`. Edges:
`0->1` (from `[1,0]`) and `1->0` (from `[0,1]`). `indegree = [1, 1]` — **neither**
course starts at indegree `0`. `q = []` from the very first line. The `while`
loop never runs. `processed = 0 != 2` → **False**. The two courses are stuck
waiting on each other forever — a 2-node cycle.

---

## 8. Python Code (primary — Kahn's algorithm)

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        indegree = [0] * numCourses

        for a, b in prerequisites:            # "a requires b" -> edge b -> a
            graph[b].append(a)
            indegree[a] += 1

        q = deque(course for course in range(numCourses) if indegree[course] == 0)
        processed = 0

        while q:
            course = q.popleft()
            processed += 1
            for nei in graph[course]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        return processed == numCourses


if __name__ == "__main__":
    sol = Solution()

    assert sol.canFinish(2, [[1, 0]]) is True
    assert sol.canFinish(2, [[1, 0], [0, 1]]) is False
    assert sol.canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
    assert sol.canFinish(1, []) is True                          # single course, no prereqs
    assert sol.canFinish(3, [[0, 1], [1, 2], [2, 0]]) is False    # 3-cycle
    assert sol.canFinish(5, []) is True                           # no prerequisites at all

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS with 3 colors (directed cycle detection)

```python
def canFinish(self, numCourses, prerequisites):
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * numCourses

    def dfs(node):
        color[node] = GRAY
        for nei in graph[node]:
            if color[nei] == GRAY:
                return False            # back edge to an ancestor -> cycle
            if color[nei] == WHITE and not dfs(nei):
                return False
        color[node] = BLACK
        return True

    return all(color[c] != WHITE or dfs(c) for c in range(numCourses))
```

Equally correct, same `O(V+E)`. **The critical detail**: 3 colors, not a single
`visited` set — re-reaching an already-**black** node (fully explored via a
different path) is completely normal in a DAG and must **not** be flagged as a
cycle. Only a **gray** node (a live ancestor on the current path) signals one.
See `concepts/06`'s "diamond trap" for the exact failure mode of getting this
wrong.

### The BFS↔DFS answer the interviewer wants

> "Both are `O(V+E)`. Kahn's BFS reads very naturally as 'take what's ready,
> repeat' and directly counts how many courses got processed. DFS with 3 colors
> is equally valid and is the natural choice if I'm already doing a DFS-based
> traversal elsewhere in the same solution. I'd default to Kahn's here since the
> very next problem (Course Schedule II) needs the actual order, which Kahn's
> gives for free."

---

## 10. Complexity — derived step by step

**V and E:** node = a course, `V = numCourses`; edge = a prerequisite pair,
`E = len(prerequisites)`.

**Time:**
- Building the graph + indegree array: one pass over `prerequisites` → `O(E)`.
- Kahn's BFS: each course enqueued at most once (`O(V)`), each edge examined
  once when decrementing indegree (`O(E)`).
- **Total: `O(V + E)`.**

**Space:**
- Adjacency list: `O(V + E)`.
- `indegree` array + queue: `O(V)`.
- **Total: `O(V + E)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| No prerequisites at all | every course starts at indegree `0` → all processed immediately → `True` |
| A 2-cycle (`[1,0],[0,1]`) | neither course starts at indegree `0` → queue starts empty → `False` |
| A longer cycle not involving all courses | the cyclic courses never reach indegree `0`; `processed < numCourses` → `False` |
| Single course, no prerequisites | trivially `True` |
| A course listed as its own prerequisite (self-loop, disallowed by constraints but worth reasoning about) | its indegree would never reach `0` via itself → correctly never processed → `False` |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Reversing the edge direction.** `[a, b]` means "a requires b" → edge
      `b -> a`, i.e. `graph[b].append(a)` and `indegree[a] += 1`. Writing
      `graph[a].append(b)` instead silently inverts the entire dependency graph.
- [ ] **Using a single `visited` set for a DFS-based check** instead of 3 colors
      — the #1 conceptual bug for *any* directed cycle detection (see
      `concepts/06`). Flags false cycles on any DAG with a "diamond" shape.
- [ ] **Comparing `processed` to `len(prerequisites)` instead of `numCourses`.**
      The success condition is about courses (nodes), not edges.
- [ ] **Off-by-one on `indegree` array size** — must be `numCourses`, not
      `len(prerequisites)`.
- [ ] **Forgetting courses with zero prerequisites AND zero dependents** (isolated
      nodes) — they still belong in the initial queue (indegree `0`) and count
      toward `processed`; a bug that only iterates over nodes appearing in
      `prerequisites` would miss them.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **"Can finish" = "no cycle"** — many yes/no dependency questions reduce to
   directed cycle detection, which topological sort answers for free as a side
   effect.
2. **Kahn's algorithm is both a cycle detector and an order-builder** — running
   it once gives you both answers; whether you *use* the order depends on what
   the problem asks (this problem discards it, the next one keeps it).
3. **Directed cycle detection needs 3 colors, not a boolean set** — this is worth
   over-learning now, because it's the single most common silent bug in this
   entire pattern group.

| Problem | How this transfers |
|---|---|
| Course Schedule II | identical setup; keep the `order` list instead of discarding it |
| Alien Dictionary | you must first *build* the edges (from comparing adjacent words), then it's this exact algorithm |
| Minimum Height Trees | Kahn's-style peeling, generalized to undirected trees (peel by degree, not indegree) |
| Any "is a valid build/dependency order possible" question | directed cycle detection via Kahn's or 3-color DFS |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Also return a valid course order (not just yes/no)."

- **(b) Pattern:** this is exactly **Course Schedule II**, the very next
  problem in this repo.
- **(c) Adapt:** keep the `order` list Kahn's algorithm already builds instead of
  discarding it; return `order` if `len(order) == numCourses`, else `[]`.
- **(d) Say:** "Course Schedule already computes the order internally — the
  'yes/no' version just throws it away. Keeping it is the whole difference."

### Scenario 2 — "Some prerequisite pairs mean 'must be taken in the *same* semester' (a symmetric, undirected constraint) alongside the usual 'before' (directed) constraints."

- **(b) Pattern:** a hybrid of **Union-Find** (Group 07) and topological sort.
- **(c) Adapt:** first, use Union-Find to merge every "same semester" pair into
  one combined group/super-node. Then build the directed "before" graph **on
  the groups** (an edge between two groups if any course in one requires any
  course in the other), and run Kahn's algorithm on that condensed graph. A
  cycle *within* a same-semester group (via a "before" edge) would be
  immediately impossible — worth an explicit check.
- **(d) Say:** "Symmetric 'grouped together' constraints get collapsed with
  Union-Find first; the directed dependency logic then runs on the resulting
  condensed graph, unchanged."

### Scenario 3 — "Each course has a duration (time to complete). Courses whose prerequisites are satisfied can be taken in parallel with unlimited capacity. What's the minimum total time to finish all courses?"

- **(b) Pattern:** **longest path in a DAG** — a critical-path scheduling
  problem, computed via topological order + DP.
- **(c) Adapt:** process nodes in topological order (Kahn's naturally gives this
  order as it pops nodes). For each course, `finish_time[course] = duration[course]
  + max(finish_time[p] for p in its prerequisites, default 0)`. The answer is
  `max(finish_time)` over all courses. `O(V + E)` — same traversal, one extra DP
  update per edge.
- **(d) Say:** "The moment 'can you finish' becomes 'what's the minimum time to
  finish everything, given parallelism,' it's a longest-path-in-a-DAG /
  critical-path problem — solved by adding one DP relaxation on top of the exact
  same topological traversal."

### Scenario 4 — "There's a cap on how many courses you can take per semester (limited capacity). Minimize the number of semesters."

- **(b) Pattern:** the **unlimited**-capacity version of this (any number of
  ready courses per semester) is just "count the number of BFS rounds" — the
  Rotting-Oranges ring-counting idea applied to Kahn's algorithm (this is
  LeetCode 1494, Parallel Courses). The **capacity-limited** version is
  materially harder — now you must *choose which* ready courses to take each
  semester when there are more ready than capacity allows, which can affect which
  courses become ready next.
- **(c) Adapt:** for unlimited capacity: run Kahn's algorithm ring-by-ring
  (freeze `len(q)` per round, like Rotting Oranges), incrementing a semester
  counter per round. For limited capacity: flag it as a harder scheduling/
  bin-packing-flavored problem — a reasonable interview answer is a greedy
  heuristic (prioritize courses that unblock the most future courses) while being
  explicit that greedy isn't provably optimal here, and that true optimality may
  require more advanced techniques (e.g., ILP) depending on the exact constraints.
- **(d) Say:** "Unlimited-capacity semester counting is just ring-counted Kahn's.
  The moment capacity is limited, I'd name it as combinatorially harder rather
  than force a clean polynomial answer that doesn't exist in general."

### Scenario 5 — "If it's impossible, report the actual cycle (the specific courses forming it), not just `False`, so the user can see why."

- **(b) Pattern:** cycle detection **plus path reconstruction** — extend the
  DFS 3-color approach (9a) to track the current path.
- **(c) Adapt:** maintain a `path` stack alongside the DFS (push on entry, pop on
  exit/mark-black). The moment you hit a **gray** node `g`, the cycle is exactly
  the suffix of `path` from `g` to the current node — slice it out. `O(V+E)`
  time, `O(V)` extra space for the path stack.
- **(d) Say:** "Kahn's BFS naturally tells you *that* a cycle exists (leftover
  courses) but not *which* one directly; DFS with an explicit path stack gives
  you the exact cycle the moment you hit a gray node."

### Scenario 6 — "This is a real distributed build system: services declare dependencies on each other dynamically, and new dependency edges are added continuously. Continuously verify no cyclic dependency has been introduced."

- **(b) Pattern:** **incremental** / online cycle detection on a directed graph
  — a genuinely advanced systems topic, worth naming as such rather than
  papering over.
- **(c) Adapt:** the simple, defensible approach: after each new edge is added,
  re-run a bounded check — you only need to verify whether the new edge's
  endpoints are now mutually reachable (a single BFS/DFS from the edge's
  destination back to its source), not a full `O(V+E)` re-scan of the whole
  graph — still `O(V+E)` worst case per edge, but often much cheaper in
  practice. For true high-throughput systems, note that **online topological
  order maintenance** under edge insertions is an active algorithms research
  area (algorithms achieving better-than-naive amortized cost per insertion
  exist) — name it as such rather than claim a simple trick solves it optimally.
- **(d) Say:** "The pragmatic answer is checking reachability from the new
  edge's target back to its source on each insertion; for extreme scale, I'd
  flag that maintaining topological order online under insertions is a real,
  actively-studied algorithms problem, not something to improvise a perfect
  answer to on the spot."

---

## 15. Flashcards

**Q:** How does "can finish all courses" reduce to a graph question?
**A:** It's directed cycle detection — a valid order exists iff the
prerequisite graph has no cycle.

**Q:** Which direction does the edge go for a pair `[a, b]` ("a requires b")?
**A:** `b -> a` (b must come before a) — `graph[b].append(a)`,
`indegree[a] += 1`. Reversing this is the most common bug.

**Q:** How does Kahn's algorithm detect a cycle?
**A:** Nodes in a cycle can never reach indegree 0 (each always has an
unprocessed prerequisite within the cycle) — if `processed < numCourses` at the
end, a cycle exists.

**Q:** Why must directed cycle detection via DFS use 3 colors, not one
`visited` set?
**A:** Re-reaching an already-fully-explored (black) node via a different path
is normal in a DAG, not a cycle. Only reaching a **gray** (currently-on-path)
node signals a real cycle.

**Q:** Time and space, with derivation?
**A:** `O(V + E)` both — build the graph/indegree array in `O(E)`, Kahn's BFS
visits each node once and each edge once.

**Q:** "Also give me a valid order" — what changes?
**A:** Nothing algorithmically — Kahn's already builds that order; just keep it
instead of discarding it (Course Schedule II).

**Q:** Per-course durations, minimize total time with unlimited parallelism —
which technique?
**A:** Longest path in a DAG: process in topological order, DP
`finish_time[node] = duration[node] + max(finish_time[prereq])`.

**Q:** Limited courses per semester (capacity cap) — same difficulty?
**A:** No — unlimited capacity is just ring-counted Kahn's (BFS rounds =
semesters); limited capacity becomes a harder scheduling/bin-packing-flavored
problem without a clean polynomial exact solution in general.
