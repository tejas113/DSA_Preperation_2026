# 909. Snakes and Ladders

**LC 909** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** BFS on an implicit graph (board squares are nodes, dice rolls are edges)

---

## 1. Intuition

Each turn you roll a die (1–6) and move forward. If you land on a snake or ladder, you slide to its end.
"Fewest dice rolls to reach the last square" is a **shortest path where every move costs 1**, which is
exactly what BFS gives. Nobody hands you a graph. The squares are the nodes, and the 6 possible rolls
from each square are the edges. The only fiddly part is turning a square number into a board position.

* **The square number is the node:** `queue` holds `(cell, moves)`, starting at `(1, 0)`. The first time `cell == n * n` is popped, `moves` is the answer, because BFS pops squares in order of how many rolls it took to reach them.
* **6 edges per square:** `for i in range(1, 7)` tries `next_cell = cell + i`, and `break`s once it goes past `n * n`.
* **The zig-zag numbering:** `get_row_col` turns a square number into `(row, col)`. Square 1 is at the **bottom-left**, so `row = n - 1 - r`, and every other row runs right-to-left: `col = c if r % 2 == 0 else n - 1 - c`.
* **Take the snake or ladder at most once:** `destination = board[row][col]` if it isn't `-1`. You **stand on** the destination, so that's what goes into `visited` and `queue`. You don't keep following a ladder that starts where another one ends.

**Recall:** BFS from square 1 with `(cell, moves)`. For each roll 1–6, map `next_cell` to `(row, col)` with the zig-zag formula, jump if the board says so, and mark and push the destination. Return `moves` at `n*n`, or `-1`.

## 2. Approach

* **Idea:** Plain BFS on squares `1 … n²`. Every dice roll is an edge of cost 1, so the first time BFS reaches `n²` is the fewest rolls.
* **Graph representation:** **implicit graph**. The nodes are squares `1 … n²`. Each square `x` has up to 6 **directed**, unweighted edges, to `x+1 … x+6`, each one redirected to the end of a snake or ladder if there is one. The 2-D `board` is only used to look up those jumps.
* **Data structure / pointers:**
  * `queue` (`deque`): `(cell, moves)`, where `moves` = the rolls used to stand on `cell`.
  * `visited`: the squares already queued. A square is marked **when pushed**, and only the square you actually **end up on** after a jump counts, never the bottom of a ladder you slid away from.
  * `get_row_col(cell)`: `r = (cell - 1) // n` counts rows **from the bottom**, and `c = (cell - 1) % n` is the position along that row. `row = n - 1 - r` flips it to the board's index (row 0 is the top). On odd `r`, the row runs right-to-left, so `col = n - 1 - c`.
  * Bounds: `next_cell > n * n`, so `break`. There's no 2-D bounds check, because `get_row_col` only ever receives valid squares.
* **Invariant:** squares come out of `queue` in order of `moves`, and each square's first push carries its fewest rolls. A later route to the same square can never be shorter.
* **Edge cases:**
  * The last square is unreachable (for example, every square you can land on is a snake back down): the queue empties, so it returns `-1`.
  * `n = 2`: a 4-square board, which you can usually finish in one roll (`1 + 3 = 4`).
  * A ladder that lands on the start of another ladder: you take **only the first** one. That's correct by the rules, and the code reads the board once per roll.
  * A snake back to an already-visited square: the destination is in `visited`, so it isn't pushed again. That's what stops loops.
  * LC guarantees squares 1 and `n²` have no snake or ladder.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import deque

class Solution:
    def snakesAndLadders(self, board: list[list[int]]) -> int:
        n = len(board)
        
        def get_row_col(cell):
            r = (cell - 1) // n
            c = (cell - 1) % n
            row = n - 1 - r
            col = c if r % 2 == 0 else n - 1 - c
            return row, col

        queue = deque([(1, 0)])  # (cell, moves)
        visited = {1}

        while queue:
            cell, moves = queue.popleft()

            if cell == n * n:
                return moves

            for i in range(1, 7):
                next_cell = cell + i
                if next_cell > n * n:
                    break

                row, col = get_row_col(next_cell)
                
                # Take snake or ladder if present
                destination = board[row][col] if board[row][col] != -1 else next_cell

                if destination not in visited:
                    visited.add(destination)
                    queue.append((destination, moves + 1))

        return -1
```

## 4. Dry Run

Input: a 3 × 3 board with a **ladder 3 → 7** and a **snake 8 → 1**:

```text
board (row 0 = top)         square numbers on the board
[-1,  1, -1]                 7   8   9      ← row 0 goes left → right
[-1, -1, -1]                 6   5   4      ← row 1 goes right → left
[-1, -1,  7]                 1   2   3      ← row 2 (bottom) goes left → right
```

For example, square 3 → `r = 0, c = 2` → `row = 2, col = 2` → `board[2][2] = 7`, a ladder. Square 8 → `r = 2, c = 1` → `row = 0, col = 1` → `board[0][1] = 1`, a snake.

| Pop `(cell, moves)` | Rolls → square → destination | Pushed | `queue` after |
| --- | --- | --- | --- |
| `(1, 0)` | 1→2, **2→3→7 (ladder)**, 3→4, 4→5, 5→6, 6→7 (already visited) | `2, 7, 4, 5, 6` with moves 1 | `(2,1) (7,1) (4,1) (5,1) (6,1)` |
| `(2, 1)` | 3→7, 4, 5, 6, 7 are visited. **8→1 (snake)** is visited | none | `(7,1) (4,1) (5,1) (6,1)` |
| `(7, 1)` | 8→1 is visited. **9** is new | `9` with moves 2 | `(4,1) (5,1) (6,1) (9,2)` |
| `(4,1)`, `(5,1)`, `(6,1)` | every square they reach is already visited | none | `(9,2)` |
| `(9, 2)` | `cell == 9 == n*n` | — | return **2** |

So the answer is 2: roll a 2 (square 3, ladder to 7), then roll a 2 (square 9).

## 5. Complexity

* **Time: O(n²)**, where the board is n × n, so there are n² squares
  Think of it as: each square is pushed and popped at most once, and each pop tries just 6 rolls. Each roll does a fixed amount of work (a little arithmetic in `get_row_col` and one board lookup). So the work is about 6 × n², which grows like n².
* **Space: O(n²)**
  Think of it as: `visited` and `queue` can each hold up to one entry per square.

## 6. Recall (30 seconds)

* Squares are nodes and rolls 1–6 are edges of cost 1, so **BFS** gives the fewest rolls. Start at `(1, 0)` and return `moves` when you pop `n*n`.
* Zig-zag mapping: `r = (cell-1)//n`, `c = (cell-1)%n`, `row = n-1-r`, `col = c if r even else n-1-c`.
* Jump once if `board[row][col] != -1`, then mark and push the **destination**. O(n²) time and space, and `-1` if the last square is unreachable.
