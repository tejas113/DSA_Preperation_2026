# 295. Find Median from Data Stream

**LC 295** · **Source:** LC150 + NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Two heaps (max-heap for the lower half, min-heap for the upper half)

---

## 1. Intuition

The median is the middle of the sorted data. We never need the whole sorted list, only the middle. So split the numbers into two halves: the smaller half and the larger half. The median is then at the edge where the halves meet, and both edges are heap roots.

* `self.small` is the **lower half**, stored as a **max-heap**. `heapq` is a min-heap, so we push `-num`, and the real largest value of the lower half is `-self.small[0]`.
* `self.large` is the **upper half**, a plain min-heap. `self.large[0]` is the smallest value of the upper half.
* Step 1 always pushes the new number into `small`. Step 2 checks `-self.small[0] > self.large[0]`. If the lower half's top is bigger than the upper half's bottom, that top moves across. This keeps every value in `small` at most every value in `large`.
* Step 3 keeps the sizes balanced, so `small` has the same number of items as `large`, or one more.
* `findMedian`: if `small` is bigger, its root is the middle. If they are equal, the median is the average of the two roots.

**Recall:** `small` is a max-heap (negated), `large` is a min-heap; keep `len(small) == len(large)` or one more.

---

## 2. Approach

* **Idea:** Keep the lower half in a max-heap and the upper half in a min-heap. Both tops sit at the middle, so the median is read in O(1).
* **Data structure / pointers:**
  * `self.small`: a **max-heap** of the lower half, stored by pushing negated ints (`-num`). Root is `-self.small[0]`.
  * `self.large`: a **min-heap** of the upper half, plain ints. Root is `self.large[0]`.
  * No tuples, so no tie-breaker is needed. Equal values may land in either heap, which is fine.
* **Invariant:**
  * Order: every value in `small` is `<=` every value in `large`.
  * Size: `len(small) == len(large)` or `len(small) == len(large) + 1`.
  * So `small` always holds the extra middle item when the count is odd.
* **Edge cases:**
  * One number: `small = [-x]`, `large = []`, and the median is `float(x)`.
  * Two numbers: one in each heap, and the median is their average.
  * Duplicates (`1, 1, 1`): they can split across the heaps, and the median is still right.
  * Negatives: negating works for them too (`-(-5) = 5`).
  * `findMedian` is only valid after at least one `addNum`. LeetCode guarantees that.
  * The result is a `float`, even for an odd count (`2.0`).

---

## 3. Code

```python
import heapq


class MedianFinder:

    def __init__(self):
        self.small = []  # max-heap for lower half
        self.large = []  # min-heap for upper half

    def addNum(self, num: int) -> None:
        # Step 1: Push to max-heap
        heapq.heappush(self.small, -num)

        # Step 2: Ensure all elements in small <= all elements in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Step 3: Maintain size invariant (len(small) == len(large) or len(small) == len(large) + 1)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


if __name__ == "__main__":
    median_finder = MedianFinder()
    median_finder.addNum(1)
    median_finder.addNum(2)
    assert median_finder.findMedian() == 1.5
    median_finder.addNum(3)
    assert median_finder.findMedian() == 2.0

    single = MedianFinder()
    single.addNum(-5)
    assert single.findMedian() == -5.0

    duplicates = MedianFinder()
    for value in (1, 1, 1):
        duplicates.addNum(value)
    assert duplicates.findMedian() == 1.0
    print("All tests passed")
```

### Alternative: Follow-ups when the numbers are bounded

These are ideas only, with no code. They are for the two LeetCode follow-up questions.

* **All numbers in `[0, 100]`:** keep a frequency array `count = [0] * 101` and a total `n`.
  * `addNum` increments `count[num]` and `n`, which is O(1).
  * `findMedian` walks the 101 buckets until it reaches the `floor(n/2)`th and `ceil(n/2)`th items. That is at most 101 steps, so O(1). Space is O(1).
* **99% of numbers in `[0, 100]`:** keep the same `count` array, plus two counters, `less_than_0` and `greater_than_100`, for the outliers.
  * Start the walk by treating `less_than_0` as already counted, then find the middle item inside the buckets.
  * The median lies in `[0, 100]` unless more than half the data is outliers on one side. Only then would you need to store the outlier values themselves (for example in heaps).

---

## 4. Dry Run

Operations: `addNum(1)`, `addNum(2)`, `findMedian()`, `addNum(3)`, `findMedian()`. The heap columns show the real values. `small` is stored negated, but it is printed with the signs flipped back.

| Operation | What happens | `small` (max-heap) | `large` (min-heap) | `findMedian()` |
| --- | --- | --- | --- | --- |
| `addNum(1)` | Push `-1` into `small`. Sizes are fine. | `[1]` | `[]` | - |
| `addNum(2)` | Push `-2` into `small`. `large` is empty, so no order check. `len(small) > len(large) + 1`, so move `2` to `large`. | `[1]` | `[2]` | - |
| `findMedian()` | Sizes are equal, so average the roots. | `[1]` | `[2]` | **`1.5`** |
| `addNum(3)` | Push `-3` into `small`. `3 > 2`, so move `3` to `large`. Then `len(large) > len(small)`, so move `2` back to `small`. | `[2, 1]` | `[3]` | - |
| `findMedian()` | `len(small) > len(large)`, so return the root of `small`. | `[2, 1]` | `[3]` | **`2.0`** |

---

## 5. Complexity

* **Time:** `addNum` is O(log n), and `findMedian` is O(1). `addNum` does at most about three pushes or pops on heaps of at most `n` items. `findMedian` only reads the roots.
* **Space:** O(n). Every number added is stored in one of the two heaps.

---

## 6. Recall (30 seconds)

* `small` is a max-heap of the lower half (push `-num`), and `large` is a min-heap of the upper half.
* `addNum`: push into `small`, move `small`'s top to `large` if it is bigger than `large`'s top, then rebalance so `len(small)` is `len(large)` or one more.
* `findMedian`: if `small` is bigger, return `-small[0]`. Otherwise return `(-small[0] + large[0]) / 2`.
