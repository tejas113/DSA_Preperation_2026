# Reconstruct Itinerary  ·  LeetCode 332  ·  Hard

Group 14 — Eulerian Path  ·  the canonical "use every edge exactly once" problem.
One trick — **Hierholzer's algorithm** — and no BFS/DFS fallback if you don't
know it.

Prereqs: `concepts/04` (DFS), `14-eulerian-path/README.md` (Hierholzer).

---

## 1. Problem

You have a list of airline `tickets`, `tickets[i] = [from_i, to_i]` (3-letter
airport codes). Reconstruct the itinerary in order. It must:

- **Start at `"JFK"`**.
- **Use every ticket exactly once.**
- Among all valid itineraries, be the **lexicographically smallest** when read as
  a single concatenated string.

The input is guaranteed to have at least one valid itinerary.

Constraints:
- `1 <= tickets.length <= 300`.
- All codes are 3 uppercase letters.

Example 1:

```
tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
answer  = ["JFK","MUC","LHR","SFO","SJC"]
```

Example 2:

```
tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
answer  = ["JFK","ATL","JFK","SFO","ATL","SFO"]
# ["JFK","SFO","ATL","JFK","ATL","SFO"] is also valid but lexically larger.
```

---

## 2. Explain Like I'm 5

You have a stack of one-way plane tickets. You must use **all** of them, each
exactly once, and you start in JFK. Print the cities in the order you visit them.
If there's a choice of where to fly next, always pick the airport whose name
comes first alphabetically.

The way to do it: from wherever you are, keep flying out on the
alphabetically-smallest ticket you still have, going deeper and deeper. When you
land somewhere with **no tickets left**, that airport is the *last* stop of your
whole trip (or the last stop of a little loop) — write it down and back up. Keep
backing up and writing down airports as you run out of tickets. When you're done,
the list you wrote is your itinerary **backwards** — flip it.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Use **every ticket / edge** exactly once" | ✅ → **Eulerian path** |
| Directed graph (one-way tickets), fixed start | ✅ |
| "Reconstruct the tour / route / arrangement" | ✅ |
| Lexicographically smallest among valid ones | ✅ → take the smallest edge first (min-heap) |

**Reduce it to:** *"Find the lexicographically smallest Eulerian path from `JFK`
in the directed multigraph of tickets. Hierholzer's algorithm: DFS taking the
smallest next edge, append each node to the route **on the way out**, reverse at
the end."*

**Not** a shortest-path or a BFS problem. **Not** Hamiltonian (which would be
NP-hard). "Every edge once" = Eulerian = polynomial.

---

## 4. Intuition

1. Each ticket is a **directed edge**. Using all tickets exactly once, starting
   at `JFK`, is exactly an **Eulerian path** from `JFK`.
2. **Greedy alone isn't enough.** If you just always fly the smallest ticket, you
   can walk into an airport, get stuck there with tickets still unused elsewhere,
   and have no way to represent "go back and do those." Hierholzer fixes this
   with a **post-order** trick.
3. **Hierholzer:** `dfs(node)` — while `node` still has an outgoing ticket, pop
   the smallest and recurse into it. *After* the loop (node has no tickets left),
   **append `node` to `route`.**
4. Because a node is appended only after *everything reachable via its tickets*
   is appended, `route` comes out **reversed**. Flip it → the itinerary.
5. The post-order append is what **splices sub-loops** into the right place: if
   the DFS dives into a loop that returns to a node which still had other
   tickets, those other tickets' branch gets appended first (deeper in the
   recursion), landing *before* this node in the final reversed order.
6. Using a **min-heap** per node makes "smallest ticket first" automatic → the
   lexicographically smallest Eulerian path.

---

## 5. Approach (primary): Hierholzer's algorithm, recursive

1. Build `graph = defaultdict(list)`; for each `[src, dst]`, `heapq.heappush(
   graph[src], dst)` (a min-heap of destinations, duplicates allowed).
2. `route = []`.
3. `dfs(node)`:
   - While `graph[node]` is non-empty: `dfs(heapq.heappop(graph[node]))`.
   - `route.append(node)`  ← **post-order**.
