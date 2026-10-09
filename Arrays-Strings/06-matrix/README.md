# Topic 6 — Matrix / 2D Array

## The pattern

Treat the grid as **row and column index math**, and do the work **in place**. The three tricks you'll see:

```python
rows, cols = len(matrix), len(matrix[0])

# 1. Transpose, then reverse each row  → rotate 90° clockwise
for r in range(rows):
    for c in range(r + 1, cols):
        matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
for row in matrix:
    row.reverse()

# 2. Peel layers with four moving borders → spiral order
top, bottom, left, right = 0, rows - 1, 0, cols - 1     # walk right, down, left, up, then shrink

# 3. Use the first row and first column as markers → set zeroes in O(1) space
```

## How to spot this topic

* The input is a **2D array**, and the task is to **rearrange it, read it in an order, or validate it**.
* Words to look for: **"rotate"**, **"spiral"**, **"in place"**, **"set to zero"**, **"valid sudoku"**, **"transpose"**.
* Quick test: *am I moving values by their row/column positions, not walking from cell to neighbor?* If yes, it's this topic.

**Not this topic if:** you are **walking between neighboring cells** to find a path, a region or a word (→ Graphs BFS/DFS, or Backtracking's grid topic).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 47 | Valid Sudoku | One set per row, column and 3×3 box; the box index is `(r // 3, c // 3)` |
| 48 | Rotate Image | Transpose, then reverse every row |
| 49 | Spiral Matrix | Four borders (`top`, `bottom`, `left`, `right`) that shrink after each side |
| 50 | Set Matrix Zeroes | Use the first row and first column as flags, so no extra space is needed |
| 51 | Game of Life | Encode "old state → new state" in each cell, then decode in a second pass |
| 52 | Diagonal Traverse | Cells on one diagonal share `r + c`; alternate the direction of each diagonal, or bounce off the borders |
