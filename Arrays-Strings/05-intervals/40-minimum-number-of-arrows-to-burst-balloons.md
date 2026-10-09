# 452. Minimum Number of Arrows to Burst Balloons

**LC 452** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Greedy, sort by end, keep the earliest-ending

---

## 1. Intuition

This is the exact same greedy shape as Non-overlapping Intervals ([[36-non-overlapping-intervals]]): sort by
end coordinate, and shoot each arrow at the earliest-ending balloon still standing — that arrow's position
automatically bursts every other balloon that starts on or before it, since they're guaranteed to overlap
that point.

* `points.sort(key=lambda x: x[1])` — sort by end coordinate, so the balloon most worth "anchoring" an arrow to comes first.
* `prev_end` is the x-position of the most recently fired arrow.
* `if start > prev_end` — this balloon starts after the last arrow's position, so it can't be burst by it; fire a new arrow at *this* balloon's end (the earliest-ending option among what's left).
* No `else` branch is needed — if `start <= prev_end`, the balloon is already burst by the existing arrow, so nothing changes.

**Recall:** sort by end; fire a new arrow (at the current balloon's end) only when `start > prev_end`.

---

## 2. Approach

* **Idea:** greedily anchor each arrow at the earliest-ending balloon among those not yet burst — that position bursts the maximum possible number of remaining balloons, since anything overlapping it is guaranteed to include this specific point.
* **Data structure / pointers:** `prev_end` (the x-position of the last arrow fired); `arrows` (the running count).
* **Invariant:** every balloon processed so far has been burst by one of the `arrows` fired, and `arrows` is the minimum possible for those balloons — no arrow was ever fired earlier than strictly necessary.
* **Edge cases:**
  * Empty input → `0`, guarded explicitly.
  * Touching balloons (`[1, 2]` then `[2, 3]`) → `2 > 2` is `False`, so one arrow at `x = 2` bursts both.
  * All balloons overlapping (`[1,10], [2,9], [3,8]`) → sorted by end gives `[3,8]` first; one arrow at `x = 8` bursts all three.
  * No balloons overlapping (`[1,2], [3,4], [5,6]`) → every balloon needs its own arrow, `arrows = n`.
  * Single balloon → `arrows = 1`.

---

## 3. Code

```python
class Solution:

    def findMinArrowShots(self, points: list[list[int]]) -> int:
        if not points:
            return 0

        # 1. Sort balloons by end coordinate
        points.sort(key=lambda x: x[1])

        arrows = 1
        prev_end = points[0][1]

        # 2. Greedily shoot arrows at earliest ending coordinates
        for start, end in points[1:]:
            if start > prev_end:
                arrows += 1
                prev_end = end

        return arrows


if __name__ == "__main__":
    solution = Solution()
    assert solution.findMinArrowShots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert solution.findMinArrowShots([[1, 2], [2, 3]]) == 1
    assert solution.findMinArrowShots([[1, 10], [2, 9], [3, 8]]) == 1
    assert solution.findMinArrowShots([[1, 2], [3, 4], [5, 6]]) == 3
    assert solution.findMinArrowShots([]) == 0
    print("All tests passed")
```

---

## 4. Dry Run

`points = [[10, 16], [2, 8], [1, 6], [7, 12]]` → sorted by end: `[[1, 6], [2, 8], [7, 12], [10, 16]]`

| Step | Balloon `[start, end]` | `prev_end` before | `start > prev_end`? | Action | `arrows` after |
| --- | --- | --- | --- | --- | --- |
| **init** | `[1, 6]` | — | — | fire arrow at `x=6` | `1` |
| **1** | `[2, 8]` | `6` | `2 > 6` → False | burst by existing arrow | `1` |
| **2** | `[7, 12]` | `6` | `7 > 6` → True | fire new arrow at `x=12` | **`2`** |
| **3** | `[10, 16]` | `12` | `10 > 12` → False | burst by existing arrow | `2` |

**Return:** `2`

---

## 5. Complexity

* **Time:** `O(n log n)` — dominated by the sort; the scan afterward is `O(n)`.
* **Space:** `O(1)` extra beyond what Python's sort itself uses internally.

---

## 6. Recall (30 seconds)

* **Same shape as Non-overlapping Intervals:** sort by end, greedily keep/anchor on the earliest-ending item.
* **Fire rule:** `start > prev_end` → new arrow needed; otherwise the existing arrow already bursts it.
* **Touching counts as burst:** `start == prev_end` still means one arrow covers both.
