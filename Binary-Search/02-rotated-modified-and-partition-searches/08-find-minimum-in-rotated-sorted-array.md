# 153. Find Minimum in Rotated Sorted Array

**LC 153** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Compare `mid` with the right end; the minimum is on the side with the drop

---

## 1. Intuition

The minimum element is exactly the rotation point — the one spot where a bigger value sits right before a smaller one. Two checks locate it: first, is the *whole remaining range* already a clean ascending run (no rotation point left inside it)? If so, its first element is the minimum. If not, check whether the *left half* up to `mid` is clean — that tells you which side still hides the rotation point.

- `nums[left] <= nums[right]` → the current `[left, right]` segment has no rotation point left inside it (it's already sorted), so its smallest value is simply `nums[left]` — return it immediately.
- Otherwise, a rotation point exists somewhere in `[left, right]`. Compute `mid` and check the left half: `nums[left] <= nums[mid]` → the left half `[left, mid]` is itself a clean ascending run, so the drop must be strictly after `mid`. Move `left = mid + 1`.
- `nums[left] > nums[mid]` → the left half already contains the drop, so the minimum is at `mid` or somewhere to its left. Keep `mid` in play: `right = mid`.
- Same boundary-search shape as [#3 Find First and Last Position](../01-binary-search-on-sorted-sequences/03-find-first-and-last-position-of-element-in-sorted-array.md) — narrowing `[left, right]` until the minimum is pinned down — just with an early-exit fast path for already-sorted segments.

**Recall:** if `nums[left] <= nums[right]`, the segment is already sorted — return `nums[left]`. Otherwise compare `nums[left]` to `nums[mid]` to tell which half still hides the rotation point.

## 2. Approach

* **Idea:** boundary search with an early-exit check — "is this whole segment already sorted?" — before falling back to comparing the left half's endpoints to decide which half to keep.
* **Data structure / pointers:** `left`/`right` bound the search range; `mid` is computed only when the segment isn't already sorted, and is compared against `nums[left]` (not `nums[right]`) to test whether the left half is clean.
* **Invariant:** the minimum is always within `[left, right]`; `nums[left] <= nums[mid]` proves the left half `[left, mid]` is sorted and therefore can't contain the drop, so it's safe to move past it entirely (`left = mid + 1`).
* **Edge cases:**
  - Unrotated array → `nums[left] <= nums[right]` is true on the very first check, returning `nums[0]` with zero iterations of the halving logic.
  - Single element → `left == right`, so `nums[left] <= nums[right]` is trivially true (`nums[0] <= nums[0]`), returns `nums[0]` immediately.
  - Two elements → either sorted (`nums[0] <= nums[1]`, returns `nums[0]`) or rotated (`nums[0] > nums[1]`, falls through to `mid = left`, `nums[left] <= nums[mid]` is trivially true since `mid == left`, so `left = mid + 1`, then the next loop's sorted-check returns `nums[1]`).

## 3. Code

```python
class Solution:
    def findMin(self, nums: list[int]) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            # Check if the subsegment is already sorted
            if nums[left] <= nums[right]:
                return nums[left]

            mid = left + (right - left) // 2

            # If the left half is sorted, the minimum must be in the right half
            if nums[left] <= nums[mid]:
                left = mid + 1
            else:
                # Otherwise, the minimum is in the left half (including mid)
                right = mid

        return nums[left]
```

## 4. Dry Run

`nums = [4, 5, 6, 7, 0, 1, 2]`

| Iteration | `left` | `right` | `nums[left] <= nums[right]`? | `mid` | `nums[left]` | `nums[mid]` | Left half sorted? | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | `4 <= 2`? No | 3 | 4 | 7 | `4 <= 7` yes | `left = 4` |
| 2 | 4 | 6 | `0 <= 2`? **Yes** | — | — | — | — | return `nums[4] = 0` |

## 5. Complexity

* **Time:** `O(log n)` — each iteration either returns immediately or halves `[left, right]`, same as any boundary search.
* **Space:** `O(1)` — only `left`, `right`, `mid`.

## 6. Recall (30 seconds)

- First ask "is this segment already sorted?" (`nums[left] <= nums[right]`) — if yes, `nums[left]` is the answer, done.
- If not, the rotation point is somewhere inside — check if the *left* half up to `mid` is sorted (`nums[left] <= nums[mid]`): if yes, the drop is past `mid` (`left = mid + 1`); if no, the drop is at or before `mid` (`right = mid`).
- This version compares `nums[left]` to `nums[mid]`, not `nums[mid]` to `nums[right]` — a different but equally valid way to find which half hides the rotation point.
