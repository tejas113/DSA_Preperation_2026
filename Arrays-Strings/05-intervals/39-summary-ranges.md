# 228. Summary Ranges

**LC 228** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Scan for runs of consecutive numbers

---

## 1. Intuition

Since `nums` is sorted with no duplicates, a run of consecutive integers (`nums[i+1] == nums[i] + 1`) is a
single range worth compressing into one string. Anchor at the start of a run, walk forward while the run
continues, then format whatever was found — a single number if the run was length 1, or `"start->end"` if
it spanned more than one.

* `start = nums[i]` anchors the beginning of the current run, before the inner loop moves `i`.
* `while i + 1 < n and nums[i] + 1 == nums[i + 1]: i += 1` walks `i` forward as long as the *next* number continues the run.
* After the inner loop, `nums[i]` is the *last* number of the run (it stopped because either the array ended or the next number broke the sequence).
* `if start == nums[i]` — a run of length 1 has nothing to show as a range, so it's printed as a single number.
* `i += 1` moves past this whole run to start scanning the next one.

**Recall:** anchor `start`; grow `i` while consecutive; format `str(start)` if `start == nums[i]`, else `f"{start}->{nums[i]}"`; move past the run.

---

## 2. Approach

* **Idea:** each iteration of the outer `while` consumes one entire run of consecutive numbers at once, using an inner `while` to find where that run ends.
* **Data structure / pointers:** `i` does double duty — the outer loop's current position, and the inner loop's scan-ahead pointer; `start` remembers where the current run began.
* **Invariant:** at the point the inner loop stops, `nums[start_index .. i]` is exactly one maximal run of consecutive integers — extending it any further would break the consecutive property (or run off the array).
* **Edge cases:**
  * Empty array → the outer loop never runs, returns `[]`.
  * Single element → the inner loop never runs (nothing to compare), so `start == nums[i]`, giving `["<that number>"]`.
  * No two numbers are consecutive → every run has length 1, and the output is just every number as its own string.
  * The whole array is one consecutive run → a single `"start->end"` string.
  * Negative numbers → handled the same way; `+1` consecutiveness doesn't care about sign.

---

## 3. Code

```python
class Solution:

    def summaryRanges(self, nums: list[int]) -> list[str]:
        res = []
        i = 0
        n = len(nums)

        while i < n:
            start = nums[i]

            # Advance i while numbers remain consecutive
            while i + 1 < n and nums[i] + 1 == nums[i + 1]:
                i += 1

            # Format range based on single vs multi-element span
            if start == nums[i]:
                res.append(str(start))
            else:
                res.append(f"{start}->{nums[i]}")

            i += 1

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.summaryRanges([0, 1, 2, 4, 5, 7]) == ["0->2", "4->5", "7"]
    assert solution.summaryRanges([]) == []
    assert solution.summaryRanges([0]) == ["0"]
    assert solution.summaryRanges([0, 2, 4, 6]) == ["0", "2", "4", "6"]
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [0, 1, 2, 4, 5, 7]`

| Run start `i` | `start` | Inner loop ends at `i` | `nums[i]` | `start == nums[i]`? | Appended | `res` after |
| --- | --- | --- | --- | --- | --- | --- |
| `0` | `0` | `2` | `2` | False | `"0->2"` | `["0->2"]` |
| `3` | `4` | `4` | `5` | False | `"4->5"` | `["0->2", "4->5"]` |
| `5` | `7` | `5` | `7` | True | `"7"` | `["0->2", "4->5", "7"]` |

**Return:** `["0->2", "4->5", "7"]`

---

## 5. Complexity

* **Time:** `O(n)` — although there's a nested `while`, each element is only ever advanced past once across the outer and inner loops combined, never revisited.
* **Space:** `O(1)` extra — beyond the required output list, only `start`, `i`, and `n` are used.

---

## 6. Recall (30 seconds)

* **Anchor, then extend:** `start = nums[i]`, then grow `i` while the run of consecutive numbers continues.
* **Format rule:** `start == nums[i]` → single number; otherwise → `f"{start}->{nums[i]}"`.
* **One outer step per run:** the outer loop advances past a whole run at once, not one number at a time.
