# 57. Insert Interval

**LC 57** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Three-phase linear scan on already-sorted intervals

---

## 1. Intuition

`intervals` is already sorted, so there's no need to re-sort — just walk through it once and classify each
interval into one of three groups relative to `newInterval`: entirely before it, overlapping it, or entirely
after it. The "overlapping" group all gets absorbed into `newInterval` by growing its boundaries as you go.

* Phase 1 (`intervals[i][1] < newInterval[0]`) — this interval ends before `newInterval` even starts, so it can never overlap; copy it straight to `results`.
* Phase 2 (`intervals[i][0] <= newInterval[1]`) — this interval starts at or before `newInterval`'s current end, so it overlaps; absorb it by taking `min` of the starts and `max` of the ends. `newInterval` itself grows as this phase runs, so later comparisons use the *updated* `newInterval[1]`, not the original.
* Phase 3 (whatever's left) — everything after Phase 2 stops must start after `newInterval`'s final end, so it's copied as-is.
* The merged `newInterval` is only appended to `results` once, right after Phase 2 ends — not once per overlapping interval.

**Recall:** three phases in one pass — copy what's strictly before, absorb what overlaps (growing `newInterval` with `min`/`max`), copy what's strictly after.

---

## 2. Approach

* **Idea:** since the input is already sorted, a single index `i` sweeping left to right is enough to find exactly where `newInterval` belongs, without ever needing to look backward.
* **Data structure / pointers:** `i` walks through `intervals`; `newInterval` itself is mutated in place as it absorbs overlaps; `results` collects the answer.
* **Invariant:** at the boundary between Phase 1 and Phase 2, every interval in `results` truly ends before `newInterval` starts; at the boundary between Phase 2 and Phase 3, `newInterval` has absorbed every interval that overlapped it, and everything remaining in `intervals` starts strictly after `newInterval`'s current end.
* **Edge cases:**
  * `intervals = []` → both scanning phases are skipped entirely; `newInterval` is appended directly, giving `[newInterval]`.
  * `newInterval` overlaps nothing → Phase 2 never runs, and `newInterval` is inserted in its correct sorted position by Phases 1 and 3 alone.
  * `newInterval` fully encloses several existing intervals (like `[1, 10]` swallowing `[2, 3]` and `[4, 5]`) → each gets absorbed in Phase 2, and the `min`/`max` correctly keep `newInterval`'s own wider bounds.
  * `newInterval` inserted before everything or after everything → handled naturally by Phase 1 or Phase 3 doing all the work.

---

## 3. Code

```python
class Solution:

    def insert(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:
        results = []
        i = 0
        n = len(intervals)

        # Phase 1: Add all intervals that come strictly BEFORE newInterval
        while i < n and intervals[i][1] < newInterval[0]:
            results.append(intervals[i])
            i += 1

        # Phase 2: Merge all overlapping intervals into newInterval
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1

        # Append the merged newInterval
        results.append(newInterval)

        # Phase 3: Add all remaining intervals that come strictly AFTER newInterval
        while i < n:
            results.append(intervals[i])
            i += 1

        return results


if __name__ == "__main__":
    solution = Solution()
    assert solution.insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2],
        [3, 10],
        [12, 16],
    ]
    assert solution.insert([], [5, 7]) == [[5, 7]]
    assert solution.insert([[2, 3], [4, 5]], [1, 10]) == [[1, 10]]
    assert solution.insert([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]
    print("All tests passed")
```

### Alternative: append + re-sort — O(n log n)

Correct, and simpler to write, but doesn't take advantage of `intervals` already being sorted — it re-sorts
from scratch every time.

```python
class SolutionAppendAndSort:

    def insert(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:
        intervals.append(newInterval)
        intervals.sort(key=lambda i: i[0])

        results = [intervals[0]]

        for start, end in intervals[1:]:
            last_end = results[-1][1]

            if start <= last_end:
                results[-1][1] = max(last_end, end)
            else:
                results.append([start, end])

        return results


if __name__ == "__main__":
    solution = SolutionAppendAndSort()
    assert solution.insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2],
        [3, 10],
        [12, 16],
    ]
    assert solution.insert([], [5, 7]) == [[5, 7]]
    print("All tests passed")
```

---

## 4. Dry Run

`intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]`, `newInterval = [4, 8]`

| Phase | `i` | Interval | Condition | Action | `newInterval` after | `results` after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `0` | `[1, 2]` | `2 < 4` → True | append | `[4, 8]` | `[[1, 2]]` |
| 1 | `1` | `[3, 5]` | `5 < 4` → False | phase 1 ends | `[4, 8]` | `[[1, 2]]` |
| 2 | `1` | `[3, 5]` | `3 <= 8` → True | absorb: `[min(4,3), max(8,5)]` | `[3, 8]` | `[[1, 2]]` |
| 2 | `2` | `[6, 7]` | `6 <= 8` → True | absorb: `[3, 8]` (no change) | `[3, 8]` | `[[1, 2]]` |
| 2 | `3` | `[8, 10]` | `8 <= 8` → True | absorb: `[min(3,8), max(8,10)]` | `[3, 10]` | `[[1, 2]]` |
| 2 | `4` | `[12, 16]` | `12 <= 10` → False | phase 2 ends | `[3, 10]` | `[[1, 2]]` |
| — | — | — | append merged `newInterval` | — | `[3, 10]` | `[[1, 2], [3, 10]]` |
| 3 | `4` | `[12, 16]` | remaining | append | `[3, 10]` | `[[1, 2], [3, 10], [12, 16]]` |

**Return:** `[[1, 2], [3, 10], [12, 16]]`

---

## 5. Complexity

* **Time:** `O(n)` — a single pass, each interval visited exactly once across the three phases.
* **Space:** `O(n)` — for the `results` output list.

**Alternative:** `O(n log n)` — dominated by the re-sort after appending `newInterval`.

---

## 6. Recall (30 seconds)

* **Three phases, one pass:** strictly-before → absorb-overlapping → strictly-after.
* **Absorb, don't overwrite:** `newInterval[0] = min(...)`, `newInterval[1] = max(...)` — it keeps growing across multiple overlaps in Phase 2.
* **Append once:** the merged `newInterval` is added to `results` a single time, right after Phase 2 finishes — not per overlapping interval.
