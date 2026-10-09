# 253. Meeting Rooms II

**LC 253** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Sweep line over separated start/end events

---

## 1. Intuition

The number of rooms needed at any moment equals how many meetings are happening *at the same time*. Instead
of tracking whole `[start, end]` intervals, split every meeting into two separate events — "a room is
needed" (a start) and "a room frees up" (an end) — sort each list independently, and sweep through time
comparing the next start against the next end. The peak number of rooms in use at once is the answer.

* `start` and `end` are sorted separately — the original pairing between a specific start and its own end no longer matters, only the *order* events happen in.
* `if start[s] < end[e]` — the next start happens strictly before the next end, so a new room is needed before any existing one frees up: `count += 1`.
* `else` — the next end happens at or before the next start, so a room frees up first: `count -= 1`. This also covers back-to-back meetings (`start[s] == end[e]`), which correctly free the room before reusing it.
* `res = max(res, count)` tracks the highest `count` ever reached — the peak concurrent meetings, which is the minimum rooms required.

**Recall:** split into sorted `start` and `end` arrays; sweep with two pointers, `count += 1` on a start-before-end, `count -= 1` otherwise; track the max `count`.

---

## 2. Approach

* **Idea:** the identity of *which* meeting starts or ends doesn't matter for counting concurrency — only the timeline of start/end events does, so separating and independently sorting the two arrays is valid.
* **Data structure / pointers:** `start`/`end` (sorted event times), `s`/`e` (pointers into each), `count` (rooms currently in use), `res` (peak `count` seen).
* **Invariant:** at every step, `count` equals the number of meetings that have started (among the first `s` starts processed) but not yet ended (among the first `e` ends processed) — exactly the number of rooms in use at that point in the sweep.
* **Edge cases:**
  * Empty `intervals` → the `while s < len(intervals)` loop never runs, correctly returning `0`.
  * Back-to-back meetings (`[0, 5]` then `[5, 10]`) → at `t = 5`, `start[s] == end[e]`, so the `else` branch runs first (`5 < 5` is `False`), freeing the room before the new meeting claims it — never needs a second room.
  * Single meeting → `count` reaches `1` once and never higher, so `res = 1`.
  * All meetings fully overlapping (same start, or heavily nested) → `count` climbs to `len(intervals)` before any end event is reached.

---

## 3. Code

```python
class Solution:

    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        # 1. Separate and sort start and end times
        start = sorted([i[0] for i in intervals])
        end = sorted([i[1] for i in intervals])

        res, count = 0, 0
        s, e = 0, 0

        # 2. Process events chronologically
        while s < len(intervals):
            if start[s] < end[e]:
                # Meeting starts before current earliest end time -> Need a room
                s += 1
                count += 1
            else:
                # Meeting ends at or before current start time -> Free a room
                e += 1
                count -= 1

            res = max(res, count)

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.minMeetingRooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert solution.minMeetingRooms([[0, 5], [5, 10]]) == 1
    assert solution.minMeetingRooms([]) == 0
    assert solution.minMeetingRooms([[1, 5], [2, 6], [3, 7]]) == 3
    print("All tests passed")
```

### Alternative: min-heap of active end times

Sort by start time, then keep a min-heap of the end times of currently occupied rooms. If the earliest-ending
room is already free by the time the next meeting starts, reuse it instead of allocating a new one.

```python
import heapq


class SolutionHeap:

    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0

        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])

        # Min-heap stores end times of active rooms
        rooms = []
        heapq.heappush(rooms, intervals[0][1])

        for interval in intervals[1:]:
            # If the room with the earliest end time is free, reuse it
            if interval[0] >= rooms[0]:
                heapq.heappop(rooms)

            # Assign new/reused room by pushing current end time
            heapq.heappush(rooms, interval[1])

        return len(rooms)


if __name__ == "__main__":
    solution = SolutionHeap()
    assert solution.minMeetingRooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert solution.minMeetingRooms([[0, 5], [5, 10]]) == 1
    assert solution.minMeetingRooms([]) == 0
    print("All tests passed")
```

---

## 4. Dry Run

`intervals = [[0, 30], [5, 10], [15, 20]]` → `start = [0, 5, 15]`, `end = [10, 20, 30]`

| Step | `s` after | `e` after | `start[s]` used | `end[e]` used | `start[s] < end[e]`? | `count` | `res` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **1** | `1` | `0` | `0` | `10` | True | `1` | `1` |
| **2** | `2` | `0` | `5` | `10` | True | `2` | **`2`** |
| **3** | `2` | `1` | `15` | `10` | False | `1` | `2` |
| **4** | `3` | `1` | `15` | `20` | True | `2` | `2` |

`s == 3 == len(intervals)`, loop ends. **Return:** `2`

---

## 5. Complexity

* **Time:** `O(n log n)` — dominated by sorting `start` and `end`; the two-pointer sweep afterward is `O(n)`.
* **Space:** `O(n)` — for the two extracted, sorted arrays.

**Min-heap alternative:** `O(n log n)` time (sorting plus up to `n` heap operations, each `O(log n)`), `O(n)` space for the heap in the worst case (all meetings overlapping).

---

## 6. Recall (30 seconds)

* **Split into events:** sort starts and ends *separately* — the pairing between a specific meeting's start and end doesn't matter for counting concurrency.
* **Sweep rule:** `start[s] < end[e]` → need a room (`count += 1`); otherwise → free a room (`count -= 1`), which also correctly handles back-to-back meetings.
* **Answer = peak concurrency:** `res` tracks the highest `count` ever reached, which is the minimum rooms required.
