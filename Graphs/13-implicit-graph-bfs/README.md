# Group 13 — Implicit-Graph BFS

## What this pattern is

The graph is **never built**. You're not handed nodes and edges — you're handed a
**start state**, a **goal test**, and a **rule for legal moves**. The "nodes" are
*states*; the "edges" are *one legal move to another state*. Run BFS over that,
generating neighbors on the fly.

Because every move counts as one step, **BFS gives the fewest moves** — that's
almost always what these problems ask.

## How to recognize it

- "Minimum number of **moves / steps / transformations / rolls / mutations** to
  get from A to B."
- Each move follows a fixed rule (roll a die; change one letter; flip one gene;
  step to an adjacent cell).
- There's no explicit `edges` array — the connections are *implied* by the rule.

## The template — it's just `concepts/03` BFS with a `neighbors()` function

```python
from collections import deque

def bfs(start, is_goal, neighbors):
    if is_goal(start):
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        state, steps = q.popleft()
        for nxt in neighbors(state):          # generated from the rule, not looked up
            if nxt not in seen:
                if is_goal(nxt):
                    return steps + 1
                seen.add(nxt)
                q.append((nxt, steps + 1))
    return -1                                  # unreachable
```

Everything you learned in Groups 01–02 applies verbatim — mark visited on
enqueue, level-count for "fewest steps," multi-source if there are several
starts. The *only* new skill is **writing `neighbors(state)`** for each puzzle.

## The states, per problem

| Problem | A state is... | `neighbors(state)` = ... |
|---|---|---|
| Snakes and Ladders | a board square `1..n²` | `s+1 .. s+6`, then follow any snake/ladder |
| Minimum Genetic Mutation | an 8-char gene string | change one char to `A/C/G/T`, keep only if in the bank |
| Word Ladder | a word | change one letter, keep only if in the word list |
| Shortest Path in Binary Matrix | a cell `(r, c)` | the 8 neighboring `0` cells |
| Word Ladder II | a word | same as Word Ladder, but keep **all** shortest paths |
| Shortest Path Visiting All Nodes | `(node, visited-bitmask)` | `(neighbor, mask │ bit[neighbor])` |

## Complexity

`O(V + E)` where `V` = number of reachable states and `E` = total generated
moves. The cost of one `neighbors()` call (e.g. `L × 25` for Word Ladder) is a
multiplier — spell it out per problem.

## Problems

1. `01-snakes-and-ladders.md` — board game; state = square (LeetCode 909).
   **Start here.**
2. `02-minimum-genetic-mutation.md` — state = gene string; validity = "in the
   bank" (LeetCode 433).
3. `03-word-ladder.md` — state = word; the canonical implicit-graph BFS
   (LeetCode 127).
4. `04-shortest-path-in-binary-matrix.md` *(supplementary)* — 8-directional grid
   BFS (LeetCode 1091).
5. `05-word-ladder-ii.md` *(supplementary)* — BFS + reconstruct **every** shortest
   transformation (LeetCode 126).
6. `06-shortest-path-visiting-all-nodes.md` *(supplementary)* — BFS where the
   state carries a **bitmask** of visited nodes (LeetCode 847).
