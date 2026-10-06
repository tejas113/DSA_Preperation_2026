# 853. Car Fleet

**LC 853** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Sort by position, then a monotonic stack of arrival times

---

## 1. Intuition

Cars can't pass each other. If a car behind would reach the target **sooner or at the same time** as the car in front, it catches up and has to follow it, so the two become one fleet. A car behind that would arrive **later** can never catch up, so it is its own fleet.

So: look at the cars from the one closest to the target backwards, work out each car's arrival time, and keep only the times that start a new fleet.

* `sorted(pair, reverse=True)` orders cars from closest to the target to farthest, so the car ahead is always processed first.
* `time_to_target = (target - p) / s` is how long this car would take if nothing blocked it.
* `stack` holds the **arrival times** (floats), one per fleet found so far. The top, `stack[-1]`, is the fleet right in front of the car we just pushed.
* `stack[-1] <= stack[-2]` means the new car arrives no later than the fleet ahead, so it merges into it. `stack.pop()` throws away the new car's time, and the fleet ahead keeps its (slower) time.
* If the new time is larger, it stays on the stack as a new fleet.
* `len(stack)` at the end is the number of fleets.

**Recall:** go from the front car back; push each arrival time; if it's `<=` the one before, pop it (it merges); the stack size is the answer.

## 2. Approach

* **Idea:** Sort cars by position, front car first. Compute each arrival time. A car that arrives no later than the fleet ahead merges into it. Count the fleets that remain.
* **Data structure / pointers:** `pair` is a list of `[position, speed]`. `p` and `s` are the current car's position and speed. `stack` is a plain list of fleet arrival times (top is `stack[-1]`).
* **Invariant:** after each car, `stack` is strictly **increasing** from bottom to top: the front fleet has the smallest time, and each fleet behind it has a strictly larger one. Because of that, only the newest push can ever break the order, so a single `pop()` is enough, not a loop.
* **Why increasing:** a fleet behind that is slower than the one ahead is the only kind that stays separate.
* **Edge cases:**
  * **Fewer than two items on the stack:** the `len(stack) >= 2` check skips the comparison, so the first car always starts a fleet.
  * **Single car:** the stack has one time, so the answer is `1`.
  * **All cars merge** (the cars behind are all faster): each new time is `<=` the top fleet's time and is popped, so the answer is `1`.
  * **No merges** (each car behind is slower): nothing pops, so the answer is `n`.
  * **Equal arrival times:** `<=` counts that as a merge, because the car reaches the target exactly as the fleet does.
  * **Float comparison:** `(target - p) / s` is a float. Two equal fractions always produce the exact same float, so the `<=` check is safe.

## 3. Code

```python
class Solution:

    def carFleet(
        self, target: int, position: list[int], speed: list[int]
    ) -> int:

        pair = [[p, s] for p, s in zip(position, speed)]
        stack = []

        # Iterate through cars starting closest to target (descending position)
        for p, s in sorted(pair, reverse=True):
            time_to_target = (target - p) / s
            stack.append(time_to_target)

            # If trailing car catches up to leading car (takes <= time), merge fleets
            if len(stack) >= 2 and stack[-1] <= stack[-2]:
                stack.pop()

        return len(stack)


if __name__ == "__main__":
    solution = Solution()
    assert solution.carFleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
    assert solution.carFleet(10, [3], [3]) == 1
    assert solution.carFleet(100, [0, 2, 4], [4, 2, 1]) == 1
    assert solution.carFleet(10, [6, 8], [3, 2]) == 2
    assert solution.carFleet(10, [0, 4, 2], [2, 1, 3]) == 1
    assert solution.carFleet(10, [8, 6, 4], [3, 2, 1]) == 3
    assert solution.carFleet(10, [8, 6, 4], [1, 2, 3]) == 1
    print("All tests passed")
```

## 4. Dry Run

Input: `target = 12`, `position = [10, 8, 0, 5, 3]`, `speed = [2, 4, 1, 1, 3]`

Sorted by position, closest first: `[(10, 2), (8, 4), (5, 1), (3, 3), (0, 1)]`

| Step | Car `(p, s)` | `time_to_target` | Check `stack[-1] <= stack[-2]` | `stack` after |
|---|---|---|---|---|
| 1 | `(10, 2)` | `1.0` | Only one item, skip | `[1.0]` |
| 2 | `(8, 4)` | `1.0` | `1.0 <= 1.0`, merge, pop | `[1.0]` |
| 3 | `(5, 1)` | `7.0` | `7.0 > 1.0`, keep | `[1.0, 7.0]` |
| 4 | `(3, 3)` | `3.0` | `3.0 <= 7.0`, merge, pop | `[1.0, 7.0]` |
| 5 | `(0, 1)` | `12.0` | `12.0 > 7.0`, keep | `[1.0, 7.0, 12.0]` |

Result: `len(stack)` = `3`

## 5. Complexity

* **Time:** O(n log n), because `sorted(pair, reverse=True)` dominates, and the loop after it is O(n) with at most one push and one pop per car.
* **Space:** O(n), because `pair` holds one entry per car and `stack` can hold one time per car when no fleets merge.

## 6. Recall (30 seconds)

* Sort cars by position, closest to the target first; `time_to_target = (target - p) / s`.
* Push the time; if `stack[-1] <= stack[-2]` the car catches the fleet ahead, so `pop()` it.
* The answer is `len(stack)`, the number of fleets.
