# Snakes and Ladders  ·  LeetCode 909  ·  Medium

Group 13 — Implicit-Graph BFS  ·  the graph is a board game. A **state** is a
board square; a **move** is one die roll (plus any forced snake/ladder). BFS =
fewest rolls.

Prereqs: `concepts/03` (BFS, level counting), `13-implicit-graph-bfs/README.md`.

---

## 1. Problem

An `n x n` board. Squares are numbered `1` to `n²` in **boustrophedon** ("ox-
plowing" / zigzag) order: square `1` is the **bottom-left**; the bottom row goes
left→right; the row above goes right→left; and so on alternating.

`board[r][c]` is `-1` (nothing) or a destination square number. You start on
square `1`. Each turn:

1. Roll a die → an integer `1..6`. Move to `curr + roll` (but never past `n²`).
2. If that square has a snake or ladder (`board != -1`), you **must** move to its
   destination — but you take **at most one** snake/ladder per turn (no chaining).

**Return the least number of die rolls to reach square `n²`, or `-1` if
impossible.**

Constraints:
- `2 <= n <= 20`.
- Squares `1` and `n²` have no snake or ladder.

Example 1:

```
n = 6
board = [[-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1],
         [-1,35,-1,-1,13,-1],
         [-1,-1,-1,-1,-1,-1],
         [-1,15,-1,-1,-1,-1]]
answer = 4
```

Example 2: `board = [[-1,-1],[-1,3]]` → `1` (roll 3 from square 1 lands on square
4 = `n²`).

---

## 2. Explain Like I'm 5

It's a board game. You're on square 1 and want to get to the last square. Each
turn you roll a die and hop forward that many squares. If you land on the bottom
of a ladder, you zoom up; on the head of a snake, you slide down.

You want the **fewest rolls**. So imagine trying *all six* die results from your
square, then all six from each of those, spreading out one turn at a time. The
first time this spreading wave touches the last square, that's your answer — the
number of turns it took.

The only fiddly bit is the board's weird numbering: it snakes back and forth row
by row, so you need a little formula to turn "square 23" into "which cell of the
2D array."

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "**Fewest moves / rolls / turns**" | ✅ → BFS (each move = 1 step) |
| Moves follow a fixed rule (roll 1..6, then forced snake/ladder) | ✅ → generate neighbors from the rule |
| No explicit graph — the board *implies* the moves | ✅ → implicit-graph BFS |

**Reduce it to:** *"BFS over board squares. `neighbors(s)` = for each roll `1..6`,
`s + roll` (skip if past `n²`), then apply the snake/ladder at that square if
any. First time BFS reaches `n²` = the answer."*

---

## 4. Intuition

1. Squares are the nodes. From square `s`, a single turn can land you on `s+1 ...
   s+6` — and if that square has a snake/ladder, you're forced to its
   destination instead.
2. Every turn costs exactly `1` roll, so **BFS finds the minimum number of
   rolls** (Group 03 Flavor B — level by level).
3. Mark a square `seen` when you enqueue it, on the **resolved** square (after
   applying the snake/ladder), so you never process the same square twice.
4. The board→square conversion: square `s` (1-indexed) → let `s0 = s - 1`,
   `row_from_bottom = s0 // n`, `col = s0 % n`. The array row is `r = n - 1 -
   row_from_bottom`. The column flips direction on odd rows-from-bottom:
   `c = col` if `row_from_bottom` is even, else `c = n - 1 - col`.

---

## 5. Approach (primary): BFS with a square-lookup helper

1. `n = len(board)`, `target = n*n`.
2. `get_dest(s)`: convert `s` to `(r, c)` (boustrophedon), return `board[r][c]`.
3. `seen = {1}`, `q = deque([(1, 0)])`.
4. While `q`: pop `(square, rolls)`. If `square == target`: return `rolls`.
   For `roll` in `1..6`: `nxt = square + roll`; if `nxt > target`: `break`. If
   `get_dest(nxt) != -1`: `nxt = get_dest(nxt)`. If `nxt not in seen`:
   `seen.add(nxt)`, `q.append((nxt, rolls + 1))`.
5. Return `-1`.

Builds on: `concepts/03` BFS; the new work is `get_dest` + the roll loop.

---

## 6. Pseudocode

```
function snakesAndLadders(board):
    n = len(board);  target = n*n

    function get_dest(s):                 # square number -> board value
        s0 = s - 1
        rfb, col = divmod(s0, n)
        r = n - 1 - rfb
        c = col if rfb even else n - 1 - col
        return board[r][c]

    seen = {1}
    q = queue([(1, 0)])
    while q not empty:
        (square, rolls) = dequeue
        if square == target: return rolls
        for roll in 1..6:
            nxt = square + roll
            if nxt > target: break
            if get_dest(nxt) != -1: nxt = get_dest(nxt)
            if nxt not in seen:
                add nxt to seen
                enqueue (nxt, rolls + 1)
    return -1
```

---

## 7. Dry Run

```
n = 2, board = [[-1,-1],
                [-1, 3]]      target = 4
```

Square numbering (boustrophedon): `1 = board[1][0]`, `2 = board[1][1]`, `3 =
board[0][1]`, `4 = board[0][0]`.
`get_dest(2) = board[1][1] = 3` (a ladder). All others `-1`.

`seen = {1}`, `q = [(1, 0)]`.

| pop | rolls | rolls tried (`nxt` after snake/ladder) | enqueue | seen |
|---|---|---|---|---|
| (1, 0) | 0 | roll 1 → 2 → ladder → **3** ; roll 2 → **3** (seen now) ; roll 3 → **4** ; roll 4 → `5 > 4` break | (3,1), (4,1) | {1,3,4} |
| (3, 1) | 1 | not target | — | — |
| (4, 1) | 1 | **`square == target`** → return **1** | | |

Answer: `1`. ✅

---

## 8. Python Code (primary — BFS)

```python
from collections import deque
from typing import List


class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        target = n * n

        def get_dest(s: int) -> int:
            s0 = s - 1
            row_from_bottom, col = divmod(s0, n)
            r = n - 1 - row_from_bottom
            c = col if row_from_bottom % 2 == 0 else n - 1 - col
            return board[r][c]

        seen = {1}
        q = deque([(1, 0)])
        while q:
            square, rolls = q.popleft()
            if square == target:
                return rolls
            for roll in range(1, 7):
                nxt = square + roll
                if nxt > target:
                    break                        # bigger rolls also overshoot
                dest = get_dest(nxt)
                if dest != -1:
                    nxt = dest                   # forced snake/ladder (only once)
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, rolls + 1))
        return -1


if __name__ == "__main__":
    sol = Solution()

    b1 = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 35, -1, -1, 13, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 15, -1, -1, -1, -1],
    ]
    assert sol.snakesAndLadders(b1) == 4
    assert sol.snakesAndLadders([[-1, -1], [-1, 3]]) == 1
    assert sol.snakesAndLadders([[-1]]) == 0                              # 1x1 (n=1 edge)
    assert sol.snakesAndLadders([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) == 1  # sq5 ladder -> 9
    assert sol.snakesAndLadders([[-1, -1, -1, -1],
                                 [-1, -1, -1, -1],
                                 [-1, -1, -1, -1],
                                 [-1, -1, -1, -1]]) == 3                  # 16 squares, no L/S

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Dijkstra (needed only if rolls have *cost*, not just count)

Plain BFS is correct because every roll costs `1`. If a roll of `k` cost `k`
coins (Scenario 5), or different rolls had different costs, you'd switch to
Dijkstra with a min-heap keyed by total cost. For the base problem BFS is right
and simpler.

### The BFS↔DFS answer the interviewer wants

> "Fewest turns in an unweighted state graph → BFS. The state is the board
> square; `neighbors` = the 6 rolls, each resolved through its snake/ladder. The
> only fiddly part is the boustrophedon square→cell formula. DFS would find *a*
> path, not the shortest."

---

## 10. Complexity — derived step by step

**V and E:** node = a board square, `V = n²`; each square has ≤ 6 outgoing moves,
so `E ≤ 6n² = O(n²)`.

**Time:**
- BFS visits each square at most once (`seen`), and does `O(1)` work per roll
  (including the `O(1)` `get_dest`).
- **Total: `O(n²)`.**

**Space:**
- `seen` set + queue: `O(n²)`.
- **Total: `O(n²)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `n = 1` (`board = [[-1]]`) | `square == target == 1` on the first pop → `0` |
| Target reachable in one roll | enqueued with `rolls = 1`, popped, returns `1` |
| Target unreachable (snakes trap you before the end) | `seen` prevents loops → queue empties → `-1` |
| A ladder lands you *on* the target | `nxt = dest` becomes `target`, enqueued, then popped → correct rolls |
| `nxt` would exceed `n²` | `if nxt > target: break` — you simply don't take that roll |
| Squares 1 / `n²` have no snake/ladder (guaranteed) | code doesn't rely on it, but no special-casing needed |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Boustrophedon conversion wrong.** The `#1` bug. `s0 = s - 1`;
      `row_from_bottom = s0 // n`; `r = n - 1 - row_from_bottom`; column flips
      direction when `row_from_bottom` is **odd**. Off-by-one on the `-1` or
      swapping the parity is the usual slip.
- [ ] **Marking `seen` on the pre-snake/ladder square** instead of the resolved
      destination — lets you re-enqueue the destination via a different roll.
- [ ] **Applying the snake/ladder more than once (chaining)** — the base problem
      says at most one per turn.
- [ ] **Checking the goal before applying the snake/ladder** — you must resolve
      `nxt` first.
- [ ] **`continue` vs `break` on overshoot** — both correct; `break` is a tiny
      optimization (bigger rolls overshoot too).
- [ ] **Forgetting to seed `seen` with square 1.**
- [ ] **Using DFS** — returns some number of rolls, not the minimum.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Implicit graph:** node = a game state (board square), edge = one legal move
   (a die roll + forced transition). BFS = fewest moves. You never build an
   `edges` list.
2. **Resolve forced transitions before marking visited** — mark the state you
   actually end up in, not the intermediate one.
3. **"Flatten a non-row-major 2D layout into a 1D state index"** — the
   boustrophedon formula is a small instance of a recurring need (spiral order,
   diagonal order, Z-order).

| Problem | How this transfers |
|---|---|
| Minimum Genetic Mutation / Word Ladder | same BFS, `neighbors` = "change one symbol, keep if valid" |
| Any dice/board puzzle asking "min turns" | BFS over squares; neighbors = the die faces + teleports |
| "Min moves in a sliding puzzle / lock combination" | BFS over configurations; neighbors = legal single moves |
| Open the Lock (LC 752) | BFS over 4-digit strings; neighbors = turn one wheel ±1 |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The die has faces `1..K` (or an arbitrary set of allowed step sizes)."

- **(b) Pattern:** same BFS, different neighbor set.
- **(c) Adapt:** replace `range(1, 7)` with `range(1, K + 1)` or with the explicit
  set of allowed steps. Complexity becomes `O(K · n²)`.
- **(d) Say:** "The die faces are just the branching factor of `neighbors` —
  change the loop, nothing else."

### Scenario 2 — "Snakes and ladders **can chain** — if a ladder's top is another ladder's bottom, you take both."

- **(b) Pattern:** `get_dest` becomes a **follow-the-chain** function, with cycle
  protection.
- **(c) Adapt:** after landing, keep applying `board[...]` while it's `!= -1`,
  tracking visited squares within the chain to break an infinite snake↔ladder
  loop (return the last square, or flag the loop). BFS is otherwise unchanged.
- **(d) Say:** "Chaining moves the loop from BFS into `get_dest` — follow the
  chain, and guard against a cycle so a snake-into-ladder-into-snake doesn't spin
  forever."

### Scenario 3 — "Return the actual sequence of die rolls, not just the count."

- **(b) Pattern:** BFS + parent pointers.
- **(c) Adapt:** store `parent[nxt] = (square, roll)` on enqueue. From `target`,
  walk `parent` back to `1`, collecting the rolls, and reverse. `O(n²)` extra.
- **(d) Say:** "Record which square and which roll led to each state; reconstruct
  from the target."

### Scenario 4 — "The board is `1000 x 1000` (`10^6` squares)."

- **(b) Pattern:** BFS is already `O(n²)` — optimal (you may have to look at
  every square).
- **(c) Adapt:** use a `bytearray(target + 1)` for `seen` instead of a `set`
  (1 byte/square vs ~50 for a Python set entry), and index the queue by integers.
  `O(n²)` time, `O(n²)` space with a tiny constant.
- **(d) Say:** "No better asymptotic — just shrink the `seen` structure to a byte
  array."

### Scenario 5 — "A roll of `k` **costs `k` coins**. Minimize total coins, not rolls."

- **(b) Pattern:** the move graph is now **weighted** — BFS is wrong.
- **(c) Adapt:** Dijkstra with a min-heap keyed by total coins; relaxing a roll
  of `k` adds `k`. `O(n² log n²)`.
- **(d) Say:** "Costs on the moves means Dijkstra, not BFS — same state graph,
  weighted."

### Scenario 6 — "Taking a snake/ladder is **optional** — you may decline it."

- **(b) Pattern:** each roll now yields up to **two** neighbors.
- **(c) Adapt:** for each roll, generate both `s + roll` (decline) **and**
  `get_dest(s + roll)` if it's a snake/ladder (accept). Enqueue both if unseen.
  Branching doubles at most; BFS complexity stays `O(n²)`.
- **(d) Say:** "Optional forced-moves just add a branch — enqueue both the
  'decline' and the 'accept' square."

---

## 15. Flashcards

**Q:** What's the state and what's a move here?
**A:** State = a board square `1..n²`. Move = one die roll (`+1..+6`, capped at
`n²`), then the forced snake/ladder at that square (once).

**Q:** Why BFS, and what does the answer count?
**A:** Every roll costs `1`, so BFS gives the **minimum number of rolls**. The
answer is the BFS level at which `n²` is first reached.

**Q:** The boustrophedon square→cell formula?
**A:** `s0 = s - 1`; `rfb = s0 // n`; `r = n - 1 - rfb`; `c = s0 % n` if `rfb`
even, else `n - 1 - (s0 % n)`.

**Q:** The #1 bug in this problem?
**A:** The square→cell conversion (off-by-one, or the column parity flip). Second
most common: marking `seen` before resolving the snake/ladder.

**Q:** Time and space?
**A:** `O(n²)` both — BFS visits each of the `n²` squares once.

**Q:** Rolls have different costs — what changes?
**A:** The move graph is weighted → Dijkstra instead of BFS.

**Q:** Snakes/ladders can chain — where does the complexity go?
**A:** Into `get_dest` — follow the chain with cycle protection; BFS is
unchanged.

**Q:** How would you get the roll sequence?
**A:** Parent pointers: `parent[nxt] = (square, roll)`; walk back from `n²`.