4. `dfs("JFK")`.
5. Return `route[::-1]`.

Builds on: `concepts/04` DFS, with the post-order append being the Eulerian
twist.

---

## 6. Pseudocode

```
function findItinerary(tickets):
    graph = map: airport -> min-heap of destination airports
    for [src, dst] in tickets:
        push dst onto graph[src]

    route = []
    function dfs(node):
        while graph[node] not empty:
            dfs(pop-min graph[node])          # consume a ticket, fly there
        route.append(node)                    # no tickets left here -> record

    dfs("JFK")
    return reverse(route)
```

---

## 7. Dry Run

```
tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
```

Heaps: `JFK: [ATL, SFO]`, `SFO: [ATL]`, `ATL: [JFK, SFO]`.

`dfs("JFK")`:

| call | node's heap (before pop) | action | route (post-order appends) |
|---|---|---|---|
| dfs(JFK) | [ATL, SFO] | pop ATL → dfs(ATL) | |
| dfs(ATL) | [JFK, SFO] | pop JFK → dfs(JFK) | |
| dfs(JFK) | [SFO] | pop SFO → dfs(SFO) | |
| dfs(SFO) | [ATL] | pop ATL → dfs(ATL) | |
| dfs(ATL) | [SFO] | pop SFO → dfs(SFO) | |
| dfs(SFO) | [] | append SFO | `[SFO]` |
| ↑ back in dfs(ATL) | [] | append ATL | `[SFO, ATL]` |
| ↑ back in dfs(SFO) | [] | append SFO | `[SFO, ATL, SFO]` |
| ↑ back in dfs(JFK) | [] | append JFK | `[SFO, ATL, SFO, JFK]` |
| ↑ back in dfs(ATL) | [] | append ATL | `[SFO, ATL, SFO, JFK, ATL]` |
| ↑ back in dfs(JFK) | [] | append JFK | `[SFO, ATL, SFO, JFK, ATL, JFK]` |

`route[::-1]` = `["JFK","ATL","JFK","SFO","ATL","SFO"]`. ✅

---

## 8. Python Code (primary — recursive Hierholzer)

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)
        for src, dst in tickets:
            heapq.heappush(graph[src], dst)        # min-heap -> smallest ticket first

        route = []

        def dfs(node: str) -> None:
            while graph[node]:
                dfs(heapq.heappop(graph[node]))    # consume a ticket, fly there
            route.append(node)                     # POST-ORDER: no tickets left -> record

        dfs("JFK")
        return route[::-1]


