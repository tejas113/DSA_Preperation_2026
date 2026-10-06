# 130. Surrounded Regions

**LC 130** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Reverse search from the boundary (mark the safe `'O'`s, then flip the rest)

---

## 1. Intuition

Checking "is this region surrounded?" for every region is awkward. The opposite question is easy: an
`'O'` is **safe** only if it connects to the border. So start at the border `'O'`s, mark everything they
reach as safe, and flip every `'O'` that wasn't marked.

* **Start only from the border:** the first double loop calls `dfs(i, j)` only when `(i == 0 or i == rows - 1 or j == 0 or j == columns - 1)` and `board[i][j] == "O"`.
* **`'T'` is the temporary "safe" mark:** `board[r][c] = "T"` both protects the cell and marks it visited. `dfs` stops at anything that isn't `"O"`, so a `'T'` is never entered again.
* **One final pass, three states:** a remaining `"O"` was never reached from the border, so it's surrounded and becomes `"X"`. A `"T"` connects to the border, so it goes back to `"O"`. An `"X"` stays.
* **No extra memory for visited:** the board itself stores visited, safe and captured cells.

**Recall:** DFS from border `'O'`s marking `'T'`. Then remaining `'O'` → `'X'` and `'T'` → `'O'`.

## 2. Approach

* **Idea:** Everything reachable from a border `'O'` survives. Mark it, then capture everything else in one sweep.
* **Graph representation:** implicit **grid** graph, undirected and unweighted. The nodes are the `'O'` cells. Moves go in **4 directions**: down, up, right, left (the order of the `dfs` calls).
* **Data structure / pointers:**
  * `board` holds three states. `"O"` means not reached (yet), `"T"` means reached from the border (safe, and visited), and `"X"` means wall or captured. A cell is marked **when `dfs` enters it**.
  * Out-of-bounds is checked first (`r < 0 or r >= rows or c < 0 or c >= columns`), before `board[r][c]` is read.
* **Invariant:** after phase 1, a cell is `"T"` **exactly when** it's an `'O'` connected to the border through other `'O'`s. So every `"O"` left over is surrounded.
* **Edge cases:**
  * Empty board `[]` or `[[]]`: `if not board or not board[0]` returns at once.
  * No `'O'` on the border: phase 1 does nothing, and phase 2 flips every `'O'` to `'X'`.
  * All `'O'`s: everything is reached from the border, so nothing is captured.
  * 1×1, 2×2, a single row or a single column: every cell is on the border, so nothing can ever be captured.
  * An `'O'` touching the border only diagonally is **not** connected (4 directions only), so it gets captured.
  * **Recursion depth:** `dfs` goes one call deeper per `'O'` it reaches. On boards up to 200 × 200, a long snake of `'O'`s raises `RecursionError` under Python's default limit. `sys.setrecursionlimit(100000)` fixes it on Python 3.12 (tested on a 200 × 200 snake). On older Python versions, a very high limit can crash the interpreter, so an iterative stack or BFS is the safest choice.
  * It changes `board` in place and returns `None`, as LeetCode requires.

## 3. Code

```python
class Solution:

    def solve(self, board: list[list[str]]) -> None:
        """Do not return anything, modify board in-place instead."""
        if not board or not board[0]:
            return

        rows = len(board)
        columns = len(board[0])

        def dfs(r: int, c: int):
            # Base case: Out of bounds or not an 'O' cell
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= columns
                or board[r][c] != "O"
            ):
                return

            # Mark cell as temporary 'T' (border-connected, safe from capture)
            board[r][c] = "T"

            # Traverse 4-directional neighbors
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # 1. Run DFS starting from all border 'O's
        for i in range(rows):
            for j in range(columns):
                # Check if cell is on the border and contains 'O'
                if (
                    i == 0 or i == rows - 1 or j == 0 or j == columns - 1
                ) and board[i][j] == "O":
                    dfs(i, j)

        # 2. Final Pass: Flip remaining 'O's to 'X' and restore 'T's to 'O'
        for i in range(rows):
            for j in range(columns):
                if board[i][j] == "O":
                    board[i][j] = "X"  # Surrounded region captured
                elif board[i][j] == "T":
                    board[i][j] = "O"  # Uncaptured region restored
```

## 4. Dry Run

Input (LC Example 1):

```text
     c0   c1   c2   c3
r0:  X    X    X    X
r1:  X    O    O    X
r2:  X    X    O    X
r3:  X    O    X    X
```

| Phase | Cell | Value before | Action | Why |
| --- | --- | --- | --- | --- |
| 1 (border scan) | `(3,1)` | `O` | `dfs(3,1)` sets it to `T` | It's the only border `'O'`. Its neighbours: down is out of bounds, and up `(2,1)`, right `(3,2)` and left `(3,0)` are all `X`, so the DFS stops. |
| 1 | the other border cells | `X` | skip | not `'O'` |
| 2 (final pass) | `(1,1)` | `O` | → `X` | never reached from the border, so captured |
| 2 | `(1,2)` | `O` | → `X` | captured |
| 2 | `(2,2)` | `O` | → `X` | captured. It touches `(1,2)` but not the border |
| 2 | `(3,1)` | `T` | → `O` | safe, so restore it |

Final board:

```text
r0:  X    X    X    X
r1:  X    X    X    X
r2:  X    X    X    X
r3:  X    O    X    X
```

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: there are two full sweeps of the board plus the DFS, and each cell is changed to `'T'` at most once. The phase 1 loop looks at every cell (and checks whether it's on the border). The DFS enters each `'O'` once, and repeat calls on a `'T'` or `'X'` return at once. The phase 2 loop looks at every cell once more. A few passes over every cell grow with rows × columns.
* **Space: O(rows × columns)** in the worst case
  Think of it as: there's no visited set, because `'T'` on the board does that job. The only cost is the recursion stack. If the border-connected `'O'`s form one long snake, `dfs` goes one call deeper per cell before it returns.

## 6. Recall (30 seconds)

* Turn the question around: an `'O'` survives **only if it connects to the border**. DFS from every border `'O'`, marking `'T'`.
* Final sweep: `'O'` → `'X'` (captured) and `'T'` → `'O'` (safe). The board holds three states, so there's no visited set.
* O(R·C) time and O(R·C) worst-case recursion. This is the same "start from the edges" idea as Pacific Atlantic.
