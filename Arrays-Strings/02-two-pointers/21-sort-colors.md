# 75. Sort Colors

**LC 75** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Three-way partition (Dutch National Flag)

---

## 1. Intuition

There are only three possible values, so you don't need a general sort — you need to *partition* the array
into three zones: `0`s at the front, `1`s in the middle, `2`s at the back. Three pointers carve out those
zones as you scan once: `l` is the next open slot for a `0`, `r` is the next open slot for a `2`, and `i` is
the scanner walking through the unknown middle.

* `nums[i] == 0` → this belongs at the front, so swap it to `l` and advance both — the value it displaced into `i` is already known to be a `1` (everything between `l` and `i` was already confirmed `1`), so `i` can safely move on too.
* `nums[i] == 2` → this belongs at the back, so swap it to `r` and pull `r` in — but the value swapped *into* `i` came from the unexplored tail end and hasn't been checked yet, so `i` must **not** move yet.
* `nums[i] == 1` → already in the right zone, just advance `i`.

**Recall:** three pointers (`l`, `i`, `r`); on `0` swap-with-`l` and advance both; on `2` swap-with-`r` and only pull `r` in; on `1` just advance `i`.

---

## 2. Approach

* **Idea:** a single left-to-right scan that swaps misplaced `0`s and `2`s into their zones as soon as they're found, without knowing the final counts in advance.
* **Data structure / pointers:** `l` — everything before it is a confirmed `0`. `r` — everything after it is a confirmed `2`. `i` — the current scanner; everything between `l` and `i` is a confirmed `1`.
* **Invariant:** at every step, `nums[:l]` is all `0`s, `nums[r+1:]` is all `2`s, and `nums[l:i]` is all `1`s. Only `nums[i:r+1]` is still unknown.
* **Edge cases:**
  * Empty array → `l = 0`, `r = -1`, so `i <= r` is `False` immediately; nothing to do.
  * Already sorted (`[0,0,1,1,2,2]`) → still correct, just fewer swaps trigger.
  * All the same value → `l`/`i` or `i`/`r` advance together without needing any real swap work.
  * A `0` swapped from `l` into `i`: since everything in `nums[l:i]` was already known to be `1` (by the invariant), the value now at `i` after the swap is a `1`, so it's safe for `i` to advance — this is the subtle part interviewers probe on.

---

## 3. Code

```python
class Solution:

    def sortColors(self, nums: list[int]) -> None:
        """Do not return anything, modify nums in-place instead."""
        l, r = 0, len(nums) - 1
        i = 0

        while i <= r:
            if nums[i] == 0:
                nums[l], nums[i] = nums[i], nums[l]
                l += 1
                i += 1
            elif nums[i] == 2:
                nums[r], nums[i] = nums[i], nums[r]
                r -= 1
                # Do NOT increment i here; the swapped element at index i needs to be evaluated.
            else:  # nums[i] == 1
                i += 1


if __name__ == "__main__":
    solution = Solution()

    def check(nums: list[int]) -> None:
        expected = sorted(nums)
        solution.sortColors(nums)
        assert nums == expected, (nums, expected)

    check([2, 0, 2, 1, 1, 0])
    check([2, 0, 1])
    check([0])
    check([])
    check([1, 1, 1])
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [2, 0, 2, 1, 1, 0]`, `l = 0`, `r = 5`, `i = 0`

| Step | `i` | `l` | `r` | `nums[i]` | Action | Array after |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `0` | `0` | `5` | `2` | swap with `r`, `r -= 1` (`i` stays) | `[0, 0, 2, 1, 1, 2]` |
| **2** | `0` | `0` | `4` | `0` | swap with `l`, `l += 1`, `i += 1` | `[0, 0, 2, 1, 1, 2]` |
| **3** | `1` | `1` | `4` | `0` | swap with `l`, `l += 1`, `i += 1` | `[0, 0, 2, 1, 1, 2]` |
| **4** | `2` | `2` | `4` | `2` | swap with `r`, `r -= 1` (`i` stays) | `[0, 0, 1, 1, 2, 2]` |
| **5** | `2` | `2` | `3` | `1` | `i += 1` | `[0, 0, 1, 1, 2, 2]` |
| **6** | `3` | `2` | `3` | `1` | `i += 1` → `i = 4 > r = 3`, stop | `[0, 0, 1, 1, 2, 2]` |

**Final:** `[0, 0, 1, 1, 2, 2]`

---

## 5. Complexity

* **Time:** `O(n)` — each element is looked at a bounded number of times (at most twice: once as `nums[i]`, and possibly once more after being swapped in from `r`), so the total work is linear.
* **Space:** `O(1)` — three index variables, all swaps done in place.

---

## 6. Recall (30 seconds)

* **Three pointers, three zones:** `l` (front of `0`s), `i` (scanner), `r` (back of `2`s).
* **The `2` trap:** after swapping with `r`, do **not** advance `i` — the newly swapped-in value is unexamined.
* **Stop condition:** `i > r`, i.e. the unknown middle zone has shrunk to nothing.
