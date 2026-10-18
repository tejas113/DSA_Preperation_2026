# Group 06 — Topological Sort / Cycle Detection

## What this pattern is

You have tasks with **dependencies** ("do X before Y"). You need to know either
(a) whether it's even *possible* to do everything (no circular dependency), or
(b) an actual valid order to do them in.

The tool: build a **directed graph** where an edge `u -> v` means "u before v,"
compute each node's **indegree** (how many unsatisfied prerequisites it has),
then repeatedly **peel off nodes with indegree 0** (Kahn's algorithm,
`concepts/07`). If you can peel off every node, you have both your answer *and*
a valid order. If you get stuck with nodes left over, those leftover nodes form
a **cycle** — impossible to order.

## How to recognize it

- Words: "prerequisite," "before," "dependency," "build order," "can you
  finish," "valid sequence," "task scheduling."
- The relationship is **directed** (`A` before `B` is not the same as `B` before
  `A`).
- Either a yes/no ("is it possible") or "give me a valid order" question.

## The template

```python
from collections import defaultdict, deque

def can_finish_all(n, prereq_pairs):
    graph = defaultdict(list)
    indegree = [0] * n
    for a, b in prereq_pairs:          # "a requires b" -> edge b -> a
        graph[b].append(a)
        indegree[a] += 1

    q = deque(node for node in range(n) if indegree[node] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)

    return order if len(order) == n else []     # [] means impossible (a cycle exists)
```

## Complexity for the whole group

- **Time:** `O(V + E)` — build the graph and indegree array in `O(E)`, Kahn's
  BFS visits each node once and each edge once.
- **Space:** `O(V + E)` for the adjacency list, `O(V)` for indegree/output.

## Problems

1. `01-course-schedule.md` — the yes/no version: is a valid order even possible?
   (LeetCode 207). **Start here.**
2. `02-course-schedule-ii.md` — return the actual order (LeetCode 210).
3. `03-alien-dictionary.md` — build the edges yourself from word comparisons,
   then topologically sort the alphabet (LeetCode 269, premium).
4. `04-minimum-height-trees.md` *(supplementary)* — the leaf-peeling variant of
   Kahn's algorithm, applied to an undirected tree (LeetCode 310).
5. `05-longest-increasing-path-in-a-matrix.md` *(supplementary)* — an implicit
   DAG (cells ordered by height) + memoized DFS; conceptually a topological-order
   idea without ever building an explicit topological sort (LeetCode 329).
