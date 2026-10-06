# 74. Search a 2D Matrix

**LC 74** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Flatten the index — treat a sorted 2D matrix as one sorted 1D array

---

## 1. Intuition

Each row is sorted, and every row's first value is bigger than the previous row's last value — so reading the matrix row by row gives one long sorted sequence. You don't need to build that sequence; you just need to convert a 1D index back into `(row, col)` on the fly.

- `mid` ranges over `0 .. m*n - 1`, exactly like a flat array index.
- `row = mid // n` — how many full rows of length `n` fit before `mid`.
- `col = mid % n` — the leftover position within that row.
- Everything after that (`val == target`, `val < target`, `val > target`) is identical to [#1 Binary Search](01-binary-search.md).

**Recall:** binary search over `0..m*n-1`, but read `matrix[mid // n][mid % n]` instead of `nums[mid]`.

## 2. Approach

* **Idea:** exact-match binary search (Form 1) over a *virtual* flattened array — no extra array is built, indices are translated with `//` and `%`.
* **Data structure / pointers:** `left`/`right` bound the virtual 1D index range `[0, m*n - 1]`; `row`/`col` are derived from `mid`, not stored across iterations.
* **Invariant:** same as ordinary binary search, just over the virtual index — if `target` exists, its virtual index is always inside `[left, right]`.
* **Edge cases:**
  - Empty matrix or empty first row (`matrix = []` or `matrix = [[]]`) → guarded explicitly at the top, returns `False` before touching `left`/`right`.
  - Target smaller than every element → `right` shrinks to `-1`.
  - Target larger than every element → `left` grows to `m*n`.
  - Single row or single column → `mid // n` and `mid % n` still work correctly since one of `m`, `n` is `1`.

## 3. Code

```python
class Solution:

    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n - 1

        while left <= right:
            mid = left + (right - left) // 2

            # Map virtual 1D index 'mid' to 2D matrix coordinates
            row = mid // n
            col = mid % n

            val = matrix[row][col]

            if val == target:
                return True
            elif val < target:
                left = mid + 1
            else:
                right = mid - 1

        return False
```

## 4. Dry Run

`matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]`, `target = 3` (`m=3, n=4`, virtual range `[0, 11]`)

| Iteration | `left` | `right` | `mid` | `row` | `col` | `val` | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 11 | 5 | 1 | 1 | 11 | `11 > 3` → `right = 4` |
| 2 | 0 | 4 | 2 | 0 | 2 | 5 | `5 > 3` → `right = 1` |
| 3 | 0 | 1 | 0 | 0 | 0 | 1 | `1 < 3` → `left = 1` |
| 4 | 1 | 1 | 1 | 0 | 1 | 3 | `3 == 3` → return `True` |

## 5. Complexity

* **Time:** `O(log(m·n))` — binary search over `m*n` virtual elements.
* **Space:** `O(1)` — no matrix copy; `row`/`col` are computed per iteration, not stored.

## 6. Recall (30 seconds)

- A row-sorted-and-stacked matrix is one sorted array in disguise — search it as one.
- Convert `mid` with `row = mid // n`, `col = mid % n`, then binary-search as usual.
- Guard empty matrix / empty row up front, before computing `n` (division by zero otherwise).
