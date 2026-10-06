# 378. Kth Smallest Element in a Sorted Matrix

**LC 378** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Fixed-size max-heap (the `k` smallest items), with binary search on the value as the alternative

---

## 1. Intuition

We want the `k`th smallest number. Keep a "smallest `k`" list. The largest number on that list is the `k`th smallest overall, and it is also the first one to kick out when a smaller number shows up. That is a **max-heap** of size `k`.

* `max_heap` holds the `k` smallest values seen so far.
* `heapq` is a min-heap, so we push `-matrix[r][c]`. The most negative value is the largest number, so it sits at the root.
* `if len(max_heap) > k: heappop` evicts the largest of the `k + 1` values.
* `-max_heap[0]` flips the sign back. That root is the biggest of the `k` smallest, which is the `k`th smallest.
* This ignores the sorted rows and columns. It works, but it is the same as Kth Largest in an Array turned upside down. The binary-search alternative uses the sorting.

**Recall:** max-heap of size `k` on `-value`; the answer is `-max_heap[0]`.

---

## 2. Approach

* **Idea:** Push every cell into a size-`k` max-heap, evicting the largest whenever it is too big. The root is the answer.
* **Data structure / pointers:**
  * `max_heap`: a heap of negated ints, capped at `k`. It is a min-heap on `-value`, which makes it a max-heap on value. No tuples, so no tie-breaker is needed.
  * Binary search alternative: `left` and `right` are the smallest and largest values in the matrix (`matrix[0][0]` and `matrix[n-1][n-1]`). `count_less_equal(mid)` counts how many cells are `<= mid`. It starts at the bottom-left and walks right or up.
* **Invariant:**
  * Heap: after each cell, `max_heap` holds the `k` smallest values seen so far.
  * Binary search: the answer always lies in `[left, right]`. The answer is the smallest value whose `count_less_equal` is at least `k`.
* **Edge cases:**
  * `n == 1` (a single cell): the heap and the binary search both return it.
  * `k == 1`: the smallest value, `matrix[0][0]`.
  * `k == n * n`: the largest value, `matrix[n-1][n-1]`.
  * Duplicates: the heap keeps duplicates, so `[[1, 2], [1, 3]]` with `k = 2` gives `1`. In the binary search the loop stops at a value that is actually in the matrix, because it is the smallest value whose count reaches `k`.
  * Negative values work in both. `(left + right) // 2` floors, so the search always moves forward.

---

## 3. Code

```python
import heapq


class Solution:

    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        n = len(matrix)
        max_heap = []

        for r in range(n):
            for c in range(n):
                heapq.heappush(max_heap, -matrix[r][c])

                if len(max_heap) > k:
                    heapq.heappop(max_heap)

        return -max_heap[0]
```

### Alternative: Binary search on the value range

Uses the row and column sorting. Instead of picking cells, guess a value `mid` and count how many cells are `<= mid`. If fewer than `k`, the answer is bigger than `mid`. Otherwise it is `mid` or smaller.

```python
class SolutionBinarySearch:

    def kthSmallest(self, matrix: list[list[int]], k: int) -> int:
        n = len(matrix)
        left, right = matrix[0][0], matrix[n - 1][n - 1]

        def count_less_equal(mid: int) -> int:
            """Count elements <= mid in O(N) time starting from bottom-left."""
            count = 0
            row, col = n - 1, 0
            while row >= 0 and col < n:
                if matrix[row][col] <= mid:
                    count += row + 1  # All elements above this cell are also <= mid
                    col += 1
                else:
                    row -= 1
            return count

        while left < right:
            mid = (left + right) // 2
            if count_less_equal(mid) < k:
                left = mid + 1
            else:
                right = mid

        return left


# Shared tests: they run against both solutions above.
if __name__ == "__main__":
    for solution in (Solution(), SolutionBinarySearch()):
        assert solution.kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8) == 13
        assert solution.kthSmallest([[-5]], 1) == -5
        assert solution.kthSmallest([[1, 2], [1, 3]], 2) == 1
        assert solution.kthSmallest([[1, 2], [1, 3]], 4) == 3
    print("All tests passed")
```

Another approach (not coded here): a k-way merge with a min-heap. Push `(matrix[r][0], r, 0)` for each row, pop `k` times, and after each pop push the next cell in that row. It takes O((n + k) log n) time and O(n) space.

---

## 4. Dry Run

This traces the **binary search alternative**, on `matrix = [[1,5,9],[10,11,13],[12,13,15]]`, `k = 8`. Start with `left = 1`, `right = 15`.

| Iteration | `[left, right]` | `mid` | Cells `<= mid` | `count` vs `k` | New range |
| --- | --- | --- | --- | --- | --- |
| 1 | `[1, 15]` | `8` | `1, 5` | `2 < 8` | `left = 9` |
| 2 | `[9, 15]` | `12` | `1, 5, 9, 10, 11, 12` | `6 < 8` | `left = 13` |
| 3 | `[13, 15]` | `14` | `1, 5, 9, 10, 11, 12, 13, 13` | `8 >= 8` | `right = 13` |
| 4 | `[13, 13]` | - | - | loop ends | return `13` |

---

## 5. Complexity

* **Time (heap):** O(n² log k). All `n * n` cells are pushed, each push and pop on a heap of at most `k + 1` items.
* **Space (heap):** O(k). The heap never holds more than `k + 1` ints.
* **Time (binary search):** O(n · log(max − min)). Each `count_less_equal` walk is O(n), because `row` only goes up and `col` only goes right. The outer loop halves the value range.
* **Space (binary search):** O(1). Only a few integers are used.

---

## 6. Recall (30 seconds)

* Max-heap of size `k`: push `-value`, pop when `len > k`, answer is `-max_heap[0]`.
* It works on any matrix, but it ignores the sorting. O(n² log k) time and O(k) space.
* Follow-up: binary search on the value, counting cells `<= mid` with a bottom-left staircase walk in O(n). Return `left` at the end.
