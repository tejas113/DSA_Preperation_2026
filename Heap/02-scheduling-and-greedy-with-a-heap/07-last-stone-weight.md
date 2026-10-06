# 1046. Last Stone Weight

**LC 1046** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Max-heap simulation (pop the two largest, push back the difference)

---

## 1. Intuition

Each turn we need the two heaviest stones. After smashing them, a leftover stone goes back in the pile. "Give me the biggest, over and over, while the pile changes" is exactly what a max-heap is for.

* `max_heap = [-s for s in stones]` stores every weight negated. `heapq` is a min-heap, so the most negative value is the heaviest stone and sits at the root. This is the "negate for a max-heap" trick.
* `first` and `second` are the two pops. They are negative, and `first <= second`, so `first` is the heaviest stone.
* `if first != second` means the stones were different. `first - second` is then a negative number whose size is the leftover weight, so it is pushed back with the right sign. For example, `-8 - (-7) = -1`, a stone of weight 1.
* If `first == second`, both stones are destroyed and nothing is pushed.
* `while len(max_heap) > 1` stops when at most one stone is left.
* `-max_heap[0] if max_heap else 0` flips the sign back for the last stone, or returns `0` if none is left.

**Recall:** negate for a max-heap; pop two, push `first - second` if they differ; return `-max_heap[0]` or `0`.

---

## 2. Approach

* **Idea:** Repeat: take the two heaviest stones, smash them, put back the leftover if there is one. Stop when at most one stone remains.
* **Data structure / pointers:**
  * `max_heap`: a **max-heap** of negated ints, built with `heapify`. It has no size cap and shrinks as stones are destroyed. Root is the heaviest stone, as `-weight`.
  * `first`, `second`: the two stones popped each turn (negated).
  * No tuples, so no tie-breaker is needed.
* **Invariant:** At the start of each turn, `max_heap` holds the weights of all remaining stones (negated), so the two pops are always the two heaviest.
* **Edge cases:**
  * One stone (`[1]`): the loop never runs, and the answer is `1`.
  * Two equal stones (`[2, 2]`): both are destroyed, the heap is empty, and the answer is `0`.
  * All stones equal in pairs: they cancel out and the answer is `0`.
  * An odd number of equal stones (`[3, 3, 3]`): one pair cancels, one stone of weight 3 is left.
  * Empty input does not occur, because LeetCode guarantees at least one stone.

---

## 3. Code

```python
import heapq


class Solution:

    def lastStoneWeight(self, stones: list[int]) -> int:
        # Negate values to simulate a Max-Heap
        max_heap = [-s for s in stones]
        heapq.heapify(max_heap)

        # Smash stones while at least two remain
        while len(max_heap) > 1:
            first = heapq.heappop(max_heap)  # Heaviest stone (most negative)
            second = heapq.heappop(max_heap)  # Second heaviest stone

            if first != second:
                # first - second maintains the negative sign for max-heap
                heapq.heappush(max_heap, first - second)

        # Return the last stone's weight or 0 if no stones are left
        return -max_heap[0] if max_heap else 0


if __name__ == "__main__":
    solution = Solution()
    assert solution.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
    assert solution.lastStoneWeight([1]) == 1
    assert solution.lastStoneWeight([2, 2]) == 0
    assert solution.lastStoneWeight([3, 3, 3]) == 3
    print("All tests passed")
```

---

## 4. Dry Run

`stones = [2, 7, 4, 1, 8, 1]`. The heap stores negatives.

| Turn | `first` | `second` | `first != second`? | Pushed | `max_heap` after |
| --- | --- | --- | --- | --- | --- |
| Init | - | - | - | - | `[-8, -7, -4, -1, -2, -1]` |
| 1 | `-8` (weight 8) | `-7` (weight 7) | yes | `-1` (weight 1) | `[-4, -2, -1, -1, -1]` |
| 2 | `-4` (weight 4) | `-2` (weight 2) | yes | `-2` (weight 2) | `[-2, -1, -1, -1]` |
| 3 | `-2` (weight 2) | `-1` (weight 1) | yes | `-1` (weight 1) | `[-1, -1, -1]` |
| 4 | `-1` (weight 1) | `-1` (weight 1) | no | none | `[-1]` |

The loop ends because `len(max_heap) == 1`. Return `-(-1) = 1`.

---

## 5. Complexity

* **Time:** O(n log n). `heapify` is O(n). Each turn does 2 pops and at most 1 push, each O(log n), and there are at most `n - 1` turns.
* **Space:** O(n). `max_heap` is a new list of `n` negated weights. The code does not reuse `stones`.

---

## 6. Recall (30 seconds)

* Negate every stone, `heapify`, then loop while `len > 1`.
* Pop `first` and `second`. If they differ, push `first - second` (it stays negative). If they match, push nothing.
* Return `-max_heap[0]` if the heap is not empty, otherwise `0`.
