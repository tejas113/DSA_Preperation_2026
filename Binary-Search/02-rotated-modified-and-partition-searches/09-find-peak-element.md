# 162. Find Peak Element

**LC 162** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Move uphill — compare `nums[mid]` with its neighbor, not with a target

---

## 1. Intuition

The array isn't sorted at all, but it doesn't need to be: the problem only asks for *any* peak, and treating the boundaries as `-∞` guarantees one always exists. Looking at the local slope at `mid` — is it still climbing, or has it started descending? — always points toward a peak.

- `nums[mid] < nums[mid + 1]` → still climbing, so a peak is guaranteed somewhere to the right (the climb either keeps going to the edge, which is a peak since the boundary is `-∞`, or it turns into a descent, which creates one). Move `left = mid + 1`.
- `nums[mid] >= nums[mid + 1]` → already descending (or flat, but the problem guarantees no equal neighbors), so a peak is at `mid` or to its left. Keep `mid` as a candidate: `right = mid`.
- Same boundary-search shape as [#8 Find Minimum in Rotated Sorted Array](08-find-minimum-in-rotated-sorted-array.md) — `while left < right`, `right = mid` to keep a candidate, `left = mid + 1` to discard one — just with a slope comparison instead of a rotation-point comparison.

**Recall:** always step toward the side that's still increasing; the uphill direction is guaranteed to lead to a peak.

## 2. Approach

* **Idea:** boundary search (Form 2) where the "condition" is "has the slope turned downward by `mid`?" — never compares against a target value at all.
* **Data structure / pointers:** `left`/`right` bound the search range; `mid` is compared only to its immediate right neighbor `nums[mid + 1]`.
* **Invariant:** a peak always exists within `[left, right]`; every step either confirms the right side still has a guaranteed peak (ascending) or confirms `mid` itself is a valid candidate (descending).
* **Edge cases:**
  - Single element → `left == right` from the start, loop body never runs, returns index `0` (trivially a peak since both neighbors are `-∞`).
  - Strictly increasing → `nums[mid] < nums[mid + 1]` always holds, `left` climbs to the last index.
  - Strictly decreasing → the condition is never true, `right` drops to index `0`.
  - Multiple peaks exist (e.g. `[1,2,1,3,5,6,4]` has peaks at index 1 and 5) → the algorithm returns whichever one the slope-following path leads to; any valid peak is an accepted answer.

## 3. Code

```python
class Solution:

    def findPeakElement(self, nums: list[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            # If middle element is smaller than the next element,
            # we are on an ascending slope, so a peak exists to the right.
            if nums[mid] < nums[mid + 1]:
                left = mid + 1

            # Otherwise, we are on a descending slope,
            # so a peak exists at mid or to its left.
            else:
                right = mid

        return left
```

### Alternative: check both neighbours (exact-match loop form)

Same "walk toward the larger neighbour" idea, but written in Form 1 (`while left <= right`, `mid ± 1`): `mid` is tested as a peak directly, and discarded when a neighbour beats it.

```python
class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            # Check if left neighbor is greater
            if mid > 0 and nums[mid - 1] > nums[mid]:
                right = mid - 1
            # Check if right neighbor is greater
            elif mid < len(nums) - 1 and nums[mid + 1] > nums[mid]:
                left = mid + 1
            else:
                return mid  # neither neighbor is greater → mid is a peak

        return -1  # unreachable for a non-empty array
```

* **Why it's correct:** if a neighbour is greater, `mid` is not a peak, so it can be dropped (`mid ± 1`), and a peak is guaranteed on the side of the greater neighbour (the climb either reaches an edge, which counts as a peak because the boundary is `-∞`, or turns into a descent). If neither neighbour is greater, `mid` is a peak and is returned immediately. The `mid > 0` / `mid < len(nums) - 1` guards treat a missing neighbour as `-∞`.
* **Loop form:** `right = mid - 1` pairs with `while left <= right`. The primary solution uses `right = mid` with `while left < right`; never mix the two.
* **Trade-off:** it can return early (as soon as `mid` is a peak), but it does up to two comparisons per step and needs index guards. The primary version has one comparison, no guards (`mid + 1` is always valid since `mid < right`), and no unreachable `return -1`.
* **Time / Space:** `O(log n)` / `O(1)`, same as the primary solution.
* **Trace:** `[1, 2, 1, 3, 5, 6, 4]` → `mid = 3` (value 3): right neighbour 5 is greater → `left = 4`; `mid = 5` (value 6): neither neighbour is greater → return `5`.

## 4. Dry Run

`nums = [1, 2, 1, 3, 5, 6, 4]`

| Iteration | `left` | `right` | `mid` | `nums[mid]` | `nums[mid+1]` | Slope | Action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 3 | 5 | ascending | `left = 4` |
| 2 | 4 | 6 | 5 | 6 | 4 | descending | `right = 5` |
| 3 | 4 | 5 | 4 | 5 | 6 | ascending | `left = 5` |
| End | 5 | 5 | — | — | — | `left == right` | return index `5` (`nums[5] = 6`) |

## 5. Complexity

* **Time:** `O(log n)` — the `[left, right]` range halves every iteration.
* **Space:** `O(1)` — only `left`, `right`, `mid`.

## 6. Recall (30 seconds)

- No sortedness needed — just compare `nums[mid]` to its right neighbor and walk uphill.
- Ascending at `mid` → peak guaranteed to the right, move `left = mid + 1`.
- Descending (or equal, though the problem forbids ties) at `mid` → `mid` is a valid candidate, keep it with `right = mid`.
