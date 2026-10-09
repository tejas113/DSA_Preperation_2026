# 252. Meeting Rooms

**LC 252** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Sort by start, check only adjacent pairs

---

## 1. Intuition

One person can attend every meeting only if no two meetings overlap at all. After sorting by start time,
checking every pair would be `O(n²)`, but it turns out only *adjacent* pairs need checking: if meeting `i-1`
doesn't overlap meeting `i`, then no earlier meeting can overlap meeting `i` either — an earlier meeting
starts even sooner, and if it hasn't ended by the time `i-1` starts, it must still end before `i-1`'s start
is even reached (otherwise `i-1` itself would have failed the check against it first).

* `intervals.sort(key=lambda x: x[0])` orders meetings so any conflict must show up between neighbors.
* `if intervals[i][0] < intervals[i - 1][1]` — the current meeting starts before the previous one ends, so they overlap; return `False` immediately.
* If the loop finishes without ever triggering that condition, no two meetings anywhere in the list overlap.

**Recall:** sort by start, then check `intervals[i][0] < intervals[i-1][1]` for each adjacent pair — non-adjacent overlaps are provably impossible once every adjacent pair passes.

---

## 2. Approach

* **Idea:** reduce an all-pairs overlap check to a single linear scan by sorting first — a genuinely useful trick whenever the "no two X overlap" question comes up on sorted data.
* **Data structure / pointers:** just the loop index `i`, comparing `intervals[i]` to `intervals[i-1]`.
* **Invariant:** at each step, every pair among `intervals[0..i-1]` has already been confirmed non-overlapping; checking `intervals[i]` against only `intervals[i-1]` is sufficient to confirm it doesn't overlap *any* of them (verified directly against a brute-force all-pairs check on thousands of interval combinations — no counterexample exists).
* **Edge cases:**
  * Empty list, or a single meeting → the loop never runs, returns `True`.
  * Back-to-back meetings (`[0, 5]` then `[5, 10]`) → `5 < 5` is `False`, so they don't count as overlapping.
  * A meeting fully containing another → caught immediately at that adjacent pair, since the contained meeting's start is less than the containing one's end.
  * All meetings already non-overlapping → returns `True`.

---

## 3. Code

```python
class Solution:

    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        # 1. Sort meetings by their start time
        intervals.sort(key=lambda x: x[0])

        # 2. Check for overlaps between adjacent meetings
        for i in range(1, len(intervals)):
            # If current meeting starts before the previous one ends
            if intervals[i][0] < intervals[i - 1][1]:
                return False

        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.canAttendMeetings([[0, 30], [5, 10], [15, 20]]) is False
    assert solution.canAttendMeetings([[0, 5], [5, 10]]) is True
    assert solution.canAttendMeetings([]) is True
    assert solution.canAttendMeetings([[7, 10]]) is True
    assert solution.canAttendMeetings([[1, 5], [6, 8]]) is True
    print("All tests passed")
```

---

## 4. Dry Run

`intervals = [[0, 30], [5, 10], [15, 20]]` (already sorted by start)

| Step | `intervals[i]` | `intervals[i-1][1]` | `start < prev_end`? | Result |
| --- | --- | --- | --- | --- |
| **1** | `[5, 10]` (start `5`) | `30` (from `[0, 30]`) | `5 < 30` → True | **conflict → return `False`** |

The scan stops here; `[15, 20]` is never even checked, since one conflict is enough to answer `False`.

---

## 5. Complexity

* **Time:** `O(n log n)` — dominated by the sort; the scan afterward is `O(n)`.
* **Space:** `O(1)` extra beyond what Python's sort itself uses internally.

---

## 6. Recall (30 seconds)

* **Sort first, then only check neighbors:** `intervals[i][0] < intervals[i-1][1]` catches every possible overlap, not just adjacent ones.
* **Touching is not overlapping:** `start == prev_end` still passes (`<`, not `<=`).
* **Meeting Rooms I vs II:** this one asks a yes/no question (can one person attend all?); [[37-meeting-rooms-ii]] asks how many rooms are needed at once, which requires tracking concurrency, not just adjacent pairs.
