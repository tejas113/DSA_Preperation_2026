# 34. Find First and Last Position of Element in Sorted Array

**LC 34** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Boundary Search, run twice with opposite bias

---

## 1. Intuition

With duplicates, a plain binary search can land on *any* copy of `target` — you don't know if it's the first, last, or somewhere in the middle. The fix: after finding a match, don't stop — keep searching the same side again to push toward the edge you want.

- `findBound(isFirst=True)` records `bound = mid` on a match, then narrows `right = mid - 1` — it keeps looking left for an earlier copy.
- `findBound(isFirst=False)` records `bound = mid` on a match, then narrows `left = mid + 1` — it keeps looking right for a later copy.
- Both calls reuse the exact same loop shape as [#1 Binary Search](01-binary-search.md); the only new idea is "don't return immediately on a match, remember it and keep going."
- `bound` starts at `-1` so "never matched" and "answer" share one variable with no extra flag needed.

**Recall:** call the same helper twice, once biased left (`right = mid - 1` on match) once biased right (`left = mid + 1` on match).

## 2. Approach

* **Idea:** two independent exact-match binary searches (Form 1), each with a one-line change to keep searching past the first hit instead of returning.
* **Data structure / pointers:** `left`/`right` are the usual inclusive bounds per call; `bound` is the best answer found so far in that call (`-1` until a match happens).
* **Invariant:** every time `nums[mid] == target`, `bound` is updated to the most extreme matching index seen so far in that direction; the loop keeps shrinking until no more matches can exist on that side.
* **Edge cases:**
  - Target absent → `bound` stays `-1` in both calls → `[-1, -1]`.
  - Empty array → `right = -1` from the start, loop never runs → `[-1, -1]`.
  - Single matching element → both calls converge to the same index.
  - Every element matches → first call returns index `0`, second returns `len(nums) - 1`.

## 3. Code

```python
class Solution:

    def searchRange(self, nums: list[int], target: int) -> list[int]:

        def findBound(isFirst: bool) -> int:
            left, right = 0, len(nums) - 1
            bound = -1

            while left <= right:
                mid = left + (right - left) // 2

                if nums[mid] == target:
                    bound = mid
                    if isFirst:
                        right = (
                            mid - 1
                        )  # Search left portion for earlier occurrence
                    else:
                        left = (
                            mid + 1
                        )  # Search right portion for later occurrence
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1

            return bound

        start = findBound(isFirst=True)
        end = findBound(isFirst=False)

        return [start, end]
```

## 4. Dry Run

`nums = [5, 7, 7, 8, 8, 10]`, `target = 8`

**First boundary (`isFirst=True`):**

| left | right | mid | nums[mid] | Action |
|---|---|---|---|---|
| 0 | 5 | 2 | 7 | `7 < 8` → `left = 3` |
| 3 | 5 | 4 | 8 | match, `bound = 4`, `right = 3` |
| 3 | 3 | 3 | 8 | match, `bound = 3`, `right = 2` |

Terminates (`left=3, right=2`) → `start = 3`

**Last boundary (`isFirst=False`):**

| left | right | mid | nums[mid] | Action |
|---|---|---|---|---|
| 0 | 5 | 2 | 7 | `7 < 8` → `left = 3` |
| 3 | 5 | 4 | 8 | match, `bound = 4`, `left = 5` |
| 5 | 5 | 5 | 10 | `10 > 8` → `right = 4` |

Terminates (`left=5, right=4`) → `end = 4`

Result: `[3, 4]`

## 5. Complexity

* **Time:** `O(log n)` — two sequential binary searches, each `O(log n)`; `2 · log n` is still `O(log n)`.
* **Space:** `O(1)` — each call to `findBound` uses only `left`, `right`, `mid`, `bound`.

## 6. Recall (30 seconds)

- Duplicates break plain binary search's "just return on match" — you need to keep pushing past the match toward the edge you want.
- One helper, called twice: bias left (`right = mid - 1` on match) for the first index, bias right (`left = mid + 1` on match) for the last.
- `bound = -1` doubles as "not found yet" and "not found at all" — no separate found-flag needed.
