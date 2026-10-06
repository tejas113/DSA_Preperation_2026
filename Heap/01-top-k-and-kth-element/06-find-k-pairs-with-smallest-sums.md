# 373. Find K Pairs with Smallest Sums

**LC 373** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Min-heap of "next candidates" (k-way merge on sorted lists)

---

## 1. Intuition

Both arrays are sorted. Think of each `nums1[i]` as its own sorted list of sums: `nums1[i] + nums2[0]`, `nums1[i] + nums2[1]`, and so on. The smallest pair overall is always the front of one of those lists. So we keep only the front of each list in a heap, take the smallest, and then push that list's next item. We never build all `m * n` pairs.

* `min_heap` is a **min-heap** (plain `heapq`, no negation). Its root is the smallest sum among the current list fronts.
* `for i in range(min(len(nums1), k))` starts one list per `nums1[i]`, each at `j = 0`. Only the first `k` rows are needed, because row `i` cannot beat rows `0..i-1` until they have been used up.
* `heappop` gives the next smallest pair, which goes into `result`.
* `if j + 1 < len(nums2): heappush(... j + 1)` pushes the next item of the list we just took from, and nothing else.
* `while min_heap and len(result) < k` stops when we have `k` pairs or run out of pairs.

**Recall:** heap of `(sum, i, j)`; pop the smallest, then push `(i, j + 1)`.

---

## 2. Approach

* **Idea:** Treat each `nums1[i]` as a sorted list of sums with `nums2`. Merge `k` pairs out of those lists with a min-heap that holds one candidate per list.
* **Data structure / pointers:**
  * `min_heap`: a **min-heap** of `(pair_sum, i, j)` tuples. There is no size cap. It holds at most one entry per row, so at most `min(len(nums1), k)` entries.
  * Tuples compare left to right: `pair_sum` first, then `i`, then `j`. All three are ints, so the comparison never fails. The `i` and `j` only decide which of two equal sums comes out first, and the problem accepts any valid answer.
  * `i` is the index into `nums1`. `j` is the index into `nums2`.
  * Each `(i, j)` is pushed at most once, because only `(i, j + 1)` is ever pushed after popping `(i, j)`. That is why no "seen" set is needed.
* **Invariant:** For every row `i` that has started, the heap holds exactly its smallest pair that has not been taken yet. So the root is always the smallest pair not taken yet. `result` is in increasing order of sum.
* **Edge cases:**
  * `nums1` or `nums2` empty: return `[]`. The guard at the top handles it.
  * `k` larger than `len(nums1) * len(nums2)`: the heap runs out first, and the loop returns all pairs.
  * `k == 1`: only `(0, 0)` is pushed and popped.
  * Duplicates (`[1,1,2]`, `[1,2,3]`, `k = 2`): equal values are separate pairs, so the answer is `[[1,1],[1,1]]`.
  * Negative numbers work the same way.
  * Missing import: the pasted snippet used `heapq` without importing it. I added `import heapq`.

---

## 3. Code

```python
import heapq


class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2:
            return []

        min_heap = []
        result = []

        for i in range(min(len(nums1),k)):
            heapq.heappush(min_heap,(nums1[i] + nums2[0],i,0))

        while min_heap and len(result) < k:
            pair_sum,i,j = heapq.heappop(min_heap)
            result.append([nums1[i],nums2[j]])

            if j + 1 < len(nums2):
                heapq.heappush(min_heap, (nums1[i] + nums2[j+1], i, j+1))

        return result


if __name__ == "__main__":
    solution = Solution()
    assert solution.kSmallestPairs([1, 7, 11], [2, 4, 6], 3) == [[1, 2], [1, 4], [1, 6]]
    assert solution.kSmallestPairs([1, 1, 2], [1, 2, 3], 2) == [[1, 1], [1, 1]]
    assert solution.kSmallestPairs([1, 2], [3], 3) == [[1, 3], [2, 3]]
    assert solution.kSmallestPairs([], [1], 2) == []
    assert solution.kSmallestPairs([1], [], 2) == []
    print("All tests passed")
```

---

## 4. Dry Run

`nums1 = [1, 7, 11]`, `nums2 = [2, 4, 6]`, `k = 3`

Start: push `(1+2, 0, 0)`, `(7+2, 1, 0)`, `(11+2, 2, 0)`, so `min_heap = [(3,0,0), (9,1,0), (13,2,0)]`.

| Step | Popped `(sum, i, j)` | `result` | Pushed | `min_heap` after |
| --- | --- | --- | --- | --- |
| 1 | `(3, 0, 0)` | `[[1,2]]` | `(5, 0, 1)` | `[(5,0,1), (13,2,0), (9,1,0)]` |
| 2 | `(5, 0, 1)` | `[[1,2],[1,4]]` | `(7, 0, 2)` | `[(7,0,2), (13,2,0), (9,1,0)]` |
| 3 | `(7, 0, 2)` | `[[1,2],[1,4],[1,6]]` | none (`j + 1 == 3`) | `[(9,1,0), (13,2,0)]` |

`len(result) == 3 == k`, so the loop stops and returns `[[1,2],[1,4],[1,6]]`.

---

## 5. Complexity

* **Time:** O(k log min(k, m)), where `m = len(nums1)`. The start pushes at most `min(m, k)` items, then each of the at most `k` pops does one pop and at most one push on a heap of at most `min(m, k)` items.
* **Space:** O(min(m, k)) for the heap, plus O(k) for `result`.

---

## 6. Recall (30 seconds)

* Each `nums1[i]` is a sorted list of sums. Start a heap with `(nums1[i] + nums2[0], i, 0)` for the first `min(m, k)` rows.
* Pop the smallest, append `[nums1[i], nums2[j]]`, then push `(i, j + 1)` if it exists.
* Stop at `k` pairs or when the heap is empty. Time O(k log min(k, m)).
