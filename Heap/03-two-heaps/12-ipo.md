# 502. IPO

**LC 502** · **Source:** LC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** Greedy with two structures: projects sorted by capital + a max-heap of profits

---

## 1. Intuition

You have `w` money and can do at most `k` projects. Each project has a capital you must already have and a profit you get after finishing it. At every step the best move is greedy: among the projects you can afford right now, do the one with the biggest profit. Your money only grows, so a project you could afford earlier stays affordable.

* `projects = sorted(zip(capital, profits))` lines the projects up by the capital they need, cheapest first.
* The pointer `i` walks through that list. The `while i < n and projects[i][0] <= w` loop moves every newly affordable project into the heap, and each project is moved only once.
* `max_heap` holds the profits of all affordable, unused projects. `heapq` is a min-heap, so we push `-projects[i][1]`. The most negative value is the biggest profit, so it sits at the root.
* `w += -heapq.heappop(max_heap)` takes the best affordable project and adds its profit to `w`. The minus sign flips it back.
* `if not max_heap: break` means nothing is affordable, and more rounds cannot help.

**Recall:** sort by capital; each round, push everything affordable, then take the biggest profit.

---

## 2. Approach

* **Idea:** Do `k` rounds. In each round, make every project you can afford available, then pick the one with the largest profit.
* **Data structure / pointers:**
  * `projects`: `(capital, profit)` pairs sorted by capital. Ties are broken by profit, which does not matter here.
  * `i`: index of the first project not yet pushed into the heap. It only moves forward.
  * `max_heap`: a **max-heap** of profits (negated ints). It holds affordable projects that have not been done. It has no size cap. Root is the biggest profit.
  * No tuples in the heap, so no tie-breaker is needed. Equal profits are interchangeable.
  * `w`: current capital. It never decreases, because profits are at least 0.
* **Invariant:** At the start of each round, after the `while` loop, `max_heap` holds exactly the profits of the projects with `capital <= w` that have not been done yet.
* **Edge cases:**
  * No project is affordable at the start (`w` is too small): `max_heap` stays empty, `break` fires, and the original `w` is returned.
  * `k > n`: after all projects are used the heap is empty, so `break` stops the loop.
  * `k == 1`: one round, which picks the most profitable affordable project.
  * Profits of 0: they add nothing to `w`, but they are valid and the code handles them.
  * Doing a project opens many new ones at once: the `while` loop pushes all of them before the next pop.

---

## 3. Code

```python
import heapq


class Solution:

    def findMaximizedCapital(
        self, k: int, w: int, profits: list[int], capital: list[int]
    ) -> int:
        n = len(profits)

        # Pair (capital, profit) and sort by capital required
        projects = sorted(zip(capital, profits))

        max_heap = []
        i = 0

        for _ in range(k):
            # Push all projects we can currently afford into max_heap
            while i < n and projects[i][0] <= w:
                heapq.heappush(max_heap, -projects[i][1])
                i += 1

            # If no affordable projects are available, we cannot proceed further
            if not max_heap:
                break

            # Greedily pick the project with maximum profit
            w += -heapq.heappop(max_heap)

        return w


if __name__ == "__main__":
    solution = Solution()
    assert solution.findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert solution.findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]) == 6
    assert solution.findMaximizedCapital(2, 0, [1, 2], [1, 1]) == 0
    assert solution.findMaximizedCapital(5, 0, [1, 2, 3], [0, 0, 0]) == 6
    print("All tests passed")
```

---

## 4. Dry Run

`k = 2`, `w = 0`, `profits = [1, 2, 3]`, `capital = [0, 1, 1]`

`projects = [(0, 1), (1, 2), (1, 3)]`. Start with `max_heap = []`, `i = 0`.

| Round | `w` at start | Pushed (`-profit`) | `i` after | `max_heap` | Popped profit | `w` after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `0` | `-1` (capital 0 <= 0) | `1` | `[-1]` | `1` | `1` |
| 2 | `1` | `-2`, `-3` (capital 1 <= 1) | `3` | `[-3, -2]` | `3` | **`4`** |

Return `4`.

---

## 5. Complexity

* **Time:** O(n log n + k log n). Sorting is O(n log n). Each project is pushed at most once, which is O(n log n) in total. There are at most `k` pops, each O(log n).
* **Space:** O(n). `projects` holds all `n` pairs, and `max_heap` holds up to `n` profits.

---

## 6. Recall (30 seconds)

* Sort projects by capital. Keep a pointer `i` and a max-heap of profits (push `-profit`).
* Each of `k` rounds: push every project with `capital <= w`, then `w += -heappop(max_heap)`.
* Break if the heap is empty. Money never goes down, so affordable projects stay affordable.
