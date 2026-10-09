# 26. Remove Duplicates from Sorted Array

**LC 26** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Read/write pointer pair, on sorted data

---

## 1. Intuition

Because the array is sorted, every duplicate of a value sits right next to it — no duplicate can hide far
away. That means comparing a candidate only against the *last kept* value is enough to tell if it's new. Two
pointers do this in one pass: `writer_ptr` marks the last unique value placed, `reader_ptr` scans ahead
looking for the next one.

* `writer_ptr = 0` starts assuming `nums[0]` is already a unique value worth keeping (it always is, since there's nothing before it).
* `reader_ptr` starts at `1`, scanning every element after the first.
* `if nums[reader_ptr] != nums[writer_ptr]` — the reader found a genuinely new value (not equal to the last *kept* one), so it's worth keeping.
* `writer_ptr += 1; nums[writer_ptr] = nums[reader_ptr]` — advance the writer and copy the new value into the next slot.
* `return writer_ptr + 1` — `writer_ptr` is the *index* of the last kept element, so the count of unique elements is one more than that.

**Recall:** compare each new element only to `nums[writer_ptr]` (the last kept value); on a mismatch, advance `writer_ptr` and copy it in. Return `writer_ptr + 1`.

---

## 2. Approach

* **Idea:** sortedness guarantees duplicates are always adjacent, so a single running "last kept value" is enough to detect every new unique value — no need to remember the whole set of values seen so far.
* **Data structure / pointers:** `writer_ptr` (index of the last unique value kept so far), `reader_ptr` (scans forward looking for the next one).
* **Invariant:** at every point, `nums[0:writer_ptr+1]` holds every distinct value seen so far, in sorted order, with no duplicates — and `nums[writer_ptr]` is always the most recently kept value.
* **Edge cases:**
  * Single-element array → `range(1, 1)` never runs, returns `1` (the one element is trivially unique).
  * All elements distinct → `writer_ptr` advances on every step, ending at `len(nums) - 1`, so the return is `len(nums)`.
  * All elements identical → the `if` condition never triggers, `writer_ptr` stays `0`, returns `1`.
  * Duplicates only need to be compared against the immediately preceding *kept* value, not every earlier occurrence — this only works because the array is sorted.

---

## 3. Code

```python
class Solution:

    def removeDuplicates(self, nums: list[int]) -> int:
        writer_ptr = 0

        # Scan the array starting from index 1
        for reader_ptr in range(1, len(nums)):
            # Found a new unique element
            if nums[reader_ptr] != nums[writer_ptr]:
                writer_ptr += 1
                nums[writer_ptr] = nums[reader_ptr]

        return writer_ptr + 1


if __name__ == "__main__":
    solution = Solution()

    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = solution.removeDuplicates(nums)
    assert k == 5
    assert nums[:k] == [0, 1, 2, 3, 4]

    assert solution.removeDuplicates([1]) == 1
    assert solution.removeDuplicates([1, 2, 3]) == 3
    assert solution.removeDuplicates([1, 1, 1]) == 1

    print("All tests passed")
```

---

## 4. Dry Run

`nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`

| `reader_ptr` | `nums[reader_ptr]` | vs `nums[writer_ptr]` | Action | `writer_ptr` after | `nums[:writer_ptr+1]` |
| --- | --- | --- | --- | --- | --- |
| `1` | `0` | equal (`0`) | skip | `0` | `[0]` |
| `2` | `1` | not equal (`0`) | advance + write | `1` | `[0, 1]` |
| `3` | `1` | equal (`1`) | skip | `1` | `[0, 1]` |
| `4` | `1` | equal (`1`) | skip | `1` | `[0, 1]` |
| `5` | `2` | not equal (`1`) | advance + write | `2` | `[0, 1, 2]` |
| `6` | `2` | equal (`2`) | skip | `2` | `[0, 1, 2]` |
| `7` | `3` | not equal (`2`) | advance + write | `3` | `[0, 1, 2, 3]` |
| `8` | `3` | equal (`3`) | skip | `3` | `[0, 1, 2, 3]` |
| `9` | `4` | not equal (`3`) | advance + write | `4` | `[0, 1, 2, 3, 4]` |

**Return:** `writer_ptr + 1 = 5`, with `nums[:5] == [0, 1, 2, 3, 4]`

---

## 5. Complexity

* **Time:** `O(n)` — a single pass; `reader_ptr` visits every element once.
* **Space:** `O(1)` — everything happens in place.

---

## 6. Recall (30 seconds)

* **Compare to the last kept value, not the whole history:** `nums[reader_ptr] != nums[writer_ptr]` is enough because sortedness groups all duplicates together.
* **Advance-then-write:** `writer_ptr += 1` before `nums[writer_ptr] = nums[reader_ptr]`.
* **Return `writer_ptr + 1`:** the count is one more than the last kept index.
* **Generalizes to LC 80** (allow up to 2 duplicates): compare `nums[reader_ptr]` against `nums[writer_ptr - 1]` instead.
