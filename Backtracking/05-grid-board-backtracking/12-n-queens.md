# 51. N-Queens

**LC 51** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Row-by-Row Placement Backtracking

---

## 1. Intuition

Fill the board row by row, top to bottom, with exactly **one queen per row**. That already guarantees no two queens share a row. For each row `r`, try every column `c` and skip any square that a queen above already attacks.

A square can be attacked three ways, so we keep three sets:

* `col` — columns that already have a queen.
* `posDiag` holds `r + c` — every cell on the same `/` diagonal has the same `r + c`. Example: `(0,3)`, `(1,2)`, `(2,1)`, `(3,0)` all give `3`.
* `negDiag` holds `r - c` — every cell on the same `\` diagonal has the same `r - c`. Example: `(0,0)`, `(1,1)`, `(2,2)` all give `0`.
* `r == n` — every row has a queen, so save `["".join(row) for row in board]`. That builds *copies* of the rows, which matters because `board` keeps changing.

**Recall:** row by row; three sets (`col`, `r + c`, `r - c`); undo all three.

---

## 2. Template

* **Choose:** add `c`, `r + c`, `r - c` to the three sets, and set `board[r][c] = "Q"`
* **Explore:** `backtrack(r + 1)`
* **Un-choose:** remove all three from the sets, and set `board[r][c] = "."`
* **Prune / dedup:** `if c in col or (r + c) in posDiag or (r - c) in negDiag: continue` — the square is attacked.

---

## 3. Code

```python
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        col = set()
        posDiag = set()  # Tracks (r + c) anti-diagonals /
        negDiag = set()  # Tracks (r - c) main diagonals \

        res = []
        board = [["."] * n for _ in range(n)]

        def backtrack(r: int):
            # Base Case: Placed queens in all N rows
            if r == n:
                copy = ["".join(row) for row in board]
                res.append(copy)
                return

            for c in range(n):
                # Constraint Check: Column or Diagonals already under attack
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                # Choice: Place Queen and update attack sets
                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = "Q"

                # Recurse: Move to next row
                backtrack(r + 1)

                # Backtrack: Undo choices
                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res

```

---

## 4. Dry Run (`n = 4`)

Each line is a queen placed in that row; the tree only lists squares that are not attacked. Rows 0 and 1 for `c=2` and `c=3` mirror the `c=1` and `c=0` starts.

```text
row 0: c=0                                    row 0: c=1
  └─ row 1: c=2                                 └─ row 1: c=3   (only free square)
  │     └─ row 2: no free square  ✗              └─ row 2: c=0
  └─ row 1: c=3                                        └─ row 3: c=2  ✔ SOLUTION
        └─ row 2: c=1
              └─ row 3: no free square  ✗
```

**Solution found:** queens at `(0,1) (1,3) (2,0) (3,2)` → `[".Q..", "...Q", "Q...", "..Q."]`. Starting at `c=2` gives the mirror image, so `n=4` has 2 solutions.

---

## 5. Complexity

* **Time: O(n!)** — row 0 has `n` choices, row 1 at most `n - 1` (its column is taken), and the diagonals cut it further. Each solution also costs `O(n²)` to copy the board.
* **Space: O(n²)** — the `n × n` board, plus `O(n)` for the three sets and the recursion depth (the output list isn't counted).

---

## 6. Recall (30 seconds)

* One queen per row → only columns and diagonals to check.
* `r + c` identifies the `/` diagonal; `r - c` identifies the `\` diagonal.
* Undo everything you added: the three sets and the board cell.
