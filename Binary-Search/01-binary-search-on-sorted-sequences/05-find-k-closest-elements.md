# 658. Find K Closest Elements

**LC 658** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Binary search the start of a window, not a value

---

## 1. Intuition

The answer is always some contiguous window of `k` elements in the sorted array — so instead of finding `x` and expanding outward, binary search directly for *where that window should start*. A window starting at index `mid` is `arr[mid .. mid + k - 1]`; the element just outside it on the right is `arr[mid + k]`.

- Compare the window's leftmost element `arr[mid]` against the element right after the window, `arr[mid + k]` — whichever is farther from `x` tells you which element doesn't belong.
- `x - arr[mid] > arr[mid + k] - x` → `arr[mid]` is strictly farther from `x` than `arr[mid + k]` is, so the window should slide right past `mid`: `left = mid + 1`.
- Otherwise → `arr[mid]` is closer (or tied, and ties favor the smaller/leftmost value by the problem's rule), so `mid` is a valid window start: record it (`ans = mid`) and keep looking left for an even earlier valid start (`right = mid - 1`).
- `mid + k` can reach `len(arr)` when `mid` is the last possible start (`right == len(arr) - k`) — there's no element past the window to compare against, so that comparison is skipped and the window is treated as valid by default.
- Same "record + keep pushing" shape as [#3 Find First and Last Position](03-find-first-and-last-position-of-element-in-sorted-array.md) — exact-match style (`while left <= right`), remembering the best candidate seen (`ans`) instead of returning immediately.

**Recall:** binary search the window's starting index in `[0, n - k]`; on a valid start, record it in `ans` and keep pushing left for an earlier one.

## 2. Approach

* **Idea:** exact-match-style binary search (Form 1, `while left <= right`) over the possible window-start positions `[0, len(arr) - k]`, using a distance comparison between the window's edge and its right neighbor as the "condition," and remembering the best start seen in `ans`.
* **Data structure / pointers:** `left`/`right` bound the window's start index; `mid` is a candidate start; `ans` holds the best (leftmost) valid start found so far; `arr[mid]` and `arr[mid + k]` are the two values actually compared (never `x` directly against the full window).
* **Invariant:** `ans` always holds a valid window start at least as good as any seen before it; the search keeps pushing `right` left to see if an even earlier start is also valid.
* **Edge cases:**
  - `x` smaller than every element → `x - arr[mid]` is always negative, `arr[mid+k] - x` positive, so the comparison is always false and `right` shrinks toward `0` — `ans` settles on the first `k` elements.
  - `x` larger than every element → the comparison is always true, `left` grows toward `len(arr) - k` — `ans` settles on the last `k` elements.
  - `k == len(arr)` → `right = len(arr) - k = 0` from the start; the single iteration sets `ans = 0` and returns the whole array.
  - `mid` is the last possible start (`mid + k == len(arr)`) → no element exists at `arr[mid + k]` to compare against. Without a guard this indexes past the end of `arr`; guarding `mid + k < len(arr)` before the comparison treats "nothing to compare against" as "this start is valid," which is the only sound default.
  - Duplicate values → handled the same as any other comparison; ties resolve toward the smaller/earlier start since the tie falls into the `else` branch that records `ans` and keeps searching left.

## 3. Code

```python
class Solution:
    def findClosestElements(self, arr: list[int], k: int, x: int) -> list[int]:
        left = 0
        right = len(arr) - k
        ans = 0

        while left <= right:
            mid = (left + right) // 2

            # Compare the distance of the element to the left of our window
            # with the element just outside the window on the right.
            # Guard: when mid is the last possible start, mid + k == len(arr)
            # and there is no element past the window to compare against —
            # treat that as "this start is valid" rather than indexing out of range.
            if mid + k < len(arr) and x - arr[mid] > arr[mid + k] - x:
                left = mid + 1
            else:
                ans = mid  # Record the valid starting index
                right = mid - 1

        return arr[ans : ans + k]
```

> **Bug fixed:** the pasted version omitted the `mid + k < len(arr)` guard. Without it, whenever the optimal window starts at the very last valid position (`mid == len(arr) - k`), `arr[mid + k]` indexes one past the end of `arr` and raises `IndexError` — e.g. `findClosestElements([1,2,3,4,5], 4, 10)` crashes without the guard. Fuzz-testing caught this (see below); the fix just skips the comparison when there's no element to compare against, which is the only element-count-safe interpretation.

### Alternative: Max-Heap (evict the farthest element)

Doesn't use the sorted-array/window structure at all — just keeps the `k` closest elements seen so far in a size-`k` max-heap, evicting the farthest one whenever the heap overflows.

```python
import heapq

class Solution:
    def findClosestElements(self, arr: list[int], k: int, x: int) -> list[int]:
        max_heap = []

        for num in arr:
            dist = abs(num - x)
            # Push negative distance and negative value to simulate a max-heap
            # (furthest elements bubble to the top)
            heapq.heappush(max_heap, (-dist, -num))

            if len(max_heap) > k:
                heapq.heappop(max_heap)

        # Extract the elements and sort them in ascending order
        result = [-num for dist, num in max_heap]
        return sorted(result)
```

* **Why it's correct:** pushing `(-dist, -num)` turns Python's min-heap into a max-heap on `(dist, num)` — the top of the heap is always the element that is farthest from `x`, and among ties the one with the larger value (matching the problem's "prefer the smaller value on a tie" rule, since that larger value is exactly the one that should be evicted first).
* **Time:** `O(n log k)` — every element does one heap push, and overflow triggers one pop; both are `O(log k)` since the heap never holds more than `k + 1` elements. The final `sorted()` adds `O(k log k)`.
* **Space:** `O(k)` for the heap, versus `O(1)` for the binary-search version above.
* **When to prefer which:** the binary-search version is the one to use in an interview — it's `O(log(n-k) + k)`, asymptotically faster, and is the technique this topic is about. The heap version is worth knowing as a fallback that doesn't require the "answer is a contiguous window" insight, but it's strictly worse here since the array is already sorted.

## 4. Dry Run

`arr = [1, 2, 3, 4, 5]`, `k = 4`, `x = 3` (`left=0, right=5-4=1, ans=0`)

| Iteration | `left` | `right` | `mid` | `mid+k` in range? | `arr[mid]` | `arr[mid+k]` | `x-arr[mid]` | `arr[mid+k]-x` | Decision | Action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | yes (`4<5`) | 1 | 5 | 2 | 2 | `2 ≤ 2` → not farther | `ans = 0`, `right = -1` |
| End | 0 | -1 | — | — | — | — | — | — | `left > right` | return `arr[0:4] = [1,2,3,4]` |

Second example showing the guard fire, `x = 10` (`left=0, right=1, ans=0`):

| Iteration | `left` | `right` | `mid` | `mid+k` in range? | Decision | Action |
|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | yes (`4<5`) | `9 > -5` → farther | `left = 1` |
| 2 | 1 | 1 | 1 | **no** (`5 == 5`) | guard skips comparison → treat as valid | `ans = 1`, `right = 0` |
| End | 1 | 0 | — | — | `left > right` | return `arr[1:5] = [2,3,4,5]` |

## 5. Complexity

* **Time:** `O(log(n - k) + k)` — binary search over `n - k` possible start positions, plus `O(k)` to slice out the final window.
* **Space:** `O(1)` auxiliary, not counting the output slice.

## 6. Recall (30 seconds)

- The answer is always a contiguous window — binary search *where it starts*, not the elements themselves.
- Compare the window's current left edge `arr[mid]` against the element one past the window's right edge `arr[mid + k]` — but only when that element exists (`mid + k < len(arr)`).
- `x - arr[mid] > arr[mid + k] - x` → slide right (`left = mid + 1`); otherwise record `mid` as the best start so far (`ans = mid`) and keep searching left (`right = mid - 1`).
