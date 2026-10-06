# 215. Kth Largest Element in an Array

**LC 215** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Fixed-size min-heap (the `k` largest items), with QuickSelect as the follow-up

---

## 1. Intuition

Picture a leaderboard with only `k` seats. Read the numbers one at a time. When a number is added and there are too many people, the lowest one leaves. When you are done, the person in the last seat is the `k`th largest.

* `min_heap` holds only the `k` largest numbers seen so far.
* `heapq` is a min-heap, which is what we want. The number to throw away is the smallest, and that is the root.
* `if len(min_heap) > k: heappop` evicts the one number that no longer belongs. It may be the number just pushed.
* `min_heap[0]` is the smallest of the `k` largest, which is the `k`th largest overall.

**Recall:** push every number, pop when the size goes above `k`, answer is `min_heap[0]`.

---

## 2. Approach

* **Idea:** Keep a heap of the `k` largest values. The root is the answer. QuickSelect (the alternative) finds the answer in O(n) average without a heap.
* **Data structure / pointers:**
  * `min_heap`: a **min-heap** (plain `heapq`, no negation) of plain ints, capped at `k`. No tuples, so no tie-breaker is needed.
  * QuickSelect: `target_index = len(nums) - k` is where the answer would sit if `nums` were sorted ascending. `left` and `right` bound the slice that still contains it. `pivot` splits that slice into smaller, equal and larger parts.
* **Invariant:**
  * Heap: after each number, `min_heap` holds the `k` largest values seen so far.
  * QuickSelect: `target_index` always lies inside `[left, right]`.
* **Edge cases:**
  * `k == 1`: the heap holds one number, the maximum.
  * `k == len(nums)`: the heap keeps everything, and the root is the minimum.
  * One element: the heap returns it (`k` must be 1).
  * Duplicates (`[3,2,3,1,2,4,5,5,6]`, `k = 4`): the problem wants the `k`th in sorted order, not the `k`th distinct value, so duplicates count separately.
  * Negatives work the same way.
  * QuickSelect reorders `nums` in place.
  * QuickSelect needs a 3-way split so that many equal values stay fast (see the note under the alternative).

---

## 3. Code

```python
import heapq


class Solution:

    def findKthLargest(self, nums: list[int], k: int) -> int:
        min_heap = []

        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return min_heap[0]
```

### Alternative: QuickSelect (O(n) average time)

Often asked as the follow-up: "can you do better than O(n log k)?" Pick a random pivot, split the slice into smaller, equal and larger parts, then keep only the part that contains `target_index`.

**Fix to the original:** the original two-way version recursed once per element when `nums` was full of equal values. For example, `[1] * 2000` with `k = 1` raised `RecursionError`, and the time was O(n²). This version is a loop with a 3-way split. Equal values are all handled in one pass.

```python
import random


class SolutionQuickSelect:

    def findKthLargest(self, nums: list[int], k: int) -> int:
        target_index = len(nums) - k
        left, right = 0, len(nums) - 1

        while True:
            pivot = nums[random.randint(left, right)]

            # 3-way partition: [left, less) < pivot, [less, greater] == pivot, (greater, right] > pivot
            less, i, greater = left, left, right
            while i <= greater:
                if nums[i] < pivot:
                    nums[less], nums[i] = nums[i], nums[less]
                    less += 1
                    i += 1
                elif nums[i] > pivot:
                    nums[i], nums[greater] = nums[greater], nums[i]
                    greater -= 1
                else:
                    i += 1

            if target_index < less:
                right = less - 1
            elif target_index > greater:
                left = greater + 1
            else:
                return pivot


# Shared tests: they run against both solutions above.
if __name__ == "__main__":
    for solution in (Solution(), SolutionQuickSelect()):
        assert solution.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
        assert solution.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
        assert solution.findKthLargest([1], 1) == 1
        assert solution.findKthLargest([7, 7, 7, 7], 3) == 7
        assert solution.findKthLargest([-1, -3, -2], 3) == -3
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [3, 2, 1, 5, 6, 4]`, `k = 2` (heap solution)

| `num` | `min_heap` before pop | Popped | `min_heap` after | `min_heap[0]` |
| --- | --- | --- | --- | --- |
| `3` | `[3]` | - | `[3]` | `3` |
| `2` | `[2, 3]` | - | `[2, 3]` | `2` |
| `1` | `[1, 3, 2]` | `1` | `[2, 3]` | `2` |
| `5` | `[2, 3, 5]` | `2` | `[3, 5]` | `3` |
| `6` | `[3, 5, 6]` | `3` | `[5, 6]` | `5` |
| `4` | `[4, 6, 5]` | `4` | `[5, 6]` | **`5`** |

Return `min_heap[0] = 5`.

---

## 5. Complexity

* **Time:** O(n log k). Each of the `n` numbers does one push and at most one pop on a heap of at most `k + 1` items.
* **Space:** O(k). The heap never holds more than `k + 1` numbers.
* **QuickSelect:** O(n) average time, because each round discards a large part of the slice. The worst case is O(n²), which is very unlikely with a random pivot. Space is O(1) because it is a loop with no recursion, though it reorders `nums` in place.

---

## 6. Recall (30 seconds)

* Min-heap of size `k`: push, pop if `len > k`, return `min_heap[0]`.
* Time O(n log k), space O(k). Better than sorting when `k` is small.
* Follow-up: QuickSelect with `target_index = len(nums) - k`. Use a 3-way split so many duplicates don't make it slow.
