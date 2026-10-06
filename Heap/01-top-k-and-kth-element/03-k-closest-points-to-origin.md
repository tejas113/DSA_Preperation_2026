# 973. K Closest Points to Origin

**LC 973** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Fixed-size max-heap on a computed key (the `k` smallest distances)

---

## 1. Intuition

Keep a "closest `k`" list. The point in it that is furthest from the origin is the one most likely to get kicked out, so we want that point at the top where we can reach it fast. That is a **max-heap** on distance.

* `dist = x * x + y * y` is the squared distance. Skipping the square root keeps the order the same and avoids floats.
* `heapq` is a min-heap, so we push `-dist`. The most negative value is the largest distance, so it sits at the root. This is the "negate for a max-heap" trick.
* `if len(max_heap) > k: heappop` removes the furthest point, so only the `k` closest remain.
* The tuple `(-dist, x, y)` keeps the coordinates with the key, so we can read the points back at the end.
* The last line `[[x, y] for _, x, y in max_heap]` drops the distance and returns the points. The order does not matter.

**Recall:** max-heap of size `k` on `-dist`; pop the furthest when the size goes above `k`.

---

## 2. Approach

* **Idea:** Scan the points once, keeping only the `k` closest in a heap. The furthest of those is always at the root, ready to be evicted.
* **Data structure / pointers:**
  * `max_heap`: a heap of `(-dist, x, y)` tuples, capped at `k`. It is a min-heap on `-dist`, which makes it a max-heap on distance.
  * Tuples compare left to right. If two points have the same `-dist`, Python compares `x` and then `y`. All three fields are ints, so this never raises an error. It only decides which of two equally far points is evicted first, and the problem accepts any valid answer.
* **Invariant:** After each point, `max_heap` holds the `k` closest points seen so far, and its root is the furthest of them.
* **Edge cases:**
  * `k == len(points)`: nothing is ever evicted, so all points are returned.
  * One point: it is returned as is.
  * Ties in distance: any `k` closest set is accepted.
  * Negative coordinates: squaring removes the sign, so `(-2)**2 = 4`.
  * The origin itself (`[0, 0]`) has distance 0, and `-0` is `0`, so this works.

---

## 3. Code

```python
import heapq


class Solution:

    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        max_heap = []

        for x, y in points:
            dist = x * x + y * y

            # Store (-dist, x, y) to convert Python's min-heap into a max-heap
            heapq.heappush(max_heap, (-dist, x, y))

            # Evict the point with the largest distance if capacity exceeds k
            if len(max_heap) > k:
                heapq.heappop(max_heap)

        # Extract (x, y) coordinates from remaining max-heap
        return [[x, y] for _, x, y in max_heap]


if __name__ == "__main__":
    solution = Solution()
    assert sorted(solution.kClosest([[1, 3], [-2, 2]], 1)) == [[-2, 2]]
    assert sorted(solution.kClosest([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]
    assert solution.kClosest([[0, 1]], 1) == [[0, 1]]
    assert sorted(solution.kClosest([[1, 1], [-1, -1], [1, -1]], 3)) == [[-1, -1], [1, -1], [1, 1]]
    print("All tests passed")
```

---

## 4. Dry Run

`points = [[3,3],[5,-1],[-2,4]]`, `k = 2`

| Point | `dist` | Pushed tuple | `max_heap` after push | Popped | `max_heap` after |
| --- | --- | --- | --- | --- | --- |
| `[3, 3]` | `18` | `(-18, 3, 3)` | `[(-18, 3, 3)]` | - | `[(-18, 3, 3)]` |
| `[5, -1]` | `26` | `(-26, 5, -1)` | `[(-26, 5, -1), (-18, 3, 3)]` | - | `[(-26, 5, -1), (-18, 3, 3)]` |
| `[-2, 4]` | `20` | `(-20, -2, 4)` | `[(-26, 5, -1), (-18, 3, 3), (-20, -2, 4)]` | `(-26, 5, -1)` | `[(-20, -2, 4), (-18, 3, 3)]` |

Output: `[[-2, 4], [3, 3]]`. The furthest point `[5, -1]` (distance 26) was evicted.

---

## 5. Complexity

* **Time:** O(n log k). Each of the `n` points does one push and at most one pop on a heap of at most `k + 1` items.
* **Space:** O(k). The heap never holds more than `k + 1` tuples (the returned list is also size `k`).

---

## 6. Recall (30 seconds)

* Max-heap of size `k` on distance: push `(-dist, x, y)`, pop when `len > k`.
* Use the squared distance `x*x + y*y`. No square root is needed, since the order is the same.
* Return `[[x, y] for _, x, y in max_heap]`. The order of the result doesn't matter.
