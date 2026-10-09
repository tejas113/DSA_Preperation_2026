# 239. Sliding Window Maximum

**LC 239** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Monotonic deque

---

## 1. Intuition

Re-scanning each window of size `k` for its max would be `O(n·k)`. Instead, keep a deque that's always sorted
from largest (front) to smallest (back) — then the max of the current window is always sitting at the front,
free to read. The trick is maintaining that order cheaply: any value smaller than the one just arriving can
never become the max of a *future* window either (the new, larger value will always outlast it), so it's
safe to throw those smaller values away immediately.

* `while q and q[-1] < nums[r]: q.pop()` clears out everything at the back that's smaller than the incoming value — those values are now useless, since `nums[r]` is both bigger and will leave the window later.
* `q.append(nums[r])` adds the new value once the deque's back is no longer smaller than it.
* `if (r + 1) >= k` — only start recording answers once the window has actually reached size `k`.
* `if nums[l] == q[0]: q.popleft()` — if the value about to leave the window (`nums[l]`) is the one currently at the front, remove it; otherwise it was already discarded earlier by the popping step above, so there's nothing to do.

**Recall:** keep the deque strictly decreasing by popping smaller values from the back before adding; the max is always `q[0]`; pop the front only if it equals the value falling out of the window.

---

## 2. Approach

* **Idea:** maintain a deque of "candidates that could still become a future window's max," discarding anything that's provably useless the moment a bigger value shows up.
* **Data structure / pointers:** `q` (the monotonic deque of values), `output` (one max per completed window), `l`/`r` (window bounds).
* **Invariant:** `q` is always sorted from largest to smallest, front to back, and among equal values the earliest-seen one sits closer to the front (since ties are never popped — only strictly smaller values are). This guarantees the front of `q` is always both the window's max *and* the earliest surviving index holding that value.
* **Edge cases:**
  * `k == 1` → every element is its own window's max; nothing ever gets popped as smaller before it's recorded.
  * `k == len(nums)` → one window, one answer, the true max of the whole array.
  * Duplicate values (like `[4, 4, 4]`) → still correct: because ties are never popped from the back, the front of the deque always corresponds to the *oldest* surviving index of the max value — exactly the one that will expire first, so comparing by value (not index) still identifies the right entry to remove.
  * Strictly decreasing input → no back-pops ever happen (each new value is smaller than the last, not larger), so the deque fills up to size `k` and then stays there, evicting exactly one value from the front each step once the window is full.
  * Strictly increasing input → the deque collapses to size `1` at every step, since each new value is larger than everything before it and pops the entire back of the deque.

---

## 3. Code

```python
from collections import deque


class Solution:

    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        q = deque()
        output = []
        l, r = 0, 0

        while r < len(nums):
            while q and q[-1] < nums[r]:
                q.pop()
            q.append(nums[r])

            if (r + 1) >= k:
                output.append(q[0])

                if nums[l] == q[0]:
                    q.popleft()
                l += 1
            r += 1
        return output


if __name__ == "__main__":
    solution = Solution()
    assert solution.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert solution.maxSlidingWindow([1], 1) == [1]
    assert solution.maxSlidingWindow([4, 4, 4], 2) == [4, 4]
    assert solution.maxSlidingWindow([9, 8, 7, 6], 2) == [9, 8, 7]
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`

| `r` | `nums[r]` | `q` after | Window active (`r+1 >= k`)? | `q[0]` (max) | `output` after | Front popped? | `l` after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0` | `1` | `[1]` | No | — | `[]` | — | `0` |
| `1` | `3` | `[3]` (popped `1`) | No | — | `[]` | — | `0` |
| `2` | `-1` | `[3, -1]` | Yes | `3` | `[3]` | `1 != 3` → no | `1` |
| `3` | `-3` | `[3, -1, -3]` → `[-1, -3]` | Yes | `3` then popped | `[3, 3]` | `3 == 3` → **yes** | `2` |
| `4` | `5` | `[5]` (popped `-1, -3`) | Yes | `5` | `[3, 3, 5]` | `-1 != 5` → no | `3` |
| `5` | `3` | `[5, 3]` | Yes | `5` | `[3, 3, 5, 5]` | `-3 != 5` → no | `4` |
| `6` | `6` | `[6]` (popped `5, 3`) | Yes | `6` | `[3, 3, 5, 5, 6]` | `5 != 6` → no | `5` |
| `7` | `7` | `[7]` (popped `6`) | Yes | `7` | `[3, 3, 5, 5, 6, 7]` | `3 != 7` → no | `6` |

**Return:** `[3, 3, 5, 5, 6, 7]`

---

## 5. Complexity

* **Time:** `O(n)` — each value is pushed onto `q` exactly once and popped at most once (either from the back, as a discarded smaller value, or from the front, when its window expires), so total deque operations are bounded by `2n`.
* **Space:** `O(k)` — the deque never holds more than `k` values, since anything outside the current window has either been popped as smaller or expired from the front.

---

## 6. Recall (30 seconds)

* **Monotonic decreasing deque:** front is always the current window's max.
* **Discard smaller values immediately:** `while q[-1] < nums[r]: pop()` — a smaller value that arrived earlier can never win against a bigger one that arrives later and outlasts it.
* **Expire from the front only when it matches:** `if nums[l] == q[0]: popleft()` — safe even with duplicates, because ties are never popped early, so the front is always the oldest surviving index of the max value.
