# 36. Valid Sudoku

**LC 36** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Hash sets keyed by row, column, and 3×3 box

---

## 1. Intuition

Validating a Sudoku board doesn't require solving it — just checking that no digit repeats within any row,
column, or 3×3 box. Track "have I seen this digit here before?" independently for all three groupings at
once, using one hash set per row, per column, and per box, and check every cell against all three the moment
it's visited.

* `rows[r]`, `cols[c]`, `boxes[box_idx]` are `defaultdict(set)` — a fresh empty set is created automatically the first time any row/column/box index is touched.
* `box_idx = (r // 3, c // 3)` maps a cell's row and column to which of the 9 sub-boxes it belongs to — integer division collapses every 3 rows/columns into one box index.
* `if val in rows[r] or val in cols[c] or val in boxes[box_idx]` checks all three constraints in one line; a hit in *any* of them means an invalid board.
* The three `.add(val)` calls only run once a cell has passed all three checks, so a set never ends up holding a digit that was actually a duplicate.

**Recall:** one hash set per row, column, and box; check `val` against all three before adding it to all three.

---

## 2. Approach

* **Idea:** because Sudoku's constraints are three independent "no repeats" rules over overlapping groupings of the same 81 cells, tracking each grouping with its own set and checking a cell against all three at once catches a violation in any of them.
* **Data structure / pointers:** `rows`, `cols`, `boxes` — three dicts of sets, keyed by row index, column index, and `(box_row, box_col)` respectively.
* **Invariant:** at the start of processing cell `(r, c)`, `rows[r]`, `cols[c]`, and `boxes[box_idx]` contain exactly the non-empty digits already seen in that row, column, and box among cells processed so far (in reading order).
* **Edge cases:**
  * Board is all `"."` → every cell is skipped, returns `True`.
  * A valid, filled board with no violations → returns `True`, even if the board wouldn't be solvable as an actual puzzle — the problem only asks about the *current* state, not solvability.
  * A duplicate anywhere (same row, same column, or same 3×3 box) → caught the moment the second occurrence is reached, returning `False` immediately without scanning the rest of the board.
  * `box_idx` correctly groups cells even though rows and columns are checked independently — a duplicate that's only a box violation (not a row or column violation) is still caught, since all three checks run together.

---

## 3. Code

```python
from collections import defaultdict


class Solution:

    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        boxes = defaultdict(set)

        for r in range(9):
            for c in range(9):
                val = board[r][c]

                if val == ".":
                    continue

                box_idx = (r // 3, c // 3)

                # Check if digit already exists in row, col, or 3x3 box
                if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                    return False

                rows[r].add(val)
                cols[c].add(val)
                boxes[box_idx].add(val)

        return True


if __name__ == "__main__":
    solution = Solution()

    valid_board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert solution.isValidSudoku([row[:] for row in valid_board]) is True

    invalid_board = [row[:] for row in valid_board]
    invalid_board[0][0] = "8"  # duplicates the '8' already in column 0, row 3
    assert solution.isValidSudoku(invalid_board) is False

    empty_board = [["." for _ in range(9)] for _ in range(9)]
    assert solution.isValidSudoku(empty_board) is True

    print("All tests passed")
```

---

## 4. Dry Run

Minimal example: an otherwise empty board with `board[0][0] = "8"` and `board[0][1] = "8"` (same row, same box).

| Cell `(r, c)` | `val` | `box_idx` | `rows[r]` has it? | `cols[c]` has it? | `boxes[box_idx]` has it? | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `(0, 0)` | `"8"` | `(0, 0)` | No | No | No | insert `"8"` into all three sets |
| `(0, 1)` | `"8"` | `(0, 0)` | **Yes** | No | **Yes** | **duplicate → return `False`** |

---

## 5. Complexity

* **Time:** `O(1)` — the board is a fixed `9 × 9 = 81` cells, so the loop always runs the same bounded number of times regardless of input; each check/insert is `O(1)` average.
* **Space:** `O(1)` — at most `81` entries total spread across all the hash sets, again bounded by the fixed board size.

---

## 6. Recall (30 seconds)

* **Three groupings, one pass:** `rows[r]`, `cols[c]`, `boxes[(r // 3, c // 3)]` — check all three before inserting into any.
* **Box index formula:** `(r // 3, c // 3)` collapses each 3×3 block into a single key.
* **Bitmask alternative:** an integer per row/column/box, where bit `d` marks digit `d` as seen, avoids allocating actual set objects — same `O(1)` bound, slightly less overhead.
