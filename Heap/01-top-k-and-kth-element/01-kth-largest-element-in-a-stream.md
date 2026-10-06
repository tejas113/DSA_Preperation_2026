# 703. Kth Largest Element in a Stream

**LC 703** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Fixed-size min-heap (the `k` largest items)

---

## 1. Intuition

Think of a leaderboard that only keeps the top `k` scores. The lowest score on that board is the `k`th best overall. A new score either beats it (and bumps it off) or is too low to matter.

* `self.min_heap` holds only the `k` largest values seen so far.
* `self.min_heap[0]` is the smallest of those `k`, so it is the `k`th largest overall. Reading it is O(1).
* `heapq` is a min-heap, which is what we want here: the item we need to throw away is the smallest one, and that is the root.
* `while len(self.min_heap) > self.k: heappop` in `__init__` trims the starting numbers down to the top `k`.
* `if len(self.min_heap) > self.k: heappop` in `add` throws away the one value that just fell out of the top `k`. It may be the new value itself.

**Recall:** min-heap of size `k`; the root is the `k`th largest.

---

## 2. Approach

* **Idea:** Keep only the `k` largest values. After every `add`, the root is the answer.
* **Data structure / pointers:**
  * `self.k`: how many top values to keep.
  * `self.min_heap`: a **min-heap** (plain `heapq`, no negation) of plain ints, capped at `k`. Each pop removes the smallest, which is the one that no longer belongs in the top `k`.
  * No tuples, so no tie-breaker is needed.
* **Invariant:** After `__init__` and after every `add`, `min_heap` holds the `k` largest values seen so far (or all of them if fewer than `k` have been seen), and `min_heap[0]` is the smallest of them.
* **Edge cases:**
  * `nums = []`, `k = 1`: the trim loop is skipped. The first `add(val)` pushes `val`, the size is 1, and it returns `val`.
  * Duplicates (`nums = [7, 7, 7, 7]`, `k = 2`): the heap keeps `[7, 7]`. Duplicates count separately, which is correct for "kth largest".
  * `len(nums) < k`: the heap just grows until it reaches `k`. LeetCode guarantees at least `k` values by the time `add` is called, so the root is always a real `k`th largest.
  * Negative values work the same way.
  * Note: `self.min_heap = nums` does not copy the list. It heapifies and trims the caller's list in place. That is fine for LeetCode, but copy it first if you reuse `nums` afterwards.

---

## 3. Code

```python
import heapq


class KthLargest:

    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)

        # Truncate heap size to k elements
        while len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)

        # Keep only the k largest elements
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)

        # Min element among top k is the k-th largest
        return self.min_heap[0]


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)


if __name__ == "__main__":
    obj = KthLargest(3, [4, 5, 8, 2])
    assert obj.add(3) == 4
    assert obj.add(5) == 5
    assert obj.add(10) == 5
    assert obj.add(9) == 8
    assert obj.add(4) == 8

    assert KthLargest(1, []).add(5) == 5
    assert KthLargest(2, [7, 7, 7, 7]).add(7) == 7
    print("All tests passed")
```

---

## 4. Dry Run

`k = 3`, `nums = [4, 5, 8, 2]`

| Step | Operation | `min_heap` before pop | Popped | `min_heap` after | Return (`min_heap[0]`) |
| --- | --- | --- | --- | --- | --- |
| Init | `KthLargest(3, [4,5,8,2])` | `[2, 4, 8, 5]` (after heapify) | `2` | `[4, 5, 8]` | - |
| 1 | `add(3)` | `[3, 4, 8, 5]` | `3` | `[4, 5, 8]` | **4** |
| 2 | `add(5)` | `[4, 5, 8, 5]` | `4` | `[5, 5, 8]` | **5** |
| 3 | `add(10)` | `[5, 5, 8, 10]` | `5` | `[5, 10, 8]` | **5** |
| 4 | `add(9)` | `[5, 9, 8, 10]` | `5` | `[8, 9, 10]` | **8** |

---

## 5. Complexity

* **Time:** `__init__` is O(n log n), and `add` is O(log k).
  * `__init__`: `heapify` is O(n), then up to `n - k` pops at O(log n) each.
  * `add`: one push and at most one pop on a heap of at most `k + 1` items.
* **Space:** O(k). The heap never holds more than `k` items after `__init__` (plus one briefly inside `add`). In `__init__` it reuses the `nums` list, so there is no extra copy.

---

## 6. Recall (30 seconds)

* Min-heap of size `k`, because the item to evict is the smallest of the top `k`.
* `add` = `heappush`, then `heappop` if `len > k`, then return `min_heap[0]`.
* Trim the starting `nums` to `k` in `__init__` with the same pop loop.
