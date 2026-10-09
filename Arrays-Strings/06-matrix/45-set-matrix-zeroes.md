# 73. Set Matrix Zeroes

**LC 73** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Store extra state inside the matrix itself

---

## 1. Intuition

Setting a whole row and column to zero the moment you find a zero would corrupt the matrix before you've
finished scanning it for *other* zeroes. So first record *which* rows and columns need zeroing, then apply
it in a second pass. Approach 1 records that in two sets; Approach 2 gets the same information for free by
reusing the matrix's own first row and first column as the marker space — no extra `O(m+n)` storage needed.

* In Approach 2, `matrix[i][0] = 0` and `matrix[0][j] = 0` mean "row `i`" and "column `j`" need zeroing — the first row/column double as the marker arrays.
* `matrix[0][0]` can only hold one of those two meanings at once, so the first column's flag is tracked separately in `col_zero`, checked *before* the scan can overwrite `matrix[i][0]`.
* The scan (`for j in range(1, n)`) deliberately skips column `0` — that column is read for `col_zero` separately, so it's never treated as ordinary data during the marking pass.
* Pass 2 only touches inner cells (`i, j` both `>= 1`), so the markers in row `0` and column `0` are never overwritten before they're used.
* Row `0` and column `0` themselves are only zeroed at the very end, using `matrix[0][0]` and `col_zero` — doing this earlier would erase the markers before the inner cells could read them.

**Recall:** mark needed rows/columns in the matrix's own first row/column (with `col_zero` for the ambiguous top-left cell); zero the inner cells from those markers; zero row 0 and column 0 last.

---

## 2. Approach

* **Idea:** any extra bookkeeping space can potentially be squeezed into unused parts of the input itself — here, the first row and column, since they only ever need to become all-zero or stay as-is anyway.
* **Data structure / pointers:** Approach 1 uses `rows`/`cols` sets. Approach 2 reuses `matrix[i][0]`/`matrix[0][j]` as markers, plus one extra boolean `col_zero` for the top-left ambiguity.
* **Invariant:** by the time Pass 2 runs, `matrix[i][0] == 0` means row `i` (for `i >= 1`) must be zeroed, and `matrix[0][j] == 0` means column `j` (for `j >= 1`) must be zeroed — and neither has been touched by anything except the marking pass.
* **Edge cases:**
  * A zero in row `0` or column `0` itself → handled by `matrix[0][0]` (for row `0`) and `col_zero` (for column `0`), applied only in the final two steps, after the inner cells have already been updated from them.
  * A `1×1` matrix → the marking loop's `range(1, n)` never runs; only the final `matrix[0][0] == 0` check matters.
  * No zeroes anywhere → nothing changes.
  * Order matters: updating row `0`/column `0` *before* the inner cells would destroy the markers before they're read — this is the classic bug this approach is designed to avoid.

---

## 3. Code

```python
class Solution:

    def setZeroes(self, matrix: list[list[int]]) -> None:
        """Do not return anything, modify matrix in-place instead."""
        m, n = len(matrix), len(matrix[0])
        col_zero = False  # Flag to track if column 0 needs to be zeroed

        # 1. Mark rows and columns in the first row/col
        for i in range(m):
            if matrix[i][0] == 0:
                col_zero = True
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # 2. Update inner matrix cells based on flags in first row/col
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # 3. Update first row if matrix[0][0] was flagged
        if matrix[0][0] == 0:
            for j in range(n):
                matrix[0][j] = 0

        # 4. Update first column if col_zero flag was set
        if col_zero:
            for i in range(m):
                matrix[i][0] = 0


if __name__ == "__main__":
    solution = Solution()

    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    solution.setZeroes(matrix)
    assert matrix == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

    zero_in_first_col = [[1, 2, 3], [4, 5, 6], [0, 8, 9]]
    solution.setZeroes(zero_in_first_col)
    assert zero_in_first_col == [[0, 2, 3], [0, 5, 6], [0, 0, 0]]

    zero_at_origin = [[0, 2, 3], [4, 5, 6], [7, 8, 9]]
    solution.setZeroes(zero_at_origin)
    assert zero_at_origin == [[0, 0, 0], [0, 5, 6], [0, 8, 9]]

    single_cell = [[0]]
    solution.setZeroes(single_cell)
    assert single_cell == [[0]]

    print("All tests passed")
```

### Alternative: hash sets of affected rows/columns (O(m + n) space)

Simpler to reason about, and a natural first solution — record every row and column that contains a zero in
two sets during one pass, then zero out any cell whose row or column is in either set.

```python
class SolutionSets:

    def setZeroes(self, matrix: list[list[int]]) -> None:
        """Do not return anything, modify matrix in-place instead."""
        m, n = len(matrix), len(matrix[0])
        rows, cols = set(), set()

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    rows.add(i)
                    cols.add(j)

        for i in range(m):
            for j in range(n):
                if i in rows or j in cols:
                    matrix[i][j] = 0


if __name__ == "__main__":
    solution = SolutionSets()
    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    solution.setZeroes(matrix)
    assert matrix == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    print("All tests passed")
```

---

## 4. Dry Run

`matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]`

**Pass 1 (mark):** at `(1, 1)`, `matrix[1][1] == 0` → set `matrix[1][0] = 0` and `matrix[0][1] = 0`. `col_zero` stays `False` (column 0 never held a `0`).

Matrix after Pass 1: `[[1, 0, 1], [0, 0, 1], [1, 1, 1]]`

**Pass 2 (inner cells, `i, j >= 1`):**

| Cell | `matrix[i][0] == 0`? | `matrix[0][j] == 0`? | Result |
| --- | --- | --- | --- |
| `(1, 1)` | Yes | Yes | `0` |
| `(1, 2)` | Yes | No | `0` |
| `(2, 1)` | No | Yes | `0` |
| `(2, 2)` | No | No | stays `1` |

Matrix after Pass 2: `[[1, 0, 1], [0, 0, 0], [1, 0, 1]]`

**Pass 3 & 4:** `matrix[0][0] == 1` (no row-0 zeroing needed); `col_zero == False` (no column-0 zeroing needed).

**Final:** `[[1, 0, 1], [0, 0, 0], [1, 0, 1]]`

---

## 5. Complexity

* **Time:** `O(m · n)` for both approaches — each visits every cell a constant number of times.
* **Space:** `O(1)` for the in-place marker approach — only `col_zero` is extra. `O(m + n)` for the hash-set approach — the two sets can each grow up to `m` and `n` entries.

---

## 6. Recall (30 seconds)

* **Reuse row 0 / column 0 as markers:** `matrix[i][0]` and `matrix[0][j]` record which rows/columns need zeroing, with `col_zero` handling the ambiguous `matrix[0][0]` cell.
* **Order is everything:** update the inner cells *before* touching row 0 or column 0, or the markers get destroyed before they're read.
* **Simpler fallback:** two hash sets (`rows`, `cols`) do the same job in `O(m + n)` space if `O(1)` isn't required.
