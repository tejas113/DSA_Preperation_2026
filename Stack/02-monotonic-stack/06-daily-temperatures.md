# 739. Daily Temperatures

**LC 739** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Monotonic decreasing stack of indices

---

## 1. Intuition

For each day, you want to know how many days until a warmer one. Walk through the days once and keep a stack of days that are still **waiting** for a warmer day. When a warmer day `i` arrives, every cooler waiting day on top of the stack has just found its answer.

* `stack` holds **indices** of days (not temperatures) that have not seen a warmer day yet. Storing the index lets you get the temperature with `temperatures[stack[-1]]` and the gap with `i - prev_i`.
* `while stack and t > temperatures[stack[-1]]` pops every waiting day that today beats.
* `res[prev_i] = i - prev_i` is the number of days that popped day waited.
* `stack.append(i)` always runs, because today is itself waiting for a warmer day.
* `res = [0] * len(temperatures)` is the default. A day never popped has no warmer day ahead, so it keeps `0`.

**Recall:** stack of waiting day indices; a warmer day pops the cooler ones and the answer is `i - prev_i`; unpopped days stay `0`.

## 2. Approach

* **Idea:** One pass. Pop every waiting day that today is warmer than, record the gap, then push today.
* **Data structure / pointers:** `stack` is a plain list of day indices (top is `stack[-1]`). `i` is today's index and `t` is today's temperature. `prev_i` is the popped day. `res[prev_i]` is its answer.
* **Invariant:** the temperatures at the indices in `stack` are non-increasing from bottom to top (the code pops only when `t` is strictly warmer, so equal temperatures stay). Every index on the stack is still waiting for a strictly warmer day.
* **Why decreasing:** before pushing day `i`, everything cooler than it is popped, so what remains below is as warm or warmer.
* **Edge cases:**
  * **Stack empty when day `i` arrives:** `while stack and ...` fails, nothing is popped, and `i` is pushed.
  * **Single day** (`[50]`): pushed, never popped, result `[0]`.
  * **Strictly decreasing** (`[90, 80, 70]`): nothing pops, result `[0, 0, 0]`.
  * **Strictly increasing** (`[30, 40, 50]`): each day pops the one before it, result `[1, 1, 0]`.
  * **Duplicates** (`[70, 70, 70, 75]`): equal days are not popped by each other, so all three wait until `75` arrives, giving `[3, 2, 1, 0]`.

## 3. Code

```python
class Solution:

    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        res = [0] * len(temperatures)
        stack = []  # Stores indices of temperatures

        for i, t in enumerate(temperatures):
            # While current temp `t` is warmer than stack top temp
            while stack and t > temperatures[stack[-1]]:
                prev_i = stack.pop()
                res[prev_i] = i - prev_i
            stack.append(i)

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert solution.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert solution.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    assert solution.dailyTemperatures([90, 80, 70]) == [0, 0, 0]
    assert solution.dailyTemperatures([70, 70, 70, 75]) == [3, 2, 1, 0]
    assert solution.dailyTemperatures([50]) == [0]
    assert solution.dailyTemperatures([]) == []
    print("All tests passed")
```

## 4. Dry Run

Input: `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`

| Step | Day `i` | `t` | What happens | `res` after | `stack` after |
|---|---|---|---|---|---|
| 1 | `0` | `73` | Stack empty, push | `[0, 0, 0, 0, 0, 0, 0, 0]` | `[0]` |
| 2 | `1` | `74` | Pop `0`: `res[0] = 1 - 0 = 1`. Push | `[1, 0, 0, 0, 0, 0, 0, 0]` | `[1]` |
| 3 | `2` | `75` | Pop `1`: `res[1] = 2 - 1 = 1`. Push | `[1, 1, 0, 0, 0, 0, 0, 0]` | `[2]` |
| 4 | `3` | `71` | `71 < 75`, push | `[1, 1, 0, 0, 0, 0, 0, 0]` | `[2, 3]` |
| 5 | `4` | `69` | `69 < 71`, push | `[1, 1, 0, 0, 0, 0, 0, 0]` | `[2, 3, 4]` |
| 6 | `5` | `72` | Pop `4`: `res[4] = 1`. Pop `3`: `res[3] = 2`. `72 < 75`, stop. Push | `[1, 1, 0, 2, 1, 0, 0, 0]` | `[2, 5]` |
| 7 | `6` | `76` | Pop `5`: `res[5] = 1`. Pop `2`: `res[2] = 4`. Push | `[1, 1, 4, 2, 1, 1, 0, 0]` | `[6]` |
| 8 | `7` | `73` | `73 < 76`, push | `[1, 1, 4, 2, 1, 1, 0, 0]` | `[6, 7]` |

Result: `[1, 1, 4, 2, 1, 1, 0, 0]`. Days `6` and `7` stay on the stack, so they keep `0`.

## 5. Complexity

* **Time:** O(n), because each index is pushed once and popped at most once, so the inner `while` does at most n pops over the whole run.
* **Space:** O(n), because `stack` holds every index when the temperatures never rise (like `[90, 80, 70]`), plus the output `res`.

## 6. Recall (30 seconds)

* `stack` holds day indices still waiting for a warmer day; always push `i` after popping.
* `while stack and t > temperatures[stack[-1]]`: pop `prev_i`, and `res[prev_i] = i - prev_i`.
* Days never popped keep the default `0`.
