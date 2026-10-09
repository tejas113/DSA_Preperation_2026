# 80. Remove Duplicates from Sorted Array II

**LC 80** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Read/write pointer pair, generalized to "at most K duplicates"

---

## 1. Intuition

Remove Duplicates I ([[49-remove-duplicates-from-sorted-array]]) allows each value once, so comparing a new
element to the *last kept* value (`nums[writer - 1]`) is enough to detect a repeat. Allowing up to two copies
means the check has to look one slot further back: a new element is safe to keep as long as it doesn't match
what was written *two* slots ago (`nums[writer - 2]`) — if it did, keeping it would create a third copy in a
row.

* `writer = 2` — the first two elements are always safe to keep, since two copies of anything is allowed.
* `for reader in range(2, len(nums))` starts scanning from the third element onward.
* `if nums[reader] != nums[writer - 2]` — comparing against `writer - 2`, not `writer - 1`, is exactly what allows a *second* copy of a value to survive while still blocking a third.
* When the check passes, `nums[writer] = nums[reader]; writer += 1` copies the value forward and advances the write position; when it fails, the element is simply skipped.

**Recall:** compare each new element to `nums[writer - 2]` (not `writer - 1`); keep it and advance `writer` only if it differs — this is what allows exactly two copies of any value through.

---

## 2. Approach

* **Idea:** generalize the "compare to the last kept value" trick from Remove Duplicates I by comparing further back — checking `writer - K` allows up to `K` copies of any value to survive.
* **Data structure / pointers:** `writer` (next write position, and also defines how many elements have been kept so far), `reader` (scans forward looking for the next keepable element).
* **Invariant:** at every point, `nums[0:writer]` holds a valid prefix where no value appears more than twice, and it matches what the final answer's prefix would be given everything read so far.
* **Edge cases:**
  * `len(nums) <= 2` → nothing can violate the "at most 2" rule yet, so the array is returned unchanged, guarded explicitly before the loop even starts.
  * All elements identical (`[1,1,1,1]`) → only the first two are ever kept; every later comparison against `nums[writer - 2]` (which stays `1`) fails, so `writer` never advances past `2`.
  * No duplicates at all (`[1,2,3,4]`) → every comparison passes, and the array is effectively unchanged, `writer` reaching `len(nums)`.
  * Generalizes directly to "allow at most K duplicates" by starting `writer` at `K` and comparing against `nums[writer - K]` instead of `nums[writer - 2]`.

---

## 3. Code

```python
class Solution:

    def removeDuplicates(self, nums: list[int]) -> int:
        if len(nums) <= 2:
            return len(nums)

        writer = 2  # First two elements are always valid

        for reader in range(2, len(nums)):
            # Check if current element differs from the element 2 slots behind writer
            if nums[reader] != nums[writer - 2]:
                nums[writer] = nums[reader]
                writer += 1

        return writer


if __name__ == "__main__":
    solution = Solution()

    nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]
    k = solution.removeDuplicates(nums)
    assert k == 7
    assert nums[:k] == [0, 0, 1, 1, 2, 3, 3]

    assert solution.removeDuplicates([1, 1, 1, 1]) == 2
    assert solution.removeDuplicates([1, 2, 3, 4]) == 4
    assert solution.removeDuplicates([]) == 0
    assert solution.removeDuplicates([1]) == 1

    print("All tests passed")
```

---

## 4. Dry Run

`nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]`

| `reader` | `nums[reader]` | vs `nums[writer - 2]` | Passes? | Action | `writer` after |
| --- | --- | --- | --- | --- | --- |
| `2` | `1` | `nums[0] = 0` | `1 != 0` → Yes | write `nums[2] = 1` | `3` |
| `3` | `1` | `nums[1] = 0` | `1 != 0` → Yes | write `nums[3] = 1` | `4` |
| `4` | `1` | `nums[2] = 1` | `1 == 1` → No | skip (3rd copy) | `4` |
| `5` | `1` | `nums[2] = 1` | `1 == 1` → No | skip (4th copy) | `4` |
| `6` | `2` | `nums[2] = 1` | `2 != 1` → Yes | write `nums[4] = 2` | `5` |
| `7` | `3` | `nums[3] = 1` | `3 != 1` → Yes | write `nums[5] = 3` | `6` |
| `8` | `3` | `nums[4] = 2` | `3 != 2` → Yes | write `nums[6] = 3` | `7` |

**Return:** `7`, with `nums[:7] == [0, 0, 1, 1, 2, 3, 3]`

---

## 5. Complexity

* **Time:** `O(n)` — a single pass; `reader` visits every element once.
* **Space:** `O(1)` — everything happens in place.

---

## 6. Recall (30 seconds)

* **Look back `K` slots, not 1:** comparing against `nums[writer - 2]` (instead of `writer - 1`) is what allows exactly two copies through.
* **`writer` starts at `2`:** the first two elements never need checking, since two copies is always allowed.
* **Generalizes to any K:** start `writer` at `K`, compare against `nums[writer - K]`.
