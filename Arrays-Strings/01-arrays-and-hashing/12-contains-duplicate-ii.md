# 219. Contains Duplicate II

**LC 219** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Hash map (seen-set with an index, i.e. #1 with a distance limit)

---

## 1. Intuition

This is Contains Duplicate ([[01-contains-duplicate]]) with one more rule: the repeat has to happen within
`k` steps. You don't need every past index of a number — only the *most recent* one. If the current index
is too far from that, any earlier occurrence of the same number is even farther away, so it can never help.

* `seen = {}` maps a number to the index it was *last* seen at, not a list of all its indices.
* `if num in seen and i - seen[num] <= k` checks two things: has this number appeared before, and is that last occurrence close enough?
* `seen[num] = i` always overwrites with the newest index, whether or not the check passed — so the map only ever remembers the closest occurrence to look at next time.

**Recall:** keep `seen = {num: last_index}`; check `i - seen[num] <= k` before overwriting with the current index.

---

## 2. Approach

* **Idea:** one pass, storing only the last-seen index of each number. Overwriting on every visit keeps that index as close as possible to any future match.
* **Data structure / pointers:** `seen` maps number → its most recent index. `i` is the current index, `num` is the current value.
* **Invariant:** at the start of each iteration, `seen[num]` (if present) holds the largest index less than `i` where `num` appeared — the closest possible earlier occurrence.
* **Edge cases:**
  * `k = 0` → the condition becomes `i - seen[num] <= 0`, which can only be true if `i == seen[num]`, impossible since `seen[num] < i`; so it correctly never matches (no duplicate can be "0 apart" at two different indices).
  * Empty list, or no duplicates → `False`.
  * Duplicates farther apart than `k` → correctly skipped, and `seen[num]` still updates so a *later*, closer pair can still be caught.
  * `k` larger than `len(nums)` → equivalent to plain Contains Duplicate.

---

## 3. Code

```python
class Solution:

    def containsNearbyDuplicate(self, nums: list[int], k: int) -> bool:
        seen = {}  # Map number -> last seen index

        for i, num in enumerate(nums):
            # If seen before and within the k-distance window
            if num in seen and i - seen[num] <= k:
                return True

            # Update to the latest index
            seen[num] = i

        return False


if __name__ == "__main__":
    solution = Solution()
    assert solution.containsNearbyDuplicate([1, 2, 3, 1], 3) is True
    assert solution.containsNearbyDuplicate([1, 0, 1, 1], 1) is True
    assert solution.containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2) is False
    assert solution.containsNearbyDuplicate([1, 2, 1], 0) is False
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 2, 3, 1]`, `k = 3`

| Index `i` | `num` | `num in seen`? | `i - seen[num]` | `<= k`? | `seen` after |
| --- | --- | --- | --- | --- | --- |
| `0` | `1` | `False` | — | — | `{1: 0}` |
| `1` | `2` | `False` | — | — | `{1: 0, 2: 1}` |
| `2` | `3` | `False` | — | — | `{1: 0, 2: 1, 3: 2}` |
| `3` | `1` | `True` | `3 - 0 = 3` | `True` | — (**return `True`**) |

---

## 5. Complexity

* **Time:** `O(n)` — one pass, with `O(1)` average dict lookups and inserts.
* **Space:** `O(n)` — `seen` holds one entry per distinct number, up to `n`.

---

## 6. Recall (30 seconds)

* **Store only the last index:** `seen[num] = i`, overwritten every time — never a list of indices.
* **Check before overwrite:** `i - seen[num] <= k` — the last occurrence is the closest possible, so if it fails, no earlier one can pass either.
* **Sliding-window variant:** keep a hash *set* of the last `k` numbers, evicting `nums[i - k - 1]` as `i` grows past `k` — same result, framed as a window instead of last-seen indices.
