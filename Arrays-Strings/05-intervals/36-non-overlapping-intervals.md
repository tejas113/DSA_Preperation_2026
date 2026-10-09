# 435. Non-overlapping Intervals

**LC 435** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Greedy, sort by end time, keep the earliest-ending

---

## 1. Intuition

Minimizing removals is the same as maximizing how many intervals you can *keep* without any overlap. The
greedy insight: whenever you have to choose which interval to keep, always favor the one that ends
*earliest* — it leaves the most room for everything that comes after. Sorting by end time up front means
you never have to compare "which one should I have kept" after the fact; the earliest-ending interval is
always considered first.

* `intervals.sort(key=lambda x: x[1])` — sort by end time, not start time, so the interval most worth keeping always comes first.
* `prev_end` tracks the end of the most recently *kept* interval — not the most recently seen one.
* `if start >= prev_end` — this interval starts at or after the last kept one ends, so there's no overlap; keep it and advance `prev_end`.
* `else: removals += 1` — this interval starts before the last kept one ends, so it overlaps. Since we sorted by end time, the current interval can never end *earlier* than the one already kept, so discarding the current one (not the kept one) is always the right choice — `prev_end` doesn't need to change.

**Recall:** sort by end time; keep an interval if `start >= prev_end`, otherwise count it as a removal (and don't touch `prev_end`).

---

## 2. Approach

* **Idea:** greedily keep the interval that ends earliest whenever a conflict arises, since that maximizes room for future intervals — sorting by end time makes this the natural scan order.
* **Data structure / pointers:** `prev_end` (the end time of the most recently kept interval), `removals` (the count of discarded intervals). No extra array is needed — we only ever care about the *last kept* end time.
* **Invariant:** at every point in the scan, `prev_end` is the smallest possible end time achievable by any valid selection of non-overlapping intervals among those processed so far — which is exactly why it's safe to greedily discard the current interval instead of the one already kept.
* **Edge cases:**
  * The problem guarantees `start < end` for every interval (no zero-length/point intervals), which is what makes "touching endpoints don't overlap" (`start >= prev_end`, using `>=` not `>`) an unambiguous rule.
  * Touching intervals (`[1, 2]` then `[2, 3]`) → `2 >= 2` is `True`, so both are kept — touching is not overlapping.
  * All intervals identical (`[1,2], [1,2], [1,2]`) → the first is kept, the other two are removed, giving `removals = 2`.
  * Already non-overlapping → `removals = 0`.
  * Single interval → `removals = 0`, since the loop just keeps it.

---

## 3. Code

```python
class Solution:

    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        # Sort intervals by their END times
        intervals.sort(key=lambda x: x[1])

        removals = 0
        prev_end = float("-inf")

        for start, end in intervals:
            if start >= prev_end:
                # No overlap: keep interval and update prev_end
                prev_end = end
            else:
                # Overlap detected: greedy removal
                removals += 1

        return removals


if __name__ == "__main__":
    solution = Solution()
    assert solution.eraseOverlapIntervals([[1, 3], [2, 3], [3, 4], [1, 2]]) == 1
    assert solution.eraseOverlapIntervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert solution.eraseOverlapIntervals([[1, 2], [2, 3]]) == 0
    assert solution.eraseOverlapIntervals([]) == 0
    print("All tests passed")
```

---

## 4. Dry Run

`intervals = [[1, 3], [2, 3], [3, 4], [1, 2]]` → sorted by end time: `[[1, 2], [1, 3], [2, 3], [3, 4]]`

| Step | `[start, end]` | `prev_end` before | `start >= prev_end`? | Action | `prev_end` after | `removals` |
| --- | --- | --- | --- | --- | --- | --- |
| **init** | — | `-inf` | — | — | `-inf` | `0` |
| **1** | `[1, 2]` | `-inf` | True | keep | `2` | `0` |
| **2** | `[1, 3]` | `2` | `1 >= 2` → False | **discard** | `2` (unchanged) | `1` |
| **3** | `[2, 3]` | `2` | `2 >= 2` → True | keep | `3` | `1` |
| **4** | `[3, 4]` | `3` | `3 >= 3` → True | keep | `4` | `1` |

**Return:** `1`

---

## 5. Complexity

* **Time:** `O(n log n)` — dominated by the sort; the scan afterward is `O(n)`.
* **Space:** `O(1)` extra beyond what Python's sort itself uses internally.

---

## 6. Recall (30 seconds)

* **Sort by end time**, not start time — this is what makes the greedy choice simple and correct.
* **Keep rule:** `start >= prev_end` → keep and advance `prev_end`; otherwise, discard the *current* interval and leave `prev_end` alone.
* **Sorting by start time instead** still works, but then a conflict requires `prev_end = min(prev_end, end)` to greedily keep the earlier-ending option — sorting by end time avoids needing that extra step.
