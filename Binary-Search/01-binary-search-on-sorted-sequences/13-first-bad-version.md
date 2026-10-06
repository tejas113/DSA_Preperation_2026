# 278. First Bad Version

**LC 278** · **Source:** [+] Claude · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Boundary Search (yes/no condition instead of a value)

---

## 1. Intuition

Versions form `[good, good, ..., bad, bad, ..., bad]` — a monotonic sequence of booleans. This is the same boundary search as [#2 Search Insert Position](02-search-insert-position.md), except the thing you compare at `mid` isn't `nums[mid] < target`, it's a yes/no call to `isBadVersion(mid)`.

- `isBadVersion(mid)` is `True` → `mid` might be the *first* bad one, so keep it in range: `right = mid`.
- `isBadVersion(mid)` is `False` → `mid` and everything before it is good, so the first bad version is strictly after: `left = mid + 1`.
- Loop with `while left < right` (not `<=`) because `right = mid` must still be reachable — `mid` is never provably eliminated the way it is in exact-match search.
- When `left == right`, that index is the first bad version.

**Recall:** boundary search where the "condition" is an API call instead of a comparison; `isBadVersion(mid) → right = mid`, else `left = mid + 1`.

## 2. Approach

* **Idea:** Form 2 (boundary search) from the README, applied to a predicate function instead of an array value.
* **Data structure / pointers:** `left`/`right` are 1-indexed version numbers (`right` starts at `n`, not `n - 1`, since `hi = mid` needs `right` to represent "could still be the answer," matching the `while left < right` form); `mid` is the version being tested.
* **Invariant:** every version `< left` is known good; every version `>= right` is known bad (or is `right` itself, still a candidate). The first bad version always lies in `[left, right]`.
* **Edge cases:**
  - `n = 1` → `left == right` from the start, loop body never runs, no API call needed, returns `1`.
  - First version is bad → `right` shrinks every iteration until it reaches `1`.
  - Last version is bad → `left` grows every iteration until it reaches `n`.

## 3. Code

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:


class Solution:

    def firstBadVersion(self, n: int) -> int:
        left, right = 1, n

        while left < right:
            mid = left + (right - left) // 2

            if isBadVersion(mid):
                right = (
                    mid  # mid could be the first bad version; include it in range
                )
            else:
                left = (
                    mid + 1
                )  # mid is good; first bad version must be after mid

        return left
```

## 4. Dry Run

`n = 5`, `bad = 4`

| Iteration | `left` | `right` | `mid` | `isBadVersion(mid)` | Action |
|---|---|---|---|---|---|
| 1 | 1 | 5 | 3 | `False` | `left = 4` |
| 2 | 4 | 5 | 4 | `True` | `right = 4` |
| End | 4 | 4 | — | — | `left == right`, return `4` |

## 5. Complexity

* **Time:** `O(log n)` — one `isBadVersion` call per iteration, and the `[left, right]` range halves each time, so at most `log₂ n` calls total.
* **Space:** `O(1)` — only `left`, `right`, `mid`.

## 6. Recall (30 seconds)

- Same boundary-search shape as insert position, but the "is this true?" test is an API call, not a value comparison.
- `while left < right`, and on `True` do `right = mid` (keep `mid` as a candidate) — never `mid - 1` here.
- `n = 1` needs zero API calls: the loop condition itself skips the body.
