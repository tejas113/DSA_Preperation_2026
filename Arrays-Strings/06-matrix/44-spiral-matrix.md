# 54. Spiral Matrix

**LC 54** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Peel layers with four shrinking boundaries

---

## 1. Intuition

A spiral traversal peels the matrix like an onion, one ring at a time: go right across the top, down the
right side, left across the bottom, up the left side, then shrink inward and repeat. Four boundary variables
(`top`, `bottom`, `left`, `right`) track what's left to peel, each shrinking by one after its side is walked.

* `top, bottom, left, right` define the current unvisited rectangle; the loop continues only while that rectangle is non-empty (`top <= bottom and left <= right`).
* Right and Down always run once per layer — they're what shrink `top` and `right` in the first place.
* Left and Up are guarded (`if top <= bottom`, `if left <= right`) because after Right and Down already shrank the rectangle, it might have collapsed to a single row or column — walking Left or Up on a rectangle that no longer exists would revisit cells already added.

**Recall:** four boundaries shrinking inward; Right and Down always run, Left and Up are guarded by re-checking `top <= bottom` / `left <= right` after the first two shrink the rectangle.

---

## 2. Approach

* **Idea:** simulate peeling the outer ring of whatever rectangle remains, then shrink that rectangle and repeat, until nothing is left.
* **Data structure / pointers:** `top`/`bottom`/`left`/`right` mark the current unvisited rectangle's edges; `res` accumulates the answer in visiting order.
* **Invariant:** at the top of each `while` iteration, every cell outside `[top, bottom] × [left, right]` has already been added to `res` exactly once, and every cell inside it has not been added yet.
* **Edge cases:**
  * Single row (`[[1,2,3,4]]`) → after Right, `top` becomes `1`, but `bottom` is still `0`, so `top <= bottom` fails and Left is skipped — no reverse duplicate of the row.
  * Single column (`[[1],[2],[3],[4]]`) → after Down, `right` becomes `-1`, so `left <= right` fails and Up is skipped.
  * `1×1` matrix → Right adds the single cell and shrinks `top` past `bottom`; Down, Left, and Up all get skipped.
  * Empty matrix → `if not matrix: return []` guards this before the loop even starts.
  * Non-square (rectangular) matrices → handled the same way, since `top`/`bottom` and `left`/`right` are independent of each other.

---

## 3. Code

```python
class Solution:

    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        if not matrix:
            return []

        res = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # 1. Traverse Right
            for col in range(left, right + 1):
                res.append(matrix[top][col])
            top += 1

            # 2. Traverse Down
            for row in range(top, bottom + 1):
                res.append(matrix[row][right])
            right -= 1

            # 3. Traverse Left (Guard check against single remaining row)
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    res.append(matrix[bottom][col])
                bottom -= 1

            # 4. Traverse Up (Guard check against single remaining column)
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    res.append(matrix[row][left])
                left += 1

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert solution.spiralOrder([[1, 2, 3, 4]]) == [1, 2, 3, 4]
    assert solution.spiralOrder([[1], [2], [3], [4]]) == [1, 2, 3, 4]
    assert solution.spiralOrder([[1]]) == [1]
    assert solution.spiralOrder([]) == []
    print("All tests passed")
```

---

## 4. Dry Run

`matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`

| Step | `top` after | `bottom` after | `left` after | `right` after | Direction | Cells added | `res` after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **1.1** | `1` | `2` | `0` | `2` | Right | `[1, 2, 3]` | `[1, 2, 3]` |
| **1.2** | `1` | `2` | `0` | `1` | Down | `[6, 9]` | `[1, 2, 3, 6, 9]` |
| **1.3** | `1` | `1` | `0` | `1` | Left | `[8, 7]` | `[1, 2, 3, 6, 9, 8, 7]` |
| **1.4** | `1` | `1` | `1` | `1` | Up | `[4]` | `[1, 2, 3, 6, 9, 8, 7, 4]` |
| **2.1** | `2` | `1` | `1` | `1` | Right | `[5]` | `[1, 2, 3, 6, 9, 8, 7, 4, 5]` |

After step 2.1, `top (2) <= bottom (1)` is `False`, so the loop ends before Down/Left/Up run again.

**Return:** `[1, 2, 3, 6, 9, 8, 7, 4, 5]`

---

## 5. Complexity

* **Time:** `O(m × n)` — every cell is visited exactly once across all four directions combined.
* **Space:** `O(1)` extra — beyond the required output list, only the four boundary variables are used.

---

## 6. Recall (30 seconds)

* **Four shrinking boundaries:** `top`, `bottom`, `left`, `right`, peeling one ring per outer loop iteration.
* **Right and Down always run; Left and Up are guarded:** re-check `top <= bottom` and `left <= right` before them, since the rectangle may have collapsed to a single row or column.
* **Loop condition:** `top <= bottom and left <= right` — the rectangle still has at least one cell left to visit.
