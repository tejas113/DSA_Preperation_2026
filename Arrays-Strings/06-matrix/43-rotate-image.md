# 48. Rotate Image

**LC 48** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Transpose, then reverse each row

---

## 1. Intuition

A 90° clockwise rotation is hard to reason about with raw index math, but it splits cleanly into two simple
operations you can each verify independently: flip the matrix across its main diagonal (transpose), then
flip each row left-to-right (reverse). Doing both in sequence produces exactly a 90° clockwise turn.

* `matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]` swaps a cell with its mirror across the diagonal — this is the transpose step, turning row `i` into column `i`.
* `for j in range(i + 1, n)` — only the upper triangle (`j > i`) is swapped; each pair `(i,j)`/`(j,i)` must be touched exactly once, or a swap would immediately undo itself.
* `matrix[i].reverse()` reverses each row after the transpose, which turns "columns read top-to-bottom, left-to-right" into "columns read top-to-bottom, right-to-left" — completing the clockwise rotation.

**Recall:** transpose (`matrix[i][j] <-> matrix[j][i]` for `j > i`), then reverse every row.

---

## 2. Approach

* **Idea:** decompose a rotation that's awkward to do directly into two operations that are each easy to get right on their own.
* **Data structure / pointers:** `i`, `j` walk the upper triangle of the matrix for the transpose; a second pass just calls `.reverse()` per row.
* **Invariant:** after the transpose loop finishes, `matrix[r][c]` holds what was originally at `matrix[c][r]` for every cell — the matrix is now the true transpose of the input, with no cell touched twice.
* **Edge cases:**
  * `1×1` matrix → the transpose loop's `range(i+1, n)` never executes (nothing to swap), and reversing a single-element row leaves it unchanged.
  * Starting `j` at `i` instead of `i + 1` → each off-diagonal pair would be swapped twice, silently undoing the transpose entirely; starting at `i + 1` is what guarantees each pair is only ever touched once.
  * All values equal → no visible change happens, but the operations still run correctly.
  * Non-square input is out of scope — the problem guarantees `n × n`.

---

## 3. Code

```python
class Solution:

    def rotate(self, matrix: list[list[int]]) -> None:
        """Do not return anything, modify matrix in-place instead."""
        n = len(matrix)

        # 1. Transpose the matrix (swap matrix[i][j] with matrix[j][i])
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # 2. Reverse each row
        for i in range(n):
            matrix[i].reverse()


if __name__ == "__main__":
    solution = Solution()

    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    solution.rotate(matrix)
    assert matrix == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    single = [[1]]
    solution.rotate(single)
    assert single == [[1]]

    two_by_two = [[1, 2], [3, 4]]
    solution.rotate(two_by_two)
    assert two_by_two == [[3, 1], [4, 2]]

    print("All tests passed")
```

### Alternative: four-way cyclic swap (also O(1) space)

Rotate four cells at a time (one from each of the matrix's four "sides") using layer and offset pointers,
without a separate transpose pass. Correct, and avoids a full second pass over the matrix, but noticeably
fiddlier to get the boundary indices right than transpose-then-reverse.

---

## 4. Dry Run

`matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`

**Transpose:**

| `i` | `j` | Swap | Matrix after |
| --- | --- | --- | --- |
| `0` | `1` | `matrix[0][1] <-> matrix[1][0]` (`2 <-> 4`) | `[[1,4,3],[2,5,6],[7,8,9]]` |
| `0` | `2` | `matrix[0][2] <-> matrix[2][0]` (`3 <-> 7`) | `[[1,4,7],[2,5,6],[3,8,9]]` |
| `1` | `2` | `matrix[1][2] <-> matrix[2][1]` (`6 <-> 8`) | `[[1,4,7],[2,5,8],[3,6,9]]` |

**Reverse each row:**

| Row `i` | Before | After |
| --- | --- | --- |
| `0` | `[1, 4, 7]` | `[7, 4, 1]` |
| `1` | `[2, 5, 8]` | `[8, 5, 2]` |
| `2` | `[3, 6, 9]` | `[9, 6, 3]` |

**Final matrix:**

```
[7, 4, 1]
[8, 5, 2]
[9, 6, 3]
```

---

## 5. Complexity

* **Time:** `O(n²)` — the transpose visits roughly `n(n-1)/2` pairs, and reversing all `n` rows is `O(n²)` total; both are linear in the number of cells.
* **Space:** `O(1)` — everything happens in place on the input matrix.

---

## 6. Recall (30 seconds)

* **Two clean steps:** transpose, then reverse each row — clockwise 90°.
* **Counter-clockwise 90°** would be reverse rows *first*, then transpose — the order matters.
* **`j = i + 1`, not `j = i`:** starting the inner loop past the diagonal is what prevents double-swapping a pair back to its original position.