if __name__ == "__main__":
    sol = Solution()

    assert sol.findItinerary(
        [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    ) == ["JFK", "MUC", "LHR", "SFO", "SJC"]

    assert sol.findItinerary(
        [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    ) == ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]

    assert sol.findItinerary([["JFK", "AAA"]]) == ["JFK", "AAA"]
    assert sol.findItinerary(
        [["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]
    ) == ["JFK", "NRT", "JFK", "KUL"]

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Iterative Hierholzer (explicit stack — no recursion depth risk)

```python
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)
        for src, dst in tickets:
            heapq.heappush(graph[src], dst)

        stack = ["JFK"]
        route = []
        while stack:
            while graph[stack[-1]]:
                stack.append(heapq.heappop(graph[stack[-1]]))
            route.append(stack.pop())              # dead end -> pop to the route
        return route[::-1]
```

Same algorithm; the stack replaces the call stack. Here `tickets ≤ 300` so
recursion is fine, but the iterative form is the safe habit for large inputs.

### 9b. Sorted lists instead of heaps (pop from the end)

```python
graph = defaultdict(list)
for src, dst in sorted(tickets, reverse=True):     # descending, so list.pop() gives the smallest
    graph[src].append(dst)
# ... dfs pops graph[node].pop()
```

Avoids per-node heap overhead; one upfront sort. Equivalent output.

### The BFS↔DFS answer the interviewer wants

> "'Use every ticket exactly once' is an Eulerian path — Hierholzer's DFS with a
> **post-order** append, then reverse. A min-heap per node gives the
> lexicographically smallest one. It's `O(E log E)`. This is *not* BFS/shortest-
> path, and *not* Hamiltonian (which would be NP-hard) — 'every edge once' is the
> polynomial case."

---

## 10. Complexity — derived step by step

**V and E:** `V` = distinct airports, `E = len(tickets)` (`≤ 300`).

**Time:**
- Building the heaps: `E` pushes, `O(E log E)`.
- Hierholzer DFS: each edge is consumed exactly once — `E` `heappop`s, each
  `O(log E)` — plus one `route.append` per vertex visit (`E + 1` of them).
- Reverse: `O(E)`.
- **Total: `O(E log E)`.**

**Space:**
- `graph` heaps: `O(E)`. Recursion/stack depth: `O(E)` worst case. `route`:
  `O(E)`.
- **Total: `O(E)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| One ticket | `["JFK", X]` → `["JFK", X]` |
| Self-loop ticket `["JFK","JFK"]` | consumed like any edge; appears twice in the route |
| Multiple tickets between the same pair (multigraph) | the heap holds duplicates; each is consumed once |
| A sub-loop that must be spliced in (Example 2) | post-order append places it correctly |
| Input guaranteed valid | no need to check Eulerian-existence conditions in the base problem |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Appending on the way *in* (pre-order) instead of *out* (post-order).**
      Pre-order gives a wrong route whenever there's a sub-loop to splice —
      Example 2 breaks. The append must be **after** the `while` loop empties the
      node's tickets.
- [ ] **Forgetting to reverse `route`** at the end — you'd return the itinerary
      backwards.
- [ ] **Not sorting / not using a min-heap** — you get *a* valid itinerary but
      not the lexicographically smallest one.
- [ ] **Using a `set` for adjacency** — loses duplicate tickets in a multigraph.
      Use a list or heap.
- [ ] **Consuming an edge without removing it** — the `while graph[node]` loop
      must `pop` (shrink the heap) each iteration, or it never terminates.
- [ ] **Recursion depth** on a very long chain — 300 tickets is fine; use the
      iterative form (9a) for larger.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **"Use every edge exactly once" = Eulerian path = Hierholzer's algorithm.**
   Polynomial. (Contrast "every *node* once" = Hamiltonian = NP-hard.)
2. **Hierholzer's post-order trick:** DFS, exhaust a node's edges, *then* append
   the node; reverse at the end. The append-after-exhaustion is what splices
   sub-cycles into place — greedy-only walking can't do that.
3. **Greedy-smallest-edge + Hierholzer = the lexicographically smallest Eulerian
   path.**
4. **Existence conditions** (directed): connected + exactly one vertex with
   `out - in = 1` (start), exactly one with `in - out = 1` (end), rest balanced.

| Problem | How this transfers |
|---|---|
| Valid Arrangement of Pairs (LC 2097) | Eulerian path where the start vertex isn't given — find it from degree balance |
| Cracking the Safe (LC 753) | Eulerian circuit in a de Bruijn graph builds the shortest superstring |
| Chinese Postman / route inspection | add the minimum edges to make a graph Eulerian, then Hierholzer |
| "Reconstruct a sequence from all its overlapping k-grams" | Eulerian path in a de Bruijn graph |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Tickets are **round-trip** (the graph is undirected)."

- **(b) Pattern:** Eulerian path/circuit in an **undirected** graph — Hierholzer
  still works, but an undirected edge appears in *both* endpoints' lists, so you
  must mark each edge used, not just pop it.
- **(c) Adapt:** give each undirected edge an id; store `(neighbor, edge_id)` in
  the adjacency lists; keep a `used` set of edge ids. In `dfs`, skip a neighbor
  whose edge id is already `used`; mark it used before recursing. Post-order
  append and reverse as before.
- **(d) Say:** "Undirected means each edge is in two adjacency lists — track a
  `used` set keyed by edge id so you don't traverse it twice."

### Scenario 2 — "You might **not** be able to use all tickets. Return the **longest** valid trip from JFK."

- **(b) Pattern:** this is **not** Eulerian anymore — a longest trail (edge-
  simple path) is **NP-hard** in general.
- **(c) Adapt:** for small inputs, backtracking: try each unused outgoing ticket,
  recurse, undo, track the best. For larger inputs there's no known polynomial
  algorithm — say so and offer a heuristic (greedy + restarts) or an ILP
  formulation.
- **(d) Say:** "Dropping 'must use all' turns it from Eulerian (polynomial) into
  longest-trail (NP-hard) — I'd backtrack for small `n` and be upfront about the
  hardness otherwise."

### Scenario 3 — "Detect whether a valid full itinerary even exists."

- **(b) Pattern:** check the Eulerian-path existence conditions.
- **(c) Adapt:** compute `in`/`out` degree per airport. A valid Eulerian path
  from JFK exists iff (a) every airport with an edge is in one connected
  component (ignoring direction for connectivity, then verifying with a walk),
  (b) JFK has `out - in = 1` (or `= 0` if it's a circuit), (c) exactly one
  airport has `in - out = 1`, (d) all others balanced. Equivalently: run
  Hierholzer and check `len(route) == len(tickets) + 1`.
- **(d) Say:** "Degree balance plus connectivity — or just run Hierholzer and
  verify the route length is `E + 1`."

### Scenario 4 — "Return **all** valid itineraries, not just the smallest."

- **(b) Pattern:** backtracking over ticket choices.
- **(c) Adapt:** from the current airport, try every currently-unused outgoing
  ticket in turn: use it, recurse, un-use it. Record a full itinerary whenever
  all `E` tickets are used. **Exponential** in the number of valid itineraries —
  only viable for small inputs.
- **(d) Say:** "Enumerating all is backtracking over the next-ticket choice, and
  it's exponential — Hierholzer only gives you one (the smallest)."

### Scenario 5 — "Each ticket has a **price**. Among all valid full itineraries, return the **cheapest**."

- **(b) Pattern:** trick question.
- **(c) Adapt:** every valid full itinerary uses **exactly the same set of
  edges** (all tickets, each once), so every valid itinerary has the **same total
  price** — `sum(prices)`. Any valid itinerary (e.g. Hierholzer's) is a cheapest
  one.
- **(d) Say:** "All full itineraries use the identical edge set, so they all cost
  the same — the answer is `sum(prices)` and any valid itinerary."

### Scenario 6 — "The itinerary may start from **any** airport, not just JFK."

- **(b) Pattern:** find a valid Eulerian start vertex first.
- **(c) Adapt:** compute `out - in` per airport. If exactly one airport has
  `out - in = 1`, that's the unique start (Eulerian path). If all are balanced,
  it's an Eulerian circuit — start from any airport that has an outgoing edge.
  Then run Hierholzer from that start.
- **(d) Say:** "Pick the start from degree balance: the `out - in = 1` vertex for
  a path, or any vertex with an edge for a circuit."

---

## 15. Flashcards

**Q:** "Use every ticket / edge exactly once" — what problem is this, and what
algorithm?
**A:** Eulerian path. **Hierholzer's algorithm**: DFS, append each node
**on the way out** (post-order), reverse at the end.

**Q:** Eulerian vs Hamiltonian?
**A:** Eulerian = every *edge* once → polynomial (Hierholzer). Hamiltonian =
every *node* once → NP-hard.

**Q:** Why post-order append + reverse (not just greedy walk)?
**A:** Greedy walking can get stuck with edges unused elsewhere. Appending a node
only *after* its edges are exhausted, then reversing, splices sub-cycles into
their correct positions automatically.

**Q:** How do you get the lexicographically smallest itinerary?
**A:** Store each node's destinations in a **min-heap** (or sorted list); always
take the smallest next edge.

**Q:** The #1 bug?
**A:** Appending in pre-order instead of post-order — breaks whenever a sub-loop
must be spliced in.

**Q:** Time and space?
**A:** `O(E log E)` time (heap the adjacency), `O(E)` space. Each edge consumed
exactly once.

**Q:** Existence conditions for a directed Eulerian path?
**A:** Connected (ignoring isolated vertices) + exactly one vertex with
`out - in = 1` (start), one with `in - out = 1` (end), all others `in = out`.

**Q:** Tickets have prices — cheapest full itinerary?
**A:** Trick: all full itineraries use every edge once, so all cost `sum(prices)`
— any valid one is cheapest.
