# 289. Game of Life

**LC 289** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Store extra state inside the matrix, via intermediate codes

---

## 1. Intuition

Every cell's next state depends on the *current* (unmodified) state of its neighbors, but you're only allowed
one pass over one array — so overwriting a cell to its final `0`/`1` too early would corrupt the neighbor
count for cells not yet processed. Set Matrix Zeroes ([[45-set-matrix-zeroes]]) solved this kind of problem
by reusing the first row/column as markers; here, the trick is reusing the *value itself* — encode "what it
was" and "what it's becoming" into one number, so a neighbor check can still recover the *original* state
mid-pass.

* `-1` means "was live (`1`), now dying" and `2` means "was dead (`0`), now being born" — both intermediate codes still let you recover the original state.
* `abs(board[nr][nc]) == 1` checks "was this neighbor originally live?" — this works for `1` (still live) and `-1` (was live, now dying), but correctly excludes `0` (still dead) and `2` (was dead, now being born, so it wasn't live *yet* when this generation's counts are being computed).
* Pass 1 writes the intermediate codes based on Conway's rules, using neighbor counts computed entirely from *original* states (since no cell has reached its final `0`/`1` yet).
* Pass 2 (`if board[r][c] > 0: 1 else: 0`) collapses every intermediate code to its true final value — `-1` and `0` become `0`; `1` and `2` become `1`.

**Recall:** encode transitions as `-1` (dying) and `2` (being born); count live neighbors with `abs(...) == 1`; then collapse everything with `> 0` in a second pass.

---

## 2. Approach

* **Idea:** since only two "new" pieces of information are needed per cell (was it live, and is it changing), encode both into a single number instead of a separate array — the classic trick of reusing the value space itself as scratch storage.
* **Data structure / pointers:** `directions` lists the 8 neighbor offsets; no extra grid is needed, since the board holds its own working state.
* **Invariant:** during Pass 1, `abs(board[r][c]) == 1` for any cell not yet visited this pass always reflects that cell's *original* state, because Pass 1 never writes a `0` or a `1` directly — only `-1` or `2` — so the original liveness is always recoverable via `abs(...)`.
* **Edge cases:**
  * All cells dead → no cell ever has 3 live neighbors (there are none), so the board stays all `0`.
  * All cells live, in a small board → most cells likely die from overcrowding (more than 3 live neighbors), depending on board size.
  * `1×1` board → no neighbors exist at all; a single live cell has `0` live neighbors and dies (under-population).
  * A cell on the edge or corner → the bounds check `0 <= nr < rows and 0 <= nc < cols` naturally excludes out-of-bounds neighbors without special-casing corners or edges.

---

## 3. Code

```python
class Solution:

    def gameOfLife(self, board: list[list[int]]) -> None:
        """Do not return anything, modify board in-place instead."""
        rows, cols = len(board), len(board[0])
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        # Pass 1: Encode state transitions in-place
        for r in range(rows):
            for c in range(cols):
                live_neighbors = 0

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and abs(board[nr][nc]) == 1
                    ):
                        live_neighbors += 1

                # Apply Conway's rules using intermediate values
                if board[r][c] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        board[r][c] = -1  # Live -> Dead
                else:
                    if live_neighbors == 3:
                        board[r][c] = 2  # Dead -> Live

        # Pass 2: Map intermediate values back to binary 0/1
        for r in range(rows):
            for c in range(cols):
                if board[r][c] > 0:
                    board[r][c] = 1
                else:
                    board[r][c] = 0


if __name__ == "__main__":
    solution = Solution()

    board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    solution.gameOfLife(board)
    assert board == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]

    all_dead = [[0, 0], [0, 0]]
    solution.gameOfLife(all_dead)
    assert all_dead == [[0, 0], [0, 0]]

    single_cell = [[1]]
    solution.gameOfLife(single_cell)
    assert single_cell == [[0]]  # dies from under-population (0 neighbors)

    print("All tests passed")
```

---

## 4. Dry Run

`board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]`

**Pass 1 (only the cells that actually change are shown):**

| Cell `(r, c)` | Original | Live neighbors | Rule | New code |
| --- | --- | --- | --- | --- |
| `(0, 1)` | live | `1` | under-population | `-1` |
| `(1, 0)` | dead | `3` | reproduction | `2` |
| `(2, 0)` | live | `1` | under-population | `-1` |
| `(3, 1)` | dead | `3` | reproduction | `2` |

Board after Pass 1:

```
[ 0, -1,  0]
[ 2,  0,  1]
[-1,  1,  1]
[ 0,  2,  0]
```

**Pass 2:** every value `> 0` becomes `1`, everything else becomes `0`.

**Final board:**

```
[0, 0, 0]
[1, 0, 1]
[0, 1, 1]
[0, 1, 0]
```

---

## 5. Complexity

* **Time:** `O(m · n)` — each cell is visited once in Pass 1 (checking up to 8 neighbors, a constant) and once in Pass 2.
* **Space:** `O(1)` — the intermediate codes are stored directly in the input board; no extra grid is allocated.

---

## 6. Recall (30 seconds)

* **Encode, don't overwrite directly:** `-1` (was live, now dead), `2` (was dead, now live) — both let the original state be recovered mid-pass.
* **Original-state check:** `abs(board[nr][nc]) == 1` catches both "still live" (`1`) and "was live, dying" (`-1`).
* **Follow-up: infinite board** → track only live cell coordinates in a hash set, generate candidate cells as the union of every live cell's 8 neighbors, and evaluate rules only for those candidates.
