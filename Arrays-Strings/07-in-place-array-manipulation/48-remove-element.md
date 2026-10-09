# 27. Remove Element

**LC 27** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Read/write pointer pair

---

## 1. Intuition

Removing elements in place, without extra space, means keeping two roles for one array: a fast pointer that
reads every element, and a slow pointer that only advances when something worth keeping is found. Everything
that isn't `val` gets copied forward into the next open slot; everything else is simply skipped over.

* `i` (the loop variable) is the fast/reader pointer — it always advances, checking every element.
* `index` is the slow/writer pointer — it only advances after actually writing something.
* `if nums[i] != val: nums[index] = nums[i]; index += 1` — a kept element gets copied to the next open front slot.
* When `nums[i] == val`, nothing happens — `i` moves on, but `index` (and the slots at and after it) stay untouched, ready to be overwritten by the next kept element.
* `return index` — after the scan, `index` is both the count of kept elements and the boundary marking where they end.

**Recall:** `index` only advances when a kept element is copied to `nums[index]`; `i` always advances. Return `index` as the count.

---

## 2. Approach

* **Idea:** overwrite the array from the front using only kept elements, so the array is compacted with no gaps — anything past the returned `index` no longer matters.
* **Data structure / pointers:** `i` (read pointer, scans everything), `index` (write pointer, only advances on a keep).
* **Invariant:** at every point in the loop, `nums[0:index]` holds every kept element seen so far, in their original relative order, with no `val` among them.
* **Edge cases:**
  * Empty array → the loop never runs, returns `0`.
  * Every element equals `val` → `index` never advances, returns `0`.
  * No element equals `val` → every element gets copied onto itself, `index` ends at `n`, effectively unchanged.
  * `val` values scattered throughout, including consecutive occurrences → still handled correctly, since each skip just leaves `index` in place for the next real write.

---

## 3. Code

```python
class Solution:

    def removeElement(self, nums: list[int], val: int) -> int:
        n = len(nums)
        index = 0  # Writer pointer for elements != val

        for i in range(n):
            if nums[i] != val:
                nums[index] = nums[i]
                index += 1

        return index


if __name__ == "__main__":
    solution = Solution()

    nums = [0, 1, 2, 2, 3, 0, 4, 2]
    k = solution.removeElement(nums, 2)
    assert k == 5
    assert nums[:k] == [0, 1, 3, 0, 4]

    assert solution.removeElement([], 1) == 0
    assert solution.removeElement([2, 2, 2], 2) == 0

    no_match = [1, 2, 3]
    k2 = solution.removeElement(no_match, 4)
    assert k2 == 3 and no_match[:k2] == [1, 2, 3]

    print("All tests passed")
```

### Alternative: swap-with-end (when matches are rare, order not preserved)

If `val` is expected to be rare, it can be cheaper to swap a match with the last unprocessed element and
shrink the array from the back, avoiding a write for every single kept element. This does not preserve the
original relative order of the remaining elements, which the problem allows.

---

## 4. Dry Run

`nums = [0, 1, 2, 2, 3, 0, 4, 2]`, `val = 2`

| `i` | `nums[i]` | `!= val`? | Action | `index` after | `nums[:index]` |
| --- | --- | --- | --- | --- | --- |
| `0` | `0` | True | write `nums[0] = 0` | `1` | `[0]` |
| `1` | `1` | True | write `nums[1] = 1` | `2` | `[0, 1]` |
| `2` | `2` | False | skip | `2` | `[0, 1]` |
| `3` | `2` | False | skip | `2` | `[0, 1]` |
| `4` | `3` | True | write `nums[2] = 3` | `3` | `[0, 1, 3]` |
| `5` | `0` | True | write `nums[3] = 0` | `4` | `[0, 1, 3, 0]` |
| `6` | `4` | True | write `nums[4] = 4` | `5` | `[0, 1, 3, 0, 4]` |
| `7` | `2` | False | skip | `5` | `[0, 1, 3, 0, 4]` |

**Return:** `5`, with `nums[:5] == [0, 1, 3, 0, 4]`

---

## 5. Complexity

* **Time:** `O(n)` — a single pass; `i` visits every element exactly once.
* **Space:** `O(1)` — everything happens in place.

---

## 6. Recall (30 seconds)

* **Two roles, one array:** `i` reads everything, `index` only advances on a keep.
* **Write only on keep:** `if nums[i] != val: nums[index] = nums[i]; index += 1`.
* **Return `index`:** it's both the count of kept elements and the boundary of the valid prefix.
