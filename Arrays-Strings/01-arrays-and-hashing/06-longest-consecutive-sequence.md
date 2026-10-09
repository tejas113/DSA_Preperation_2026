# 128. Longest Consecutive Sequence

**LC 128** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Hash set, count only from the start of a run

---

## 1. Intuition

Sorting would give `O(n log n)`. Instead, put every number in a set so "is `x` here?" is one lookup. A run
like `1, 2, 3, 4` should be counted once, from its first number `1`. So for each number, ask: "is the number
just below me in the set?" If yes, I am in the middle of a run and can skip. If no, I am the start, so walk
upward and count.

* `nums_set = set(nums)` gives `O(1)` average lookups and removes duplicates.
* `if (num - 1) not in nums_set` is the "am I the start of a run?" test — nothing sits just below `num`.
* `while num + length in nums_set` walks up `num, num + 1, num + 2, ...` and stops at the first gap.
* `length = length + 1` counts how many numbers the run has.
* `longest = max(longest, length)` keeps the best run so far.

**Recall:** only count from a number whose `num - 1` is missing, then walk up while `num + length` is in the set.

---

## 2. Approach

* **Idea:** find each run's first number and walk upward from it. Numbers that are not run starts are skipped, so no run is counted twice.
* **Data structure / pointers:** `nums_set` holds the unique numbers. `num` is the current candidate start. `length` is how far the run extends from `num`. `longest` is the best run found.
* **Invariant:** `longest` is the length of the longest run among the starts processed so far, and every run is walked at most once — only from its first number.
* **Edge cases:**
  * Empty list → `0` (the loop never runs).
  * One element → `1`.
  * Duplicates such as `[1, 0, 1, 2]` → the set removes them, so the answer is `3`, not `4`.
  * Negatives and `0` → work as normal; there is no sorting or index math.
  * Several runs of the same length → `max` handles it.
  * The input order does not matter, and neither does the order the set is iterated in.

---

## 3. Code

```python
class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:

        nums_set = set(nums)
        longest = 0

        for num in nums_set:
            if (num - 1) not in nums_set:
                length = 0
                while num + length in nums_set:
                    length = length + 1

                longest = max(longest, length)

        return longest


if __name__ == "__main__":
    solution = Solution()
    assert solution.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert solution.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert solution.longestConsecutive([1, 0, 1, 2]) == 3
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [100, 4, 200, 1, 3, 2]`, so `nums_set = {100, 4, 200, 1, 3, 2}`.

A set has no fixed order. The order below is the one Python actually gives for this set; any other order gives the same answer.

| `num` | `(num - 1) not in nums_set`? | Action | Run counted | `longest` after |
| --- | --- | --- | --- | --- |
| `1` | `True` | start; `1, 2, 3, 4` are in the set, `5` is not | `[1, 2, 3, 4]`, `length = 4` | `4` |
| `2` | `False` (`1` is there) | skip | — | `4` |
| `3` | `False` (`2` is there) | skip | — | `4` |
| `100` | `True` | start; `100` is in the set, `101` is not | `[100]`, `length = 1` | `4` |
| `4` | `False` (`3` is there) | skip | — | `4` |
| `200` | `True` | start; `200` is in the set, `201` is not | `[200]`, `length = 1` | `4` |

**Return:** `4`

---

## 5. Complexity

* **Time:** `O(n)` — building the set is `O(n)`; the `while` loop only runs from run starts, and each number is stepped over in at most one run, so all `while` steps together are at most `n` (plus one failing check per start).
* **Space:** `O(n)` — `nums_set` holds up to `n` unique numbers.

---

## 6. Recall (30 seconds)

* **Start test:** `(num - 1) not in nums_set` — count only from the first number of a run.
* **Why it is linear:** the `while` loop is nested, but each number belongs to at most one run walk, so the total work stays `O(n)`.
* **Set first:** `set(nums)` gives `O(1)` lookups and removes duplicates.
