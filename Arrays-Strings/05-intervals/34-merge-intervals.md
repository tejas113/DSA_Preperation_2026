# 56. Merge Intervals

**LC 56** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Sort by start, compare with the last merged interval

---

## 1. Intuition

Overlapping intervals are only easy to spot once they're next to each other. Sort by start time first, and
every interval that could possibly overlap the one you're building ends up right next to it — so a single
left-to-right scan is enough, comparing each interval only against the *last* one you've already merged.

* `intervals.sort(key=lambda i: i[0])` — after this, any interval that overlaps an earlier one must appear later in the list, never out of order.
* `results = [intervals[0]]` seeds the answer with the first interval.
* `if start <= last_end` — the new interval's start is at or before the current merged interval's end, so they overlap (or touch) and belong together.
* `results[-1][1] = max(last_end, end)` — extend the merged interval's end, but only if the new interval reaches further; a fully-enclosed interval (like `[2, 6]` inside `[1, 10]`) must not shrink the end.
* `else: results.append([start, end])` — no overlap with the last merged interval means a brand-new interval starts here.

**Recall:** sort by start, then merge into `results[-1]` whenever `start <= results[-1][1]`, using `max(...)` to extend the end.

---

## 2. Approach

* **Idea:** after sorting by start, only the most recently merged interval can possibly overlap the next one — anything merged earlier is already known to end before the current interval starts.
* **Data structure / pointers:** `results` (the growing list of merged intervals); no extra pointers needed since each interval is only ever compared against `results[-1]`.
* **Invariant:** at every point in the scan, `results` holds the correct merged intervals for everything processed so far, and none of them overlap each other.
* **Edge cases:**
  * Complete enclosure (`[1, 10]` then `[2, 6]`) → `max(10, 6) = 10` keeps the larger end; without the `max`, a naive `results[-1][1] = end` would wrongly shrink it.
  * Touching boundaries (`[1, 4]` then `[4, 5]`) → `4 <= 4` is `True`, so they merge into `[1, 5]`.
  * A genuine gap (`[5, 10]` then `[11, 13]`) → `11 <= 10` is `False`, so they stay separate; adjacent integers are not the same as touching endpoints.
  * Single interval → returned as-is.
  * Unsorted or reverse-sorted input → handled correctly, since sorting happens first regardless of input order.

---

## 3. Code

```python
class Solution:

    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        # 1. Sort intervals by start time
        intervals.sort(key=lambda i: i[0])

        results = [intervals[0]]

        # 2. Iterate and merge overlapping intervals
        for start, end in intervals[1:]:
            last_end = results[-1][1]

            if start <= last_end:
                # Overlap detected: extend the end boundary if needed
                results[-1][1] = max(last_end, end)
            else:
                # No overlap: add new interval
                results.append([start, end])

        return results


if __name__ == "__main__":
    solution = Solution()
    assert solution.merge([[2, 6], [1, 3], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert solution.merge([[1, 4], [4, 5]]) == [[1, 5]]
    assert solution.merge([[1, 10], [2, 6]]) == [[1, 10]]
    assert solution.merge([[1, 4]]) == [[1, 4]]
    print("All tests passed")
```

---

## 4. Dry Run

`intervals = [[2, 6], [1, 3], [8, 10], [15, 18]]` → sorted: `[[1, 3], [2, 6], [8, 10], [15, 18]]`

| Step | `[start, end]` | `results[-1]` before | `start <= last_end`? | Action | `results` after |
| --- | --- | --- | --- | --- | --- |
| **init** | `[1, 3]` | — | — | seed | `[[1, 3]]` |
| **1** | `[2, 6]` | `[1, 3]` | `2 <= 3` → True | `max(3, 6) = 6` | `[[1, 6]]` |
| **2** | `[8, 10]` | `[1, 6]` | `8 <= 6` → False | append | `[[1, 6], [8, 10]]` |
| **3** | `[15, 18]` | `[8, 10]` | `15 <= 10` → False | append | `[[1, 6], [8, 10], [15, 18]]` |

**Return:** `[[1, 6], [8, 10], [15, 18]]`

---

## 5. Complexity

* **Time:** `O(n log n)` — dominated by the sort; the scan afterward is `O(n)`.
* **Space:** `O(n)` — for the sort itself and for the `results` output list.

---

## 6. Recall (30 seconds)

* **Sort first:** by start time, so overlaps are always adjacent in the list.
* **Merge rule:** `start <= results[-1][1]` → overlap; extend with `max(...)`, never just overwrite the end.
* **Touching counts as overlapping:** `start == last_end` still merges (`<=`, not `<`).
