# 621. Task Scheduler

**LC 621** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Max-heap of counts + cooldown queue (with a counting formula as the alternative)

---

## 1. Intuition

A CPU runs one task per time step. The same task type must wait `n` steps before it runs again. The best plan: at every step, run the task type that has the most copies left, because that type is the hardest to fit in later. If every type is cooling down, the CPU idles for that step.

* `max_heap` holds the remaining count of every task type that is ready to run. `heapq` is a min-heap, so the counts are stored negated and the most negative one (the biggest count) sits at the root.
* `cnt = 1 + heapq.heappop(max_heap)` runs one copy. The count is negative, so adding 1 moves it closer to zero, meaning one fewer copy left.
* `if cnt: q.append([cnt, time + n])` puts the task type into the cooldown queue `q` if copies remain. `time + n` is the step at which it comes back to the heap, so it can next run at `time + n + 1`.
* `if q and q[0][1] == time: heappush(max_heap, q.popleft()[0])` moves a task type out of cooldown as soon as its time is reached.
* `while max_heap or q` keeps going while anything is ready or cooling down. A step with an empty `max_heap` but a non-empty `q` is an idle step, and `time` still goes up.

**Recall:** run the biggest count, park it in `q` until `time + n`, move it back when its time comes; `time` is the answer.

---

## 2. Approach

* **Idea:** Simulate the CPU one step at a time. Always run the ready task type with the highest remaining count. Park it in a cooldown queue, and release it back to the heap when the cooldown is over. The final `time` is the answer.
* **Data structure / pointers:**
  * `count`: a `Counter` of task type to how many copies there are.
  * `max_heap`: a **max-heap** of remaining counts (negated ints) for task types that are ready. No tuples, so no tie-breaker is needed. We only need the counts, not the letters.
  * `q`: a `deque` of `[remaining_count, available_time]` pairs, one per cooling task type. Pairs are added in increasing `available_time` order, so the front is always the next one to release. At most one pair is added per step, so checking only `q[0]` once per step is enough.
  * `time`: the current step number.
* **Invariant:** At the start of each step, `max_heap` holds the counts of task types that can run now, `q` holds the types still cooling down, and every type with copies left is in exactly one of them.
* **Edge cases:**
  * `n = 0`: no cooldown. A task enters `q` with `available_time == time`, and is released in the same step. The answer is `len(tasks)`.
  * One task: `time = 1`.
  * All tasks the same (`["A","A","A"]`, `n = 2`): the CPU idles between them, giving `A _ _ A _ _ A`, which is 7.
  * Many distinct task types: nothing ever idles, so the answer is `len(tasks)`.
  * Only 26 task types exist (`A` to `Z`), so the heap and queue are always tiny.

---

## 3. Code

```python
from collections import Counter, deque
import heapq


class Solution:

    def leastInterval(self, tasks: list[str], n: int) -> int:
        count = Counter(tasks)
        max_heap = [-val for val in count.values()]
        heapq.heapify(max_heap)

        time = 0
        q = deque()  # stores pairs of [remaining_count, available_time]

        while max_heap or q:
            time += 1

            if max_heap:
                cnt = 1 + heapq.heappop(max_heap)
                if cnt:
                    q.append([cnt, time + n])

            if q and q[0][1] == time:
                heapq.heappush(max_heap, q.popleft()[0])

        return time
```

### Alternative: Counting formula (O(n) time, no simulation)

The most frequent task type forces the layout: `max_freq - 1` blocks of size `n + 1`, then a last row holding every type that ties for the most copies. If there are more tasks than that layout has slots, there is no idle time and the answer is `len(tasks)`.

```python
class SolutionMath:

    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        max_freq = max(counts.values())
        max_freq_count = sum(1 for f in counts.values() if f == max_freq)

        # Formula: (max_freq - 1) blocks of size (n + 1) + max_freq_count
        ans = (max_freq - 1) * (n + 1) + max_freq_count

        return max(len(tasks), ans)


# Shared tests: they run against both solutions above.
if __name__ == "__main__":
    for solution in (Solution(), SolutionMath()):
        assert solution.leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8
        assert solution.leastInterval(["A", "C", "A", "B", "D", "B"], 1) == 6
        assert solution.leastInterval(["A", "A", "A", "B", "B", "B"], 0) == 6
        assert solution.leastInterval(["A", "A", "A"], 2) == 7
        assert solution.leastInterval(["A"], 5) == 1
    print("All tests passed")
```

---

## 4. Dry Run

`tasks = ["A","A","A","B","B","B"]`, `n = 2`. Start: `max_heap = [-3, -3]`, `q = []`. In `q`, each pair is `[remaining, available_time]`, with `remaining` negative.

| Time | What happens | `max_heap` after | `q` after |
| --- | --- | --- | --- |
| 1 | Run `A` (`-3` becomes `-2`), park it with `available_time = 3` | `[-3]` | `[[-2, 3]]` |
| 2 | Run `B` (`-3` becomes `-2`), park it with `available_time = 4` | `[]` | `[[-2, 3], [-2, 4]]` |
| 3 | Heap empty, so idle. `q[0]` is due (`3 == 3`), so `A` returns | `[-2]` | `[[-2, 4]]` |
| 4 | Run `A` (`-2` becomes `-1`), park it with `available_time = 6`. `q[0]` is due (`4 == 4`), so `B` returns | `[-2]` | `[[-1, 6]]` |
| 5 | Run `B` (`-2` becomes `-1`), park it with `available_time = 7` | `[]` | `[[-1, 6], [-1, 7]]` |
| 6 | Idle. `q[0]` is due (`6 == 6`), so `A` returns | `[-1]` | `[[-1, 7]]` |
| 7 | Run `A` (`-1` becomes `0`, so it is not parked). `q[0]` is due (`7 == 7`), so `B` returns | `[-1]` | `[]` |
| 8 | Run `B` (`-1` becomes `0`) | `[]` | `[]` |

Both the heap and the queue are empty, so the loop ends. Return `8`. The schedule is `A B _ A B _ A B`.

---

## 5. Complexity

* **Time:** O(T), where `T` is the returned time, and `T <= len(tasks) * (n + 1)`. The loop runs once per step, including idle steps. Each step does a constant amount of work, because the heap holds at most 26 counts, so each heap operation is O(log 26), which is O(1).
  * Formula alternative: O(len(tasks)), one pass to count.
* **Space:** O(1). `count`, `max_heap` and `q` each hold at most 26 task types.

---

## 6. Recall (30 seconds)

* Max-heap of negated counts. Each step: pop the biggest, add 1 (one copy done), and if copies remain, put `[cnt, time + n]` in the queue `q`.
* If `q[0][1] == time`, push that count back into the heap. Loop while `max_heap or q`; idle steps count too.
* Shortcut: `max((max_freq - 1) * (n + 1) + max_freq_count, len(tasks))`.
